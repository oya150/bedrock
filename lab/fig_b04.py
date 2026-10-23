"""인체 4편 그림 만들기. 실행: python lab/fig_b04.py  → docs/body/img/04/*.svg

글자는 SVG 안에 글자로 남긴다(글꼴 모양을 파일에 넣지 않는다). 보는 쪽 글꼴로 그려진다.
카드는 차분한 색으로, 강조(새로 받은 카드, 비교 화살표, 많이 든 일)만 빨강으로 칠한다.
"""
import itertools
import os

import matplotlib

matplotlib.use("svg")
import matplotlib.pyplot as plt
from matplotlib.patches import Arc, Circle, FancyArrowPatch, FancyBboxPatch, Rectangle

OUT = os.path.join(os.path.dirname(__file__), "..", "docs", "body", "img", "04")
os.makedirs(OUT, exist_ok=True)

plt.rcParams.update({
    "font.family": ["Apple SD Gothic Neo", "Noto Sans KR", "Malgun Gothic", "sans-serif"],
    "svg.fonttype": "none",
    "text.color": "#222",
    "figure.facecolor": "white",
    "savefig.facecolor": "white",
})

RED, GREY, INK, PAPER, NOTE, YEL = "#e4572e", "#c9ccd1", "#555", "#f4f6f8", "#fffdf5", "#f6c445"
BLUE, GREEN = "#7da2c8", "#8fb58f"
LIGHT = "#e9ecef"


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), bbox_inches="tight", pad_inches=0.25)
    plt.close(fig)


def canvas(w, h, xmax, ymax):
    fig, ax = plt.subplots(figsize=(w, h))
    ax.set_xlim(0, xmax); ax.set_ylim(0, ymax); ax.axis("off")
    return fig, ax


def box(ax, x, y, w, h, fc="white", ec=INK, lw=1.8):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.08", fc=fc, ec=ec, lw=lw))


def arrow(ax, a, b, color=INK, lw=2, rad=0.0, ms=18):
    ax.add_patch(FancyArrowPatch(a, b, arrowstyle="-|>", mutation_scale=ms, color=color, lw=lw,
                                 connectionstyle=f"arc3,rad={rad}"))


def kid(ax, cx, y, s=1.0):
    ax.add_patch(Circle((cx, y + 1.55 * s), 0.32 * s, fc="white", ec=INK, lw=1.6))
    ax.add_patch(Circle((cx - 0.11 * s, y + 1.6 * s), 0.035 * s, fc=INK))
    ax.add_patch(Circle((cx + 0.11 * s, y + 1.6 * s), 0.035 * s, fc=INK))
    ax.add_patch(Arc((cx, y + 1.5 * s), 0.3 * s, 0.2 * s, theta1=200, theta2=340, color=INK, lw=1.4))
    ax.plot([cx, cx], [y + 1.23 * s, y + 0.55 * s], color=INK, lw=2)
    ax.plot([cx, cx - 0.3 * s], [y + 0.55 * s, y], color=INK, lw=2)
    ax.plot([cx, cx + 0.3 * s], [y + 0.55 * s, y], color=INK, lw=2)
    ax.plot([cx - 0.35 * s, cx + 0.35 * s], [y + 1.0 * s, y + 1.0 * s], color=INK, lw=2)


def card(ax, x, y, w, h, num, hot=False, gone=False, fs=12):
    fc = LIGHT if gone else ("#fbe3dc" if hot else NOTE)
    ax.add_patch(Rectangle((x, y), w, h, fc=fc, ec=RED if hot else (GREY if gone else INK), lw=2.2 if hot else 1.2))
    ax.text(x + w / 2, y + h / 2, str(num), ha="center", va="center", fontsize=fs,
            color=RED if hot else (GREY if gone else "#222"), fontweight="bold")


def stones(ax, x, y, n, color=INK, r=0.13, gap=0.34):
    for k in range(n):
        ax.add_patch(Circle((x + k * gap, y), r, fc=color, ec=color))


def row(ax, x, y, nums, cw=0.9, ch=1.1, gap=0.1, hot=(), fs=12, gone=()):
    for k, n in enumerate(nums):
        card(ax, x + k * (cw + gap), y, cw, ch, n, hot=(k in hot), gone=(k in gone), fs=fs)
    return x + len(nums) * (cw + gap) - gap

import math
from matplotlib.patches import Ellipse, Polygon

SKIN = "#f6d8c4"
CELL = "#fbe3dc"
BLOOD = "#c0392b"
PLASMA = "#f3dc8c"
BACK = "#7da2c8"


def house(ax, x, y, s=1.0):
    ax.add_patch(Rectangle((x, y), 1.2 * s, 1.0 * s, fc=CELL, ec=RED, lw=1.4))
    ax.add_patch(Polygon([(x - 0.1 * s, y + 1.0 * s), (x + 0.6 * s, y + 1.6 * s), (x + 1.3 * s, y + 1.0 * s)],
                         closed=True, fc="white", ec=RED, lw=1.4))
    ax.add_patch(Rectangle((x + 0.45 * s, y), 0.3 * s, 0.5 * s, fc="white", ec=INK, lw=1))


def truck(ax, x, y, s=1.0):
    ax.add_patch(Rectangle((x, y + 0.25 * s), 1.4 * s, 0.75 * s, fc=BLOOD, ec=INK, lw=1.2))
    ax.add_patch(Rectangle((x + 1.4 * s, y + 0.25 * s), 0.55 * s, 0.55 * s, fc="white", ec=INK, lw=1.2))
    for dx in (0.3, 1.6):
        ax.add_patch(Circle((x + dx * s, y + 0.2 * s), 0.18 * s, fc=INK, ec=INK))


# 1. 여는 장면: 집은 그 자리에, 트럭이 집 앞까지
fig, ax = canvas(11.0, 5.0, 18.0, 8.2)
ax.add_patch(FancyBboxPatch((1.0, 1.2), 16.0, 5.0, boxstyle="round,pad=0.4", fc="none", ec=GREY, lw=14))
for k, x in enumerate([2.6, 5.6, 8.6, 11.6, 14.6]):
    house(ax, x - 0.6, 3.0)
truck(ax, 4.0, 6.0)
ax.add_patch(Circle((4.5, 7.6), 0.2, fc="white", ec=RED, lw=1.4))
ax.add_patch(Rectangle((5.0, 7.4), 0.4, 0.4, fc=YEL, ec=INK, lw=1))
ax.text(7.2, 7.6, "산소와 영양을 싣고 집 앞까지", ha="left", va="center", fontsize=11, color=BLOOD,
        fontweight="bold")
ax.text(9.0, 2.2, "집(세포)은 그 자리에 붙어 있어요", ha="center", va="center", fontsize=11)
save(fig, "b04-town.svg")

# 2. 이 편의 지도
fig, ax = canvas(11.6, 2.9, 19.4, 4.6)
titles = ["피 속에 든 것", "나가는 길, 돌아오는 길", "실핏줄에서 주고받아요", "한 바퀴 돌아요"]
for i, t in enumerate(titles):
    x = 0.3 + i * 4.8
    box(ax, x, 0.4, 3.8, 3.6)
    ax.text(x + 1.9, 0.95, t, ha="center", va="center", fontsize=11, fontweight="bold")
    cx = x + 1.9
    if i == 0:
        ax.add_patch(Rectangle((cx - 0.35, 1.6), 0.7, 1.0, fc=BLOOD, ec=INK, lw=1))
        ax.add_patch(Rectangle((cx - 0.35, 2.6), 0.7, 0.9, fc=PLASMA, ec=INK, lw=1))
    elif i == 1:
        arrow(ax, (cx - 1.2, 2.9), (cx + 1.2, 2.9), color=BLOOD, lw=1.6, ms=10)
        arrow(ax, (cx + 1.2, 2.0), (cx - 1.2, 2.0), color=BACK, lw=1.6, ms=10)
    elif i == 2:
        ax.plot([x + 0.4, x + 3.4], [2.5, 2.5], color=BLOOD, lw=1)
        for k in range(4):
            ax.add_patch(Circle((x + 0.9 + k * 0.7, 3.1), 0.2, fc=CELL, ec=RED, lw=1))
            arrow(ax, (x + 0.9 + k * 0.7, 2.55), (x + 0.9 + k * 0.7, 2.85), color=RED, lw=1, ms=7)
    else:
        ax.add_patch(Circle((cx, 2.5), 0.8, fc="none", ec=BLOOD, lw=1.8))
        arrow(ax, (cx + 0.8, 2.45), (cx + 0.78, 2.3), color=BLOOD, lw=1.8, ms=10)
    if i < 3:
        arrow(ax, (x + 3.95, 2.2), (x + 4.65, 2.2))
save(fig, "b04-map.svg")

# 3. 피를 가만히 두면 나뉘어요
fig, ax = canvas(10.0, 5.0, 16.0, 8.0)
ax.add_patch(FancyBboxPatch((3.0, 1.0), 1.6, 5.6, boxstyle="round,pad=0.1", fc="white", ec=INK, lw=1.8))
ax.add_patch(Rectangle((3.05, 1.05), 1.5, 2.4, fc=BLOOD, ec="none"))
ax.add_patch(Rectangle((3.05, 3.45), 1.5, 0.12, fc="white", ec=GREY, lw=0.6))
ax.add_patch(Rectangle((3.05, 3.57), 1.5, 2.6, fc=PLASMA, ec="none"))
ax.text(5.2, 4.9, "노르스름한 물\n영양과 다 쓴 숨이 녹아 있어요", ha="left", va="center", fontsize=11)
ax.text(5.2, 3.5, "아주 얇은 흰 층: 몸을 지키는 세포와 피를 멈추는 조각", ha="left", va="center", fontsize=10)
ax.text(5.2, 2.1, "붉은 층: 산소를 나르는 세포", ha="left", va="center", fontsize=11, color=BLOOD,
        fontweight="bold")
ax.text(3.8, 0.3, "피를 굳지 않게 해서 기계로 빙빙 돌리면 이렇게 나뉘어요", ha="left", va="center", fontsize=10)
save(fig, "b04-tube.svg")

# 4. 나가는 길 → 실핏줄 → 돌아오는 길
fig, ax = canvas(11.0, 5.2, 18.0, 8.4)
box(ax, 0.3, 3.6, 2.2, 1.6, fc=NOTE)
ax.text(1.4, 4.4, "심장", ha="center", va="center", fontsize=13, fontweight="bold")
ends = [6.6, 5.4, 3.4, 2.2]
ax.plot([2.6, 4.6], [4.4, 4.4], color=BLOOD, lw=8, solid_capstyle="round")
for top, pair in ((True, ends[:2]), (False, ends[2:])):
    my = 6.0 if top else 2.8
    ax.plot([4.6, 5.8], [4.4, my], color=BLOOD, lw=5, solid_capstyle="round")
    for y in pair:
        ax.plot([5.8, 7.4], [my, y], color=BLOOD, lw=3, solid_capstyle="round")
        for k in (-0.22, 0, 0.22):
            xs = [7.4 + t * 0.06 for t in range(51)]
            ys = [y + k * math.sin(math.pi * t / 50) + 0.05 * math.sin(t * 0.8) for t in range(51)]
            ax.plot(xs, ys, color="#a05a8a", lw=0.9)
        ax.plot([10.4, 12.0], [y, my], color=BACK, lw=3, solid_capstyle="round")
    ax.plot([12.0, 13.2], [my, 4.4], color=BACK, lw=5, solid_capstyle="round")
ax.plot([13.2, 14.2, 14.2, 1.4, 1.4], [4.4, 4.4, 0.8, 0.8, 3.5], color=BACK, lw=8, solid_capstyle="round",
        solid_joinstyle="round")
arrow(ax, (1.4, 2.2), (1.4, 3.5), color=BACK, lw=2.4)
arrow(ax, (3.0, 4.95), (4.2, 4.95), color=BLOOD, lw=1.4, ms=10)
ax.text(3.8, 5.6, "나가는 길", ha="center", va="center", fontsize=12, color=BLOOD, fontweight="bold")
ax.text(8.9, 7.7, "실핏줄", ha="center", va="center", fontsize=13, color="#a05a8a", fontweight="bold")
ax.text(8.9, 7.1, "아주 가늘고 벽이 얇아요", ha="center", va="center", fontsize=10, color="#a05a8a")
ax.text(7.8, 0.2, "돌아오는 길", ha="center", va="center", fontsize=12, color=BACK, fontweight="bold")
ax.text(16.2, 4.4, "색은 길을\n나누려고\n칠했어요.\n피는 늘\n붉어요", ha="center", va="center", fontsize=10)
save(fig, "b04-roads.svg")

# 5. 실핏줄에서 주고받아요
fig, ax = canvas(11.0, 4.8, 18.0, 7.8)
ax.add_patch(Rectangle((1.0, 3.3), 16.0, 0.8, fc="#f7d6d0", ec=BLOOD, lw=1.4))
for k in range(16):
    ax.add_patch(Ellipse((1.6 + k * 0.95, 3.7), 0.5, 0.5, fc=BLOOD, ec=INK, lw=0.6))
arrow(ax, (17.1, 3.7), (17.9, 3.7), color=INK, lw=1.6, ms=12)
ax.text(11.0, 4.4, "얇은 벽", ha="center", va="center", fontsize=9, color=BLOOD)
ax.text(2.4, 2.8, "빨간 세포", ha="center", va="center", fontsize=10, color=BLOOD, fontweight="bold")
ax.text(9.0, 2.2, "빨간 세포가 한 줄로 겨우 지나갈 만큼 가늘어요", ha="center", va="center", fontsize=10)
for k, x in enumerate([3.2, 7.8, 12.4]):
    ax.add_patch(Circle((x + 0.8, 6.4), 1.0, fc=CELL, ec=RED, lw=1.6))
    ax.text(x + 0.8, 6.4, "세포", ha="center", va="center", fontsize=11)
    arrow(ax, (x + 0.2, 4.2), (x + 0.2, 5.5), color=RED, lw=1.6, ms=12)
    arrow(ax, (x + 1.4, 5.5), (x + 1.4, 4.2), color=BACK, lw=1.6, ms=12)
ax.text(2.4, 5.6, "산소, 영양", ha="center", va="center", fontsize=10, color=RED, fontweight="bold")
ax.text(15.6, 5.4, "다 쓴 숨,\n쓰레기", ha="center", va="center", fontsize=10, color=BACK, fontweight="bold")
ax.text(9.0, 1.4, "크기는 실제와 맞추지 않았어요", ha="center", va="center", fontsize=10)
save(fig, "b04-swap.svg")

# 6. 한 바퀴: 폐 고리 + 온몸 고리(작은창자와 세포는 나란히)
fig, ax = canvas(11.0, 6.0, 18.0, 9.8)
box(ax, 7.6, 4.2, 2.8, 1.6, fc=NOTE)
ax.text(9.0, 5.0, "심장", ha="center", va="center", fontsize=13, fontweight="bold")
box(ax, 0.4, 4.0, 3.6, 2.0, fc="white")
ax.text(2.2, 5.0, "폐\n산소를 싣고\n다 쓴 숨을 내려요", ha="center", va="center", fontsize=10, fontweight="bold")
arrow(ax, (7.5, 5.5), (4.1, 5.6), color=BACK, lw=2.4, rad=0.3)
arrow(ax, (4.1, 4.4), (7.5, 4.5), color=BLOOD, lw=2.4, rad=0.3)
box(ax, 13.4, 6.8, 4.2, 1.6, fc="white")
ax.text(15.5, 7.6, "작은창자\n영양을 실어요", ha="center", va="center", fontsize=10, fontweight="bold")
box(ax, 13.4, 1.6, 4.2, 1.6, fc=CELL)
ax.text(15.5, 2.4, "온몸의 세포\n산소와 영양을 내려요", ha="center", va="center", fontsize=10, fontweight="bold")
arrow(ax, (10.5, 5.3), (13.3, 7.4), color=BLOOD, lw=2.4, rad=0.2)
arrow(ax, (10.5, 4.7), (13.3, 2.6), color=BLOOD, lw=2.4, rad=-0.2)
arrow(ax, (14.2, 6.7), (10.3, 5.9), color=BACK, lw=2.0, rad=0.3)
arrow(ax, (14.2, 3.3), (10.3, 4.1), color=BACK, lw=2.0, rad=-0.3)
ax.text(9.0, 0.6, "빨강은 산소를 실은 피, 파랑은 산소를 내려 준 피예요. 피는 늘 붉어요. 실제 길은 훨씬 복잡해요", ha="center",
        va="center", fontsize=10)
save(fig, "b04-loop.svg")

# 7. 손등 핏줄: 내리면 불룩, 올리면 납작
fig, ax = canvas(10.0, 4.8, 16.0, 7.8)
for k, (x, up) in enumerate([(4.0, False), (12.0, True)]):
    ax.add_patch(FancyBboxPatch((x - 1.6, 1.6), 3.2, 3.6, boxstyle="round,pad=0.4", fc=SKIN, ec=INK, lw=1.6))
    lw = 1.5 if up else 4.5
    for dx in (-0.8, 0.0, 0.8):
        ax.plot([x + dx * 0.6, x + dx, x + dx * 1.2], [1.4, 3.2, 5.0], color=BACK, lw=lw, solid_capstyle="round")
    ax.text(x, 0.6, "손을 머리 위로 올리면\n핏줄이 납작해요" if up else "손을 아래로 내리면\n핏줄이 불룩해요",
            ha="center", va="center", fontsize=11, fontweight="bold")
    arrow(ax, (x + 2.6, 4.0 if not up else 2.6), (x + 2.6, 2.6 if not up else 4.0), color=INK, lw=1.8)
ax.text(8.0, 7.2, "손등에 보이는 핏줄은 돌아오는 길이에요", ha="center", va="center", fontsize=11)
save(fig, "b04-hand.svg")
