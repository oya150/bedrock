"""Elasticsearch 14편: 노드 3개 클러스터에서 주 샤드·복제본·시퀀스 번호·체크포인트를 들여다본다.

준비: lab/es/14_compose.yml 로 노드 3개를 띄운다(es01:9211, es02:9212, es03:9213).
실행:
  python lab/es/14_es.py setup          # 주 샤드 1개 + 복제본 2개 인덱스를 만들고 100건 쓴다
  python lab/es/14_es.py show           # 샤드가 어느 노드에 있고 체크포인트가 어디인지 본다
  python lab/es/14_es.py write 10       # 10건 더 쓰고 응답의 _seq_no·_primary_term 을 본다
주 샤드가 있는 노드를 멈춘 뒤(docker compose stop esNN) show 와 write 를 다시 해 본다.
"""
import json
import os
import sys
import urllib.error
import urllib.request

PORTS = os.environ.get("ES_PORTS", "9211,9212,9213").split(",")
IDX = "orders14"


def call(method, path, body=None):
    # 살아 있는 노드 아무 데나 보낸다
    last = None
    for p in PORTS:
        req = urllib.request.Request(f"http://127.0.0.1:{p}{path}", method=method,
                                     data=json.dumps(body).encode() if body is not None else None,
                                     headers={"Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=40) as r:
                return json.loads(r.read() or b"{}")
        except urllib.error.HTTPError as e:
            return {"error_status": e.code, "error": json.loads(e.read() or b"{}").get("error", {}).get("type")}
        except OSError as e:
            last = e
    raise SystemExit(f"살아 있는 노드가 없어요: {last}")


def count():
    call("POST", f"/{IDX}/_refresh")
    return call("GET", f"/{IDX}/_count").get("count")


def setup():
    call("DELETE", f"/{IDX}")
    call("PUT", f"/{IDX}", {"settings": {"number_of_shards": 1, "number_of_replicas": 2}})
    call("GET", f"/_cluster/health/{IDX}?wait_for_status=green&timeout=30s")
    write(100, quiet=True)
    show()


def write(n, quiet=False):
    start = count() or 0
    for i in range(start, start + n):
        r = call("PUT", f"/{IDX}/_doc/{i}", {"item": f"주문{i}"})
        if not quiet:
            print(f"  doc {i}: _seq_no {r.get('_seq_no')}, _primary_term {r.get('_primary_term')}, "
                  f"샤드 {r.get('_shards')}" if "_seq_no" in r else f"  doc {i}: {r}")


def show():
    nodes = {k: v["name"] for k, v in call("GET", "/_nodes/_local,_all")["nodes"].items()}
    master = call("GET", "/_cluster/state/master_node").get("master_node")
    health = call("GET", f"/_cluster/health/{IDX}")
    print(f"마스터 {nodes.get(master, master)}, 인덱스 상태 {health.get('status')}, 문서 {count()}건")
    st = call("GET", f"/{IDX}/_stats?level=shards")
    for copy in st["indices"][IDX]["shards"]["0"]:
        seq = copy["seq_no"]
        role = "주 샤드" if copy["routing"]["primary"] else "복제본"
        print(f"  {nodes.get(copy['routing']['node'])}: {role}  최대 번호 {seq['max_seq_no']}, "
              f"로컬 체크포인트 {seq['local_checkpoint']}, 글로벌 체크포인트 {seq['global_checkpoint']}")
    meta = call("GET", f"/_cluster/state/metadata/{IDX}")["metadata"]["indices"][IDX]
    print(f"  primary term {meta['primary_terms']['0']}, in-sync 사본 수(주 샤드 포함) {len(meta['in_sync_allocations']['0'])}")
    vc = call("GET", "/_cluster/state/metadata?filter_path=metadata.cluster_coordination")
    cc = vc["metadata"]["cluster_coordination"]
    print(f"  투표 구성(마스터 후보 node id) {len(cc['last_committed_config'])}개")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "show"
    if cmd == "setup":
        setup()
    elif cmd == "write":
        write(int(sys.argv[2]) if len(sys.argv) > 2 else 10)
    else:
        show()
