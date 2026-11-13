"""물질과 에너지 3편 그림 만들기. 실행: python lab/fig_m03.py  → docs/matter/img/03/*.svg

글자는 SVG 안에 글자로 남긴다(글꼴 모양을 파일에 넣지 않는다). 보는 쪽 글꼴로 그려진다.
카드는 차분한 색으로, 강조(새로 받은 카드, 비교 화살표, 많이 든 일)만 빨강으로 칠한다.
"""
import itertools
import os

import matplotlib

matplotlib.use("svg" if os.environ.get("FIG_FMT", "svg") == "svg" else "agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Arc, Circle, FancyArrowPatch, FancyBboxPatch, Rectangle

OUT = os.environ.get("FIG_OUT") or os.path.join(os.path.dirname(__file__), "..", "docs", "matter", "img", "03")
FMT = os.environ.get("FIG_FMT", "svg")
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
    name = name.rsplit(".", 1)[0] + "." + FMT
    fig.savefig(os.path.join(OUT, name), bbox_inches="tight", pad_inches=0.25, dpi=110)
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




SKIN = "#f3b9a3"


# 1. 여는 장면: 얼음을 손에 쥐면
fig, ax = canvas(7.0, 2.8, 12.0, 4.6)
hand(ax, 3.4, 0.3, 1.4)
ax.add_patch(Polygon([(4.5, 1.4), (5.9, 1.4), (6.2, 2.4), (4.8, 2.4)], closed=True, fc=ICE, ec=INK, lw=1.4))
for k in range(3):
    ax.add_patch(Ellipse((4.8 + k * 0.5, 1.25), 0.18, 0.12, fc=WATER, ec="none"))
arrow(ax, (5.35, 0.75), (5.35, 1.35), color=RED, lw=2.6, ms=16)
ax.annotate("손", (3.5, 1.2), (1.6, 1.2), fontsize=13, fontweight="bold", va="center", ha="center",
            arrowprops=dict(arrowstyle="-", color=INK, lw=1))
ax.annotate("얼음", (6.1, 2.0), (8.4, 2.0), fontsize=13, fontweight="bold", va="center", ha="center",
            arrowprops=dict(arrowstyle="-", color=INK, lw=1))
save(fig, "m03-hand.svg")

# 2. 찬물과 따뜻한 물
fig, ax = canvas(10.0, 4.2, 16.0, 6.6)
for x, strength, fc, lab in [(1.0, 0.25, "#eef5fb", "찬물"), (9.0, 0.7, "#fbe9e3", "따뜻한 물")]:
    cup(ax, x, 1.4, 6.0, 4.6, fc=fc)
    for i in range(4):
        for j in range(5):
            mover(ax, x + 1.0 + j * 1.0 + (0.5 if i % 2 else 0) + random.uniform(-0.1, 0.1),
                  2.2 + i * 1.0 + random.uniform(-0.1, 0.1), strength * random.uniform(0.8, 1.1))
    ax.text(x + 3.0, 0.8, lab, ha="center", va="center", fontsize=13, fontweight="bold",
            color=RED if strength > 0.5 else "#222")
save(fig, "m03-cups.svg")

# 3. 구슬치기
fig, ax = canvas(9.0, 4.2, 14.0, 6.8)
MARBLE = "#cfd8e3"
ax.text(0.4, 5.9, "부딪히는 순간", ha="left", va="center", fontsize=12, fontweight="bold")
ax.add_patch(Circle((5.0, 4.4), 0.45, fc=MARBLE, ec=INK, lw=1.4))
arrow(ax, (2.2, 4.4), (4.5, 4.4), color=RED, lw=2.2)
ax.add_patch(Circle((5.9, 4.4), 0.45, fc=MARBLE, ec=INK, lw=1.4))
arrow(ax, (6.4, 4.4), (7.0, 4.4), color=INK, lw=1.6)
ax.text(5.0, 3.6, "빠름", ha="center", va="center", fontsize=11, color=RED, fontweight="bold")
ax.text(5.9, 3.6, "느림", ha="center", va="center", fontsize=11)
ax.text(0.4, 2.6, "부딪힌 뒤", ha="left", va="center", fontsize=12, fontweight="bold")
ax.add_patch(Circle((4.2, 1.3), 0.45, fc=MARBLE, ec=INK, lw=1.4))
arrow(ax, (4.7, 1.3), (5.3, 1.3), color=INK, lw=1.6)
ax.add_patch(Circle((7.0, 1.3), 0.45, fc=MARBLE, ec=INK, lw=1.4))
arrow(ax, (7.5, 1.3), (9.8, 1.3), color=RED, lw=2.2)
ax.text(4.2, 0.5, "느림", ha="center", va="center", fontsize=11)
ax.text(7.0, 0.5, "빠름", ha="center", va="center", fontsize=11, color=RED, fontweight="bold")
save(fig, "m03-marbles.svg")

# 4. 손과 얼음이 닿은 곳
fig, ax = canvas(9.0, 4.6, 14.0, 7.2)
ax.add_patch(Rectangle((0.6, 0.9), 6.0, 5.4, fc="#fbe9e3", ec=INK, lw=1.2))
ax.add_patch(Rectangle((6.6, 0.9), 6.0, 5.4, fc="#eef5fb", ec=INK, lw=1.2))
for i in range(5):
    for j in range(5):
        mover(ax, 1.3 + j * 1.15, 1.5 + i * 1.05, 0.65 * random.uniform(0.85, 1.1), fc=SKIN)
        mover(ax, 7.3 + j * 1.15, 1.5 + i * 1.05, 0.2 * random.uniform(0.8, 1.1), color=INK)
ax.add_patch(FancyArrowPatch((5.6, 6.75), (7.6, 6.75), arrowstyle="simple", mutation_scale=26, fc=RED, ec=RED))
ax.text(3.6, 0.35, "손", ha="center", va="center", fontsize=13, fontweight="bold")
ax.text(9.6, 0.35, "얼음", ha="center", va="center", fontsize=13, fontweight="bold")
save(fig, "m03-contact.svg")

# 5. 숟가락을 따라 차례로
fig, ax = canvas(8.0, 4.6, 13.0, 8.0)
cup(ax, 1.0, 0.8, 5.0, 4.0, fc="#e8d3c0")
ax.text(3.5, 1.8, "코코아", ha="center", va="center", fontsize=12)
ax.plot([3.0, 8.4], [3.4, 7.2], color="#9aa3ad", lw=10, solid_capstyle="round")
for k in range(6):
    px, py = 3.6 + k * 0.95, 3.82 + k * 0.67
    particle(ax, px, py, r=0.2, fc="#b9c2cc")
    if k < 5:
        arrow(ax, (px + 0.15, py + 0.45), (px + 0.85, py + 0.95), color=RED, lw=1.2, ms=9)
ax.text(9.0, 7.3, "손잡이", ha="left", va="center", fontsize=12, fontweight="bold")
save(fig, "m03-spoon.svg")

# 6. 쇠와 나무
fig, ax = canvas(10.0, 4.4, 16.0, 7.0)
for x, fc, w, lab, speed, col in [(0.6, "#9aa3ad", 4.0, "쇠 숟가락", "빨리", RED),
                                  (8.6, "#c8a27a", 1.6, "나무 주걱", "천천히", INK)]:
    ax.add_patch(Rectangle((x + 0.4, 1.9), 4.6, 0.4, fc=fc, ec=INK, lw=1.2))
    ax.add_patch(Ellipse((x + 5.6, 2.1), 1.4, 0.9, fc=fc, ec=INK, lw=1.2))
    hand(ax, x + 1.0, 2.35, 0.8)
    ax.add_patch(FancyArrowPatch((x + 0.55, 3.6), (x + 0.55, 2.45), arrowstyle="simple", mutation_scale=8 + w * 6,
                                 fc=RED, ec=RED, lw=0.5))
    ax.text(x - 0.1, 3.05, "열", ha="right", va="center", fontsize=11, color=RED, fontweight="bold")
    ax.text(x + 3.4, 1.0, lab, ha="center", va="center", fontsize=12, fontweight="bold")
    ax.text(x + 3.4, 0.35, speed, ha="center", va="center", fontsize=11, color=col, fontweight="bold")
ax.text(8.0, 6.7, "같은 방 · 같은 온도", ha="center", va="center", fontsize=11)
save(fig, "m03-metal-wood.svg")

# 7. 같아지면 멈춰요
fig, ax = canvas(8.0, 4.4, 12.0, 7.0)
for y, start_fc, lab in [(4.0, "#f3c6b8", "따뜻한 우유"), (0.8, "#cfe3f3", "차가운 우유")]:
    cup(ax, 1.0, y, 1.8, 2.0, fc=start_fc)
    ax.text(1.9, y - 0.35, lab, ha="center", va="center", fontsize=11)
    arrow(ax, (3.3, y + 1.0), (6.3, y + 1.0), color=INK, lw=1.8)
    ax.text(4.8, y + 1.4, "시간", ha="center", va="center", fontsize=10)
    cup(ax, 6.8, y, 1.8, 2.0, fc="#efe9dc")
    ax.text(7.7, y - 0.35, "방 온도", ha="center", va="center", fontsize=11, color=RED, fontweight="bold")
save(fig, "m03-equal.svg")
