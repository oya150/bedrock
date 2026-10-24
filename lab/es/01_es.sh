#!/bin/bash
# Elasticsearch 1편 직접 해 보기. 조사 없이 낱말만 띄어 쓴 글 세 개를 넣는다. ES 7.17과 9.x에서 같은 결과가 나온다.
# ES 띄우기(둘 중 하나):
#   docker run -d --name es -p 9200:9200 -e discovery.type=single-node -e xpack.security.enabled=false elasticsearch:7.17.26
#   docker run -d --name es -p 9200:9200 -e discovery.type=single-node -e xpack.security.enabled=false docker.elastic.co/elasticsearch/elasticsearch:9.2.0
ES=${ES:-http://localhost:9200}
J='Content-Type: application/json'

curl -s -XDELETE "$ES/board" >/dev/null
curl -s -XPUT "$ES/board" -H "$J" -d '{"settings":{"number_of_shards":1,"number_of_replicas":0}}' >/dev/null

curl -s -XPUT "$ES/board/_doc/1" -H "$J" -d '{"body":"주문 환불 요청"}' >/dev/null
curl -s -XPUT "$ES/board/_doc/2" -H "$J" -d '{"body":"주문 배송 언제"}' >/dev/null
curl -s -XPUT "$ES/board/_doc/3" -H "$J" -d '{"body":"환불 완료 감사"}' >/dev/null
curl -s -XPOST "$ES/board/_refresh" >/dev/null

echo "== 1번 글의 낱말과, 그 낱말이 든 글 수(doc_freq)"
curl -s "$ES/board/_termvectors/1?fields=body&term_statistics=true" \
  | python3 -c 'import sys,json; t=json.load(sys.stdin)["term_vectors"]["body"]["terms"]; [print("  %s doc_freq=%d" % (w, v["doc_freq"])) for w,v in t.items()]'

echo "== 환불 AND 주문"
curl -s "$ES/board/_search" -H "$J" -d '{"query":{"match":{"body":{"query":"환불 주문","operator":"and"}}}}' \
  | python3 -c 'import sys,json; print("  ", [h["_id"] for h in json.load(sys.stdin)["hits"]["hits"]])'
