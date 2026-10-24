#!/bin/bash
# Elasticsearch 3편 직접 해 보기. 샤드 수 바꾸기, 쪼개기(split), 라우팅 값 직접 주기.
ES=${ES:-http://localhost:9200}
J='Content-Type: application/json'
for i in orders orders-6 orders-4 by-user; do curl -s -XDELETE "$ES/$i" >/dev/null; done
curl -s -XPUT "$ES/orders" -H "$J" -d '{"settings":{"number_of_shards":3,"number_of_replicas":0}}' >/dev/null
for n in $(seq 1 30); do curl -s -XPUT "$ES/orders/_doc/order-$n" -H "$J" -d "{\"n\":$n}" >/dev/null; done
curl -s -XPOST "$ES/orders/_refresh" >/dev/null
err() { python3 -c 'import sys,json; d=json.load(sys.stdin); print("  ", d["error"]["reason"][:120] if "error" in d else d)'; }

echo "== 샤드 수를 바로 바꾸기"
curl -s -XPUT "$ES/orders/_settings" -H "$J" -d '{"index":{"number_of_shards":4}}' | err
echo "== 쪼개기는 쓰기를 막은 뒤에. 3 → 4는 안 되고 3 → 6은 돼요"
curl -s -XPUT "$ES/orders/_settings" -H "$J" -d '{"index.blocks.write":true}' >/dev/null
curl -s -XPOST "$ES/orders/_split/orders-4" -H "$J" -d '{"settings":{"index.number_of_shards":4}}' | err
curl -s -XPOST "$ES/orders/_split/orders-6" -H "$J" -d '{"settings":{"index.number_of_shards":6,"index.number_of_replicas":0}}' | err

echo "== 라우팅 값 user-7을 준 글 9개는 한 샤드에 모여요"
curl -s -XPUT "$ES/by-user" -H "$J" -d '{"settings":{"number_of_shards":3,"number_of_replicas":0}}' >/dev/null
for k in $(seq 1 9); do curl -s -XPUT "$ES/by-user/_doc/m$k?routing=user-7" -H "$J" -d "{\"k\":$k}" >/dev/null; done
curl -s -XPOST "$ES/by-user/_refresh" >/dev/null
curl -s "$ES/_cat/shards/by-user?h=shard,docs&s=shard"
echo "== 라우팅 값 없이 GET 하면 _id로 계산한 다른 샤드를 봐서 못 찾을 수 있어요"
curl -s -o /dev/null -w "   routing 없이: HTTP %{http_code}\n" "$ES/by-user/_doc/m1"
curl -s -o /dev/null -w "   routing=user-7: HTTP %{http_code}\n" "$ES/by-user/_doc/m1?routing=user-7"
