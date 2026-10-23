"""물질과 에너지 6편 그림 만들기. 실행: python lab/fig_m06.py  → docs/matter/img/06/*.svg

글자는 SVG 안에 글자로 남긴다(글꼴 모양을 파일에 넣지 않는다). 보는 쪽 글꼴로 그려진다.
카드는 차분한 색으로, 강조(새로 받은 카드, 비교 화살표, 많이 든 일)만 빨강으로 칠한다.
"""
import itertools
import os

import matplotlib

matplotlib.use("svg")
import matplotlib.pyplot as plt
from matplotlib.patches import Arc, Circle, FancyArrowPatch, FancyBboxPatch, Rectangle

OUT = os.path.join(os.path.dirname(__file__), "..", "docs", "matter", "img", "06")
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


STONE, WOOD = "#9aa3ad", "#c8a27a"


def honeycomb(x0, y0, cols, rows, a=0.42):
    """육각 고리 꼭짓점들(겹치지 않게)."""
    pts = set()
    w, h = math.sqrt(3) * a, 1.5 * a
    for r in range(rows):
        for c in range(cols):
            cx = x0 + c * w + (w / 2 if r % 2 else 0)
            cy = y0 + r * h
            for k in range(6):
                ang = math.radians(90 + 60 * k)
                pts.add((round(cx + a * math.cos(ang), 3), round(cy + a * math.sin(ang), 3)))
    return sorted(pts), [(x0 + c * w + (w / 2 if r % 2 else 0), y0 + r * h) for r in range(rows) for c in range(cols)]


# 1. 여는 장면
fig, ax = canvas(8.0, 4.2, 13.0, 6.8)
cup(ax, 3.5, 0.6, 5.0, 4.6)
ax.add_patch(Rectangle((3.75, 0.65), 4.5, 3.6, fc="#cfe3f3", ec="none"))
ax.add_patch(Rectangle((4.6, 3.05), 1.4, 1.35, fc=ICE, ec=INK, lw=1.4))
ax.plot([3.75, 8.25], [4.25, 4.25], color=WATER, lw=1.2)
ax.add_patch(Ellipse((6.9, 0.95), 1.0, 0.55, fc=STONE, ec=INK, lw=1.2))
ax.annotate("얼음", (6.0, 4.3), (9.4, 4.9), fontsize=10, arrowprops=dict(arrowstyle="-", color=INK, lw=1))
ax.annotate("돌멩이", (7.4, 1.0), (9.4, 1.0), fontsize=10, arrowprops=dict(arrowstyle="-", color=INK, lw=1))
ax.text(6.5, 6.3, "같은 물인데 얼음은 왜 뜰까?", ha="center", va="center", fontsize=12, color=RED, fontweight="bold")
save(fig, "m06-cup.svg")

# 2. 이 편의 지도
fig, ax = canvas(11.6, 2.9, 19.4, 4.6)
titles = ["같은 크기에 얼마나 무거울까", "물보다 가벼우면 떠요", "물은 얼면 듬성듬성", "얼음은 조금 가벼워요"]
for i, t in enumerate(titles):
    x = 0.3 + i * 4.8
    box(ax, x, 0.4, 3.8, 3.6)
    ax.text(x + 1.9, 0.95, t, ha="center", va="center", fontsize=9.5, fontweight="bold")
    cx = x + 1.9
    if i == 0:
        for bx, n in [(cx - 1.4, 9), (cx + 0.2, 3)]:
            ax.add_patch(Rectangle((bx, 1.7), 1.2, 1.2, fc="white", ec=INK, lw=1))
            for k in range(n):
                particle(ax, bx + 0.25 + (k % 3) * 0.35 + (0.1 if n < 9 else 0), 1.95 + (k // 3) * 0.35 + (0.3 if n < 9 else 0), r=0.12)
    elif i in (1, 3):
        ax.add_patch(Rectangle((cx - 1.4, 1.6), 2.8, 1.6, fc="#cfe3f3", ec=INK, lw=1))
        if i == 1:
            ax.add_patch(Rectangle((cx - 1.1, 3.0), 1.2, 0.35, fc=WOOD, ec=INK, lw=1))
            ax.add_patch(Ellipse((cx + 0.7, 1.8), 0.5, 0.3, fc=STONE, ec=INK, lw=1))
        else:
            ax.add_patch(Rectangle((cx - 0.5, 2.6), 1.0, 0.75, fc=ICE, ec=INK, lw=1))
    else:
        hx = [(cx + 0.55 * math.cos(math.radians(90 + 60 * k)), 2.5 + 0.55 * math.sin(math.radians(90 + 60 * k))) for k in range(7)]
        ax.plot([p[0] for p in hx], [p[1] for p in hx], color=INK, lw=1.2, zorder=3)
        for p in hx[:6]:
            ax.add_patch(Circle(p, 0.15, fc=WATER, ec=INK, lw=0.7, zorder=4))
    if i < 3:
        arrow(ax, (x + 3.95, 2.2), (x + 4.65, 2.2))
save(fig, "m06-map.svg")

# 3. 같은 크기 상자
fig, ax = canvas(9.0, 4.0, 15.0, 6.6)
for x, dense, lab in [(1.2, True, "빽빽해요: 무거워요"), (8.6, False, "듬성듬성해요: 가벼워요")]:
    ax.add_patch(Rectangle((x, 1.4), 4.4, 4.4, fc="white", ec=INK, lw=1.6))
    if dense:
        for i in range(8):
            for j in range(8):
                particle(ax, x + 0.4 + j * 0.51 + (0.2 if i % 2 else 0) * 0.5, 1.75 + i * 0.51, r=0.22, fc=STONE)
    else:
        for (dx, dy) in [(0.8, 1.0), (2.4, 0.8), (3.6, 1.6), (1.4, 2.4), (3.0, 3.0), (0.9, 3.7), (2.2, 3.9), (3.7, 3.8)]:
            particle(ax, x + dx, 1.4 + dy, r=0.22, fc=STONE)
    ax.text(x + 2.2, 0.8, lab, ha="center", va="center", fontsize=11, fontweight="bold")
save(fig, "m06-boxes.svg")

# 4. 통나무와 조약돌
fig, ax = canvas(9.0, 4.0, 15.0, 6.6)
ax.add_patch(Rectangle((0.8, 0.6), 8.4, 4.4, fc="#cfe3f3", ec=INK, lw=1.4))
ax.add_patch(FancyBboxPatch((1.6, 4.55), 4.4, 0.7, boxstyle="round,pad=0.1", fc=WOOD, ec=INK, lw=1.2))
ax.add_patch(Ellipse((6.0, 4.9), 0.5, 0.8, fc="#e0c49e", ec=INK, lw=1.2))
ax.add_patch(Ellipse((7.4, 0.85), 0.5, 0.3, fc=STONE, ec=INK, lw=1.2))
ax.text(9.6, 5.0, "통나무: 같은 크기의\n물보다 가벼워요", ha="left", va="center", fontsize=10.5, fontweight="bold")
ax.text(9.6, 1.0, "돌멩이: 같은 크기의\n물보다 무거워요", ha="left", va="center", fontsize=10.5, fontweight="bold",
        color=RED)
save(fig, "m06-log.svg")

# 5. 물과 얼음 고리
fig, ax = canvas(10.0, 4.6, 16.0, 7.4)
pts, centers = honeycomb(9.5, 1.7, 4, 4, a=0.5)
n = len(pts)
box(ax, 0.6, 1.0, 6.2, 4.8, fc="#eef5fb")
ax.text(3.7, 0.4, "물: 바짝 모여 있어요", ha="center", va="center", fontsize=11, fontweight="bold")
placed = []
y = 1.35
while len(placed) < n and y < 5.6:
    x = 0.95 + random.uniform(0, 0.2)
    while x < 6.55 and len(placed) < n:
        placed.append((x + random.uniform(-0.05, 0.05), y + random.uniform(-0.05, 0.05)))
        x += 0.44
    y += 0.42
for p in placed:
    particle(ax, *p, r=0.19)
box(ax, 8.9, 1.0, 6.2, 4.8, fc="#eef5fb")
for i, p in enumerate(pts):
    for q in pts[i + 1:]:
        if (p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2 < (0.5 * 1.05) ** 2:
            ax.plot([p[0], q[0]], [p[1], q[1]], color=INK, lw=1.2, zorder=3)
for p in pts:
    ax.add_patch(Circle(p, 0.19, fc=WATER, ec=INK, lw=0.7, zorder=4))
cx, cy = centers[9]
ax.annotate("빈 자리", (cx, cy), (cx + 0.3, 6.5), fontsize=10, color=RED, fontweight="bold", ha="center",
            arrowprops=dict(arrowstyle="-", color=RED, lw=1))
ax.text(12.0, 0.4, "얼음: 여섯씩 이어진 고리", ha="center", va="center", fontsize=11, fontweight="bold")
ax.text(5.0, 7.0, "같은 수의 알갱이가 얼음이 되면 자리를 더 차지해요", ha="center", va="center", fontsize=10)
save(fig, "m06-rings.svg")

# 6. 가득 채워 얼리면
fig, ax = canvas(9.0, 3.8, 15.0, 6.2)
cup(ax, 1.0, 0.6, 3.2, 3.8)
ax.add_patch(Polygon([(1.14, 3.7), (4.06, 3.7), (3.95, 0.65), (1.25, 0.65)], closed=True, fc="#cfe3f3", ec="none"))
ax.plot([0.8, 4.4], [3.7, 3.7], color=RED, lw=1.2, ls="--")
arrow(ax, (5.0, 2.4), (7.0, 2.4))
ax.text(6.0, 3.0, "냉동실에서 얼리면", ha="center", va="center", fontsize=9)
cup(ax, 7.8, 0.6, 3.2, 3.8)
ax.add_patch(Polygon([(7.89, 4.05), (10.91, 4.05), (10.75, 0.65), (8.05, 0.65)], closed=True, fc=ICE, ec="none"))
ax.plot([7.6, 11.2], [3.7, 3.7], color=RED, lw=1.2, ls="--")
ax.text(11.6, 4.2, "얼면 높이가\n올라가요", ha="left", va="center", fontsize=11, color=RED, fontweight="bold")
save(fig, "m06-freeze.svg")

# 7. 저울: 같은 크기의 물과 대어 보기
def scale(ax, y, left_fc, tilt, lab, col):
    ax.add_patch(Polygon([(4.6, y), (5.4, y), (5.0, y + 1.0)], closed=True, fc=GREY, ec=INK, lw=1))
    lx, rx = 2.6, 7.4
    ly, ry = y + 1.0 + tilt, y + 1.0 - tilt
    ax.plot([lx, rx], [ly, ry], color=INK, lw=2)
    for x, yy in [(lx, ly), (rx, ry)]:
        ax.plot([x - 0.9, x + 0.9], [yy - 0.05, yy - 0.05], color=INK, lw=2)
    ax.add_patch(Rectangle((lx - 0.5, ly), 1.0, 1.0, fc=left_fc, ec=INK, lw=1.2))
    ax.add_patch(Rectangle((rx - 0.5, ry), 1.0, 1.0, fc="white", ec=INK, lw=1.2))
    ax.add_patch(Rectangle((rx - 0.45, ry + 0.05), 0.9, 0.85, fc="#cfe3f3", ec="none"))
    ax.text(rx, ry - 0.45, "같은 크기의 물", ha="center", va="center", fontsize=9)
    ax.text(9.2, y + 1.3, lab, ha="left", va="center", fontsize=11, color=col, fontweight="bold")


fig, ax = canvas(9.0, 4.8, 15.0, 8.0)
scale(ax, 4.6, WOOD, 0.35, "나무가 가벼워요: 떠요", INK)
scale(ax, 0.6, STONE, -0.35, "돌멩이가 무거워요: 가라앉아요", RED)
save(fig, "m06-scale.svg")
