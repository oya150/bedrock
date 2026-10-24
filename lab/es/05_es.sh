#!/bin/bash
# Elasticsearch 5편 직접 해 보기. 지우고 고친 문서가 언제 실제로 사라지는지 본다.
ES=${ES:-http://localhost:9200}
J='Content-Type: application/json'
curl -s -XDELETE "$ES/posts" >/dev/null
# 병합이 저절로 일어나지 않게 refresh를 꺼 두고, 우리가 부를 때만 세그먼트를 만든다
curl -s -XPUT "$ES/posts" -H "$J" -d '{"settings":{"number_of_shards":1,"number_of_replicas":0,"refresh_interval":"-1"}}' >/dev/null
stats() { curl -s "$ES/_cat/indices/posts?h=docs.count,docs.deleted,store.size&v" | sed 's/^/   /'; }
segs() { curl -s "$ES/_cat/segments/posts?h=segment,docs.count,docs.deleted,size&v" | sed 's/^/   /'; }
df() { curl -s "$ES/posts/_termvectors/$1?fields=body&term_statistics=true" | python3 -c 'import sys,json; t=json.load(sys.stdin)["term_vectors"]["body"]["terms"]; print("   환불 doc_freq =", t["환불"]["doc_freq"])'; }

echo "== 문서 300개를 100개씩 세 번 넣고 그때마다 refresh: 세그먼트 3개"
for b in 0 1 2; do
  body=""
  for i in $(seq 1 100); do n=$((b*100+i)); body+="{\"index\":{\"_id\":\"$n\"}}\n{\"body\":\"환불 문의 $n\"}\n"; done
  printf "$body" | curl -s -XPOST "$ES/posts/_bulk" -H 'Content-Type: application/x-ndjson' --data-binary @- >/dev/null
  curl -s -XPOST "$ES/posts/_refresh" >/dev/null
done
segs; stats; df 1
echo "== 1~100번을 지우고 101번을 고침"
for i in $(seq 1 100); do curl -s -XDELETE "$ES/posts/_doc/$i" >/dev/null; done
curl -s -XPUT "$ES/posts/_doc/101" -H "$J" -d '{"body":"환불 문의 101 수정"}' >/dev/null
curl -s -XPOST "$ES/posts/_refresh" >/dev/null
segs; stats
echo "== 검색에는 안 나오지만 doc_freq에는 아직 섞여 있어요"
curl -s "$ES/posts/_count" -H "$J" -d '{"query":{"match":{"body":"환불"}}}' | python3 -c 'import sys,json; print("   환불 검색 건수 =", json.load(sys.stdin)["count"])'
df 150
echo "== 바로 강제 병합(세그먼트 1개로): 세그먼트는 하나가 되지만 지운 문서가 아직 남아요"
curl -s -XPOST "$ES/posts/_forcemerge?max_num_segments=1" >/dev/null
curl -s -XPOST "$ES/posts/_refresh" >/dev/null
segs; stats
echo "== 복구용 보존 표시(retention lease)가 앞으로 갈 때까지 기다렸다가 다시 병합"
echo "   (보존 표시는 기본 30초마다 갱신돼요. 70초 기다려요)"
sleep 70
curl -s -XPOST "$ES/posts/_forcemerge?max_num_segments=1" >/dev/null
curl -s -XPOST "$ES/posts/_refresh" >/dev/null
segs; stats; df 150
