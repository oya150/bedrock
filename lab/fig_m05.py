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


SALT = "#f7f7f2"


def salt(ax, x, y, r=0.22):
    ax.add_patch(Circle((x, y), r, fc=SALT, ec=RED, lw=1.2))


def hydrated(ax, x, y, r=0.22, n=6, rw=0.17):
    salt(ax, x, y, r)
    for k in range(n):
        a = 2 * math.pi * k / n + 0.3
        particle(ax, x + (r + rw + 0.02) * math.cos(a), y + (r + rw + 0.02) * math.sin(a), r=rw)


def pile(ax, cx, y, w, h):
    ax.add_patch(Polygon([(cx - w / 2, y), (cx + w / 2, y), (cx + w / 6, y + h), (cx - w / 6, y + h)], closed=True,
                         fc=SALT, ec=INK, lw=1))


# 1. 여는 장면
fig, ax = canvas(9.0, 4.2, 15.0, 7.0)
cup(ax, 1.0, 0.8, 3.6, 3.6)
ax.add_patch(FancyBboxPatch((2.4, 5.2), 2.6, 0.35, boxstyle="round,pad=0.08", fc=GREY, ec=INK, lw=1, mutation_aspect=1))
for k in range(10):
    ax.add_patch(Circle((2.7 + random.uniform(-0.2, 0.3), 4.5 + random.uniform(0, 0.7)), 0.06, fc=SALT, ec=INK, lw=0.5))
pile(ax, 2.8, 0.85, 1.4, 0.35)
arrow(ax, (5.2, 2.6), (7.0, 2.6))
ax.text(6.1, 3.1, "저으면", ha="center", va="center", fontsize=9)
cup(ax, 7.6, 0.8, 3.6, 3.6)
ax.text(11.6, 2.6, "맛을 보면\n짜요", ha="left", va="center", fontsize=11, fontweight="bold")
ax.text(7.5, 6.5, "소금은 어디로 갔을까?", ha="center", va="center", fontsize=12, color=RED, fontweight="bold")
save(fig, "m05-salt.svg")

# 2. 이 편의 지도
fig, ax = canvas(11.6, 2.9, 19.4, 4.6)
titles = ["물 알갱이가 끌어내요", "사라지지 않아요", "빨리 녹는 때", "녹는 데도 끝이 있어요"]
for i, t in enumerate(titles):
    x = 0.3 + i * 4.8
    box(ax, x, 0.4, 3.8, 3.6)
    ax.text(x + 1.9, 0.95, t, ha="center", va="center", fontsize=10.5, fontweight="bold")
    cx = x + 1.9
    if i == 0:
        for a in range(2):
            for b in range(2):
                salt(ax, cx - 1.0 + b * 0.36, 2.2 + a * 0.36, 0.16)
        hydrated(ax, cx + 0.6, 2.75, 0.16, 6, 0.12)
    elif i == 1:
        ax.add_patch(Ellipse((cx, 2.3), 2.6, 0.6, fc="white", ec=INK, lw=1))
        pile(ax, cx, 2.3, 1.4, 0.25)
        particle(ax, cx + 0.6, 3.2, r=0.13)
        arrow(ax, (cx + 0.65, 3.35), (cx + 0.9, 3.7), color=RED, lw=1.2, ms=8)
    elif i == 2:
        cup(ax, cx - 0.8, 1.6, 1.6, 1.6)
        ax.plot([cx + 0.1, cx + 0.9], [2.0, 3.6], color=INK, lw=2)
        ax.add_patch(Arc((cx - 0.05, 2.2), 1.0, 0.4, theta1=200, theta2=520, color=RED, lw=1.4))
    else:
        cup(ax, cx - 0.8, 1.6, 1.6, 1.6)
        pile(ax, cx, 1.65, 1.1, 0.3)
    if i < 3:
        arrow(ax, (x + 3.95, 2.2), (x + 4.65, 2.2))
save(fig, "m05-map.svg")

# 3. 물 알갱이가 떼어 내요
fig, ax = canvas(10.0, 5.0, 16.0, 7.8)
ax.add_patch(Rectangle((0.4, 0.6), 9.6, 6.0, fc="#eef5fb", ec=INK, lw=1.2))
for i in range(5):
    for j in range(5):
        if (i, j) == (4, 4):
            continue
        salt(ax, 1.2 + j * 0.5, 2.0 + i * 0.5)
hydrated(ax, 4.1, 4.4)
arrow(ax, (4.5, 4.75), (5.2, 5.3), color=INK, lw=1.2, ms=9)
hydrated(ax, 6.6, 2.6)
hydrated(ax, 8.4, 5.2)
for (x, y) in [(5.6, 1.4), (7.6, 1.2), (9.2, 3.4), (5.2, 6.0), (7.2, 4.0), (3.4, 6.0), (1.4, 5.6), (9.4, 1.4)]:
    particle(ax, x, y, r=0.17)
ax.text(5.2, 7.2, "크기와 거리는 실제와 맞추지 않았어요", ha="center", va="center", fontsize=9)
ax.annotate("물 알갱이", (5.45, 1.35), (3.6, 0.95), fontsize=10, fontweight="bold",
            arrowprops=dict(arrowstyle="-", color=INK, lw=1))
ax.annotate("소금 알갱이", (1.2, 1.8), (0.9, 0.95), fontsize=10, color=RED, fontweight="bold",
            arrowprops=dict(arrowstyle="-", color=RED, lw=1))
ax.text(10.4, 5.2, "물 알갱이가\n소금 알갱이를\n하나씩 둘러싸\n끌어내요", ha="left", va="center", fontsize=11, color=RED,
        fontweight="bold")
save(fig, "m05-pull.svg")

# 4. 말리면 소금이 남아요
fig, ax = canvas(10.0, 3.8, 16.0, 6.2)
ax.add_patch(Ellipse((2.8, 1.6), 4.4, 1.0, fc="white", ec=INK, lw=1.2))
ax.add_patch(Ellipse((2.8, 1.7), 3.6, 0.6, fc="#eef5fb", ec="none"))
ax.text(2.8, 0.6, "소금물", ha="center", va="center", fontsize=10)
arrow(ax, (5.4, 1.6), (7.4, 1.6))
ax.text(6.4, 2.1, "며칠 뒤", ha="center", va="center", fontsize=9)
ax.add_patch(Ellipse((10.4, 1.6), 4.4, 1.0, fc="white", ec=INK, lw=1.2))
for k in range(30):
    ax.add_patch(Circle((10.4 + random.uniform(-1.6, 1.6), 1.6 + random.uniform(-0.25, 0.25)), 0.06, fc=SALT, ec=INK,
                        lw=0.5))
for (x, y) in [(9.4, 3.2), (10.8, 3.8), (11.8, 2.9)]:
    particle(ax, x, y, r=0.18)
    arrow(ax, (x + 0.1, y + 0.2), (x + 0.45, y + 0.8), color=RED, lw=1.4, ms=9)
ax.text(10.4, 0.6, "하얀 소금", ha="center", va="center", fontsize=10)
ax.text(13.0, 4.8, "물 알갱이만 날아가고\n소금은 남아요", ha="left", va="center", fontsize=11, color=RED, fontweight="bold")
save(fig, "m05-dry.svg")

# 5. 빨리 녹는 때
fig, ax = canvas(11.0, 3.8, 18.0, 6.2)
for i, lab in enumerate(["저으면", "따뜻하면", "가루면"]):
    x = 0.3 + i * 6.0
    box(ax, x, 0.5, 5.4, 5.0, fc=NOTE)
    ax.text(x + 2.7, 1.0, lab, ha="center", va="center", fontsize=11, fontweight="bold")
    cx = x + 2.7
    if i == 0:
        cup(ax, cx - 1.3, 1.7, 2.6, 2.8)
        ax.plot([cx + 0.2, cx + 1.4], [2.2, 5.0], color=INK, lw=2.2)
        ax.add_patch(Arc((cx, 2.6), 1.8, 0.6, theta1=200, theta2=520, color=RED, lw=1.6))
    elif i == 1:
        cup(ax, cx - 1.3, 1.7, 2.6, 2.8, fc="#fbe9e3")
        for k in range(5):
            mover(ax, cx - 0.8 + k * 0.4, 2.4 + 0.5 * (k % 2), 0.55, r=0.13)
    else:
        ax.add_patch(Polygon([(x + 0.8, 2.0), (x + 2.2, 2.0), (x + 2.4, 3.2), (x + 1.0, 3.4)], closed=True, fc=SALT,
                             ec=INK, lw=1.2))
        ax.text(x + 1.6, 3.8, "덩어리", ha="center", va="center", fontsize=9)
        pile(ax, x + 4.0, 2.0, 1.8, 0.7)
        ax.text(x + 4.0, 3.2, "가루", ha="center", va="center", fontsize=9)
save(fig, "m05-fast.svg")

# 6. 녹는 데도 끝이 있어요
fig, ax = canvas(10.0, 3.8, 16.0, 6.2)
for i, (lab, heap) in enumerate([("한 숟가락: 맑아요", 0), ("여러 숟가락: 아직 맑아요", 0), ("더 넣으면: 바닥에 쌓여요", 1)]):
    x = 0.8 + i * 5.2
    cup(ax, x, 1.4, 3.2, 3.6, fc="white")
    ax.add_patch(Polygon([(x + 0.32, 1.42), (x + 2.88, 1.42), (x + 3.04, 3.2), (x + 0.16, 3.2)], closed=True, fc="#eef5fb", ec="none"))
    if heap:
        pile(ax, x + 1.6, 1.45, 2.2, 0.5)
    ax.text(x + 1.6, 0.8, lab, ha="center", va="center", fontsize=10, fontweight="bold",
            color=RED if heap else "#222")
save(fig, "m05-limit.svg")
