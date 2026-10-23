"""7편 '파이썬은 카드를 어떻게 정렬할까요' 실측.

실행: python3 lab/07_timsort.py
본문의 비교 수는 지어낸 값이 아니다. 파이썬 sorted()가 두 카드를 비교할 때마다(__lt__가 불릴 때마다)
하나씩 세는 카드로 실제 sorted()를 돌려서 센다. 4편·5편 방법은 그 편 스크립트와 같은 방식으로 센다.
결과는 컴퓨터마다 다르다(비교 수는 같다). 문서에 실린 시간은 이 스크립트를 한 번 돌린 결과다.
"""
import platform
import random
import timeit


class Card:
    """비교될 때마다 수를 세는 카드."""
    count = 0

    def __init__(self, v):
        self.v = v

    def __lt__(self, other):
        Card.count += 1
        return self.v < other.v


def tim_count(xs):
    Card.count = 0
    out = sorted(Card(x) for x in xs)
    assert [c.v for c in out] == sorted(xs)
    return Card.count


def insertion_count(xs):
    """4편 삽입 정렬의 비교 수."""
    xs = xs[:]
    count = 0
    for i in range(1, len(xs)):
        card = xs[i]
        j = i - 1
        while j >= 0:
            count += 1
            if xs[j] <= card:
                break
            xs[j + 1] = xs[j]
            j -= 1
        xs[j + 1] = card
    return count


def merge_sort(xs, counter):
    """5편 병합 정렬."""
    if len(xs) <= 1:
        return xs
    mid = len(xs) // 2
    left, right = merge_sort(xs[:mid], counter), merge_sort(xs[mid:], counter)
    out, i, j = [], 0, 0
    while i < len(left) and j < len(right):
        counter[0] += 1
        if left[i] <= right[j]:
            out.append(left[i]); i += 1
        else:
            out.append(right[j]); j += 1
    return out + left[i:] + right[j:]


def merge_count(xs):
    counter = [0]
    merge_sort(list(xs), counter)
    return counter[0]


def runs(xs):
    """왼쪽부터 이웃끼리 비교하며 차례대로 이어진 줄로 나눈다(본문 그림과 같은 생각)."""
    out = [[xs[0]]]
    for a, b in zip(xs, xs[1:]):
        if a < b:
            out[-1].append(b)
        else:
            out.append([b])
    return out


def best(fn, repeat=5):
    return min(timeit.repeat(fn, number=1, repeat=repeat))


print(f"# {platform.python_implementation()} {platform.python_version()} / {platform.machine()}")

print("\n## 1. 카드 8장")
for name, xs in (("차례대로", list(range(1, 9))), ("거꾸로", list(range(8, 0, -1)))):
    print(f"  {name} {xs}: 팀 정렬 {tim_count(xs)}번, 4편 {insertion_count(xs)}번, 5편 {merge_count(xs)}번")

print("\n## 2. 카드 64장")
cards = list(range(1, 65))
friends = cards[0::2] + cards[1::2]     # 홀수 32장 줄 + 짝수 32장 줄
random.seed(3)
mixed = random.sample(cards, 64)
for name, xs in (("친구 둘이 정리한 줄(홀수 줄 + 짝수 줄)", friends), ("뒤죽박죽", mixed)):
    print(f"  {name}: 줄 {len(runs(xs))}개, 팀 정렬 {tim_count(xs)}번, 4편 {insertion_count(xs)}번, "
          f"5편 {merge_count(xs)}번")
class Spot(Card):
    """입력에서 몇 번째였는지 기억하는 카드. 이웃끼리 비교(줄 찾기)와 나머지(합치기)를 나눠 센다."""
    near = 0

    def __init__(self, v, i):
        super().__init__(v)
        self.i = i

    def __lt__(self, other):
        if abs(self.i - other.i) == 1:
            Spot.near += 1
        return super().__lt__(other)


Card.count = Spot.near = 0
sorted(Spot(v, i) for i, v in enumerate(friends))
print(f"  친구 둘 카드: 이웃끼리 비교 {Spot.near}번, 나머지(합치기) {Card.count - Spot.near}번")
print(f"  뒤죽박죽 64장의 줄 길이: {[len(r) for r in runs(mixed)]}")

print("\n## 3. 확인 문제")
print(f"  3, 5, 8, 2, 4, 9의 줄: {runs([3, 5, 8, 2, 4, 9])}")
print(f"  6, 5, 4, 3, 2, 1: 팀 정렬 {tim_count([6, 5, 4, 3, 2, 1])}번")

print("\n## 4. 시간: 5편 병합 정렬(순수 파이썬) vs sorted()(C로 짠 팀 정렬)")
for n in (1_000, 10_000):
    a = list(range(n))
    two = a[0::2] + a[1::2]
    rnd = random.sample(a, n)
    for name, xs in (("차례대로", a), ("줄 둘", two), ("뒤죽박죽", rnd)):
        t1 = best(lambda: merge_count(xs))
        t2 = best(lambda: sorted(xs))
        print(f"  {n:,} {name}: 5편 {t1 * 1e3:,.2f} ms, sorted() {t2 * 1e3:,.3f} ms")
