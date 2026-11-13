"""Elasticsearch 5편 그림 만들기. 실행: python lab/fig_es05.py  → docs/elasticsearch/img/05/*.svg

예시는 쇼핑몰 문의 게시판의 환불 문의 글 300개를 편 끝까지 잇는다.
세그먼트 _0 = 글 1~100, _1 = 글 101~200, _2 = 글 201~300, 지운 뒤 생긴 _3 = 빈 문서 100.
그림 안 글씨는 낱말과 숫자만 둔다. 문장은 본문과 그림 설명에 둔다.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "es"))
from figkit import (GREY, INK, LIGHT, NOTE, PAPER, PINK, RED, arrow, board, box, bubble,  # noqa: E402
                    canvas, cell, cells, cylinder, label, outdir, save)
from matplotlib.patches import Rectangle  # noqa: E402

OUT = outdir("05")
POSTS = [(1, "환불 문의"), (2, "환불 언제 돼요"), None, (101, "환불 문의"), None, (300, "환불 요청")]
CYL = (8.0, 3.0, 3.6, 1.7)
SEGX = [0.2, 3.05, 5.9, 8.75]
SEGW = 2.7
SIZE, LIM = (7.2, 3.8), (12, 6.6)


def one(draw, name):
    """장면 하나를 그린다. 모든 장면이 같은 틀 크기를 쓴다."""
    fig, ax = canvas(*SIZE, *LIM)
    ax.add_patch(Rectangle((0, 0), *LIM, fill=False, ec="none"))
    draw(ax)
    save(fig, OUT, name)


def empty(ax, x, y, w, h, s="", fs=10):
    ax.add_patch(Rectangle((x, y), w, h, fc="white", ec=GREY, lw=1.0, ls="--"))
    if s:
        label(ax, x + w / 2, y + h / 2, s, fs=fs, color=GREY)


def strike(ax, x, y, w, h):
    ax.plot([x, x + w], [y, y + h], color=GREY, lw=1.4)


def seg(ax, x, y, w, name, items, dead=(), hot=False, h=1.5, fs=10):
    """세그먼트 상자. items=칸 글자, dead=지운 문서 칸(회색 줄), hot=상자 빨강."""
    box(ax, x, y, w, h, fc=PINK if hot else NOTE, ec=RED if hot else INK)
    label(ax, x + 0.15, y + h - 0.3, name, fs=10, ha="left", bold=True, color=RED if hot else "#222")
    n = len(items)
    cw = (w - 0.3 - (n - 1) * 0.1) / n
    for k, t in enumerate(items):
        cx, cy = x + 0.15 + k * (cw + 0.1), y + 0.15
        cell(ax, cx, cy, cw, 0.7, t, dim=k in dead, fs=fs)
        if k in dead:
            strike(ax, cx, cy, cw, 0.7)


def shard4(ax, y=3.9):
    """세그먼트 넷: _0(지운 글), _1, _2, _3(빈 문서)."""
    rows = [("_0", "글 1~100", True), ("_1", "글 101~200", False), ("_2", "글 201~300", False), ("_3", "빈 문서 100", True)]
    for x, (n, t, dead) in zip(SEGX, rows):
        seg(ax, x, y, SEGW, f"세그먼트 {n}", [t], dead=(0,) if dead else ())


# ── 1절: 지웠는데 디스크가 줄지 않아요 ─────────────────────────────
def opening(ax):
    board(ax, POSTS, dim=(1, 2), footer=None)
    label(ax, 3.8, 0.88, "글 300개 → 200개", fs=11.5, color=INK)
    x, y, w, h = CYL
    cylinder(ax, *CYL, "ES")
    label(ax, x + w / 2, y + 1.15, "디스크 ↑", fs=12, color=RED, bold=True)
    label(ax, x + w / 2, y + 0.45, "지운 문서 200", fs=11, color=RED, bold=True)
    bubble(ax, 7.2, 0.55, 4.5, 1.3, "1~100번 지움", (9.8, 2.75))


def mark(ax, step):
    """step 1: 살아 있나 표에 0 / step 2: 검색은 0을 건너뜀."""
    label(ax, 0.2, 4.92, "글", fs=11, ha="left", color=INK)
    label(ax, 0.2, 3.87, "살아\n있나", fs=10.5, ha="left", color=INK)
    for x, name, nums in ((1.4, "세그먼트 _0", ["1", "2", "⋯", "100"]), (6.6, "세그먼트 _1", ["101", "102", "⋯", "200"])):
        box(ax, x, 3.35, 5.0, 2.75, fc=NOTE)
        label(ax, x + 0.15, 5.8, name, fs=10.5, ha="left", bold=True)
        gone = x < 2
        for k, t in enumerate(nums):
            cx = x + 0.2 + k * 1.17
            cell(ax, cx, 4.6, 1.07, 0.65, t, dim=gone, fs=10.5)
            if gone:
                strike(ax, cx, 4.6, 1.07, 0.65)
            alive = "⋯" if t == "⋯" else ("0" if gone else "1")
            cell(ax, cx, 3.55, 1.07, 0.65, alive, hot=(gone and step == 1), fs=11)
    if step == 1:
        label(ax, 6.0, 2.3, "1~100번 지움 → 표에 0", fs=12, color=RED, bold=True)
        label(ax, 6.0, 1.55, "글·역색인은 그대로", fs=11, color=INK)
        return
    ax.add_patch(Rectangle((0.3, 1.85), 1.6, 0.6, fc="white", ec=INK, lw=1.2))
    label(ax, 1.1, 2.15, "환불", fs=11)
    label(ax, 2.1, 2.15, "→", fs=12, color=INK)
    cells(ax, 2.5, 1.85, ["1", "⋯", "100", "101", "⋯", "300"], w=0.85, h=0.6, gap=0.08,
          dim=(0, 1, 2), hot=(3, 4, 5), fs=10)
    label(ax, 8.2, 2.15, "200건", fs=12, color=RED, bold=True, ha="left")
    label(ax, 6.0, 1.0, "'환불'이 든 문서 수 300", fs=11, color=INK)


# ── 2절: 지우기도 빈 문서를 남겨요 ─────────────────────────────────
def tomb(ax):
    label(ax, 11.6, 6.2, "지운 문서 수 200", fs=11, ha="right", bold=True)
    rows = [("_0", "글 1~100", True), ("_1", "글 101~200", False), ("_2", "글 201~300", False)]
    for x, (n, t, dead) in zip(SEGX, rows):
        seg(ax, x, 3.9, SEGW, f"세그먼트 {n}", [t], dead=(0,) if dead else ())
    label(ax, SEGX[0] + SEGW / 2, 3.55, "지운 글 100", fs=10, color=INK)
    seg(ax, SEGX[3], 3.9, SEGW, "세그먼트 _3", ["빈 문서 100"], dead=(0,), hot=True)
    label(ax, SEGX[3] + SEGW / 2, 3.55, "1번 지움 ⋯ 100번 지움", fs=10, color=RED)
    label(ax, 6.0, 2.2, "지운 글 100 + 빈 문서 100 = 200", fs=12, color=RED, bold=True)


# ── 3절: 고치기는 지우고 새로 넣기 ─────────────────────────────────
def update(ax):
    label(ax, 0.3, 6.15, "101번 글:  환불 문의 → 환불 문의 수정", fs=11, ha="left", color=INK)
    box(ax, 0.3, 3.3, 5.4, 2.0, fc=NOTE)
    label(ax, 0.45, 5.0, "세그먼트 _1", fs=10.5, ha="left", bold=True)
    cell(ax, 0.5, 3.6, 2.7, 0.8, "101 환불 문의", dim=True, fs=10.5)
    strike(ax, 0.5, 3.6, 2.7, 0.8)
    cell(ax, 3.35, 3.6, 2.15, 0.8, "102 ⋯ 200", fs=10.5)
    label(ax, 1.85, 2.85, "삭제 표시", fs=11, color=INK)
    box(ax, 6.4, 3.3, 5.2, 2.0, fc=PINK, ec=RED)
    label(ax, 6.55, 5.0, "새 세그먼트", fs=10.5, ha="left", bold=True, color=RED)
    cell(ax, 6.7, 3.6, 4.6, 0.8, "101 환불 문의 수정", hot=True, fs=10.5)
    label(ax, 9.0, 2.85, "고친 글 전체", fs=11, color=RED)
    label(ax, 6.0, 1.4, "고치기 = 삭제 표시 + 새로 넣기", fs=12.5, color=RED, bold=True)


# ── 4절: 병합 ──────────────────────────────────────────────────────
def merge(ax):
    shard4(ax)
    label(ax, 11.6, 6.2, "세그먼트 4개 → 1개", fs=11, ha="right", bold=True)
    for x in (SEGX[1], SEGX[2]):
        arrow(ax, (x + SEGW / 2, 3.85), (x + SEGW / 2 + (0.6 if x < 5 else -0.6), 2.65), color=RED, ms=14)
    for x in (SEGX[0], SEGX[3]):
        label(ax, x + SEGW / 2, 3.35, "✗ 안 옮김", fs=10.5, color=RED, bold=True)
    seg(ax, 2.2, 1.0, 7.6, "새 세그먼트", ["글 101~200", "글 201~300"], hot=True, h=1.6)


BIG_DEAD = {2, 7, 11, 13, 18}


def cap(ax):
    box(ax, 0.3, 1.9, 5.6, 3.2, fc=NOTE)
    label(ax, 0.45, 4.8, "큰 세그먼트", fs=10.5, ha="left", bold=True)
    for i in range(20):
        cx, cy = 0.55 + (i % 5) * 1.05, 3.9 - (i // 5) * 0.6
        if i in BIG_DEAD:
            cell(ax, cx, cy, 0.9, 0.45, "", dim=True)
            strike(ax, cx, cy, 0.9, 0.45)
            ax.add_patch(Rectangle((cx, cy), 0.9, 0.45, fill=False, ec=RED, lw=2.0))
        else:
            cell(ax, cx, cy, 0.9, 0.45, "", fc="white")
    label(ax, 3.1, 1.5, "상한 5 GB 가까이", fs=10.5, color=INK)
    label(ax, 3.1, 0.9, "지운 문서가 꽤 쌓일 때까지 그대로", fs=11, color=RED, bold=True)
    label(ax, 9.0, 6.15, "작은 세그먼트들", fs=10.5, color=INK)
    for k in range(3):
        box(ax, 7.0 + k * 1.45, 4.85, 1.1, 0.8, fc=NOTE)
        arrow(ax, (7.55 + k * 1.45, 4.75), (9.0, 3.9), color=GREY, ms=12, lw=1.5)
    box(ax, 7.6, 2.9, 2.8, 0.9, fc=NOTE)
    label(ax, 9.0, 3.35, "합친 세그먼트", fs=10.5)
    label(ax, 9.0, 2.4, "비슷한 크기끼리", fs=10.5, color=INK)


# ── 5절: 복제본에 보낼 기록은 합쳐도 남겨요 ────────────────────────
PHASES = ["지운 직후", "바로 강제 병합", "조금 뒤 다시 병합"]


def retain(ax, step):
    """step 1: 바로 합침(지운 문서 그대로) / step 2: 조금 뒤 다시 합침(지운 문서 0)."""
    for k, t in enumerate(PHASES):
        x = 0.3 + k * 3.9
        on = k == step
        label(ax, x + 1.6, 6.1, t, fs=11, color=RED if on else INK, bold=on)
        if k < len(PHASES) - 1:
            arrow(ax, (x + 3.25, 6.1), (x + 3.85, 6.1), color=GREY, ms=10, lw=1.2)
    if step == 1:
        seg(ax, 0.3, 3.3, 11.3, "세그먼트 (하나로 합침)", ["글 1~100", "글 101~200", "글 201~300", "빈 문서 100"],
            dead=(0, 3), hot=True)
        label(ax, 6.0, 2.2, "세그먼트 1개 · 지운 문서 200", fs=12, color=RED, bold=True)
        return
    seg(ax, 0.3, 3.3, 11.3, "세그먼트 (다시 합침)", ["글 101~200", "글 201~300"], hot=True)
    label(ax, 6.0, 2.2, "세그먼트 1개 · 지운 문서 0", fs=12, color=RED, bold=True)


# ── 6절: 강제 병합은 언제 ──────────────────────────────────────────
def decide():
    fig, ax = canvas(10, 3.6, 15, 5.4)
    box(ax, 0.3, 3.6, 6.0, 1.3, fc=NOTE)
    label(ax, 3.3, 4.25, "앞으로 더 쓰는 인덱스", fs=11, bold=True)
    arrow(ax, (6.4, 4.25), (8.4, 4.25), color=RED)
    label(ax, 7.4, 4.55, "예", fs=10, color=RED)
    box(ax, 8.5, 3.6, 6.2, 1.3, fc=PINK, ec=RED)
    label(ax, 11.6, 4.25, "강제 병합 ✗  ES에 맡기기", fs=11, color=RED, bold=True)
    arrow(ax, (3.3, 3.5), (3.3, 2.6))
    label(ax, 3.6, 3.05, "아니요", fs=10, color=INK, ha="left")
    box(ax, 0.3, 1.3, 6.0, 1.2, fc=PAPER)
    label(ax, 3.3, 1.9, "세그먼트 하나로 강제 병합 ○", fs=11)
    box(ax, 8.5, 1.3, 6.2, 1.2, fc=LIGHT, ec=GREY)
    label(ax, 11.6, 1.9, "기간 지난 데이터\n→ 기간별 인덱스째 지우기", fs=10.5, color=INK)
    save(fig, OUT, "es05-decide.svg")


if __name__ == "__main__":
    one(opening, "es05-open.svg")
    one(lambda ax: mark(ax, 1), "es05-mark-1.svg")
    one(lambda ax: mark(ax, 2), "es05-mark-2.svg")
    one(tomb, "es05-tomb.svg")
    one(update, "es05-update.svg")
    one(merge, "es05-merge.svg")
    one(cap, "es05-cap.svg")
    one(lambda ax: retain(ax, 1), "es05-retain-1.svg")
    one(lambda ax: retain(ax, 2), "es05-retain-2.svg")
    decide()
