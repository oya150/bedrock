"""Elasticsearch 3편 그림 만들기. 실행: python lab/fig_es03.py  → docs/elasticsearch/img/03/*.svg

본문 절은 장면 띠로 그린다: 같은 무대를 여러 장 그리고 장마다 바뀐 곳만 빨강으로 칠한다.
예시는 처음부터 끝까지 주문 기록(샤드 3개)과 order-1(해시값 41)을 잇는다.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "es"))
from figkit import (BLUE, GREEN, GREY, INK, LIGHT, NOTE, PAPER, PINK, RED, YEL, arrow, box, bubble,  # noqa: E402
                    canvas, cell, cells, cylinder, label, moral, outdir, save, stage)
from matplotlib.patches import Rectangle  # noqa: E402

OUT = outdir("03")
SC = [BLUE, GREEN, YEL, "#c6a0d8"]
SC6 = [BLUE, GREEN, YEL, "#c6a0d8", "#e8a87c", "#9fd3c7"]


def empty(ax, x, y, w, h):
    ax.add_patch(Rectangle((x, y), w, h, fc="white", ec=GREY, lw=1.0, ls="--"))


def shard(ax, x, y, w, h, name, fc="white", hot=False, dim=False, fs=10.5, top=True):
    """샤드 상자. 이름은 상자 안 위쪽(top=False면 가운데)에 쓴다."""
    ec = RED if hot else (GREY if dim else INK)
    ax.add_patch(Rectangle((x, y), w, h, fc=PINK if hot else fc, ec=ec, lw=2.0 if hot else 1.2))
    label(ax, x + w / 2, y + h - 0.25 if top else y + h / 2, name, fs=fs,
          color=RED if hot else (GREY if dim else "#222"), bold=hot)


# ── 여는 장면과 돌아오는 장면: 요청 창 + ES ─────────────────────────
CYL = (7.8, 3.3, 3.8, 1.7)
SAY = (6.95, 0.45, 4.75, 1.45)
TAIL = (9.7, 3.05)


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


def es_pieces(ax, word="조각", note=None):
    x, y, w, h = CYL
    cylinder(ax, *CYL, "ES (주문 기록)")
    for k in range(3):
        if note:
            ax.add_patch(Rectangle((x + 0.2 + k * 1.15, y + 0.15), 1.05, 1.3, fc=SC[k], ec=INK, lw=1.2))
            label(ax, x + 0.72 + k * 1.15, y + 1.2, f"{word} {k}", fs=9.5)
        else:
            cell(ax, x + 0.2 + k * 1.15, y + 0.75, 1.05, 0.6, f"{word} {k}", fs=9.5, fc=SC[k])
    if note:
        cell(ax, x + 0.25 + 2 * 1.15, y + 0.3, 0.95, 0.5, note, fs=8.5)


ASK4, ASK6 = "조각을 4개로 늘려 줘", "조각 6개로 쪼개 줘"
NO, OK = "✗ 거절: 조각 수는 바꿀 수 없어요", "✓ 조각 6개짜리를 만들었어요"


def open_(ax, step):
    if step == 1:
        window(ax, [(ASK4, None, ""), (None, None, "")])
        es_pieces(ax)
        bubble(ax, *SAY, "주문 기록을 조각 3개에\n나눠 담았어요", TAIL, fs=11)
    elif step == 2:
        window(ax, [(ASK4, NO, "hot"), (None, None, "")])
        es_pieces(ax)
        bubble(ax, *SAY, "조각 수는 못 바꿔요", TAIL, hot=True, fs=11)
    else:
        window(ax, [(ASK4, NO, ""), (ASK6, OK, "hot")])
        es_pieces(ax)
        bubble(ax, *SAY, "6개로 쪼개는 건\n해 줄게요", TAIL, hot=True, fs=11)
        moral(ax, 3.45, 0.75, "4개는 거절, 6개는 받아 줘요")


def back(ax, step):
    if step == 1:
        window(ax, [(ASK4, NO, "dim"), (ASK6, OK, "dim")])
        es_pieces(ax, "샤드", "order-1")
        bubble(ax, *SAY, "처음엔 4개는 거절하고\n6개는 받아 줬어요", TAIL, fs=11)
    elif step == 2:
        window(ax, [(ASK4, "✗ 4개였다면 order-1을 샤드 1에서 찾아요", "hot"), (ASK6, OK, "dim")])
        es_pieces(ax, "샤드", "order-1")
        bubble(ax, *SAY, "4개였다면 41 ÷ 4 나머지 1\norder-1은 샤드 2에 있는데요", TAIL, hot=True, fs=10.5)
    else:
        window(ax, [(ASK4, NO, "dim"), (ASK6, "✓ order-1은 샤드 2에서 샤드 5로", "hot")])
        es_pieces(ax, "샤드", "order-1")
        bubble(ax, *SAY, "41 ÷ 6 나머지 5\n샤드 2가 갈라진 샤드 5예요", TAIL, hot=True, fs=10.5)
        moral(ax, 3.45, 0.75, "샤드 수는 못 바꾸고 2배로 쪼개요")


# ── 인덱스는 샤드 여러 개로 ────────────────────────────────────────
DOCS = ["order-8 ⋯", "order-4 ⋯", "order-1 ⋯"]


def shards(ax, step):
    box(ax, 3.4, 5.4, 5.2, 0.85, fc=PAPER)
    label(ax, 6.0, 5.82, "주문 인덱스 (문서 수억 개)", fs=11.5, bold=True)
    for k in range(3):
        x = 0.3 + k * 3.9
        if step == 1 and k > 0:
            empty(ax, x, 0.95, 3.5, 3.4)
            label(ax, x + 1.75, 2.65, f"노드 {k + 1}", fs=10.5, color=GREY)
            continue
        box(ax, x, 0.95, 3.5, 3.4, fc="white", ec=GREY)
        label(ax, x + 1.75, 4.05, f"노드 {k + 1} (컴퓨터)", fs=10, color=INK)
        if step == 1:
            arrow(ax, (5.0, 5.35), (x + 1.75, 4.4), color=RED, ms=14)
            label(ax, x + 1.75, 2.45, "문서가 너무 많아\n디스크도 메모리도\n모자라요", fs=10.5, color=RED)
            continue
        arrow(ax, (6.0, 5.35), (x + 1.75, 4.4), color=RED if step == 2 else GREY, ms=13)
        shard(ax, x + 0.25, 1.15, 3.0, 2.55, f"샤드 {k}", fc=SC[k], hot=(step == 2))
        if step == 3:
            cell(ax, x + 0.45, 2.45, 2.6, 0.5, DOCS[k], hot=True, fs=9.5)
            cell(ax, x + 0.45, 1.35, 2.6, 0.9, "용어 사전\n포스팅 목록", hot=True, fs=9)
    if step == 3:
        moral(ax, 6.0, 0.4, "샤드는 자기 몫 문서로 만든 작은 인덱스예요")


# ── 샤드 번호는 계산으로 ──────────────────────────────────────────
ROUTE = [("order-8", 30, 0), ("order-4", 25, 1), ("order-1", 41, 2)]


def route(ax, step):
    for x, t in ((1.2, "_id"), (5.45, "해시값"), (7.4, "÷ 3 나머지"), (10.35, "샤드")):
        label(ax, x, 6.1, t, fs=10, color=INK)
    for k, (i, h, sh) in enumerate(ROUTE):
        y = 4.75 - k * 1.2
        mine = k == 2
        if mine and step == 1:
            cell(ax, 0.3, y, 1.8, 0.7, i, hot=True, fs=11)
            label(ax, 2.4, y + 0.35, "?", fs=16, color=RED, bold=True)
            for xx, w in ((2.7, 1.8), (5.05, 0.8), (6.9, 1.0), (9.2, 2.3)):
                empty(ax, xx, y, w, 0.7)
            continue
        now = mine and step == 2
        cell(ax, 0.3, y, 1.8, 0.7, i, fs=11)
        arrow(ax, (2.15, y + 0.35), (2.65, y + 0.35), color=RED if now else GREY, ms=11)
        box(ax, 2.7, y, 1.8, 0.7, fc=PAPER)
        label(ax, 3.6, y + 0.35, "해시 함수", fs=10)
        arrow(ax, (4.55, y + 0.35), (5.0, y + 0.35), color=RED if now else GREY, ms=11)
        cell(ax, 5.05, y, 0.8, 0.7, h, fs=11, hot=now)
        if now:
            empty(ax, 6.9, y, 1.0, 0.7)
            empty(ax, 9.2, y, 2.3, 0.7)
            continue
        hot = mine and step == 3
        arrow(ax, (5.9, y + 0.35), (6.85, y + 0.35), color=RED if hot else GREY, ms=11)
        cell(ax, 6.9, y, 1.0, 0.7, h % 3, fs=11, hot=hot)
        arrow(ax, (7.95, y + 0.35), (9.15, y + 0.35), color=RED if hot else GREY, ms=11)
        shard(ax, 9.2, y, 2.3, 0.7, f"샤드 {sh}", fc=SC[sh], hot=hot, fs=10.5, top=False)
    label(ax, 11.7, 0.35, "해시값은 설명용으로 작게 적었어요", fs=9, color=INK, ha="right")
    if step == 1:
        label(ax, 6.0, 1.2, "order-8과 order-4는 이미 자리를 찾았어요", fs=10.5, color=INK)
    if step == 3:
        moral(ax, 6.0, 1.2, "어느 노드든 _id만 알면 같은 샤드를 계산해요")


# ── 꺼낼 때 묻는 샤드 ──────────────────────────────────────────────
def get(ax, step):
    ys = [4.55, 3.0, 1.45]
    for k, y in enumerate(ys):
        shard(ax, 8.6, y, 3.0, 1.05, f"샤드 {k}", fc=SC[k], hot=(step == 2) or (step == 1 and k == 2), top=False, fs=11)
    on1 = step == 1
    cell(ax, 0.3, 1.45, 3.6, 1.05, "번호로 꺼내기\norder-1", hot=on1, fs=10.5)
    arrow(ax, (4.0, 1.97), (8.5, 1.97), color=RED if on1 else GREY, ms=13)
    label(ax, 6.25, 1.65, "샤드 2에만 물어요", fs=10.5, color=RED if on1 else GREY)
    if step == 1:
        empty(ax, 0.3, 4.55, 3.6, 1.05)
        return
    cell(ax, 0.3, 4.55, 3.6, 1.05, "낱말로 찾기\n'배송'", hot=True, fs=10.5)
    for y in ys:
        arrow(ax, (4.0, 5.07), (8.5, y + 0.52), color=RED, ms=12)
    label(ax, 6.0, 5.9, "샤드 셋에 다 물어요", fs=10.5, color=RED)
    moral(ax, 6.0, 0.6, "번호로 꺼내면 샤드 하나, 낱말로 찾으면 샤드 전부")


# ── 라우팅 값 ─────────────────────────────────────────────────────
SX = [6.0, 7.95, 9.9]


def photos(ax, k, names, hot=False):
    for j, n in enumerate(names):
        cell(ax, SX[k] + 0.1 + (j % 2) * 0.85, 3.55 - (j // 2) * 0.55, 0.78, 0.45, n, hot=hot, fs=8.5)


def lane(ax, y, title, chip, red, target, below=False, side=False):
    """왼쪽 요청 줄: 값 → 해시 함수 → 샤드. 위 줄은 샤드 윗변으로, below=True면 샤드 아래로 돌아 들어간다."""
    c = RED if red else GREY
    label(ax, 0.3, y + 0.95, title, fs=10.5, ha="left", bold=True, color=RED if red else "#222")
    cell(ax, 0.3, y, 2.3, 0.6, chip, hot=red, fs=10)
    arrow(ax, (2.65, y + 0.3), (3.05, y + 0.3), color=c, ms=11)
    box(ax, 3.1, y, 1.6, 0.6, fc=PAPER)
    label(ax, 3.9, y + 0.3, "해시 함수", fs=9.5)
    for t in target:
        if below:
            arrow(ax, (4.8, y + 0.15), (SX[t] + 0.9, 1.25), color=c, ms=12, rad=0.2)
        elif y > 4 and side:
            arrow(ax, (4.8, y + 0.3), (SX[t] - 0.05, y + 0.3), color=c, ms=12)
        elif y > 4:
            arrow(ax, (4.8, y + 0.3), (SX[t] + 0.9, 4.55), color=c, ms=12)
        else:
            arrow(ax, (4.8, y + 0.3), (SX[t] - 0.05, 2.9), color=c, ms=12)


def routing(ax, step):
    tall = step == 5
    for k in range(3):
        top = 6.3 if (tall and k == 0) else 4.5
        shard(ax, SX[k], 1.3, 1.8, top - 1.3, f"샤드 {k}", fc=SC[k] if k == 0 or step == 1 else "white",
              hot=(tall and k == 0) or (step == 4 and k == 2))
    if step == 1:
        lane(ax, 5.0, "사진을 _id로 넣으면", "m1~m9", True, (0, 1, 2))
        for k, ns in enumerate([["m2", "m5", "m9"], ["m3", "m6", "m8"], ["m1", "m4", "m7"]]):
            photos(ax, k, ns, hot=True)
        label(ax, 2.8, 1.8, "user-7의 사진이\n샤드 셋에 흩어져요", fs=10.5, color=RED)
        return
    lane(ax, 5.0, "routing=user-7로 넣으면", "user-7", step == 2, (0,), side=tall)
    photos(ax, 0, [f"m{j}" for j in range(1, 10)], hot=(step == 2))
    if tall:
        for j in range(4):
            cell(ax, SX[0] + 0.1 + (j % 2) * 0.85, 5.3 - (j // 2) * 0.55, 0.78, 0.45, "m⋯", hot=True, fs=8.5)
        label(ax, SX[0] + 0.9, 4.35, "⋮", fs=12, color=RED)
        label(ax, 8.0, 5.75, "사진이 아주 많은 user-7", fs=10.5, color=RED, ha="left")
    if step == 3:
        lane(ax, 1.6, "user-7의 사진 찾기", "routing=user-7", True, (0,))
        for k in (1, 2):
            label(ax, SX[k] + 0.9, 2.6, "안 물어요", fs=9.5, color=GREY)
        moral(ax, 6.0, 0.55, "같은 라우팅 값을 주면 샤드 하나에만 물어요")
    elif step == 4:
        lane(ax, 1.6, "m1을 라우팅 값 없이 꺼내면", "m1 (_id)", True, (2,), below=True)
        label(ax, SX[2] + 0.9, 2.6, "없음\n(404)", fs=11, color=RED, bold=True)
    if step == 5:
        moral(ax, 6.0, 0.55, "한 사용자의 사진이 많으면 그 샤드만 커져요")


# ── 샤드 수를 바꾸면 ───────────────────────────────────────────────
def reshuffle(ax, step):
    label(ax, 0.3, 6.2, "해시값 0~11을 샤드 수로 나눈 나머지로 담으면", fs=11.5, ha="left", bold=True)
    for n, y0 in ((3, 3.9), (4, 1.3)):
        label(ax, 0.3, y0 + 0.55, f"샤드\n{n}개", fs=10.5, ha="left", color=RED if (n == 4 and step == 2) else INK)
        W = 10.4 / n
        for s in range(n):
            x = 1.3 + s * W
            w = W - 0.2
            label(ax, x + w - 0.05, y0 + 1.32, f"샤드 {s}", fs=9.5, color=INK, ha="right")
            if n == 4 and step == 1:
                empty(ax, x, y0, w, 1.1)
                continue
            ax.add_patch(Rectangle((x, y0), w, 1.1, fc="white", ec=INK, lw=1.2))
            for j, h in enumerate([h for h in range(12) if h % n == s]):
                moved = n == 4 and (h % 3 != h % 4)
                cell(ax, x + 0.12 + j * 0.78, y0 + 0.2, 0.68, 0.7, h, hot=moved, fs=10.5, fc=None if moved else SC[h % 3])
    if step == 2:
        moral(ax, 6.0, 0.45, "12개 중 9개가 다른 샤드로 가요")


def lost(ax, step):
    ax.add_patch(Rectangle((0.2, 0.95), 11.5, 2.6, fill=False, ec=INK, lw=1.2))
    label(ax, 0.35, 3.3, "ES (샤드 4개)", fs=10.5, ha="left", bold=True)
    for s in range(4):
        x = 0.45 + s * 2.85
        shard(ax, x, 1.1, 2.6, 1.85, f"샤드 {s}", fc=SC[s] if s < 3 else "white", hot=(step == 1 and s == 3), fs=10)
    cell(ax, 0.45 + 2 * 2.85 + 0.4, 1.3, 1.8, 0.6, "order-1", fs=10)
    if step == 1:
        label(ax, 0.45 + 3 * 2.85 + 1.3, 2.0, "새로 생김", fs=10, color=RED)
        bubble(ax, 6.4, 4.2, 5.3, 1.5, "샤드 수만 4개로 바뀌었다고\n해 봐요 (문서는 그대로)", (9.0, 3.6), fs=11)
        return
    ask = "order-1 꺼내기" if step == 2 else "order-1 다시 쓰기"
    cell(ax, 0.3, 4.95, 2.6, 0.65, ask, hot=True, fs=10.5)
    label(ax, 3.1, 5.27, "41 ÷ 4 나머지 1", fs=10.5, ha="left", color=RED)
    arrow(ax, (1.6, 4.9), (4.4, 3.0), color=RED, ms=14)
    if step == 2:
        label(ax, 4.6, 1.6, "없어요", fs=11, color=RED, bold=True)
        bubble(ax, 6.4, 4.2, 5.3, 1.5, "샤드 1에는 order-1이 없어요\n'없는 문서'라고 답해요", (9.0, 3.6), hot=True, fs=10.5)
    else:
        cell(ax, 0.45 + 2.85 + 0.4, 1.3, 1.8, 0.6, "order-1", hot=True, fs=10)
        bubble(ax, 6.4, 4.2, 5.3, 1.5, "샤드 2의 옛것도 남아\n같은 번호가 두 개예요", (9.0, 3.6), hot=True, fs=10.5)
        moral(ax, 6.0, 0.4, "그래서 ES는 샤드 수를 바꾸지 못하게 막아요")


# ── 심화: 노드를 늘리면 ───────────────────────────────────────────
def relocate(ax, step):
    nodes = [[0, 1], [2, 3], [4, 5], []] if step == 1 else [[0, None], [2, 3], [4, 5], [1]]
    for n, shs in enumerate(nodes):
        x = 0.3 + n * 2.9
        if step == 1 and n == 3:
            empty(ax, x, 1.6, 2.65, 2.2)
            label(ax, x + 1.32, 2.7, "새 노드 4", fs=10, color=GREY)
            continue
        box(ax, x, 1.6, 2.65, 2.2, fc="white", ec=GREY)
        label(ax, x + 1.32, 3.45, f"노드 {n + 1}", fs=10, color=INK)
        for j, s in enumerate(shs):
            if s is None:
                empty(ax, x + 0.12 + j * 1.25, 1.95, 1.15, 0.8)
                continue
            hot = step == 2 and s == 1
            cell(ax, x + 0.12 + j * 1.25, 1.95, 1.15, 0.8, f"샤드 {s}", hot=hot, fs=9.5, fc=None if hot else SC6[s])
    if step == 1:
        label(ax, 6.0, 5.3, "샤드 6개짜리 인덱스에 노드를 한 대 더 붙여요", fs=11, color=INK)
    else:
        arrow(ax, (2.0, 3.9), (9.6, 3.9), color=RED, ms=15, rad=-0.3)
        label(ax, 5.8, 5.55, "샤드 1을 통째로 옮겨요", fs=11, color=RED)
        moral(ax, 6.0, 0.8, "문서는 다시 계산하지 않고 샤드만 옮겨요")


# ── 쪼개기 ────────────────────────────────────────────────────────
OLD0 = [0, 3, 6, 9]


def split(ax, step):
    label(ax, 0.3, 6.2, "옛 샤드 0 (3으로 나눈 나머지가 0)", fs=11, ha="left", bold=True)
    for j, h in enumerate(OLD0):
        cell(ax, 0.3 + j * 0.85, 5.15, 0.75, 0.7, h, fs=11, fc=BLUE)
    for k, (n, y) in enumerate([(6, 3.4), (4, 1.2)]):
        on = step == k + 2
        label(ax, 0.3, y + 1.3, "6으로 나누면 (샤드 6개)" if n == 6 else "4로 나누면 (샤드 4개)", fs=10.5, ha="left",
              bold=True, color=RED if on else "#222")
        W = 11.4 / n
        for t in range(n):
            x = 0.3 + t * W
            if step < k + 2:
                empty(ax, x, y, W - 0.15, 0.95)
                continue
            hs = [h for h in OLD0 if h % n == t]
            got = bool(hs)
            ax.add_patch(Rectangle((x, y), W - 0.15, 0.95, fc=(PINK if on else BLUE) if got else "white",
                                   ec=RED if (on and got) else INK, lw=1.8 if (on and got) else 1.1))
            label(ax, x + (W - 0.15) / 2, y + 0.7, f"샤드 {t}", fs=9.5, color=INK)
            label(ax, x + (W - 0.15) / 2, y + 0.3, "  ".join(map(str, hs)), fs=11, color=RED if on else "#222", bold=got)
        if step >= k + 2:
            label(ax, 11.7, y + 1.3, "두 샤드로만 가요" if n == 6 else "네 샤드로 다 흩어져요", fs=10.5, ha="right",
                  color=RED if on else INK)
    if step == 3:
        moral(ax, 6.0, 0.45, "배수가 아닌 수로 나누면 옛 샤드 하나가 다 흩어져요")


def link(ax, step):
    box(ax, 3.6, 4.55, 4.8, 1.35, fc=NOTE)
    label(ax, 6.0, 5.62, "옛 샤드 0의 파일", fs=10.5, bold=True)
    cells(ax, 4.2, 4.7, OLD0, w=0.8, h=0.6, gap=0.12, fs=10.5)
    mine = {0: (0, 6), 3: (3, 9)}
    for t, x in ((0, 0.5), (3, 6.9)):
        if step == 1:
            empty(ax, x, 1.3, 4.6, 1.8)
            label(ax, x + 2.3, 2.2, f"새 샤드 {t}", fs=10.5, color=GREY)
            continue
        box(ax, x, 1.3, 4.6, 1.8, fc="white", ec=INK)
        label(ax, x + 2.3, 2.8, f"새 샤드 {t}", fs=10.5, bold=True)
        for i, h in enumerate(OLD0):
            gone = step == 3 and h not in mine[t]
            cell(ax, x + 0.4 + i * 1.0, 1.5, 0.85, 0.65, h, fs=10.5, hot=(step == 2) or gone, fc=LIGHT if gone else None)
            if gone:
                ax.plot([x + 0.4 + i * 1.0, x + 1.25 + i * 1.0], [1.5, 2.15], color=RED, lw=1.8)
        end = (4.75, 4.5) if t == 0 else (7.25, 4.5)
        arrow(ax, (x + 2.3, 3.15), end, color=RED if step == 2 else GREY, ms=13)
        if step == 3:
            other = [h for h in OLD0 if h not in mine[t]]
            label(ax, x + 2.3, 0.95, f"{other[0]}과 {other[1]}에 '지웠음' 표시", fs=10, color=RED)
    if step == 2:
        label(ax, 6.0, 3.65, "이름표 하나 더\n(하드 링크)", fs=10.5, color=RED)
    if step == 3:
        moral(ax, 6.0, 0.35, "다른 샤드에서 받아 올 문서가 없어서 빨라요")


# ── 라우팅 칸 ─────────────────────────────────────────────────────
def cuts(ax, step):
    label(ax, 0.3, 6.15, "칸 768개를 24칸으로 줄여 그렸어요", fs=11, ha="left", bold=True)
    X0, W = 1.5, 6.6
    for k, n in enumerate([3, 6, 9]):
        y = 4.6 - k * 1.5
        on = step == k + 1
        label(ax, 0.3, y + 0.35, f"{n}조각", fs=11, ha="left", color=RED if on else INK, bold=on)
        if step < k + 1:
            empty(ax, X0, y, W, 0.7)
            continue
        bad = n == 9
        ax.add_patch(Rectangle((X0, y), W, 0.7, fc=PINK if bad else YEL, ec=RED if bad else INK, lw=1.2))
        for t in range(1, 24):
            x = X0 + W * t / 24
            ax.plot([x, x], [y + 0.42, y + 0.7], color=INK, lw=0.8)
        for c in range(1, n):
            x = X0 + W * c / n
            ok = (24 * c) % n == 0
            ax.plot([x, x], [y - 0.12, y + 0.82], color="#222" if ok else RED, lw=2.4)
        label(ax, X0 + W + 0.2, y + 0.35, "칸 한가운데를 지나요" if bad else "칸 경계에서 잘려요", fs=10.5, ha="left",
              color=RED if on else INK)
    if step == 3:
        moral(ax, 6.0, 0.55, "칸 수를 나누어떨어지게 하는 수로만 쪼개요")


# ── 심화: 9.3까지의 칸 ────────────────────────────────────────────
def slots(ax, step):
    label(ax, 0.3, 6.2, "ES 7.0~9.3, 칸 768개를 6개로 줄여 그렸어요", fs=11, ha="left", bold=True)
    X0, W = 1.5, 1.7
    label(ax, 0.3, 5.0, "칸", fs=10.5, ha="left", color=INK)
    for s in range(6):
        cell(ax, X0 + s * W, 4.65, W - 0.1, 0.7, f"칸 {s}", fs=10, fc=SC[s // 2])
    label(ax, 0.3, 3.55, "샤드\n3개", fs=10.5, ha="left", color=INK)
    label(ax, 0.3, 1.45, "샤드\n6개", fs=10.5, ha="left", color=RED if step == 2 else INK)
    for p in range(3):
        x = X0 + p * 2 * W
        ax.add_patch(Rectangle((x, 3.2), 2 * W - 0.1, 0.75, fc=SC[p], ec=INK, lw=1.2))
        label(ax, x + W - 0.05, 3.57, f"샤드 {p} (칸 {2 * p}, {2 * p + 1})", fs=10)
        for c in range(2):
            t = 2 * p + c
            xx = X0 + t * W
            if step == 1:
                empty(ax, xx, 1.0, W - 0.1, 0.9)
                continue
            hot = p == 2
            arrow(ax, (x + W - 0.05, 3.15), (xx + (W - 0.1) / 2, 1.95), color=RED if hot else GREY, lw=1.4, ms=11)
            ax.add_patch(Rectangle((xx, 1.0), W - 0.1, 0.9, fc=PINK if hot else SC[p], ec=RED if hot else INK,
                                   lw=2 if hot else 1.2))
            label(ax, xx + (W - 0.1) / 2, 1.45, f"샤드 {t}\n칸 {t}", fs=9.5, color=RED if hot else "#222")
    if step == 2:
        moral(ax, 6.0, 0.45, "샤드 하나가 맡던 칸을 반씩 나눠 맡아요")


# ── 샤드 크기 ─────────────────────────────────────────────────────
def size(ax, step):
    label(ax, 0.3, 6.2, "1년 뒤 100 GB가 될 상품 인덱스", fs=11, ha="left", bold=True)
    base, k = 1.4, 3.6 / 50
    for gb in (10, 50):
        y = base + gb * k
        ax.plot([1.4, 11.7], [y, y], color=INK, lw=1.0, ls="--")
        label(ax, 0.3, y, f"{gb} GB", fs=10, ha="left", color=INK)
    label(ax, 11.7, base + 50 * k + 0.25, "권하는 크기의 끝", fs=9.5, ha="right", color=INK)
    ax.plot([1.4, 11.7], [base, base], color=INK, lw=1.2)
    for j in range(2):
        x = 2.0 + j * 1.6
        ax.add_patch(Rectangle((x, base), 1.3, 50 * k, fc=PINK if step == 1 else BLUE, ec=RED if step == 1 else INK, lw=1.5))
        label(ax, x + 0.65, base + 50 * k / 2, "50\nGB", fs=10, color=RED if step == 1 else "#222")
    label(ax, 3.3, 0.95, "샤드 2개", fs=10.5, color=RED if step == 1 else INK)
    if step == 1:
        label(ax, 3.3, 0.45, "권하는 크기의 끝에 닿아요", fs=10.5, color=RED)
        for j in range(3):
            empty(ax, 6.6 + j * 1.6, base, 1.3, 2.4)
        return
    for j in range(3):
        x = 6.6 + j * 1.6
        ax.add_patch(Rectangle((x, base), 1.3, 33 * k, fc=PINK, ec=RED, lw=1.5))
        label(ax, x + 0.65, base + 33 * k / 2, "33\nGB", fs=10, color=RED)
    label(ax, 8.55, 0.95, "샤드 3개", fs=10.5, color=RED)
    moral(ax, 6.0, 0.35, "샤드 3개면 하나에 여유가 있어요")


def decide():
    """샤드 수 정하기 (한 장)."""
    fig, ax = canvas(10, 3.2, 15, 4.8)
    box(ax, 0.3, 3.0, 5.6, 1.4, fc=NOTE)
    label(ax, 3.1, 3.7, "시간이 지나며 계속 쌓이기만 하나요?\n(가계부·주문 기록)", fs=10.5, bold=True)
    arrow(ax, (6.0, 3.7), (7.4, 3.7), color=RED)
    label(ax, 6.7, 4.0, "예", fs=10, color=RED)
    box(ax, 7.5, 3.0, 7.2, 1.4, fc=PINK, ec=RED)
    label(ax, 11.1, 3.7, "기간마다 새 인덱스\n만들 때마다 샤드 수를 다시 정해요", fs=10.5, color=RED)
    arrow(ax, (3.1, 2.9), (3.1, 1.7))
    label(ax, 3.6, 2.3, "아니요", fs=10, color=INK, ha="left")
    box(ax, 0.3, 0.3, 5.6, 1.3, fc=NOTE)
    label(ax, 3.1, 0.95, "앞으로 클 크기 ÷ 샤드 하나 크기\n(10~50 GB 정도)", fs=10.5, bold=True)
    arrow(ax, (6.0, 0.95), (7.4, 0.95))
    box(ax, 7.5, 0.3, 7.2, 1.3, fc=PAPER)
    label(ax, 11.1, 0.95, "그 수로 정하고\n예상보다 커지면 2배로 쪼개요", fs=10.5)
    save(fig, OUT, "es03-decide.svg")


# ── 정리: 낱말 카드 ────────────────────────────────────────────────
def cards():
    fig, ax = canvas(6.4, 11.6, 9.8, 16.3)
    W, H = 4.6, 3.8

    def card(i, name, line):
        col, row = i % 2, i // 2
        x, y = 0.2 + col * 4.9, 12.3 - row * 4.05
        box(ax, x, y, W, H, fc="white")
        label(ax, x + 0.25, y + H - 0.4, name, fs=12.5, ha="left", bold=True)
        label(ax, x + W / 2, y + 0.45, line, fs=10, color=INK)
        return x, y

    x, y = card(0, "문서", "ES에 넣는 기록 하나 (주문 하나)")
    cell(ax, x + 1.3, y + 1.9, 2.0, 0.65, "order-1", hot=True, fs=11)
    x, y = card(1, "샤드", "인덱스를 나눈 작은 인덱스")
    for k in range(3):
        cell(ax, x + 0.5 + k * 1.25, y + 1.8, 1.1, 0.8, f"샤드 {k}", hot=(k == 0), fc=None if k == 0 else SC[k], fs=9.5)
    x, y = card(2, "노드", "ES가 돌아가는 컴퓨터 한 대")
    box(ax, x + 1.0, y + 1.3, 2.6, 1.6, fc="white", ec=RED, lw=1.5)
    label(ax, x + 2.3, y + 2.6, "노드 1", fs=9.5, color=RED)
    cell(ax, x + 1.5, y + 1.5, 1.6, 0.6, "샤드 0", fs=9.5, fc=BLUE)
    x, y = card(3, "라우팅", "문서가 갈 샤드를 계산으로 정하기")
    cell(ax, x + 0.3, y + 1.9, 1.4, 0.6, "order-1", fs=9.5)
    label(ax, x + 2.25, y + 2.2, "41÷3", fs=9.5, color=RED)
    arrow(ax, (x + 2.8, y + 2.2), (x + 3.15, y + 2.2), ms=9, color=RED)
    cell(ax, x + 3.2, y + 1.9, 1.15, 0.6, "샤드 2", hot=True, fs=9.5)
    x, y = card(4, "라우팅 값", "_id 대신 계산에 넣는 값")
    cell(ax, x + 0.3, y + 1.9, 1.6, 0.6, "user-7", hot=True, fs=10)
    arrow(ax, (x + 2.0, y + 2.2), (x + 2.6, y + 2.2), ms=10, color=RED)
    cell(ax, x + 2.7, y + 1.9, 1.6, 0.6, "샤드 0", fs=9.5, fc=BLUE)
    x, y = card(5, "쪼개기", "샤드를 2배, 4배로 늘린 새 인덱스")
    cell(ax, x + 0.2, y + 1.9, 1.15, 0.6, "샤드 0", fs=9.5, fc=BLUE)
    arrow(ax, (x + 1.45, y + 2.2), (x + 1.95, y + 2.2), ms=10, color=RED)
    cells(ax, x + 2.05, y + 1.9, ["샤드 0", "샤드 3"], w=1.15, h=0.6, gap=0.1, hot=(0, 1), fs=9.5)
    x, y = card(6, "하드 링크", "한 파일에 붙인 이름표 하나 더")
    cell(ax, x + 1.5, y + 2.4, 1.6, 0.55, "파일", fs=10, fc=NOTE)
    for xx, t in ((x + 0.3, 0), (x + 2.8, 3)):
        cell(ax, xx, y + 1.25, 1.5, 0.5, f"새 샤드 {t}", hot=True, fs=9)
        arrow(ax, (xx + 0.75, y + 1.8), (x + 2.3, y + 2.35), ms=9, color=RED)
    x, y = card(7, "라우팅 칸", "쪼갤 수 있는지 따지는 칸 (768)")
    ax.add_patch(Rectangle((x + 0.4, y + 1.9), 3.8, 0.5, fc=YEL, ec=INK, lw=1.0))
    for t in range(1, 12):
        xx = x + 0.4 + 3.8 * t / 12
        ax.plot([xx, xx], [y + 2.15, y + 2.4], color=INK, lw=0.7)
    for c in (1, 2):
        xx = x + 0.4 + 3.8 * c / 3
        ax.plot([xx, xx], [y + 1.8, y + 2.5], color="#222", lw=2.0)
    save(fig, OUT, "es03-cards.svg")


if __name__ == "__main__":
    S, L = (7.2, 3.8), (12, 6.6)
    stage(open_, 3, OUT, "es03-open", S, L)
    stage(shards, 3, OUT, "es03-shards", S, L)
    stage(route, 3, OUT, "es03-route", S, L)
    stage(get, 2, OUT, "es03-get", S, L)
    stage(routing, 3, OUT, "es03-routing", S, L)
    stage(lambda ax, k: routing(ax, k + 3), 2, OUT, "es03-cost", S, L)
    stage(reshuffle, 2, OUT, "es03-reshuffle", S, L)
    stage(lost, 3, OUT, "es03-lost", S, L)
    stage(relocate, 2, OUT, "es03-relocate", S, L)
    stage(split, 3, OUT, "es03-split", S, L)
    stage(link, 3, OUT, "es03-link", S, L)
    stage(cuts, 3, OUT, "es03-cuts", S, L)
    stage(slots, 2, OUT, "es03-slots", S, L)
    stage(size, 2, OUT, "es03-size", S, L)
    decide()
    stage(back, 3, OUT, "es03-back", S, L)
    cards()
