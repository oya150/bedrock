"""물질과 에너지 2편 그림 만들기. 실행: python lab/fig_m02.py  → docs/matter/img/02/*.svg

글자는 SVG 안에 글자로 남긴다(글꼴 모양을 파일에 넣지 않는다). 보는 쪽 글꼴로 그려진다.
카드는 차분한 색으로, 강조(새로 받은 카드, 비교 화살표, 많이 든 일)만 빨강으로 칠한다.
"""
import itertools
import os

import matplotlib

matplotlib.use("svg")
import matplotlib.pyplot as plt
from matplotlib.patches import Arc, Circle, FancyArrowPatch, FancyBboxPatch, Rectangle

OUT = os.path.join(os.path.dirname(__file__), "..", "docs", "matter", "img", "02")
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


# 1. 여는 장면: 얼음 → 물 → 김
fig, ax = canvas(11.0, 4.2, 18.0, 7.0)
ax.add_patch(Polygon([(1.0, 2.0), (2.8, 2.0), (3.2, 3.6), (1.4, 3.6)], closed=True, fc=ICE, ec=INK, lw=1.4))
ax.text(2.1, 1.2, "얼음", ha="center", va="center", fontsize=12, fontweight="bold")
arrow(ax, (3.8, 2.8), (5.6, 2.8))
ax.add_patch(Polygon([(6.4, 1.6), (9.4, 1.6), (9.8, 4.4), (6.0, 4.4)], closed=True, fc="white", ec=INK, lw=1.4))
ax.add_patch(Polygon([(6.5, 1.65), (9.3, 1.65), (9.55, 3.2), (6.25, 3.2)], closed=True, fc="#cfe3f3", ec="none"))
ax.text(7.9, 1.0, "물", ha="center", va="center", fontsize=12, fontweight="bold")
arrow(ax, (10.4, 2.8), (12.2, 2.8))
ax.add_patch(Rectangle((12.8, 1.4), 3.6, 1.6, fc=GREY, ec=INK, lw=1.4))
ax.text(14.6, 2.2, "냄비", ha="center", va="center", fontsize=10)
for k in range(3):
    ax.add_patch(FancyArrowPatch((13.6 + k * 1.0, 3.3), (13.6 + k * 1.0, 5.0), arrowstyle="-|>", mutation_scale=12,
                                 color=WATER, lw=1.4, ls="--"))
ax.text(14.6, 0.8, "수증기", ha="center", va="center", fontsize=12, fontweight="bold")
ax.text(14.6, 5.5, "눈에 안 보여요", ha="center", va="center", fontsize=9)
ax.text(9.0, 6.4, "셋 다 물인데 왜 모양이 다를까?", ha="center", va="center", fontsize=12, color=RED, fontweight="bold")
save(fig, "m02-three.svg")

# 2. 이 편의 지도
fig, ax = canvas(12.6, 2.4, 24.2, 4.6)
titles = ["모두 물 알갱이", "얼음: 꼭 붙어서", "물: 스치며 지나가요", "수증기: 흩어져서", "식으면 다시 모여요"]
for i, t in enumerate(titles):
    x = 0.3 + i * 4.8
    box(ax, x, 0.4, 3.8, 3.6)
    ax.text(x + 1.9, 0.95, t, ha="center", va="center", fontsize=11, fontweight="bold")
    cx = x + 1.9
    if i == 0:
        particle(ax, cx, 2.6, r=0.4)
    elif i == 1:
        for a in range(3):
            for b in range(3):
                particle(ax, cx - 0.4 + b * 0.4, 2.2 + a * 0.4, r=0.17)
    elif i == 2:
        for (dx, dy) in [(-0.36, 0.0), (0.0, -0.1), (0.36, 0.05), (-0.18, 0.32), (0.2, 0.33), (-0.3, -0.34), (0.22, -0.4)]:
            particle(ax, cx + dx, 2.6 + dy, r=0.17)
    elif i == 3:
        for (dx, dy) in [(-1.0, 0.5), (0.8, 0.7), (-0.2, -0.3), (1.1, -0.4)]:
            particle(ax, cx + dx, 2.6 + dy, r=0.17)
    else:
        arrow(ax, (cx - 1.2, 2.6), (cx + 0.1, 2.6), color=WATER, lw=2)
        ax.add_patch(Ellipse((cx + 0.6, 2.6), 0.5, 0.7, fc=WATER, ec=INK, lw=0.8))
    if i < 4:
        arrow(ax, (x + 3.95, 2.2), (x + 4.65, 2.2))
save(fig, "m02-map.svg")

# 3. 세 모습 나란히 (알갱이 그림)
fig, ax = canvas(11.0, 4.6, 18.0, 7.6)
box(ax, 0.4, 1.4, 5.2, 5.0, fc=ICE)
solid(ax, 1.1, 2.2, rows=7, cols=8, gap=0.5)
ax.text(3.0, 0.8, "얼음: 꼭 붙어 제자리에서 떨어요", ha="center", va="center", fontsize=10, fontweight="bold")
box(ax, 6.4, 1.4, 5.2, 5.0, fc="#eef5fb")
liquid(ax, 6.5, 1.5, 5.0, 4.8, n=75)
ax.text(9.0, 0.8, "물: 붙은 채 스치며 지나가요", ha="center", va="center", fontsize=10, fontweight="bold")
box(ax, 12.4, 1.4, 5.2, 5.0, fc="white")
gas(ax, 12.5, 1.5, 5.0, 4.8, n=7)
ax.text(15.0, 0.8, "수증기: 멀리 떨어져 날아다녀요", ha="center", va="center", fontsize=10, fontweight="bold")
ax.text(9.0, 7.2, "모두 같은 물 알갱이예요 (크기와 거리는 실제와 맞추지 않았어요)", ha="center", va="center",
        fontsize=10)
save(fig, "m02-particles.svg")

# 4. 운동장 비유
fig, ax = canvas(11.0, 4.0, 18.0, 6.6)
for k, (x, mode, lab) in enumerate([(3.0, 0, "줄 서서 제자리 콩콩"), (9.0, 1, "붐비는 복도에서 스치며 지나가요"), (15.0, 2, "흩어져 뛰어다녀요")]):
    box(ax, x - 2.6, 1.3, 5.2, 4.6, fc=NOTE)
    if mode == 0:
        for i in range(2):
            for j in range(3):
                kid(ax, x - 1.4 + j * 1.4, 1.8 + i * 1.9, 0.75)
    elif mode == 1:
        for j, (dx, dy, d) in enumerate([(-1.5, 1.8, 1), (-0.5, 1.9, -1), (0.5, 1.8, 1), (1.5, 1.9, -1),
                                          (-0.9, 3.5, -1), (0.4, 3.6, 1)]):
            kid(ax, x + dx, dy, 0.7)
            arrow(ax, (x + dx + 0.1 * d, dy + 1.0), (x + dx + 0.6 * d, dy + 1.0), color=RED, lw=1.2, ms=9)
    else:
        for (dx, dy) in [(-1.8, 2.8), (1.4, 3.6), (-0.4, 1.6), (1.8, 1.7)]:
            kid(ax, x + dx, dy, 0.7)
    ax.text(x, 0.7, lab, ha="center", va="center", fontsize=11, fontweight="bold")
ax.text(9.0, 6.3, "얼음, 물, 수증기의 알갱이는 이런 아이들과 닮았어요", ha="center", va="center", fontsize=11, color=RED,
        fontweight="bold")
save(fig, "m02-playground.svg")

# 5. 데우면 풀려나고 식히면 붙어요
fig, ax = canvas(11.0, 3.8, 18.0, 6.2)
box(ax, 0.4, 1.2, 4.6, 3.8, fc=ICE)
solid(ax, 1.1, 1.8, rows=5, cols=7, gap=0.5)
box(ax, 6.7, 1.2, 4.6, 3.8, fc="#eef5fb")
liquid(ax, 6.8, 1.3, 4.4, 3.6, n=50)
box(ax, 13.0, 1.2, 4.6, 3.8, fc="white")
gas(ax, 13.1, 1.3, 4.4, 3.6, n=6)
arrow(ax, (5.1, 3.6), (6.6, 3.6), color=RED, lw=2.2)
arrow(ax, (11.4, 3.6), (12.9, 3.6), color=RED, lw=2.2)
arrow(ax, (6.6, 2.4), (5.1, 2.4), color=WATER, lw=2.2)
arrow(ax, (12.9, 2.4), (11.4, 2.4), color=WATER, lw=2.2)
for xm in (5.85, 12.15):
    ax.text(xm, 4.1, "데우면", ha="center", va="center", fontsize=10, color=RED, fontweight="bold")
    ax.text(xm, 1.9, "식히면", ha="center", va="center", fontsize=10, color=WATER, fontweight="bold")
ax.text(9.0, 5.8, "데우면 알갱이가 세게 꿈틀거려 풀려나고 식히면 약해져 다시 붙어요", ha="center", va="center", fontsize=10)
ax.text(2.7, 0.6, "얼음", ha="center", va="center", fontsize=11, fontweight="bold")
ax.text(9.0, 0.6, "물", ha="center", va="center", fontsize=11, fontweight="bold")
ax.text(15.3, 0.6, "수증기", ha="center", va="center", fontsize=11, fontweight="bold")
save(fig, "m02-change.svg")

# 6. 찬 컵 겉에 맺히는 물방울
fig, ax = canvas(10.0, 4.4, 16.0, 7.0)
ax.add_patch(Polygon([(5.0, 1.0), (9.0, 1.0), (9.6, 5.6), (4.4, 5.6)], closed=True, fc="#eef5fb", ec=INK, lw=1.6))
ax.add_patch(Polygon([(4.65, 4.4), (9.35, 4.4), (9.05, 1.05), (4.95, 1.05)], closed=True, fc="#cfe3f3", ec="none"))
for k in range(4):
    ax.add_patch(Rectangle((5.3 + k * 0.85, 3.9 + 0.15 * (k % 2)), 0.7, 0.7, fc=ICE, ec=INK, lw=1.0))
ax.text(7.0, 2.4, "얼음물", ha="center", va="center", fontsize=10)
for k in range(10):
    y = 1.4 + k * 0.42
    xl = 5.0 - (y - 1.0) * 0.13
    ax.add_patch(Ellipse((xl - 0.08, y), 0.14, 0.2, fc=WATER, ec=INK, lw=0.5))
for k in range(8):
    p = (random.uniform(0.6, 3.6), random.uniform(1.5, 5.5))
    particle(ax, *p, r=0.2)
    arrow(ax, (p[0] + 0.25, p[1]), (p[0] + 1.0, p[1] + random.uniform(-0.2, 0.2)), color=WATER, lw=1.4, ms=10)
ax.text(2.1, 6.3, "공기 속 보이지 않는\n물 알갱이(수증기)", ha="center", va="center", fontsize=10)
ax.text(2.4, 0.5, "차가운 컵에 닿으면\n모여서 물방울이 돼요", ha="center", va="center", fontsize=11, color=RED,
        fontweight="bold")
save(fig, "m02-cold-cup.svg")

# 7. 냄비 위: 맑은 곳과 하얀 김
fig, ax = canvas(9.0, 4.8, 15.0, 8.0)
ax.add_patch(Rectangle((2.0, 0.6), 4.4, 1.8, fc=GREY, ec=INK, lw=1.4))
ax.text(4.2, 1.5, "끓는 냄비", ha="center", va="center", fontsize=10)
for k in range(5):
    p = (2.6 + k * 0.8 + random.uniform(-0.2, 0.2), 3.0 + random.uniform(0, 1.6))
    particle(ax, *p, r=0.12)
    arrow(ax, (p[0], p[1] + 0.15), (p[0] + random.uniform(-0.3, 0.3), p[1] + 0.7), color=RED, lw=0.9, ms=7)
for k in range(9):
    ax.add_patch(Ellipse((3.0 + random.uniform(0, 2.4), 5.8 + random.uniform(0, 1.4)), random.uniform(0.9, 1.5),
                         random.uniform(0.5, 0.8), fc="#e8edf2", ec="#b0bcc8", lw=0.8))
for k in range(14):
    ax.add_patch(Circle((3.0 + random.uniform(0, 2.4), 5.8 + random.uniform(0, 1.4)), 0.05, fc=WATER, ec="none"))
ax.annotate("맑아요: 수증기(눈에 안 보여요)", (5.6, 3.8), (7.6, 3.8), fontsize=11, va="center",
            arrowprops=dict(arrowstyle="-", color=INK, lw=1))
ax.annotate("하얀 김: 식어서 생긴 아주 작은 물방울", (5.8, 6.5), (7.6, 6.5), fontsize=11, va="center", color=RED,
            fontweight="bold", arrowprops=dict(arrowstyle="-", color=RED, lw=1))
save(fig, "m02-steam.svg")
