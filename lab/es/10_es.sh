#!/bin/bash
# Elasticsearch 10편 직접 해 보기. 정렬·집계가 쓰는 doc values를 본다.
ES=${ES:-http://localhost:9200}
J='Content-Type: application/json'
curl -s -XDELETE "$ES/orders10" >/dev/null
curl -s -XPUT "$ES/orders10" -H "$J" -d '{"settings":{"number_of_shards":1,"number_of_replicas":0},
 "mappings":{"properties":{
   "title":{"type":"text"},
   "brand":{"type":"keyword"},
   "order_no_kw":{"type":"keyword"},
   "order_no":{"type":"long"},
   "memo":{"type":"keyword","doc_values":false}}}}' >/dev/null
i=0
for n in 9 10 100 25 3; do
  i=$((i+1))
  curl -s -XPUT "$ES/orders10/_doc/$i" -H "$J" -d "{\"title\":\"주문 $n\",\"brand\":\"brand-$((n%3))\",\"order_no_kw\":\"$n\",\"order_no\":$n,\"memo\":\"m$n\"}" >/dev/null
done
curl -s -XPOST "$ES/orders10/_refresh" >/dev/null
err() { python3 -c 'import sys,json; d=json.load(sys.stdin); e=d.get("error"); print("  ", (e.get("root_cause",[{}])[0].get("reason") or e.get("reason"))[:150] if e else [h["sort"][0] for h in d["hits"]["hits"]])'; }

echo "== text 필드로 정렬"
curl -s "$ES/orders10/_search" -H "$J" -d '{"sort":[{"title":"asc"}]}' | err
echo "== keyword에 담은 주문번호로 정렬(글자 순서)"
curl -s "$ES/orders10/_search" -H "$J" -d '{"sort":[{"order_no_kw":"asc"}]}' | err
echo "== long에 담은 주문번호로 정렬(숫자 순서)"
curl -s "$ES/orders10/_search" -H "$J" -d '{"sort":[{"order_no":"asc"}]}' | err
echo "== doc_values를 끈 keyword로 정렬"
curl -s "$ES/orders10/_search" -H "$J" -d '{"sort":[{"memo":"asc"}]}' | err
echo "== doc_values를 끈 keyword로 검색(역색인은 있음)"
curl -s "$ES/orders10/_search" -H "$J" -d '{"query":{"term":{"memo":"m9"}}}' | python3 -c 'import sys,json; print("   hits =", json.load(sys.stdin)["hits"]["total"]["value"])'
echo "== 브랜드별 건수(terms 집계)"
curl -s "$ES/orders10/_search" -H "$J" -d '{"size":0,"aggs":{"b":{"terms":{"field":"brand"}}}}' | python3 -c 'import sys,json; print("  ", [(b["key"], b["doc_count"]) for b in json.load(sys.stdin)["aggregations"]["b"]["buckets"]])'
