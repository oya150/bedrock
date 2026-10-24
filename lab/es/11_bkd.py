"""Elasticsearch 11편: 숫자 범위 검색을 역색인 방식과 BKD 방식으로 했을 때의 일을 센다.

실행: python lab/es/11_bkd.py
상품 100만 개의 가격(100원 단위, 서로 다른 값이 많음)에서 '1만 원 이상 5만 원 이하'를 찾는다.
1) 역색인 방식: 가격 값마다 문서 목록이 있으니 범위 안의 서로 다른 값을 하나씩 꺼내 목록을 합친다
2) BKD(1차원) 방식: (가격, 문서) 쌍을 가격순으로 정렬해 512개씩 잎 칸에 담고 칸마다 최솟값·최댓값을 적어 둔다
   범위에 완전히 들어가는 칸은 안을 보지 않고 통째로 담고, 걸치는 칸만 하나씩 확인하고, 밖의 칸은 건너뛴다
"""
import random

random.seed(11)
N, LEAF = 1_000_000, 512


def run(name, values, lo, hi):
    # 1) 역색인: 값 → 문서 목록
    inv = {}
    for d, p in enumerate(values):
        inv.setdefault(p, []).append(d)
    terms_in_range = [v for v in sorted(inv) if lo <= v <= hi]
    hits1 = sorted(d for v in terms_in_range for d in inv[v])

    # 2) BKD 1차원: 값순 정렬 → 잎 칸
    pairs = sorted((p, d) for d, p in enumerate(values))
    leaves = [pairs[i:i + LEAF] for i in range(0, N, LEAF)]
    inside = crossing = outside = checked = 0
    hits2 = []
    for leaf in leaves:
        leaf_min, leaf_max = leaf[0][0], leaf[-1][0]      # 칸마다 적어 둔 최솟값·최댓값
        if leaf_max < lo or leaf_min > hi:
            outside += 1
        elif lo <= leaf_min and leaf_max <= hi:
            inside += 1
            hits2.extend(d for _, d in leaf)            # 칸 안은 비교 없이 통째로
        else:
            crossing += 1
            for p, d in leaf:
                checked += 1
                if lo <= p <= hi:
                    hits2.append(d)
    hits2.sort()
    assert hits1 == hits2
    print(f"{name}: 문서 {N:,}개, 서로 다른 값 {len(inv):,}종 → 범위에 맞는 문서 {len(hits1):,}개")
    print(f"  역색인 방식: 범위 안의 서로 다른 값 {len(terms_in_range):,}개의 목록을 꺼내 합침")
    print(f"  BKD 방식: 잎 칸 {len(leaves):,}개 중 통째로 담기 {inside:,}, 하나씩 확인 {crossing:,}(값 {checked:,}개), 건너뛰기 {outside:,}")


if __name__ == "__main__":
    prices = [random.randrange(1, 2000) * 100 for _ in range(N)]          # 100원 단위 가격, 값 종류 2천 개쯤
    run("가격 1만~5만 원", prices, 10_000, 50_000)
    stamps = random.sample(range(10 * N), N)                                 # 밀리초 시각처럼 값이 거의 다 다름
    run("시각 범위(값이 다 다름)", stamps, 2 * N, 4 * N)
