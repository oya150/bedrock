"""물질과 에너지 5편 그림 만들기. 실행: python lab/fig_m05.py  → docs/matter/img/05/*.svg

글자는 SVG 안에 글자로 남긴다(글꼴 모양을 파일에 넣지 않는다). 보는 쪽 글꼴로 그려진다.
카드는 차분한 색으로, 강조(새로 받은 카드, 비교 화살표, 많이 든 일)만 빨강으로 칠한다.
"""
import itertools
import os

import matplotlib

matplotlib.use("svg")
import matplotlib.pyplot as plt
from matplotlib.patches import Arc, Circle, FancyArrowPatch, FancyBboxPatch, Rectangle

OUT = os.path.join(os.path.dirname(__file__), "..", "docs", "matter", "img", "05")
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


FMT = os.environ.get("FIG_FMT", "svg")
if os.environ.get("FIG_OUT"):
    OUT = os.environ["FIG_OUT"]
    os.makedirs(OUT, exist_ok=True)


def save(fig, name):
    if FMT != "svg":
        name = name.rsplit(".", 1)[0] + "." + FMT
    fig.savefig(os.path.join(OUT, name), bbox_inches="tight", pad_inches=0.25, dpi=110)
    plt.close(fig)


def canvas(w, h, xmax, ymax):
    fig, ax = plt.subplots(figsize=(w, h))
    ax.set_xlim(0, xmax); ax.set_ylim(0, ymax); ax.axis("off")
    return fig, ax


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


def cup(ax, x, y, w, h, fc="#eef5fb"):
    ax.add_patch(Polygon([(x, y + h), (x + w, y + h), (x + w - 0.3, y), (x + 0.3, y)], closed=True, fc=fc, ec=INK,
                         lw=1.6))


def hand(ax, x, y, s=1.0):
    ax.add_patch(FancyBboxPatch((x, y), 2.6 * s, 2.0 * s, boxstyle="round,pad=0.25", fc="#f6d8c4", ec=INK, lw=1.4))
    for k in range(4):
        ax.add_patch(FancyBboxPatch((x + 0.1 * s + k * 0.65 * s, y + 2.05 * s), 0.42 * s, 0.9 * s,
                                    boxstyle="round,pad=0.12", fc="#f6d8c4", ec=INK, lw=1.2))


SALT = "#f7f7f2"


def salt(ax, x, y, r=0.22, hot=False):
    ax.add_patch(Circle((x, y), r, fc=SALT, ec=RED if hot else INK, lw=1.8 if hot else 0.9))


def hydrated(ax, x, y, r=0.22, n=6, rw=0.17, hot=False):
    salt(ax, x, y, r, hot)
    for k in range(n):
        a = 2 * math.pi * k / n + 0.3
        particle(ax, x + (r + rw + 0.02) * math.cos(a), y + (r + rw + 0.02) * math.sin(a), r=rw)


def pile(ax, cx, y, w, h):
    ax.add_patch(Polygon([(cx - w / 2, y), (cx + w / 2, y), (cx + w / 6, y + h), (cx - w / 6, y + h)], closed=True,
                         fc=SALT, ec=INK, lw=1))


# 1. 여는 장면: 녹여도 짠맛
fig, ax = canvas(9.0, 4.2, 14.0, 7.0)
cup(ax, 1.0, 0.8, 3.6, 3.6)
ax.add_patch(FancyBboxPatch((2.4, 5.2), 2.6, 0.35, boxstyle="round,pad=0.08", fc=GREY, ec=INK, lw=1, mutation_aspect=1))
for k in range(10):
    ax.add_patch(Circle((2.7 + random.uniform(-0.2, 0.3), 4.5 + random.uniform(0, 0.7)), 0.06, fc=SALT, ec=INK, lw=0.5))
pile(ax, 2.8, 0.85, 1.4, 0.35)
ax.text(2.8, 0.2, "소금", ha="center", va="center", fontsize=11)
arrow(ax, (5.2, 2.6), (7.0, 2.6))
ax.text(6.1, 3.1, "젓기", ha="center", va="center", fontsize=11)
cup(ax, 7.6, 0.8, 3.6, 3.6)
ax.text(9.4, 0.2, "짠맛", ha="center", va="center", fontsize=11)
ax.text(9.4, 5.3, "?", ha="center", va="center", fontsize=30, color=RED, fontweight="bold")
save(fig, "m05-salt.svg")

# 2. 물 알갱이가 소금 알갱이를 끌어내요
fig, ax = canvas(7.0, 4.6, 10.8, 7.2)
ax.add_patch(Rectangle((0.4, 0.6), 9.6, 6.0, fc="#eef5fb", ec=INK, lw=1.2))
for i in range(5):
    for j in range(5):
        if (i, j) == (4, 4):
            continue
        salt(ax, 1.2 + j * 0.5, 2.0 + i * 0.5)
hydrated(ax, 4.1, 4.4, hot=True)
arrow(ax, (4.5, 4.75), (5.2, 5.3), color=RED, lw=1.6, ms=11)
hydrated(ax, 6.6, 2.6)
hydrated(ax, 8.4, 5.2)
for (x, y) in [(5.6, 1.4), (7.6, 1.2), (9.2, 3.4), (5.2, 6.0), (7.2, 4.0), (3.4, 6.0), (1.4, 5.6), (9.4, 1.4)]:
    particle(ax, x, y, r=0.17)
ax.annotate("물 알갱이", (5.45, 1.35), (3.6, 0.0), fontsize=11, fontweight="bold",
            arrowprops=dict(arrowstyle="-", color=INK, lw=1))
ax.annotate("소금 알갱이", (1.2, 1.8), (0.6, 0.0), fontsize=11, fontweight="bold",
            arrowprops=dict(arrowstyle="-", color=INK, lw=1))
save(fig, "m05-pull.svg")

# 3. 겉부터 작아져요 (세 장면)
fig, ax = canvas(11.0, 3.9, 17.4, 6.2)
loose = [
    [(3.9, 4.8)],
    [(3.7, 5.0), (4.4, 3.8), (3.6, 2.3), (4.5, 1.5), (1.0, 1.5), (0.8, 5.2)],
    [(0.9, 5.0), (2.3, 5.1), (3.8, 5.0), (1.5, 3.7), (3.0, 3.6), (4.4, 3.4), (0.9, 2.0), (2.4, 1.6), (4.0, 1.7)],
]
for p, (name, n) in enumerate([("처음", 5), ("조금 뒤", 3), ("다 녹음", 0)]):
    x0 = 0.3 + p * 5.8
    ax.add_patch(Rectangle((x0, 0.9), 5.2, 5.0, fc="#eef5fb", ec=INK, lw=1.2))
    off = (5 - n) / 2
    for i in range(n):
        for j in range(n):
            edge = i in (0, n - 1) or j in (0, n - 1)
            salt(ax, x0 + 1.15 + (j + off) * 0.36, 2.65 + (i + off) * 0.36, r=0.16, hot=edge)
    for (dx, dy) in loose[p]:
        hydrated(ax, x0 + dx, dy, r=0.15, n=6, rw=0.1)
    ax.text(x0 + 2.6, 0.4, name, ha="center", va="center", fontsize=11, fontweight="bold")
    if p < 2:
        arrow(ax, (x0 + 5.25, 3.4), (x0 + 5.75, 3.4), lw=1.6, ms=12)
save(fig, "m05-shrink.svg")

# 4. 말리면 소금이 남아요
fig, ax = canvas(8.4, 3.6, 13.2, 5.4)
ax.add_patch(Ellipse((2.8, 1.6), 4.4, 1.0, fc="white", ec=INK, lw=1.2))
ax.add_patch(Ellipse((2.8, 1.7), 3.6, 0.6, fc="#eef5fb", ec="none"))
ax.text(2.8, 0.6, "소금물", ha="center", va="center", fontsize=11)
arrow(ax, (5.4, 1.6), (7.4, 1.6))
ax.text(6.4, 2.1, "며칠 뒤", ha="center", va="center", fontsize=11)
ax.add_patch(Ellipse((10.4, 1.6), 4.4, 1.0, fc="white", ec=INK, lw=1.2))
for k in range(30):
    ax.add_patch(Circle((10.4 + random.uniform(-1.6, 1.6), 1.6 + random.uniform(-0.25, 0.25)), 0.06, fc=SALT, ec=INK,
                        lw=0.5))
for (x, y) in [(9.4, 3.2), (10.8, 3.8), (11.8, 2.9)]:
    particle(ax, x, y, r=0.18)
    arrow(ax, (x + 0.1, y + 0.2), (x + 0.45, y + 0.8), color=RED, lw=1.4, ms=9)
ax.text(12.6, 3.6, "물 알갱이", ha="left", va="center", fontsize=11)
ax.text(10.4, 0.6, "하얀 소금", ha="center", va="center", fontsize=11)
save(fig, "m05-dry.svg")

# 5. 가만히 두면 북적이고, 저으면 새 물이 와요
fig, ax = canvas(10.0, 4.2, 12.4, 5.6)
for p, name in enumerate(["가만히", "저으면"]):
    x0 = 0.3 + p * 6.2
    ax.add_patch(Rectangle((x0, 0.9), 5.6, 4.4, fc="#eef5fb", ec=INK, lw=1.2))
    for i in range(3):
        for j in range(4):
            salt(ax, x0 + 2.25 + j * 0.36, 1.35 + i * 0.36, r=0.16)
    if p == 0:
        near = [(x0 + 1.55, 1.5), (x0 + 1.6, 2.4), (x0 + 2.35, 2.75), (x0 + 3.2, 2.85), (x0 + 3.95, 2.3),
                (x0 + 4.0, 1.4)]
        for (x, y) in near:
            hydrated(ax, x, y, r=0.15, n=6, rw=0.1)
        for (x, y) in [(x0 + 0.8, 4.6), (x0 + 2.4, 4.7), (x0 + 4.2, 4.6), (x0 + 1.4, 3.8), (x0 + 3.4, 3.9),
                       (x0 + 4.9, 3.5), (x0 + 0.6, 3.0)]:
            particle(ax, x, y, r=0.15)
    else:
        far = [(x0 + 0.8, 4.6), (x0 + 2.3, 4.75), (x0 + 3.9, 4.75), (x0 + 0.7, 3.2), (x0 + 4.9, 3.2), (x0 + 5.0, 1.6)]
        for (x, y) in far:
            hydrated(ax, x, y, r=0.15, n=6, rw=0.1)
        for (x, y) in [(x0 + 1.8, 1.4), (x0 + 1.85, 2.15), (x0 + 2.4, 2.65), (x0 + 3.05, 2.7), (x0 + 3.65, 2.5),
                       (x0 + 3.9, 1.65)]:
            ax.add_patch(Circle((x, y), 0.15, fc=WATER, ec=RED, lw=1.6))
        ax.add_patch(Arc((x0 + 2.8, 3.45), 3.2, 0.8, theta1=200, theta2=520, color=RED, lw=1.6))
    ax.text(x0 + 2.8, 0.4, name, ha="center", va="center", fontsize=11, fontweight="bold")
save(fig, "m05-stir.svg")

# 6. 잘게 부수면 물에 닿는 알갱이가 늘어요
fig, ax = canvas(9.0, 3.8, 11.6, 5.0)
ax.add_patch(Rectangle((0.3, 0.9), 11.0, 3.9, fc="#eef5fb", ec=INK, lw=1.2))
for i in range(4):
    for j in range(4):
        edge = i in (0, 3) or j in (0, 3)
        salt(ax, 1.5 + j * 0.44, 1.9 + i * 0.44, r=0.2, hot=edge)
ax.text(2.16, 0.4, "덩어리: 겉 12", ha="center", va="center", fontsize=11, fontweight="bold")
arrow(ax, (3.9, 2.85), (5.5, 2.85), lw=1.6, ms=12)
for (bx, by) in [(6.4, 3.2), (8.3, 3.4), (6.7, 1.5), (8.7, 1.6)]:
    for i in range(2):
        for j in range(2):
            salt(ax, bx + j * 0.44, by + i * 0.44, r=0.2, hot=True)
ax.text(7.8, 0.4, "가루: 겉 16", ha="center", va="center", fontsize=11, fontweight="bold")
save(fig, "m05-powder.svg")

# 7. 녹는 데도 끝이 있어요
fig, ax = canvas(11.0, 3.8, 19.2, 6.4)
cases = [("한 숟가락", 0, 3.2), ("여러 숟가락", 0, 3.2), ("더 넣으면", 1, 3.2), ("물을 더", 0, 4.4)]
for i, (lab, heap, lvl) in enumerate(cases):
    x = 0.6 + i * 4.7
    cup(ax, x, 1.4, 3.2, 3.6, fc="white")
    top = min(lvl, 4.9)
    ax.add_patch(Polygon([(x + 0.32, 1.42), (x + 2.88, 1.42), (x + 2.88 + 0.3 * (top - 1.4) / 3.6, top),
                          (x + 0.32 - 0.3 * (top - 1.4) / 3.6, top)], closed=True, fc="#eef5fb", ec="none"))
    if heap:
        pile(ax, x + 1.6, 1.45, 2.2, 0.5)
    ax.text(x + 1.6, 0.8, lab, ha="center", va="center", fontsize=11, fontweight="bold",
            color=RED if heap else "#222")
    if i < 3:
        arrow(ax, (x + 3.3, 3.2), (x + 4.5, 3.2), lw=1.4, ms=11)
save(fig, "m05-limit.svg")
