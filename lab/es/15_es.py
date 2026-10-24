"""Elasticsearch 15편: dense_vector 필드로 가까운 벡터를 찾고 정확한 답과 비교한다.

실행: ES=http://localhost:9200 python lab/es/15_es.py
- 16차원 벡터 20,000개를 넣는다.
- 정확한 답: script_score로 모든 문서의 거리를 계산(7.17과 8.x 이후 모두 됨)
- 근사 답: knn 검색(8.x부터, HNSW). num_candidates를 바꿔 가며 정답 10개 중 몇 개를 찾는지 센다.
  8.x 이후에서는 기본 index_options(버전마다 다름) 인덱스와 압축 없는 hnsw 인덱스를 함께 잰다.
"""
import json
import os
import random
import urllib.error
import urllib.request

ES = os.environ.get("ES", "http://localhost:9200")
N, DIM = 20_000, 16


def call(method, path, body=None, raw=None):
    data = raw if raw is not None else (json.dumps(body).encode() if body is not None else None)
    ctype = "application/x-ndjson" if raw is not None else "application/json"
    req = urllib.request.Request(ES + path, method=method, data=data, headers={"Content-Type": ctype})
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            return json.loads(r.read() or b"{}")
    except urllib.error.HTTPError as e:
        return {"error": json.loads(e.read() or b"{}").get("error", {})}


def build(idx, field, vecs):
    call("DELETE", f"/{idx}")
    call("PUT", f"/{idx}", {"settings": {"number_of_shards": 1, "number_of_replicas": 0},
                            "mappings": {"properties": {"v": field}}})
    for s in range(0, N, 2000):
        lines = []
        for i in range(s, min(N, s + 2000)):
            lines.append(json.dumps({"index": {"_id": str(i)}}))
            lines.append(json.dumps({"v": vecs[i]}))
        call("POST", f"/{idx}/_bulk", raw=("\n".join(lines) + "\n").encode())
    call("POST", f"/{idx}/_refresh")
    call("POST", f"/{idx}/_forcemerge?max_num_segments=1")


def recall(idx, queries, exact, nc, extra=None):
    hit = 0
    for q, ex in zip(queries, exact):
        knn = {"field": "v", "query_vector": q, "k": 10, "num_candidates": nc, **(extra or {})}
        r = call("POST", f"/{idx}/_search", {"size": 10, "_source": False, "knn": knn})
        if "error" in r:
            return r["error"].get("type")
        hit += len(ex & {h["_id"] for h in r["hits"]["hits"]})
    return f"정답 10개 중 평균 {hit / len(queries):.1f}개"


def main():
    ver = call("GET", "/")["version"]["number"]
    major = int(ver.split(".")[0])
    random.seed(15)
    vecs = [[round(random.gauss(0, 1), 4) for _ in range(DIM)] for _ in range(N)]
    queries = [[round(random.gauss(0, 1), 4) for _ in range(DIM)] for _ in range(30)]

    field = {"type": "dense_vector", "dims": DIM}
    if major >= 8:
        field.update({"index": True, "similarity": "l2_norm"})
    build("vec15", field, vecs)
    print(f"ES {ver}: 벡터 {N:,}개({DIM}차원) 넣음")

    exact = []
    for q in queries:
        r = call("POST", "/vec15/_search", {"size": 10, "_source": False, "query": {"script_score": {
            "query": {"match_all": {}},
            "script": {"source": "1 / (1 + l2norm(params.q, 'v'))", "params": {"q": q}}}}})
        exact.append({h["_id"] for h in r["hits"]["hits"]})
    print(f"  script_score(정확): 질의마다 문서 {N:,}개 모두 계산")

    if major < 8:
        print("  knn 검색:", recall("vec15", queries[:1], exact[:1], 50), "(7.x에는 근사 검색이 없어요)")
        return
    opts = call("GET", "/vec15/_mapping")["vec15"]["mappings"]["properties"]["v"].get("index_options")
    build("vec15f", {**field, "index_options": {"type": "hnsw"}}, vecs)
    print(f"  기본 index_options: {opts}")
    for nc in (10, 50, 100):
        print(f"  num_candidates {nc:>3}: 압축 없는 hnsw {recall('vec15f', queries, exact, nc)} / "
              f"기본 {recall('vec15', queries, exact, nc)} / "
              f"기본+rescore_vector {recall('vec15', queries, exact, nc, {'rescore_vector': {'oversample': 3}})}")


if __name__ == "__main__":
    main()
