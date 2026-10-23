"""인체 8편 그림 만들기. 실행: python lab/fig_b08.py  → docs/body/img/08/*.svg

글자는 SVG 안에 글자로 남긴다(글꼴 모양을 파일에 넣지 않는다). 보는 쪽 글꼴로 그려진다.
카드는 차분한 색으로, 강조(새로 받은 카드, 비교 화살표, 많이 든 일)만 빨강으로 칠한다.
"""
import itertools
import os

import matplotlib

matplotlib.use("svg")
import matplotlib.pyplot as plt
from matplotlib.patches import Arc, Circle, FancyArrowPatch, FancyBboxPatch, Rectangle

OUT = os.path.join(os.path.dirname(__file__), "..", "docs", "body", "img", "08")
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
NAIL = "#f3ece2"
HARD = "#d9cbb5"
NERVE = "#8e5ea2"
BLOOD = "#c0392b"


def finger_side(ax, x, y, w=9.0, h=2.6):
    """손가락 끝을 옆에서 자른 모습."""
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.0,rounding_size=1.2", fc=SKIN, ec=INK, lw=1.6))


# 1. 여는 장면: 손톱깎이 vs 손톱 밑 살
fig, ax = canvas(10.0, 4.6, 16.0, 7.4)
for k, (x, ok) in enumerate([(1.0, True), (9.0, False)]):
    ax.add_patch(FancyBboxPatch((x, 1.6), 2.4, 4.4, boxstyle="round,pad=0.4", fc=SKIN, ec=INK, lw=1.6))
    ax.add_patch(FancyBboxPatch((x + 0.4, 4.4), 1.6, 1.8, boxstyle="round,pad=0.2", fc=NAIL, ec=INK, lw=1.2))
    if ok:
        ax.add_patch(Rectangle((x + 0.2, 6.3), 2.0, 0.35, fc=GREY, ec=INK, lw=1))
        ax.text(x + 4.2, 5.4, "손톱 끝을 깎으면\n안 아파요", ha="left", va="center", fontsize=12)
    else:
        arrow(ax, (x + 1.2, 3.0), (x + 1.2, 4.2), color=RED, lw=2)
        ax.text(x + 3.2, 5.4, "손톱 밑 살을 꾹 누르면\n아파요", ha="left", va="center", fontsize=12, color=RED,
                fontweight="bold")
ax.text(8.0, 0.6, "같은 손가락인데 왜 다를까?", ha="center", va="center", fontsize=12, color=RED, fontweight="bold")
save(fig, "b08-clip.svg")

# 2. 이 편의 지도
fig, ax = canvas(11.6, 2.9, 19.4, 4.6)
titles = ["아픔을 알리는 줄", "끝은 굳은 세포", "자라는 곳은 뿌리", "손톱과 털이 하는 일"]
for i, t in enumerate(titles):
    x = 0.3 + i * 4.8
    box(ax, x, 0.4, 3.8, 3.6)
    ax.text(x + 1.9, 0.95, t, ha="center", va="center", fontsize=11, fontweight="bold")
    cx = x + 1.9
    if i == 0:
        ax.plot([x + 0.5, x + 1.5, x + 2.3, x + 3.3], [2.2, 2.8, 2.3, 3.0], color=NERVE, lw=2)
    elif i == 1:
        for k in range(4):
            ax.add_patch(Rectangle((x + 0.7 + k * 0.6, 2.2), 0.55, 0.6, fc=HARD, ec=INK, lw=1))
    elif i == 2:
        ax.plot([cx, cx], [2.0, 3.4], color=INK, lw=2.4)
        ax.add_patch(Ellipse((cx, 1.9), 0.6, 0.5, fc=CELL, ec=RED, lw=1.4))
    else:
        ax.add_patch(FancyBboxPatch((cx - 0.5, 1.8), 1.0, 1.4, boxstyle="round,pad=0.15", fc=NAIL, ec=INK, lw=1.2))
    if i < 3:
        arrow(ax, (x + 3.95, 2.2), (x + 4.65, 2.2))
save(fig, "b08-map.svg")

# 3. 신경: 아픔을 뇌로 알리는 줄
fig, ax = canvas(10.0, 4.4, 16.0, 7.0)
ax.add_patch(FancyBboxPatch((0.6, 1.0), 2.2, 4.4, boxstyle="round,pad=0.3", fc=SKIN, ec=INK, lw=1.4))
ax.add_patch(Circle((1.7, 4.4), 0.25, fc=RED, ec=RED))
xs = [1.7 + 11.0 * t / 60 for t in range(61)]
ys = [4.4 + 1.2 * math.sin(math.pi * t / 60) + 0.12 * math.sin(t * 0.7) for t in range(61)]
ax.plot(xs, ys, color=NERVE, lw=2.4)
for t in (15, 30, 45):
    arrow(ax, (xs[t], ys[t]), (xs[t + 3], ys[t + 3]), color=NERVE, lw=1.6, ms=14)
ax.add_patch(Ellipse((13.6, 4.4), 3.2, 2.4, fc=NOTE, ec=INK, lw=1.6))
ax.text(13.6, 4.4, "뇌", ha="center", va="center", fontsize=15, fontweight="bold")
ax.text(13.6, 2.4, "\"아야!\"", ha="center", va="center", fontsize=13, color=RED, fontweight="bold")
ax.text(7.2, 6.4, "신경", ha="center", va="center", fontsize=13, color=NERVE, fontweight="bold")
ax.text(7.0, 0.6, "신경이 없는 곳은 눌리거나 잘려도 뇌에 알릴 수 없어요", ha="center", va="center", fontsize=11)
save(fig, "b08-nerve.svg")

# 4. 손가락 끝 옆모습: 굳은 손톱, 뿌리, 신경·핏줄
fig, ax = canvas(11.0, 5.0, 18.0, 8.2)
finger_side(ax, 0.8, 1.0, w=13.0, h=3.8)
ax.add_patch(Polygon([(4.2, 4.8), (14.6, 4.8), (15.2, 4.4), (14.6, 4.3), (4.4, 4.3)], closed=True, fc=HARD, ec=INK,
                     lw=1.4))
ax.add_patch(Ellipse((4.0, 4.1), 1.6, 0.9, fc=CELL, ec=RED, lw=1.6))
ax.plot([1.4, 12.6], [3.4, 3.6], color=NERVE, lw=1.8)
for x in (5.0, 7.0, 9.0, 11.0, 12.6):
    ax.plot([x, x + 0.3], [3.55, 4.1], color=NERVE, lw=1.2)
ax.plot([1.4, 12.6], [2.6, 2.8], color=BLOOD, lw=1.8)
ax.text(4.0, 6.2, "뿌리: 살아 있는 세포가\n나뉘어 손톱을 만들어요", ha="center", va="center", fontsize=10, color=RED,
        fontweight="bold")
arrow(ax, (4.0, 5.6), (4.0, 4.6), color=RED, lw=1.2, ms=10)
ax.text(14.6, 6.2, "보이는 손톱 전체: 굳은 세포\n신경도 핏줄도 없어요", ha="center", va="center", fontsize=10, fontweight="bold")
arrow(ax, (14.6, 5.6), (14.6, 4.9), color=INK, lw=1.2, ms=10)
ax.text(8.0, 3.95, "신경", ha="center", va="center", fontsize=10, color=NERVE, fontweight="bold")
ax.text(8.0, 2.25, "핏줄", ha="center", va="center", fontsize=10, color=BLOOD, fontweight="bold")
arrow(ax, (5.2, 5.05), (9.0, 5.05), color=INK, lw=1.4, ms=12)
ax.text(7.1, 5.4, "앞으로 밀려 나와요", ha="center", va="center", fontsize=10)
ax.text(9.0, 0.4, "손가락 끝을 옆에서 자른 모습 (크기는 실제와 맞추지 않았어요)", ha="center", va="center", fontsize=10)
ax.set_ylim(0.0, 8.2)
save(fig, "b08-nail.svg")

# 5. 머리카락: 피부 속 뿌리에 신경이 감겨 있어요
fig, ax = canvas(10.0, 5.0, 16.0, 8.0)
ax.add_patch(Rectangle((1.0, 1.0), 14.0, 4.6, fc=SKIN, ec=INK, lw=1.4))
ax.add_patch(Polygon([(7.3, 5.6), (8.7, 5.6), (8.5, 2.4), (7.5, 2.4)], closed=True, fc="#f2c9b0", ec=INK, lw=1.2))
ax.add_patch(Ellipse((8.0, 2.3), 1.3, 1.0, fc=CELL, ec=RED, lw=1.6))
ax.plot([8.0, 8.0, 8.6], [2.6, 5.6, 7.6], color=INK, lw=3)
for k in range(3):
    y = 2.6 + k * 0.4
    ax.add_patch(Arc((8.0, y), 1.9, 0.5, theta1=180, theta2=360, color=NERVE, lw=1.4))
ax.plot([2.0, 7.1], [3.0, 3.0], color=NERVE, lw=1.6)
ax.plot([2.0, 7.4], [1.8, 2.1], color=BLOOD, lw=1.6)
ax.text(9.0, 6.9, "굳은 세포", ha="left", va="center", fontsize=10, fontweight="bold")
arrow(ax, (8.95, 6.9), (8.45, 6.9), color=INK, lw=1.0, ms=8)
ax.text(11.0, 2.2, "둥근 끝: 살아 있어요", ha="left", va="center", fontsize=10, color=RED, fontweight="bold")
arrow(ax, (10.9, 2.2), (8.8, 2.3), color=RED, lw=1.2, ms=10)
ax.text(2.0, 3.4, "신경", ha="left", va="center", fontsize=10, color=NERVE, fontweight="bold")
ax.text(2.0, 1.4, "핏줄", ha="left", va="center", fontsize=10, color=BLOOD, fontweight="bold")
ax.text(8.0, 0.4, "뿌리 아래쪽을 신경이 감싸서 잡아당기면 아파요", ha="center", va="center", fontsize=11, color=RED,
        fontweight="bold")
ax.set_ylim(0.0, 8.0)
save(fig, "b08-hair.svg")

# 6. 해 보기: 손톱 점 일기
fig, ax = canvas(11.0, 4.0, 18.0, 6.6)
for k, (x, d, lab) in enumerate([(1.0, 0.0, "오늘"), (7.0, 0.5, "두 주 뒤"), (13.0, 1.0, "한 달 뒤")]):
    ax.add_patch(FancyBboxPatch((x, 0.8), 3.2, 4.8, boxstyle="round,pad=0.4", fc=SKIN, ec=INK, lw=1.4))
    ax.add_patch(FancyBboxPatch((x + 0.5, 2.6), 2.2, 2.8, boxstyle="round,pad=0.2", fc=NAIL, ec=INK, lw=1.2))
    ax.add_patch(Circle((x + 1.6, 2.9 + d), 0.14, fc=INK, ec=INK))
    ax.text(x + 1.6, -0.2, lab, ha="center", va="center", fontsize=11, fontweight="bold")
    if k < 2:
        arrow(ax, (x + 3.8, 3.2), (x + 5.6, 3.2))
ax.set_ylim(-1.2, 6.8)
ax.text(9.0, -0.9, "움직인 길이는 많이 늘려 그렸어요", ha="center", va="center", fontsize=10)
ax.text(9.0, 6.3, "뿌리 가까이 찍은 점이 손톱 끝 쪽으로 올라가요", ha="center", va="center", fontsize=11, color=RED,
        fontweight="bold")
save(fig, "b08-dot.svg")
