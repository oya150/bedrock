"""Elasticsearch 13편: 고유한 수를 적은 메모리로 어림하는 HyperLogLog를 직접 만들어 본다.

실행: python lab/es/13_hll.py
1) 정확히 세기: 본 값을 집합에 다 넣는다(메모리가 값 수만큼)
2) 맨 앞 0 개수 어림: 해시값의 맨 앞에 0이 몇 개 연속인지 중 가장 긴 것만 기억한다(통 하나)
3) HyperLogLog: 해시값 앞 p비트로 통 2^p개를 고르고 통마다 '가장 긴 0 줄'만 기억해 조화평균으로 합친다(Flajolet 외 2007)
"""
import hashlib
import math
import random


def h64(x: str) -> int:
    return int.from_bytes(hashlib.blake2b(x.encode(), digest_size=8).digest(), "big")


def rho(w: int, bits: int) -> int:
    """bits비트 정수 w에서 맨 앞부터 0이 몇 개 이어지는지 + 1"""
    return bits - w.bit_length() + 1


def hll_estimate(values, p):
    m = 1 << p
    reg = [0] * m
    for v in values:
        x = h64(v)
        idx = x >> (64 - p)                        # 앞 p비트로 통 고르기
        w = x & ((1 << (64 - p)) - 1)              # 나머지 비트에서 0 줄 길이
        reg[idx] = max(reg[idx], rho(w, 64 - p))
    alpha = 0.7213 / (1 + 1.079 / m)
    est = alpha * m * m / sum(2.0 ** -r for r in reg)
    zeros = reg.count(0)
    if est <= 2.5 * m and zeros:                   # 작은 수는 빈 통 비율로 고친다(선형 계수)
        est = m * math.log(m / zeros)
    return est, m


def one_bucket_estimate(values):
    best = max(rho(h64(v), 64) for v in values) - 1   # 가장 긴 앞 0 줄 길이
    return 2 ** best


if __name__ == "__main__":
    random.seed(13)
    for true_n in (1_000, 100_000, 1_000_000):
        users = [f"user-{random.randrange(10**12)}" for _ in range(true_n)]
        users = list(dict.fromkeys(users))[:true_n]
        n = len(users)
        stream = users + random.sample(users, n // 2)     # 같은 사용자가 여러 번 온다
        random.shuffle(stream)
        one = one_bucket_estimate(stream)
        print(f"실제 고유 사용자 {n:,}명 (기록 {len(stream):,}건)")
        print(f"  통 하나로 어림: {one:,}  (2의 거듭제곱으로만 나와요)")
        for p in (10, 14):
            est, m = hll_estimate(stream, p)
            print(f"  HyperLogLog 통 {m:,}개(ES는 통 하나에 1바이트, {m // 1024} KB): {est:,.0f}  오차 {abs(est - n) / n:.1%}")
        print(f"  정확히 세기: 집합에 {n:,}개 저장 (값 하나에 40 B만 잡아도 {n * 40 / 1e6:,.2f} MB)")
