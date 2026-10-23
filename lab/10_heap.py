"""10편 '가장 급한 것을 늘 빨리 꺼내려면' 실측.

실행: python3 lab/10_heap.py
본문의 힙(대진표)은 교과서 방식으로 짠다. 넣을 때는 맨 아래에 놓고 위 카드와 비교하며 올라가고,
꺼낼 때는 맨 위를 꺼낸 뒤 맨 끝 카드를 맨 위에 올려 아래 두 카드와 비교하며 내려간다.
비교할 때마다 센다. 파이썬 heapq는 꺼낼 때 조금 다른 순서로 내려가서 비교 수가 조금 다를 수 있다(어른 상자).
결과는 컴퓨터마다 다르다(비교 수는 같다). 문서에 실린 시간은 이 스크립트를 한 번 돌린 결과다.
"""
import heapq
import platform
import random
import timeit


class Heap:
    def __init__(self):
        self.a = []
        self.count = 0

    def less(self, i, j):
        self.count += 1
        return self.a[i] < self.a[j]

    def push(self, x):
        a = self.a
        a.append(x)
        i = len(a) - 1
        while i > 0:
            up = (i - 1) // 2
            if not self.less(i, up):
                break
            a[i], a[up] = a[up], a[i]
            i = up

    def pop(self):
        a = self.a
        top = a[0]
        last = a.pop()
        if a:
            a[0] = last
            i = 0
            while True:
                l, r = 2 * i + 1, 2 * i + 2
                if l >= len(a):
                    break
                small = l
                if r < len(a) and self.less(r, l):
                    small = r
                if not self.less(small, i):
                    break
                a[i], a[small] = a[small], a[i]
                i = small
        return top


def levels(n):
    k, size = 0, 1
    while size <= n:
        k += 1
        size += size
    return k


print(f"# {platform.python_implementation()} {platform.python_version()} / {platform.machine()}")

print("\n## 1. 본문 장면: 5, 3, 8, 1, 9, 4, 7을 차례로 넣기")
h = Heap()
for x in [5, 3, 8, 1, 9, 4, 7]:
    before = h.count
    h.push(x)
    print(f"  {x} 넣기: 비교 {h.count - before}번 → {h.a}")
before = h.count
h.push(2)
print(f"  2 넣기: 비교 {h.count - before}번 → {h.a}")
before = h.count
top = h.pop()
print(f"  꺼내기: {top}, 비교 {h.count - before}번 → {h.a}")

print("\n## 2. 확인 문제: 2를 넣은 뒤의 힙(꺼내기 전)에 6 넣기")
h = Heap()
h.a = [1, 2, 4, 3, 9, 8, 7, 5]
before = h.count
h.push(6)
print(f"  위 힙에 6 넣기: 비교 {h.count - before}번 → {h.a}")

print("\n## 3. 카드 수와 줄 수, 가장 많이 드는 비교")
for n in (7, 15, 1_000):
    k = levels(n)
    print(f"  {n:,}장: {k}줄, 넣기 많아야 {k - 1}번, 꺼내기 많아야 {2 * (k - 1)}번, 다 뒤지기 {n - 1}번")

print("\n## 4. 실제로 1,000장에서 넣고 꺼내기를 섞어 해 보기")
random.seed(10)
h = Heap()
for x in random.sample(range(100_000), 1_000):
    h.push(x)
worst_push = worst_pop = 0
for _ in range(1_000):
    before = h.count
    h.pop()
    worst_pop = max(worst_pop, h.count - before)
    before = h.count
    h.push(random.randrange(100_000))
    worst_push = max(worst_push, h.count - before)
print(f"  꺼내기 가장 많을 때 {worst_pop}번, 넣기 가장 많을 때 {worst_push}번")

print("\n## 5. 시간: 1만 개에서 '가장 작은 것 꺼내고 새것 넣기' 1,000번")
base = random.sample(range(10**6), 10_000)
new = [random.randrange(10**6) for _ in range(1_000)]


def with_list():
    xs = base[:]
    for v in new:
        xs.remove(min(xs))
        xs.append(v)


def with_heapq():
    xs = base[:]
    heapq.heapify(xs)
    for v in new:
        heapq.heapreplace(xs, v)


t1 = min(timeit.repeat(with_list, number=1, repeat=3))
t2 = min(timeit.repeat(with_heapq, number=1, repeat=3))
print(f"  리스트에서 min 찾기: {t1 * 1e3:,.1f} ms, heapq: {t2 * 1e3:,.2f} ms")
