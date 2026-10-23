"""4편 '손에 든 카드는 어떻게 정리할까요' 실측.

실행: python3 lab/04_insertion.py
결과는 컴퓨터마다 다르다. 문서에 실린 숫자는 이 스크립트를 한 번 돌린 결과다.
"""
import platform
import random
import timeit


def insertion_sort(xs):
    """손에 카드를 끼우듯 정렬한다. 두 장을 비교한 횟수를 돌려준다."""
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


def best(fn, number=1, repeat=5):
    return min(timeit.repeat(fn, number=number, repeat=repeat)) / number


print(f"# {platform.python_implementation()} {platform.python_version()} / {platform.machine()}")

print("\n## 1. 비교 횟수: 차례대로 받을 때와 거꾸로 받을 때")
for n in (4, 5, 8, 10, 20):
    up = insertion_sort(list(range(1, n + 1)))
    down = insertion_sort(list(range(n, 0, -1)))
    print(f"  {n}장: 차례대로 {up}번, 거꾸로 {down}번")

print("\n## 2. 본문 장면")
hand = [3, 7, 9, 5]
print(f"  3, 7, 9에 5 끼우기: 5를 끼울 때 비교 {insertion_sort(hand) - 2}번 → {hand}")
hand = [2, 4, 8, 6]
print(f"  2, 4, 8에 6 끼우기: 6을 끼울 때 비교 {insertion_sort(hand) - 2}번 → {hand}")
hand = [1, 2, 3, 4, 6, 7, 8, 9, 5]
print(f"  1~9(5 빠짐) 끝에 5: 5를 끼울 때 비교 {insertion_sort(hand) - 7}번 → {hand}")

print("\n## 3. 순수 파이썬 삽입 정렬 시간 (sorted()와 비교)")
print("| n | 정렬된 것 | 거꾸로 | 무작위 | 정렬된 것 끝에 1개 | sorted(무작위) |")
random.seed(4)
for n in (1_000, 2_000):
    asc = list(range(n))
    desc = asc[::-1]
    mixed = random.sample(asc, n)
    tail = list(range(1, n)) + [0]
    row = [best(lambda d=d: insertion_sort(d[:]), repeat=3) for d in (asc, desc, mixed, tail)]
    row.append(best(lambda: sorted(mixed), number=100))
    print(f"| {n:,} | " + " | ".join(f"{t * 1e3:,.2f} ms" for t in row) + " |")
