"""9편 '이름으로 어떻게 바로 찾을까요' 실측.

실행: python3 lab/09_hash.py
1) 본문의 장난감 규칙(이름 첫 글자의 첫소리 번호로 사물함 칸 고르기)으로 친구 이름을 넣고 찾는다.
   칸이 차 있으면 다음 칸으로 간다. 찾을 때 몇 칸을 열어 봤는지 센다.
2) 파이썬 dict가 처음에 칸 8개로 시작해 몇 개째에서 커지는지 sys.getsizeof로 본다.
3) 이름 10만 개에서 list로 찾기(1편 '다 뒤지기')와 dict로 찾기 시간을 잰다.
결과는 컴퓨터마다 다르다. 문서에 실린 시간은 이 스크립트를 한 번 돌린 결과다.
"""
import platform
import random
import sys
import timeit

CHO = "ㄱㄲㄴㄷㄸㄹㅁㅂㅃㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎ"
# 본문 표: 첫소리마다 번호. 쌍자음은 쓰지 않는다.
NUM = {c: k for k, c in enumerate("ㄱㄴㄷㄹㅁㅂㅅㅇㅈㅊㅋㅌㅍㅎ")}


def first_sound(name):
    return CHO[(ord(name[0]) - 0xAC00) // 588]


def slot(name, n=8):
    """첫소리 번호. 칸 수보다 크거나 같으면 칸 수를 뺀다(칸이 8개면 8을 뺀다)."""
    k = NUM[first_sound(name)]
    while k >= n:
        k -= n
    return k


def put(lockers, name):
    i = slot(name, len(lockers))
    while lockers[i] is not None:
        i = (i + 1) % len(lockers)
    lockers[i] = name
    return i


def find(lockers, name):
    i, looks = slot(name, len(lockers)), 0
    while True:
        looks += 1
        if lockers[i] == name:
            return i, looks
        if lockers[i] is None:
            return None, looks
        i = (i + 1) % len(lockers)


print(f"# {platform.python_implementation()} {platform.python_version()} / {platform.machine()}")

print("\n## 1. 사물함 8칸에 친구 다섯")
lockers = [None] * 8
for name in ["민준", "서연", "하준", "지우", "서준"]:
    print(f"  {name}: 첫소리 {first_sound(name)} → 규칙 칸 {slot(name)}, 들어간 칸 {put(lockers, name)}")
print(f"  사물함: {lockers}")
for name in ["하준", "서준", "도윤"]:
    where, looks = find(lockers, name)
    print(f"  {name} 찾기: 칸 {where}, 열어 본 칸 {looks}개")

quiz = ["지우", None, None, None, None, "하준", "서연", "서준"]
print(f"  확인 문제(민준 없이 네 명): 하은 규칙 칸 {slot('하은')}, 들어간 칸 {put(quiz, '하은')}, "
      f"찾을 때 열어 본 칸 {find(quiz, '하은')[1]}개")

print("\n## 2. 모두 첫소리가 ㄱ이면")
bad = [None] * 8
for name in ["가온", "건우", "고은", "규리", "기현"]:
    put(bad, name)
print(f"  사물함: {bad}, 기현 찾기 열어 본 칸 {find(bad, '기현')[1]}개")

print("\n## 2-1. 여섯째 친구 도윤이 오면 칸을 16개로 늘려 다시 넣기")
big = [None] * 16
for name in ["민준", "서연", "하준", "지우", "서준", "도윤"]:
    print(f"  {name}: 규칙 칸 {slot(name, 16)}, 들어간 칸 {put(big, name)}")
print(f"  사물함: {big}")

print("\n## 3. 파이썬 dict 크기가 바뀌는 때")
d, last = {}, sys.getsizeof({})
for k in range(1, 25):
    d[k] = k
    size = sys.getsizeof(d)
    if size != last:
        print(f"  {k}개째 넣을 때 커짐 ({last} → {size} 바이트)")
        last = size

print("\n## 4. 이름 10만 개: list에서 찾기 vs dict에서 찾기")
random.seed(9)
names = [f"학생{k:06d}" for k in range(100_000)]
book = {n: k for k, n in enumerate(names)}
target = names[-1]
t_list = min(timeit.repeat(lambda: target in names, number=10, repeat=5)) / 10
t_dict = min(timeit.repeat(lambda: target in book, number=100_000, repeat=5)) / 100_000
print(f"  맨 끝 이름 찾기: list {t_list * 1e3:.2f} ms, dict {t_dict * 1e9:.0f} ns")
