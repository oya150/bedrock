#!/bin/bash
# Elasticsearch 5편 실험. 지운 문서가 언제 실제로 사라지는지 본다.
ES=${ES:-http://localhost:9200}
J='Content-Type: application/json'
# 인덱스 크기 통계는 10초마다 다시 계산돼서 잴 때마다 11초를 기다린다
stats() { sleep 11; curl -s "$ES/_cat/indices/$1?h=docs.count,docs.deleted,store.size&v" | sed 's/^/   /'; }
segs() { curl -s "$ES/_cat/segments/$1?h=segment,docs.count,docs.deleted,size&v" | sed 's/^/   /'; }
df() { curl -s "$ES/$1/_termvectors/$2?fields=body&term_statistics=true" | python3 -c 'import sys,json; t=json.load(sys.stdin)["term_vectors"]["body"]["terms"]; print("   환불이 든 문서 수(doc_freq) =", t["환불"]["doc_freq"])'; }
count() { curl -s "$ES/$1/_count" -H "$J" -d '{"query":{"match":{"body":"환불"}}}' | python3 -c 'import sys,json; print("   환불 검색 건수 =", json.load(sys.stdin)["count"])'; }
fill() {
  curl -s -XDELETE "$ES/$1" >/dev/null
  # 병합이 저절로 일어나지 않게 refresh를 꺼 두고 우리가 부를 때만 세그먼트를 만든다
  curl -s -XPUT "$ES/$1" -H "$J" -d '{"settings":{"number_of_shards":1,"number_of_replicas":0,"refresh_interval":"-1"}}' >/dev/null
  for b in 0 1 2; do
    body=""
    for i in $(seq 1 100); do n=$((b*100+i)); body+="{\"index\":{\"_id\":\"$n\"}}\n{\"body\":\"환불 문의 $n\"}\n"; done
    printf "$body" | curl -s -XPOST "$ES/$1/_bulk" -H 'Content-Type: application/x-ndjson' --data-binary @- >/dev/null
    curl -s -XPOST "$ES/$1/_refresh" >/dev/null
  done
}

echo "== 글 300개를 100개씩 세 번 넣고 그때마다 refresh: 세그먼트 3개"
fill posts; segs posts; stats posts
echo "== 1~100번을 지우고 refresh: 지운 문서 200(빈 문서 100 포함), 크기는 오히려 커져요"
for i in $(seq 1 100); do curl -s -XDELETE "$ES/posts/_doc/$i" >/dev/null; done
curl -s -XPOST "$ES/posts/_refresh" >/dev/null
segs posts; stats posts; count posts; df posts 150
echo "== 바로 강제 병합(세그먼트 1개로): 세그먼트는 하나가 되지만 지운 문서가 남아요"
curl -s -XPOST "$ES/posts/_forcemerge?max_num_segments=1" >/dev/null
segs posts; stats posts
echo "== 보존 표시가 앞으로 갈 때까지 기다렸다가 다시 병합 (기본 30초 주기라 60초 더 기다려요)"
sleep 60
curl -s -XPOST "$ES/posts/_forcemerge?max_num_segments=1" >/dev/null
segs posts; stats posts; df posts 150

echo "== 따로: 글 하나(101번)를 고치면 옛 세그먼트에 지운 문서 1, 새 세그먼트에 고친 글"
fill edits
curl -s -XPUT "$ES/edits/_doc/101" -H "$J" -d '{"body":"환불 문의 101 수정"}' >/dev/null
curl -s -XPOST "$ES/edits/_refresh" >/dev/null
segs edits
curl -s -XDELETE "$ES/posts" >/dev/null; curl -s -XDELETE "$ES/edits" >/dev/null
