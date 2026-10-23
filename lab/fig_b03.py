"""인체 3편 그림 만들기. 실행: python lab/fig_b03.py  → docs/body/img/03/*.svg

글자는 SVG 안에 글자로 남긴다(글꼴 모양을 파일에 넣지 않는다). 보는 쪽 글꼴로 그려진다.
카드는 차분한 색으로, 강조(새로 받은 카드, 비교 화살표, 많이 든 일)만 빨강으로 칠한다.
"""
import itertools
import os

import matplotlib

matplotlib.use("svg")
import matplotlib.pyplot as plt
from matplotlib.patches import Arc, Circle, FancyArrowPatch, FancyBboxPatch, Rectangle

OUT = os.path.join(os.path.dirname(__file__), "..", "docs", "body", "img", "03")
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
FOOD = "#f6e7b8"
WATER = "#7da2c8"


def grain(ax, cx, cy, w, h, ang=0, fc=FOOD):
    ax.add_patch(Ellipse((cx, cy), w, h, angle=ang, fc=fc, ec=INK, lw=1.2))


# 1. 여는 장면: 밥알은 세포보다 훨씬 커요
fig, ax = canvas(11.0, 4.8, 18.0, 7.8)
ax.add_patch(Ellipse((2.6, 3.4), 3.6, 1.2, fc="white", ec=INK, lw=1.6))
ax.add_patch(Polygon([(0.8, 3.4), (4.4, 3.4), (3.9, 1.6), (1.3, 1.6)], closed=True, fc="white", ec=INK, lw=1.6))
for k in range(9):
    grain(ax, 1.4 + (k % 5) * 0.55, 3.6 + (k // 5) * 0.35, 0.5, 0.26, ang=20 * (k % 3))
ax.text(2.6, 0.9, "밥 한 그릇", ha="center", va="center", fontsize=12, fontweight="bold")
grain(ax, 8.2, 5.4, 3.0, 1.5, ang=10)
ax.text(8.2, 3.9, "밥알 하나", ha="center", va="center", fontsize=11)
ax.add_patch(Circle((14.6, 4.6), 0.55, fc=CELL, ec=RED, lw=1.6))
ax.text(14.6, 3.6, "세포", ha="center", va="center", fontsize=11, fontweight="bold")
arrow(ax, (10.0, 5.3), (13.7, 4.8), color=GREY, lw=1.8)
ax.text(11.9, 5.7, "그대로는 못 들어가요", ha="center", va="center", fontsize=10, color=INK)
for k in range(6):
    ax.add_patch(Circle((9.0 + k * 0.35, 2.0 + 0.15 * (k % 2)), 0.07, fc=RED, ec=RED))
arrow(ax, (11.2, 2.1), (14.0, 4.1), color=RED, lw=1.8)
ax.text(9.9, 1.4, "밥알을 쪼갠 것", ha="center", va="center", fontsize=9)
ax.text(13.6, 1.6, "아주 작게 쪼개면 들어가요", ha="center", va="center", fontsize=10, color=RED, fontweight="bold")
ax.text(9.0, 7.3, "크기는 실제와 맞추지 않았어요. 진짜 세포는 밥알보다 훨씬 더 작아요", ha="center", va="center",
        fontsize=10, color=INK)
save(fig, "b03-rice.svg")

# 2. 이 편의 지도
fig, ax = canvas(11.6, 2.9, 19.4, 4.6)
titles = ["입에서 잘게", "위에서 죽처럼", "작은창자에서 받아요", "큰창자에서 물을"]
for i, t in enumerate(titles):
    x = 0.3 + i * 4.8
    box(ax, x, 0.4, 3.8, 3.6)
    ax.text(x + 1.9, 0.95, t, ha="center", va="center", fontsize=12, fontweight="bold")
    cx = x + 1.9
    if i == 0:
        grain(ax, cx - 0.7, 2.6, 1.0, 0.6)
        arrow(ax, (cx - 0.1, 2.6), (cx + 0.4, 2.6), lw=1.4, ms=10)
        for k in range(4):
            grain(ax, cx + 0.7 + (k % 2) * 0.35, 2.4 + (k // 2) * 0.4, 0.28, 0.18)
    elif i == 1:
        ax.add_patch(Ellipse((cx, 2.5), 2.2, 1.6, fc=FOOD, ec=INK, lw=1.4))
        for k in range(3):
            ax.plot([cx - 0.7 + k * 0.5, cx - 0.5 + k * 0.5], [2.3, 2.7], color=INK, lw=1)
    elif i == 2:
        ax.plot([x + 0.4, x + 3.4], [2.0, 2.0], color=INK, lw=1.4)
        for k in range(6):
            ax.add_patch(FancyBboxPatch((x + 0.55 + k * 0.48, 2.0), 0.25, 0.8, boxstyle="round,pad=0.05",
                                        fc=CELL, ec=RED, lw=1))
    else:
        for k in range(3):
            ax.add_patch(Circle((cx - 0.6 + k * 0.6, 2.6), 0.18, fc=WATER, ec=WATER))
        arrow(ax, (cx, 2.3), (cx, 1.5), color=WATER, lw=1.4, ms=10)
    if i < 3:
        arrow(ax, (x + 3.95, 2.2), (x + 4.65, 2.2))
save(fig, "b03-map.svg")

# 3. 먹은 것이 가는 길
fig, ax = canvas(9.0, 8.4, 14.0, 12.4)
ax.set_ylim(-0.8, 12.4)
ax.add_patch(Ellipse((7.0, 11.0), 2.2, 1.4, fc=SKIN, ec=INK, lw=1.4))
ax.text(8.6, 11.0, "입", ha="left", va="center", fontsize=12, fontweight="bold")
ax.plot([7.0, 7.0], [10.3, 7.6], color=INK, lw=7, solid_capstyle="round")
ax.plot([7.0, 7.0], [10.3, 7.6], color=FOOD, lw=4, solid_capstyle="round")
ax.text(7.5, 9.0, "식도", ha="left", va="center", fontsize=12, fontweight="bold")
ax.add_patch(Ellipse((7.9, 6.8), 3.0, 1.9, angle=-20, fc=FOOD, ec=INK, lw=1.6))
ax.text(10.0, 7.4, "위", ha="left", va="center", fontsize=12, fontweight="bold")
# 큰창자: 왼쪽 아래에서 올라가 위를 가로지르고 오른쪽으로 내려가요
ax.plot([3.4, 3.4, 10.6, 10.6], [1.6, 5.2, 5.2, 0.9], color="#b58b5a", lw=10, solid_capstyle="round",
        solid_joinstyle="round")
arrow(ax, (10.6, 0.9), (10.6, 0.2), color="#8b6b43", lw=2)
ax.text(11.2, 3.6, "큰창자", ha="left", va="center", fontsize=12, fontweight="bold")
# 작은창자: 위 아래에서 시작해 꼬불꼬불, 왼쪽 아래 큰창자 시작점으로
xs, ys = [], []
for k in range(240):
    t = k / 239
    xs.append(8.6 - 4.6 * t + 0.5 * math.sin(t * 8 * math.pi))
    ys.append(4.4 - 2.8 * t)
ax.plot([8.3, 8.6], [6.0, 4.4], color=RED, lw=3.5)
ax.plot(xs, ys, color=RED, lw=3.5)
ax.plot([xs[-1], 3.4], [ys[-1], 1.6], color=RED, lw=3.5)
ax.text(1.0, 3.2, "작은창자", ha="left", va="center", fontsize=12, color=RED, fontweight="bold")
arrow(ax, (2.6, 3.0), (5.9, 3.0), color=RED, lw=1.4, ms=12)
ax.text(6.0, -0.3, "모양과 크기는 실제와 맞추지 않았어요", ha="center", va="center", fontsize=10)
save(fig, "b03-path.svg")

# 4. 입: 씹고, 침이 섞이고, 삼킬 때 숨길 뚜껑이 닫혀요
fig, ax = canvas(11.0, 4.8, 18.0, 7.8)
grain(ax, 1.6, 5.0, 1.8, 1.0)
arrow(ax, (2.8, 5.0), (4.0, 5.0))
for k in range(8):
    grain(ax, 4.6 + (k % 4) * 0.55, 4.7 + (k // 4) * 0.6, 0.45, 0.28, ang=30 * k)
for k in range(5):
    ax.add_patch(Circle((4.8 + k * 0.4, 3.8), 0.09, fc=WATER, ec=WATER))
ax.text(4.1, 2.9, "이로 잘게 씹고, 침이 섞여요", ha="center", va="center", fontsize=11)
ax.text(4.1, 2.2, "(오래 씹으면 단맛이 나기도 해요)", ha="center", va="center", fontsize=10)
ax.plot([8.6, 8.6], [0.5, 7.4], color=GREY, lw=1.2, ls="--")
# 두 관: 앞쪽 숨관, 뒤쪽 식도
ax.add_patch(Rectangle((11.0, 0.6), 1.2, 4.6, fc="white", ec=INK, lw=1.6))
ax.text(11.6, 0.2, "숨관", ha="center", va="center", fontsize=11, fontweight="bold")
ax.add_patch(Rectangle((14.0, 0.6), 1.2, 4.6, fc=FOOD, ec=INK, lw=1.6))
ax.text(14.6, 0.2, "식도", ha="center", va="center", fontsize=11, fontweight="bold")
ax.add_patch(Polygon([(10.9, 5.2), (12.3, 5.2), (12.6, 5.75)], closed=True, fc=RED, ec=RED, lw=1))
ax.text(10.4, 6.3, "뚜껑이 숨관을 덮어요", ha="center", va="center", fontsize=11, color=RED, fontweight="bold")
ax.add_patch(Circle((13.1, 6.6), 0.35, fc=FOOD, ec=INK, lw=1.2))
arrow(ax, (13.3, 6.2), (14.5, 4.8), color=INK, lw=1.6)
ax.text(15.8, 6.8, "꿀꺽!", ha="center", va="center", fontsize=12, fontweight="bold")
save(fig, "b03-mouth.svg")

# 5. 위: 주머니가 꿈틀거리며 섞고, 시큼한 위액이 녹여요
fig, ax = canvas(10.0, 5.0, 16.0, 8.0)
ax.add_patch(Ellipse((8.0, 4.0), 7.4, 4.6, angle=-15, fc=FOOD, ec=INK, lw=2))
ax.plot([6.0, 5.4], [6.0, 7.6], color=INK, lw=6, solid_capstyle="round")
ax.text(4.6, 7.4, "식도에서", ha="center", va="center", fontsize=10)
ax.plot([11.2, 12.6], [2.6, 1.6], color=RED, lw=4, solid_capstyle="round")
ax.text(13.6, 1.4, "작은창자로", ha="center", va="center", fontsize=10, color=RED)
for k in range(10):
    grain(ax, 6.0 + (k % 5) * 0.9, 3.4 + (k // 5) * 1.1, 0.5 - 0.03 * k, 0.3 - 0.015 * k, ang=40 * k)
for k in range(7):
    ax.add_patch(Circle((5.6 + k * 0.75, 5.3 - 0.2 * (k % 2)), 0.1, fc=YEL, ec="#c9a227"))
arrow(ax, (3.4, 4.0), (4.6, 4.6), color=INK, lw=1.6, rad=-0.4)
arrow(ax, (12.6, 4.0), (11.4, 3.4), color=INK, lw=1.6, rad=-0.4)
ax.text(2.0, 5.0, "근육이\n꿈틀", ha="center", va="center", fontsize=10)
ax.text(11.0, 7.4, "위는 꿈틀거리며 먹은 것을 섞어요", ha="center", va="center", fontsize=11)
ax.text(7.0, 0.3, "노란 방울은 시큼한 위액이에요. 먹은 것을 풀어 죽처럼 만들어요", ha="center", va="center",
        fontsize=11, color="#8a6d00")
save(fig, "b03-stomach.svg")

# 6. 작은창자 벽: 손가락 같은 돌기가 많아서 벽이 넓어요
fig, ax = canvas(11.0, 4.8, 18.0, 7.8)
ax.add_patch(Rectangle((0.6, 2.0), 6.4, 0.5, fc=CELL, ec="none"))
ax.plot([0.6, 7.0], [2.5, 2.5], color=RED, lw=2.6)
for k in range(10):
    ax.add_patch(Circle((1.0 + k * 0.62, 6.4 + 0.25 * (k % 2)), 0.08, fc=RED, ec=RED))
ax.text(3.8, 7.4, "잘게 쪼갠 영양", ha="center", va="center", fontsize=11, color=RED, fontweight="bold")
ax.text(3.8, 1.2, "매끈한 벽", ha="center", va="center", fontsize=12, fontweight="bold")
ax.plot([8.8, 8.8], [0.5, 7.2], color=GREY, lw=1.2, ls="--")
ax.add_patch(Rectangle((10.2, 2.0), 6.6, 0.5, fc=CELL, ec="none"))
ax.plot([10.2, 16.8], [2.0, 2.0], color=RED, lw=2.6)
for k in range(8):
    x0 = 10.4 + k * 0.8
    ax.add_patch(FancyBboxPatch((x0, 2.5), 0.45, 2.6, boxstyle="round,pad=0.12", fc=CELL, ec=RED, lw=2.6))
    ax.plot([x0 + 0.22, x0 + 0.22], [2.2, 4.9], color="#c0392b", lw=0.9)
ax.text(17.4, 4.6, "돌기", ha="left", va="center", fontsize=11, fontweight="bold")
arrow(ax, (17.3, 4.6), (16.75, 4.4), color=INK, lw=1.2, ms=10)
ax.text(17.4, 3.4, "핏줄", ha="left", va="center", fontsize=11, color="#c0392b", fontweight="bold")
arrow(ax, (17.3, 3.4), (16.4, 3.4), color="#c0392b", lw=1.2, ms=10)
ax.text(13.5, 1.2, "손가락 같은 돌기가 빽빽한 벽", ha="center", va="center", fontsize=12, fontweight="bold")
for k in range(10):
    ax.add_patch(Circle((10.6 + k * 0.62, 6.4 + 0.25 * (k % 2)), 0.08, fc=RED, ec=RED))
ax.text(13.5, 7.4, "잘게 쪼갠 영양", ha="center", va="center", fontsize=11, color=RED, fontweight="bold")
ax.text(9.0, 0.3, "빨간 테두리가 영양이 드나드는 벽이에요. 테두리가 길수록 영양이 많이 들어가요", ha="center",
        va="center", fontsize=11)
save(fig, "b03-villi.svg")

# 7. 큰창자: 물을 거둬들이고 남은 것은 똥으로
fig, ax = canvas(11.0, 3.8, 18.0, 6.2)
ax.add_patch(FancyBboxPatch((0.8, 2.2), 14.0, 1.6, boxstyle="round,pad=0.3", fc="#efe2cf", ec="#b58b5a", lw=2))
for k, x in enumerate([2.0, 5.6, 9.2, 12.8]):
    n = 5 - k
    for j in range(n):
        ax.add_patch(Circle((x + (j - (n - 1) / 2) * 0.22, 3.0), 0.09, fc=WATER, ec=WATER))
    ax.add_patch(Ellipse((x, 3.0), 1.0 + 0.0 * k, 0.8, fc="none", ec="#8b6b43", lw=1.2, ls="--"))
for x in [3.8, 7.4, 11.0]:
    arrow(ax, (x, 4.2), (x, 5.4), color=WATER, lw=1.6, ms=12)
ax.text(7.4, 5.8, "남은 물을 마지막으로 거둬들여요", ha="center", va="center", fontsize=11, color=WATER,
        fontweight="bold")
arrow(ax, (15.2, 3.0), (16.6, 3.0), color=INK, lw=2)
ax.text(16.9, 3.0, "똥", ha="left", va="center", fontsize=13, fontweight="bold")
arrow(ax, (1.4, 2.5), (3.4, 2.5), color=INK, lw=1.4, ms=10)
ax.text(7.8, 1.0, "갈수록 물이 줄어 단단해져요", ha="center", va="center", fontsize=11)
save(fig, "b03-large.svg")
