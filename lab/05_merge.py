"""5편 '카드를 반씩 나눠 정리하면 왜 빠를까요' 실측.

실행: python3 lab/05_merge.py
결과는 컴퓨터마다 다르다. 문서에 실린 숫자는 이 스크립트를 한 번 돌린 결과다.
"""
import itertools
import platform
import random
import timeit


def merge(left, right, counter):
    """정렬된 두 줄을 맨 앞끼리 비교하며 한 줄로 합친다."""
    out = []
    i = j = 0
    while i < len(left) and j < len(right):
        counter[0] += 1
        if left[i] <= right[j]:
            out.append(left[i])
            i += 1
        else:
            out.append(right[j])
            j += 1
    return out + left[i:] + right[j:]


def merge_sort(xs, counter):
    if len(xs) <= 1:
        return xs
    mid = len(xs) // 2
    return merge(merge_sort(xs[:mid], counter), merge_sort(xs[mid:], counter), counter)


def insertion_sort(xs):
    """4편과 같은 삽입 정렬. 비교 횟수를 돌려준다."""
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


def merge_count(xs):
    counter = [0]
    merge_sort(list(xs), counter)
    return counter[0]


def levels(xs):
    """한 장씩에서 시작해 층마다 합칠 때 비교 횟수."""
    piles = [[x] for x in xs]
    result = []
    while len(piles) > 1:
        counter = [0]
        piles = [merge(piles[k], piles[k + 1], counter) for k in range(0, len(piles), 2)]
        result.append(counter[0])
    return result


def best(fn, number=1, repeat=5):
    return min(timeit.repeat(fn, number=number, repeat=repeat)) / number


print(f"# {platform.python_implementation()} {platform.python_version()} / {platform.machine()}")

print("\n## 1. 본문 장면")
c = [0]
print(f"  2, 5, 7, 8 + 1, 3, 4, 6 합치기: {merge([2, 5, 7, 8], [1, 3, 4, 6], c)}, 비교 {c[0]}번")
deck = [5, 2, 8, 7, 3, 6, 1, 4]
print(f"  덱 {deck}: 층별 {levels(deck)}, 병합 {merge_count(deck)}번, 삽입 {insertion_sort(deck)}번")
for n in (8, 16):
    desc = list(range(n, 0, -1))
    print(f"  거꾸로 {n}장: 층별 {levels(desc)}, 병합 {merge_count(desc)}번, 삽입 {insertion_sort(desc)}번")
print(f"  8장 병합 정렬이 운이 제일 나쁠 때: {max(merge_count(p) for p in itertools.permutations(range(8)))}번")

print("\n## 2. 확인 문제")
for a, b in (([1, 4, 6], [2, 3, 5]), ([1, 2, 3], [4, 5, 6])):
    c = [0]
    merge(a, b, c)
    print(f"  {a} + {b}: 비교 {c[0]}번")

print("\n## 3. 순수 파이썬 시간: 삽입 정렬(4편) vs 병합 정렬")
print("| n | 삽입 거꾸로 | 병합 거꾸로 | 삽입 무작위 | 병합 무작위 |")
random.seed(5)
for n in (1_000, 2_000):
    desc = list(range(n, 0, -1))
    mixed = random.sample(range(n), n)
    row = [best(lambda d=d: insertion_sort(d), repeat=3) if k % 2 == 0 else best(lambda d=d: merge_count(d), repeat=3)
           for k, d in enumerate((desc, desc, mixed, mixed))]
    print(f"| {n:,} | " + " | ".join(f"{t * 1e3:,.2f} ms" for t in row) + " |")
