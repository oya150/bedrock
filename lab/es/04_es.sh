#!/bin/bash
# Elasticsearch 4편 직접 해 보기. 넣은 문서가 언제 검색에 보이는지, 세그먼트와 translog를 본다.
ES=${ES:-http://localhost:9200}
J='Content-Type: application/json'
curl -s -XDELETE "$ES/nrt" >/dev/null
# 자동 refresh를 꺼서(-1) 우리가 부를 때만 refresh 되게 한다
curl -s -XPUT "$ES/nrt" -H "$J" -d '{"settings":{"number_of_shards":1,"number_of_replicas":0,"refresh_interval":"-1"}}' >/dev/null
hits() { python3 -c 'import sys,json; print("   검색 결과:", json.load(sys.stdin)["hits"]["total"]["value"], "건")'; }
segs() { curl -s "$ES/_cat/segments/nrt?h=segment,docs.count,committed,searchable&v" | sed 's/^/   /'; }
tl() { curl -s "$ES/nrt/_stats/translog?filter_path=indices.nrt.primaries.translog.uncommitted_operations" | python3 -c 'import sys,json; print("   translog에 커밋 안 된 작업:", json.load(sys.stdin)["indices"]["nrt"]["primaries"]["translog"]["uncommitted_operations"])'; }

echo "== 문서 하나를 넣고 바로 검색"
curl -s -XPUT "$ES/nrt/_doc/1" -H "$J" -d '{"body":"환불 요청"}' >/dev/null
curl -s "$ES/nrt/_search" -H "$J" -d '{"query":{"match":{"body":"환불"}}}' | hits
echo "== 같은 문서를 _id로 GET"
curl -s "$ES/nrt/_doc/1" | python3 -c 'import sys,json; print("   found:", json.load(sys.stdin)["found"])'
segs; tl
echo "== _refresh 뒤에 검색"
curl -s -XPOST "$ES/nrt/_refresh" >/dev/null
curl -s "$ES/nrt/_search" -H "$J" -d '{"query":{"match":{"body":"환불"}}}' | hits
segs; tl
echo "== 두 번 더 넣고 그때마다 refresh: 세그먼트가 하나씩 늘어요"
for i in 2 3; do curl -s -XPUT "$ES/nrt/_doc/$i" -H "$J" -d '{"body":"배송 문의"}' >/dev/null; curl -s -XPOST "$ES/nrt/_refresh" >/dev/null; done
segs
echo "== _flush 뒤: 세그먼트가 디스크에 커밋되고 translog가 비어요"
curl -s -XPOST "$ES/nrt/_flush" >/dev/null
segs; tl
echo "== refresh=wait_for: 다음 refresh까지 기다렸다가 응답 (자동 refresh를 1초로 되돌려서)"
curl -s -XPUT "$ES/nrt/_settings" -H "$J" -d '{"index":{"refresh_interval":"1s"}}' >/dev/null
curl -s -XPUT "$ES/nrt/_doc/4?refresh=wait_for" -H "$J" -d '{"body":"환불 완료"}' -o /dev/null -w "   응답까지 %{time_total}초\n"
curl -s "$ES/nrt/_search" -H "$J" -d '{"query":{"match":{"body":"환불"}}}' | hits
