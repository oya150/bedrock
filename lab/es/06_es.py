"""Elasticsearch 6편 직접 해 보기: 낱말 약 23만 개를 넣고 필드별 역색인 크기를 본다.

실행: ES=http://localhost:9200 python lab/es/06_es.py
_disk_usage API(7.15부터)로 필드 w와 ES가 문서마다 붙이는 _id의 역색인 크기를 따로 본다.
세그먼트 파일(.tim, .tip 등) 크기는 모든 필드가 섞여 있어서 참고로만 찍는다.
병합으로 새로 쓴 세그먼트가 파일을 따로 두도록 index.compound_format을 끈다.
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


words = sorted({w.strip().lower() for w in open("/usr/share/dict/words") if w.strip()})
req("DELETE", "/words")
req("PUT", "/words", {"settings": {"number_of_shards": 1, "number_of_replicas": 0, "refresh_interval": "-1",
                                   "index.compound_format": False},
                      "mappings": {"properties": {"w": {"type": "keyword"}}}})
for i in range(0, len(words), 20000):
    lines = []
    for w in words[i:i + 20000]:
        lines.append('{"index":{}}')
        lines.append(json.dumps({"w": w}))
    req("POST", "/words/_bulk", ("\n".join(lines) + "\n").encode(), ndjson=True)
    req("POST", "/words/_refresh")   # 묶음마다 세그먼트를 하나씩 만든다
# refresh로 만든 작은 세그먼트는 파일 하나(.cfs)로 묶여 있어서 병합으로 새로 써야 파일이 따로 보인다
req("POST", "/words/_forcemerge?max_num_segments=1")
st = req("GET", "/words/_stats/segments?include_segment_file_sizes=true")
seg = st["indices"]["words"]["primaries"]["segments"]
files = seg.get("file_sizes", {})
print(f"낱말 {len(words):,}개, 글자 {sum(map(len, words)):,}개")
for ext in ("tim", "tip"):
    if ext in files:
        print(f"  (참고, 모든 필드 합) .{ext}: {files[ext]['size_in_bytes']:,} B")
du = req("POST", "/words/_disk_usage?run_expensive_tasks=true")["words"]["fields"]
for f in ("w", "_id"):
    print(f"  {f} 역색인(용어 사전+포스팅): {du[f]['inverted_index']['total_in_bytes']:,} B")
print(f"  힙에 올린 용어 사전 색인 통계: {seg.get('terms_memory_in_bytes')} B (9.x는 이 통계가 늘 0이에요)")
