"""Elasticsearch 15편 그림 만들기. 실행: python lab/fig_es15.py  → docs/elasticsearch/img/15/*.svg

본문 절은 장면 띠로 그린다: 같은 무대를 여러 장 그리고 장마다 바뀐 곳만 빨강으로 칠한다.
예시는 1편의 쇼핑몰 문의 게시판(글 20,000개)에서 "비밀번호를 잊어버렸어요"로 3번 글
"암호 재설정은 어디서 하나요"를 찾는 장면을 편 끝까지 잇는다(.claude/writing/work/cal/units-es15.md).
점 지도는 2차원 점 120개로 lab/es/15_hnsw.py 의 HNSW를 실제로 만들어 걷는 길을 계산한다.
"""
import heapq
import importlib
import math
import os
import random
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "es"))
from figkit import (GREY, INK, LIGHT, NOTE, PAPER, PINK, RED, arrow, board, box, bubble,  # noqa: E402
                    canvas, cell, cells, cylinder, label, moral, outdir, save, stage)
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
def opening(ax, step):
    cylinder(ax, *CYL, "ES (역색인)")
    x, y, w, h = CYL
    label(ax, x + w / 2, y + 0.85, "낱말 → 글 번호", fs=10.5, color=INK)
    if step == 1:
        board(ax, POSTS, query=QUERY, footer=None)
        footer(ax, "글 20,000개")
        bubble(ax, *SAY, "'비밀번호'나 '잊어버렸어요'가\n든 글을 찾아요", TAIL)
    else:
        board(ax, POSTS, query=QUERY, miss=(3,), footer=None)
        footer(ax, "검색 결과 0건", hot=True)
        bubble(ax, *SAY, "두 낱말 중 하나라도\n든 글이 없어요", TAIL, hot=True)
        moral(ax, 4.0, 0.2, "낱말이 안 겹치면 역색인으로는 못 찾아요")


# ── 글을 숫자 목록으로 ──────────────────────────────────────────────
def embed(ax, step):
    box(ax, 0.3, 4.75, 3.2, 1.3, fc=NOTE)
    label(ax, 1.9, 5.4, "비밀번호를\n잊어버렸어요", fs=11)
    arrow(ax, (3.6, 5.4), (4.4, 5.4), ms=12)
    box(ax, 4.5, 4.85, 2.4, 1.1, fc=PAPER)
    label(ax, 5.7, 5.4, "임베딩 모델", fs=11, bold=True)
    arrow(ax, (7.0, 5.4), (7.6, 5.4), color=RED if step == 1 else INK, ms=12)
    hot = (0, 1, 2) if step == 1 else ()
    cells(ax, 7.7, 5.1, ["0.12", "-0.80", "0.33", "…"], w=0.95, h=0.6, gap=0.06, hot=hot, fs=10)
    label(ax, 9.65, 4.6, "숫자 목록 = 벡터", fs=10.5, color=RED if step == 1 else INK, bold=step == 1)
    ax.add_patch(Rectangle((0.3, 0.75), 11.4, 3.3, fill=False, ec=GREY, lw=1.0, ls="--"))
    label(ax, 0.5, 3.8, "숫자 목록을 점으로 찍으면", fs=10.5, ha="left", color=INK)
    if step == 1:
        return
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
    moral(ax, 6.0, 0.3, "뜻이 비슷한 글은 숫자 목록도 가까워요")


# ── 전부 재기 ──────────────────────────────────────────────────────
def brute(ax, step):
    head(ax, "점 하나 = 저장된 글 하나 (그림은 120개만)")
    sx, sy = M(Q)
    for p in PTS:
        x, y = M(p)
        ax.plot([sx, x], [sy, y], color=RED if step == 1 else LIGHT, lw=0.6 if step == 1 else 0.8, zorder=1)
    dotmap(ax)
    if step == 1:
        label(ax, 11.7, 0.45, "모든 점과 거리를 재요 (20,000개면 20,000번)", fs=11, color=RED, ha="right", bold=True)
        return
    for i in ORDER[:10]:
        dot(ax, i, s=45)
    label(ax, 9.3, 6.25, "가장 가까운 10개", fs=10.5, color=RED, ha="center", bold=True)
    moral(ax, 6.0, 0.45, "답은 정확하지만 점 수만큼 재요")


# ── 이웃 따라 걷기 ─────────────────────────────────────────────────
def walk(ax, step):
    titles = {1: "가까운 점끼리 이웃으로 이어 둬요 (그래프)", 2: "이웃 중 질문에 가장 가까운 점으로 옮겨요",
              3: f"더 가까운 이웃이 없을 때까지 {len(PATH) - 1}걸음", 4: "후보 2개를 들고 다니면 둘째 후보로 넘어가요"}
    head(ax, titles[step], color=RED if step > 1 else INK)
    dotmap(ax, links=True)
    sx, sy = M(PTS[START])
    ax.scatter([sx], [sy], s=60, color=INK, zorder=4)
    label(ax, sx - 0.05, sy - 0.42, "출발 (1번 글)", fs=10, color=INK, ha="left", bbox=WHITE)
    if step == 2:
        hops(ax, PATH[:2])
    elif step >= 3:
        hops(ax, PATH, color=RED if step == 3 else GREY, lw=1.8 if step == 3 else 1.4)
        x, y = M(PTS[STOP])
        if step == 3:
            dot(ax, STOP, s=55)
            label(ax, x + 0.1, y - 0.45, "멈춘 곳", fs=10.5, color=RED, bold=True, bbox=WHITE)
            moral(ax, 6.0, 0.45, "질문과 먼 곳에서 멈췄어요")
        else:
            label(ax, x + 0.1, y - 0.45, "멈춘 곳", fs=10, color=INK, bbox=WHITE)
            hops(ax, ESCAPE)
            ring(ax, ESCAPE[1])
            ring(ax, NEAR, r=0.2)
            nx, ny = M(PTS[NEAR])
            label(ax, nx - 0.3, ny + 0.38, "3번 글", fs=10.5, color=RED, bold=True, ha="right", bbox=WHITE, zorder=7)
            moral(ax, 6.0, 0.45, "후보를 여럿 들면 막힌 길을 빠져나가요")


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
    walks = [(2, W2), (1, W1), (0, W0)]
    for k, (lvl, seq) in enumerate(walks[:step - 1]):
        now = k == step - 2
        c = RED if now else GREY
        y = LY[lvl]
        if lvl < 2:
            arrow(ax, (seq[0], LY[lvl + 1] - 0.12), (seq[0], y + 0.12), color=c, lw=1.8, ms=12)
        for a, b in zip(seq, seq[1:]):
            if lvl:
                arrow(ax, (a, y + 0.06), (b, y + 0.06), color=c, lw=2.2 if now else 1.6, ms=12, rad=-0.45)
        if lvl == 0:
            arrow(ax, (seq[0] - 0.05, y - 0.25), (seq[-1] + 0.12, y - 0.25), color=c, lw=2.4, ms=12)
        if now and lvl == 0:
            ax.scatter(seq, [y] * len(seq), s=[35] * (len(seq) - 1) + [70], color=RED, zorder=4)
            label(ax, seq[-1] + 0.3, y - 0.42, "3번 글", fs=10.5, color=RED, bold=True, ha="left")
    notes = {1: ("점마다 몇 층까지 올라갈지 무작위로 정해요", INK),
             2: ("위층은 점이 드물어 한 걸음이 길어요", RED),
             3: ("한 층 내려가 그 자리에서 다시 걸어요", RED)}
    if step in notes:
        s, c = notes[step]
        label(ax, 6.0, 0.45, s, fs=11, color=c, bold=c == RED)
    else:
        moral(ax, 6.0, 0.45, "위층에서 크게 건너뛰고 아래층에서 촘촘히 찾아요")


# ── 벡터가 늘어도 일은 조금만 ──────────────────────────────────────
def grow():
    fig, ax = canvas(7.2, 3.8, 12, 6.6)
    label(ax, 0.3, 6.2, "질문 하나에 거리를 재는 횟수 (파이썬, 후보 50개)", fs=11, ha="left", color=INK)
    rows = [("벡터 1,000개", 1_000, 515), ("벡터 5,000개", 5_000, 780), ("벡터 20,000개", 20_000, 953)]
    sc = 8.6 / 20_000
    for k, (name, full, hn) in enumerate(rows):
        y = 4.9 - k * 1.45
        label(ax, 0.3, y, name, fs=10.5, ha="left")
        ax.add_patch(Rectangle((2.6, y + 0.05), full * sc, 0.4, fc=LIGHT, ec=GREY))
        label(ax, 2.6 + full * sc + 0.15, y + 0.25, f"전부 재기 {full:,}번", fs=9.5, ha="left", color=INK)
        ax.add_patch(Rectangle((2.6, y - 0.5), hn * sc, 0.4, fc=PINK, ec=RED))
        label(ax, 2.6 + hn * sc + 0.15, y - 0.3, f"HNSW {hn:,}번", fs=10, ha="left", color=RED, bold=True)
    moral(ax, 6.0, 0.4, "벡터가 20배 늘어도 일은 2배도 안 늘었어요")
    save(fig, OUT, "es15-grow.svg")


# ── 전환: 빨라진 대신 치르는 값 ─────────────────────────────────────
def turn(ax, step):
    """층 그림을 작게 다시 그린 무대. 1장=지금까지 얻은 것(층을 타고 내려와 3번 글), 2장=말풍선으로 대가 세 가지."""
    fx = lambda v: 0.5 + (v - 2.4) * 6.0 / 8.91                       # noqa: E731  층 그림을 왼쪽 절반에
    ty = {2: 5.2, 1: 3.9, 0: 2.6}
    c = GREY if step == 2 else INK
    for lvl in (2, 1, 0):
        xs = [fx(v) for v in LAYER[lvl]]
        ax.plot([xs[0], xs[-1]], [ty[lvl]] * 2, color=LIGHT, lw=1.0, zorder=1)
        ax.scatter(xs, [ty[lvl]] * len(xs), s=10 if lvl == 0 else 22, color=c, zorder=2)
    for lvl, seq in ((2, W2), (1, W1), (0, W0)):
        if lvl < 2:
            arrow(ax, (fx(seq[0]), ty[lvl + 1] - 0.1), (fx(seq[0]), ty[lvl] + 0.1), color=GREY, lw=1.4, ms=9)
        if len(seq) > 1:
            arrow(ax, (fx(seq[0]), ty[lvl] + 0.05), (fx(seq[-1]), ty[lvl] + 0.05), color=GREY, lw=1.4, ms=9, rad=-0.4)
    ex = fx(W0[-1])
    ax.scatter([ex], [ty[0]], s=55, color=RED if step == 1 else GREY, zorder=4)
    label(ax, ex + 0.2, ty[0] + 0.4, "3번 글", fs=10.5, color=RED if step == 1 else GREY, bold=step == 1, ha="left")
    label(ax, 0.3, 6.2, "위층에서 건너뛰고 아래층에서 둘러봤어요", fs=10.5, ha="left", color=c)
    cylinder(ax, 8.4, 3.2, 3.0, 1.5, "ES (HNSW)")
    label(ax, 9.9, 4.0, "층 있는 그래프", fs=10.5, color=INK)
    if step == 1:
        bubble(ax, 7.0, 0.9, 4.8, 1.5, "5,000번 대신 780번만 재고\n정답 10개를 다 찾았어요", (9.9, 2.95), fs=11)
        return
    bubble(ax, 7.2, 0.2, 4.6, 2.4, "", (9.9, 2.95), hot=True)
    label(ax, 9.5, 2.2, "대신 치르는 값이 있어요", fs=11.5, color=RED, bold=True)
    for k, t in enumerate(["① 정답을 놓칠 수 있어요", "② 그래프를 짓느라 색인이 무거워요", "③ 벡터가 메모리에 들어가야 빨라요"]):
        label(ax, 7.4, 1.7 - k * 0.5, t, fs=10, ha="left", color=RED)


# ── 첫째 값: 후보 수와 정답 ────────────────────────────────────────
def tradeoff(ax, step):
    ef = [10, 20, 50, 100, 200]
    work = [284, 431, 780, 1217, 1840]
    hits = [8.8, 9.5, 10.0, 10.0, 10.0]
    base, sc = 1.3, 3.9 / 5000
    label(ax, 0.3, 6.25, "벡터 5,000개, 질문 하나에 거리를 재는 횟수 (파이썬)", fs=11, ha="left", color=INK)
    ax.plot([0.9, 11.6], [base + 5000 * sc] * 2, color=INK, lw=1.3, ls="--")
    label(ax, 11.6, base + 5000 * sc + 0.25, "전부 재기 5,000번", fs=10, ha="right", color=INK)
    ax.plot([0.9, 11.6], [base, base], color=INK, lw=1.2)
    for k, (e, wk, ht) in enumerate(zip(ef, work, hits)):
        x = 1.5 + k * 2.05
        ax.add_patch(Rectangle((x, base), 1.3, wk * sc, fc=LIGHT, ec=GREY))
        label(ax, x + 0.65, base + wk * sc + 0.25, f"{wk:,}번", fs=10, color=INK)
        label(ax, x + 0.65, base - 0.3, f"후보 {e}개", fs=10, color=INK)
        if step == 2:
            miss = ht < 10
            label(ax, x + 0.65, base + wk * sc + 0.7, f"정답 {ht:.1f}/10", fs=10.5,
                  color=RED if miss else "#222", bold=miss)
    if step == 2:
        moral(ax, 6.0, 0.3, "후보가 적으면 빠르지만 정답을 놓쳐요")


# ── 첫째 값: k와 num_candidates ────────────────────────────────────
def kc(ax, step):
    head(ax, "num_candidates: 50 → 후보 50개를 모아요" if step == 1 else "k: 10 → 그중 가까운 10개를 돌려줘요",
         color=RED)
    dotmap(ax, dim=True)
    for i in KC50:
        if step == 1:
            ring(ax, i, r=0.14, lw=1.4)
        else:
            ring(ax, i, color=GREY, r=0.14, lw=1.0)
    if step == 2:
        for i in KC50[:10]:
            dot(ax, i, s=45)
        moral(ax, 6.0, 0.45, "후보를 넉넉히 모을수록 정답을 덜 놓쳐요")


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


def build(ax, step):
    for name, x, ps in (("세그먼트 _0", 0.3, SEG0), ("세그먼트 _1", 4.2, SEG1)):
        box(ax, x, 3.2, 3.6, 2.5, fc=NOTE)
        label(ax, x + 0.15, 6.0, name, fs=10.5, ha="left", bold=True)
        graph(ax, ps, nn_links(ps))
    near = sorted(range(len(SEG1)), key=lambda j: (SEG1[j][0] - NEW[0]) ** 2 + (SEG1[j][1] - NEW[1]) ** 2)[:2]
    c = RED if step == 1 else GREY
    for j in near:
        ax.plot([NEW[0], SEG1[j][0]], [NEW[1], SEG1[j][1]], color=c, lw=1.8 if step == 1 else 1.2, zorder=1)
    ax.scatter([NEW[0]], [NEW[1]], s=50 if step == 1 else 22, color=RED if step == 1 else INK, zorder=3)
    if step == 1:
        label(ax, 6.0, 2.45, "새 벡터를 넣을 때마다\n가까운 점을 찾아 이어요", fs=10.5, color=RED, bold=True)
        ax.add_patch(Rectangle((8.3, 3.2), 3.4, 2.5, fill=False, ec=GREY, lw=1.0, ls="--"))
        label(ax, 10.0, 4.45, "합친 세그먼트", fs=10, color=GREY)
        return
    box(ax, 8.3, 3.2, 3.4, 2.5, fc=PINK, ec=RED)
    label(ax, 8.45, 6.0, "합친 세그먼트", fs=10.5, ha="left", bold=True, color=RED)
    merged = [(8.3 + (p[0] - 0.3) * 3.2 / 7.5, p[1]) for p in SEG0 + SEG1 + [NEW]]
    graph(ax, merged, nn_links(merged), color=RED, pc=RED)
    arrow(ax, (2.1, 3.1), (8.9, 2.6), color=RED, lw=1.8, ms=12, rad=0.25)
    arrow(ax, (6.0, 3.1), (9.4, 3.0), color=RED, lw=1.8, ms=12, rad=0.2)
    label(ax, 4.6, 1.75, "합칠 때 벡터를 다시 넣어 이어요 (5편)", fs=10.5, color=RED)
    moral(ax, 6.0, 0.5, "그래프를 짓고 다시 잇느라 색인이 무거워요")


# ── 셋째 값: 벡터가 메모리에 들어가야 빨라요 ───────────────────────
def memory(ax, step):
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
    label(ax, 9.95, 3.45, "메모리", fs=10.5, bold=True)
    label(ax, 9.95, 2.2, "파일 캐시\n(메모리에서\n힙을 뺀 몫)", fs=10, color=INK)
    if step == 1:
        label(ax, 3.9, 2.3, "벡터가 1,000만 개라면?", fs=11, color=INK)
        return
    for k in range(5):
        y = 3.5 - k * 0.48
        if k == 3:
            label(ax, 3.0, y + 0.18, "⋮", fs=12, color=RED)
            continue
        ax.add_patch(Rectangle((0.3, y), 5.4, 0.36, fc=PINK, ec=RED, lw=1.2))
    label(ax, 5.9, 2.6, "× 1,000만 개\n≈ 30 GB", fs=11, ha="left", color=RED, bold=True)
    arrow(ax, (7.4, 2.4), (8.1, 2.4), color=RED, ms=12)
    moral(ax, 6.0, 0.35, "벡터가 파일 캐시에 다 들어가야 빨라요")


# ── 심화: 압축과 다시 재기 ─────────────────────────────────────────
def quant(ax, step):
    label(ax, 0.3, 6.2, "벡터 하나의 숫자 세 개", fs=11, ha="left", color=INK)
    label(ax, 0.3, 5.3, "원래 값", fs=10.5, ha="left", color=INK)
    for k in range(3):
        for b in range(4):
            cell(ax, 2.4 + k * 2.6 + b * 0.5, 5.0, 0.46, 0.55, "", fs=8)
    label(ax, 10.4, 5.27, "숫자 하나 = 4바이트", fs=10, ha="left", color=INK)
    hot2 = step == 2
    if step >= 2:
        label(ax, 0.3, 3.95, "int8 사본", fs=10.5, ha="left", color=RED if hot2 else INK, bold=hot2)
        for k in range(3):
            cell(ax, 2.4 + k * 2.6, 3.65, 0.46, 0.55, "", hot=hot2, fs=8)
        label(ax, 10.4, 3.92, "숫자 하나 = 1바이트", fs=10, ha="left", color=RED if hot2 else INK, bold=hot2)
    if step == 1:
        label(ax, 6.0, 2.3, "그래프를 걸으며 거리를 잴 때마다 이 값을 읽어요", fs=10.5, color=INK)
    elif step == 2:
        label(ax, 6.0, 2.6, "그래프는 사본으로 걸어요. 읽는 양이 4분의 1", fs=11, color=RED, bold=True)
        label(ax, 6.0, 1.9, "원래 값은 디스크에 남겨 둬요. 거리가 조금씩 틀려요", fs=10.5, color=INK)
    else:
        label(ax, 6.0, 2.75, "① 사본으로 k의 3배를 찾아요", fs=10.5, color=INK)
        arrow(ax, (3.6, 3.55), (3.6, 4.95), color=RED, lw=1.8, ms=12)
        label(ax, 3.85, 4.4, "②", fs=10.5, color=RED, ha="left")
        label(ax, 6.0, 2.05, "② 원래 값으로 다시 재서 순위를 고쳐요 (rescore_vector)", fs=10.5, color=RED, bold=True)
        moral(ax, 6.0, 1.1, "적게 읽고 찾은 뒤 원래 값으로 바로잡아요")


# ── 언제 쓸모 있을까요 ─────────────────────────────────────────────
def decide():
    fig, ax = canvas(10, 4.2, 15, 6.0)
    box(ax, 0.3, 4.4, 4.4, 1.2, fc=NOTE)
    label(ax, 2.5, 5.0, "낱말이 달라도\n뜻으로 찾아야 하나요?", fs=11, bold=True)
    box(ax, 5.6, 4.4, 4.4, 1.2, fc=NOTE)
    label(ax, 7.8, 5.0, "글자가 꼭 맞아야 하는\n검색어도 많나요?", fs=11, bold=True)
    box(ax, 10.9, 4.4, 3.8, 1.2, fc=PINK, ec=RED)
    label(ax, 12.8, 5.0, "역색인 검색과\n벡터 검색을 섞어요", fs=11, color=RED, bold=True)
    arrow(ax, (4.8, 5.0), (5.5, 5.0)); label(ax, 5.15, 5.45, "예", fs=10, color=INK)
    arrow(ax, (10.1, 5.0), (10.8, 5.0), color=RED); label(ax, 10.45, 5.45, "예", fs=10, color=RED)
    arrow(ax, (2.5, 4.3), (2.5, 2.9)); label(ax, 2.85, 3.6, "아니요", fs=10, color=INK, ha="left")
    arrow(ax, (7.8, 4.3), (7.8, 2.9)); label(ax, 8.15, 3.6, "아니요", fs=10, color=INK, ha="left")
    box(ax, 0.3, 0.6, 4.4, 2.2, fc=LIGHT, ec=GREY)
    label(ax, 2.5, 1.7, "역색인 검색 (1편·8편)\n예: '환불'이 든\n문의 글 찾기", fs=10.5)
    box(ax, 5.6, 0.6, 4.4, 2.2, fc=LIGHT, ec=GREY)
    label(ax, 7.8, 1.7, "벡터 검색\n예: '비밀번호를 잊어버렸어요'로\n비슷한 문의 찾기", fs=10.5)
    label(ax, 12.8, 3.6, "예: '아이폰 15 프로 256GB'", fs=10, color=INK)
    save(fig, OUT, "es15-decide.svg")


# ── 정리: 처음 장면으로 돌아가기 ───────────────────────────────────
def back(ax, step):
    board(ax, POSTS, query=QUERY, hot=(3,) if step == 3 else (), dim=(1, 2, 4) if step == 3 else (), footer=None)
    footer(ax, "검색 결과 0건" if step == 1 else "글 20,000개")
    x, y, w, h = CYL
    if step == 1:
        ry = 4.15 - 2 * 0.55                                           # 3번 줄: 그때 못 찾은 글(회색)
        ax.add_patch(Rectangle((0.85, ry - 0.24), 5.9, 0.48, fill=False, ec=GREY, lw=1.5, ls="--"))
        label(ax, 6.45, ry, "✗", fs=13, color=GREY, bold=True)
        cylinder(ax, *CYL, "ES (역색인)")
        label(ax, x + w / 2, y + 0.85, "낱말 → 글 번호", fs=10.5, color=INK)
        bubble(ax, *SAY, "처음엔 낱말이 안 겹쳐\n0건이었어요", TAIL)
        return
    cylinder(ax, *CYL, "ES (HNSW)", ec=RED if step == 2 else INK, color=RED if step == 2 else "#222")
    label(ax, x + w / 2, y + 0.85, "층 있는 그래프", fs=10.5, color=RED if step == 2 else INK)
    if step == 2:
        bubble(ax, *SAY, "질문을 숫자 목록으로 바꿔\n위층부터 질문 근처로 내려가요", TAIL, hot=True)
    else:
        arrow(ax, (x - 0.05, y + 0.6), (6.8, 3.06), color=RED, ms=14)
        bubble(ax, *SAY, "가장 가까운 글은\n3번 글이에요", TAIL, hot=True)
        moral(ax, 4.0, 0.2, "낱말이 안 겹쳐도 뜻이 가까운 글을 찾아요")


# ── 정리: 낱말 카드 ────────────────────────────────────────────────
def cards():
    """이 편 본문에서 이름 붙인 말 여덟. 카드마다 본문 그림을 작게 다시 그리고 한 줄 뜻을 단다. 휴대폰 폭에 맞게 두 장씩."""
    fig, ax = canvas(6.4, 10.4, 9.8, 16.25)
    W, H = 4.6, 3.8

    def card(i, name, line):
        col, row = i % 2, i // 2
        x, y = 0.2 + col * 4.9, 12.25 - row * 4.05
        box(ax, x, y, W, H, fc="white")
        label(ax, x + 0.25, y + H - 0.4, name, fs=12.5, ha="left", bold=True)
        label(ax, x + W / 2, y + 0.6, line, fs=10, color=INK)
        return x, y

    x, y = card(0, "임베딩 모델", "문장을 받아\n숫자 목록을 내주는 모델")
    box(ax, x + 0.3, y + 1.75, 1.3, 0.6, fc=NOTE, lw=1.2)
    label(ax, x + 0.95, y + 2.05, "문장", fs=9.5)
    arrow(ax, (x + 1.7, y + 2.05), (x + 2.3, y + 2.05), color=RED, ms=10)
    cells(ax, x + 2.4, y + 1.75, ["0.12", "…"], w=0.85, h=0.6, gap=0.05, hot=(0,), fs=9)
    x, y = card(1, "벡터", "글을 바꾼 숫자 목록")
    cells(ax, x + 0.4, y + 1.75, ["0.12", "-0.80", "0.33", "…"], w=0.9, h=0.6, gap=0.05, hot=(0, 1, 2), fs=9)
    x, y = card(2, "차원", "벡터에 든 숫자 개수\n(보통 수백~수천)")
    cells(ax, x + 0.4, y + 1.75, ["1", "2", "3", "…", "768"], w=0.7, h=0.6, gap=0.05, hot=(0, 1, 2, 4), fs=9.5)
    x, y = card(3, "정확한 검색", "모든 벡터와 거리를 재기\n(script_score)")
    cx, cy = x + 2.3, y + 2.05
    for k in range(8):
        a = k * math.pi / 4
        px, py = cx + 1.3 * math.cos(a), cy + 0.6 * math.sin(a)
        ax.plot([cx, px], [cy, py], color=RED, lw=1.0)
        ax.scatter([px], [py], s=10, color=INK, zorder=3)
    ax.scatter([cx], [cy], s=110, marker="*", color=RED, zorder=4)
    x, y = card(4, "그래프", "가까운 점끼리\n이웃으로 이어 둔 그물")
    gp = [(x + 0.6, y + 1.7), (x + 1.5, y + 2.45), (x + 2.4, y + 1.8), (x + 3.2, y + 2.5), (x + 4.0, y + 1.75)]
    for (a, b) in ((0, 1), (1, 2), (0, 2), (2, 3), (3, 4), (2, 4)):
        ax.plot([gp[a][0], gp[b][0]], [gp[a][1], gp[b][1]], color=RED, lw=1.4)
    ax.scatter([p[0] for p in gp], [p[1] for p in gp], s=22, color=INK, zorder=3)
    x, y = card(5, "HNSW", "그래프를 층으로 쌓아\n위에서 크게, 아래에서 촘촘히")
    for k, n in enumerate((2, 4, 8)):
        yy = y + 2.7 - k * 0.45
        xs = [x + 0.6 + j * 3.4 / (n - 1) for j in range(n)]
        ax.plot([xs[0], xs[-1]], [yy, yy], color=GREY, lw=1.0)
        ax.scatter(xs, [yy] * n, s=14, color=INK, zorder=3)
    arrow(ax, (x + 0.6, y + 2.7), (x + 4.0, y + 2.7), color=RED, lw=1.6, ms=9, rad=-0.3)
    arrow(ax, (x + 4.0, y + 2.65), (x + 4.0, y + 1.85), color=RED, lw=1.6, ms=9)
    x, y = card(6, "num_candidates", "그래프를 걸을 때\n들고 다니는 후보 수")
    for k in range(6):
        ax.add_patch(Circle((x + 0.7 + k * 0.62, y + 2.05), 0.2, fill=False, ec=RED, lw=1.5))
    label(ax, x + 4.3, y + 2.05, "…", fs=11, color=RED)
    x, y = card(7, "k", "후보 중 돌려받을\n가까운 개수")
    for k in range(6):
        on = k < 3
        ax.add_patch(Circle((x + 0.7 + k * 0.62, y + 2.05), 0.2, fc=RED if on else "white",
                            ec=RED if on else GREY, lw=1.5))
    save(fig, OUT, "es15-cards.svg")


if __name__ == "__main__":
    S, L = (7.2, 3.8), (12, 6.6)
    SM, LM = (7.2, 4.2), (12, 7.0)
    stage(opening, 2, OUT, "es15-open", S, L)
    stage(embed, 2, OUT, "es15-embed", S, L)
    stage(brute, 2, OUT, "es15-brute", SM, LM)
    stage(walk, 4, OUT, "es15-walk", SM, LM)
    stage(layers, 4, OUT, "es15-layers", S, L)
    grow()
    stage(turn, 2, OUT, "es15-turn", S, L)
    stage(tradeoff, 2, OUT, "es15-tradeoff", S, L)
    stage(kc, 2, OUT, "es15-kc", SM, LM)
    stage(build, 2, OUT, "es15-build", S, L)
    stage(memory, 2, OUT, "es15-memory", S, L)
    stage(quant, 3, OUT, "es15-quant", S, L)
    decide()
    stage(back, 3, OUT, "es15-back", S, L)
    cards()
    print("걸음", len(PATH) - 1, "멈춘 곳", STOP, "가장 가까운 점", NEAR, "빠져나간 길", ESCAPE)
