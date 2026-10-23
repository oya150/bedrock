"""물질과 에너지 7편 그림 만들기. 실행: python lab/fig_m07.py  → docs/matter/img/07/*.svg

글자는 SVG 안에 글자로 남긴다(글꼴 모양을 파일에 넣지 않는다). 보는 쪽 글꼴로 그려진다.
카드는 차분한 색으로, 강조(새로 받은 카드, 비교 화살표, 많이 든 일)만 빨강으로 칠한다.
"""
import itertools
import os

import matplotlib

matplotlib.use("svg")
import matplotlib.pyplot as plt
from matplotlib.patches import Arc, Circle, FancyArrowPatch, FancyBboxPatch, Rectangle

OUT = os.path.join(os.path.dirname(__file__), "..", "docs", "matter", "img", "07")
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
import random
from matplotlib.patches import Ellipse, Polygon

random.seed(2)
WATER = "#7da2c8"
ICE = "#dbeaf5"


def particle(ax, x, y, r=0.24, fc=WATER):
    ax.add_patch(Circle((x, y), r, fc=fc, ec=INK, lw=0.7))


def jig(ax, x, y, s=0.12):
    for a in (0, 180):
        r = math.radians(a)
        ax.plot([x + 0.28 * math.cos(r), x + (0.28 + s) * math.cos(r)], [y, y], color=INK, lw=0.7)


def solid(ax, x0, y0, rows=4, cols=5, gap=0.5):
    for i in range(rows):
        for j in range(cols):
            particle(ax, x0 + j * gap, y0 + i * gap)
            jig(ax, x0 + j * gap, y0 + i * gap)


def liquid(ax, x0, y0, w, h, n=None, gap=0.5):
    pts = []
    y = y0 + 0.3
    while y < y0 + h - 0.25:
        x = x0 + 0.3 + random.uniform(0, gap / 2)
        while x < x0 + w - 0.25:
            if random.random() > 0.06:
                pts.append((x + random.uniform(-0.07, 0.07), y + random.uniform(-0.07, 0.07)))
            x += gap * random.uniform(0.98, 1.1)
        y += gap * random.uniform(0.9, 1.0)
    for p in pts:
        particle(ax, *p)
    for p in pts[::5]:
        arrow(ax, p, (p[0] + random.uniform(-0.4, 0.4), p[1] + random.uniform(-0.25, 0.25)), color=INK, lw=0.8, ms=6)


def gas(ax, x0, y0, w, h, n=6):
    pts = []
    for _ in range(5000):
        if len(pts) >= n:
            break
        p = (x0 + random.uniform(0.4, w - 1.0), y0 + random.uniform(0.4, h - 1.0))
        if all((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2 > 1.4 ** 2 for q in pts):
            pts.append(p)
    for p in pts:
        particle(ax, *p)
        a = random.uniform(0, 2 * math.pi)
        arrow(ax, p, (p[0] + 0.8 * math.cos(a), p[1] + 0.8 * math.sin(a)), color=RED, lw=1.0, ms=8)


def mover(ax, x, y, strength, r=0.24, fc=WATER, color=None):
    """알갱이 하나와 꿈틀거림 세기만큼의 화살표."""
    particle(ax, x, y, r=r, fc=fc)
    a = random.uniform(0, 2 * math.pi)
    L = r + strength
    arrow(ax, (x + (r + 0.02) * math.cos(a), y + (r + 0.02) * math.sin(a)), (x + L * math.cos(a), y + L * math.sin(a)),
          color=color or (RED if strength > 0.5 else INK), lw=1.2 if strength > 0.5 else 0.9, ms=8)


def cup(ax, x, y, w, h, fc="#eef5fb"):
    ax.add_patch(Polygon([(x, y + h), (x + w, y + h), (x + w - 0.3, y), (x + 0.3, y)], closed=True, fc=fc, ec=INK,
                         lw=1.6))


def hand(ax, x, y, s=1.0):
    ax.add_patch(FancyBboxPatch((x, y), 2.6 * s, 2.0 * s, boxstyle="round,pad=0.25", fc="#f6d8c4", ec=INK, lw=1.4))
    for k in range(4):
        ax.add_patch(FancyBboxPatch((x + 0.1 * s + k * 0.65 * s, y + 2.05 * s), 0.42 * s, 0.9 * s,
                                    boxstyle="round,pad=0.12", fc="#f6d8c4", ec=INK, lw=1.2))


CARBON, OXY, HYD = "#2f2f33", "#9aa3ad", "#f4f6f8"
WAX, WOOD, APPLE, RUST = "#fbf3dc", "#c8a27a", "#fbf3dc", "#b5532a"


def flame(ax, x, y, s=1.0):
    ax.add_patch(Ellipse((x, y + 0.55 * s), 0.55 * s, 1.1 * s, fc=YEL, ec=RED, lw=1.2))
    ax.add_patch(Ellipse((x, y + 0.4 * s), 0.25 * s, 0.5 * s, fc="white", ec="none"))


def candle(ax, x, y, h, s=1.0):
    ax.add_patch(Rectangle((x - 0.25 * s, y), 0.5 * s, h, fc=WAX, ec=INK, lw=1.2))
    ax.plot([x, x], [y + h, y + h + 0.2 * s], color=INK, lw=1.2)


def block(ax, x, y, fc, w=0.6):
    ax.add_patch(Rectangle((x, y), w, w, fc=fc, ec=INK, lw=1.2))
    ax.add_patch(Circle((x + w / 2, y + w + 0.05), 0.1, fc=fc, ec=INK, lw=0.8))


def waves(ax, x, y, ang, L=1.0, color=RED):
    xs = [x + t * L / 12 * math.cos(ang) - 0.08 * math.sin(t * 1.3) * math.sin(ang) for t in range(13)]
    ys = [y + t * L / 12 * math.sin(ang) + 0.08 * math.sin(t * 1.3) * math.cos(ang) for t in range(13)]
    ax.plot(xs, ys, color=color, lw=1.4)


# 1. 여는 장면: 촛불
fig, ax = canvas(9.0, 4.2, 15.0, 7.0)
for cx, h, lab in [(3.5, 2.2, "처음"), (10.5, 0.9, "한참 뒤")]:
    ax.add_patch(FancyBboxPatch((cx - 2.0, 0.6), 4.0, 1.2, boxstyle="round,pad=0.1", fc="#f6d8c4", ec=INK, lw=1.2))
    candle(ax, cx, 1.9, h)
    flame(ax, cx, 1.9 + h + 0.2)
    ax.text(cx, 0.2, lab, ha="center", va="center", fontsize=10)
arrow(ax, (6.0, 2.6), (8.0, 2.6))
ax.text(7.0, 6.5, "줄어든 초는 어디로 갔을까?", ha="center", va="center", fontsize=12, color=RED, fontweight="bold")
save(fig, "m07-candle.svg")

# 2. 이 편의 지도
fig, ax = canvas(11.6, 2.9, 19.4, 4.6)
titles = ["원자가 짝을 바꿔요", "불에 필요한 셋", "열과 빛이 나와요", "불 없이도 바뀌어요"]
for i, t in enumerate(titles):
    x = 0.3 + i * 4.8
    box(ax, x, 0.4, 3.8, 3.6)
    ax.text(x + 1.9, 0.95, t, ha="center", va="center", fontsize=10.5, fontweight="bold")
    cx = x + 1.9
    if i == 0:
        for k, c in enumerate([CARBON, OXY, OXY]):
            block(ax, cx - 1.65 + k * 0.35, 2.0, c, 0.35)
        arrow(ax, (cx - 0.5, 2.2), (cx + 0.1, 2.2), lw=1.2, ms=10)
        for k, c in enumerate([OXY, CARBON, OXY]):
            block(ax, cx + 0.3 + k * 0.35, 2.0, c, 0.35)
    elif i == 1:
        ax.add_patch(Rectangle((cx - 1.5, 1.8), 0.8, 0.35, fc=WOOD, ec=INK, lw=1))
        ax.text(cx + 0.05, 1.98, "산소", ha="center", va="center", fontsize=8.5)
        waves(ax, cx + 0.6, 1.8, math.pi / 2, 0.8)
        flame(ax, cx, 2.6, 0.7)
    elif i == 2:
        flame(ax, cx, 1.8, 0.9)
        for k in range(6):
            a = math.radians(30 * k - 60) if k < 3 else math.radians(30 * k + 30)
            waves(ax, cx + 0.5 * math.cos(a), 2.3 + 0.5 * math.sin(a), a, 0.6)
    else:
        ax.add_patch(Ellipse((cx, 2.3), 1.6, 1.0, fc=APPLE, ec=INK, lw=1))
        ax.add_patch(Ellipse((cx, 2.3), 1.2, 0.7, fc="#c69a5b", ec="none", alpha=0.7))
    if i < 3:
        arrow(ax, (x + 3.95, 2.2), (x + 4.65, 2.2))
save(fig, "m07-map.svg")

# 3. 블록 수는 그대로, 모양은 달라요
fig, ax = canvas(10.0, 3.8, 16.0, 6.2)
for (x, c) in [(1.0, HYD), (1.6, CARBON), (2.2, HYD)]:
    block(ax, x, 3.6, c)
ax.text(3.2, 3.9, "초 조각", ha="left", va="center", fontsize=10)
for x in (1.0, 1.9, 2.8):
    block(ax, x, 1.8, OXY)
ax.text(3.7, 2.1, "산소", ha="left", va="center", fontsize=10)
arrow(ax, (5.0, 3.0), (7.4, 3.0))
ax.text(6.2, 3.5, "다시 이어지면", ha="center", va="center", fontsize=9)
for (x, c) in [(9.0, OXY), (9.6, CARBON), (10.2, OXY)]:
    block(ax, x, 3.6, c)
for (x, c) in [(9.0, HYD), (9.6, OXY), (10.2, HYD)]:
    block(ax, x, 1.8, c)
ax.text(8.0, 0.7, "블록 수는 그대로, 모양은 달라요", ha="center", va="center", fontsize=11, color=RED, fontweight="bold")
save(fig, "m07-blocks.svg")

# 4. 불에 필요한 셋
fig, ax = canvas(9.0, 4.6, 15.0, 7.6)
flame(ax, 7.5, 3.0, 1.6)
ax.add_patch(Rectangle((1.0, 5.0), 2.4, 0.7, fc=WOOD, ec=INK, lw=1.2))
ax.text(2.2, 4.5, "탈 것", ha="center", va="center", fontsize=11, fontweight="bold")
for (dx, dy) in [(0, 0), (0.6, 0.3), (0.3, -0.4)]:
    particle(ax, 12.2 + dx, 5.4 + dy, r=0.18, fc=OXY)
ax.text(12.6, 4.5, "산소", ha="center", va="center", fontsize=11, fontweight="bold")
for k in range(3):
    waves(ax, 6.6 + k * 0.6, 0.6, math.pi / 2, 1.2)
ax.text(7.5, 0.2, "처음의 열", ha="center", va="center", fontsize=11, fontweight="bold")
arrow(ax, (3.6, 5.2), (6.6, 4.4), color=INK, lw=1.4)
arrow(ax, (11.6, 5.2), (8.4, 4.4), color=INK, lw=1.4)
ax.text(10.6, 2.6, "셋이 다 있어야\n불이 붙어요", ha="left", va="center", fontsize=11, color=RED, fontweight="bold")
save(fig, "m07-three.svg")

# 5. 열과 빛 (heat)
fig, ax = canvas(9.0, 4.6, 15.0, 7.6)
candle(ax, 5.0, 0.6, 2.4, 1.4)
flame(ax, 5.0, 3.1, 2.0)
for k, a in enumerate([20, 50, 130, 160, 80, 100]):
    r = math.radians(a)
    waves(ax, 5.0 + 1.1 * math.cos(r), 4.2 + 1.1 * math.sin(r), r, 1.2)
ax.add_patch(FancyArrowPatch((6.4, 3.6), (5.6, 2.9), arrowstyle="-|>", mutation_scale=14, color=RED, lw=1.6,
                             connectionstyle="arc3,rad=-0.5"))
ax.text(7.4, 6.4, "아주 뜨거워서 빛나요", ha="left", va="center", fontsize=11, color=RED, fontweight="bold")
ax.text(7.6, 4.6, "열이 나와요", ha="left", va="center", fontsize=11, color=RED, fontweight="bold")
ax.text(7.0, 2.6, "그 열이 곁의 초를\n뜨겁게 해요", ha="left", va="center", fontsize=10.5)
save(fig, "m07-heat.svg")

# 5b. 초는 기체가 되어 날아가요
fig, ax = canvas(9.0, 5.0, 15.0, 8.4)
ax.add_patch(Rectangle((2.6, 0.6), 2.8, 3.0, fc=WAX, ec=INK, lw=1.4))
ax.add_patch(Ellipse((4.0, 3.6), 2.4, 0.5, fc="#f3e3b5", ec=INK, lw=1))
ax.plot([4.0, 4.0], [3.6, 4.4], color=INK, lw=2)
for k in range(4):
    arrow(ax, (3.9, 3.5 + k * 0.2), (3.9, 3.7 + k * 0.2), color=INK, lw=0.8, ms=6)
flame(ax, 4.0, 4.3, 2.4)
for (x0, y0, cols) in [(3.2, 6.9, [OXY, CARBON, OXY]), (4.4, 7.6, [HYD, OXY, HYD])]:
    for k, c in enumerate(cols):
        block(ax, x0 + k * 0.32, y0, c, 0.3)
    arrow(ax, (x0 + 0.5, y0 + 0.45), (x0 + 0.8, y0 + 0.8), color=RED, lw=1.2, ms=9)
ax.annotate("녹은 초가 심지를 타고\n올라가 타요", (4.1, 3.9), (6.6, 3.0), fontsize=10.5,
            arrowprops=dict(arrowstyle="-", color=INK, lw=1))
ax.text(6.6, 7.4, "눈에 안 보이는 기체가\n되어 날아가요", ha="left", va="center", fontsize=10.5, color=RED, fontweight="bold")
save(fig, "m07-flame.svg")

# 6. 불 없이도
fig, ax = canvas(10.0, 4.2, 16.0, 6.8)
ax.add_patch(Ellipse((2.0, 5.0), 2.2, 1.3, fc=APPLE, ec=INK, lw=1.2))
arrow(ax, (3.6, 5.0), (5.4, 5.0))
ax.add_patch(Ellipse((7.0, 5.0), 2.2, 1.3, fc="#c69a5b", ec=INK, lw=1.2))
ax.text(8.8, 5.0, "사과 조각이 공기를 만나면", ha="left", va="center", fontsize=11)
for x0, fc in [(1.0, "#c9ccd1"), (6.0, RUST)]:
    ax.add_patch(Rectangle((x0, 1.6), 2.4, 0.3, fc=fc, ec=INK, lw=1.2))
    ax.add_patch(Rectangle((x0 - 0.2, 1.4), 0.25, 0.7, fc=fc, ec=INK, lw=1.2))
arrow(ax, (3.6, 1.75), (5.4, 1.75))
for k in range(8):
    ax.add_patch(Circle((6.2 + random.uniform(0, 2.2), 1.75 + random.uniform(-0.12, 0.12)), 0.05, fc="#7a3518", ec="none"))
ax.text(8.8, 1.75, "쇠가 물과 공기를 만나면", ha="left", va="center", fontsize=11)
save(fig, "m07-slow.svg")
