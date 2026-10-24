#!/bin/bash
# Elasticsearch 2편 직접 해 보기. 분석기가 글을 어떻게 자르는지 본다.
# nori는 공식 플러그인이라 따로 설치해야 한다(아래 nori 부분은 설치했을 때만 돈다):
#   docker exec es bin/elasticsearch-plugin install --batch analysis-nori && docker restart es
ES=${ES:-http://localhost:9200}
J='Content-Type: application/json'
tok() { python3 -c 'import sys,json; print("  ", [t["token"] for t in json.load(sys.stdin)["tokens"]])'; }

echo "== standard 분석기: 환불했어요. Refund-Request!"
curl -s "$ES/_analyze" -H "$J" -d '{"analyzer":"standard","text":"환불했어요. Refund-Request!"}' | tok

echo "== 단계별로: char_filter(html_strip) → tokenizer(standard) → filter(lowercase)"
curl -s "$ES/_analyze" -H "$J" -d '{"char_filter":["html_strip"],"tokenizer":"standard","filter":["lowercase"],"text":"<b>Refund</b> 요청"}' | tok

echo "== keyword 분석기(자르지 않음)"
curl -s "$ES/_analyze" -H "$J" -d '{"analyzer":"keyword","text":"Refund Request"}' | tok

curl -s -XDELETE "$ES/shop" >/dev/null
curl -s -XPUT "$ES/shop" -H "$J" -d '{"settings":{"number_of_shards":1,"number_of_replicas":0},
 "mappings":{"properties":{"title":{"type":"text"},"code":{"type":"keyword"}}}}' >/dev/null
curl -s -XPUT "$ES/shop/_doc/1" -H "$J" -d '{"title":"Refund Request","code":"Refund Request"}' >/dev/null
curl -s -XPOST "$ES/shop/_refresh" >/dev/null
hits() { python3 -c 'import sys,json; print("   hits =", json.load(sys.stdin)["hits"]["total"]["value"])'; }
echo "== text 필드에 term \"Refund\" (검색어는 자르지 않음)"
curl -s "$ES/shop/_search" -H "$J" -d '{"query":{"term":{"title":"Refund"}}}' | hits
echo "== text 필드에 match \"Refund\" (검색어도 같은 분석기로 자름)"
curl -s "$ES/shop/_search" -H "$J" -d '{"query":{"match":{"title":"Refund"}}}' | hits
echo "== keyword 필드에 match \"refund request\" (keyword는 글자 그대로)"
curl -s "$ES/shop/_search" -H "$J" -d '{"query":{"match":{"code":"refund request"}}}' | hits

if curl -s "$ES/_cat/plugins" | grep -q nori; then
  echo "== nori 분석기"
  for t in "환불했어요" "환불 요청합니다" "간식을 샀어요"; do
    curl -s "$ES/_analyze" -H "$J" -d "{\"analyzer\":\"nori\",\"text\":\"$t\"}" | tok
  done
  echo "== nori_tokenizer만(품사 거르기 없이)"
  curl -s "$ES/_analyze" -H "$J" -d '{"tokenizer":"nori_tokenizer","text":"환불했어요"}' | tok
fi
