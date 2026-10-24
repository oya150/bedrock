"""Elasticsearch 15편: 가까운 벡터 찾기를 전부 비교하는 방법과 HNSW 그래프로 하는 방법으로 해 보고 일을 센다.

실행: python lab/es/15_hnsw.py          (벡터 5,000개, 후보 수별)
      python lab/es/15_hnsw.py sizes    (벡터 1,000·5,000·20,000개, 후보 50개, 1분쯤 걸림)
벡터 5,000개(16차원)에서 질의 벡터마다 가장 가까운 10개를 찾는다.
1) 전부 비교: 5,000개 모두와 거리를 잰다. 답이 정확하다.
2) HNSW(Malkov·Yashunin 2016): 층이 있는 이웃 그래프를 만들고 위층에서 크게 건너뛴 뒤 맨 아래층에서
   후보 ef개를 들고 이웃을 따라가며 찾는다. 거리를 재는 횟수가 훨씬 적지만 가끔 정답을 놓친다.
"""
import heapq
import math
import random
import sys

random.seed(15)
N, DIM, M, EF_BUILD, K = 5_000, 16, 16, 100, 10


def dist(a, b):
    return sum((x - y) ** 2 for x, y in zip(a, b))


class HNSW:
    def __init__(self, m=M, ef_build=EF_BUILD):
        self.m, self.ef_build = m, ef_build
        self.vecs, self.levels, self.links = [], [], []   # links[node][층] = 이웃 목록
        self.entry, self.top = None, -1
        self.count = 0                                      # 거리 계산 횟수

    def d(self, q, i):
        self.count += 1
        return dist(q, self.vecs[i])

    def search_layer(self, q, starts, ef, layer):
        seen = set(starts)
        cand = [(self.d(q, s), s) for s in starts]          # 아직 둘러볼 후보(가까운 순)
        heapq.heapify(cand)
        best = [(-dd, s) for dd, s in cand]                 # 지금까지 찾은 가까운 ef개(먼 것이 위)
        heapq.heapify(best)
        while cand:
            dd, c = heapq.heappop(cand)
            if dd > -best[0][0] and len(best) >= ef:
                break                                       # 후보가 지금 ef개 중 가장 먼 것보다 멀면 멈춤
            for nb in self.links[c][layer]:
                if nb in seen:
                    continue
                seen.add(nb)
                dn = self.d(q, nb)
                if len(best) < ef or dn < -best[0][0]:
                    heapq.heappush(cand, (dn, nb))
                    heapq.heappush(best, (-dn, nb))
                    if len(best) > ef:
                        heapq.heappop(best)
        return sorted((-nd, n) for nd, n in best)

    def add(self, v):
        i = len(self.vecs)
        self.vecs.append(v)
        lvl = int(-math.log(1 - random.random()) / math.log(self.m))   # 위층일수록 드물게
        self.levels.append(lvl)
        self.links.append([[] for _ in range(lvl + 1)])
        if self.entry is None:
            self.entry, self.top = i, lvl
            return
        cur = [self.entry]
        for layer in range(self.top, lvl, -1):              # 새 점의 층보다 위에서는 가장 가까운 하나만 따라 내려감
            cur = [self.search_layer(v, cur, 1, layer)[0][1]]
        for layer in range(min(lvl, self.top), -1, -1):
            near = self.search_layer(v, cur, self.ef_build, layer)
            cap = self.m * 2 if layer == 0 else self.m
            for _, nb in near[:self.m]:
                self.links[i][layer].append(nb)
                self.links[nb][layer].append(i)
                if len(self.links[nb][layer]) > cap:        # 이웃이 넘치면 가까운 것만 남김
                    self.links[nb][layer] = sorted(self.links[nb][layer],
                                                   key=lambda x: dist(self.vecs[nb], self.vecs[x]))[:cap]
            cur = [n for _, n in near]
        if lvl > self.top:
            self.entry, self.top = i, lvl

    def query(self, q, k, ef):
        cur = [self.entry]
        for layer in range(self.top, 0, -1):
            cur = [self.search_layer(q, cur, 1, layer)[0][1]]
        return [n for _, n in self.search_layer(q, cur, max(ef, k), 0)[:k]]


def sizes():
    for n in (1_000, 5_000, 20_000):
        random.seed(15)
        data = [[random.gauss(0, 1) for _ in range(DIM)] for _ in range(n)]
        queries = [[random.gauss(0, 1) for _ in range(DIM)] for _ in range(50)]
        g = HNSW()
        for v in data:
            g.add(v)
        g.count, hit = 0, 0
        for q in queries:
            exact = set(sorted(range(n), key=lambda i: dist(q, data[i]))[:K])
            hit += len(exact & set(g.query(q, K, 50)))
        print(f"벡터 {n:>6,}개, 후보 50개: 질의마다 거리 계산 평균 {g.count // len(queries):,}번, "
              f"정답 10개 중 평균 {hit / len(queries):.1f}개")


if __name__ == "__main__" and sys.argv[1:] == ["sizes"]:
    sizes()
elif __name__ == "__main__":
    data = [[random.gauss(0, 1) for _ in range(DIM)] for _ in range(N)]
    queries = [[random.gauss(0, 1) for _ in range(DIM)] for _ in range(50)]
    g = HNSW()
    for v in data:
        g.add(v)
    per_level = [sum(1 for l in g.levels if l >= k) for k in range(g.top + 1)]
    print(f"벡터 {N:,}개({DIM}차원), 이웃 수 M={M}: 층별 점 수 {per_level} (맨 아래층부터)")
    print(f"그래프를 만드는 데 거리 계산 {g.count:,}번")
    print(f"전부 비교: 질의마다 거리 계산 {N:,}번, 정답 10개 중 10개")
    for ef in (10, 20, 50, 100, 200):
        g.count, hit = 0, 0
        for q in queries:
            exact = set(sorted(range(N), key=lambda i: dist(q, data[i]))[:K])
            got = g.query(q, K, ef)
            hit += len(exact & set(got))
        print(f"HNSW 후보 {ef:>3}개: 질의마다 거리 계산 평균 {g.count // len(queries):,}번, "
              f"정답 10개 중 평균 {hit / len(queries):.1f}개")
