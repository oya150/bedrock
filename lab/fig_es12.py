"""Elasticsearch 12편 그림 만들기. 실행: python lab/fig_es12.py  → docs/elasticsearch/img/12/*.svg

같은 무대(조율 노드와 샤드 셋)를 여러 그림이 함께 쓰고 그림마다 볼 곳만 빨강으로 칠한다.
그림 안 글씨는 낱말과 숫자만 둔다. 예시는 처음부터 끝까지 판매 기록 57건(샤드 3개, 샤드마다 x·z·w 10건 + y 9건)과 판매 번호 목록을 잇는다.
예시 세트: .claude/writing/work/cal/units-es12.md
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "es"))
from figkit import (GREY, INK, LIGHT, PINK, RED, arrow, box,  # noqa: E402
                    canvas, cell, cylinder, label, outdir, save)
from matplotlib.patches import Polygon, Rectangle  # noqa: E402

OUT = outdir("12")
SC = ["#f1f3f5", "#dde1e5", "#c4c9cf"]  # 샤드 구별은 회색 농도로만


# ── 여는 그림: 요청 창 + ES ─────────────────────────────────────
CYL = (7.8, 3.3, 3.8, 1.7)


def window(ax, rows):
    """요청 창. rows=[(요청 글, 답 글)] 두 줄. 답은 모두 빨강."""
    box(ax, 0.3, 1.85, 6.3, 4.35, fc="white", round_=False)
    ax.add_patch(Rectangle((0.3, 5.75), 6.3, 0.45, fc=LIGHT, ec=INK, lw=1.2))
    label(ax, 0.5, 5.97, "ES에 보내는 요청", fs=11, ha="left", color=INK)
    for k, (ask, ans) in enumerate(rows):
        y = 4.75 - k * 1.75
        ax.add_patch(Rectangle((0.55, y), 4.4, 0.55, fc="white", ec=INK, lw=1.2))
        label(ax, 0.7, y + 0.27, ask, fs=11, ha="left")
        ax.add_patch(Rectangle((5.05, y), 1.3, 0.55, fc=LIGHT, ec=INK, lw=1.2))
        label(ax, 5.7, y + 0.27, "보내기", fs=10.5)
        ax.add_patch(Rectangle((0.55, y - 0.8), 5.8, 0.6, fc=PINK, ec=RED, lw=1.8))
        label(ax, 0.7, y - 0.5, ans, fs=10.5, ha="left", color=RED, bold=True)


def open_fig():
    fig, ax = canvas(*S, *L)
    window(ax, [("판매 1위 브랜드", "✗ 1위 w 10건 (직접 세면 y 27건)"),
                ("판매 기록 목록 1,001쪽째", "✗ Result window is too large")])
    x, y, w, h = CYL
    cylinder(ax, *CYL, "ES (판매 기록 57건)")
    for k in range(3):
        cell(ax, x + 0.2 + k * 1.15, y + 0.75, 1.05, 0.6, f"샤드 {k}", fs=9.5, fc=SC[k])
    save(fig, OUT, "es12-open.svg")


# ── 조율 노드와 샤드 셋 무대 (검색·깊은 쪽·search_after·집계가 함께 쓴다) ──
SX = [0.3 + k * 3.9 for k in range(3)]   # 샤드 상자 왼쪽 x
SY, SW, SH = 0.8, 3.5, 1.85               # 샤드 상자 아래 y, 폭, 높이
COORD = (4.75, 4.5, 2.5, 0.85)            # 조율 노드 원통
DOWN = [((5.25, 4.33), (SX[0] + 1.45, SY + SH + 0.1)), ((5.8, 4.3), (SX[1] + 1.45, SY + SH + 0.1)),
        ((6.35, 4.33), (SX[2] + 1.45, SY + SH + 0.1))]
UP = [((SX[0] + 2.1, SY + SH + 0.1), (5.55, 4.3)), ((SX[1] + 2.1, SY + SH + 0.1), (6.2, 4.28)),
      ((SX[2] + 2.1, SY + SH + 0.1), (6.75, 4.33))]
SAY_L = (0.25, 4.15, 4.0, 2.15)           # 조율 노드 말풍선 (왼쪽 위)
TAIL_L = (4.68, 4.95)
CHIP = (7.6, 4.65, 4.15, 0.7)             # 요청 칸 (오른쪽 위)


def shard_box(ax, k, hot=False):
    x = SX[k]
    ax.add_patch(Rectangle((x, SY), SW, SH, fc=PINK if hot else "white", ec=RED if hot else INK, lw=2.0 if hot else 1.2))
    label(ax, x + SW / 2, SY + SH - 0.28, f"샤드 {k}", fs=10.5, color=RED if hot else "#222", bold=hot)


def coord(ax):
    cylinder(ax, *COORD, "조율 노드")


def chip(ax, s, hot=False):
    x, y, w, h = CHIP
    ax.add_patch(Rectangle((x, y), w, h, fc=PINK if hot else "white", ec=RED if hot else INK, lw=1.8 if hot else 1.2))
    label(ax, x + w / 2, y + h / 2, s, fs=9.5, color=RED if hot else "#222", bold=hot)
    arrow(ax, (x - 0.05, y + h / 2), (COORD[0] + COORD[2] + 0.1, y + h / 2), color=RED if hot else GREY, ms=12)


def downs(ax, mode, mark="①"):
    """요청 화살표. mode='hot'|'dim'|''(없음)."""
    if not mode:
        return
    c = RED if mode == "hot" else GREY
    for a, b in DOWN:
        arrow(ax, a, b, color=c, lw=1.8, ms=12)
    if mode == "hot":
        label(ax, 3.85, 3.35, mark, fs=12, color=RED, bold=True)


def ups(ax, mode, mark="②"):
    if not mode:
        return
    c = RED if mode == "hot" else GREY
    for a, b in UP:
        arrow(ax, a, b, color=c, lw=1.8, ms=12)
    if mode == "hot":
        label(ax, 7.3, 3.45, mark, fs=12, color=RED, bold=True)


def say(ax, lines, row=None, hot=False, row_w=0.38, fs=10.5, left=False):
    """조율 노드 말풍선. lines=글 줄들, row=[(글, 'hot'|'dim'|'')] 칸 줄(말풍선 아래쪽)."""
    x, y, w, h = SAY_L
    fc, ec = (PINK, RED) if hot else ("white", INK)
    box(ax, x, y, w, h, fc=fc, ec=ec, lw=1.5)
    ty = y + h * 0.55  # 꼬리는 오른쪽 변에서 조율 노드 쪽으로
    ax.add_patch(Polygon([(x + w + 0.06, ty - 0.18), (x + w + 0.06, ty + 0.18), TAIL_L], closed=True, fc=fc, ec=ec, lw=1.5, zorder=3))
    ax.add_patch(Rectangle((x + w + 0.02, ty - 0.16), 0.08, 0.32, fc=fc, ec="none", zorder=4))
    top = y + h - 0.35
    for i, t in enumerate(lines):
        label(ax, x + 0.25 if left else x + w / 2, top - i * 0.4, t, fs=fs, color=RED if hot else "#222",
              ha="left" if left else "center", bold=left and i == 0)
    if row:
        row = [r if len(r) == 3 else (r[0], r[1], row_w) for r in row]  # (글, 모양, 칸 폭)
        tot = sum(r[2] for r in row) + (len(row) - 1) * 0.04
        xx = x + (w - tot) / 2
        for t, m, cw in row:
            cell(ax, xx, y + 0.2, cw, 0.48, t, hot=m == "hot", dim=m == "dim", fs=9)
            xx += cw + 0.04


def shard_cells(ax, k, items, w=0.6, hot=(), dim=(), fs=9.5):
    """샤드 안 칸 줄. w는 칸 폭 하나 또는 칸마다의 폭 목록."""
    ws = w if isinstance(w, (list, tuple)) else [w] * len(items)
    tot = sum(ws) + (len(items) - 1) * 0.06
    xx = SX[k] + (SW - tot) / 2
    for i, (t, cw) in enumerate(zip(items, ws)):
        cell(ax, xx, SY + 0.65, cw, 0.5, t, hot=i in hot, dim=i in dim, fs=fs)
        xx += cw + 0.06


def shard_note(ax, k, s, hot=False):
    label(ax, SX[k] + SW / 2, SY + 0.32, s, fs=9.5, color=RED if hot else INK, bold=hot)


# ── 검색은 두 번 오가요: 1쪽(번호순 3개로 줄여 그림) ────────────────
TOP3 = [["2", "5", "9", "⋯"], ["1", "6", "7", "⋯"], ["3", "4", "8", "⋯"]]
GOT = ["2", "5", "9", "1", "6", "7", "3", "4", "8"]
ASK_P1 = "목록 1쪽 (판매 번호순 3개)"


def one(draw, name):
    fig, ax = canvas(*S, *L)
    ax.add_patch(Rectangle((0, 0), *L, fill=False, ec="none"))
    draw(ax)
    save(fig, OUT, name)


def qtf(ax, step):
    coord(ax)
    for k in range(3):
        shard_box(ax, k)
    chip(ax, ASK_P1, hot=step == 1)
    if step == 1:
        downs(ax, "hot")
        for k in range(3):
            shard_cells(ax, k, TOP3[k])
        say(ax, ["같은 요청", "× 샤드 3개"], hot=True, fs=12)
    elif step == 2:
        downs(ax, "dim")
        ups(ax, "hot")
        for k in range(3):
            shard_cells(ax, k, TOP3[k], hot=(0, 1, 2))
            shard_note(ax, k, "위 3개 번호", hot=True)
        say(ax, ["받은 번호 9개"], [(t, "") for t in GOT], hot=True, fs=12)
    else:
        downs(ax, "dim")
        ups(ax, "hot", "③")
        for k in range(3):
            shard_cells(ax, k, TOP3[k], hot=(0,))  # 샤드 0의 2, 샤드 1의 1, 샤드 2의 3: 모두 맨 앞 칸
            shard_note(ax, k, "원문 1개", hot=True)
        say(ax, ["위 3개 → 원문"], [(str(i), "hot" if i <= 3 else "dim") for i in range(1, 10)], hot=True, fs=12)


# ── 깊은 쪽 ───────────────────────────────────────────────────────
DEEP = ["1위", "2위", "⋯", "10,000위"]
DW = [0.68, 0.68, 0.4, 1.45]


def deep(ax):
    coord(ax)
    for k in range(3):
        shard_box(ax, k)
    chip(ax, "1,000쪽째 (from 9990, size 10)")
    downs(ax, "dim")
    ups(ax, "hot")
    for k in range(3):
        shard_cells(ax, k, DEEP, w=DW, hot=(0, 1, 2, 3), fs=9.5)
        shard_note(ax, k, "위 10,000개", hot=True)
    say(ax, ["합친 수 30,000", "쓰는 수 10"],
        [("버림", "dim", 0.85), ("9,991~10,000위", "hot", 2.0), ("버림", "dim", 0.85)], hot=True, fs=12)


AFTER = [["21", "24", "27", "30", "33"], ["22", "23", "28", "31", "34"], ["25", "26", "29", "32", "35"]]


def after(ax):
    coord(ax)
    for k in range(3):
        shard_box(ax, k)
    chip(ax, "판매 번호 20 다음 5개")
    downs(ax, "dim")
    ups(ax, "hot")
    for k in range(3):
        shard_cells(ax, k, AFTER[k], w=0.55, hot=(0, 1, 2, 3, 4))
        shard_note(ax, k, "5개", hot=True)
    say(ax, ["합친 수 15", "쓰는 수 5"],
        [(str(i), "hot") for i in range(21, 26)] + [("26", "dim"), ("⋯", "dim")], hot=True, fs=12)


# ── 집계 ──────────────────────────────────────────────────────────
BR = [("x", 10), ("z", 10), ("w", 10)]


def brand_cells(ax, k, top_hot=False, y_dim=False, all_hot=False):
    b, c = BR[k]
    shard_cells(ax, k, [f"{b} {c}건", "y 9건"], w=1.35, hot=(0, 1) if all_hot else ((0,) if top_hot else ()),
                dim=(1,) if y_dim else (), fs=10)


def terms(ax, step):
    coord(ax)
    for k in range(3):
        shard_box(ax, k)
    chip(ax, "판매 1위 브랜드 (shard_size 1)")
    downs(ax, "dim")
    if step == 1:
        ups(ax, "hot")
        for k in range(3):
            brand_cells(ax, k, top_hot=True, y_dim=True)
            shard_note(ax, k, "1위만", hot=True)
        say(ax, ["1위 w 10건"], [("w 10", "hot"), ("x 10", ""), ("z 10", ""), ("y ?", "dim")],
            hot=True, row_w=0.85, fs=12)
    else:
        ups(ax, "dim")
        for k in range(3):
            brand_cells(ax, k, y_dim=True)
            shard_note(ax, k, "안 보낸 브랜드 ≤ 10건", hot=True)
        say(ax, ["오차 상한", "10 + 10 + 10 = 30", "1위 10건 < 30"], hot=True, fs=12)


def fix(ax):
    coord(ax)
    for k in range(3):
        shard_box(ax, k)
    chip(ax, "판매 1위 브랜드 (shard_size 10)", hot=True)
    downs(ax, "dim")
    ups(ax, "hot")
    for k in range(3):
        brand_cells(ax, k, all_hot=True)
        shard_note(ax, k, "2개 모두", hot=True)
    say(ax, ["y 9 + 9 + 9 = 27", "오차 상한 0"],
        [("y 27", "hot"), ("w 10", ""), ("x 10", ""), ("z 10", "")], hot=True, row_w=0.85, fs=12)


S, L = (7.2, 3.8), (12, 6.6)

if __name__ == "__main__":
    open_fig()
    for k in (1, 2, 3):
        one(lambda ax, k=k: qtf(ax, k), f"es12-qtf-{k}.svg")
    one(deep, "es12-deep.svg")
    one(after, "es12-after.svg")
    for k in (1, 2):
        one(lambda ax, k=k: terms(ax, k), f"es12-terms-{k}.svg")
    one(fix, "es12-fix.svg")
