"""Elasticsearch 3편: 문서가 어느 샤드로 가는지 직접 계산하고, 샤드 수를 바꾸면 몇 개가 옮겨야 하는지 센다.

실행: python lab/es/03_routing.py            (계산만)
      ES=http://localhost:9200 python lab/es/03_routing.py   (실제 ES와 맞춰 보기)

ES가 쓰는 식(OperationRouting, 7.x~9.x 같음):
  routing_factor = number_of_routing_shards / number_of_shards
  shard = floorMod(murmur3(_routing), number_of_routing_shards) // routing_factor
_routing을 따로 주지 않으면 _id를 쓴다. murmur3는 문자열의 UTF-16 바이트(리틀 엔디언)에 seed 0으로 돌린다.
number_of_routing_shards(칸 수)를 주지 않으면 ES 7부터는 샤드 수에 2를 거듭 곱해 1,024를 넘지 않는 가장 큰 수로 잡는다.
샤드 3개면 768, 5개면 640, 4개면 1,024. (_settings의 include_defaults에는 이 값이 샤드 수로 보이지만 실제 배치는 이 칸 수를 따른다.)
"""
import json
import os
import urllib.request


def murmur3_32(data: bytes, seed: int = 0) -> int:
    c1, c2 = 0xCC9E2D51, 0x1B873593
    h = seed
    n = len(data) // 4 * 4
    for i in range(0, n, 4):
        k = int.from_bytes(data[i:i + 4], "little")
        k = (k * c1) & 0xFFFFFFFF
        k = ((k << 15) | (k >> 17)) & 0xFFFFFFFF
        k = (k * c2) & 0xFFFFFFFF
        h ^= k
        h = ((h << 13) | (h >> 19)) & 0xFFFFFFFF
        h = (h * 5 + 0xE6546B64) & 0xFFFFFFFF
    k = 0
    tail = data[n:]
    if len(tail) >= 3:
        k ^= tail[2] << 16
    if len(tail) >= 2:
        k ^= tail[1] << 8
    if len(tail) >= 1:
        k ^= tail[0]
        k = (k * c1) & 0xFFFFFFFF
        k = ((k << 15) | (k >> 17)) & 0xFFFFFFFF
        k = (k * c2) & 0xFFFFFFFF
        h ^= k
    h ^= len(data)
    h ^= h >> 16
    h = (h * 0x85EBCA6B) & 0xFFFFFFFF
    h ^= h >> 13
    h = (h * 0xC2B2AE35) & 0xFFFFFFFF
    h ^= h >> 16
    return h - (1 << 32) if h >= (1 << 31) else h   # 자바 int처럼 부호 있는 값


def es_hash(routing: str) -> int:
    return murmur3_32(routing.encode("utf-16-le"))


def default_routing_shards(shards: int) -> int:
    n = shards
    while n * 2 <= 1024:
        n *= 2
    return n


def shard_of(routing: str, shards: int, routing_shards: int = None) -> int:
    routing_shards = routing_shards or default_routing_shards(shards)
    return (es_hash(routing) % routing_shards) // (routing_shards // shards)   # 파이썬 %는 floorMod와 같다


def moved(n_docs, old, new, slots=None):
    """새 인덱스를 샤드 new개로 만들어 다시 넣으면, 옛 샤드와 다른 샤드에 가는 문서 비율.
    slots를 주면 두 인덱스가 같은 칸 수를 쓴다고 보고 단순 나머지만 비교한다."""
    ids = [str(i) for i in range(n_docs)]
    return sum(shard_of(i, old, slots) != shard_of(i, new, slots) for i in ids) / n_docs


def check_with_es(es):
    def req(method, path, body=None):
        r = urllib.request.Request(es + path, method=method, data=json.dumps(body).encode() if body is not None else None,
                                   headers={"Content-Type": "application/json"})
        try:
            return json.load(urllib.request.urlopen(r))
        except urllib.error.HTTPError as e:
            return json.load(e)
    req("DELETE", "/routing-test")
    req("PUT", "/routing-test", {"settings": {"number_of_shards": 3, "number_of_replicas": 0}})   # 칸 수는 기본값(768)
    ids = [f"order-{i}" for i in range(30)]
    for i in ids:
        req("PUT", f"/routing-test/_doc/{i}", {"n": i})
    req("POST", "/routing-test/_refresh")
    ok = 0
    for s in range(3):
        hits = req("POST", f"/routing-test/_search?preference=_shards:{s}&size=100", {"query": {"match_all": {}}})["hits"]["hits"]
        for h in hits:
            ok += shard_of(h["_id"], 3) == s   # 기본 칸 수 768로 계산
    print(f"ES와 맞춰 보기: 문서 30개 중 {ok}개가 계산한 샤드에 있었어요")


if __name__ == "__main__":
    for i in ["order-1", "order-4", "order-6"]:
        h = es_hash(i)
        print(f"{i}: murmur3 {h}, 칸 768개 중 {h % 768}번 → 샤드 3개면 {shard_of(i, 3)}번")
    N = 100_000
    for old, new in [(3, 4), (5, 6)]:
        print(f"샤드 {old}개 인덱스 → {new}개 새 인덱스로 다시 넣으면 다른 샤드에 가는 문서 {moved(N, old, new):.0%}")
    print(f"(칸 없이 단순 나머지 % 3 → % 4라면 {moved(N, 3, 4, slots=None) if False else sum(es_hash(str(i)) % 3 != es_hash(str(i)) % 4 for i in range(N)) / N:.0%})")
    # split: 칸 수는 그대로 두고 샤드가 맡은 칸 묶음만 반으로 나눈다
    rs = 768
    same_parent = sum(shard_of(str(i), 6, rs) // 2 == shard_of(str(i), 3, rs) for i in range(N)) / N
    print(f"칸 {rs}개 그대로 3 → 6 split: 새 샤드가 옛 샤드에서 갈라진 것인 문서 {same_parent:.0%}")
    if os.environ.get("ES"):
        check_with_es(os.environ["ES"])
