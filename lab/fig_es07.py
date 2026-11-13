"""Elasticsearch 7편 그림 만들기. 실행: python lab/fig_es07.py  → docs/elasticsearch/img/07/*.svg

그림은 낱말과 숫자만 두고 지금 볼 곳만 빨강으로 칠한다. 장면 띠는 건너뛰기 표(2장)와 OR 힙(3장)만.
예시는 쇼핑몰 문의 게시판의 "환불 신청" 검색을 편 끝까지 잇는다.
환불 = 글 1천 개(5, 70, 77, ⋯), 신청 = 글 100만 개, 건너뛰기 표 = 12 31 47 66 80 99.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "es"))
from figkit import (GREY, INK, LIGHT, NOTE, PINK, RED, arrow, board, box,  # noqa: E402
                    canvas, cell, cells, cylinder, label, outdir, save, stage)
from matplotlib.patches import Circle, Rectangle  # noqa: E402

OUT = outdir("07")
CYL = (8.0, 3.0, 3.6, 1.7)
W, G = 0.85, 0.08


def empty(ax, x, y, w, h, s="", fs=10):
    ax.add_patch(Rectangle((x, y), w, h, fc="white", ec=GREY, lw=1.0, ls="--"))
    if s:
        label(ax, x + w / 2, y + h / 2, s, fs=fs, color=GREY)


def cx(x0, i, w=W, g=G):
    """칸 줄에서 i번째 칸의 가운데 x."""
    return x0 + i * (w + g) + w / 2


def finger(ax, x, y, up=False, color=RED):
    ax.plot([x], [y], marker="^" if up else "v", ms=12, color=color)


def hop(ax, a, b, y, color=RED, rad=-0.6, ms=10, lw=1.6):
    arrow(ax, (a, y), (b, y), color=color, rad=rad, ms=ms, lw=lw)


# ── 여는 장면: 게시판 + ES 원통 ───────────────────────────────────
BAR_X, BAR_W = 8.85, 2.6


def opening():
    fig, ax = canvas(7.2, 3.8, 12, 6.6)
    board(ax, [], query="환불 신청", footer="⋮   글 1천만 개")
    cylinder(ax, *CYL, "ES")
    label(ax, 8.2, 4.3, "환불", fs=10.5, ha="left")
    ax.add_patch(Rectangle((BAR_X, 4.18), 0.12, 0.24, fc=LIGHT, ec=INK, lw=1.2))
    label(ax, BAR_X + 0.25, 4.3, "1천 개", fs=9.5, ha="left", color=INK)
    label(ax, 8.2, 3.45, "신청", fs=10.5, ha="left", color=RED, bold=True)
    ax.add_patch(Rectangle((BAR_X, 3.33), BAR_W, 0.24, fc=PINK, ec=RED, lw=1.2))
    label(ax, BAR_X + BAR_W / 2, 3.45, "100만 개", fs=9, color=RED)
    arrow(ax, (BAR_X, 3.1), (BAR_X + BAR_W, 3.1), color=RED, ms=11, lw=1.6)
    label(ax, BAR_X + BAR_W / 2, 2.3, "처음부터 끝까지", fs=10, color=RED, bold=True)
    save(fig, OUT, "es07-open.svg")


# ── 두 손가락은 긴 목록을 다 걸어요 ────────────────────────────────
REF = ["5", "70", "77", "⋯"]
APP = ["0", "1", "2", "4", "5", "6", "⋯", "69", "72", "⋯"]
X0 = 1.6


def walk():
    fig, ax = canvas(7.2, 3.3, 12, 5.4)
    label(ax, 0.3, 4.3, "환불", fs=12, ha="left", bold=True)
    label(ax, 0.3, 2.3, "신청", fs=12, ha="left", bold=True)
    cells(ax, X0, 3.9, REF, w=W, h=0.8, gap=G, hot=(1,), dim=(0,), fs=12)
    cells(ax, X0, 1.9, APP, w=W, h=0.8, gap=G, hot=(4, 8), fs=12)
    finger(ax, cx(X0, 1), 4.95)
    finger(ax, cx(X0, 8), 1.55, up=True)
    for a in range(0, 8):
        hop(ax, cx(X0, a) + 0.1, cx(X0, a + 1) - 0.1, 2.8)
    label(ax, 6.0, 0.8, "한 칸씩: 0 → 1 → 2 → ⋯ → 72", fs=12, color=RED, bold=True)
    save(fig, OUT, "es07-walk.svg")


# ── 짧은 목록이 앞장서요 ───────────────────────────────────────────
APP2 = ["⋯", "66", "67", "68", "69", "72", "⋯"]


def lead():
    fig, ax = canvas(7.2, 3.6, 12, 6.0)
    label(ax, 0.3, 4.7, "환불", fs=12, ha="left", bold=True, color=RED)
    label(ax, 0.3, 4.25, "1천 개", fs=10, ha="left", color=RED)
    label(ax, 0.3, 2.3, "신청", fs=12, ha="left", bold=True)
    label(ax, 0.3, 1.85, "100만 개", fs=10, ha="left", color=INK)
    cells(ax, X0, 4.1, REF, w=W, h=0.8, gap=G, hot=(1, 2), dim=(0,), fs=12)
    cells(ax, X0, 1.7, APP2, w=W, h=0.8, gap=G, hot=(5,), fs=12)
    a70, a72, a77 = (cx(X0, 1), 4.0), (cx(X0, 5), 2.6), (cx(X0, 2), 4.0)
    arrow(ax, a70, a72, color=RED, ms=14)
    arrow(ax, (a72[0] - 0.15, a72[1] + 0.1), (a77[0] + 0.2, a77[1]), color=RED, ms=14, rad=0.25)
    label(ax, 6.0, 5.4, "환불이 앞장", fs=11.5, color=RED, bold=True)
    label(ax, 8.4, 4.4, "① advance(70) → 72", fs=11.5, ha="left", color=RED)
    label(ax, 8.4, 3.8, "   70 탈락", fs=11, ha="left", color=INK)
    label(ax, 8.4, 3.2, "② advance(72) → 77", fs=11.5, ha="left", color=RED)
    save(fig, OUT, "es07-lead.svg")


# ── 건너뛰기 표로 껑충 ─────────────────────────────────────────────
TBL = ["12", "31", "47", "66", "80", "99"]
RANGES = ["0…12", "13…31", "32…47", "48…66", "67…80", "81…99"]
TX, TW, TG = 2.4, 1.2, 0.08
OPEN5 = ["67", "68", "69", "72", "⋯", "80"]


def leap(ax, step):
    """step 1: 표만 보고 묶음 2~4를 넘어 묶음 5를 고른다. step 2: 묶음 5만 풀어 72를 찾는다."""
    label(ax, 0.2, 5.85, "환불", fs=11.5, ha="left", bold=True)
    cells(ax, TX, 5.55, REF, w=0.75, h=0.6, gap=0.08, hot=(1,), dim=(0,), fs=11)
    label(ax, 6.0, 5.85, "advance(70)", fs=11.5, ha="left", color=RED, bold=True)
    label(ax, 0.2, 4.4, "건너뛰기 표", fs=11, ha="left", bold=True)
    hot_t = (1, 2, 3, 4) if step == 1 else ()
    cells(ax, TX, 4.1, TBL, w=TW, h=0.6, gap=TG, hot=hot_t, dim=(5,), fs=11.5)
    label(ax, 0.2, 2.85, "신청 묶음", fs=11, ha="left", bold=True)
    for k, r in enumerate(RANGES):
        x = TX + k * (TW + TG)
        skip = k in (1, 2, 3, 5)
        hot = k == 4
        fc, ec = (PINK, RED) if hot else ((LIGHT, GREY) if skip else (NOTE, INK))
        ax.add_patch(Rectangle((x, 2.45), TW, 0.8, fc=fc, ec=ec, lw=1.8 if hot else 1.1))
        c = RED if hot else (GREY if skip else "#222")
        label(ax, x + TW / 2, 3.03, f"묶음 {k + 1}", fs=9.5, color=c, bold=hot)
        label(ax, x + TW / 2, 2.68, r, fs=9.5, color=c)
    x5 = cx(TX, 4, TW, TG)
    hc = RED if step == 1 else GREY
    for a in range(0, 3):
        hop(ax, cx(TX, a, TW, TG) + 0.15, cx(TX, a + 1, TW, TG) - 0.15, 4.8, color=hc, rad=-0.5, ms=11)
    arrow(ax, (x5, 4.0), (x5, 3.35), color=hc, ms=13)
    if step == 1:
        label(ax, 6.0, 1.5, "31, 47, 66 < 70 → 묶음 2~4 넘어감", fs=12, color=RED, bold=True)
        label(ax, 6.0, 0.8, "80 ≥ 70 → 묶음 5만 풂", fs=12, color=RED, bold=True)
    else:
        arrow(ax, (x5, 2.35), (x5 - 0.3, 1.78), color=RED, ms=12)
        cells(ax, 5.3, 1.15, OPEN5, w=0.68, h=0.55, gap=0.06, hot=(3,), fs=10.5)
        finger(ax, cx(5.3, 3, 0.68, 0.06), 0.95, up=True)
        label(ax, 5.1, 1.42, "70 이상 첫 번호: 72", fs=11, color=RED, ha="right")


# ── 첫째: OR는 힙으로 ──────────────────────────────────────────────
OR_LISTS = [("환불", [3, 9, 14]), ("교환", [5, 9, 21]), ("반품", [8, 30])]
OR_ROWS = [5.0, 3.85, 2.7]
NODES = [(6.7, 4.75), (6.0, 3.45), (7.4, 3.45)]
RES = [3, 5, 8, 9, 14, 21, 30]


def node(ax, xy, v, hot=False, gone=False):
    if gone:
        ax.add_patch(Circle(xy, 0.36, fc="white", ec=GREY, lw=1.0, ls="--"))
        return
    ax.add_patch(Circle(xy, 0.36, fc=PINK if hot else NOTE, ec=RED if hot else INK, lw=1.8 if hot else 1.2))
    label(ax, xy[0], xy[1], v, fs=12, color=RED if hot else "#222", bold=hot)


def orheap(ax, step):
    """step 1: 세 목록 맨 앞 번호를 힙에. step 2: 3을 꺼내고 환불의 9를 넣음. step 3: 다 끝남."""
    pos = {1: [0, 0, 0], 2: [1, 0, 0]}.get(step)
    for (name, vals), y, k in zip(OR_LISTS, OR_ROWS, range(3)):
        label(ax, 0.3, y + 0.35, name, fs=11.5, ha="left", bold=True)
        hot = (pos[k],) if (step == 1 or (step == 2 and k == 0)) else ()
        dim = tuple(range(len(vals))) if step == 3 else ((0,) if step == 2 and k == 0 else ())
        cells(ax, 1.3, y, vals, w=0.8, h=0.7, gap=0.08, hot=hot, dim=dim, fs=12)
        if pos:
            finger(ax, cx(1.3, pos[k], 0.8, 0.08), y + 0.88, color=RED if hot else INK)
    label(ax, 6.7, 5.65, "힙", fs=11.5, bold=True)
    for a, b in ((0, 1), (0, 2)):
        ax.plot([NODES[a][0], NODES[b][0]], [NODES[a][1], NODES[b][1]], color=INK, lw=1.2, zorder=0)
    if step == 1:
        for xy, v in zip(NODES, [3, 5, 8]):
            node(ax, xy, v, hot=True)
        label(ax, 8.3, 4.1, "맨 위 3\n= 가장 작은 번호", fs=10.5, ha="left", color=RED)
    elif step == 2:
        node(ax, NODES[0], 5)
        node(ax, NODES[1], 8)
        node(ax, NODES[2], 9, hot=True)
        label(ax, 8.3, 4.1, "3 꺼냄\n9 넣음", fs=10.5, ha="left", color=RED)
    else:
        for xy in NODES:
            node(ax, xy, "", gone=True)
        label(ax, 8.3, 4.1, "9는 한 번만", fs=10.5, ha="left", color=INK)
    label(ax, 0.3, 1.35, "결과", fs=11.5, ha="left", bold=True)
    n = {1: 0, 2: 1, 3: 7}[step]
    for k in range(7):
        x = 1.3 + k * 0.88
        if k < n:
            cell(ax, x, 1.0, 0.8, 0.7, RES[k], hot=True, fs=12)
        else:
            empty(ax, x, 1.0, 0.8, 0.7)


# ── 둘째: 구문 검색은 후보마다 위치를 ──────────────────────────────
DOC_A = ["주문", "환불", "요청"]
DOC_B = ["요청", "먼저", "하고", "환불", "대기"]


def phrase():
    fig, ax = canvas(7.2, 3.8, 12, 6.6)
    ax.add_patch(Rectangle((0.3, 5.75), 3.6, 0.6, fc="white", ec=INK, lw=1.2))
    label(ax, 2.1, 6.05, "\"환불 요청\"", fs=12)
    label(ax, 4.2, 6.05, "구문 검색 (match_phrase)", fs=11, ha="left", color=INK)
    label(ax, 0.3, 5.15, "① AND로 남은 후보", fs=11, ha="left", color=INK)
    for words, y in ((DOC_A, 3.9), (DOC_B, 2.3)):
        box(ax, 0.4, y - 0.25, 6.6, 1.15, fc="white", ec=INK, lw=1.2)
        for k, wd in enumerate(words):
            on = wd in ("환불", "요청")
            cell(ax, 0.6 + k * 1.25, y + 0.1, 1.15, 0.6, wd, hot=on, fs=11)
            label(ax, 0.6 + k * 1.25 + 0.575, y - 0.08, str(k), fs=9.5, color=RED if on else GREY)
    label(ax, 0.3, 1.25, "② 후보에서만 위치 읽기", fs=11, ha="left", color=RED, bold=True)
    label(ax, 7.3, 4.25, "1 → 2  붙음 ✓", fs=11.5, ha="left", color=RED, bold=True)
    label(ax, 7.3, 2.65, "0 … 3  떨어짐 ✗", fs=11.5, ha="left", color=INK)
    save(fig, OUT, "es07-phrase.svg")


# ── 건너뛰기는 언제 쓸모 있을까요 ─────────────────────────────────
def decide():
    fig, ax = canvas(10, 4.2, 15, 6.0)
    box(ax, 0.3, 4.4, 4.4, 1.2, fc=NOTE)
    label(ax, 2.5, 5.0, "모두 맞아야?\n(AND)", fs=11.5, bold=True)
    box(ax, 5.6, 4.4, 4.4, 1.2, fc=NOTE)
    label(ax, 7.8, 5.0, "드문 조건이\n하나라도?", fs=11.5, bold=True)
    box(ax, 10.9, 4.4, 3.8, 1.2, fc=PINK, ec=RED)
    label(ax, 12.8, 5.0, "드문 쪽이 앞장\n쓴 순서 상관없음", fs=10.5, color=RED, bold=True)
    arrow(ax, (4.8, 5.0), (5.5, 5.0)); label(ax, 5.15, 5.45, "예", fs=10, color=INK)
    arrow(ax, (10.1, 5.0), (10.8, 5.0), color=RED); label(ax, 10.45, 5.45, "예", fs=10, color=RED)
    arrow(ax, (2.5, 4.3), (2.5, 2.9)); label(ax, 2.85, 3.6, "아니요 (OR)", fs=10, color=INK, ha="left")
    arrow(ax, (7.8, 4.3), (7.8, 2.9)); label(ax, 8.15, 3.6, "아니요", fs=10, color=INK, ha="left")
    box(ax, 0.3, 0.6, 4.4, 2.2, fc=LIGHT, ec=GREY)
    label(ax, 2.5, 1.7, "목록 전부 걷기\n값이 많으면\nfilter + terms", fs=10.5)
    box(ax, 5.6, 0.6, 4.4, 2.2, fc=LIGHT, ec=GREY)
    label(ax, 7.8, 1.7, "흔한 조건끼리\n앞장부터 김\n느림", fs=10.5)
    save(fig, OUT, "es07-decide.svg")


if __name__ == "__main__":
    S, L = (7.2, 3.8), (12, 6.6)
    opening()
    walk()
    lead()
    stage(leap, 2, OUT, "es07-leap", S, L)
    stage(orheap, 3, OUT, "es07-or", S, L)
    phrase()
    decide()
