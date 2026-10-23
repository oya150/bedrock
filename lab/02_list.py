"""2편 '사물함은 왜 몇 번이든 바로 찾을까요' 실측.

실행: python3 lab/02_list.py
결과는 컴퓨터마다 다르다. 문서에 실린 숫자는 이 스크립트를 한 번 돌린 결과다.
"""
import platform
import timeit


def fill_back(n):
    xs = []
    for i in range(n):
        xs.append(i)
    return xs


def fill_front(n):
    xs = []
    for i in range(n):
        xs.insert(0, i)
    return xs


def best(fn, number=1, repeat=5):
    return min(timeit.repeat(fn, number=number, repeat=repeat)) / number


def ms(t):
    return f"{t * 1000:,.3f} ms"


print(f"# {platform.python_implementation()} {platform.python_version()} / {platform.machine()}")

print("\n## 1. 몇 번째 칸을 꺼내든: 리스트가 커져도 한 번 꺼내는 시간")
print("| 길이 | 첫 칸 | 마지막 칸 |")
for n in (1_000, 1_000_000):
    xs = list(range(n))
    a, b = 0, n - 1
    first = best(lambda: xs[a], number=1_000_000)
    last = best(lambda: xs[b], number=1_000_000)
    print(f"| {n:,} | {first * 1e9:.1f} ns | {last * 1e9:.1f} ns |")

print("\n## 2. n개를 채우기: 끝에 넣기(append) vs 맨 앞에 끼우기(insert(0, x))")
print("| n | 끝에 넣기 | 맨 앞에 끼우기 |")
for n in (10_000, 20_000, 40_000, 80_000):
    back = best(lambda: fill_back(n), number=5)
    front = best(lambda: fill_front(n), repeat=3)
    print(f"| {n:,} | {ms(back)} | {ms(front)} |")
