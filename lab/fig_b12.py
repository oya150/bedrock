"""인체 12편 그림 만들기. 실행: python lab/fig_b12.py  → docs/body/img/12/*.svg

글자는 SVG 안에 글자로 남긴다(글꼴 모양을 파일에 넣지 않는다). 보는 쪽 글꼴로 그려진다.
카드는 차분한 색으로, 강조(새로 받은 카드, 비교 화살표, 많이 든 일)만 빨강으로 칠한다.
"""
import itertools
import os

import matplotlib

matplotlib.use("svg")
import matplotlib.pyplot as plt
from matplotlib.patches import Arc, Circle, FancyArrowPatch, FancyBboxPatch, Rectangle

OUT = os.path.join(os.path.dirname(__file__), "..", "docs", "body", "img", "12")
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

random.seed(12)
SKIN = "#f6d8c4"
CELL = "#fbe3dc"
GUARD = "#dbe7f3"
BUG = "#8fb58f"
BLOOD = "#c0392b"


def bug(ax, x, y, r=0.22):
    pts = []
    for k in range(10):
        a = 2 * math.pi * k / 10
        rr = r if k % 2 == 0 else r * 0.7
        pts.append((x + rr * math.cos(a), y + rr * math.sin(a)))
    ax.add_patch(Polygon(pts, closed=True, fc=BUG, ec="#4f7a4f", lw=1))


def guard(ax, x, y, r=0.6, eat=False):
    ax.add_patch(Circle((x, y), r, fc=GUARD, ec="#4a6f96", lw=1.6))
    ax.add_patch(Circle((x - r * 0.3, y + r * 0.25), r * 0.1, fc=INK, ec=INK))
    ax.add_patch(Circle((x + r * 0.15, y + r * 0.25), r * 0.1, fc=INK, ec=INK))
    if eat:
        bug(ax, x + r * 0.1, y - r * 0.25, r=r * 0.28)


# 1. 여는 장면: 감기
fig, ax = canvas(10.0, 4.6, 16.0, 7.4)
kid(ax, 3.4, 0.6, 3.0)
ax.add_patch(Ellipse((3.4, 0.6 + 1.3 * 3.0), 0.25, 0.4, fc="#cfe3f3", ec="#7da2c8", lw=1))
for k in range(4):
    bug(ax, 6.4 + k * 0.9, 5.6 - (k % 2) * 0.6, r=0.28)
ax.text(8.0, 6.8, "눈에 안 보이는 아주 작은 침입자", ha="center", va="center", fontsize=11, color="#4f7a4f",
        fontweight="bold")
ax.text(11.6, 3.2, "콧물, 기침, 열…\n몸속에서 무슨 일이?", ha="center", va="center", fontsize=12, color=RED,
        fontweight="bold")
ax.text(8.0, 0.4, "크기는 실제와 맞추지 않았어요. 진짜 침입자는 눈으로 볼 수 없어요", ha="center", va="center",
        fontsize=10)
save(fig, "b12-cold.svg")

# 2. 이 편의 지도
fig, ax = canvas(11.6, 2.9, 19.4, 4.6)
titles = ["성벽이 막아요", "삼키는 지킴이", "열이 나요", "기억하는 지킴이"]
for i, t in enumerate(titles):
    x = 0.3 + i * 4.8
    box(ax, x, 0.4, 3.8, 3.6)
    ax.text(x + 1.9, 0.95, t, ha="center", va="center", fontsize=11, fontweight="bold")
    cx = x + 1.9
    if i == 0:
        for k in range(4):
            ax.add_patch(Rectangle((x + 0.7 + k * 0.62, 2.0), 0.55, 1.2, fc=SKIN, ec=INK, lw=1))
        bug(ax, cx, 3.6, r=0.2)
    elif i == 1:
        guard(ax, cx, 2.6, r=0.7, eat=True)
    elif i == 2:
        ax.add_patch(FancyBboxPatch((cx - 0.15, 1.8), 0.3, 1.6, boxstyle="round,pad=0.05", fc="white", ec=INK, lw=1.2))
        ax.add_patch(Circle((cx, 1.8), 0.3, fc=RED, ec=INK, lw=1.2))
        ax.add_patch(Rectangle((cx - 0.08, 1.8), 0.16, 1.3, fc=RED, ec="none"))
    else:
        guard(ax, cx - 0.5, 2.6, r=0.5)
        ax.add_patch(Rectangle((cx + 0.3, 2.2), 0.9, 0.9, fc=NOTE, ec=INK, lw=1))
        bug(ax, cx + 0.75, 2.65, r=0.2)
    if i < 3:
        arrow(ax, (x + 3.95, 2.2), (x + 4.65, 2.2))
save(fig, "b12-map.svg")

# 3. 성벽이 막아요
fig, ax = canvas(11.0, 4.6, 18.0, 7.6)
for k, (x, title, sub) in enumerate([(2.2, "피부", "단단한 벽"), (6.8, "코와 목", "끈적한 물이 붙잡아요"),
                                    (11.4, "위", "시큼한 위액"), (15.8, "입", "침")]):
    box(ax, x - 1.9, 1.4, 3.8, 3.8, fc=NOTE)
    ax.text(x, 4.6, title, ha="center", va="center", fontsize=12, fontweight="bold")
    ax.text(x, 1.9, sub, ha="center", va="center", fontsize=10)
    if k == 0:
        ax.add_patch(Rectangle((x - 1.4, 2.6), 2.8, 0.7, fc=SKIN, ec=INK, lw=1.2))
        bug(ax, x - 0.4, 3.7, r=0.2)
        bug(ax, x + 0.5, 3.6, r=0.2)
    elif k == 1:
        ax.add_patch(Ellipse((x, 3.1), 2.4, 0.9, fc="#e8f1d8", ec="#8fb58f", lw=1.2))
        bug(ax, x - 0.4, 3.1, r=0.18)
        bug(ax, x + 0.4, 3.2, r=0.18)
    elif k == 2:
        ax.add_patch(Ellipse((x, 3.1), 2.2, 1.2, fc="#f6e7b8", ec=INK, lw=1.2))
        for j in range(4):
            ax.add_patch(Circle((x - 0.6 + j * 0.4, 3.3), 0.08, fc=YEL, ec="#c9a227"))
        ax.plot([x - 0.2, x + 0.2], [2.8, 3.0], color=GREY, lw=2)
        ax.plot([x - 0.2, x + 0.2], [3.0, 2.8], color=GREY, lw=2)
    else:
        for j in range(5):
            ax.add_patch(Circle((x - 0.8 + j * 0.4, 3.1), 0.12, fc="#cfe3f3", ec="#7da2c8", lw=0.8))
ax.text(9.0, 6.6, "침입자가 몸 안으로 들어오기 어렵게 막는 첫 번째 벽", ha="center", va="center", fontsize=11,
        color=RED, fontweight="bold")
save(fig, "b12-walls.svg")

# 4. 삼키는 지킴이
fig, ax = canvas(11.0, 4.4, 18.0, 7.2)
for k, (x, stage) in enumerate([(2.6, 0), (8.6, 1), (14.6, 2)]):
    if stage == 0:
        guard(ax, x - 0.6, 3.6, r=1.0)
        bug(ax, x + 1.2, 3.6, r=0.35)
        arrow(ax, (x + 0.5, 3.6), (x + 0.85, 3.6), color=INK, lw=1.2, ms=10)
        lab = "침입자를 찾아가요"
    elif stage == 1:
        ax.add_patch(Circle((x, 3.6), 1.1, fc=GUARD, ec="#4a6f96", lw=1.6))
        ax.add_patch(Circle((x - 0.35, 3.9), 0.1, fc=INK, ec=INK))
        ax.add_patch(Circle((x + 0.15, 3.9), 0.1, fc=INK, ec=INK))
        bug(ax, x + 0.3, 3.2, r=0.35)
        lab = "감싸서 삼켜요"
    else:
        guard(ax, x, 3.6, r=1.0)
        for j in range(4):
            ax.add_patch(Circle((x - 0.3 + j * 0.2, 3.2 + 0.1 * (j % 2)), 0.06, fc=BUG, ec=BUG))
        lab = "안에서 녹여 없애요"
    ax.text(x, 1.6, lab, ha="center", va="center", fontsize=11, fontweight="bold")
    if k < 2:
        arrow(ax, (x + 2.0, 3.6), (x + 3.8, 3.6))
ax.text(9.0, 6.4, "파란 동그라미가 몸을 지키는 세포예요 (크기는 실제와 맞추지 않았어요)", ha="center",
        va="center", fontsize=10)
save(fig, "b12-eat.svg")

# 5. 열이 나요: 온도 지킴이가 맞춰 둔 온도를 올려요
fig, ax = canvas(11.0, 4.6, 18.0, 7.6)
for k, (x, lvl, lab) in enumerate([(3.0, 0.5, "평소: 37도쯤에 맞춰져 있어요"), (12.0, 0.75, "침입자와 싸울 때: 더 높게 맞춰요")]):
    ax.add_patch(FancyBboxPatch((x - 0.25, 1.8), 0.5, 4.2, boxstyle="round,pad=0.05", fc="white", ec=INK, lw=1.4))
    ax.add_patch(Circle((x, 1.8), 0.5, fc=RED, ec=INK, lw=1.4))
    ax.add_patch(Rectangle((x - 0.13, 1.8), 0.26, 4.2 * lvl, fc=RED, ec="none"))
    ax.plot([x + 0.4, x + 1.2], [1.8 + 4.2 * lvl, 1.8 + 4.2 * lvl], color=INK, lw=1.4, ls="--")
    ax.text(x, 0.7, lab, ha="center", va="center", fontsize=10, fontweight="bold")
arrow(ax, (5.2, 4.0), (10.6, 4.4), color=RED, lw=1.8)
ax.text(7.9, 5.0, "뇌의 온도 지킴이", ha="center", va="center", fontsize=10)
ax.text(15.4, 5.0, "몸이 떨려\n열을 만들어요", ha="center", va="center", fontsize=10, color=RED, fontweight="bold")
ax.text(15.4, 3.2, "어떤 침입자는\n덜 자라고\n지킴이는 더\n잘 싸워요", ha="center", va="center", fontsize=10)
save(fig, "b12-fever.svg")

# 6. 기억하는 지킴이: 처음 vs 두 번째
fig, ax = canvas(11.0, 4.6, 18.0, 7.6)
ax.plot([1.0, 17.0], [1.4, 1.4], color=INK, lw=1.4)
ax.text(9.0, 0.7, "시간", ha="center", va="center", fontsize=10)
xs1 = [1.5 + t * 0.12 for t in range(50)]
ys1 = [1.4 + 2.0 * max(0, math.sin(math.pi * max(0, t - 15) / 35)) for t in range(50)]
ax.plot(xs1, ys1, color="#4a6f96", lw=2.4)
xs2 = [9.5 + t * 0.12 for t in range(50)]
ys2 = [1.4 + 4.6 * max(0, math.sin(math.pi * max(0, t - 4) / 46)) for t in range(50)]
ax.plot(xs2, ys2, color=RED, lw=2.8)
bug(ax, 1.7, 1.9, r=0.25)
bug(ax, 9.7, 1.9, r=0.25)
ax.text(4.5, 4.4, "처음 만났을 때\n천천히, 조금", ha="center", va="center", fontsize=10, color="#4a6f96",
        fontweight="bold")
ax.text(13.6, 6.8, "두 번째 만났을 때\n빨리, 많이", ha="center", va="center", fontsize=10, color=RED, fontweight="bold")
ax.text(9.0, 7.4, "선의 높이는 맞춤 지킴이가 얼마나 많이 싸우는지를 그림으로만 나타냈어요", ha="center",
        va="center", fontsize=9)
ax.set_ylim(0.0, 7.8)
save(fig, "b12-memory.svg")

# 7. 해 보기: 밀가루 손 도장
fig, ax = canvas(10.0, 4.0, 16.0, 6.4)
for k, (x, n, lab) in enumerate([(2.6, 26, "씻기 전"), (8.0, 12, "물로만 씻은 뒤"), (13.4, 3, "비누로 씻은 뒤")]):
    ax.add_patch(Rectangle((x - 2.0, 1.4), 4.0, 4.2, fc="#2f2f3a", ec=INK, lw=1.2))
    ax.add_patch(FancyBboxPatch((x - 0.9, 2.0), 1.8, 2.4, boxstyle="round,pad=0.35", fc="none", ec="#6b6b78", lw=1.2))
    for j in range(n):
        ax.add_patch(Circle((x + random.uniform(-0.9, 0.9), random.uniform(2.1, 4.3)), 0.07, fc="white", ec="white"))
    ax.text(x, 0.8, lab, ha="center", va="center", fontsize=11, fontweight="bold")
ax.text(8.0, 6.1, "검은 종이에 찍은 손바닥 예시 (결과는 집집마다 다를 수 있어요)", ha="center", va="center", fontsize=10)
save(fig, "b12-flour.svg")
