"""8편 '비교하지 않고 정렬할 수 있을까요' 실측.

실행: python3 lab/08_counting.py
1) 카드 n장이 놓일 수 있는 순서의 수와, 비교 한 번에 많아야 반씩만 줄일 수 있을 때 필요한 비교 수를 센다.
2) 카드 세 장을 비교 세 번으로 정렬하는 순서(본문 그림의 나무)를 모든 순서에 돌려 확인한다.
3) 숫자 범위가 작은 카드를 상자에 나눠 담아 정렬한다(계수 정렬). 비교는 하지 않는다.
결과는 컴퓨터마다 다르다(비교 수는 같다). 문서에 실린 시간은 이 스크립트를 한 번 돌린 결과다.
"""
import itertools
import math
import platform
import random
import timeit


class Card:
    count = 0

    def __init__(self, v):
        self.v = v

    def __lt__(self, other):
        Card.count += 1
        return self.v < other.v


def halvings(k):
    """k가지에서 반씩 버려 1가지가 될 때까지 몇 번 걸리나(반이 딱 안 나뉘면 많은 쪽이 남는다)."""
    steps = 0
    while k > 1:
        k = (k + 1) // 2
        steps += 1
    return steps


def three(a, b, c):
    """카드 세 장 a, b, c를 비교 세 번 안에 정렬한다. 비교 수도 돌려준다."""
    n = 1
    if a < b:
        n += 1
        if b < c:
            return [a, b, c], n
        n += 1
        return ([a, c, b], n) if a < c else ([c, a, b], n)
    n += 1
    if a < c:
        return [b, a, c], n
    n += 1
    return ([b, c, a], n) if b < c else ([c, b, a], n)


def counting_sort(xs, low, high):
    """상자 low~high에 카드를 나눠 담고, 작은 상자부터 꺼낸다."""
    boxes = [[] for _ in range(high - low + 1)]
    for x in xs:
        boxes[x - low].append(x)
    return [x for box in boxes for x in box]


def merge_count(xs):
    c = 0

    def ms(a):
        nonlocal c
        if len(a) <= 1:
            return a
        m = len(a) // 2
        l, r = ms(a[:m]), ms(a[m:])
        out, i, j = [], 0, 0
        while i < len(l) and j < len(r):
            c += 1
            if l[i] <= r[j]:
                out.append(l[i]); i += 1
            else:
                out.append(r[j]); j += 1
        return out + l[i:] + r[j:]
    ms(list(xs))
    return c


def best(fn, repeat=5):
    return min(timeit.repeat(fn, number=1, repeat=repeat))


print(f"# {platform.python_implementation()} {platform.python_version()} / {platform.machine()}")

print("\n## 1. 카드가 놓일 수 있는 순서와 꼭 필요한 비교 수")
for n in (2, 3, 4, 5, 8):
    orders = math.factorial(n)
    print(f"  {n}장: 순서 {orders:,}가지, 반씩 줄이면 {halvings(orders)}번")
print(f"  4장 24가지를 반씩: {[24, 12, 6, 3, 2, 1]}")

print("\n## 2. 카드 세 장 나무: 모든 순서에서 정렬되는지, 비교는 몇 번인지")
worst = 0
for p in itertools.permutations([1, 2, 3]):
    out, n = three(*p)
    assert out == [1, 2, 3]
    worst = max(worst, n)
    print(f"  {p}: 비교 {n}번")
print(f"  가장 많을 때 {worst}번")
print(f"  5편 병합 정렬, 카드 4장 모든 순서에서 가장 많을 때: "
      f"{max(merge_count(p) for p in itertools.permutations(range(4)))}번")

for n in (3, 4, 8):
    w = 0
    for p in itertools.permutations(range(n)):
        Card.count = 0
        sorted(Card(x) for x in p)
        w = max(w, Card.count)
    print(f"  sorted() {n}장 모든 순서에서 가장 많을 때: {w}번")

print("\n## 3. 계수 정렬: 숫자가 1~5뿐인 카드 20장")
random.seed(8)
deck = [random.randint(1, 5) for _ in range(20)]
print(f"  카드: {deck}")
print(f"  상자별 장수: {[deck.count(v) for v in range(1, 6)]}")
print(f"  결과: {counting_sort(deck, 1, 5)}")
Card.count = 0
sorted(Card(x) for x in deck)
print(f"  같은 카드를 sorted()로: 비교 {Card.count}번, 5편 병합 정렬: 비교 {merge_count(deck)}번")

print("\n## 4. 시간(순수 파이썬): 0~100점 10만 개, 계수 정렬 vs 5편 병합 정렬, 참고로 sorted()")
scores = [random.randint(0, 100) for _ in range(100_000)]
t1 = best(lambda: counting_sort(scores, 0, 100), repeat=3)
t2 = best(lambda: merge_count(scores), repeat=3)
t3 = best(lambda: sorted(scores), repeat=3)
print(f"  계수 {t1 * 1e3:,.1f} ms, 병합 {t2 * 1e3:,.1f} ms, sorted() {t3 * 1e3:,.1f} ms")
