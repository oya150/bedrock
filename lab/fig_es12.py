"""Elasticsearch 12편 그림 만들기. 실행: python lab/fig_es12.py  → docs/elasticsearch/img/12/*.svg

본문 절은 장면 띠로 그린다: 같은 무대를 여러 장 그리고 장마다 바뀐 곳만 빨강으로 칠한다.
예시는 처음부터 끝까지 판매 기록 57건(샤드 3개, 샤드마다 x·z·w 10건 + y 9건)과 판매 번호 목록을 잇는다.
예시 세트: .claude/writing/work/cal/units-es12.md
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "es"))
from figkit import (BLUE, GREEN, GREY, INK, LIGHT, NOTE, PAPER, PINK, RED, YEL, arrow, box, bubble,  # noqa: E402
                    canvas, cell, cells, cylinder, label, moral, outdir, save, stage)
from matplotlib.patches import Polygon, Rectangle  # noqa: E402

OUT = outdir("12")
SC = [BLUE, GREEN, YEL]


def empty(ax, x, y, w, h):
    ax.add_patch(Rectangle((x, y), w, h, fc="white", ec=GREY, lw=1.0, ls="--"))


# ── 여는 장면과 돌아오는 장면: 요청 창 + ES ─────────────────────────
CYL = (7.8, 3.3, 3.8, 1.7)
SAY = (6.95, 0.45, 4.75, 1.45)
TAIL = (9.7, 3.05)
ASK1, ASK2 = "판매 1위 브랜드", "판매 기록 목록 1,001쪽째"


def window(ax, rows):
    """요청 창. rows=[(요청 글 또는 None, 답 글 또는 None, 답 모양 'hot'|'dim'|'')] 두 줄."""
    box(ax, 0.3, 1.3, 6.3, 4.9, fc="white", round_=False)
    ax.add_patch(Rectangle((0.3, 5.75), 6.3, 0.45, fc=LIGHT, ec=INK, lw=1.2))
    label(ax, 0.5, 5.97, "ES에 보내는 요청", fs=11, ha="left", color=INK)
    for k, (ask, ans, mode) in enumerate(rows):
        y = 4.75 - k * 1.75
        if ask is None:
            empty(ax, 0.55, y, 4.4, 0.55)
            empty(ax, 0.55, y - 0.8, 5.8, 0.6)
            continue
        ax.add_patch(Rectangle((0.55, y), 4.4, 0.55, fc="white", ec=INK, lw=1.2))
        label(ax, 0.7, y + 0.27, ask, fs=11, ha="left")
        ax.add_patch(Rectangle((5.05, y), 1.3, 0.55, fc=LIGHT, ec=INK, lw=1.2))
        label(ax, 5.7, y + 0.27, "보내기", fs=10.5)
        if ans is None:
            empty(ax, 0.55, y - 0.8, 5.8, 0.6)
            continue
        hot, dim = mode == "hot", mode == "dim"
        ax.add_patch(Rectangle((0.55, y - 0.8), 5.8, 0.6, fc=PINK if hot else ("white" if dim else NOTE),
                               ec=RED if hot else (GREY if dim else INK), lw=1.8 if hot else 1.1))
        label(ax, 0.7, y - 0.5, ans, fs=10.5, ha="left", color=RED if hot else (GREY if dim else "#222"), bold=hot)


def es_shards(ax):
    x, y, w, h = CYL
    cylinder(ax, *CYL, "ES (판매 기록)")
    for k in range(3):
        cell(ax, x + 0.2 + k * 1.15, y + 0.75, 1.05, 0.6, f"샤드 {k}", fs=9.5, fc=SC[k])


ANS_W = "1위 w 10건"
ANS_W2 = "✗ 1위 w 10건 (직접 세면 y 27건)"
ANS_BIG = "✗ Result window is too large"


def open_(ax, step):
    if step == 1:
        window(ax, [(ASK1, None, ""), (None, None, "")])
        bubble(ax, *SAY, "판매 기록 57건을\n샤드 3개에 나눠 담았어요", TAIL, fs=11)
    elif step == 2:
        window(ax, [(ASK1, ANS_W, "hot"), (None, None, "")])
        bubble(ax, *SAY, "w가 10건으로 1위예요", TAIL, hot=True, fs=11)
    elif step == 3:
        window(ax, [(ASK1, ANS_W2, "hot"), (None, None, "")])
        bubble(ax, *SAY, "w가 10건으로 1위예요", TAIL, fs=11)
    else:
        window(ax, [(ASK1, ANS_W2, ""), (ASK2, ANS_BIG, "hot")])
        bubble(ax, *SAY, "1,001쪽째는 못 열어요", TAIL, hot=True, fs=11)
        moral(ax, 3.45, 0.75, "1위가 틀렸고 1,001쪽은 안 열려요")
    es_shards(ax)


def back(ax, step):
    if step == 1:
        window(ax, [(ASK1, ANS_W2, "dim"), (ASK2, ANS_BIG, "dim")])
        bubble(ax, *SAY, "처음엔 w가 1위라 했고\n1,001쪽은 거절했어요", TAIL, fs=11)
    elif step == 2:
        window(ax, [(ASK1, "✓ 1위 y 27건 (shard_size 10)", "hot"), (ASK2, ANS_BIG, "dim")])
        bubble(ax, *SAY, "샤드마다 10개까지 받아 합쳤어요\n오차 상한은 0이에요", TAIL, hot=True, fs=10.5)
    else:
        window(ax, [(ASK1, "✓ 1위 y 27건 (shard_size 10)", ""), (ASK2, "✓ search_after로 이어서 넘겨요", "hot")])
        bubble(ax, *SAY, "앞 쪽 마지막 값 다음부터\n샤드마다 10개만 받아요", TAIL, hot=True, fs=10.5)
        moral(ax, 3.45, 0.75, "샤드마다 몇 개를 받느냐가 답을 정해요")
    es_shards(ax)


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


def qtf(ax, step):
    coord(ax)
    for k in range(3):
        shard_box(ax, k)
    chip(ax, ASK_P1, hot=step == 1)
    if step == 1:
        downs(ax, "hot")
        for k in range(3):
            shard_cells(ax, k, TOP3[k])
        say(ax, ["샤드 셋에 같은 요청을", "나눠 보내요"], hot=True, fs=11)
    elif step == 2:
        downs(ax, "dim")
        ups(ax, "hot")
        for k in range(3):
            shard_cells(ax, k, TOP3[k], hot=(0, 1, 2))
            shard_note(ax, k, "위 3개의 번호만", hot=True)
        say(ax, ["샤드마다 위 3개의", "번호만 받았어요"], [(t, "") for t in GOT], hot=True)
    elif step == 3:
        downs(ax, "dim")
        ups(ax, "dim")
        for k in range(3):
            shard_cells(ax, k, TOP3[k])
        say(ax, ["9개를 합쳐", "위 3개를 골라요"], [(str(i), "hot" if i <= 3 else "dim") for i in range(1, 10)], hot=True)
    else:
        downs(ax, "dim")
        ups(ax, "hot", "③")
        for k in range(3):
            shard_cells(ax, k, TOP3[k], hot=(0,))  # 샤드 0의 2, 샤드 1의 1, 샤드 2의 3: 모두 맨 앞 칸
            shard_note(ax, k, "원문 1개", hot=True)
        say(ax, ["고른 3개의 원문만", "그 샤드에서 받아 와요"], [(str(i), "hot" if i <= 3 else "dim") for i in range(1, 10)], hot=True)
        moral(ax, 6.0, 0.35, "원문은 최종 3개만 오가요")


def turn(ax, step):
    coord(ax)
    for k in range(3):
        shard_box(ax, k)
        shard_cells(ax, k, TOP3[k])
    chip(ax, ASK_P1)
    downs(ax, "dim")
    ups(ax, "dim")
    if step == 1:
        say(ax, ["샤드 셋이 나눠 찾고", "원문은 3개만 받았어요"], [(str(i), "" if i <= 3 else "dim") for i in range(1, 10)])
    else:
        say(ax, ["그런데 이렇게 합치면", "① 깊은 쪽은 샤드마다", "     많이 보내야 해요", "② 집계는 1위를",
                 "     놓칠 수 있어요"], hot=True, fs=10.5, left=True)


# ── 첫째: 깊은 쪽 ──────────────────────────────────────────────────
DEEP = ["1위", "2위", "⋯", "10,000위"]
DW = [0.68, 0.68, 0.4, 1.45]


def deep(ax, step):
    coord(ax)
    for k in range(3):
        shard_box(ax, k)
    if step < 4:
        chip(ax, "1,000쪽째 (from 9990, size 10)", hot=step == 1)
    if step == 1:
        downs(ax, "hot")
        for k in range(3):
            shard_cells(ax, k, DEEP[:3], w=DW[:3])
        say(ax, ["9,991번째부터", "10개가 필요해요"], hot=True, fs=11)
    elif step == 2:
        downs(ax, "dim")
        ups(ax, "hot")
        for k in range(3):
            shard_cells(ax, k, DEEP, w=DW, hot=(0, 1, 2, 3), fs=9.5)
            shard_note(ax, k, "위 10,000개", hot=True)
        say(ax, ["어느 샤드 것이 들어갈지 몰라", "샤드마다 10,000개를 받아요"], hot=True, fs=10)
    elif step == 3:
        downs(ax, "dim")
        ups(ax, "dim")
        for k in range(3):
            shard_cells(ax, k, DEEP, w=DW, fs=9.5)
            shard_note(ax, k, "위 10,000개")
        say(ax, ["30,000개를 합쳐", "10개만 써요"],
            [("버림", "dim", 0.85), ("9,991~10,000위", "hot", 2.0), ("버림", "dim", 0.85)],
            hot=True, fs=11)
    else:
        chip(ax, "1,001쪽째 (from 10000, size 10)", hot=True)
        for k in range(3):
            shard_cells(ax, k, DEEP[:3], w=DW[:3])
        say(ax, ["from + size가 10,010", "1만을 넘어 거절해요"], hot=True, fs=11)
        moral(ax, 6.0, 0.35, "쪽이 깊을수록 샤드마다 보내는 수가 늘어서 1만에서 막아요")


AFTER = [["21", "24", "27", "30", "33"], ["22", "23", "28", "31", "34"], ["25", "26", "29", "32", "35"]]


def after(ax, step):
    coord(ax)
    for k in range(3):
        shard_box(ax, k)
    chip(ax, "판매 번호 20 다음 5개", hot=step == 1)
    if step == 1:
        downs(ax, "hot")
        for k in range(3):
            shard_cells(ax, k, AFTER[k], w=0.55)
        say(ax, ["샤드마다 20 다음", "5개만 달라고 해요"], hot=True, fs=11)
    else:
        downs(ax, "dim")
        ups(ax, "hot")
        for k in range(3):
            shard_cells(ax, k, AFTER[k], w=0.55, hot=(0, 1, 2, 3, 4))
            shard_note(ax, k, "5개만", hot=True)
        say(ax, ["15개를 합쳐", "앞 5개를 써요"],
            [(str(i), "hot") for i in range(21, 26)] + [("26", "dim"), ("⋯", "dim")], hot=True, fs=11)
        moral(ax, 6.0, 0.35, "몇 쪽째든 샤드마다 5개만 보내요")


# ── 둘째: 집계 ────────────────────────────────────────────────────
BR = [("x", 10), ("z", 10), ("w", 10)]


def brand_cells(ax, k, top_hot=False, y_dim=False, all_hot=False):
    b, c = BR[k]
    shard_cells(ax, k, [f"{b} {c}건", "y 9건"], w=1.35, hot=(0, 1) if all_hot else ((0,) if top_hot else ()),
                dim=(1,) if y_dim else (), fs=10)


def terms(ax, step):
    coord(ax)
    for k in range(3):
        shard_box(ax, k)
    chip(ax, "판매 1위 브랜드 (shard_size 1)", hot=step == 1)
    if step == 1:
        downs(ax, "hot")
        for k in range(3):
            brand_cells(ax, k)
        say(ax, ["샤드마다 브랜드별", "건수를 세어 달라고 해요"], hot=True, fs=11)
    elif step == 2:
        downs(ax, "dim")
        ups(ax, "hot")
        for k in range(3):
            brand_cells(ax, k, top_hot=True, y_dim=True)
            shard_note(ax, k, "1위 하나만", hot=True)
        say(ax, ["샤드마다 1위", "하나만 받았어요"], [("x 10", ""), ("z 10", ""), ("w 10", "")], hot=True, row_w=0.9, fs=11)
    elif step == 3:
        downs(ax, "dim")
        ups(ax, "dim")
        for k in range(3):
            brand_cells(ax, k, y_dim=True)
        say(ax, ["건수가 같으면 이름 순서로", "1위는 w 10건이에요"],
            [("w 10", "hot"), ("x 10", ""), ("z 10", ""), ("y ?", "dim")], hot=True, row_w=0.85, fs=11)
    else:
        downs(ax, "dim")
        ups(ax, "dim")
        for k in range(3):
            brand_cells(ax, k, y_dim=True)
            shard_note(ax, k, "숨긴 브랜드는 10건 이하", hot=True)
        say(ax, ["오차 상한", "10 + 10 + 10 = 30", "1위 10건보다 커요"], hot=True, fs=11)
        moral(ax, 6.0, 0.35, "오차 상한이 1위 건수보다 크면 1위를 믿을 수 없어요")


def fix(ax, step):
    coord(ax)
    for k in range(3):
        shard_box(ax, k)
    chip(ax, "판매 1위 브랜드 (shard_size 10)", hot=step == 1)
    downs(ax, "dim")
    if step == 1:
        ups(ax, "hot")
        for k in range(3):
            brand_cells(ax, k, all_hot=True)
            shard_note(ax, k, "두 브랜드 모두", hot=True)
        say(ax, ["샤드마다 위 10개까지", "받아요"], hot=True, fs=11)
    else:
        ups(ax, "dim")
        for k in range(3):
            brand_cells(ax, k)
            shard_note(ax, k, "두 브랜드 모두")
        say(ax, ["y 9 + 9 + 9 = 27건이 1위", "오차 상한 0"],
            [("y 27", "hot"), ("w 10", ""), ("x 10", ""), ("z 10", "")], hot=True, row_w=0.85, fs=11)
        moral(ax, 6.0, 0.35, "샤드마다 더 받으면 y 27건이 1위로 올라와요")


# ── 언제 쓸모 있을까요: 갈림길 ──────────────────────────────────────
def decide():
    fig, ax = canvas(10, 5.9, 15, 8.9)
    for row, (q, yes, no) in enumerate([
        ("목록을 수백 쪽까지 넘기나요?", "search_after로 이어 받아요\n(정렬 끝에 상품 ID 같은 타이브레이커)",
         "from과 size로 쪽을 넘겨도 돼요"),
        ("집계 순위가 정확해야 하나요?", "오차 상한을 보고\nshard_size를 늘려요",
         "기본값(size × 1.5 + 10)으로 둬요"),
    ]):
        y0 = 5.0 - row * 4.6
        box(ax, 0.3, y0 + 2.3, 6.0, 1.3, fc=NOTE)
        label(ax, 3.3, y0 + 2.95, q, fs=10.5, bold=True)
        arrow(ax, (6.4, y0 + 2.95), (8.4, y0 + 2.95), color=RED)
        label(ax, 7.4, y0 + 3.25, "예", fs=10, color=RED)
        box(ax, 8.5, y0 + 2.2, 6.2, 1.5, fc=PINK, ec=RED)
        label(ax, 11.6, y0 + 2.95, yes, fs=10.5, color=RED, bold=True)
        arrow(ax, (3.3, y0 + 2.2), (3.3, y0 + 1.4))
        label(ax, 3.6, y0 + 1.8, "아니요", fs=10, color=INK, ha="left")
        box(ax, 0.3, y0 + 0.2, 6.0, 1.1, fc=PAPER)
        label(ax, 3.3, y0 + 0.75, no, fs=10)
    save(fig, OUT, "es12-decide.svg")


# ── 이 편에서 새로 나온 말 ─────────────────────────────────────────
def cards():
    fig, ax = canvas(6.4, 10.4, 9.8, 16.25)
    W, H = 4.6, 3.8

    def card(i, name, line):
        col, row = i % 2, i // 2
        x, y = 0.2 + col * 4.9, 12.25 - row * 4.05
        box(ax, x, y, W, H, fc="white")
        label(ax, x + 0.25, y + H - 0.4, name, fs=12.5, ha="left", bold=True)
        label(ax, x + W / 2, y + 0.6, line, fs=10, color=INK)
        return x, y

    x, y = card(0, "조율 노드", "요청을 샤드에 나눠 보내고\n답을 합치는 노드")
    cylinder(ax, x + 1.6, y + 2.3, 1.4, 0.4, "", fc=PINK, ec=RED)
    for k in range(3):
        cell(ax, x + 0.5 + k * 1.3, y + 1.25, 1.0, 0.45, f"샤드 {k}", fs=9, fc=SC[k])
        arrow(ax, (x + 2.3, y + 2.15), (x + 1.0 + k * 1.3, y + 1.75), color=RED, lw=1.3, ms=9)
    x, y = card(1, "query then fetch", "번호만 먼저 모으고\n고른 문서의 원문만 받기")
    cells(ax, x + 0.35, y + 2.0, ["1", "2", "3"], w=0.5, h=0.5, gap=0.05, fs=10)
    label(ax, x + 1.2, y + 1.65, "① 번호", fs=9.5, color=INK)
    arrow(ax, (x + 2.05, y + 2.25), (x + 2.65, y + 2.25), color=RED, ms=10)
    cell(ax, x + 2.75, y + 2.0, 1.5, 0.5, "원문 3개", hot=True, fs=9.5)
    label(ax, x + 3.5, y + 1.65, "② 원문", fs=9.5, color=RED)
    x, y = card(2, "max_result_window", "from + size의 상한\n(기본 10,000)")
    cell(ax, x + 0.45, y + 1.9, 3.7, 0.6, "from + size ≤ 10,000", hot=True, fs=10.5)
    x, y = card(3, "search_after", "앞 쪽 마지막 정렬 값\n다음부터 받기")
    cell(ax, x + 0.35, y + 1.9, 0.6, 0.55, "20", dim=True, fs=10)
    arrow(ax, (x + 1.05, y + 2.17), (x + 1.55, y + 2.17), color=RED, ms=10)
    cells(ax, x + 1.65, y + 1.9, ["21", "22", "23", "⋯"], w=0.6, h=0.55, gap=0.05, hot=(0, 1, 2), fs=10)
    x, y = card(4, "타이브레이커", "정렬 값이 같을 때\n순서를 정하는 값")
    for k in range(2):
        cell(ax, x + 0.5 + k * 1.9, y + 2.3, 1.7, 0.5, "정렬 값 20", dim=True, fs=9.5)
        cell(ax, x + 0.5 + k * 1.9, y + 1.75, 1.7, 0.5, "+ 상품 ID", hot=True, fs=9.5)
    x, y = card(5, "terms 집계", "필드 값별로 건수를 세는 집계")
    cells(ax, x + 0.35, y + 1.9, ["y 27", "w 10", "x 10", "z 10"], w=0.92, h=0.55, gap=0.06, hot=(0,), fs=10)
    x, y = card(6, "shard_size", "샤드마다 조율 노드에\n보내는 묶음 수")
    cells(ax, x + 0.5, y + 2.1, ["x 10건", "y 9건"], w=1.3, h=0.5, gap=0.08, hot=(0,), dim=(1,), fs=9.5)
    label(ax, x + 2.3, y + 1.75, "shard_size 1이면 1위만", fs=9.5, color=RED)
    x, y = card(7, "오차 상한", "보이지 않은 브랜드가\n가질 수 있는 최대 건수")
    cell(ax, x + 0.5, y + 1.9, 3.6, 0.6, "10 + 10 + 10 = 30", hot=True, fs=11)
    save(fig, OUT, "es12-cards.svg")


if __name__ == "__main__":
    S, L = (7.2, 3.8), (12, 6.6)
    stage(open_, 4, OUT, "es12-open", S, L)
    stage(qtf, 4, OUT, "es12-qtf", S, L)
    stage(turn, 2, OUT, "es12-turn", S, L)
    stage(deep, 4, OUT, "es12-deep", S, L)
    stage(after, 2, OUT, "es12-after", S, L)
    stage(terms, 4, OUT, "es12-terms", S, L)
    stage(fix, 2, OUT, "es12-fix", S, L)
    decide()
    stage(back, 3, OUT, "es12-back", S, L)
    cards()
