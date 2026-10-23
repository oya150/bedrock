"""인체 6편 그림 만들기. 실행: python lab/fig_b06.py  → docs/body/img/06/*.svg

글자는 SVG 안에 글자로 남긴다(글꼴 모양을 파일에 넣지 않는다). 보는 쪽 글꼴로 그려진다.
카드는 차분한 색으로, 강조(새로 받은 카드, 비교 화살표, 많이 든 일)만 빨강으로 칠한다.
"""
import itertools
import os

import matplotlib

matplotlib.use("svg")
import matplotlib.pyplot as plt
from matplotlib.patches import Arc, Circle, FancyArrowPatch, FancyBboxPatch, Rectangle

OUT = os.path.join(os.path.dirname(__file__), "..", "docs", "body", "img", "06")
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

CELL = "#fbe3dc"
BLOOD = "#c0392b"
SKIN = "#f6d8c4"
PLATE = "#f6c445"
FIBER = "#8a6d3b"
SCAB = "#7a3b2e"

random.seed(6)


def vessel(ax, x0, x1, y, h, gap=None):
    """가로 핏줄: 위아래 벽. gap=(xa, xb)면 위 벽에 구멍."""
    ax.add_patch(Rectangle((x0, y), x1 - x0, h, fc="#f7d6d0", ec="none"))
    ax.plot([x0, x1], [y, y], color=BLOOD, lw=3)
    if gap:
        ax.plot([x0, gap[0]], [y + h, y + h], color=BLOOD, lw=3)
        ax.plot([gap[1], x1], [y + h, y + h], color=BLOOD, lw=3)
    else:
        ax.plot([x0, x1], [y + h, y + h], color=BLOOD, lw=3)


def rbc(ax, x, y, r=0.22):
    ax.add_patch(Ellipse((x, y), 2 * r, 1.6 * r, fc=BLOOD, ec=INK, lw=0.6))


def plate(ax, x, y, spiky=False):
    if spiky:
        pts = []
        for k in range(12):
            a = 2 * math.pi * k / 12
            rr = 0.17 if k % 2 == 0 else 0.09
            pts.append((x + rr * math.cos(a), y + rr * math.sin(a)))
        ax.add_patch(Polygon(pts, closed=True, fc=PLATE, ec=INK, lw=0.6))
    else:
        ax.add_patch(Ellipse((x, y), 0.26, 0.14, fc=PLATE, ec=INK, lw=0.6))


# 1. 여는 장면: 종이에 손가락 베임
fig, ax = canvas(10.0, 4.6, 16.0, 7.4)
ax.add_patch(FancyBboxPatch((1.0, 1.6), 2.0, 4.6, boxstyle="round,pad=0.5", fc=SKIN, ec=INK, lw=1.6))
ax.plot([1.4, 2.6], [4.4, 4.1], color=BLOOD, lw=2)
ax.add_patch(Circle((2.1, 3.85), 0.22, fc=BLOOD, ec=BLOOD))
ax.add_patch(Polygon([(3.6, 2.0), (6.4, 2.6), (6.0, 6.4), (3.2, 5.8)], closed=True, fc="white", ec=INK, lw=1.4))
ax.text(4.8, 4.2, "종이", ha="center", va="center", fontsize=11)
ax.text(2.0, 0.8, "피가 몽글", ha="center", va="center", fontsize=11, color=BLOOD, fontweight="bold")
arrow(ax, (7.2, 4.0), (8.6, 4.0))
ax.add_patch(FancyBboxPatch((9.4, 1.6), 2.0, 4.6, boxstyle="round,pad=0.5", fc=SKIN, ec=INK, lw=1.6))
ax.plot([9.8, 11.0], [4.4, 4.1], color=BLOOD, lw=2.6)
ax.text(10.4, 0.8, "조금 뒤 멈춰요", ha="center", va="center", fontsize=11, fontweight="bold")
ax.text(14.2, 4.0, "피는 쉬지 않고\n도는데\n왜 멈출까?", ha="center", va="center", fontsize=12, color=RED,
        fontweight="bold")
save(fig, "b06-cut.svg")

# 2. 이 편의 지도
fig, ax = canvas(11.6, 2.9, 19.4, 4.6)
titles = ["핏줄이 오므라들어요", "조각이 모여 막아요", "실로 얽어 굳혀요", "딱지 아래 새살"]
for i, t in enumerate(titles):
    x = 0.3 + i * 4.8
    box(ax, x, 0.4, 3.8, 3.6)
    ax.text(x + 1.9, 0.95, t, ha="center", va="center", fontsize=11, fontweight="bold")
    cx = x + 1.9
    if i == 0:
        ax.plot([x + 0.5, cx - 0.3, cx + 0.3, x + 3.3], [3.2, 2.8, 2.8, 3.2], color=BLOOD, lw=2)
        ax.plot([x + 0.5, cx - 0.3, cx + 0.3, x + 3.3], [1.8, 2.2, 2.2, 1.8], color=BLOOD, lw=2)
    elif i == 1:
        for k in range(7):
            plate(ax, cx - 0.6 + (k % 4) * 0.4, 2.3 + (k // 4) * 0.35, spiky=True)
    elif i == 2:
        for k in range(6):
            ax.plot([x + 0.6, x + 3.2], [1.8 + k * 0.3, 3.3 - k * 0.3], color=FIBER, lw=0.9)
        rbc(ax, cx - 0.3, 2.6)
        rbc(ax, cx + 0.4, 2.3)
    else:
        ax.add_patch(Ellipse((cx, 2.9), 2.2, 0.5, fc=SCAB, ec=INK, lw=1))
        ax.add_patch(Rectangle((x + 0.5, 1.6), 2.8, 0.9, fc=SKIN, ec=INK, lw=1))
    if i < 3:
        arrow(ax, (x + 3.95, 2.2), (x + 4.65, 2.2))
save(fig, "b06-map.svg")

# 3. 핏줄이 오므라들어요
fig, ax = canvas(11.0, 3.8, 18.0, 6.2)
vessel(ax, 0.6, 7.6, 2.0, 2.0, gap=(3.6, 4.6))
for k in range(8):
    rbc(ax, 1.0 + k * 0.8, 3.0)
for k in range(5):
    rbc(ax, 4.1 + 0.15 * k, 4.4 + k * 0.35)
ax.text(4.1, 0.9, "다친 핏줄", ha="center", va="center", fontsize=11, fontweight="bold")
arrow(ax, (8.3, 3.0), (9.6, 3.0))
xs = [10.2, 12.4, 13.3, 14.3, 15.2, 17.4]
top = [4.0, 4.0, 3.5, 3.5, 4.0, 4.0]
bot = [2.0, 2.0, 2.5, 2.5, 2.0, 2.0]
ax.add_patch(Polygon(list(zip(xs, top)) + list(zip(xs[::-1], bot[::-1])), closed=True, fc="#f7d6d0", ec="none"))
ax.plot(xs[:3], top[:3], color=BLOOD, lw=3)
ax.plot(xs[3:], top[3:], color=BLOOD, lw=3)
ax.plot(xs, bot, color=BLOOD, lw=3)
for k in range(3):
    rbc(ax, 13.6 + 0.12 * k, 4.0 + k * 0.3, r=0.18)
for x in (10.8, 11.8, 13.8, 15.8, 16.8):
    rbc(ax, x, 3.0, r=0.2)
ax.text(13.8, 0.9, "벽이 오므라들어 피가 덜 나와요", ha="center", va="center", fontsize=11, color=RED,
        fontweight="bold")
save(fig, "b06-squeeze.svg")

# 4. 혈소판이 모여 막아요
fig, ax = canvas(11.0, 4.6, 18.0, 7.4)
for p, (x0, spiky_all, lab) in enumerate([(0.6, False, "평소: 매끈하게 떠다녀요"), (9.6, True, "다치면: 구멍에 달라붙고 서로 불러 쌓여요")]):
    vessel(ax, x0, x0 + 7.6, 1.6, 2.4, gap=(x0 + 3.4, x0 + 4.6) if spiky_all else None)
    for k in range(7):
        rbc(ax, x0 + 0.6 + k * 1.1, 2.4)
    if not spiky_all:
        for k in range(6):
            plate(ax, x0 + 1.0 + k * 1.2, 3.3)
    else:
        for k in range(14):
            plate(ax, x0 + 3.5 + (k % 5) * 0.25, 3.6 + (k // 5) * 0.28, spiky=True)
        for k in range(3):
            plate(ax, x0 + 1.2 + k * 0.6, 3.2, spiky=True)
            arrow(ax, (x0 + 1.4 + k * 0.6, 3.3), (x0 + 3.2, 3.7), color=PLATE, lw=1.2, ms=9)
    ax.text(x0 + 3.8, 0.7, lab, ha="center", va="center", fontsize=11, fontweight="bold")
ax.plot([8.9, 8.9], [0.4, 6.6], color=GREY, lw=1.2, ls="--")
ax.text(1.6, 4.3, "혈소판", ha="center", va="center", fontsize=10, fontweight="bold")
ax.text(14.9, 5.2, "혈소판 마개", ha="left", va="center", fontsize=10, fontweight="bold")
save(fig, "b06-plug.svg")

# 5. 실로 얽어 굳혀요
fig, ax = canvas(10.0, 5.0, 16.0, 8.0)
clipbox = Rectangle((1.6, 1.2), 12.8, 5.6, fc="#fdf1ee", ec=GREY, lw=1)
ax.add_patch(clipbox)
for k in range(22):
    x1, y1 = random.uniform(2.0, 14.0), random.uniform(1.4, 6.6)
    a = random.uniform(0, math.pi)
    L = random.uniform(3.0, 6.0)
    ln, = ax.plot([x1 - L / 2 * math.cos(a), x1 + L / 2 * math.cos(a)],
                  [y1 - L / 2 * math.sin(a), y1 + L / 2 * math.sin(a)], color=FIBER, lw=1.0)
    ln.set_clip_path(clipbox)
for k in range(18):
    rbc(ax, random.uniform(3.0, 13.0), random.uniform(2.0, 6.0), r=0.32)
for k in range(10):
    plate(ax, random.uniform(3.0, 13.0), random.uniform(2.0, 6.0), spiky=True)
ax.plot([14.7, 15.2], [5.6, 5.6], color=FIBER, lw=1.6)
ax.text(15.3, 5.6, "실", ha="left", va="center", fontsize=11, fontweight="bold")
rbc(ax, 14.95, 4.4, r=0.25)
ax.text(15.3, 4.4, "빨간 세포", ha="left", va="center", fontsize=10, fontweight="bold")
plate(ax, 14.95, 3.2, spiky=True)
ax.text(15.3, 3.2, "혈소판", ha="left", va="center", fontsize=10, fontweight="bold")
ax.text(8.0, 7.5, "가는 실이 그물처럼 얽히고 빨간 세포가 걸려요", ha="center", va="center", fontsize=11,
        fontweight="bold")
for (x0, y0, dx, dy) in ((1.3, 7.0, 0.8, -0.6), (14.7, 7.0, -0.8, -0.6), (1.3, 1.0, 0.8, 0.6), (14.7, 1.0, -0.8, 0.6)):
    arrow(ax, (x0, y0), (x0 + dx, y0 + dy), color=RED, lw=1.6, ms=12)
ax.text(8.0, 0.6, "그물이 오므라들면서 덩어리가 단단해져요", ha="center", va="center", fontsize=11, color=RED,
        fontweight="bold")
ax.set_xlim(1.0, 17.4)
save(fig, "b06-mesh.svg")

# 6. 딱지 아래 새살
fig, ax = canvas(11.0, 4.4, 18.0, 7.2)
for k, (x0, stage) in enumerate([(0.4, 0), (6.4, 1), (12.4, 2)]):
    ax.add_patch(Rectangle((x0, 1.4), 5.2, 3.0, fc=SKIN, ec=INK, lw=1.2))
    if stage == 0:
        ax.add_patch(Polygon([(x0 + 1.8, 4.4), (x0 + 3.4, 4.4), (x0 + 2.9, 2.6), (x0 + 2.3, 2.6)], closed=True,
                             fc=BLOOD, ec=INK, lw=1))
        lab = "덩어리가 구멍을 막아요"
    elif stage == 1:
        ax.add_patch(Ellipse((x0 + 2.6, 4.5), 2.2, 0.6, fc=SCAB, ec=INK, lw=1))
        ax.add_patch(Polygon([(x0 + 1.9, 4.4), (x0 + 3.3, 4.4), (x0 + 2.9, 3.3), (x0 + 2.3, 3.3)], closed=True,
                             fc=CELL, ec=RED, lw=1))
        for j in range(4):
            ax.add_patch(Circle((x0 + 2.2 + j * 0.25, 3.7), 0.1, fc=CELL, ec=RED, lw=0.8))
        lab = "딱지 아래에서 새 세포가 채워요"
    else:
        ax.add_patch(Ellipse((x0 + 4.4, 5.8), 1.2, 0.4, fc=SCAB, ec=INK, lw=1))
        arrow(ax, (x0 + 3.2, 4.8), (x0 + 3.9, 5.5), color=INK, lw=1.2, ms=10)
        lab = "다 나으면 딱지가 떨어져요"
    ax.text(x0 + 2.6, 0.7, lab, ha="center", va="center", fontsize=10, fontweight="bold")
for x0 in (0.4, 6.4):
    arrow(ax, (x0 + 5.3, 3.0), (x0 + 6.3, 3.0), lw=2.4)
save(fig, "b06-scab.svg")
