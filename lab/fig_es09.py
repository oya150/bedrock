"""Elasticsearch 9편 그림 만들기. 실행: python lab/fig_es09.py  → docs/elasticsearch/img/09/*.svg

예시는 검색어 rare common, 맞는 문서 20만 개를 편 끝까지 잇는다.
WAND·묶음 그림의 점수(문턱 4.2, common 1.2, rare 8.5)는 설명용으로 정한 숫자다.
그림 안 글씨는 낱말과 숫자만 둔다. 문장은 본문과 그림 설명에 둔다.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "es"))
from figkit import (GREY, INK, LIGHT, NOTE, PAPER, PINK, RED, arrow, box,  # noqa: E402
                    canvas, cell, cylinder, label, magnifier, outdir, save)
from matplotlib.patches import Rectangle  # noqa: E402

OUT = outdir("09")
S, L = (7.2, 3.8), (12, 6.6)
CYL = (8.0, 2.4, 3.6, 2.0)
ROWS = ["1위 문서", "2위 문서", "⋮", "10위 문서"]
GTE = '"value": 10000, "relation": "gte"'


def figure(name, draw, size=S, lim=L):
    fig, ax = canvas(*size, *lim)
    draw(ax)
    save(fig, OUT, name)


# ── 여는 장면: 검색 화면과 ES ─────────────────────────────────────
def opening(ax):
    box(ax, 0.3, 1.55, 6.7, 4.85, fc="white", round_=False)
    ax.add_patch(Rectangle((0.3, 5.95), 6.7, 0.45, fc=LIGHT, ec=INK, lw=1.2))
    label(ax, 0.5, 6.17, "검색 화면", fs=11, ha="left", color=INK)
    ax.add_patch(Rectangle((0.55, 5.2), 4.8, 0.5, fc="white", ec=INK, lw=1.2))
    magnifier(ax, 0.8, 5.47)
    label(ax, 1.1, 5.45, "rare common", fs=12, ha="left")
    ax.add_patch(Rectangle((5.45, 5.2), 1.3, 0.5, fc=LIGHT, ec=INK, lw=1.2))
    label(ax, 6.1, 5.45, "검색", fs=11.5)
    label(ax, 0.6, 4.72, "건수", fs=11, ha="left", color=INK)
    ax.add_patch(Rectangle((1.3, 4.45), 5.6, 0.55, fc=PINK, ec=RED, lw=1.6))
    label(ax, 1.4, 4.72, GTE, fs=10.5, ha="left", color=RED, bold=True)
    ax.plot([0.55, 6.75], [4.3, 4.3], color=INK, lw=1.0)
    for k, t in enumerate(ROWS):
        y = 3.95 - k * 0.55
        if t == "⋮":
            label(ax, 3.65, y, t, fs=12, color=INK)
            continue
        label(ax, 0.75, y, t, fs=11.5, ha="left")
        ax.plot([0.55, 6.75], [y - 0.27, y - 0.27], color=GREY, lw=0.8)
    x, y, w, h = CYL
    cylinder(ax, *CYL, "ES")
    label(ax, x + w / 2, y + 1.3, "맞는 문서", fs=11)
    label(ax, x + w / 2, y + 0.7, "200,000개", fs=12, bold=True)
    arrow(ax, (7.9, 3.4), (7.1, 3.4), color=INK, ms=14)
    label(ax, 7.5, 3.8, "10개", fs=10, color=INK)


# ── 1절: 힙으로 위 10개 고르기 (그림은 위 3개로 줄임) ─────────────
def heap(ax):
    label(ax, 0.3, 6.2, "위 3개 (힙)", fs=11.5, ha="left", bold=True)
    tx, ty, nw, nh = 2.6, 4.1, 1.2, 0.75
    kids = [(1.1, 2.55), (4.1, 2.55)]
    for kx, ky in kids:
        ax.plot([tx + nw / 2, kx + nw / 2], [ty, ky + nh], color=INK, lw=1.2)
    cell(ax, tx, ty, nw, nh, "4.2", hot=True, fs=12)
    cell(ax, *kids[0], nw, nh, "6.0", fs=12)
    cell(ax, *kids[1], nw, nh, "7.5", fs=12)
    label(ax, tx - 0.15, ty + nh / 2, "문턱", fs=11, ha="right", color=RED, bold=True)
    box(ax, 8.2, 4.5, 2.6, 0.8, fc=LIGHT, ec=GREY)
    label(ax, 9.5, 4.9, "새 문서 3.1", fs=11, color=INK)
    label(ax, 9.5, 4.05, "버림", fs=10.5, color=INK)
    box(ax, 8.2, 2.6, 2.6, 0.8, fc=PINK, ec=RED)
    label(ax, 9.5, 3.0, "새 문서 5.1", fs=11, color=RED, bold=True)
    arrow(ax, (8.1, 3.0), (tx + nw + 0.1, ty + 0.25), color=RED, ms=14)
    label(ax, 9.5, 2.15, "4.2를 밀어냄", fs=10.5, color=RED)
    label(ax, 6.0, 0.9, "문턱 4.2 → 5.1", fs=12.5, color=RED, bold=True)


# ── 2절: 목록 두 줄 (common, rare) ────────────────────────────────
LX, LW, LS = 2.3, 0.9, 1.0
CY, RY = 4.3, 2.9


def cx(d):
    return LX + (d - 1) * LS


def lists(ax, dim_skipped=False, hot_rare=False):
    label(ax, 0.3, CY + 0.5, "common", fs=11, ha="left", bold=True)
    label(ax, 0.3, CY + 0.1, "최고 1.2", fs=10, ha="left", color=INK)
    label(ax, 0.3, RY + 0.5, "rare", fs=11, ha="left", bold=True)
    label(ax, 0.3, RY + 0.1, "최고 8.5", fs=10, ha="left", color=INK)
    for d in range(1, 8):
        both = d in (3, 6)
        cell(ax, cx(d), CY, LW, 0.7, d, hot=both and hot_rare, dim=dim_skipped and not both, fs=12)
        if both:
            cell(ax, cx(d), RY, LW, 0.7, d, hot=hot_rare, fs=12)


def wand_skip(ax):
    label(ax, 0.3, 6.2, "rare common · 문턱 4.2", fs=11.5, ha="left", bold=True)
    lists(ax, dim_skipped=True, hot_rare=True)
    for d in (1, 2, 4, 5, 7):
        label(ax, cx(d) + LW / 2, CY - 0.3, "건너뜀", fs=9.5, color=INK)
    for d in (3, 6):
        label(ax, cx(d) + LW / 2, RY - 0.3, "계산", fs=10, color=RED, bold=True)
    label(ax, 6.0, 1.45, "common만: 최고 1.2 < 4.2 → 건너뜀", fs=11, color=INK)
    label(ax, 6.0, 0.85, "둘 다: 최고 1.2 + 8.5 = 9.7 > 4.2 → 계산", fs=11, color=RED, bold=True)


def wand_leap(ax):
    label(ax, 0.3, 6.2, "rare common · 문턱 4.2", fs=11.5, ha="left", bold=True)
    lists(ax, dim_skipped=True)
    s0 = LX - 0.25
    a3, b3, a6 = cx(3) + 0.3, cx(3) + 0.6, cx(6) + 0.3
    arrow(ax, (s0, RY - 0.1), (a3, RY - 0.1), color=RED, rad=0.35, ms=13, lw=1.6)
    label(ax, (s0 + a3) / 2, RY - 0.85, "①", fs=11, color=RED, bold=True)
    arrow(ax, (b3, RY - 0.1), (a6, RY - 0.1), color=RED, rad=0.35, ms=13, lw=1.6)
    label(ax, (b3 + a6) / 2, RY - 0.85, "③", fs=11, color=RED, bold=True)
    arrow(ax, (s0, CY + 0.8), (a3, CY + 0.8), color=RED, rad=-0.35, ms=13, lw=1.6)
    label(ax, (s0 + a3) / 2, CY + 1.5, "② advance(3)", fs=10, color=RED)
    arrow(ax, (b3, CY + 0.8), (a6, CY + 0.8), color=RED, rad=-0.35, ms=13, lw=1.6)
    label(ax, (b3 + a6) / 2, CY + 1.5, "④ advance(6)", fs=10, color=RED)
    label(ax, 10.7, CY + 0.35, "1 2 4 5 7\n안 밟음", fs=10.5, color=INK)
    label(ax, 6.0, 0.95, "rare가 앞장 · common은 따라감", fs=11.5, color=RED, bold=True)


# ── 3절: 묶음마다 최고 점수 (block-max) ───────────────────────────
BX = [0.3, 4.2, 8.1]
BW = 3.6
BLOCKS = [("0.6", "3.0", "3.6", False), ("1.2", "8.5", "9.7", True), ("0.7", "2.9", "3.6", False)]


def blocks(ax, step):
    label(ax, 0.3, 6.2, "문턱 4.2 · 128개씩 묶음", fs=11.5, ha="left", bold=True)
    label(ax, 11.7, 6.2, "c: common만, r: rare도", fs=10, ha="right", color=INK)
    for k, (x, (c, r, s, opn)) in enumerate(zip(BX, BLOCKS)):
        skipped = step == 2 and not opn
        box(ax, x, 3.4, BW, 1.9, fc=LIGHT if skipped else NOTE, ec=GREY if skipped else INK)
        label(ax, x + 0.15, 5.0, f"묶음 {k + 1}", fs=10.5, ha="left", bold=True, color=GREY if skipped else "#222")
        for j in range(5):
            cell(ax, x + 0.2 + j * 0.65, 3.65, 0.58, 0.7, "r" if j == 2 else "c", dim=skipped, fs=10.5)
        if step == 1:
            label(ax, x + BW / 2, 2.85, "1.2 + 8.5 = 9.7", fs=10.5, color=RED, bold=True)
            label(ax, x + BW / 2, 2.3, "열어 봄", fs=10.5, color=RED)
        else:
            label(ax, x + BW / 2, 2.85, f"{c} + {r} = {s}", fs=10.5, color=INK if opn else RED, bold=not opn)
            label(ax, x + BW / 2, 2.3, "열어 봄" if opn else "통째로 건너뜀", fs=10.5,
                  color=INK if opn else RED, bold=not opn)
    if step == 1:
        label(ax, 6.0, 1.2, "목록 전체의 최고 점수로 따짐", fs=11.5, color=INK)
    else:
        label(ax, 6.0, 1.2, "묶음마다 그 안의 최고 점수로 따짐", fs=11.5, color=INK)


# ── 4절: 건너뛴 문서는 세지 않아요 ────────────────────────────────
def tally(ax):
    label(ax, 0.3, 6.2, "rare common · 맞는 문서 7개", fs=11.5, ha="left", bold=True)
    lists(ax, dim_skipped=True, hot_rare=True)
    box(ax, 9.6, 3.3, 2.1, 1.6, fc=PINK, ec=RED)
    label(ax, 10.65, 4.5, "센 건수", fs=11, color=RED)
    label(ax, 10.65, 3.8, "2", fs=16, color=RED, bold=True)
    label(ax, 6.0, 1.45, "건너뜀: 1 2 4 5 7 → 세지 않음", fs=11, color=INK)
    label(ax, 6.0, 0.85, "계산: 3 6 → 2건", fs=11, color=RED, bold=True)


def counts(ax):
    label(ax, 0.3, 6.2, "맞는 문서 20만 개 · 한 칸 = 1만 개", fs=11.5, ha="left", bold=True)
    label(ax, 11.7, 6.2, "빨강 = 세며 계산", fs=10, ha="right", color=RED)
    rows = [("true", 20, "200,000 (eq)"), ("기본값", 1, "10,000 (gte)"), ("false", 0, "세지 않음")]
    for k, (name, n, out) in enumerate(rows):
        y = 4.7 - k * 1.45
        on = k == 1
        label(ax, 0.3, y + 0.35, name, fs=11.5, ha="left", color=RED if on else "#222", bold=True)
        for i in range(20):
            cell(ax, 1.9 + i * 0.36, y, 0.32, 0.7, "", hot=i < n, fc=None if i < n else "white")
        label(ax, 9.3, y + 0.35, out, fs=11, ha="left", color=RED if on else "#222", bold=on)
    label(ax, 0.3, 0.35, "track_total_hits", fs=10.5, ha="left", color=INK, family="monospace")


# ── 5절: 다 봐야 하는 요청 ─────────────────────────────────────────
def fullscan(ax):
    box(ax, 0.3, 1.3, 6.4, 4.8, fc=PAPER)
    label(ax, 0.55, 5.75, "검색 요청", fs=11, ha="left", bold=True)
    for k, t in enumerate(["query: rare common", "size: 10"]):
        label(ax, 0.6, 5.1 - k * 0.6, t, fs=10.5, ha="left", family="monospace")
    for k, (t, note) in enumerate([("+ aggs", "집계"), ("+ function_score", "점수 섞기")]):
        y = 3.3 - k * 1.2
        ax.add_patch(Rectangle((0.55, y), 5.9, 0.6, fc=PINK, ec=RED, lw=1.5))
        label(ax, 0.7, y + 0.3, t, fs=10.5, ha="left", color=RED, bold=True, family="monospace")
        label(ax, 6.3, y + 0.3, note, fs=10, ha="right", color=RED)
    label(ax, 3.5, 2.95, "또는", fs=10, color=INK)
    x, y, w, h = CYL
    cylinder(ax, *CYL, "ES")
    label(ax, x + w / 2, y + 1.3, "건너뛰기", fs=11, color=RED, bold=True)
    label(ax, x + w / 2, y + 0.7, "꺼짐", fs=12, color=RED, bold=True)
    arrow(ax, (6.8, 3.4), (7.9, 3.4), color=RED, ms=14)
    label(ax, x + w / 2, 1.3, "맞는 문서 전부 계산", fs=10.5, color=INK)


# ── 6절: 갈림길 ───────────────────────────────────────────────────
def decide():
    fig, ax = canvas(10, 4.2, 15, 6.0)
    box(ax, 0.3, 4.4, 4.6, 1.2, fc=NOTE)
    label(ax, 2.6, 5.0, "정확한 총 건수\n필요?", fs=11.5, bold=True)
    box(ax, 7.0, 4.4, 7.7, 1.2, fc=LIGHT, ec=GREY)
    label(ax, 10.85, 5.0, "기본값 그대로\n\"1만 건 이상\"", fs=10.5)
    arrow(ax, (5.0, 5.0), (6.9, 5.0))
    label(ax, 5.95, 5.35, "아니요", fs=10, color=INK)
    arrow(ax, (2.6, 4.3), (2.6, 3.0))
    label(ax, 2.9, 3.65, "예", fs=10, color=INK, ha="left")
    box(ax, 0.3, 0.8, 4.6, 2.1, fc=NOTE)
    label(ax, 2.6, 1.85, "몇 건까지?", fs=11.5, bold=True)
    arrow(ax, (5.0, 2.2), (6.9, 2.75))
    label(ax, 5.9, 2.9, "10만 건까지", fs=10, color=INK)
    box(ax, 7.0, 2.25, 7.7, 1.0, fc=LIGHT, ec=GREY)
    label(ax, 10.85, 2.75, "track_total_hits: 100000", fs=10.5, family="monospace")
    arrow(ax, (5.0, 1.5), (6.9, 1.05), color=RED)
    label(ax, 5.9, 0.95, "끝까지", fs=10, color=RED)
    box(ax, 7.0, 0.55, 7.7, 1.0, fc=PINK, ec=RED)
    label(ax, 10.85, 1.05, "필요한 화면에서만 true", fs=10.5, color=RED, bold=True)
    save(fig, OUT, "es09-decide.svg")


if __name__ == "__main__":
    figure("es09-open.svg", opening)
    figure("es09-heap.svg", heap)
    figure("es09-wand-1.svg", wand_skip)
    figure("es09-wand-2.svg", wand_leap)
    figure("es09-block-1.svg", lambda ax: blocks(ax, 1))
    figure("es09-block-2.svg", lambda ax: blocks(ax, 2))
    figure("es09-tally.svg", tally)
    figure("es09-counts.svg", counts)
    figure("es09-full.svg", fullscan)
    decide()
