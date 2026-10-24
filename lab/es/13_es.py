"""Elasticsearch 13편 직접 해 보기: cardinality(고유 수)와 percentiles(백분위)가 어림값이라는 걸 본다.

실행: ES=http://localhost:9200 python lab/es/13_es.py
샤드 3개 인덱스에 방문 기록 30만 건(고유 사용자 10만 명, 응답 시간)을 넣는다.
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


random.seed(13)
USERS, N = 100_000, 300_000
users = [f"u{random.randrange(10**9)}" for _ in range(USERS)]
users = list(dict.fromkeys(users))
visits = [(random.choice(users), round(random.lognormvariate(4, 0.8), 1)) for _ in range(N)]
true_unique = len({u for u, _ in visits})
lat = sorted(t for _, t in visits)
true_p = {q: lat[min(len(lat) - 1, int(q / 100 * len(lat)))] for q in (50, 99, 99.9)}

req("DELETE", "/visits")
req("PUT", "/visits", {"settings": {"number_of_shards": 3, "number_of_replicas": 0, "refresh_interval": "-1"},
                       "mappings": {"properties": {"user": {"type": "keyword"}, "ms": {"type": "double"}}}})
for i in range(0, N, 50_000):
    lines = []
    for u, t in visits[i:i + 50_000]:
        lines.append('{"index":{}}')
        lines.append(json.dumps({"user": u, "ms": t}))
    req("POST", "/visits/_bulk", ("\n".join(lines) + "\n").encode(), ndjson=True)
req("POST", "/visits/_refresh")

print(f"실제 고유 사용자 {true_unique:,}명")
for pt in (100, 3000, 40000):
    aggs = {"u": {"cardinality": {"field": "user", "precision_threshold": pt}}}
    v = req("POST", "/visits/_search", {"size": 0, "aggs": aggs})["aggregations"]["u"]["value"]
    print(f"  cardinality precision_threshold {pt:>6}: {v:,}  (오차 {abs(v - true_unique) / true_unique:.2%})")
res = req("POST", "/visits/_search", {"size": 0, "aggs": {"p": {"percentiles": {"field": "ms", "percents": [50, 99, 99.9]}}}})
vals = res["aggregations"]["p"]["values"]
print("응답 시간 백분위 (실제 / ES)")
for q in (50, 99, 99.9):
    es_v = vals.get(str(float(q))) or vals.get(f"{q}") or vals.get(f"{q:.1f}")
    print(f"  {q:>5}%: {true_p[q]:8.1f} / {es_v:8.1f}")
