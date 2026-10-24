"""Elasticsearch 7편: 정렬된 두 목록의 교집합을 구하면서 일의 양을 센다.

실행: python lab/es/07_intersect.py
드문 낱말(문서 1천 개)과 흔한 낱말(문서 100만 개)의 교집합을 두 방법으로 구한다.
1) 두 손가락으로 한 칸씩(1편 방식). 긴 목록의 128개 묶음을 처음부터 끝까지 다 풀어 본다
2) 짧은 목록을 앞세우고, 긴 목록에서는 건너뛰기 표로 'target 이상인 첫 문서'가 든 묶음까지 건너뛴 뒤(advance)
   그 묶음 하나만 풀어 본다. 건너뛰기 표는 묶음마다 마지막 문서 번호를 적은 것이고,
   그 표 위에 8칸마다 하나씩 적은 윗층을 하나 더 둔다(Lucene의 다단계 건너뛰기를 줄인 모양)
"""
import random

BLOCK = 128
FAN = 8


def linear(short, long_):
    i = j = 0
    out = []
    while i < len(short) and j < len(long_):
        if short[i] == long_[j]:
            out.append(short[i]); i += 1; j += 1
        elif short[i] < long_[j]:
            i += 1
        else:
            j += 1
    blocks = (j + BLOCK - 1) // BLOCK                 # 긴 목록에서 풀어 본 묶음 수
    return out, blocks, 0


def leapfrog(short, long_):
    lv1 = long_[BLOCK - 1::BLOCK]                     # 묶음마다 마지막 번호
    lv2 = lv1[FAN - 1::FAN]                           # 1층 8칸마다 마지막 번호
    b = 0                                             # 지금 묶음 번호
    decoded = set()
    skip_reads = 0
    out = []
    for d in short:
        # 윗층에서 8묶음씩 건너뛰기
        k2 = b // FAN
        while k2 < len(lv2) and lv2[k2] < d:
            k2 += 1; skip_reads += 1
        b = max(b, k2 * FAN)
        # 아래층에서 한 묶음씩 건너뛰기
        while b < len(lv1) and lv1[b] < d:
            b += 1; skip_reads += 1
        if b * BLOCK >= len(long_):
            break
        decoded.add(b)                                # 이 묶음 하나만 풀어 본다
        if d in set(long_[b * BLOCK:(b + 1) * BLOCK]):
            out.append(d)
    return out, len(decoded), skip_reads


if __name__ == "__main__":
    random.seed(7)
    N = 10_000_000
    rare = sorted(random.sample(range(N), 1_000))
    common = sorted(random.sample(range(N), 1_000_000))
    want = sorted(set(rare) & set(common))
    r1, b1, _ = linear(rare, common)
    r2, b2, s2 = leapfrog(rare, common)
    assert r1 == r2 == want
    total = (len(common) + BLOCK - 1) // BLOCK
    print(f"드문 낱말 {len(rare):,}개 AND 흔한 낱말 {len(common):,}개 → 겹치는 문서 {len(want)}개")
    print(f"흔한 낱말 목록은 128개 묶음 {total:,}개")
    print(f"  두 손가락 한 칸씩      : 묶음 {b1:,}개를 풀어 봄")
    print(f"  짧은 쪽 앞세워 건너뛰기: 묶음 {b2:,}개를 풀어 봄, 건너뛰기 표 {s2:,}칸을 봄")
