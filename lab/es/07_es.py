"""Elasticsearch 7편 직접 해 보기: AND 검색에서 각 낱말 목록을 몇 번 읽었는지 profile로 본다.

실행: ES=http://localhost:9200 python lab/es/07_es.py
문서 10만 개 중 모든 문서에 common, 50개에만 rare가 들어 있다.
rare AND common 을 점수를 매기는 must로 profile 하면 common 쪽 advance가 rare 수만큼만 찍힌다(10만 번 한 칸씩 걷지 않는다).
세그먼트를 하나로 합쳐 두고 잰다. 세그먼트가 여럿이면 세그먼트마다 따로 센다.
"""
import json
import os
import random
import urllib.request

ES = os.environ.get("ES", "http://localhost:9200")


def req(method, path, body=None, ndjson=False):
    data = body if isinstance(body, bytes) else (json.dumps(body).encode() if body is not None else None)
    r = urllib.request.Request(ES + path, method=method, data=data,
                               headers={"Content-Type": "application/x-ndjson" if ndjson else "application/json"})
    try:
        return json.load(urllib.request.urlopen(r))
    except urllib.error.HTTPError as e:
        return json.load(e)


random.seed(7)
N = 100_000
rare = set(random.sample(range(N), 50))
req("DELETE", "/leap")
req("PUT", "/leap", {"settings": {"number_of_shards": 1, "number_of_replicas": 0, "refresh_interval": "-1"},
                     "mappings": {"properties": {"body": {"type": "text"}}}})
for i in range(0, N, 20000):
    lines = []
    for n in range(i, i + 20000):
        lines.append('{"index":{}}')
        lines.append(json.dumps({"body": "common rare" if n in rare else "common"}))
    req("POST", "/leap/_bulk", ("\n".join(lines) + "\n").encode(), ndjson=True)
req("POST", "/leap/_forcemerge?max_num_segments=1")
req("POST", "/leap/_refresh")

# 점수를 매기는 must로 묻고 결과를 실제로 꺼내게 한다(size>0). filter+size 0이면 최근 버전은 문서를 하나씩 읽지 않고 건수만 셀 수 있다
q = {"profile": True, "size": 100, "track_total_hits": False,
     "query": {"bool": {"must": [{"term": {"body": "rare"}}, {"term": {"body": "common"}}]}}}
res = req("POST", "/leap/_search", q)
print("겹치는 문서:", len(res["hits"]["hits"]))


def walk(node, depth=0):
    b = node["breakdown"]
    print(f"{'  ' * depth}{node['description']:<16} next_doc {b.get('next_doc_count', 0):>6}  advance {b.get('advance_count', 0):>6}")
    for c in node.get("children", []):
        walk(c, depth + 1)


for q in res["profile"]["shards"][0]["searches"][0]["query"]:
    walk(q)
