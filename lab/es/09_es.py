"""Elasticsearch 9편 직접 해 보기: 상위 10개만 필요할 때 ES가 문서를 얼마나 덜 계산하는지 profile로 본다.

실행: ES=http://localhost:9200 python lab/es/09_es.py
문서 20만 개 중 모든 문서에 common, 1%에 rare를 넣고 'rare common'(OR)으로 상위 10개를 찾는다.
track_total_hits를 true(건수를 끝까지 센다), 기본값(1만까지만 센다), false(세지 않는다)로 바꿔 가며 점수 계산 횟수(score_count)를 센다.
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


random.seed(9)
N = 200_000
req("DELETE", "/topk")
req("PUT", "/topk", {"settings": {"number_of_shards": 1, "number_of_replicas": 0, "refresh_interval": "-1"},
                     "mappings": {"properties": {"body": {"type": "text"}}}})
for i in range(0, N, 20000):
    lines = []
    for n in range(i, i + 20000):
        words = ["common"] * random.randint(1, 3) + ["filler"] * random.randint(0, 20)
        if random.random() < 0.01:
            words += ["rare"] * random.randint(1, 3)
        random.shuffle(words)
        lines.append('{"index":{}}')
        lines.append(json.dumps({"body": " ".join(words)}))
    req("POST", "/topk/_bulk", ("\n".join(lines) + "\n").encode(), ndjson=True)
req("POST", "/topk/_forcemerge?max_num_segments=1")
req("POST", "/topk/_refresh")


def score_count(node):
    return node["breakdown"].get("score_count", 0)


for tth in (True, None, False):
    body = {"profile": True, "size": 10, "query": {"match": {"body": "rare common"}}}
    if tth is not None:
        body["track_total_hits"] = tth
    res = req("POST", "/topk/_search", body)
    total = res["hits"].get("total", {"value": 0, "relation": "세지 않음"})
    q = res["profile"]["shards"][0]["searches"][0]["query"][0]
    name = {True: "true", None: "기본(1만)", False: "false"}[tth]
    print(f"track_total_hits={name}: 건수 {total['value']:,}({total['relation']}), "
          f"점수 계산 {score_count(q):,}번, 1위 점수 {res['hits']['hits'][0]['_score']:.3f}")
