"""Elasticsearch 3편 그림 만들기. 실행: python lab/fig_es03.py  → docs/elasticsearch/img/03/*.svg

예시는 처음부터 끝까지 주문 기록(샤드 3개)과 order-1(해시값 41)을 잇는다.
그림 안 글씨는 낱말과 숫자만 둔다. 문장은 본문과 그림 설명에 둔다.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "es"))
from figkit import (GREY, INK, NOTE, PAPER, PINK, RED, arrow, box,  # noqa: E402
                    canvas, cell, label, outdir, save)
from matplotlib.patches import Rectangle  # noqa: E402

OUT = outdir("03")
SC = ["#f1f3f5", "#dde1e5", "#c4c9cf", "#aab0b7"]  # 샤드 구별은 회색 농도로만


def shard(ax, x, y, w, h, name, fc="white", hot=False, dim=False, fs=10.5, top=True):
    """샤드 상자. 이름은 상자 안 위쪽(top=False면 가운데)에 쓴다."""
    ec = RED if hot else (GREY if dim else INK)
    ax.add_patch(Rectangle((x, y), w, h, fc=PINK if hot else fc, ec=ec, lw=2.0 if hot else 1.2))
    label(ax, x + w / 2, y + h - 0.25 if top else y + h / 2, name, fs=fs,
          color=RED if hot else (GREY if dim else "#222"), bold=hot)


def one(draw, name, ylo=0.0, lim=(12, 6.6)):
    """한 장. ylo 아래 빈자리는 잘라 내고 글씨 크기는 다른 그림과 같게 둔다."""
    fig, ax = canvas(7.2, 3.8 * (lim[1] - ylo) / lim[1], *lim)
    ax.set_ylim(ylo, lim[1])
    draw(ax)
    save(fig, OUT, name)


# ── 1절: 인덱스는 샤드 여러 개로 ───────────────────────────────────
DOCS = ["order-8 ⋯", "order-4 ⋯", "order-1 ⋯"]


def shards(ax):
    box(ax, 3.4, 5.4, 5.2, 0.85, fc=PAPER)
    label(ax, 6.0, 5.82, "주문 인덱스", fs=11.5, bold=True)
    for k in range(3):
        x = 0.3 + k * 3.9
        box(ax, x, 0.95, 3.5, 3.4, fc="white", ec=GREY)
        label(ax, x + 1.75, 4.05, f"노드 {k + 1}", fs=10, color=INK)
        arrow(ax, (6.0, 5.35), (x + 1.75, 4.4), color=GREY, ms=13)
        shard(ax, x + 0.25, 1.15, 3.0, 2.55, f"샤드 {k}", fc=SC[k])
        cell(ax, x + 0.45, 2.45, 2.6, 0.5, DOCS[k], fs=9.5)
        cell(ax, x + 0.45, 1.35, 2.6, 0.9, "용어 사전\n포스팅 목록", hot=True, fs=9)


# ── 2절: 샤드 번호는 계산으로 ─────────────────────────────────────
ROUTE = [("order-8", 30, 0), ("order-4", 25, 1), ("order-1", 41, 2)]


def route(ax):
    for x, t in ((1.2, "_id"), (5.45, "해시값"), (7.4, "÷ 3 나머지"), (10.35, "샤드")):
        label(ax, x, 6.1, t, fs=10, color=INK)
    for k, (i, h, sh) in enumerate(ROUTE):
        y = 4.75 - k * 1.2
        hot = k == 2
        c = RED if hot else GREY
        cell(ax, 0.3, y, 1.8, 0.7, i, fs=11, hot=hot)
        arrow(ax, (2.15, y + 0.35), (2.65, y + 0.35), color=c, ms=11)
        box(ax, 2.7, y, 1.8, 0.7, fc=PAPER)
        label(ax, 3.6, y + 0.35, "해시 함수", fs=10)
        arrow(ax, (4.55, y + 0.35), (5.0, y + 0.35), color=c, ms=11)
        cell(ax, 5.05, y, 0.8, 0.7, h, fs=11, hot=hot)
        arrow(ax, (5.9, y + 0.35), (6.85, y + 0.35), color=c, ms=11)
        cell(ax, 6.9, y, 1.0, 0.7, h % 3, fs=11, hot=hot)
        arrow(ax, (7.95, y + 0.35), (9.15, y + 0.35), color=c, ms=11)
        shard(ax, 9.2, y, 2.3, 0.7, f"샤드 {sh}", fc=SC[sh], hot=hot, fs=10.5, top=False)


def get(ax):
    ys = [4.55, 3.0, 1.45]
    for k, y in enumerate(ys):
        shard(ax, 8.6, y, 3.0, 1.05, f"샤드 {k}", fc=SC[k], hot=(k == 2), top=False, fs=11)
    cell(ax, 0.3, 1.45, 3.6, 1.05, "번호로 꺼내기\norder-1", hot=True, fs=10.5)
    arrow(ax, (4.0, 1.97), (8.5, 1.97), color=RED, ms=13)
    label(ax, 6.25, 1.65, "샤드 2만", fs=10.5, color=RED)
    cell(ax, 0.3, 4.55, 3.6, 1.05, "낱말로 찾기\n'배송'", fs=10.5)
    for y in ys:
        arrow(ax, (4.0, 5.07), (8.5, y + 0.52), color=INK, ms=12)
    label(ax, 6.0, 5.9, "샤드 셋 모두", fs=10.5, color=INK)


# ── 3절: 라우팅 값 ────────────────────────────────────────────────
SX = [6.0, 7.95, 9.9]


def lane(ax, y, title, chip, red, t):
    """왼쪽 요청 줄: 값 → 해시 함수 → 샤드 t. 위 줄은 샤드 윗변으로, 아래 줄은 샤드 옆구리로 들어간다."""
    c = RED if red else GREY
    label(ax, 0.3, y + 0.95, title, fs=10.5, ha="left", bold=True, color=RED if red else "#222")
    cell(ax, 0.3, y, 2.3, 0.6, chip, hot=red, fs=10)
    arrow(ax, (2.65, y + 0.3), (3.05, y + 0.3), color=c, ms=11)
    box(ax, 3.1, y, 1.6, 0.6, fc=PAPER)
    label(ax, 3.9, y + 0.3, "해시 함수", fs=9.5)
    if y > 4:
        arrow(ax, (4.8, y + 0.3), (SX[t] + 0.9, 4.55), color=c, ms=12)
    else:
        arrow(ax, (4.8, y + 0.3), (SX[t] - 0.05, 2.9), color=c, ms=12)


def routing(ax):
    for k in range(3):
        shard(ax, SX[k], 1.3, 1.8, 3.2, f"샤드 {k}", fc=SC[k] if k == 0 else "white", dim=(k > 0))
    lane(ax, 5.0, "사진 m1~m9 넣을 때", "routing=user-7", False, 0)
    for j in range(9):
        cell(ax, SX[0] + 0.1 + (j % 2) * 0.85, 3.55 - (j // 2) * 0.55, 0.78, 0.45, f"m{j + 1}", fs=8.5)
    lane(ax, 1.6, "user-7 사진 찾을 때", "routing=user-7", True, 0)


# ── 4절: 샤드 수를 바꾸면 ─────────────────────────────────────────
def reshuffle(ax):
    label(ax, 0.3, 6.2, "해시값 0~11, 샤드 수로 나눈 나머지", fs=11.5, ha="left", bold=True)
    for n, y0 in ((3, 3.9), (4, 1.3)):
        label(ax, 0.3, y0 + 0.55, f"샤드\n{n}개", fs=10.5, ha="left", color=RED if n == 4 else INK)
        W = 10.4 / n
        for s in range(n):
            x = 1.3 + s * W
            w = W - 0.2
            label(ax, x + w - 0.05, y0 + 1.32, f"샤드 {s}", fs=9.5, color=INK, ha="right")
            ax.add_patch(Rectangle((x, y0), w, 1.1, fc="white", ec=INK, lw=1.2))
            for j, h in enumerate([h for h in range(12) if h % n == s]):
                moved = n == 4 and (h % 3 != h % 4)
                cell(ax, x + 0.12 + j * 0.78, y0 + 0.2, 0.68, 0.7, h, hot=moved, fs=10.5, fc=None if moved else SC[h % 3])
    label(ax, 6.0, 0.6, "자리 바뀜 9 / 12", fs=12.5, color=RED, bold=True)


def lost(ax, step):
    ax.add_patch(Rectangle((0.2, 0.95), 11.5, 2.6, fill=False, ec=INK, lw=1.2))
    label(ax, 0.35, 0.65, "ES (샤드 수만 4개, 문서는 그대로)", fs=10.5, ha="left", bold=True)
    for s in range(4):
        x = 0.45 + s * 2.85
        shard(ax, x, 1.1, 2.6, 1.85, f"샤드 {s}", fc=SC[s] if s < 3 else "white", fs=10)
    cell(ax, 0.45 + 2 * 2.85 + 0.4, 1.3, 1.8, 0.6, "order-1", fs=10, hot=(step == 2))
    cell(ax, 0.3, 4.95, 2.6, 0.65, "order-1 꺼내기" if step == 1 else "order-1 다시 쓰기", hot=True, fs=10.5)
    label(ax, 3.1, 5.27, "41 ÷ 4 나머지 1", fs=10.5, ha="left", color=RED)
    arrow(ax, (1.6, 4.9), (3.9, 3.0), color=RED, ms=14)
    if step == 1:
        label(ax, 4.6, 1.6, "없음", fs=11, color=RED, bold=True)
    else:
        cell(ax, 0.45 + 2.85 + 0.4, 1.3, 1.8, 0.6, "order-1", hot=True, fs=10)
        label(ax, 11.6, 4.3, "같은 번호 둘", fs=11.5, ha="right", color=RED, bold=True)


# ── 5절: 쪼개기 ───────────────────────────────────────────────────
OLD0 = [0, 3, 6, 9]


def split(ax):
    label(ax, 0.3, 6.2, "옛 샤드 0 (÷ 3 나머지 0)", fs=11, ha="left", bold=True)
    for j, h in enumerate(OLD0):
        cell(ax, 0.3 + j * 0.85, 5.15, 0.75, 0.7, h, fs=11, fc=SC[1])
    for n, y in ((6, 3.4), (4, 1.2)):
        on = n == 4
        label(ax, 0.3, y + 1.3, f"÷ {n} (샤드 {n}개)", fs=10.5, ha="left", bold=True, color=RED if on else "#222")
        W = 11.4 / n
        for t in range(n):
            x = 0.3 + t * W
            hs = [h for h in OLD0 if h % n == t]
            got = bool(hs)
            ax.add_patch(Rectangle((x, y), W - 0.15, 0.95, fc=(PINK if on else SC[1]) if got else "white",
                                   ec=RED if (on and got) else INK, lw=1.8 if (on and got) else 1.1))
            label(ax, x + (W - 0.15) / 2, y + 0.7, f"샤드 {t}", fs=9.5, color=INK)
            label(ax, x + (W - 0.15) / 2, y + 0.3, "  ".join(map(str, hs)), fs=11, color=RED if on else "#222", bold=got)
        label(ax, 11.7, y + 1.3, "네 곳" if on else "두 곳", fs=10.5, ha="right", color=RED if on else INK, bold=True)


def cuts(ax):
    label(ax, 0.3, 6.15, "라우팅 칸 768개 (24칸으로 줄임)", fs=11, ha="left", bold=True)
    X0, W = 1.5, 6.6
    for k, n in enumerate([3, 6, 9]):
        y = 4.6 - k * 1.5
        bad = n == 9
        label(ax, 0.3, y + 0.35, f"{n}조각", fs=11, ha="left", color=RED if bad else INK, bold=bad)
        ax.add_patch(Rectangle((X0, y), W, 0.7, fc=PINK if bad else SC[1], ec=RED if bad else INK, lw=1.2))
        for t in range(1, 24):
            x = X0 + W * t / 24
            ax.plot([x, x], [y + 0.42, y + 0.7], color=INK, lw=0.8)
        for c in range(1, n):
            x = X0 + W * c / n
            ok = (24 * c) % n == 0
            ax.plot([x, x], [y - 0.12, y + 0.82], color="#222" if ok else RED, lw=2.4)
        label(ax, X0 + W + 0.2, y + 0.35, "칸 가운데를 지남" if bad else "경계에서 잘림", fs=10.5, ha="left",
              color=RED if bad else INK)


# ── 6절: 샤드 수 정하기 ───────────────────────────────────────────
def decide():
    fig, ax = canvas(10, 3.2, 15, 4.8)
    box(ax, 0.3, 3.0, 5.6, 1.4, fc=NOTE)
    label(ax, 3.1, 3.7, "계속 쌓이는 데이터\n(가계부·주문 기록)", fs=10.5, bold=True)
    arrow(ax, (6.0, 3.7), (7.4, 3.7), color=RED)
    label(ax, 6.7, 4.0, "예", fs=10, color=RED)
    box(ax, 7.5, 3.0, 7.2, 1.4, fc=PINK, ec=RED)
    label(ax, 11.1, 3.7, "기간마다 새 인덱스\n만들 때마다 샤드 수 새로", fs=10.5, color=RED)
    arrow(ax, (3.1, 2.9), (3.1, 1.7))
    label(ax, 3.6, 2.3, "아니요", fs=10, color=INK, ha="left")
    box(ax, 0.3, 0.3, 5.6, 1.3, fc=NOTE)
    label(ax, 3.1, 0.95, "앞으로 클 크기 ÷ 샤드 하나 크기\n(10~50 GB)", fs=10.5, bold=True)
    arrow(ax, (6.0, 0.95), (7.4, 0.95))
    box(ax, 7.5, 0.3, 7.2, 1.3, fc=PAPER)
    label(ax, 11.1, 0.95, "그 수로 시작\n커지면 2배로 쪼개기", fs=10.5)
    save(fig, OUT, "es03-decide.svg")


if __name__ == "__main__":
    one(shards, "es03-shards.svg", 0.7)
    one(route, "es03-route.svg", 2.1)
    one(get, "es03-get.svg", 1.2)
    one(routing, "es03-routing.svg", 1.1)
    one(reshuffle, "es03-reshuffle.svg", 0.3)
    one(lambda ax: lost(ax, 1), "es03-lost-1.svg", 0.3)
    one(lambda ax: lost(ax, 2), "es03-lost-2.svg", 0.3)
    one(split, "es03-split.svg", 1.0)
    one(cuts, "es03-cuts.svg", 1.4)
    decide()
