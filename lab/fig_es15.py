"""Elasticsearch 15편 그림 만들기. 실행: python lab/fig_es15.py  → docs/elasticsearch/img/15/*.svg

그림은 열 장이다(쉬운 글 정책, 2026-11-13). 그림 안 글씨는 낱말과 숫자만 둔다.
예시는 1편의 쇼핑몰 문의 게시판(글 20,000개)에서 "비밀번호를 잊어버렸어요"로 3번 글
"암호 재설정은 어디서 하나요"를 찾는 장면을 편 끝까지 잇는다.
점 지도는 2차원 점 120개로 lab/es/15_hnsw.py 의 HNSW를 실제로 만들어 걷는 길을 계산한다.
"""
import heapq
import importlib
import os
import random
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "es"))
from figkit import (GREY, INK, NOTE, PAPER, PINK, RED, arrow, board, box,  # noqa: E402
                    canvas, cell, cells, cylinder, label, outdir, save, stage)
from matplotlib.patches import Circle, Rectangle  # noqa: E402

hnsw = importlib.import_module("15_hnsw")
OUT = outdir("15")

QUERY = "비밀번호를 잊어버렸어요"
POSTS = [(1, "주문 환불 요청"), (2, "주문 배송 언제"), (3, "암호 재설정은 어디서 하나요"), (4, "사이즈 교환 문의"), None]
CYL = (8.0, 3.0, 3.6, 1.7)
SAY = (7.2, 0.55, 4.5, 1.3)
TAIL = (9.8, 2.75)

# ── 점 지도: 점 120개, 이웃 4개, 질문 (8.7, 5.4) ───────────────────
random.seed(7)
PTS = [[random.uniform(0, 10), random.uniform(0, 6)] for _ in range(120)]
G = hnsw.HNSW(m=4, ef_build=20)
for _p in PTS:
    G.add(_p)
Q = [8.7, 5.4]
START = min(range(len(PTS)), key=lambda i: hnsw.dist(PTS[i], [0.6, 0.8]))   # 1번 글 "주문 환불 요청"


def qd(i):
    return hnsw.dist(PTS[i], Q)


ORDER = sorted(range(len(PTS)), key=qd)
NEAR = ORDER[0]                                                            # 3번 글 "암호 재설정은 어디서 하나요"


def greedy():
    path, cur = [START], START
    while True:
        nxt = min(G.links[cur][0] + [cur], key=qd)
        if nxt == cur:
            return path
        path.append(nxt)
        cur = nxt


def beam(ef):
    """15_hnsw.search_layer 와 같은 규칙으로 맨 아래층을 걷고, 찾은 점과 그 점에 처음 닿은 부모를 돌려준다."""
    seen, parent = {START}, {START: None}
    cand, best = [(qd(START), START)], [(-qd(START), START)]
    while cand:
        dd, c = heapq.heappop(cand)
        if dd > -best[0][0] and len(best) >= ef:
            break
        for nb in G.links[c][0]:
            if nb in seen:
                continue
            seen.add(nb)
            parent[nb] = c
            dn = qd(nb)
            if len(best) < ef or dn < -best[0][0]:
                heapq.heappush(cand, (dn, nb))
                heapq.heappush(best, (-dn, nb))
                if len(best) > ef:
                    heapq.heappop(best)
    return sorted((-x, n) for x, n in best), parent


PATH = greedy()
STOP = PATH[-1]
RES2, PARENT2 = beam(2)
_tail = [NEAR]
while PARENT2[_tail[-1]] not in PATH:
    _tail.append(PARENT2[_tail[-1]])
ESCAPE = [STOP] + _tail[::-1]                                              # 멈춘 곳 → 둘째 후보 → … → 가장 가까운 점

# 그림이 본문과 맞는지 확인: 걸을수록 가까워지고, 멈춘 곳의 이웃은 모두 더 멀고, 후보 2개면 가장 가까운 점에 닿는다
assert all(qd(a) > qd(b) for a, b in zip(PATH, PATH[1:]))
assert all(qd(n) > qd(STOP) for n in G.links[STOP][0])
assert STOP != NEAR and RES2[0][1] == NEAR
assert all(b in G.links[a][0] for a, b in zip(PATH, PATH[1:])) and all(b in G.links[a][0] for a, b in zip(ESCAPE, ESCAPE[1:]))
KC50 = [n for _, n in G.search_layer(Q, [START], 50, 0)]                   # 후보 50개(가까운 순)
assert len(KC50) == 50 and set(KC50[:10]) == set(ORDER[:10])


WHITE = dict(fc="white", ec="none", pad=1.5)


def M(p):
    return 0.6 + p[0] * 1.08, 1.15 + p[1] * 0.8


def dotmap(ax, links=False, star=True, dim=False):
    if links:
        for i, p in enumerate(PTS):
            for j in G.links[i][0]:
                if i < j:
                    a, b = M(p), M(PTS[j])
                    ax.plot([a[0], b[0]], [a[1], b[1]], color=GREY, lw=0.8, zorder=1)
    xs, ys = zip(*(M(p) for p in PTS))
    ax.scatter(xs, ys, s=12, color=GREY if dim else INK, zorder=2)
    if star:
        sx, sy = M(Q)
        ax.scatter([sx], [sy], s=220, marker="*", color=RED, zorder=6)
        label(ax, sx + 0.35, sy - 0.02, "질문", fs=10.5, color=RED, ha="left", bold=True, bbox=WHITE, zorder=7)


def ring(ax, i, color=RED, r=0.17, lw=1.8):
    x, y = M(PTS[i])
    ax.add_patch(Circle((x, y), r, fill=False, ec=color, lw=lw, zorder=5))


def dot(ax, i, color=RED, s=40):
    x, y = M(PTS[i])
    ax.scatter([x], [y], s=s, color=color, zorder=5)


def hops(ax, seq, color=RED, lw=1.8):
    for a, b in zip(seq, seq[1:]):
        arrow(ax, M(PTS[a]), M(PTS[b]), color=color, lw=lw, ms=10)


def head(ax, s, color=INK):
    label(ax, 0.3, 6.65, s, fs=11, ha="left", color=color, bold=color == RED)


def footer(ax, s, hot=False):
    label(ax, 3.8, 0.88, s, fs=11.5, color=RED if hot else INK, bold=hot)


# ── 여는 장면: 낱말이 안 겹쳐서 못 찾아요 ──────────────────────────
def opening():
    fig, ax = canvas(7.2, 3.8, 12, 6.6)
    cylinder(ax, *CYL, "ES (역색인)")
    x, y, w, h = CYL
    label(ax, x + w / 2, y + 0.85, "낱말 → 글 번호", fs=10.5, color=INK)
    board(ax, POSTS, query=QUERY, miss=(3,), footer=None)
    footer(ax, "검색 결과 0건", hot=True)
    label(ax, x + w / 2, 2.2, "비밀번호 ✗", fs=11, color=RED, bold=True)
    label(ax, x + w / 2, 1.6, "잊어버렸어요 ✗", fs=11, color=RED, bold=True)
    save(fig, OUT, "es15-open.svg")


# ── 글을 숫자 목록으로 ──────────────────────────────────────────────
def embed():
    fig, ax = canvas(7.2, 3.8, 12, 6.6)
    box(ax, 0.3, 4.75, 3.2, 1.3, fc=NOTE)
    label(ax, 1.9, 5.4, "비밀번호를\n잊어버렸어요", fs=11)
    arrow(ax, (3.6, 5.4), (4.4, 5.4), ms=12)
    box(ax, 4.5, 4.85, 2.4, 1.1, fc=PAPER)
    label(ax, 5.7, 5.4, "임베딩 모델", fs=11, bold=True)
    arrow(ax, (7.0, 5.4), (7.6, 5.4), ms=12)
    cells(ax, 7.7, 5.1, ["0.12", "-0.80", "0.33", "…"], w=0.95, h=0.6, gap=0.06, fs=10)
    label(ax, 9.65, 4.6, "벡터", fs=10.5, color=INK)
    ax.add_patch(Rectangle((0.3, 0.75), 11.4, 3.3, fill=False, ec=GREY, lw=1.0, ls="--"))
    label(ax, 0.5, 3.8, "벡터를 찍은 점", fs=10.5, ha="left", color=INK)
    sx, sy = 9.6, 2.9
    nx, ny = 8.6, 2.2
    fx, fy = 1.6, 1.5
    ax.plot([sx, nx], [sy, ny], color=RED, lw=2.0)
    ax.plot([sx, fx], [sy, fy], color=GREY, lw=1.4, ls="--")
    ax.scatter([sx], [sy], s=240, marker="*", color=RED, zorder=5)
    label(ax, sx + 0.3, sy + 0.05, "질문", fs=10.5, color=RED, ha="left", bold=True)
    ax.scatter([nx, fx], [ny, fy], s=50, color=INK, zorder=5)
    label(ax, nx, ny - 0.4, "3번 글 '암호 재설정은 어디서 하나요'", fs=10, color=RED, ha="center")
    label(ax, fx + 0.2, fy - 0.4, "1번 글 '주문 환불 요청'", fs=10, color=INK, ha="left")
    label(ax, 9.8, 2.3, "가까워요", fs=10, color=RED, ha="left")
    label(ax, 5.2, 2.45, "멀어요", fs=10, color=INK)
    save(fig, OUT, "es15-embed.svg")


# ── 전부 재기 ──────────────────────────────────────────────────────
def brute():
    fig, ax = canvas(7.2, 4.2, 12, 7.0)
    head(ax, "점 하나 = 글 하나 (그림은 120개)")
    sx, sy = M(Q)
    for p in PTS:
        x, y = M(p)
        ax.plot([sx, x], [sy, y], color=RED, lw=0.6, zorder=1)
    dotmap(ax)
    label(ax, 11.7, 0.45, "글 20,000개 → 거리 재기 20,000번", fs=11, color=RED, ha="right", bold=True)
    save(fig, OUT, "es15-brute.svg")


# ── 이웃 따라 걷기 ─────────────────────────────────────────────────
def walk(ax, step):
    head(ax, "후보 1개" if step == 1 else "후보 2개", color=RED)
    dotmap(ax, links=True)
    sx, sy = M(PTS[START])
    ax.scatter([sx], [sy], s=60, color=INK, zorder=4)
    label(ax, sx - 0.05, sy - 0.42, "출발 (1번 글)", fs=10, color=INK, ha="left", bbox=WHITE)
    hops(ax, PATH, color=RED if step == 1 else GREY, lw=1.8 if step == 1 else 1.4)
    x, y = M(PTS[STOP])
    if step == 1:
        dot(ax, STOP, s=55)
        label(ax, x + 0.1, y - 0.45, "멈춘 곳", fs=10.5, color=RED, bold=True, bbox=WHITE)
        return
    label(ax, x + 0.1, y - 0.45, "멈춘 곳", fs=10, color=INK, bbox=WHITE)
    hops(ax, ESCAPE)
    ring(ax, ESCAPE[1])
    ring(ax, NEAR, r=0.2)
    nx, ny = M(PTS[NEAR])
    label(ax, nx - 0.3, ny + 0.38, "3번 글", fs=10.5, color=RED, bold=True, ha="right", bbox=WHITE, zorder=7)


# ── 층 ─────────────────────────────────────────────────────────────
L0 = [round(2.4 + i * 0.33, 2) for i in range(28)]
L1 = [L0[i] for i in (0, 4, 9, 12, 15, 18, 21, 25, 27)]
L2 = [L0[i] for i in (0, 9, 15)]
LAYER = {2: L2, 1: L1, 0: L0}
LY = {2: 5.3, 1: 3.75, 0: 2.2}
TARGET = 9.85


def line_walk(xs, start):
    """한 줄 그래프에서 옆 점 중 질문에 가까운 쪽으로 걷는다."""
    k, seq = xs.index(start), [start]
    while True:
        nb = [j for j in (k - 1, k + 1) if 0 <= j < len(xs)]
        j = min(nb, key=lambda j: abs(xs[j] - TARGET))
        if abs(xs[j] - TARGET) >= abs(xs[k] - TARGET):
            return seq
        k = j
        seq.append(xs[k])


W2 = line_walk(L2, L2[0])
W1 = line_walk(L1, W2[-1])
W0 = line_walk(L0, W1[-1])
assert W0[-1] == min(L0, key=lambda x: abs(x - TARGET))


def layers(ax, step):
    names = {2: "2층", 1: "1층", 0: "0층\n(모든 점)"}
    for lvl in (2, 1, 0):
        y, xs = LY[lvl], LAYER[lvl]
        label(ax, 0.3, y, names[lvl], fs=10.5, ha="left", color=INK)
        ax.plot([xs[0], xs[-1]], [y, y], color=GREY, lw=1.2, zorder=1)
        ax.scatter(xs, [y] * len(xs), s=22 if lvl == 0 else 45, color=INK, zorder=3)
        label(ax, 11.8, y + 0.4, f"점 {len(xs)}개", fs=9.5, ha="right", color=INK)
    ax.scatter([TARGET], [1.25], s=220, marker="*", color=RED, zorder=4)
    label(ax, TARGET + 0.3, 1.25, "질문", fs=10.5, color=RED, ha="left", bold=True)
    label(ax, L2[0], LY[2] + 0.42, "입구", fs=10, color=INK)
    if step == 1:
        return
    for lvl, seq in ((2, W2), (1, W1), (0, W0)):
        y = LY[lvl]
        if lvl < 2:
            arrow(ax, (seq[0], LY[lvl + 1] - 0.12), (seq[0], y + 0.12), color=RED, lw=1.8, ms=12)
        for a, b in zip(seq, seq[1:]):
            if lvl:
                arrow(ax, (a, y + 0.06), (b, y + 0.06), color=RED, lw=2.0, ms=12, rad=-0.45)
        if lvl == 0:
            arrow(ax, (seq[0] - 0.05, y - 0.25), (seq[-1] + 0.12, y - 0.25), color=RED, lw=2.2, ms=12)
            ax.scatter([seq[-1]], [y], s=70, color=RED, zorder=4)
            label(ax, seq[-1] + 0.3, y - 0.42, "3번 글", fs=10.5, color=RED, bold=True, ha="left")


# ── 첫째 값: k와 num_candidates ────────────────────────────────────
def kc():
    fig, ax = canvas(7.2, 4.2, 12, 7.0)
    label(ax, 0.3, 6.65, "○ num_candidates 50", fs=11, ha="left", color=INK)
    label(ax, 4.6, 6.65, "● k 10", fs=11, ha="left", color=RED, bold=True)
    dotmap(ax, dim=True)
    for i in KC50:
        ring(ax, i, color=INK, r=0.14, lw=1.0)
    for i in KC50[:10]:
        dot(ax, i, s=45)
    save(fig, OUT, "es15-kc.svg")


# ── 둘째 값: 그래프를 짓고 다시 이어요 ─────────────────────────────
def mini(seed, n, x0, y0, w, h):
    rnd = random.Random(seed)
    return [(x0 + rnd.uniform(0.2, w - 0.2), y0 + rnd.uniform(0.2, h - 0.2)) for _ in range(n)]


def nn_links(ps, k=2):
    out = set()
    for i, p in enumerate(ps):
        near = sorted((j for j in range(len(ps)) if j != i), key=lambda j: (ps[j][0] - p[0]) ** 2 + (ps[j][1] - p[1]) ** 2)
        for j in near[:k]:
            out.add((min(i, j), max(i, j)))
    return out


SEG0 = mini(1, 7, 0.4, 3.3, 3.4, 2.2)
SEG1 = mini(2, 6, 4.3, 3.3, 3.4, 2.2)
NEW = (6.0, 4.4)


def graph(ax, ps, links, color=GREY, pc=INK):
    for i, j in links:
        ax.plot([ps[i][0], ps[j][0]], [ps[i][1], ps[j][1]], color=color, lw=1.2, zorder=1)
    ax.scatter([p[0] for p in ps], [p[1] for p in ps], s=22, color=pc, zorder=2)


def build():
    fig, ax = canvas(7.2, 3.8, 12, 6.6)
    for name, x, ps in (("세그먼트 _0", 0.3, SEG0), ("세그먼트 _1", 4.2, SEG1)):
        box(ax, x, 3.2, 3.6, 2.5, fc=NOTE)
        label(ax, x + 0.15, 6.0, name, fs=10.5, ha="left", bold=True)
        graph(ax, ps, nn_links(ps))
    near = sorted(range(len(SEG1)), key=lambda j: (SEG1[j][0] - NEW[0]) ** 2 + (SEG1[j][1] - NEW[1]) ** 2)[:2]
    for j in near:
        ax.plot([NEW[0], SEG1[j][0]], [NEW[1], SEG1[j][1]], color=RED, lw=1.8, zorder=1)
    ax.scatter([NEW[0]], [NEW[1]], s=50, color=RED, zorder=3)
    label(ax, NEW[0] - 0.25, NEW[1] + 0.3, "새 벡터", fs=10, color=RED, ha="right", bold=True, bbox=WHITE)
    box(ax, 8.3, 3.2, 3.4, 2.5, fc=PINK, ec=RED)
    label(ax, 8.45, 6.0, "병합한 세그먼트", fs=10.5, ha="left", bold=True, color=RED)
    merged = [(8.3 + (p[0] - 0.3) * 3.2 / 7.5, p[1]) for p in SEG0 + SEG1 + [NEW]]
    graph(ax, merged, nn_links(merged), color=RED, pc=RED)
    arrow(ax, (2.1, 3.1), (8.9, 2.6), color=RED, lw=1.8, ms=12, rad=0.25)
    arrow(ax, (6.0, 3.1), (9.4, 3.0), color=RED, lw=1.8, ms=12, rad=0.2)
    label(ax, 4.6, 1.75, "병합 (5편)", fs=10.5, color=RED, bold=True)
    save(fig, OUT, "es15-build.svg")


# ── 셋째 값: 벡터가 메모리에 들어가야 빨라요 ───────────────────────
def memory():
    fig, ax = canvas(7.2, 3.8, 12, 6.6)
    label(ax, 0.3, 6.2, "벡터 하나 (768차원)", fs=11, ha="left", color=INK)
    n = 9
    for k in range(n):
        cell(ax, 0.3 + k * 0.62, 5.2, 0.58, 0.6, "…" if k == n - 2 else "", fs=10)
    label(ax, 0.3 + n * 0.62 + 0.2, 5.5, "768칸", fs=10.5, ha="left", color=INK)
    for k in range(4):
        cell(ax, 0.3 + k * 0.145, 4.45, 0.13, 0.4, "", fs=8)
    label(ax, 0.95, 4.65, "칸 하나 = 4바이트", fs=10, ha="left", color=INK)
    label(ax, 7.6, 4.65, "768 × 4바이트 ≈ 3 KB", fs=10.5, ha="left", color=INK)
    box(ax, 8.2, 0.8, 3.5, 3.0, fc=PAPER)
    label(ax, 9.95, 3.45, "노드 메모리", fs=10.5, bold=True)
    label(ax, 9.95, 2.2, "페이지 캐시\n(힙 밖)", fs=10.5, color=INK)
    for k in range(5):
        y = 3.5 - k * 0.48
        if k == 3:
            label(ax, 3.0, y + 0.18, "⋮", fs=12, color=RED)
            continue
        ax.add_patch(Rectangle((0.3, y), 5.4, 0.36, fc=PINK, ec=RED, lw=1.2))
    label(ax, 5.9, 2.6, "× 1,000만 개\n≈ 30 GB", fs=11, ha="left", color=RED, bold=True)
    arrow(ax, (7.4, 2.4), (8.1, 2.4), color=RED, ms=12)
    save(fig, OUT, "es15-memory.svg")


if __name__ == "__main__":
    opening()
    embed()
    brute()
    stage(walk, 2, OUT, "es15-walk", (7.2, 4.2), (12, 7.0))
    stage(layers, 2, OUT, "es15-layers", (7.2, 3.8), (12, 6.6))
    kc()
    build()
    memory()
    print("걸음", len(PATH) - 1, "멈춘 곳", STOP, "가장 가까운 점", NEAR, "빠져나간 길", ESCAPE)
