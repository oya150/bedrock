"""물질과 에너지 1편 그림 만들기. 실행: python lab/fig_m01.py  → docs/matter/img/01/*.svg

글자는 SVG 안에 글자로 남긴다(글꼴 모양을 파일에 넣지 않는다). 보는 쪽 글꼴로 그려진다.
카드는 차분한 색으로, 강조(새로 받은 카드, 비교 화살표, 많이 든 일)만 빨강으로 칠한다.
"""
import itertools
import os

import matplotlib

matplotlib.use("svg")
import matplotlib.pyplot as plt
from matplotlib.patches import Arc, Circle, FancyArrowPatch, FancyBboxPatch, Rectangle

OUT = os.path.join(os.path.dirname(__file__), "..", "docs", "matter", "img", "01")
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

random.seed(1)
SUGAR = "#f3f1ea"
ATOM = "#9aa3ad"
WATER = "#7da2c8"
DYE = "#e4572e"
SAND = "#e9d3a4"


def dots(ax, x0, y0, w, h, n, color=WATER, r=0.12, jitter=True):
    for k in range(n):
        ax.add_patch(Circle((x0 + random.uniform(0, w), y0 + random.uniform(0, h)), r, fc=color, ec=INK, lw=0.5))


def wiggle(ax, x, y, s=0.25, color=INK):
    for a in (20, 140, 260):
        r = math.radians(a)
        ax.plot([x + 0.18 * math.cos(r), x + (0.18 + s) * math.cos(r)], [y + 0.18 * math.sin(r), y + (0.18 + s) * math.sin(r)],
                color=color, lw=0.8)


# 1. 여는 장면: 각설탕 쪼개기
fig, ax = canvas(11.0, 4.0, 18.0, 6.6)
ax.add_patch(Rectangle((0.8, 1.6), 2.4, 2.4, fc=SUGAR, ec=INK, lw=1.6))
arrow(ax, (3.6, 2.8), (4.8, 2.8))
for k in range(4):
    ax.add_patch(Rectangle((5.2 + (k % 2) * 1.3, 1.6 + (k // 2) * 1.3), 1.1, 1.1, fc=SUGAR, ec=INK, lw=1.2))
arrow(ax, (8.0, 2.8), (9.2, 2.8))
for k in range(16):
    ax.add_patch(Rectangle((9.6 + (k % 4) * 0.55, 1.6 + (k // 4) * 0.55), 0.45, 0.45, fc=SUGAR, ec=INK, lw=0.8))
arrow(ax, (12.2, 2.8), (13.4, 2.8))
ax.add_patch(Circle((15.4, 2.8), 1.2, fc="white", ec=INK, lw=1.4, ls="--"))
ax.text(15.4, 2.8, "?", ha="center", va="center", fontsize=26, color=RED, fontweight="bold")
ax.text(9.0, 0.6, "쪼개고 또 쪼개면 마지막에는 무엇이 남을까?", ha="center", va="center", fontsize=12, color=RED,
        fontweight="bold")
ax.text(2.0, 4.6, "각설탕", ha="center", va="center", fontsize=11)
save(fig, "m01-split.svg")

# 2. 이 편의 지도
fig, ax = canvas(11.6, 2.9, 19.4, 4.6)
titles = ["멀리서 보면 매끈해도", "눈에 안 보이는 알갱이", "알갱이는 꿈틀거려요", "알갱이끼리 섞여요"]
for i, t in enumerate(titles):
    x = 0.3 + i * 4.8
    box(ax, x, 0.4, 3.8, 3.6)
    ax.text(x + 1.9, 0.95, t, ha="center", va="center", fontsize=11, fontweight="bold")
    cx = x + 1.9
    if i == 0:
        for k in range(3):
            ax.add_patch(Rectangle((x + 0.6 + k * 1.0, 2.0), 0.9 - k * 0.25, 0.9 - k * 0.25, fc=SUGAR, ec=INK, lw=1))
    elif i == 1:
        for k in range(9):
            ax.add_patch(Circle((cx - 0.6 + (k % 3) * 0.6, 2.0 + (k // 3) * 0.5), 0.18, fc=WATER, ec=INK, lw=0.6))
    elif i == 2:
        ax.add_patch(Circle((cx, 2.6), 0.3, fc=WATER, ec=INK, lw=0.8))
        wiggle(ax, cx, 2.6, s=0.35)
    else:
        for (dx, dy) in [(-0.9, 0.1), (-0.5, 0.55), (0.0, -0.1), (0.5, 0.6), (0.95, 0.0), (-0.3, -0.45), (0.6, -0.5)]:
            ax.add_patch(Circle((cx + dx, 2.5 + dy), 0.16, fc=WATER, ec=INK, lw=0.6))
        for (dx, dy) in [(-0.45, 0.05), (0.45, 0.1)]:
            ax.add_patch(Circle((cx + dx, 2.5 + dy), 0.24, fc=SUGAR, ec=RED, lw=1.0))
    if i < 3:
        arrow(ax, (x + 3.95, 2.2), (x + 4.65, 2.2))
save(fig, "m01-map.svg")

# 3. 모래사장: 멀리서는 매끈, 가까이서는 알갱이
fig, ax = canvas(11.0, 4.0, 18.0, 6.6)
ax.add_patch(Rectangle((0.6, 1.4), 7.0, 2.4, fc=SAND, ec=INK, lw=1.2))
ax.add_patch(Rectangle((0.6, 3.8), 7.0, 1.6, fc="#cfe3f3", ec=INK, lw=1.2))
ax.text(4.1, 0.8, "멀리서 본 모래사장: 매끈해 보여요", ha="center", va="center", fontsize=11)
ax.add_patch(Circle((5.6, 2.4), 0.5, fc="none", ec=RED, lw=1.6))
ax.plot([6.1, 10.0], [2.6, 3.6], color=RED, lw=1.2, ls="--")
ax.add_patch(Circle((13.2, 3.2), 2.6, fc="#fff8ea", ec=RED, lw=2))
for k in range(26):
    a = random.uniform(0, 2 * math.pi)
    rr = 2.2 * math.sqrt(random.uniform(0, 1))
    ax.add_patch(Ellipse((13.2 + rr * math.cos(a), 3.2 + rr * math.sin(a)), 0.55, 0.42, angle=random.uniform(0, 180),
                         fc=SAND, ec=INK, lw=0.8))
ax.text(13.2, 0.2, "가까이서 보면: 모래알이 따로따로", ha="center", va="center", fontsize=11, color=RED,
        fontweight="bold")
save(fig, "m01-sand.svg")

# 4. 크기 비교 사다리: 손 → 모래알 → 세포 → 알갱이
fig, ax = canvas(11.0, 4.0, 18.0, 6.6)
steps = [("손", 2.2, 1.6), ("모래알", 6.4, 0.9), ("세포", 10.8, 0.5), ("원자", 15.2, 0.15)]
for k, (lab, x, r) in enumerate(steps):
    if k == 0:
        ax.add_patch(FancyBboxPatch((x - 1.0, 2.0), 2.0, 2.6, boxstyle="round,pad=0.3", fc="#f6d8c4", ec=INK, lw=1.4))
    elif k == 1:
        ax.add_patch(Ellipse((x, 3.3), 2 * r, 1.6 * r, fc=SAND, ec=INK, lw=1.2))
    elif k == 2:
        ax.add_patch(Circle((x, 3.3), r, fc="#fbe3dc", ec=RED, lw=1.2))
    else:
        ax.add_patch(Circle((x, 3.3), r, fc=ATOM, ec=INK, lw=0.8))
    ax.text(x, 1.0, lab, ha="center", va="center", fontsize=11, fontweight="bold")
    if k < 3:
        arrow(ax, (x + 1.6, 3.3), (x + 2.6, 3.3))
        ax.text(x + 2.1, 4.0, "훨씬 작게", ha="center", va="center", fontsize=9)
ax.text(9.0, 6.0, "한 칸 갈 때마다 아주 많이 작아져요 (크기는 실제와 맞추지 않았어요)", ha="center", va="center",
        fontsize=10, color=RED)
save(fig, "m01-size.svg")

# 5. 알갱이는 꿈틀거려요: 물감 퍼지기
fig, ax = canvas(11.0, 4.6, 18.0, 7.6)
for k, (x, spread, lab) in enumerate([(2.6, 0.4, "처음"), (8.6, 1.2, "조금 지나"), (14.6, 2.0, "한참 지나")]):
    ax.add_patch(Polygon([(x - 2.0, 6.0), (x + 2.0, 6.0), (x + 1.7, 1.2), (x - 1.7, 1.2)], closed=True, fc="#eef5fb",
                         ec=INK, lw=1.4))
    n = 22
    for j in range(n):
        a = random.uniform(0, 2 * math.pi)
        rr = spread * math.sqrt(random.uniform(0, 1))
        px, py = x + rr * math.cos(a), 4.6 - abs(rr * math.sin(a)) * (1.4 if spread > 1 else 1.0)
        ax.add_patch(Circle((px, max(1.5, py)), 0.09, fc=DYE, ec=DYE))
    ax.text(x, 0.6, lab, ha="center", va="center", fontsize=11, fontweight="bold")
    if k < 2:
        arrow(ax, (x + 2.3, 3.6), (x + 3.7, 3.6))
ax.text(9.0, 7.0, "젓지 않았는데도 물감이 저절로 퍼져요", ha="center", va="center", fontsize=11, color=RED,
        fontweight="bold")
save(fig, "m01-spread.svg")

# 6. 알갱이끼리 섞여요: 설탕이 물에 녹아요
def scatter(x0, y0, w, h, n, r, taken, tries=20000):
    pts = []
    for _ in range(tries):
        if len(pts) >= n:
            break
        p = (x0 + random.uniform(r, w - r), y0 + random.uniform(r, h - r))
        if all((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2 > (r + qr + 0.04) ** 2 for q, qr in taken):
            pts.append(p); taken.append((p, r))
    return pts


fig, ax = canvas(11.0, 4.4, 18.0, 7.2)
for k, (x, sugar_in, lab) in enumerate([(4.0, False, "각설탕을 물에 넣으면"), (13.0, True, "설탕 알갱이가 물 알갱이 사이사이로 섞여 들어가요")]):
    ax.add_patch(Rectangle((x - 3.0, 1.2), 6.0, 4.8, fc="#eef5fb", ec=INK, lw=1.4))
    taken = []
    if sugar_in:
        sug = scatter(x - 2.9, 1.3, 5.8, 4.6, 6, 0.42, taken)
    else:
        ax.add_patch(Rectangle((x - 0.7, 1.25), 1.4, 1.4, fc=SUGAR, ec=RED, lw=1.6))
        taken.append(((x, 2.2), 1.25))
        sug = []
    wat = scatter(x - 2.9, 1.3, 5.8, 4.6, 70, 0.22, taken)
    for p in wat:
        ax.add_patch(Circle(p, 0.22, fc=WATER, ec=INK, lw=0.5))
    for p in sug:
        ax.add_patch(Circle(p, 0.42, fc=SUGAR, ec=RED, lw=1.4))
    if sugar_in:
        sx, sy = max(sug, key=lambda q: q[0] + q[1])
        ax.annotate("설탕 알갱이", (sx + 0.3, sy + 0.3), (x + 3.3, 6.4), fontsize=10, color=RED, fontweight="bold",
                    arrowprops=dict(arrowstyle="-", color=RED, lw=1))
    else:
        wx, wy = max(wat, key=lambda q: q[0] + q[1])
        ax.annotate("물 알갱이", (wx + 0.15, wy + 0.15), (x + 1.6, 6.5), fontsize=10, color=INK, fontweight="bold",
                    arrowprops=dict(arrowstyle="-", color=INK, lw=1))
        ax.text(x, 3.05, "각설탕", ha="center", va="center", fontsize=10, color=RED, fontweight="bold")
    ax.text(x, 0.6, lab, ha="center", va="center", fontsize=10, fontweight="bold")
arrow(ax, (7.3, 3.6), (9.7, 3.6))
ax.text(9.0, 7.1, "크기는 실제와 맞추지 않았어요", ha="center", va="center", fontsize=9)
save(fig, "m01-gaps.svg")

# 7. 물 알갱이 하나: 원자 셋
fig, ax = canvas(10.0, 3.0, 16.6, 5.0)
ax.add_patch(Circle((3.0, 2.5), 1.7, fc="#eef5fb", ec=WATER, lw=1.6, ls="--"))
ax.add_patch(Circle((3.0, 2.8), 0.85, fc=ATOM, ec=INK, lw=1.4))
ax.add_patch(Circle((1.95, 2.05), 0.5, fc="white", ec=INK, lw=1.4))
ax.add_patch(Circle((4.05, 2.05), 0.5, fc="white", ec=INK, lw=1.4))
ax.text(3.0, 0.3, "원자 셋이 꼭 붙은 물 알갱이 하나", ha="center", va="center", fontsize=11, fontweight="bold")
arrow(ax, (5.2, 2.5), (7.0, 2.5))
ax.text(6.1, 3.2, "간단히", ha="center", va="center", fontsize=9)
ax.add_patch(Circle((8.0, 2.5), 0.32, fc=WATER, ec=INK, lw=1.0))
ax.text(8.0, 1.5, "파란 동그라미", ha="center", va="center", fontsize=10)
arrow(ax, (9.0, 2.5), (10.4, 2.5))
for k in range(24):
    x, y = 11.2 + (k % 6) * 0.85 + random.uniform(-0.08, 0.08), 1.3 + (k // 6) * 0.75 + random.uniform(-0.08, 0.08)
    ax.add_patch(Circle((x, y), 0.3, fc=WATER, ec=INK, lw=0.6))
ax.text(13.3, 4.6, "아주 많이 모이면 물 한 방울", ha="center", va="center", fontsize=10)
save(fig, "m01-water.svg")
