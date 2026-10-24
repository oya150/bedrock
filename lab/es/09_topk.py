"""Elasticsearch 9편: 상위 k개 힙과 묶음별 최고 점수(block-max)로 계산을 건너뛰는 모습을 센다.

실행: python lab/es/09_topk.py
'rare OR common' 검색. common은 모든 문서에, rare는 1%에 있다.
1) 모든 문서 점수를 계산하고 힙으로 상위 10개를 고른다
2) 힙 맨 아래 점수(문턱)를 넘을 수 없는 128개 묶음은 점수를 계산하지 않고 건너뛴다
   묶음을 건너뛸지는 '그 묶음에서 나올 수 있는 최고 점수' = common의 묶음 최고 점수 + (rare가 있으면 rare 최고 점수)로 정한다
"""
import heapq
import random

random.seed(9)
N, BLOCK, K = 200_000, 128, 10

common = [random.uniform(0.2, 1.0) for _ in range(N)]               # 문서마다 common 점수
rare = {d: random.uniform(4.0, 8.0) for d in random.sample(range(N), N // 100)}   # 1% 문서의 rare 점수
block_max_common = [max(common[i:i + BLOCK]) for i in range(0, N, BLOCK)]
rare_blocks = {d // BLOCK for d in rare}
RARE_MAX = 8.0


def score(d):
    return common[d] + rare.get(d, 0.0)


def exhaustive():
    heap = []
    for d in range(N):
        s = score(d)
        if len(heap) < K:
            heapq.heappush(heap, s)
        elif s > heap[0]:
            heapq.heapreplace(heap, s)
    return sorted(heap, reverse=True), N


def block_max():
    heap = []
    scored = 0
    for b in range(0, N, BLOCK):
        bi = b // BLOCK
        upper = block_max_common[bi] + (RARE_MAX if bi in rare_blocks else 0.0)
        if len(heap) == K and upper <= heap[0]:
            continue                                   # 이 묶음에서는 문턱을 넘을 문서가 나올 수 없다
        for d in range(b, min(b + BLOCK, N)):
            if len(heap) == K and block_max_common[bi] + rare.get(d, 0.0) <= heap[0]:
                continue                               # 이 문서도 문턱을 못 넘는다(rare가 없으면 common만으로는 안 됨)
            s = score(d)
            scored += 1
            if len(heap) < K:
                heapq.heappush(heap, s)
            elif s > heap[0]:
                heapq.heapreplace(heap, s)
    return sorted(heap, reverse=True), scored


if __name__ == "__main__":
    top1, n1 = exhaustive()
    top2, n2 = block_max()
    assert top1 == top2
    print(f"문서 {N:,}개, rare 문서 {len(rare):,}개, 상위 {K}개")
    print(f"  모두 계산: 점수 계산 {n1:,}번")
    print(f"  묶음 최고 점수로 건너뛰기: 점수 계산 {n2:,}번, 상위 10개는 같음 (10위 점수 {top2[-1]:.3f})")
