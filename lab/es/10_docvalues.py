"""Elasticsearch 10편: 문서 → 값이 필요한 일(정렬·집계)을 역색인으로 할 때와 열(doc values)로 할 때를 비교한다.

실행: python lab/es/10_docvalues.py
문서 100만 개에 브랜드 값(1,000종)을 하나씩 준다.
1) 역색인(브랜드 → 문서 번호 목록)만 있을 때: 문서마다 브랜드를 알려면 모든 목록을 다 훑어 뒤집어야 한다(uninvert)
2) doc values: 문서 번호 순서로 값(정확히는 값의 순번 ordinal)을 한 줄로 적어 둔 열. 문서 번호로 바로 읽는다
"""
import random
import time
from collections import Counter

random.seed(10)
N, V = 1_000_000, 1_000
brands = sorted(f"brand-{i:04d}" for i in range(V))
doc_brand = [random.randrange(V) for _ in range(N)]

# 역색인: 브랜드 → 정렬된 문서 번호 목록
inverted = {b: [] for b in range(V)}
for d, b in enumerate(doc_brand):
    inverted[b].append(d)

# doc values: 문서 번호 순서대로 브랜드 순번(ordinal)을 적은 열 + 순번 → 값 사전
column = list(doc_brand)

# 질문: 검색 결과 1만 개 문서를 브랜드 이름순으로 정렬하고, 브랜드별 건수를 센다
hits = sorted(random.sample(range(N), 10_000))

t = time.perf_counter()
uninverted = [0] * N
for b, docs in inverted.items():            # 1) 모든 목록을 훑어 문서 → 브랜드 표를 새로 만든다
    for d in docs:
        uninverted[d] = b
a1 = sorted(hits, key=lambda d: uninverted[d])
c1 = Counter(uninverted[d] for d in hits)
t1 = time.perf_counter() - t

t = time.perf_counter()
a2 = sorted(hits, key=lambda d: column[d])   # 2) 열에서 바로 읽는다. 순번끼리 비교하면 이름순과 같다
c2 = Counter(column[d] for d in hits)
t2 = time.perf_counter() - t

assert a1 == a2 and c1 == c2
print(f"문서 {N:,}개, 브랜드 {V:,}종, 검색 결과 {len(hits):,}개를 정렬하고 브랜드별로 센다")
print(f"  역색인을 뒤집어서: {t1 * 1000:8.1f} ms (문서 {N:,}개 전부를 훑음)")
print(f"  doc values 열에서: {t2 * 1000:8.1f} ms (결과 {len(hits):,}개만 읽음)")
print(f"  정렬 1위 문서의 브랜드: {brands[column[a2[0]]]}")
