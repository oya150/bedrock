"""인체 2편 그림 만들기. 실행: python lab/fig_b02.py  → docs/body/img/02/*.svg

글자는 SVG 안에 글자로 남긴다(글꼴 모양을 파일에 넣지 않는다). 보는 쪽 글꼴로 그려진다.
카드는 차분한 색으로, 강조(새로 받은 카드, 비교 화살표, 많이 든 일)만 빨강으로 칠한다.
"""
import itertools
import os

import matplotlib

matplotlib.use("svg")
import matplotlib.pyplot as plt
from matplotlib.patches import Arc, Circle, FancyArrowPatch, FancyBboxPatch, Rectangle

OUT = os.path.join(os.path.dirname(__file__), "..", "docs", "body", "img", "02")
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
from matplotlib.patches import Ellipse, Polygon

SKIN = "#f6d8c4"
CELL = "#fbe3dc"
AIR = "#7da2c8"


def lung(ax, cx, cy, w, h, fc=CELL, ec=RED, flip=False):
    """한쪽 폐: 세로로 긴 둥근 모양. flip은 오른쪽 폐."""
    ax.add_patch(Ellipse((cx, cy), w, h, fc=fc, ec=ec, lw=1.8))


# 1. 여는 장면: 숨 참기 놀이
fig, ax = canvas(11.0, 4.6, 18.0, 7.6)
kid(ax, 3.0, 0.6, 1.6)
hy = 0.6 + 1.55 * 1.6
ax.add_patch(Circle((3.0, hy), 0.62, fc="#fbe3dc", ec=INK, lw=1.6))
ax.plot([2.72, 2.9], [hy + 0.12, hy + 0.12], color=INK, lw=1.6)
ax.plot([3.1, 3.28], [hy + 0.12, hy + 0.12], color=INK, lw=1.6)
ax.plot([2.9, 3.1], [hy - 0.22, hy - 0.22], color=INK, lw=1.8)
ax.add_patch(Circle((2.6, hy - 0.12), 0.13, fc="#f2b8a6", ec="none"))
ax.add_patch(Circle((3.4, hy - 0.12), 0.13, fc="#f2b8a6", ec="none"))
ax.text(3.0, 0.1, "숨 참기!", ha="center", va="center", fontsize=12, fontweight="bold")
for t, x in [("처음", 7.0), ("조금\n지나", 9.6), ("한참\n지나", 12.2)]:
    ax.add_patch(Circle((x, 4.2), 0.9, fc="white", ec=INK, lw=1.6))
    ax.text(x, 4.2, t, ha="center", va="center", fontsize=12, fontweight="bold")
    if x < 12:
        arrow(ax, (x + 1.0, 4.2), (x + 1.6, 4.2))
ax.text(15.6, 4.6, "왜 결국\n숨을 쉬게\n될까?", ha="center", va="center", fontsize=13, color=RED, fontweight="bold")
save(fig, "b02-hold.svg")

# 2. 이 편의 지도
fig, ax = canvas(11.6, 2.9, 19.4, 4.6)
titles = ["숨이 가는 길", "작은 주머니", "다 쓴 숨이 나가요", "쉬지 않는 까닭"]
for i, t in enumerate(titles):
    x = 0.3 + i * 4.8
    box(ax, x, 0.4, 3.8, 3.6)
    ax.text(x + 1.9, 0.95, t, ha="center", va="center", fontsize=12, fontweight="bold")
    if i == 0:
        ax.plot([x + 1.9, x + 1.9], [3.6, 2.6], color=INK, lw=2)
        ax.plot([x + 1.9, x + 1.5], [2.6, 2.3], color=INK, lw=1.4)
        ax.plot([x + 1.9, x + 2.3], [2.6, 2.3], color=INK, lw=1.4)
        lung(ax, x + 1.3, 2.0, 0.9, 1.5)
        lung(ax, x + 2.5, 2.0, 0.9, 1.5, flip=True)
    elif i == 1:
        for k, (dx, dy) in enumerate([(0, 0), (0.45, 0.2), (-0.45, 0.2), (0.25, 0.6), (-0.25, 0.6), (0, -0.4)]):
            ax.add_patch(Circle((x + 1.9 + dx, 2.4 + dy), 0.25, fc=CELL, ec=RED, lw=1.2))
    elif i == 2:
        arrow(ax, (x + 2.8, 2.6), (x + 0.9, 2.6), color=AIR, lw=1.6, ms=11)
        ax.text(x + 1.9, 3.2, "후-", ha="center", va="center", fontsize=12)
    else:
        ax.add_patch(Ellipse((x + 1.9, 2.5), 2.0, 1.4, fc=NOTE, ec=INK, lw=1.4))
        ax.text(x + 1.9, 2.5, "뇌", ha="center", va="center", fontsize=12, fontweight="bold")
        ax.text(x + 1.9, 3.5, "숨 쉬어!", ha="center", va="center", fontsize=11, color=RED, fontweight="bold")
    if i < 3:
        arrow(ax, (x + 3.95, 2.2), (x + 4.65, 2.2))
save(fig, "b02-map.svg")

# 3. 숨이 가는 길: 코 → 숨관 → 갈라진 길 → 폐
fig, ax = canvas(10.4, 6.8, 17.0, 10.8)
ax.set_ylim(-0.8, 10.8)
ax.add_patch(Ellipse((8.5, 9.4), 1.6, 1.8, fc=SKIN, ec=INK, lw=1.4))
ax.text(9.6, 9.6, "코", ha="left", va="center", fontsize=12, fontweight="bold")
ax.plot([8.5, 8.5], [8.5, 6.2], color=INK, lw=6, solid_capstyle="round")
ax.plot([8.5, 8.5], [8.5, 6.2], color="white", lw=3, solid_capstyle="round")
ax.text(9.0, 7.4, "숨관", ha="left", va="center", fontsize=12, fontweight="bold")
lung(ax, 5.9, 3.6, 4.4, 6.0)
lung(ax, 11.1, 3.6, 4.4, 6.0, flip=True)


def branch(x, y, ang, length, depth):
    if depth == 0:
        ax.add_patch(Circle((x, y), 0.18, fc=CELL, ec=RED, lw=1))
        return
    x2 = x + length * math.cos(math.radians(ang))
    y2 = y + length * math.sin(math.radians(ang))
    ax.plot([x, x2], [y, y2], color=INK, lw=0.6 + depth * 0.5)
    branch(x2, y2, ang - 28, length * 0.7, depth - 1)
    branch(x2, y2, ang + 28, length * 0.7, depth - 1)


branch(8.5, 6.2, -125, 1.5, 4)
branch(8.5, 6.2, -55, 1.5, 4)
ax.text(3.0, 6.4, "폐", ha="center", va="center", fontsize=16, color=RED, fontweight="bold")
ax.text(14.0, 6.4, "폐", ha="center", va="center", fontsize=16, color=RED, fontweight="bold")
ax.text(8.5, -0.3, "숨이 가는 길은 거꾸로 선 나무처럼 갈라져요", ha="center",
        va="center", fontsize=11)
arrow(ax, (6.5, 10.2), (7.6, 9.6), color=AIR, lw=1.8)
ax.text(5.6, 10.3, "공기", ha="center", va="center", fontsize=11, color=AIR, fontweight="bold")
save(fig, "b02-path.svg")

# 4. 작은 주머니: 산소는 피로, 다 쓴 숨은 주머니로
fig, ax = canvas(11.0, 5.4, 18.0, 8.8)
ax.plot([4.0, 4.0], [8.2, 6.4], color=INK, lw=2.2)
cluster = [(4.0, 5.6), (3.0, 5.0), (5.0, 5.0), (2.6, 3.9), (3.8, 4.0), (5.0, 3.9), (3.3, 2.9), (4.6, 2.9)]
for (cx, cy) in cluster:
    ax.add_patch(Circle((cx, cy), 0.62, fc="white", ec=INK, lw=1.4))
    ax.add_patch(Arc((cx, cy), 1.42, 1.42, theta1=200, theta2=340, color="#c0392b", lw=1.6))
    ax.add_patch(Arc((cx, cy), 1.42, 1.42, theta1=20, theta2=160, color="#c0392b", lw=1.0))
ax.text(4.0, 1.6, "포도송이 같은 작은 주머니,\n그 둘레를 가는 핏줄이 감싸요", ha="center", va="center", fontsize=11)
ax.plot([7.2, 7.2], [0.6, 8.2], color=GREY, lw=1.2, ls="--")
ax.add_patch(Circle((10.8, 4.6), 1.6, fc="white", ec=INK, lw=2))
ax.text(10.8, 6.6, "주머니 하나", ha="center", va="center", fontsize=11, fontweight="bold")
ax.add_patch(Rectangle((12.4, 2.4), 1.0, 4.6, fc="#f2b8a6", ec="#c0392b", lw=1.6))
ax.text(12.4, 7.4, "얇은 벽 두 겹", ha="center", va="center", fontsize=11, color=RED, fontweight="bold")
arrow(ax, (12.4, 7.1), (12.4, 6.1), color=RED, lw=1.2, ms=10)
ax.text(12.9, 1.9, "핏줄", ha="center", va="center", fontsize=11, fontweight="bold")
arrow(ax, (11.4, 5.2), (13.0, 5.2), color=RED, lw=2.2)
ax.text(15.6, 5.6, "산소는\n피 속으로", ha="center", va="center", fontsize=12, color=RED, fontweight="bold")
arrow(ax, (13.0, 3.8), (11.4, 3.8), color=AIR, lw=2.2)
ax.text(15.6, 3.2, "다 쓴 숨은\n주머니로", ha="center", va="center", fontsize=12, color=AIR, fontweight="bold")
save(fig, "b02-sac.svg")

# 5. 한 바퀴: 공기 → 폐 → 피 → 세포 → 피 → 폐 → 밖
fig, ax = canvas(11.0, 5.0, 18.0, 8.2)
nodes = [("공기", 2.0, 6.4), ("폐", 6.6, 6.4), ("피", 11.4, 6.4), ("세포", 15.8, 4.0), ("피", 11.4, 1.6),
         ("폐", 6.6, 1.6), ("밖으로", 2.0, 1.6)]
for name, x, y in nodes:
    fc = CELL if name == "세포" else ("#f2b8a6" if name == "피" else NOTE)
    ax.add_patch(FancyBboxPatch((x - 1.0, y - 0.55), 2.0, 1.1, boxstyle="round,pad=0.15", fc=fc, ec=INK, lw=1.4))
    ax.text(x, y, name, ha="center", va="center", fontsize=13, fontweight="bold")
for (a, b, col, lab) in [(0, 1, RED, "산소"), (1, 2, RED, "산소"), (2, 3, RED, "산소"),
                         (3, 4, AIR, "다 쓴 숨"), (4, 5, AIR, "다 쓴 숨"), (5, 6, AIR, "다 쓴 숨")]:
    _, x1, y1 = nodes[a]
    _, x2, y2 = nodes[b]
    sx = 1.15 if x2 > x1 else (-1.15 if x2 < x1 else 0)
    arrow(ax, (x1 + sx, y1 - (0.6 if y2 < y1 else 0)), (x2 - sx, y2 + (0.6 if y2 < y1 else 0)), color=col, lw=2)
    ax.text((x1 + x2) / 2, (y1 + y2) / 2 + 0.5, lab, ha="center", va="center", fontsize=10, color=col,
            fontweight="bold")
ax.text(9.0, 4.0, "피는 이 길을\n계속 돌아요", ha="center", va="center", fontsize=11)
save(fig, "b02-loop.svg")

# 6. 숨 참기: 다 쓴 숨이 쌓이면 뇌가 "숨 쉬어!"
fig, ax = canvas(11.0, 4.6, 18.0, 7.6)
for k in range(6):
    h = 0.5 + k * 0.75
    ax.add_patch(Rectangle((1.0 + k * 1.3, 1.2), 0.9, h, fc=AIR if k < 5 else RED, ec=INK, lw=1.0))
    pass
ax.text(1.45, 0.7, "처음", ha="center", va="center", fontsize=10)
ax.text(7.95, 0.7, "한참 지나", ha="center", va="center", fontsize=10)
ax.text(4.6, 6.9, "숨을 참는 동안 몸속에 다 쓴 숨이 쌓여요", ha="center", va="center", fontsize=11)
ax.text(4.6, 6.2, "막대가 높을수록 다 쓴 숨이 많아요", ha="center", va="center", fontsize=10, color=AIR)
ax.add_patch(Ellipse((13.6, 4.6), 3.6, 2.6, fc=NOTE, ec=INK, lw=1.6))
ax.text(13.6, 4.6, "뇌", ha="center", va="center", fontsize=16, fontweight="bold")
ax.text(13.6, 6.8, "\"숨 쉬어!\"", ha="center", va="center", fontsize=14, color=RED, fontweight="bold")
arrow(ax, (9.0, 4.4), (11.6, 4.6), color=RED, lw=1.8)
ax.text(13.6, 2.4, "참을수록 몸이 저절로 숨을 쉬어요", ha="center", va="center", fontsize=11, color=RED,
        fontweight="bold")
save(fig, "b02-why.svg")

# 7. 큰 풍선 하나 vs 작은 주머니 여럿: 핏줄과 붙은 벽(빨간 선)의 길이
fig, ax = canvas(11.0, 5.0, 18.0, 8.2)
ax.add_patch(Circle((4.4, 4.4), 2.6, fc="white", ec=RED, lw=3.2))
ax.text(4.4, 0.9, "큰 풍선 하나", ha="center", va="center", fontsize=12, fontweight="bold")
ax.plot([9.0, 9.0], [0.6, 7.8], color=GREY, lw=1.2, ls="--")
ax.add_patch(Circle((13.6, 4.4), 2.6, fc="none", ec=GREY, lw=1.0, ls=":"))
r = 0.52
for cx, cy in [(13.6, 4.4)] + [(13.6 + 1.08 * math.cos(math.radians(a)), 4.4 + 1.08 * math.sin(math.radians(a)))
                               for a in range(0, 360, 60)] + \
        [(13.6 + 2.05 * math.cos(math.radians(a)), 4.4 + 2.05 * math.sin(math.radians(a))) for a in range(30, 390, 30)]:
    ax.add_patch(Circle((cx, cy), r, fc="white", ec=RED, lw=3.2))
ax.text(13.6, 0.9, "작은 주머니 여럿", ha="center", va="center", fontsize=12, fontweight="bold")
ax.text(9.0, 8.4, "빨간 선은 핏줄과 붙어 있는 벽이에요. 작은 주머니가 많으면 빨간 선이 훨씬 길어져요", ha="center",
        va="center", fontsize=11, color=RED)
save(fig, "b02-many.svg")
