"""6편 '기준 카드 하나로 나누면 어떻게 정렬될까요' 실측.

실행: python3 lab/06_quick.py
비교 횟수는 본문처럼 "기준 카드와 나머지 카드를 한 번씩 비교"로 센다.
기준을 맨 앞으로 잡고 차례대로인 카드를 정렬하면 줄이 한 장씩만 줄어 아주 깊게 나뉜다.
그래서 함수가 자기를 부르는 방식(재귀) 대신, 남은 일을 목록에 쌓아 두고 하나씩 꺼내 처리한다.
결과는 컴퓨터마다 다르다. 문서에 실린 숫자는 이 스크립트를 한 번 돌린 결과다.
"""
import itertools
import platform
import random
import timeit


def first(xs):
    return 0


def middle(xs):
    return (len(xs) - 1) // 2


def quick_sort(xs, pick, log=None):
    """더미를 새로 만드는 방식(본문 그림과 같음). 정렬된 줄과 비교 횟수를 돌려준다."""
    count = 0
    done = {}
    todo = [(0, list(xs))]          # (이 더미가 들어갈 첫 자리, 더미)
    while todo:
        start, pile = todo.pop()
        if len(pile) <= 1:
            for k, x in enumerate(pile):
                done[start + k] = x
            continue
        p = pick(pile)
        pivot = pile[p]
        rest = pile[:p] + pile[p + 1:]
        count += len(rest)
        left = [x for x in rest if x < pivot]
        right = [x for x in rest if x >= pivot]
        if log is not None:
            log.append((pile, pivot, left, right, len(rest)))
        done[start + len(left)] = pivot
        todo.append((start + len(left) + 1, right))
        todo.append((start, left))
    return [done[k] for k in range(len(xs))], count


def quick_count(xs, pick=first):
    return quick_sort(xs, pick)[1]


def merge_count(xs):
    """5편 병합 정렬의 비교 횟수(시간 비교용)."""
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
    c = 0
    ms(list(xs))
    return c


def best(fn, repeat=3):
    return min(timeit.repeat(fn, number=1, repeat=repeat))


print(f"# {platform.python_implementation()} {platform.python_version()} / {platform.machine()}")

print("\n## 1. 본문 장면: 덱 5, 2, 8, 7, 3, 6, 1, 4, 맨 앞 카드가 기준")
deck = [5, 2, 8, 7, 3, 6, 1, 4]
log = []
out, c = quick_sort(deck, first, log)
for pile, pivot, left, right, n in log:
    print(f"  {pile}: 기준 {pivot} → {left} {pivot} {right}, 비교 {n}번")
print(f"  결과 {out}, 모두 {c}번")

print("\n## 2. 차례대로인 카드")
for n in (8, 16):
    asc = list(range(1, n + 1))
    print(f"  {n}장: 맨 앞 기준 {quick_count(asc, first)}번, 가운데 기준 {quick_count(asc, middle)}번, "
          f"병합 정렬(거꾸로) {merge_count(asc[::-1])}번")
log = []
quick_sort(list(range(1, 9)), middle, log)
for pile, pivot, left, right, n in log:
    print(f"    가운데 기준 {pile}: 기준 {pivot}, 비교 {n}번")

print("\n## 3. 8장 모든 순서(40,320가지), 맨 앞 기준")
counts = [quick_count(p) for p in itertools.permutations(range(8))]
print(f"  가장 적게 {min(counts)}번, 가장 많이 {max(counts)}번, 평균 {sum(counts) / len(counts):.1f}번")
print(f"  28번이 나오는 순서 수: {counts.count(28)}가지")

print("\n## 4. 확인 문제")
log = []
quick_sort([4, 1, 6, 3, 5], first, log)
pile, pivot, left, right, n = log[0]
print(f"  [4, 1, 6, 3, 5] 첫 나누기: {left} {pivot} {right}, 비교 {n}번")
print(f"  [1, 2, 3, 4] 맨 앞 기준: {quick_count([1, 2, 3, 4])}번")

print("\n## 5. 순수 파이썬 시간: 차례대로인 카드")
print("| n | 퀵(맨 앞 기준) | 퀵(가운데 기준) | 병합 |")
for n in (1_000, 2_000):
    asc = list(range(n))
    row = [best(lambda: quick_count(asc, first)), best(lambda: quick_count(asc, middle)),
           best(lambda: merge_count(asc))]
    print(f"| {n:,} | " + " | ".join(f"{t * 1e3:,.2f} ms" for t in row) + " |")
print("\n## 6. 순수 파이썬 시간: 섞인 카드(맨 앞 기준)")
random.seed(6)
for n in (1_000, 2_000):
    mixed = random.sample(range(n), n)
    print(f"  {n:,}: 퀵 {best(lambda: quick_count(mixed)) * 1e3:,.2f} ms, 병합 {best(lambda: merge_count(mixed)) * 1e3:,.2f} ms")
