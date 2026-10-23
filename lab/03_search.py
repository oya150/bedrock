"""3편 '업다운 놀이는 왜 금방 맞힐까요' 실측.

실행: python3 lab/03_search.py
결과는 컴퓨터마다 다르다. 문서에 실린 숫자는 이 스크립트를 한 번 돌린 결과다.
"""
import bisect
import platform
import timeit


def guesses(n, target):
    """1~n 업다운에서 늘 가운데를 부를 때 부른 횟수."""
    lo, hi, count = 1, n, 0
    while True:
        mid = (lo + hi) // 2
        count += 1
        if mid == target:
            return count
        if mid < target:
            lo = mid + 1
        else:
            hi = mid - 1


def best(fn, number=1, repeat=5):
    return min(timeit.repeat(fn, number=number, repeat=repeat)) / number


print(f"# {platform.python_implementation()} {platform.python_version()} / {platform.machine()}")

print("\n## 1. 업다운: 가운데를 부르면 운이 제일 나빠도 몇 번")
for n in (100, 200, 1_000):
    print(f"  1~{n:,}: 최대 {max(guesses(n, t) for t in range(1, n + 1))}번")

print("\n## 2. 정렬된 리스트에서 맨 끝 값 찾기: 하나씩(x in xs) vs 이진 탐색(bisect)")
print("| n | 하나씩 | 이진 탐색 |")
for n in (1_000, 2_000, 1_000_000, 2_000_000):
    xs = list(range(n))
    x = n - 1
    seq = best(lambda: x in xs, number=20)
    bin_ = best(lambda: bisect.bisect_left(xs, x), number=100_000)
    print(f"| {n:,} | {seq * 1e6:,.1f} µs | {bin_ * 1e9:,.0f} ns |")
