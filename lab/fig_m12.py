"""물질과 에너지 12편 그림 만들기. 실행: python lab/fig_m12.py  → docs/matter/img/12/*.svg

글자는 SVG 안에 글자로 남긴다(글꼴 모양을 파일에 넣지 않는다). 보는 쪽 글꼴로 그려진다.
카드는 차분한 색으로, 강조(새로 받은 카드, 비교 화살표, 많이 든 일)만 빨강으로 칠한다.
"""
import itertools
import os

import matplotlib

matplotlib.use("svg")
import matplotlib.pyplot as plt
from matplotlib.patches import Arc, Circle, FancyArrowPatch, FancyBboxPatch, Rectangle

OUT = os.path.join(os.path.dirname(__file__), "..", "docs", "matter", "img", "12")
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


NCOL, SCOL = "#e4572e", "#3b7dd8"
STEEL = "#9aa3ad"


def magnet(ax, x, y, w=3.0, h=0.8, flip=False, label=True):
    left, right = (SCOL, NCOL) if not flip else (NCOL, SCOL)
    ax.add_patch(Rectangle((x, y), w / 2, h, fc=left, ec=INK, lw=1.2))
    ax.add_patch(Rectangle((x + w / 2, y), w / 2, h, fc=right, ec=INK, lw=1.2))
    if label:
        ax.text(x + w * 0.15, y + h / 2, "S" if not flip else "N", ha="center", va="center", fontsize=11, color="white",
                fontweight="bold")
        ax.text(x + w * 0.85, y + h / 2, "N" if not flip else "S", ha="center", va="center", fontsize=11, color="white",
                fontweight="bold")


def clip(ax, x, y, s=1.0, ang=0):
    ax.add_patch(FancyBboxPatch((x - 0.15 * s, y - 0.45 * s), 0.3 * s, 0.9 * s, boxstyle="round,pad=0.08",
                                fc="none", ec=STEEL, lw=2.4))


def tiny(ax, x, y, ang, L=0.45, color=INK):
    dx, dy = L / 2 * math.cos(ang), L / 2 * math.sin(ang)
    ax.add_patch(FancyArrowPatch((x - dx, y - dy), (x + dx, y + dy), arrowstyle="-|>", mutation_scale=9, color=color, lw=1.4))


# 1. 여는 장면
fig, ax = canvas(9.0, 4.2, 15.0, 7.0)
ax.add_patch(Rectangle((0.8, 0.6), 4.6, 5.6, fc="#eef1f4", ec=INK, lw=1.4))
ax.add_patch(Rectangle((1.6, 2.4), 2.6, 2.4, fc="white", ec=INK, lw=1))
ax.plot([1.9, 3.9], [3.2, 3.2], color=GREY, lw=1); ax.plot([1.9, 3.5], [3.6, 3.6], color=GREY, lw=1)
ax.add_patch(Circle((2.9, 4.6), 0.35, fc=NCOL, ec=INK, lw=1))
ax.text(3.1, 0.2, "냉장고 문", ha="center", va="center", fontsize=10)
magnet(ax, 7.6, 4.4, 3.4, 0.8, label=True)
for k in range(3):
    clip(ax, 11.4, 4.3 - k * 1.0)
ax.text(7.5, 6.6, "손을 대지 않았는데 어떻게 끌어당길까?", ha="center", va="center", fontsize=12, color=RED, fontweight="bold")
save(fig, "m12-fridge.svg")

# 2. 이 편의 지도
fig, ax = canvas(11.6, 2.9, 19.4, 4.6)
titles = ["붙는 것과 안 붙는 것", "밀고 당기는 두 극", "쇠 속 작은 자석들", "보이지 않는 힘"]
for i, t in enumerate(titles):
    x = 0.3 + i * 4.8
    box(ax, x, 0.4, 3.8, 3.6)
    ax.text(x + 1.9, 0.95, t, ha="center", va="center", fontsize=10, fontweight="bold")
    cx = x + 1.9
    if i == 0:
        clip(ax, cx - 0.8, 2.6, 0.9)
        ax.add_patch(FancyBboxPatch((cx + 0.2, 2.3), 0.9, 0.55, boxstyle="round,pad=0.08", fc="#f3c6cf", ec=INK, lw=1))
    elif i == 1:
        magnet(ax, cx - 1.6, 2.4, 1.4, 0.45, label=False)
        magnet(ax, cx + 0.2, 2.4, 1.4, 0.45, label=False)
    elif i == 3:
        magnet(ax, cx - 0.7, 2.4, 1.4, 0.4, label=False)
        for k, hgt in enumerate((0.5, 0.9)):
            ax.add_patch(Arc((cx, 2.6), 2.2 + k * 0.6, 2 * hgt, theta1=0, theta2=180, color=INK, lw=1))
    else:
        for k in range(8):
            tiny(ax, cx - 1.2 + (k % 4) * 0.8, 2.3 + (k // 4) * 0.7, 0.0)
    if i < 3:
        arrow(ax, (x + 3.95, 2.2), (x + 4.65, 2.2))
save(fig, "m12-map.svg")

# 3. 붙는 것과 안 붙는 것
fig, ax = canvas(10.0, 4.4, 16.0, 7.0)
magnet(ax, 0.6, 4.8, 2.6, 0.7)
clip(ax, 3.45, 5.15, 0.8)
ax.plot([4.6, 6.2], [5.15, 5.15], color=STEEL, lw=3); ax.add_patch(Rectangle((4.5, 4.95), 0.15, 0.4, fc=STEEL, ec=INK, lw=0.8))
ax.add_patch(Rectangle((6.8, 4.6), 1.6, 1.1, fc="#eef1f4", ec=INK, lw=1))
ax.text(3.45, 4.2, "클립", ha="center", va="center", fontsize=9); ax.text(5.6, 4.6, "쇠못", ha="center", va="center", fontsize=9)
ax.text(7.6, 4.2, "냉장고 문 조각", ha="center", va="center", fontsize=9)
ax.text(9.2, 5.2, "붙어요", ha="left", va="center", fontsize=11, color=RED, fontweight="bold")
magnet(ax, 0.6, 1.6, 2.6, 0.7)
ax.add_patch(Rectangle((4.0, 1.2), 0.8, 1.4, fc="#d6dde3", ec=INK, lw=1))
ax.add_patch(Circle((5.8, 1.9), 0.4, fc="#c9a96e", ec=INK, lw=1))
ax.add_patch(FancyBboxPatch((6.8, 1.6), 0.9, 0.55, boxstyle="round,pad=0.08", fc="#f3c6cf", ec=INK, lw=1))
ax.add_patch(Rectangle((8.2, 1.8), 1.6, 0.18, fc="#c8a27a", ec=INK, lw=1))
for (x, lab) in [(4.4, "알루미늄 캔"), (5.8, "동전"), (7.25, "지우개"), (9.0, "나무젓가락")]:
    ax.text(x, 0.6, lab, ha="center", va="center", fontsize=9)
ax.text(10.4, 1.9, "안 붙어요", ha="left", va="center", fontsize=11, fontweight="bold")
save(fig, "m12-stick.svg")

# 4. 두 극
fig, ax = canvas(10.0, 3.8, 16.0, 6.2)
magnet(ax, 0.8, 4.0, 3.0, 0.8)
magnet(ax, 5.6, 4.0, 3.0, 0.8)
arrow(ax, (4.0, 4.4), (4.6, 4.4), color=INK, lw=1.6); arrow(ax, (5.4, 4.4), (4.8, 4.4), color=INK, lw=1.6)
ax.text(9.4, 4.4, "다른 극끼리 당겨요", ha="left", va="center", fontsize=11, color=RED, fontweight="bold")
magnet(ax, 0.8, 1.2, 3.0, 0.8)
magnet(ax, 5.6, 1.2, 3.0, 0.8, flip=True)
arrow(ax, (4.4, 1.6), (3.9, 1.6), color=INK, lw=1.6); arrow(ax, (4.8, 1.6), (5.3, 1.6), color=INK, lw=1.6)
ax.text(9.4, 1.6, "같은 극끼리 밀어요", ha="left", va="center", fontsize=11, fontweight="bold")
save(fig, "m12-poles.svg")

# 5. 보이지 않는 힘: 철가루 무늬
fig, ax = canvas(10.0, 4.6, 16.0, 7.4)
ax.add_patch(Rectangle((0.6, 0.4), 11.4, 6.6, fc="#fbfaf6", ec=GREY, lw=1))
magnet(ax, 4.8, 3.3, 3.0, 0.8)
pS, pN = (4.95, 3.7), (7.65, 3.7)
qN, qS = (7.35, 3.7), (5.25, 3.7)


def fld(x, y):
    ex = ey = 0.0
    for (qx, qy), q in ((qN, 1), (qS, -1)):
        dx, dy = x - qx, y - qy
        r3 = (dx * dx + dy * dy) ** 1.5 + 1e-9
        ex += q * dx / r3; ey += q * dy / r3
    return ex, ey


for a0 in range(-165, 166, 22):
    t = math.radians(a0)
    x, y = qN[0] + 0.3 * math.cos(t), qN[1] + 0.3 * math.sin(t)
    pts = [(x, y)]
    for _ in range(4000):
        ex, ey = fld(x, y)
        n = math.hypot(ex, ey)
        x += 0.02 * ex / n; y += 0.02 * ey / n
        pts.append((x, y))
        if math.hypot(x - qS[0], y - qS[1]) < 0.25 or not (0.7 < x < 11.9 and 0.5 < y < 6.9):
            break
    for k in range(0, len(pts) - 6, 12):
        (x1, y1), (x2, y2) = pts[k], pts[k + 6]
        if not (4.8 < x1 < 7.8 and abs(y1 - 3.7) < 0.42):
            ax.plot([x1, x2], [y1, y2], color=INK, lw=1.1)
            if x1 > 7.8 or x2 > 7.8:
                ax.plot([12.6 - x1, 12.6 - x2], [y1, y2], color=INK, lw=1.1)
ax.annotate("여기가 가장 세요", (pN[0] + 0.6, 3.2), (10.0, 1.2), fontsize=10, color=RED, fontweight="bold",
            arrowprops=dict(arrowstyle="-", color=RED, lw=1))
ax.text(6.3, 7.4, "자석 둘레에 힘이 퍼져 있어요", ha="center", va="center", fontsize=11, color=RED, fontweight="bold")
save(fig, "m12-field.svg")

# 6. 쇠 속 작은 자석들
fig, ax = canvas(10.0, 4.2, 16.0, 6.8)
box(ax, 0.6, 1.4, 5.6, 4.2, fc="#eef1f4")
groups = [(0, 0, 0.3), (0, 1, 2.0), (1, 0, 3.6), (1, 1, 5.0)]
for gi, gj, ang in groups:
    gx, gy = 1.0 + gi * 2.6, 1.8 + gj * 1.9
    ax.add_patch(Rectangle((gx - 0.1, gy - 0.15), 2.4, 1.7, fc="none", ec=GREY, lw=1, ls="--"))
    for i in range(2):
        for j in range(3):
            tiny(ax, gx + 0.4 + j * 0.75, gy + 0.35 + i * 0.75, ang)
ax.text(3.4, 0.8, "자석이 멀리 있을 때", ha="center", va="center", fontsize=10.5, fontweight="bold")
arrow(ax, (6.6, 3.5), (8.0, 3.5))
magnet(ax, 8.4, 3.1, 2.0, 0.8, flip=True)
box(ax, 10.8, 1.4, 4.8, 4.2, fc="#eef1f4")
for i in range(4):
    for j in range(6):
        tiny(ax, 11.25 + j * 0.75, 1.95 + i * 0.95, math.pi, color=RED)
ax.text(13.2, 0.8, "자석이 가까이 오면", ha="center", va="center", fontsize=10.5, fontweight="bold", color=RED)
ax.text(8.0, 6.4, "크기는 실제와 맞추지 않았어요", ha="center", va="center", fontsize=9)
save(fig, "m12-domains.svg")

# 7. 지구와 나침반, 전기
fig, ax = canvas(10.0, 4.6, 16.0, 7.4)
ax.add_patch(Circle((4.0, 4.0), 1.6, fc="#bfe0c8", ec=INK, lw=1.4))
for a_ in (0.9, 1.4, 1.9):
    for d in (-1, 1):
        ax.add_patch(Ellipse((4.0 + d * a_, 4.0), 2 * a_, 2.0 + a_ * 2.2, fc="none", ec=INK, lw=1, ls=(0, (1, 2))))
ax.add_patch(Circle((4.0, 4.0), 1.6, fc="#bfe0c8", ec=INK, lw=1.4, zorder=3))
ax.text(4.0, 7.2, "북쪽", ha="center", va="center", fontsize=10)
ax.add_patch(Circle((8.8, 4.6), 0.9, fc="white", ec=INK, lw=1.4))
ax.add_patch(Polygon([(8.8, 5.35), (8.65, 4.6), (8.95, 4.6)], closed=True, fc=NCOL, ec=INK, lw=0.6))
ax.add_patch(Polygon([(8.8, 3.85), (8.65, 4.6), (8.95, 4.6)], closed=True, fc=SCOL, ec=INK, lw=0.6))
ax.text(8.8, 3.3, "나침반", ha="center", va="center", fontsize=10)
ax.text(9.2, 5.3, "N", ha="left", va="center", fontsize=10, color=NCOL, fontweight="bold")
ax.plot([10.6, 15.4], [1.6, 1.6], color="#c0504d", lw=3)
arrow(ax, (11.0, 2.0), (12.6, 2.0), color=SCOL, lw=1.4)
ax.add_patch(Circle((13.6, 1.6), 0.6, fc="white", ec=INK, lw=1.2, zorder=4))
ax.add_patch(Polygon([(13.15, 1.95), (13.6, 1.55), (13.6, 1.75)], closed=True, fc=NCOL, ec=INK, lw=0.5, zorder=5))
ax.add_patch(Polygon([(14.05, 1.25), (13.6, 1.55), (13.6, 1.75)], closed=True, fc=SCOL, ec=INK, lw=0.5, zorder=5))
ax.text(13.0, 0.5, "전기가 흐르면 자석의 힘이 생겨요", ha="center", va="center", fontsize=10.5, color=RED, fontweight="bold")
save(fig, "m12-earth.svg")
