"""Elasticsearch 7편 그림 만들기. 실행: python lab/fig_es07.py  → docs/elasticsearch/img/07/*.svg

본문 절은 장면 띠로 그린다: 같은 무대를 여러 장 그리고 장마다 바뀐 곳만 빨강으로 칠한다.
예시는 쇼핑몰 문의 게시판의 "환불 신청" 검색을 편 끝까지 잇는다(.claude/writing/work/cal/units-es07.md).
환불 = 글 1천 개(5, 70, 77, ⋯), 신청 = 글 100만 개, 건너뛰기 표 = 12 31 47 66 80 99.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "es"))
from figkit import (GREY, INK, LIGHT, NOTE, PINK, RED, arrow, board, box, bubble,  # noqa: E402
                    canvas, cell, cells, cylinder, label, moral, outdir, save, stage)
from matplotlib.patches import Circle, Rectangle  # noqa: E402

OUT = outdir("07")
CYL = (8.0, 3.0, 3.6, 1.7)
SAY = (7.2, 0.55, 4.5, 1.3)
TAIL = (9.8, 2.75)
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


# ── 여는 장면·돌아오는 장면: 게시판 + ES 원통 ──────────────────────
BAR_X, BAR_W = 8.85, 2.6


def lists(ax, lead=False, walk=None, hops=None):
    """원통 안의 두 포스팅 목록. walk=신청 막대를 걷는 화살표 색, hops=신청 막대 위 껑충 화살표 색."""
    cylinder(ax, *CYL, "ES")
    c1 = RED if lead else "#222"
    label(ax, 8.2, 4.3, "환불", fs=10.5, ha="left", color=c1, bold=lead)
    ax.add_patch(Rectangle((BAR_X, 4.18), 0.12, 0.24, fc=PINK if lead else LIGHT, ec=RED if lead else INK, lw=1.2))
    label(ax, BAR_X + 0.25, 4.3, "1천 개" + (" · 앞장" if lead else ""), fs=9.5, ha="left", color=c1)
    hotbar = walk == RED
    label(ax, 8.2, 3.45, "신청", fs=10.5, ha="left", color=RED if hotbar else "#222")
    ax.add_patch(Rectangle((BAR_X, 3.33), BAR_W, 0.24, fc=PINK if hotbar else LIGHT, ec=RED if hotbar else INK, lw=1.2))
    label(ax, BAR_X + BAR_W / 2, 3.45, "100만 개", fs=9, color=RED if hotbar else INK)
    if walk:
        arrow(ax, (BAR_X, 3.15), (BAR_X + BAR_W, 3.15), color=walk, ms=11, lw=1.6)
    if hops:
        xs = [BAR_X + 0.1 + k * 0.6 for k in range(5)]
        for a, b in zip(xs, xs[1:]):
            hop(ax, a, b, 3.65, color=hops, rad=-0.7, ms=9, lw=1.4)


def scene(ax, posts, foot, foot_hot=False, hot=()):
    board(ax, posts, query="환불 신청", hot=hot, footer=None)
    label(ax, 3.8, 0.88, foot, fs=11.5, color=RED if foot_hot else INK, bold=foot_hot)


RESULT = [(5, "환불 신청했어요"), None]


def opening(ax, step):
    if step == 1:
        scene(ax, [], "⋮   글이 1천만 개")
        lists(ax)
        bubble(ax, *SAY, "환불과 신청이 둘 다 든\n글을 찾을게요", TAIL)
    elif step == 2:
        scene(ax, [], "⋮   글이 1천만 개")
        lists(ax, walk=RED)
        bubble(ax, *SAY, "두 손가락으로 겹치면\n신청 100만 칸을 다 걸어요", TAIL, hot=True)
    else:
        scene(ax, RESULT, "둘 다 든 글은 많아야 1천 개", foot_hot=True, hot=(5,))
        lists(ax, walk=GREY)
        bubble(ax, *SAY, "두 손가락으로 겹치면\n신청 100만 칸을 다 걸어요", TAIL)
        moral(ax, 6.0, 0.2, "결과는 1천 개도 안 되는데 100만 칸을 걸어야 할까요?")


def back(ax, step):
    if step == 1:
        scene(ax, [], "⋮   글이 1천만 개")
        lists(ax, walk=GREY)
        bubble(ax, *SAY, "처음엔 신청 100만 칸을\n다 걸어야 할 것 같았어요", TAIL)
    elif step == 2:
        scene(ax, [], "⋮   글이 1천만 개")
        lists(ax, lead=True, hops=RED)
        bubble(ax, *SAY, "환불이 앞장서고 신청은\n표를 보고 껑충 뛰어요", TAIL, hot=True)
    else:
        scene(ax, RESULT, "둘 다 든 글이 하나씩 나와요", foot_hot=True, hot=(5,))
        lists(ax, hops=GREY)
        bubble(ax, *SAY, "신청 묶음은 7,813개 중\n937개만 풀었어요", TAIL)
        moral(ax, 6.0, 0.2, "긴 목록은 짧은 목록을 따라 건너뛰기만 해요")


# ── 두 손가락은 긴 목록을 다 걸어요 ────────────────────────────────
REF = ["5", "70", "77", "⋯"]
APP = ["0", "1", "2", "4", "5", "6", "⋯", "69", "72", "⋯"]
X0 = 1.6


def walk(ax, step):
    label(ax, 0.3, 6.2, "1편의 두 손가락: 번호가 작은 쪽 손가락을 한 칸 옮겨요", fs=11, ha="left", color=INK)
    label(ax, 0.3, 4.7, "환불", fs=12, ha="left", bold=True)
    label(ax, 0.3, 2.7, "신청", fs=12, ha="left", bold=True)
    hot_r = {1: (0,), 2: (0,), 3: (1,)}[step]
    hot_a = {1: (0,), 2: (1, 2, 3, 4), 3: (5, 6, 7, 8)}[step]
    dim_a = {1: (), 2: (0,), 3: (0, 1, 2, 3, 4)}[step]
    dim_r = (0,) if step == 3 else ()
    cells(ax, X0, 4.3, REF, w=W, h=0.8, gap=G, hot=hot_r, dim=dim_r, fs=12)
    cells(ax, X0, 2.3, APP, w=W, h=0.8, gap=G, hot=hot_a, dim=dim_a, fs=12)
    fi, fj = {1: (0, 0), 2: (0, 4), 3: (1, 8)}[step]
    finger(ax, cx(X0, fi), 5.35, color=INK if step == 2 else RED)
    finger(ax, cx(X0, fj), 1.95, up=True)
    if step == 1:
        label(ax, 6.0, 1.0, "두 목록 맨 앞에 손가락을 하나씩 올려요", fs=12, color=RED)
    elif step == 2:
        for a in range(0, 4):
            hop(ax, cx(X0, a) + 0.1, cx(X0, a + 1) - 0.1, 3.2)
        label(ax, 6.0, 1.0, "신청 손가락이 한 칸씩 5까지 와요. 5는 둘 다 있어요", fs=12, color=RED)
    else:
        for a in range(4, 8):
            hop(ax, cx(X0, a) + 0.1, cx(X0, a + 1) - 0.1, 3.2)
        label(ax, 6.0, 1.15, "70까지도 한 칸씩 걸어요. 72에 서야 70이 없는 걸 알아요", fs=11.5, color=RED)
        moral(ax, 6.0, 0.4, "신청 쪽은 결국 끝까지 다 걸어요")


# ── 묶음 풀기: 칸 하나 = 묶음 약 200개 ─────────────────────────────
def grid(ax, opened=0, hot=True):
    """신청 포스팅 목록의 묶음 7,813개를 칸 40개로. opened=앞에서부터 푼 칸 수."""
    for i in range(40):
        x, y = 0.8 + (i % 10) * 1.05, 4.3 - (i // 10) * 0.75
        if i < opened:
            fc, ec = (PINK, RED) if hot else (LIGHT, GREY)
            ax.add_patch(Rectangle((x, y), 0.9, 0.55, fc=fc, ec=ec, lw=1.6 if hot else 1.0))
            label(ax, x + 0.45, y + 0.27, "풂", fs=9, color=RED if hot else GREY)
        else:
            ax.add_patch(Rectangle((x, y), 0.9, 0.55, fc=NOTE, ec=INK, lw=1.0))
            ax.plot([x + 0.12, x + 0.78], [y + 0.27, y + 0.27], color=GREY, lw=2.5)
    label(ax, 0.3, 6.15, "신청 포스팅 목록: 128개씩 압축된 묶음 7,813개", fs=11, ha="left", bold=True)
    label(ax, 11.7, 5.4, "칸 하나 = 묶음 약 200개", fs=10, ha="right", color=INK)


def unpack(ax, step):
    if step == 1:
        grid(ax)
        label(ax, 6.0, 1.45, "한 칸씩 걸으려면 묶음을 풀어 번호를 꺼내야 해요", fs=11.5, color=INK)
        return
    grid(ax, opened=40)
    label(ax, 6.0, 1.45, "두 손가락: 푼 묶음 7,811개", fs=12.5, color=RED, bold=True)
    moral(ax, 6.0, 0.6, "한 칸씩 걸으면 묶음을 거의 다 풀어요")


def saved(ax, step):
    if step == 1:
        grid(ax, opened=40, hot=False)
        label(ax, 6.0, 1.45, "두 손가락: 푼 묶음 7,811개", fs=12, color=INK)
        return
    grid(ax, opened=5)
    label(ax, 6.0, 1.45, "앞장 + 건너뛰기 표: 푼 묶음 937개 (표는 3,696칸 봄)", fs=12, color=RED, bold=True)
    moral(ax, 6.0, 0.6, "푼 묶음이 8분의 1로 줄었어요")


# ── 짧은 목록이 앞장서요 ───────────────────────────────────────────
APP2 = ["⋯", "66", "67", "68", "69", "72", "⋯"]


def lead(ax, step):
    label(ax, 0.3, 4.7, "환불", fs=12, ha="left", bold=True, color=RED if step == 1 else "#222")
    label(ax, 0.3, 4.25, "1천 개", fs=10, ha="left", color=RED if step == 1 else INK)
    label(ax, 0.3, 2.3, "신청", fs=12, ha="left", bold=True)
    label(ax, 0.3, 1.85, "100만 개", fs=10, ha="left", color=INK)
    hot_r = {2: (1,), 4: (2,)}.get(step, ())
    dim_r = ((0,) if step > 1 else ()) + ((1,) if step == 4 else ())
    cells(ax, X0, 4.1, REF, w=W, h=0.8, gap=G, hot=hot_r, dim=dim_r, fs=12)
    cells(ax, X0, 1.7, APP2, w=W, h=0.8, gap=G, hot=(5,) if step == 3 else (), fs=12)
    if step == 1:
        box(ax, 5.6, 4.15, 3.6, 0.7, fc="white", ec=RED, lw=1.6)
        label(ax, 7.4, 4.5, "짧은 쪽이 앞장서요", fs=11.5, color=RED, bold=True)
        label(ax, 6.0, 0.7, "목록마다 든 문서 수(doc_freq)를 알아요", fs=11, color=INK)
        return
    a70, a72, a77 = (cx(X0, 1), 4.0), (cx(X0, 5), 2.6), (cx(X0, 2), 4.0)
    arrow(ax, a70, a72, color=RED if step == 2 else GREY, ms=14)
    if step < 4:
        label(ax, 5.3, 3.75, "advance(70)", fs=11, ha="left", color=RED if step == 2 else INK)
    if step == 2:
        label(ax, 8.6, 3.1, "70 이상인\n첫 문서는?", fs=11.5, ha="left", color=RED)
    elif step == 3:
        label(ax, 8.6, 3.1, "72예요.\n70은 탈락", fs=11.5, ha="left", color=RED, bold=True)
    else:
        arrow(ax, (a72[0] - 0.15, a72[1] + 0.1), (a77[0] + 0.2, a77[1]), color=RED, ms=14, rad=0.25)
        label(ax, 8.6, 3.1, "환불도 advance(72)\n→ 77이 다음 후보", fs=11, ha="left", color=RED)
        moral(ax, 6.0, 0.6, "짧은 목록 번호만 후보가 되고 긴 목록은 묻는 말에만 답해요")


# ── 건너뛰기 표로 껑충 ─────────────────────────────────────────────
TBL = ["12", "31", "47", "66", "80", "99"]
RANGES = ["0…12", "13…31", "32…47", "48…66", "67…80", "81…99"]
TX, TW, TG = 2.4, 1.2, 0.08
OPEN5 = ["67", "68", "69", "72", "⋯", "80"]


def leap(ax, step):
    label(ax, 0.2, 5.85, "환불", fs=11.5, ha="left", bold=True)
    cells(ax, TX, 5.55, REF, w=0.75, h=0.6, gap=0.08, hot=(1,) if step == 1 else (), dim=(0,), fs=11)
    label(ax, 6.0, 5.85, "advance(70)", fs=11.5, ha="left", color=RED if step == 1 else INK, bold=step == 1)
    label(ax, 0.2, 4.4, "건너뛰기 표", fs=11, ha="left", bold=True)
    hot_t = {2: (1, 2, 3), 3: (4,)}.get(step, ())
    cells(ax, TX, 4.1, TBL, w=TW, h=0.6, gap=TG, hot=hot_t, dim=(5,), fs=11.5)
    label(ax, 0.2, 2.85, "신청 묶음", fs=11, ha="left", bold=True)
    for k, r in enumerate(RANGES):
        x = TX + k * (TW + TG)
        skip = step >= 2 and k in (1, 2, 3)
        hot = step == 3 and k == 4
        fc, ec = (PINK, RED) if hot else ((LIGHT, GREY) if skip or k == 5 else (NOTE, INK))
        ax.add_patch(Rectangle((x, 2.45), TW, 0.8, fc=fc, ec=ec, lw=1.8 if hot else 1.1))
        c = RED if hot else (GREY if skip or k == 5 else "#222")
        label(ax, x + TW / 2, 3.03, f"묶음 {k + 1}", fs=9.5, color=c, bold=hot)
        label(ax, x + TW / 2, 2.68, r, fs=9.5, color=c)
    if step < 4:
        finger(ax, TX + TW / 2, 2.2, up=True, color=INK)
    if step >= 2:
        for a in range(0, 3):
            hop(ax, cx(TX, a, TW, TG) + 0.15, cx(TX, a + 1, TW, TG) - 0.15, 4.8,
                color=RED if step == 2 else GREY, rad=-0.5, ms=11)
    if step == 1:
        label(ax, 6.0, 1.3, "지금 손가락은 묶음 1. 묶음을 풀기 전에 표부터 봐요", fs=11.5, color=INK)
    elif step == 2:
        label(ax, 6.0, 1.3, "31, 47, 66 < 70: 묶음 2~4는 넘어가요", fs=12, color=RED, bold=True)
    else:
        x5 = cx(TX, 4, TW, TG)
        arrow(ax, (x5, 4.0), (x5, 3.35), color=RED if step == 3 else GREY, ms=13)
        if step == 3:
            label(ax, 6.0, 1.3, "80 ≥ 70: 묶음 5만 풀어요", fs=12, color=RED, bold=True)
        else:
            arrow(ax, (x5, 2.35), (x5 - 0.3, 1.78), color=RED, ms=12)
            cells(ax, 5.3, 1.15, OPEN5, w=0.68, h=0.55, gap=0.06, hot=(3,), fs=10.5)
            finger(ax, cx(5.3, 3, 0.68, 0.06), 0.95, up=True)
            label(ax, 5.1, 1.42, "70 이상인 첫 번호는 72", fs=11, color=RED, ha="right")
            moral(ax, 6.0, 0.28, "묶음 2~4는 풀지도 않고 지나가요")


# ── ES에서 세어 보기 ───────────────────────────────────────────────
RARE_X = [2.9 + k * 1.05 for k in range(8)]


def profile(ax, step):
    label(ax, 0.3, 6.15, "문서 10만 개 모두에 common, 그중 50개에만 rare", fs=11, ha="left", color=INK)
    label(ax, 0.3, 4.5, "rare", fs=12, ha="left", bold=True)
    label(ax, 0.3, 4.05, "50개", fs=10, ha="left", color=INK)
    for x in RARE_X:
        cell(ax, x - 0.25, 4.15, 0.5, 0.5, "", fs=9)
    label(ax, 11.4, 4.4, "⋯", fs=14, color=INK)
    label(ax, 0.3, 2.3, "common", fs=12, ha="left", bold=True)
    label(ax, 0.3, 1.85, "10만 개", fs=10, ha="left", color=INK)
    for k in range(60):
        ax.add_patch(Rectangle((2.45 + k * 0.15, 1.9), 0.12, 0.55, fc=NOTE, ec=INK, lw=0.5))
    label(ax, 11.6, 2.17, "⋯", fs=14, color=INK)
    if step == 1:
        label(ax, 6.0, 0.9, "둘 다 든 문서를 must로 찾고 profile로 호출 수를 세요", fs=11.5, color=INK)
        return
    for x in RARE_X:
        arrow(ax, (x, 4.1), (x, 2.55), color=RED, ms=11, lw=1.5)
    label(ax, 6.0, 1.15, "common: advance 50번 (한 칸씩이면 10만 번)", fs=12, color=RED, bold=True)
    moral(ax, 6.0, 0.4, "10만 개 목록을 50번 뛰어 끝냈어요")


# ── 전환: 건너뛰기만으로 끝나지 않는 검색 ──────────────────────────
def turn(ax, step):
    label(ax, 0.3, 5.9, "환불 (앞장)", fs=11, ha="left", bold=True)
    cells(ax, 2.4, 5.6, REF, w=0.75, h=0.6, gap=0.08, fs=11)
    label(ax, 0.3, 4.75, "신청 묶음", fs=11, ha="left", bold=True)
    for k in range(6):
        skip = k in (1, 2, 3, 5)
        x = 2.4 + k * 0.83
        ax.add_patch(Rectangle((x, 4.45), 0.75, 0.6, fc=LIGHT if skip else NOTE, ec=GREY if skip else INK, lw=1.0))
        label(ax, x + 0.375, 4.75, f"{k + 1}" + (" 풂" if k == 4 else ""), fs=9.5, color=GREY if skip else "#222")
    label(ax, 4.85, 4.1, "묶음 2~4는 건너뛰고 5만 풂", fs=9.5, color=INK)
    cylinder(ax, 8.4, 3.9, 3.0, 1.4, "ES")
    if step == 1:
        bubble(ax, 3.4, 1.0, 7.8, 1.6, "짧은 목록이 앞장서고 긴 목록은 표를 보고\n건너뛰었어요. 푼 묶음 7,811개 → 937개", (9.9, 3.6))
        return
    bubble(ax, 0.5, 0.2, 11.1, 3.0, "", (9.9, 3.6), hot=True)
    label(ax, 6.0, 2.75, "그런데 건너뛰기만으로 끝나지 않는 검색이 있어요", fs=12, color=RED, bold=True)
    for k, t in enumerate(["① OR는 모든 목록을 끝까지 걸어요", "② 구문 검색은 후보마다 위치를 더 읽어요"]):
        label(ax, 1.2, 1.95 - k * 0.7, t, fs=11.5, ha="left", color=RED)


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
    pos = {1: [0, 0, 0], 2: [0, 0, 0], 3: [1, 0, 0]}.get(step)
    for (name, vals), y, k in zip(OR_LISTS, OR_ROWS, range(3)):
        label(ax, 0.3, y + 0.35, name, fs=11.5, ha="left", bold=True)
        hot = (pos[k],) if (step == 1 or (step == 3 and k == 0)) else ()
        dim = tuple(range(len(vals))) if step == 4 else ((0,) if step == 3 and k == 0 else ())
        cells(ax, 1.3, y, vals, w=0.8, h=0.7, gap=0.08, hot=hot, dim=dim, fs=12)
        if pos:
            finger(ax, cx(1.3, pos[k], 0.8, 0.08), y + 0.88, color=RED if hot else INK)
    label(ax, 6.7, 5.65, "힙", fs=11.5, bold=True)
    for a, b in ((0, 1), (0, 2)):
        ax.plot([NODES[a][0], NODES[b][0]], [NODES[a][1], NODES[b][1]], color=INK, lw=1.2, zorder=0)
    if step == 1:
        for xy, v in zip(NODES, [3, 5, 8]):
            node(ax, xy, v, hot=True)
        label(ax, 8.3, 4.1, "세 손가락의 번호를\n힙에 넣으면\n3이 맨 위", fs=10.5, ha="left", color=RED)
    elif step == 2:
        node(ax, NODES[0], 3, gone=True)
        node(ax, NODES[1], 5)
        node(ax, NODES[2], 8)
        arrow(ax, (6.3, 4.62), (1.85, 1.78), color=RED, ms=13)
        label(ax, 8.3, 4.1, "맨 위 3을\n꺼내 결과로", fs=10.5, ha="left", color=RED)
    elif step == 3:
        node(ax, NODES[0], 5)
        node(ax, NODES[1], 8)
        node(ax, NODES[2], 9, hot=True)
        label(ax, 8.3, 4.1, "환불 손가락을\n한 칸 옮겨\n9를 넣어요", fs=10.5, ha="left", color=RED)
    else:
        for xy in NODES:
            node(ax, xy, "", gone=True)
        label(ax, 8.3, 4.1, "9는 두 목록에\n있지만 한 번만", fs=10.5, ha="left", color=INK)
    label(ax, 0.3, 1.35, "결과", fs=11.5, ha="left", bold=True)
    n = {1: 0, 2: 1, 3: 1, 4: 7}[step]
    for k in range(7):
        x = 1.3 + k * 0.88
        if k < n:
            cell(ax, x, 1.0, 0.8, 0.7, RES[k], hot=(step in (2, 4)), fs=12)
        else:
            empty(ax, x, 1.0, 0.8, 0.7)
    if step == 4:
        moral(ax, 6.0, 0.35, "OR는 모든 목록을 끝까지 걸어요")


# ── 둘째: 구문 검색은 후보마다 위치를 ──────────────────────────────
DOC_A = ["주문", "환불", "요청"]
DOC_B = ["요청", "먼저", "하고", "환불", "대기"]


def phrase(ax, step):
    ax.add_patch(Rectangle((0.3, 5.75), 3.6, 0.6, fc="white", ec=INK, lw=1.2))
    label(ax, 2.1, 6.05, "\"환불 요청\"", fs=12)
    label(ax, 4.2, 6.05, "구문 검색 (match_phrase)", fs=11, ha="left", color=INK)
    c1 = RED if step == 1 else INK
    label(ax, 0.3, 5.15, "① AND로 두 낱말이 다 든 글만 후보로 남겨요 (건너뛰기 그대로)", fs=11, ha="left", color=c1,
          bold=step == 1)
    for words, y in ((DOC_A, 3.9), (DOC_B, 2.3)):
        box(ax, 0.4, y - 0.25, 6.6, 1.15, fc="white", ec=RED if step == 1 else INK, lw=1.6 if step == 1 else 1.2)
        for k, wd in enumerate(words):
            on = wd in ("환불", "요청")
            cell(ax, 0.6 + k * 1.25, y + 0.1, 1.15, 0.6, wd, hot=on and step == 2, fs=11)
            if step == 2:
                label(ax, 0.6 + k * 1.25 + 0.575, y - 0.08, str(k), fs=9.5, color=RED if on else GREY)
    if step == 2:
        label(ax, 0.3, 1.25, "② 남은 후보에서만 위치를 읽어요", fs=11, ha="left", color=RED, bold=True)
        label(ax, 7.3, 4.25, "1 다음 2: 붙어 있어요 ✓", fs=11, ha="left", color=RED)
        label(ax, 7.3, 2.65, "0과 3: 떨어져 있어요 ✗", fs=11, ha="left", color=RED)
        moral(ax, 6.0, 0.45, "비싼 위치 읽기는 남은 후보에만 해요")
    else:
        label(ax, 7.3, 3.4, "두 낱말이 다 든\n글만 후보로", fs=11, ha="left", color=RED)


# ── 건너뛰기는 언제 쓸모 있을까요 ─────────────────────────────────
def decide():
    fig, ax = canvas(10, 4.2, 15, 6.0)
    box(ax, 0.3, 4.4, 4.4, 1.2, fc=NOTE)
    label(ax, 2.5, 5.0, "모두 맞아야 하나요?\n(AND)", fs=11.5, bold=True)
    box(ax, 5.6, 4.4, 4.4, 1.2, fc=NOTE)
    label(ax, 7.8, 5.0, "드문 조건이\n하나라도 있나요?", fs=11.5, bold=True)
    box(ax, 10.9, 4.4, 3.8, 1.2, fc=PINK, ec=RED)
    label(ax, 12.8, 5.0, "드문 쪽이 앞장서요\n쓴 순서는 상관없어요", fs=10.5, color=RED, bold=True)
    arrow(ax, (4.8, 5.0), (5.5, 5.0)); label(ax, 5.15, 5.45, "예", fs=10, color=INK)
    arrow(ax, (10.1, 5.0), (10.8, 5.0), color=RED); label(ax, 10.45, 5.45, "예", fs=10, color=RED)
    arrow(ax, (2.5, 4.3), (2.5, 2.9)); label(ax, 2.85, 3.6, "아니요 (하나만 맞아도 돼요)", fs=10, color=INK, ha="left")
    arrow(ax, (7.8, 4.3), (7.8, 2.9)); label(ax, 8.15, 3.6, "아니요", fs=10, color=INK, ha="left")
    box(ax, 0.3, 0.6, 4.4, 2.2, fc=LIGHT, ec=GREY)
    label(ax, 2.5, 1.7, "OR는 모든 목록을 걸어요\n값이 많으면 filter 안\nterms로 한꺼번에 모아요", fs=10.5)
    box(ax, 5.6, 0.6, 4.4, 2.2, fc=LIGHT, ec=GREY)
    label(ax, 7.8, 1.7, "흔한 조건끼리면\n앞장선 목록부터 길어\n느려요", fs=10.5)
    save(fig, OUT, "es07-decide.svg")


# ── 정리: 낱말 카드 ────────────────────────────────────────────────
def cards():
    """본문에서 이름 붙인 말 여섯. 휴대폰 폭에 맞게 두 장씩 세 줄."""
    fig, ax = canvas(6.4, 7.8, 9.8, 12.2)
    CW, CH = 4.6, 3.8

    def card(i, name, line):
        col, row = i % 2, i // 2
        x, y = 0.2 + col * 4.9, 8.2 - row * 4.05
        box(ax, x, y, CW, CH, fc="white")
        label(ax, x + 0.25, y + CH - 0.4, name, fs=12.5, ha="left", bold=True)
        label(ax, x + CW / 2, y + 0.6, line, fs=10, color=INK)
        return x, y

    x, y = card(0, "advance", "이 번호 이상인\n첫 문서로 가기")
    cells(ax, x + 0.5, y + 1.6, ["67", "68", "69", "72"], w=0.8, h=0.55, gap=0.06, hot=(3,), fs=10)
    label(ax, x + CW / 2, y + 1.3, "advance(70)", fs=9.5, color=RED)
    hop(ax, x + 0.9, x + 3.45, y + 2.25, rad=-0.3, ms=10)
    x, y = card(1, "next (nextDoc)", "한 칸 앞으로 가기")
    cells(ax, x + 0.8, y + 1.6, ["0", "1", "2"], w=0.8, h=0.55, gap=0.06, hot=(1,), fs=10)
    hop(ax, x + 1.25, x + 2.0, y + 2.25, rad=-0.6, ms=10)
    x, y = card(2, "건너뛰기 표", "묶음마다 마지막 번호를\n적은 표 (skip data)")
    cells(ax, x + 0.5, y + 1.8, ["31", "47", "66", "80"], w=0.8, h=0.55, gap=0.06, hot=(3,), fs=10)
    x, y = card(3, "doc_freq", "낱말이 든 문서 수,\n적은 쪽이 앞장서요")
    label(ax, x + 0.4, y + 2.35, "환불", fs=10, ha="left", color=RED, bold=True)
    ax.add_patch(Rectangle((x + 1.2, y + 2.22), 0.15, 0.26, fc=PINK, ec=RED, lw=1.2))
    label(ax, x + 0.4, y + 1.75, "신청", fs=10, ha="left")
    ax.add_patch(Rectangle((x + 1.2, y + 1.62), 3.0, 0.26, fc=LIGHT, ec=INK, lw=1.0))
    x, y = card(4, "힙", "가장 작은 번호를\n늘 맨 위에 두는 나무")
    pts = [(x + 2.3, y + 2.55), (x + 1.7, y + 1.65), (x + 2.9, y + 1.65)]
    for b in (1, 2):
        ax.plot([pts[0][0], pts[b][0]], [pts[0][1], pts[b][1]], color=INK, lw=1.0, zorder=1.5)
    for xy, v, hot in zip(pts, [3, 5, 8], [True, False, False]):
        ax.add_patch(Circle(xy, 0.3, fc=PINK if hot else NOTE, ec=RED if hot else INK, lw=1.4, zorder=2))
        label(ax, xy[0], xy[1], v, fs=10.5, color=RED if hot else "#222", zorder=3)
    x, y = card(5, "구문 검색", "AND로 후보를 줄이고\n위치로 붙었는지 확인")
    for k, wd in enumerate(["환불", "요청"]):
        cell(ax, x + 1.2 + k * 1.15, y + 1.85, 1.05, 0.55, wd, hot=True, fs=10)
        label(ax, x + 1.725 + k * 1.15, y + 1.62, str(k + 1), fs=9, color=RED)
    save(fig, OUT, "es07-cards.svg")


if __name__ == "__main__":
    S, L = (7.2, 3.8), (12, 6.6)
    stage(opening, 3, OUT, "es07-open", S, L)
    stage(walk, 3, OUT, "es07-walk", S, L)
    stage(unpack, 2, OUT, "es07-unpack", S, L)
    stage(lead, 4, OUT, "es07-lead", S, L)
    stage(leap, 4, OUT, "es07-leap", S, L)
    stage(saved, 2, OUT, "es07-saved", S, L)
    stage(profile, 2, OUT, "es07-profile", S, L)
    stage(turn, 2, OUT, "es07-turn", S, L)
    stage(orheap, 4, OUT, "es07-or", S, L)
    stage(phrase, 2, OUT, "es07-phrase", S, L)
    decide()
    stage(back, 3, OUT, "es07-back", S, L)
    cards()
