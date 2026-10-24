"""Elasticsearch 12편 직접 해 보기: 샤드 셋에 나뉜 결과를 합칠 때 생기는 일을 본다.

실행: ES=http://localhost:9200 python lab/es/12_es.py
1) terms 집계: 샤드마다 자기 몫의 위 몇 개만 보내면 전체 1위를 놓칠 수 있다(shard_size)
2) 깊은 페이지: from+size가 1만을 넘으면 거절된다(index.max_result_window), search_after로 이어 읽는다
"""
import json
import os
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


req("DELETE", "/sales")
req("PUT", "/sales", {"settings": {"number_of_shards": 3, "number_of_replicas": 0},
                      "mappings": {"properties": {"brand": {"type": "keyword"}, "n": {"type": "long"}}}})
# 샤드마다 1등 브랜드가 따로 있고(x, z, w 각 10건), y는 모든 샤드에서 2등(9건씩, 합계 27건)이다.
# routing 값 shop-5, shop-1, shop-0은 3편의 계산(lab/es/03_routing.py)으로 샤드 0, 1, 2에 하나씩 간다. _cat/shards로 확인한다.
plan = {"shop-5": {"x": 10, "y": 9}, "shop-1": {"z": 10, "y": 9}, "shop-0": {"w": 10, "y": 9}}
lines, n = [], 0
for routing, counts in plan.items():
    for brand, c in counts.items():
        for _ in range(c):
            n += 1
            lines.append(json.dumps({"index": {"_id": str(n), "routing": routing}}))
            lines.append(json.dumps({"brand": brand, "n": n}))
req("POST", "/sales/_bulk?refresh=true", ("\n".join(lines) + "\n").encode(), ndjson=True)
shards = req("GET", "/_cat/shards/sales?format=json&h=shard,docs")
print("샤드별 문서 수:", sorted((int(s["shard"]), int(s["docs"])) for s in shards))

for shard_size in (1, 10):
    res = req("POST", "/sales/_search", {"size": 0, "aggs": {"top": {"terms": {"field": "brand", "size": 1,
                                                                                "shard_size": shard_size,
                                                                                "show_term_doc_count_error": True}}}})
    agg = res["aggregations"]["top"]
    b = agg["buckets"][0]
    print(f"terms size 1, shard_size {shard_size}: 1위 {b['key']} {b['doc_count']}건 "
          f"(오차 상한 {agg.get('doc_count_error_upper_bound')}, 이 칸 오차 {b.get('doc_count_error_upper_bound')})")

# 깊은 페이지
res = req("POST", "/sales/_search", {"from": 10000, "size": 10, "query": {"match_all": {}}})
err = res.get("error", {}).get("root_cause", [{}])[0].get("reason", "")
print("from 10000 + size 10 (1,001쪽째):", err[:110] if err else f"{len(res['hits']['hits'])}건")
page = req("POST", "/sales/_search", {"size": 20, "sort": [{"n": "asc"}]})
last = page["hits"]["hits"][-1]["sort"]
nxt = req("POST", "/sales/_search", {"size": 5, "sort": [{"n": "asc"}], "search_after": last})
print("search_after", last, "→ 다음 5건 n =", [h["_source"]["n"] for h in nxt["hits"]["hits"]])
