"""컴퓨터 1편 그림 만들기. 실행: python lab/fig_c01.py  → docs/computer/img/01/*.svg

무대는 게임 화면이 켜진 컴퓨터 하나다. 그림마다 지금 볼 곳만 빨강으로 칠한다.
예시는 편 끝까지 같은 수를 쓴다: 별 하나 10점, 점수 60 → 70, 최고 기록 50 → 70.
그림 안 글씨는 낱말과 숫자만 둔다. 문장은 본문에 쓴다.
검토용 PNG가 필요하면 FIG_FMT=png FIG_OUT=<폴더> 로 실행한다.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "es"))
from figkit import (GREY, INK, LIGHT, NOTE, PAPER, PINK, RED, YEL, arrow, box, canvas, label, save)  # noqa: E402
from matplotlib.patches import Circle, Rectangle  # noqa: E402

OUT = os.environ.get("FIG_OUT") or os.path.join(os.path.dirname(__file__), "..", "docs", "computer", "img", "01")
os.makedirs(OUT, exist_ok=True)

ORDERS = ["별 → 점수 + 10", "끝 → 두 수 비교", "점수가 크면 → 최고 기록 바꾸기", "바꿨으면 → 새 기록!"]
SMALL = ((4.6, 4.2), (7.0, 6.6))       # 컴퓨터만 있는 그림
WIDE = ((7.6, 4.2), (12.2, 6.6))       # 컴퓨터 + 쪽지


def star(ax, x, y, hot=False, size=30):
    ax.plot(x, y, marker="*", markersize=size, color=RED if hot else YEL, mec=INK, mew=1.0)


def hud(ax, x, name, value, hot=False):
    """화면 위쪽 점수판 칸."""
    label(ax, x + 1.05, 5.45, name, fs=11, color=RED if hot else INK)
    ax.add_patch(Rectangle((x, 4.25), 2.1, 0.95, fc=PINK if hot else "white", ec=RED if hot else INK, lw=2.0 if hot else 1.3))
    label(ax, x + 1.05, 4.72, value, fs=22, color=RED if hot else "#222", bold=True)


def computer(ax, score="60", best="50", hot_score=False, hot_best=False):
    """무대: 게임 화면이 켜진 컴퓨터. 화면 위쪽에 점수판 두 칸."""
    box(ax, 0.4, 1.3, 6.2, 5.05, fc=LIGHT, ec=INK, lw=1.8)
    ax.add_patch(Rectangle((0.7, 1.6), 5.6, 4.45, fc="white", ec=INK, lw=1.2))
    ax.add_patch(Rectangle((3.0, 0.75), 1.0, 0.55, fc=LIGHT, ec=INK, lw=1.2))
    ax.add_patch(Rectangle((2.3, 0.55), 2.4, 0.22, fc=LIGHT, ec=INK, lw=1.2))
    hud(ax, 0.95, "점수", score, hot=hot_score)
    hud(ax, 3.95, "최고 기록", best, hot=hot_best)


def notes(ax, hot=()):
    """오른쪽 쪽지 네 장(명령어)."""
    label(ax, 9.7, 3.95, "쪽지", fs=12, color=INK, bold=True)
    for i, what in enumerate(ORDERS):
        y = 3.05 - i * 0.68
        on = i in hot
        box(ax, 7.55, y, 4.4, 0.56, fc=PINK if on else NOTE, ec=RED if on else INK, lw=1.8 if on else 1.2)
        ax.add_patch(Circle((7.2, y + 0.28), 0.22, fc="white", ec=RED if on else INK, lw=1.3))
        label(ax, 7.2, y + 0.28, i + 1, fs=10.5, color=RED if on else INK, bold=True)
        label(ax, 7.7, y + 0.28, what, fs=10.5, ha="left", color=RED if on else "#222")


def one(draw, name, size=SMALL):
    fig, ax = canvas(*size[0], *size[1])
    draw(ax)
    save(fig, OUT, name)


def game_1(ax):
    computer(ax, "60", "50")
    star(ax, 4.6, 3.0)
    ax.plot([1.4, 4.0], [3.0, 3.0], color=GREY, lw=2, ls=":")
    label(ax, 1.2, 3.0, "●", fs=20, color=INK)
    label(ax, 3.5, 2.05, "별 하나 = 10점", fs=11, color=INK)


def game_2(ax):
    computer(ax, "70", "70", hot_score=True, hot_best=True)
    label(ax, 3.5, 3.45, "게임 끝", fs=15, color=INK)
    label(ax, 3.5, 2.45, "새 기록!", fs=24, color=RED, bold=True)


def map_():
    fig, ax = canvas(9.0, 3.2, 13.5, 4.6)
    items = [("별을 먹으면", "더하기"), ("게임이 끝나면", "비교"), ("더 크면", "바꿔 적기")]
    for i, (when, what) in enumerate(items):
        x = 0.3 + i * 4.5
        box(ax, x, 0.9, 3.6, 2.7, fc="white")
        ax.add_patch(Rectangle((x + 0.25, 2.05), 3.1, 1.3, fc=PAPER, ec=INK, lw=1.0))
        if i == 0:
            label(ax, x + 1.8, 2.7, "60 + 10", fs=15, bold=True)
        elif i == 1:
            label(ax, x + 1.8, 2.7, "70 ? 50", fs=15, bold=True)
        else:
            label(ax, x + 1.25, 2.7, "50", fs=15, color=GREY, bold=True)
            label(ax, x + 1.8, 2.7, "→", fs=15, color=INK)
            label(ax, x + 2.35, 2.7, "70", fs=15, color=RED, bold=True)
        label(ax, x + 0.3, 3.95, "①②③"[i], fs=14, color=RED, bold=True, ha="left")
        label(ax, x + 1.8, 1.65, what, fs=14, bold=True)
        label(ax, x + 1.8, 1.15, when, fs=11, color=INK)
        if i < 2:
            arrow(ax, (x + 3.7, 2.25), (x + 4.4, 2.25), ms=14)
    save(fig, OUT, "c01-map.svg")


def add(ax):
    computer(ax, "70", "50", hot_score=True)
    star(ax, 1.9, 2.9, size=22)
    label(ax, 3.9, 2.9, "60 + 10 = 70", fs=17, color=RED, bold=True)
    arrow(ax, (4.9, 3.25), (2.6, 4.15), color=RED, ms=14, rad=0.2)


def compare(ax):
    computer(ax, "70", "50", hot_score=True)
    label(ax, 3.5, 4.72, ">", fs=24, color=RED, bold=True)
    label(ax, 3.5, 2.9, "게임 끝", fs=15, color=INK)
    label(ax, 3.5, 2.1, "70 > 50", fs=17, color=RED, bold=True)


def write(ax):
    computer(ax, "70", "70", hot_best=True)
    label(ax, 3.5, 3.1, "게임 끝", fs=15, color=INK)
    label(ax, 2.9, 2.2, "50", fs=18, color=GREY, bold=True)
    ax.plot([2.55, 3.25], [2.2, 2.2], color=GREY, lw=2.5)
    label(ax, 3.6, 2.2, "→", fs=16, color=INK)
    label(ax, 4.3, 2.2, "70", fs=18, color=RED, bold=True)
    arrow(ax, (4.7, 2.45), (5.0, 4.15), color=RED, ms=14, rad=0.3)


def orders(ax):
    computer(ax, "60", "50")
    star(ax, 3.5, 3.0)
    notes(ax)


def back(ax):
    computer(ax, "70", "70")
    label(ax, 3.5, 3.45, "게임 끝", fs=15, color=INK)
    label(ax, 3.5, 2.45, "새 기록!", fs=24, color=INK, bold=True)
    for x, y, t in [(2.0, 3.95, "①"), (5.0, 3.95, "②③"), (5.5, 2.45, "④")]:
        label(ax, x, y, t, fs=13, color=RED, bold=True)
    notes(ax, hot=(0, 1, 2, 3))


def speed():
    fig, ax = canvas(7.6, 4.8, 10.5, 7.6)
    label(ax, 4.0, 7.0, "1초 동안", fs=15, color=INK)
    ax.add_patch(Circle((1.6, 3.6), 0.45, fc="white", ec=INK, lw=2))
    ax.plot([1.6, 1.6], [3.15, 1.9], color=INK, lw=2.5)
    ax.plot([1.0, 2.2], [2.8, 2.8], color=INK, lw=2.5)
    ax.plot([1.6, 1.1], [1.9, 1.0], color=INK, lw=2.5)
    ax.plot([1.6, 2.1], [1.9, 1.0], color=INK, lw=2.5)
    box(ax, 2.6, 1.6, 1.3, 0.5, fc=NOTE)
    label(ax, 3.25, 1.85, "더하기", fs=10)
    label(ax, 2.2, 0.3, "사람: 1번", fs=13)
    box(ax, 5.3, 1.0, 2.6, 1.8, fc=PAPER)
    ax.add_patch(Rectangle((6.3, 0.55), 0.6, 0.45, color=INK))
    label(ax, 6.6, 1.9, "컴퓨터", fs=14)
    # 쪽지 더미는 그림 위쪽 끝을 넘어가서 몇 장인지 셀 수 없게 그린다
    for k in range(30):
        box(ax, 8.5, 1.0 + k * 0.4, 1.4, 0.3, fc=NOTE, ec=RED, lw=1.2)
        ax.text(9.2, 1.15 + k * 0.4, "더하기", ha="center", va="center", fontsize=8, clip_on=True)
    label(ax, 7.4, 0.3, "컴퓨터: 25억 번쯤", fs=13, color=RED, bold=True)
    save(fig, OUT, "c01-speed.svg")


if __name__ == "__main__":
    one(game_1, "c01-game-1.svg")
    one(game_2, "c01-game-2.svg")
    map_()
    one(add, "c01-add.svg")
    one(compare, "c01-compare.svg")
    one(write, "c01-write.svg")
    one(orders, "c01-orders.svg", WIDE)
    one(back, "c01-back.svg", WIDE)
    speed()
