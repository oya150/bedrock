"""인체 7편 그림 만들기. 실행: python lab/fig_b07.py  → docs/body/img/07/*.svg

글자는 SVG 안에 글자로 남긴다(글꼴 모양을 파일에 넣지 않는다). 보는 쪽 글꼴로 그려진다.
카드는 차분한 색으로, 강조(새로 받은 카드, 비교 화살표, 많이 든 일)만 빨강으로 칠한다.
"""
import itertools
import os

import matplotlib

matplotlib.use("svg")
import matplotlib.pyplot as plt
from matplotlib.patches import Arc, Circle, FancyArrowPatch, FancyBboxPatch, Rectangle

OUT = os.path.join(os.path.dirname(__file__), "..", "docs", "body", "img", "07")
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

CELL = "#fbe3dc"
SKIN = "#f6d8c4"
BLOOD = "#c0392b"
WATER = "#7da2c8"
HEAT = "#e4572e"
COOL = "#7da2c8"


def wavy(ax, x, y, h=1.0, color=HEAT, lw=1.6):
    ys = [y + h * t / 30 for t in range(31)]
    xs = [x + 0.12 * math.sin(t * 0.6) for t in range(31)]
    ax.plot(xs, ys, color=color, lw=lw)


def thermo(ax, x, y, level, h=3.0):
    ax.add_patch(FancyBboxPatch((x - 0.18, y), 0.36, h, boxstyle="round,pad=0.05", fc="white", ec=INK, lw=1.4))
    ax.add_patch(Circle((x, y), 0.36, fc=RED, ec=INK, lw=1.4))
    ax.add_patch(Rectangle((x - 0.1, y), 0.2, h * level, fc=RED, ec="none"))


# 1. 여는 장면: 뛰고 난 뒤 이마에 땀
fig, ax = canvas(10.0, 4.6, 16.0, 7.4)
kid(ax, 4.0, 0.8, 3.0)
for dx, dy in ((-0.5, 5.9), (0.45, 6.1), (0.05, 6.35)):
    ax.add_patch(Ellipse((4.0 + dx, dy), 0.18, 0.3, fc=WATER, ec=INK, lw=0.8))
for k in range(3):
    wavy(ax, 6.2 + k * 0.5, 3.0, 1.6)
ax.text(8.6, 5.4, "운동장을 뛰고 나면\n이마에 땀이 송골송골", ha="left", va="center", fontsize=12)
ax.text(12.4, 2.2, "땀은 왜 날까?", ha="center", va="center", fontsize=13, color=RED, fontweight="bold")
save(fig, "b07-run.svg")

# 2. 이 편의 지도
fig, ax = canvas(11.6, 2.9, 19.4, 4.6)
titles = ["몸에서 열이 나요", "늘 비슷한 온도", "땀이 마르며 식혀요", "땀구멍과 모공"]
for i, t in enumerate(titles):
    x = 0.3 + i * 4.8
    box(ax, x, 0.4, 3.8, 3.6)
    ax.text(x + 1.9, 0.95, t, ha="center", va="center", fontsize=11, fontweight="bold")
    cx = x + 1.9
    if i == 0:
        ax.add_patch(Circle((cx, 2.4), 0.5, fc=CELL, ec=RED, lw=1.4))
        for k in range(3):
            wavy(ax, cx - 0.5 + k * 0.5, 3.0, 0.7, lw=1.2)
    elif i == 1:
        thermo(ax, cx, 1.9, 0.6, h=1.6)
    elif i == 2:
        ax.add_patch(Ellipse((cx, 2.2), 0.4, 0.6, fc=WATER, ec=INK, lw=1))
        for k in range(3):
            wavy(ax, cx - 0.4 + k * 0.4, 2.7, 0.7, color=HEAT, lw=1.2)
    else:
        ax.add_patch(Rectangle((x + 0.4, 1.6), 3.0, 0.9, fc=SKIN, ec=INK, lw=1))
        ax.plot([cx - 0.6, cx - 0.4], [2.5, 3.4], color=INK, lw=1.4)
        ax.add_patch(Circle((cx + 0.6, 2.5), 0.08, fc=WATER, ec=INK, lw=0.6))
    if i < 3:
        arrow(ax, (x + 3.95, 2.2), (x + 4.65, 2.2))
save(fig, "b07-map.svg")

# 3. 세포가 일하면 열이 나요
fig, ax = canvas(10.0, 4.4, 16.0, 7.2)
for k, (x, busy, lab) in enumerate([(3.6, False, "가만히 있을 때"), (11.6, True, "뛸 때")]):
    for j in range(3):
        ax.add_patch(Ellipse((x - 1.2 + j * 1.2, 3.0), 1.0, 2.2, fc=CELL, ec=RED, lw=1.4))
    n = 6 if busy else 2
    for j in range(n):
        wavy(ax, x - 1.5 + j * (3.0 / max(n - 1, 1)), 4.3, 1.4 if busy else 0.8)
    ax.text(x, 0.9, lab, ha="center", va="center", fontsize=11, fontweight="bold")
ax.plot([7.6, 7.6], [0.4, 6.6], color=GREY, lw=1.2, ls="--")
ax.text(8.0, 6.8, "근육 세포가 일을 많이 하면 열도 많이 나요", ha="center", va="center", fontsize=11, color=RED,
        fontweight="bold")
save(fig, "b07-heat.svg")

# 4. 늘 비슷한 온도: 더우면 식히고, 추우면 데우고
fig, ax = canvas(11.0, 5.0, 18.0, 8.2)
thermo(ax, 9.0, 2.0, 0.55, h=4.0)
ax.text(9.0, 1.0, "37도쯤", ha="center", va="center", fontsize=13, fontweight="bold")
ax.text(9.0, 7.6, "뇌의 온도 지킴이가 살펴요", ha="center", va="center", fontsize=11)
box(ax, 0.6, 3.2, 6.4, 3.2, fc="#fdecea")
ax.text(3.8, 5.8, "너무 더워지면", ha="center", va="center", fontsize=12, color=RED, fontweight="bold")
ax.text(3.8, 4.6, "피부 핏줄을 넓혀 열을 보내요\n땀을 내요", ha="center", va="center", fontsize=11)
box(ax, 11.0, 3.2, 6.4, 3.2, fc="#eaf1f8")
ax.text(14.2, 5.8, "너무 추워지면", ha="center", va="center", fontsize=12, color=WATER, fontweight="bold")
ax.text(14.2, 4.6, "피부 핏줄을 좁혀 열을 지켜요\n몸이 떨려 열을 만들어요", ha="center", va="center", fontsize=11)
ax.plot([1.6, 6.0], [3.7, 3.7], color=BLOOD, lw=9, solid_capstyle="round")
ax.plot([12.0, 16.4], [3.7, 3.7], color=BLOOD, lw=2.5, solid_capstyle="round")
arrow(ax, (7.1, 4.8), (8.5, 4.6), color=RED, lw=1.8)
arrow(ax, (10.9, 4.8), (9.5, 4.6), color=WATER, lw=1.8)
save(fig, "b07-keep.svg")

# 5. 땀이 마르며 열을 가져가요
fig, ax = canvas(11.0, 4.6, 18.0, 7.4)
ax.add_patch(Rectangle((1.0, 1.0), 16.0, 1.6, fc=SKIN, ec=INK, lw=1.4))
ax.text(9.0, 1.6, "피부", ha="center", va="center", fontsize=11)
for k, x in enumerate([3.0, 7.0, 11.0, 15.0]):
    ax.add_patch(Ellipse((x, 2.9), 0.7, 0.55, fc=WATER, ec=INK, lw=1, alpha=1.0 - k * 0.22))
for k, x in enumerate([7.0, 11.0, 15.0]):
    for j in range(2):
        wavy(ax, x - 0.3 + j * 0.6, 3.5, 1.4, color=HEAT, lw=1.4)
    arrow(ax, (x, 5.0), (x, 6.2), color=HEAT, lw=1.6, ms=12)
ax.text(3.0, 4.0, "땀방울", ha="center", va="center", fontsize=11, color=WATER, fontweight="bold")
ax.text(11.0, 6.8, "땀이 마르면서 피부의 열을 데리고 날아가요", ha="center", va="center", fontsize=11, color=RED,
        fontweight="bold")
arrow(ax, (2.0, 0.5), (16.0, 0.5), color=INK, lw=1.2, ms=10)
ax.text(9.0, 0.1, "시간이 지나며 땀이 말라요", ha="center", va="center", fontsize=10)
ax.set_ylim(-0.4, 7.4)
save(fig, "b07-dry.svg")

# 6. 모공과 땀구멍: 피부 단면
fig, ax = canvas(11.0, 5.2, 18.0, 8.6)
ax.add_patch(Rectangle((1.0, 1.0), 16.0, 5.0, fc=SKIN, ec=INK, lw=1.4))
ax.add_patch(Rectangle((1.0, 5.2), 16.0, 0.8, fc="#f2c9b0", ec="none"))
# 털과 모공
ax.add_patch(Polygon([(4.6, 6.0), (5.4, 6.0), (5.3, 2.6), (4.7, 2.6)], closed=True, fc="#f2c9b0", ec=INK, lw=1.2))
ax.plot([5.0, 5.0, 5.8], [2.8, 6.0, 7.8], color=INK, lw=2.4)
ax.add_patch(Ellipse((6.0, 3.8), 1.0, 0.8, fc=YEL, ec=INK, lw=1))
arrow(ax, (5.55, 3.9), (5.25, 4.4), color=INK, lw=1.2, ms=9)
ax.text(6.7, 3.8, "기름이 나오는 곳", ha="left", va="center", fontsize=10)
ax.text(5.0, 0.4, "모공(털구멍): 털과 기름", ha="center", va="center", fontsize=11, fontweight="bold")
# 땀샘과 땀구멍
xs = [12.0 + 0.3 * math.sin(t * 0.9) for t in range(20)]
ys = [2.2 + 3.8 * t / 19 for t in range(20)]
ax.plot(xs, ys, color=WATER, lw=2)
ax.add_patch(Circle((12.0, 2.0), 0.6, fc="#dbe7f3", ec=WATER, lw=1.6))
ax.text(12.8, 2.0, "땀을 만드는 곳", ha="left", va="center", fontsize=10)
ax.add_patch(Ellipse((xs[-1], 6.3), 0.3, 0.4, fc=WATER, ec=INK, lw=0.6))
ax.text(xs[-1] + 0.5, 6.6, "땀구멍", ha="left", va="center", fontsize=10, color=WATER, fontweight="bold")
arrow(ax, (xs[-1] + 0.45, 6.55), (xs[-1] + 0.1, 6.05), color=WATER, lw=1.0, ms=8)
ax.text(12.6, 0.4, "땀구멍: 땀이 나오는 작은 구멍", ha="center", va="center", fontsize=11, color=WATER, fontweight="bold")
ax.text(9.0, 8.3, "피부를 잘라 옆에서 본 모습 (크기는 실제와 맞추지 않았어요)", ha="center", va="center", fontsize=10)
ax.set_ylim(-0.2, 8.6)
save(fig, "b07-pores.svg")
