"""1편 '빅오는 왜 필요한가' 실측.

실행: python3 lab/01_big_o.py
결과는 컴퓨터마다 다르다. 문서에 실린 숫자는 이 스크립트를 한 번 돌린 결과다.
"""
import platform
import random
import timeit


def withdrawn_slow(members, withdrawn):
    # 회원마다 탈퇴 목록 전체를 훑는다: n × m
    out = []
    for m in members:
        for w in withdrawn:
            if m == w:
                out.append(m)
    return out


def withdrawn_fast(members, withdrawn):
    # 탈퇴 목록을 set에 한 번 담고 회원마다 한 번 묻는다: n + m
    gone = set(withdrawn)
    return [m for m in members if m in gone]


def total_loop(xs):
    s = 0
    for x in xs:
        s += x
    return s


def insertion_sort(xs):
    xs = list(xs)
    for i in range(1, len(xs)):
        cur = xs[i]
        j = i - 1
        while j >= 0 and xs[j] > cur:
            xs[j + 1] = xs[j]
            j -= 1
        xs[j + 1] = cur
    return xs


def merge_sort(xs):
    if len(xs) <= 1:
        return list(xs)
    mid = len(xs) // 2
    a, b = merge_sort(xs[:mid]), merge_sort(xs[mid:])
    out, i, j = [], 0, 0
    while i < len(a) and j < len(b):
        if a[i] <= b[j]:
            out.append(a[i]); i += 1
        else:
            out.append(b[j]); j += 1
    out.extend(a[i:]); out.extend(b[j:])
    return out


def best(stmt, number=1, repeat=5):
    return min(timeit.repeat(stmt, number=number, repeat=repeat)) / number


def ms(t):
    return f"{t * 1000:,.3f} ms"


print(f"# {platform.python_implementation()} {platform.python_version()} / {platform.machine()}")

print("\n## 1. 같은 코드를 다섯 번 재면")
xs = list(range(1_000_000))
runs = timeit.repeat(lambda: total_loop(xs), number=1, repeat=5)
print("  ", ", ".join(ms(t) for t in runs))

print("\n## 2. 탈퇴 회원 고르기: 회원이 두 배가 되면 (탈퇴는 회원의 10%)")
print("| 회원 수 | 느린 코드 | 빠른 코드 |")
for n in (1_000, 2_000, 4_000, 8_000):
    members = list(range(n))
    withdrawn = random.sample(members, n // 10)
    slow = best(lambda: withdrawn_slow(members, withdrawn), repeat=3)
    fast = best(lambda: withdrawn_fast(members, withdrawn), number=20)
    print(f"| {n:,} | {ms(slow)} | {ms(fast)} |")

print("\n## 3. 둘 다 n번인데: for 반복 합 vs 내장 sum")
for n in (100_000, 1_000_000):
    xs = list(range(n))
    a = best(lambda: total_loop(xs), number=5)
    b = best(lambda: sum(xs), number=5)
    print(f"  n={n:,}: for {ms(a)}, sum {ms(b)}, {a / b:.1f}배")

print("\n## 4. n이 작을 때: 삽입정렬(n²) vs 병합정렬(n log n), 둘 다 순수 파이썬")
print("| n | 삽입 | 병합 | 빠른 쪽 |")
for n in (4, 8, 16, 32, 64, 128, 256, 1024):
    data = [random.random() for _ in range(n)]
    k = max(1, 20_000 // n)
    a = best(lambda: insertion_sort(data), number=k)
    b = best(lambda: merge_sort(data), number=k)
    print(f"| {n} | {a * 1e6:,.1f} µs | {b * 1e6:,.1f} µs | {'삽입' if a < b else '병합'} |")
