"""Elasticsearch 1편: 하나씩 다 보기와 역색인 찾기를 재 본다.

실행: python lab/es/01_inverted_index.py
글 20만 개를 만들고, 낱말 하나가 들어 있는 글을 두 방법으로 찾는다.
1) 글마다 처음부터 끝까지 보기 (LIKE '%낱말%'와 같은 일)
2) 낱말 → 글 번호 목록(역색인)을 미리 만들어 두고 목록만 꺼내기
"""
import bisect
import random
import time

random.seed(1)
WORDS = [f"w{i}" for i in range(5000)]   # 낱말 5,000개
N = 200_000                               # 글 20만 개


def make_docs():
    docs = []
    for _ in range(N):
        docs.append(" ".join(random.choices(WORDS, k=30)))
    docs[123_456] += " 환불"
    docs[150_000] += " 환불"
    return docs


def scan(docs, word):
    return [i for i, d in enumerate(docs) if word in d.split()]


def build(docs):
    index = {}
    for i, d in enumerate(docs):
        for w in set(d.split()):
            index.setdefault(w, []).append(i)   # 글 번호 순서대로 들어가니 목록은 늘 정렬돼 있다
    terms = sorted(index)                      # 용어 사전: 낱말을 정렬해 둔다
    return terms, index


def lookup(terms, index, word):
    k = bisect.bisect_left(terms, word)        # 정렬된 사전에서 이진 탐색
    if k < len(terms) and terms[k] == word:
        return index[word]
    return []


def intersect(a, b):
    """정렬된 두 목록에서 둘 다 있는 번호만. 두 목록을 한 번씩만 훑는다."""
    i = j = 0
    out = []
    while i < len(a) and j < len(b):
        if a[i] == b[j]:
            out.append(a[i]); i += 1; j += 1
        elif a[i] < b[j]:
            i += 1
        else:
            j += 1
    return out


if __name__ == "__main__":
    docs = make_docs()

    t = time.perf_counter(); hit = scan(docs, "환불"); t_scan = time.perf_counter() - t
    t = time.perf_counter(); terms, index = build(docs); t_build = time.perf_counter() - t
    t = time.perf_counter(); hit2 = lookup(terms, index, "환불"); t_look = time.perf_counter() - t

    assert hit == hit2 == [123_456, 150_000]
    print(f"글 {N:,}개, 낱말 종류 {len(terms):,}개")
    print(f"하나씩 다 보기:   {t_scan*1000:9.1f} ms  → {hit}")
    print(f"역색인 만들기:     {t_build*1000:9.1f} ms  (한 번만)")
    print(f"역색인에서 찾기:   {t_look*1000:9.4f} ms  → {hit2}")
    print(f"찾기만 비교하면 약 {t_scan/t_look:,.0f}배")

    a, b = index["w1"], index["w2"]
    t = time.perf_counter(); both = intersect(a, b); t_and = time.perf_counter() - t
    print(f"w1 목록 {len(a):,}개, w2 목록 {len(b):,}개 → 둘 다 있는 글 {len(both):,}개, {t_and*1000:.2f} ms")
