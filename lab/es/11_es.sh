#!/bin/bash
# Elasticsearch 11편 직접 해 보기. 숫자 범위를 숫자 필드와 keyword 필드로 각각 찾아본다.
ES=${ES:-http://localhost:9200}
J='Content-Type: application/json'
curl -s -XDELETE "$ES/prices" >/dev/null
curl -s -XPUT "$ES/prices" -H "$J" -d '{"settings":{"number_of_shards":1,"number_of_replicas":0},
 "mappings":{"properties":{"price":{"type":"long"},"price_kw":{"type":"keyword"}}}}' >/dev/null
for p in 9 10 25 100 300 2000; do curl -s -XPOST "$ES/prices/_doc" -H "$J" -d "{\"price\":$p,\"price_kw\":\"$p\"}" >/dev/null; done
curl -s -XPOST "$ES/prices/_refresh" >/dev/null
show() { python3 -c 'import sys,json; print("  ", sorted(h["_source"]["price"] for h in json.load(sys.stdin)["hits"]["hits"]))'; }
echo "== long 필드로 10 이상 25 이하"
curl -s "$ES/prices/_search" -H "$J" -d '{"query":{"range":{"price":{"gte":10,"lte":25}}}}' | show
echo "== keyword 필드로 \"10\" 이상 \"25\" 이하 (글자 순서)"
curl -s "$ES/prices/_search" -H "$J" -d '{"query":{"range":{"price_kw":{"gte":"10","lte":"25"}}}}' | show
echo "== 필드별 저장소 크기(_disk_usage): long은 points, keyword는 inverted_index"
curl -s -XPOST "$ES/prices/_disk_usage?run_expensive_tasks=true" | python3 -c '
import sys,json
f=json.load(sys.stdin)["prices"]["fields"]
for k in ("price","price_kw"):
    x=f[k]; print("  ", k, "points", x.get("points_in_bytes"), "inverted", x["inverted_index"]["total_in_bytes"], "doc_values", x.get("doc_values_in_bytes"))'
