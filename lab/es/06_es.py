"""Elasticsearch 6편: 용어 사전과 포스팅 목록이 실제로 얼마나 작게 담기는지 ES에서 잰다.

실행: ES=http://localhost:9200 python lab/es/06_es.py
_disk_usage API(7.15부터)로 필드마다 역색인(용어 사전+포스팅 목록) 크기를 따로 본다.
세 가지를 잰다.
1) words: 영어 낱말 약 23만 개를 글 하나에 하나씩 넣고 낱말 글자 수 합과 역색인 크기를 비교한다.
2) posts: 글 100만 개에 낱말이 얼마나 자주 나오느냐에 따라 포스팅 목록 크기가 어떻게 달라지는지 본다.
   c(10개 중 1개꼴), r(1천 개 중 1개꼴), s(1만 번 고르게), k(1만 번이 11월 몫 8만 2천 개 안에 몰림).
3) names: 사진 이름 10만 개를 찍은 시각 꼴(IMG_20261029_093512)과 무작위 32글자 꼴로 넣어 용어 사전 크기를 본다.
글 번호가 넣은 순서대로 매겨지도록 샤드 하나, refresh 끔, 끝에 세그먼트 하나로 병합한다.
"""
import json
import os
import random
import urllib.request
from datetime import datetime, timedelta

ES = os.environ.get("ES", "http://localhost:9200")


def req(method, path, body=None, ndjson=False):
    data = body if isinstance(body, bytes) else (json.dumps(body).encode() if body is not None else None)
    r = urllib.request.Request(ES + path, method=method, data=data,
                               headers={"Content-Type": "application/x-ndjson" if ndjson else "application/json"})
    try:
        return json.load(urllib.request.urlopen(r))
    except urllib.error.HTTPError as e:
        return json.load(e)


def build(name, props, docs):
    req("DELETE", "/" + name)
    req("PUT", "/" + name, {"settings": {"number_of_shards": 1, "number_of_replicas": 0, "refresh_interval": "-1"},
                            "mappings": {"properties": {p: {"type": "keyword"} for p in props}}})
    batch = []
    for d in docs:
        batch.append('{"index":{}}')
        batch.append(json.dumps(d))
        if len(batch) >= 100000:
            req("POST", f"/{name}/_bulk", ("\n".join(batch) + "\n").encode(), ndjson=True)
            batch = []
    if batch:
        req("POST", f"/{name}/_bulk", ("\n".join(batch) + "\n").encode(), ndjson=True)
    req("POST", f"/{name}/_refresh")
    req("POST", f"/{name}/_forcemerge?max_num_segments=1")
    du = req("POST", f"/{name}/_disk_usage?run_expensive_tasks=true")[name]["fields"]
    return {p: du[p]["inverted_index"]["total_in_bytes"] for p in props if p in du}


# 1) 낱말 23만 개
words = sorted({w.strip().lower() for w in open("/usr/share/dict/words") if w.strip()})
size = build("words", ["w"], ({"w": w} for w in words))
seg = req("GET", "/words/_stats/segments")["indices"]["words"]["primaries"]["segments"]
print(f"낱말 {len(words):,}개, 글자 수 합 {sum(map(len, words)):,} B")
print(f"  필드 w 역색인: {size['w']:,} B   (힙에 올린 용어 사전 색인 통계 {seg.get('terms_memory_in_bytes')} B, 9.x는 늘 0)")

# 2) 글 100만 개의 포스팅 목록
N = 1_000_000
random.seed(6)
c = set(random.sample(range(N), N // 10))
r = set(random.sample(range(N), N // 1000))
s = set(random.sample(range(N), 10_000))
nov = range(int(N * 304 / 365), int(N * 334 / 365))        # 날짜순으로 넣었을 때 11월 몫
k = set(random.sample(nov, 10_000))
size = build("posts", ["c", "r", "s", "k"],
             ({f: "y" for f, ids in (("c", c), ("r", r), ("s", s), ("k", k)) if i in ids} for i in range(N)))
for f, ids, t in (("c", c, "10개 중 1개꼴"), ("r", r, "1천 개 중 1개꼴"), ("s", s, "1만 번 고르게"), ("k", k, "1만 번 11월에 몰림")):
    print(f"  {f} {t}: 글 {len(ids):,}개, 그대로(4바이트씩) {4 * len(ids):,} B, 역색인 {size[f]:,} B ({size[f] / (4 * len(ids)):.0%})")

# 3) 사진 이름 10만 개
random.seed(7)
t = datetime(2026, 1, 1)
names_a = []
for _ in range(100_000):
    t += timedelta(seconds=random.randint(1, 600))
    names_a.append(t.strftime("IMG_%Y%m%d_%H%M%S"))
names_b = ["%032x" % random.getrandbits(128) for _ in range(100_000)]
size = build("names", ["a", "b"], ({"a": a, "b": b} for a, b in zip(names_a, names_b)))
print(f"사진 이름 10만 개: 시각 꼴 글자 {sum(map(len, names_a)):,} B → 역색인 {size['a']:,} B, "
      f"무작위 꼴 글자 {sum(map(len, names_b)):,} B → 역색인 {size['b']:,} B")
