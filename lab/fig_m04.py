"""물질과 에너지 4편 그림 만들기. 실행: python lab/fig_m04.py  → docs/matter/img/04/*.svg

글자는 SVG 안에 글자로 남긴다(글꼴 모양을 파일에 넣지 않는다). 보는 쪽 글꼴로 그려진다.
카드는 차분한 색으로, 강조(새로 받은 카드, 비교 화살표, 많이 든 일)만 빨강으로 칠한다.
"""
import itertools
import os

import matplotlib

matplotlib.use("svg" if os.environ.get("FIG_FMT", "svg") == "svg" else "agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Arc, Circle, FancyArrowPatch, FancyBboxPatch, Rectangle

OUT = os.environ.get("FIG_OUT") or os.path.join(os.path.dirname(__file__), "..", "docs", "matter", "img", "04")
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


def towel(ax, x, y, w, h, fc="#cfe3f3"):
    ax.add_patch(Rectangle((x, y), w, h, fc=fc, ec=INK, lw=1.2))


def wind(ax, x, y, n=3, L=1.6):
    for k in range(n):
        xs = [x + t * L / 12 for t in range(13)]
        ys = [y + k * 0.45 + 0.08 * math.sin(t * 1.2) for t in range(13)]
        ax.plot(xs, ys, color=INK, lw=1.2)


# 1. 여는 장면: 수영장에서 나오면
fig, ax = canvas(7.0, 3.6, 11.0, 5.6)
kid(ax, 5.0, 0.8, 2.2)
for (dx, dy) in [(-0.7, 3.4), (0.6, 3.0), (-0.4, 2.0), (0.8, 1.6), (-0.9, 1.2)]:
    ax.add_patch(Ellipse((5.0 + dx, 0.8 + dy), 0.18, 0.28, fc=WATER, ec=INK, lw=0.6))
wind(ax, 0.6, 2.2, n=4, L=2.4)
ax.text(1.8, 1.6, "바람", ha="center", va="center", fontsize=12)
ax.text(7.2, 3.6, "으슬으슬", ha="left", va="center", fontsize=13, color=RED, fontweight="bold")
save(fig, "m04-pool.svg")

# 2. 표면에서 날아가는 알갱이
fig, ax = canvas(9.0, 4.6, 14.0, 7.4)
ax.add_patch(Rectangle((0.6, 0.8), 9.0, 3.6, fc="#eef5fb", ec=INK, lw=1.4))
for i in range(4):
    for j in range(9):
        x = 1.2 + j * 0.95 + (0.45 if i % 2 else 0) + random.uniform(-0.08, 0.08)
        y = 1.3 + i * 0.85 + random.uniform(-0.06, 0.06)
        if x > 9.2:
            continue
        mover(ax, x, y, random.choice([0.15, 0.2, 0.3, 0.35, 0.45]))
for (x, y) in [(3.0, 5.4), (6.8, 6.1)]:
    particle(ax, x, y)
    arrow(ax, (x + 0.1, y + 0.25), (x + 0.6, y + 1.0), color=RED, lw=1.6, ms=10)
    ax.plot([x - 0.2, x - 0.6], [y - 0.3, y - 0.9], color=RED, lw=1, ls=":")
ax.text(10.2, 2.6, "물", ha="left", va="center", fontsize=12)
ax.text(10.2, 5.6, "공기", ha="left", va="center", fontsize=12)
save(fig, "m04-surface.svg")

# 3. 구슬 쟁반
fig, ax = canvas(8.0, 3.6, 12.0, 5.8)
MARBLE = "#cfd8e3"
ax.add_patch(Rectangle((1.0, 1.0), 7.0, 0.25, fc="#c8a27a", ec=INK, lw=1.2))
ax.add_patch(Rectangle((1.0, 1.25), 0.25, 0.7, fc="#c8a27a", ec=INK, lw=1.2))
ax.add_patch(Rectangle((7.75, 1.25), 0.25, 0.7, fc="#c8a27a", ec=INK, lw=1.2))
for k, x in enumerate([2.0, 3.3, 4.6, 5.9]):
    ax.add_patch(Circle((x, 1.65), 0.38, fc=MARBLE, ec=INK, lw=1.2))
    L = [0.35, 0.55, 0.3, 0.5][k]
    arrow(ax, (x + 0.42, 1.65), (x + 0.42 + L, 1.65), color=INK, lw=1.2, ms=9)
for (x, y) in [(8.9, 2.7), (2.0, 3.9)]:
    ax.add_patch(Circle((x, y), 0.38, fc=MARBLE, ec=INK, lw=1.2))
arrow(ax, (9.3, 2.85), (10.6, 3.3), color=RED, lw=2.2)
arrow(ax, (1.6, 4.1), (0.5, 4.7), color=RED, lw=2.2)
ax.text(10.0, 3.8, "빠름", ha="center", va="center", fontsize=11, color=RED, fontweight="bold")
ax.text(1.0, 5.2, "빠름", ha="center", va="center", fontsize=11, color=RED, fontweight="bold")
ax.text(4.5, 0.45, "느림", ha="center", va="center", fontsize=11)
ax.annotate("턱", (8.0, 1.9), (8.6, 0.6), fontsize=11, arrowprops=dict(arrowstyle="-", color=INK, lw=1))
save(fig, "m04-tray.svg")

# 4. 손등 위 물
fig, ax = canvas(8.0, 4.6, 12.5, 7.4)
ax.add_patch(FancyBboxPatch((0.8, 0.6), 8.4, 1.6, boxstyle="round,pad=0.3", fc="#f6d8c4", ec=INK, lw=1.4))
ax.text(5.0, 1.0, "손등", ha="center", va="center", fontsize=11)
ax.add_patch(Rectangle((1.4, 2.3), 7.2, 1.3, fc="#eef5fb", ec=INK, lw=1.0))
for j in range(8):
    mover(ax, 1.9 + j * 0.9, 2.95, [0.12, 0.2, 0.15, 0.25, 0.1, 0.18, 0.22, 0.14][j], r=0.22)
for x in (2.6, 5.0, 7.4):
    arrow(ax, (x, 1.5), (x, 2.5), color=RED, lw=2.0, ms=12)
ax.text(3.8, 1.9, "열", ha="center", va="center", fontsize=11, color=RED, fontweight="bold")
for (x, y) in [(3.6, 4.8), (6.4, 5.4)]:
    particle(ax, x, y, r=0.22)
    arrow(ax, (x + 0.1, y + 0.25), (x + 0.5, y + 1.0), color=RED, lw=1.6, ms=10)
ax.text(9.6, 5.2, "날아간 알갱이", ha="left", va="center", fontsize=11)
ax.text(9.6, 3.0, "남은 물", ha="left", va="center", fontsize=11, fontweight="bold")
save(fig, "m04-hand.svg")

# 5. 돌아오는 알갱이와 바람
fig, ax = canvas(10.0, 4.0, 16.0, 6.4)
for i, (lab, windy) in enumerate([("바람 없음", False), ("바람", True)]):
    x = 0.4 + i * 8.0
    ax.add_patch(Rectangle((x, 0.9), 6.6, 1.4, fc="#eef5fb", ec=INK, lw=1.2))
    for j in range(7):
        particle(ax, x + 0.5 + j * 0.93, 1.6, r=0.22)
    ax.text(x + 3.3, 0.35, lab, ha="center", va="center", fontsize=12, fontweight="bold")
    if not windy:
        for (px, py) in [(x + 1.5, 4.2), (x + 3.4, 3.4), (x + 5.2, 4.6)]:
            particle(ax, px, py, r=0.22)
        arrow(ax, (x + 3.4, 3.1), (x + 3.4, 2.4), color=RED, lw=1.8, ms=12)
        arrow(ax, (x + 1.5, 3.9), (x + 1.7, 2.4), color=RED, lw=1.8, ms=12)
    else:
        wind(ax, x + 0.2, 3.2, n=3, L=2.0)
        for (px, py) in [(x + 4.4, 3.4), (x + 5.4, 4.3), (x + 6.4, 3.7)]:
            particle(ax, px, py, r=0.22)
            arrow(ax, (px + 0.25, py), (px + 1.0, py + 0.1), color=INK, lw=1.4, ms=10)
save(fig, "m04-return.svg")

# 6. 빨리 마르는 때
fig, ax = canvas(11.0, 3.8, 18.0, 6.2)
for i, lab in enumerate(["바람", "햇볕", "넓게 펼치기"]):
    x = 0.3 + i * 6.0
    box(ax, x, 0.5, 5.4, 5.0, fc=NOTE)
    ax.text(x + 2.7, 1.0, lab, ha="center", va="center", fontsize=12, fontweight="bold")
    if i == 0:
        ax.plot([x + 0.4, x + 5.0], [4.6, 4.6], color=INK, lw=1)
        towel(ax, x + 2.6, 2.4, 1.6, 2.2)
        wind(ax, x + 0.4, 2.8, n=3, L=1.8)
    elif i == 1:
        ax.plot([x + 0.4, x + 5.0], [4.0, 4.0], color=INK, lw=1)
        towel(ax, x + 1.0, 1.9, 1.6, 2.1)
        ax.add_patch(Circle((x + 4.2, 4.6), 0.5, fc=YEL, ec=INK, lw=1))
        for a in range(0, 360, 45):
            r = math.radians(a)
            ax.plot([x + 4.2 + 0.65 * math.cos(r), x + 4.2 + 0.85 * math.cos(r)],
                    [4.6 + 0.65 * math.sin(r), 4.6 + 0.85 * math.sin(r)], color=INK, lw=1)
    else:
        ax.plot([x + 0.4, x + 5.0], [4.6, 4.6], color=INK, lw=1)
        towel(ax, x + 0.6, 2.0, 2.6, 2.6)
        towel(ax, x + 3.8, 3.6, 0.8, 1.0)
save(fig, "m04-fast.svg")
