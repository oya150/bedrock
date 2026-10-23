"""물질과 에너지 11편 그림 만들기. 실행: python lab/fig_m11.py  → docs/matter/img/11/*.svg

글자는 SVG 안에 글자로 남긴다(글꼴 모양을 파일에 넣지 않는다). 보는 쪽 글꼴로 그려진다.
카드는 차분한 색으로, 강조(새로 받은 카드, 비교 화살표, 많이 든 일)만 빨강으로 칠한다.
"""
import itertools
import os

import matplotlib

matplotlib.use("svg")
import matplotlib.pyplot as plt
from matplotlib.patches import Arc, Circle, FancyArrowPatch, FancyBboxPatch, Rectangle

OUT = os.path.join(os.path.dirname(__file__), "..", "docs", "matter", "img", "11")
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


ELEC = "#3b7dd8"
COPPER = "#d08a4a"
WIRE = "#c0504d"


def battery(ax, x, y, w=2.4, h=1.0):
    ax.add_patch(Rectangle((x, y), w, h, fc="#4a4a4a", ec=INK, lw=1.2))
    ax.add_patch(Rectangle((x + w * 0.7, y), w * 0.3, h, fc="#f2c12e", ec=INK, lw=1.2))
    ax.add_patch(Rectangle((x + w, y + h * 0.3), 0.15, h * 0.4, fc=GREY, ec=INK, lw=1))
    ax.text(x + w * 0.85, y + h / 2, "+", ha="center", va="center", fontsize=11, fontweight="bold")
    ax.text(x + w * 0.25, y + h / 2, "−", ha="center", va="center", fontsize=11, color="white", fontweight="bold")


def bulb(ax, x, y, on=True, s=1.0):
    ax.add_patch(Circle((x, y + 0.75 * s), 0.55 * s, fc=YEL if on else "#f4f4f4", ec=INK, lw=1.2))
    ax.add_patch(Rectangle((x - 0.3 * s, y), 0.6 * s, 0.3 * s, fc=GREY, ec=INK, lw=1))
    xs = [x - 0.2 * s + 0.4 * s * t / 20 for t in range(21)]
    ys = [y + 0.75 * s + 0.08 * s * math.sin(t * 1.5) for t in range(21)]
    ax.plot(xs, ys, color=INK, lw=0.8)
    if on:
        for a in range(30, 151, 30):
            t = math.radians(a)
            ax.plot([x + 0.7 * s * math.cos(t), x + 0.95 * s * math.cos(t)],
                    [y + 0.75 * s + 0.7 * s * math.sin(t), y + 0.75 * s + 0.95 * s * math.sin(t)], color=INK, lw=1)


def wire(ax, pts, color=WIRE, lw=2.2):
    ax.plot([p[0] for p in pts], [p[1] for p in pts], color=color, lw=lw, solid_joinstyle="round")


# 1. 여는 장면
fig, ax = canvas(10.0, 4.0, 16.0, 6.4)
for x0, on in [(0.8, True), (8.8, False)]:
    battery(ax, x0 + 1.2, 0.8)
    bulb(ax, x0 + 2.4, 3.2, on)
    wire(ax, [(x0 + 1.2, 1.3), (x0 + 0.6, 1.3), (x0 + 0.6, 3.35), (x0 + 2.15, 3.35)])
    if on:
        wire(ax, [(x0 + 3.75, 1.3), (x0 + 4.3, 1.3), (x0 + 4.3, 3.35), (x0 + 2.65, 3.35)])
    else:
        wire(ax, [(x0 + 4.0, 1.9), (x0 + 4.3, 2.0), (x0 + 4.3, 3.35), (x0 + 2.65, 3.35)])
        ax.text(x0 + 4.9, 1.4, "떨어짐", ha="left", va="center", fontsize=9)
ax.text(8.0, 6.0, "왜 두 가닥이 다 이어져야 켜질까?", ha="center", va="center", fontsize=12, color=RED, fontweight="bold")
save(fig, "m11-bulb.svg")

# 2. 이 편의 지도
fig, ax = canvas(11.6, 2.9, 19.4, 4.6)
titles = ["원자 속 전기 알갱이", "한 바퀴 이어진 길", "전구가 빛나는 까닭", "잘 흐르는 것 안 흐르는 것"]
for i, t in enumerate(titles):
    x = 0.3 + i * 4.8
    box(ax, x, 0.4, 3.8, 3.6)
    ax.text(x + 1.9, 0.95, t, ha="center", va="center", fontsize=9.5, fontweight="bold")
    cx = x + 1.9
    if i == 0:
        ax.add_patch(Circle((cx, 2.6), 0.85, fc="white", ec=INK, lw=1))
        ax.add_patch(Circle((cx, 2.6), 0.18, fc=GREY, ec=INK, lw=0.8))
        for a in range(0, 360, 72):
            t = math.radians(a)
            ax.add_patch(Circle((cx + 0.6 * math.cos(t), 2.6 + 0.6 * math.sin(t)), 0.07, fc=ELEC, ec="none"))
    elif i == 1:
        wire(ax, [(cx - 1.2, 1.7), (cx + 1.2, 1.7), (cx + 1.2, 3.4), (cx - 1.2, 3.4), (cx - 1.2, 1.7)], lw=1.6)
        ax.add_patch(Rectangle((cx - 0.5, 1.5), 1.0, 0.4, fc="#4a4a4a", ec=INK, lw=1))
        ax.add_patch(Circle((cx, 3.4), 0.25, fc=YEL, ec=INK, lw=1))
    elif i == 2:
        bulb(ax, cx, 1.6, True, 1.1)
    else:
        ax.add_patch(Rectangle((cx - 1.3, 2.4), 1.0, 0.25, fc=GREY, ec=INK, lw=1))
        ax.add_patch(Rectangle((cx + 0.3, 2.2), 0.9, 0.6, fc="#f3c6cf", ec=INK, lw=1))
    if i < 3:
        arrow(ax, (x + 3.95, 2.2), (x + 4.65, 2.2))
save(fig, "m11-map.svg")

# 3. 원자 속 전기 알갱이 / 금속 속
fig, ax = canvas(10.0, 4.4, 16.0, 7.0)
ax.add_patch(Circle((3.0, 3.6), 2.0, fc="white", ec=INK, lw=1.4))
ax.add_patch(Circle((3.0, 3.6), 0.35, fc=GREY, ec=INK, lw=1))
for a in range(0, 360, 45):
    t = math.radians(a)
    ax.add_patch(Circle((3.0 + 1.4 * math.cos(t), 3.6 + 1.4 * math.sin(t)), 0.1, fc=ELEC, ec="none"))
ax.text(3.0, 1.0, "원자 속 전기 알갱이", ha="center", va="center", fontsize=10.5, fontweight="bold")
ax.add_patch(FancyBboxPatch((7.2, 1.8), 7.8, 3.6, boxstyle="round,pad=0.1", fc="#f4e2d2", ec=COPPER, lw=2))
for i in range(4):
    for j in range(9):
        ax.add_patch(Circle((7.8 + j * 0.85, 2.3 + i * 0.85), 0.28, fc=COPPER, ec=INK, lw=0.6))
for k in range(18):
    ax.add_patch(Circle((8.225 + random.randrange(8) * 0.85, 2.725 + random.randrange(3) * 0.85), 0.1, fc=ELEC, ec="none"))
ax.text(11.1, 1.0, "금속 속에서는 전기 알갱이가\n원자 사이를 돌아다녀요", ha="center", va="center", fontsize=10.5, fontweight="bold")
ax.text(8.0, 6.6, "크기는 실제와 맞추지 않았어요", ha="center", va="center", fontsize=9)
save(fig, "m11-electron.svg")

# 4. 한 바퀴 이어진 길
fig, ax = canvas(10.0, 5.0, 16.0, 8.0)
loop = [(1.0, 3.0), (9.0, 3.0), (9.0, 7.0), (1.0, 7.0), (1.0, 3.0)]
ax.plot([q[0] for q in loop], [q[1] for q in loop], color="#e8a7a5", lw=3, zorder=0)
battery(ax, 3.8, 2.5)
bulb(ax, 5.0, 6.6, True, 0.9)
for k in range(28):
    t = k / 28
    per = 2 * (8.0 + 4.0)
    d = t * per
    if d < 8.0:
        p = (1.0 + d, 3.0)
    elif d < 12.0:
        p = (9.0, 3.0 + (d - 8.0))
    elif d < 20.0:
        p = (9.0 - (d - 12.0), 7.0)
    else:
        p = (1.0, 7.0 - (d - 20.0))
    if 3.6 < p[0] < 6.4 and abs(p[1] - 3.0) < 0.1:
        continue
    if 4.3 < p[0] < 5.7 and abs(p[1] - 7.0) < 0.1:
        continue
    ax.add_patch(Circle(p, 0.15, fc=ELEC, ec=INK, lw=0.4, zorder=5))
arrow(ax, (9.6, 5.8), (9.6, 4.2), color=RED, lw=2)
arrow(ax, (6.0, 7.5), (8.4, 7.5), color=RED, lw=2)
arrow(ax, (0.4, 4.2), (0.4, 5.8), color=RED, lw=2)
ax.text(12.6, 5.6, "한 바퀴 이어지면\n전기 알갱이가\n함께 흘러요", ha="center", va="center", fontsize=10.5, color=RED, fontweight="bold")
wire(ax, [(10.8, 1.2), (12.3, 1.2)], lw=2)
wire(ax, [(12.8, 1.4), (14.4, 1.2)], lw=2)
for k in range(5):
    ax.add_patch(Circle((11.0 + k * 0.28, 1.2), 0.07, fc=ELEC, ec="none", zorder=5))
    ax.add_patch(Circle((13.0 + k * 0.28, 1.38 - k * 0.025), 0.07, fc=ELEC, ec="none", zorder=5))
ax.text(5.1, 1.9, "건전지", ha="center", va="center", fontsize=10)
ax.text(3.9, 7.5, "꼬마전구", ha="center", va="center", fontsize=10)
ax.text(1.6, 5.0, "전선", ha="left", va="center", fontsize=10)
ax.text(12.6, 0.4, "끊기면 멈춰요", ha="center", va="center", fontsize=10.5, fontweight="bold")
save(fig, "m11-loop.svg")

# 5. 전구가 빛나는 까닭
fig, ax = canvas(10.0, 4.6, 16.0, 7.4)
bulb(ax, 3.5, 1.0, True, 3.0)
for a in range(20, 161, 35):
    t = math.radians(a)
    ax.plot([3.5 + 2.2 * math.cos(t) + 0.08 * math.sin(k) for k in range(1)], [3.25], color=RED)
ax.plot([3.8, 9.4], [3.25, 3.8], color=RED, lw=1, ls="--")
ax.add_patch(Circle((11.6, 4.0), 2.3, fc="#fff3d6", ec=RED, lw=2))
for i in range(3):
    for j in range(4):
        ax.add_patch(Circle((10.4 + j * 0.8, 3.2 + i * 0.8), 0.25, fc=GREY, ec=INK, lw=0.6))
for (x, y) in [(10.0, 4.4), (11.2, 3.6), (12.0, 4.4), (12.8, 3.6)]:
    ax.add_patch(Circle((x, y), 0.1, fc=ELEC, ec="none"))
    arrow(ax, (x - 0.5, y + 0.05), (x - 0.12, y), color=ELEC, lw=1.2, ms=8)
ax.annotate("원자", (10.4, 4.8), (9.0, 6.6), fontsize=10, arrowprops=dict(arrowstyle="-", color=INK, lw=1))
ax.annotate("전기 알갱이", (12.0, 4.4), (12.6, 6.6), fontsize=10, arrowprops=dict(arrowstyle="-", color=INK, lw=1))
ax.text(11.6, 1.0, "가는 선을 지나며 부딪혀 뜨거워져요\n아주 뜨거워지면 빛나요", ha="center", va="center", fontsize=10.5,
        color=RED, fontweight="bold")
save(fig, "m11-glow.svg")

# 6. 잘 흐르는 것 안 흐르는 것
fig, ax = canvas(10.0, 4.6, 16.0, 7.4)
ax.add_patch(FancyBboxPatch((0.8, 5.4), 1.6, 0.6, boxstyle="round,pad=0.2", fc="none", ec=GREY, lw=3))
ax.add_patch(Ellipse((4.0, 5.7), 1.6, 0.8, fc=GREY, ec=INK, lw=1)); ax.plot([4.8, 6.4], [5.7, 5.7], color=GREY, lw=4)
ax.add_patch(Rectangle((7.2, 5.3), 1.8, 0.9, fc="#dfe3e6", ec=INK, lw=1))
for (x, lab) in [(1.6, "클립"), (4.6, "숟가락"), (8.1, "알루미늄 포일")]:
    ax.text(x, 4.8, lab, ha="center", va="center", fontsize=9)
for (x, lab) in [(1.6, "지우개"), (4.7, "플라스틱 자"), (8.1, "나무젓가락")]:
    ax.text(x, 2.7, lab, ha="center", va="center", fontsize=9)
ax.text(10.0, 5.7, "전기가 잘 흘러요", ha="left", va="center", fontsize=11, fontweight="bold", color=RED)
ax.add_patch(FancyBboxPatch((0.8, 3.2), 1.6, 0.8, boxstyle="round,pad=0.1", fc="#f3c6cf", ec=INK, lw=1))
ax.add_patch(Rectangle((3.2, 3.4), 3.0, 0.4, fc="#cde8f7", ec=INK, lw=1))
ax.add_patch(Rectangle((7.2, 3.5), 1.8, 0.25, fc="#c8a27a", ec=INK, lw=1))
ax.text(10.0, 3.6, "전기가 거의 안 흘러요", ha="left", va="center", fontsize=11, fontweight="bold")
ax.add_patch(Circle((5.0, 1.2), 0.8, fc="#2c8a3a", ec=INK, lw=1.2))
ax.add_patch(Circle((5.0, 1.2), 0.35, fc=COPPER, ec=INK, lw=1))
ax.annotate("구리 선", (5.1, 1.3), (7.0, 1.6), fontsize=10, arrowprops=dict(arrowstyle="-", color=INK, lw=1))
ax.annotate("플라스틱 껍질", (5.6, 0.7), (7.0, 0.6), fontsize=10, arrowprops=dict(arrowstyle="-", color=INK, lw=1))
ax.text(2.6, 1.2, "전선을 자른 모습", ha="center", va="center", fontsize=10)
save(fig, "m11-conduct.svg")
