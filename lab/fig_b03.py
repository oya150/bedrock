"""인체 3편 그림 만들기. 실행: python lab/fig_b03.py  → docs/body/img/03/*.svg

글자는 SVG 안에 글자로 남긴다(글꼴 모양을 파일에 넣지 않는다). 보는 쪽 글꼴로 그려진다.
카드는 차분한 색으로, 강조(새로 받은 카드, 비교 화살표, 많이 든 일)만 빨강으로 칠한다.
"""
import itertools
import os

import matplotlib

matplotlib.use("Agg")
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
    # FIG_FMT=png FIG_OUT=폴더 로 확인용 PNG 사본을 만든다.
    fmt = os.environ.get("FIG_FMT", "svg")
    out = os.environ.get("FIG_OUT", OUT)
    os.makedirs(out, exist_ok=True)
    if fmt != "svg":
        name = name.rsplit(".", 1)[0] + "." + fmt
    fig.savefig(os.path.join(out, name), bbox_inches="tight", pad_inches=0.25, dpi=110)
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


# 1. 밥알은 세포보다 훨씬 커요
fig, ax = canvas(11.0, 4.4, 18.0, 7.0)
ax.add_patch(Ellipse((2.6, 3.4), 3.6, 1.2, fc="white", ec=INK, lw=1.6))
ax.add_patch(Polygon([(0.8, 3.4), (4.4, 3.4), (3.9, 1.6), (1.3, 1.6)], closed=True, fc="white", ec=INK, lw=1.6))
for k in range(9):
    grain(ax, 1.4 + (k % 5) * 0.55, 3.6 + (k // 5) * 0.35, 0.5, 0.26, ang=20 * (k % 3))
ax.text(2.6, 0.9, "밥 한 그릇", ha="center", va="center", fontsize=12, fontweight="bold")
grain(ax, 8.2, 5.4, 3.0, 1.5, ang=10)
ax.text(8.2, 3.9, "밥알 하나", ha="center", va="center", fontsize=12)
ax.add_patch(Circle((15.0, 4.0), 0.55, fc=CELL, ec=RED, lw=1.6))
ax.text(15.0, 3.0, "세포", ha="center", va="center", fontsize=12, fontweight="bold")
arrow(ax, (10.0, 5.3), (14.3, 4.4), color=GREY, lw=1.8)
ax.text(11.6, 5.9, "그대로", ha="center", va="center", fontsize=11, color=INK)
cx, cy, d = 12.4, 4.95, 0.3
ax.plot([cx - d, cx + d], [cy - d, cy + d], color=INK, lw=2.4)
ax.plot([cx - d, cx + d], [cy + d, cy - d], color=INK, lw=2.4)
for k in range(6):
    ax.add_patch(Circle((9.0 + k * 0.35, 2.0 + 0.15 * (k % 2)), 0.07, fc=RED, ec=RED))
ax.text(9.9, 1.4, "쪼갠 영양", ha="center", va="center", fontsize=11)
arrow(ax, (11.2, 2.1), (14.5, 3.6), color=RED, lw=1.8)
ax.text(13.4, 2.1, "잘게 쪼개면", ha="center", va="center", fontsize=11, color=RED, fontweight="bold")
save(fig, "b03-rice.svg")

# 2. 먹은 것이 가는 길
fig, ax = canvas(9.0, 8.0, 14.0, 12.4)
ax.set_ylim(-0.4, 12.4)
ax.add_patch(Ellipse((7.0, 11.0), 2.2, 1.4, fc=SKIN, ec=INK, lw=1.4))
ax.text(8.6, 11.0, "입", ha="left", va="center", fontsize=12, fontweight="bold")
ax.plot([7.0, 7.0], [10.3, 7.6], color=INK, lw=7, solid_capstyle="round")
ax.plot([7.0, 7.0], [10.3, 7.6], color=FOOD, lw=4, solid_capstyle="round")
ax.text(7.5, 9.0, "식도", ha="left", va="center", fontsize=12, fontweight="bold")
ax.add_patch(Ellipse((7.9, 6.8), 3.0, 1.9, angle=-20, fc=FOOD, ec=INK, lw=1.6))
ax.text(10.0, 7.4, "위", ha="left", va="center", fontsize=12, fontweight="bold")
ax.plot([3.4, 3.4, 10.6, 10.6], [1.6, 5.2, 5.2, 0.9], color="#b58b5a", lw=10, solid_capstyle="round",
        solid_joinstyle="round")
arrow(ax, (10.6, 0.9), (10.6, 0.0), color="#8b6b43", lw=2)
ax.text(11.0, 0.1, "똥", ha="left", va="center", fontsize=12, fontweight="bold")
ax.text(11.2, 3.6, "큰창자", ha="left", va="center", fontsize=12, fontweight="bold")
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
save(fig, "b03-path.svg")

# 3. 입: 이로 씹고 침이 섞여요
fig, ax = canvas(8.0, 3.6, 12.0, 5.4)
grain(ax, 1.8, 3.2, 2.2, 1.2)
ax.text(1.8, 1.6, "밥알", ha="center", va="center", fontsize=12, fontweight="bold")
arrow(ax, (3.3, 3.2), (5.0, 3.2))
ax.text(4.15, 3.75, "이로 씹기", ha="center", va="center", fontsize=11)
for k in range(8):
    grain(ax, 6.2 + (k % 4) * 0.8, 3.0 + (k // 4) * 0.8, 0.6, 0.36, ang=30 * k)
for k, (x, y) in enumerate([(6.6, 3.4), (7.4, 2.6), (8.2, 3.45), (9.0, 2.65), (6.0, 2.4), (8.6, 4.2), (7.0, 4.2)]):
    ax.add_patch(Circle((x, y), 0.13, fc=WATER, ec=WATER))
ax.text(7.4, 1.6, "잘게 부순 밥", ha="center", va="center", fontsize=12, fontweight="bold")
ax.add_patch(Circle((10.4, 3.6), 0.13, fc=WATER, ec=WATER))
ax.text(10.7, 3.6, "침", ha="left", va="center", fontsize=12, color=WATER, fontweight="bold")
save(fig, "b03-mouth.svg")

# 4. 삼킬 때 뚜껑이 숨관을 덮어요
fig, ax = canvas(6.0, 5.0, 9.0, 7.6)
ax.add_patch(Rectangle((1.8, 0.8), 1.2, 4.4, fc="white", ec=INK, lw=1.6))
ax.text(2.4, 0.3, "숨관", ha="center", va="center", fontsize=12, fontweight="bold")
ax.add_patch(Rectangle((5.0, 0.8), 1.2, 4.4, fc=FOOD, ec=INK, lw=1.6))
ax.text(5.6, 0.3, "식도", ha="center", va="center", fontsize=12, fontweight="bold")
ax.add_patch(Polygon([(1.7, 5.2), (3.1, 5.2), (3.4, 5.75)], closed=True, fc=RED, ec=RED, lw=1))
ax.text(1.2, 6.2, "뚜껑", ha="center", va="center", fontsize=12, color=RED, fontweight="bold")
arrow(ax, (1.45, 5.95), (2.0, 5.45), color=RED, lw=1.2, ms=10)
ax.add_patch(Circle((4.1, 6.8), 0.4, fc=FOOD, ec=INK, lw=1.2))
ax.text(4.1, 7.5, "밥", ha="center", va="center", fontsize=12, fontweight="bold")
arrow(ax, (4.35, 6.35), (5.5, 4.9), color=INK, lw=1.6)
save(fig, "b03-swallow.svg")

# 5. 식도 근육이 밥 위를 조이며 밀어 내려요 (세 칸)
fig, ax = canvas(8.0, 5.2, 12.0, 8.0)
for i, by in enumerate([5.0, 3.5, 2.0]):
    cx = 2.0 + i * 4.0
    pinch = by + 1.0
    ys = [7.0, pinch + 0.45, pinch, pinch - 0.45, 0.6]
    for sgn in (-1, 1):
        xs = [cx + sgn * 0.7, cx + sgn * 0.7, cx + sgn * 0.22, cx + sgn * 0.7, cx + sgn * 0.7]
        ax.plot(xs, ys, color=INK, lw=1.8)
        ax.plot(xs[1:4], ys[1:4], color=RED, lw=3.2)
    ax.add_patch(Ellipse((cx, by), 1.1, 1.3, fc=FOOD, ec=INK, lw=1.2))
    ax.text(cx, 7.6, str(i + 1), ha="center", va="center", fontsize=14, fontweight="bold")
    if i < 2:
        arrow(ax, (cx + 1.2, 3.8), (cx + 2.8, 3.8), color=GREY, lw=1.6)
ax.text(2.0 + 1.0, 6.0, "조임", ha="left", va="center", fontsize=12, color=RED, fontweight="bold")
ax.text(2.0 - 1.0, 5.0, "밥", ha="right", va="center", fontsize=12, fontweight="bold")
ax.text(6.0, 0.1, "식도", ha="center", va="center", fontsize=12, fontweight="bold")
save(fig, "b03-squeeze.svg")

# 6. 위: 꿈틀거리며 섞고 위액이 풀어요
fig, ax = canvas(10.0, 4.8, 16.0, 7.8)
ax.add_patch(Ellipse((8.0, 4.0), 7.4, 4.6, angle=-15, fc=FOOD, ec=INK, lw=2))
ax.plot([6.0, 5.4], [6.0, 7.4], color=INK, lw=6, solid_capstyle="round")
ax.text(4.6, 7.3, "식도", ha="center", va="center", fontsize=12, fontweight="bold")
ax.plot([11.2, 12.6], [2.6, 1.6], color=INK, lw=6, solid_capstyle="round")
ax.text(13.0, 1.0, "작은창자", ha="center", va="center", fontsize=12, fontweight="bold")
for k in range(10):
    grain(ax, 6.0 + (k % 5) * 0.9, 3.4 + (k // 5) * 1.1, 0.5 - 0.03 * k, 0.3 - 0.015 * k, ang=40 * k)
for k in range(7):
    ax.add_patch(Circle((5.6 + k * 0.75, 5.3 - 0.2 * (k % 2)), 0.12, fc=YEL, ec="#c9a227"))
arrow(ax, (3.4, 4.0), (4.6, 4.6), color=RED, lw=1.8, rad=-0.4)
arrow(ax, (12.6, 4.0), (11.4, 3.4), color=RED, lw=1.8, rad=-0.4)
ax.text(2.9, 3.5, "근육", ha="center", va="center", fontsize=12, color=RED, fontweight="bold")
ax.text(13.6, 4.6, "근육", ha="center", va="center", fontsize=12, color=RED, fontweight="bold")
ax.text(10.6, 6.6, "위액", ha="left", va="center", fontsize=12, color="#8a6d00", fontweight="bold")
arrow(ax, (10.5, 6.5), (9.9, 5.6), color="#8a6d00", lw=1.2, ms=10)
ax.text(8.0, 7.6, "위", ha="center", va="center", fontsize=13, fontweight="bold")
save(fig, "b03-stomach.svg")

# 7. 작은창자 벽: 돌기가 많아서 테두리가 길어요
fig, ax = canvas(11.0, 4.6, 18.0, 7.6)
ax.add_patch(Rectangle((0.6, 2.0), 6.4, 0.5, fc=CELL, ec="none"))
ax.plot([0.6, 7.0], [2.5, 2.5], color=RED, lw=2.6)
for k in range(10):
    ax.add_patch(Circle((1.0 + k * 0.62, 6.4 + 0.25 * (k % 2)), 0.08, fc=RED, ec=RED))
ax.text(3.8, 7.3, "영양", ha="center", va="center", fontsize=12, color=RED, fontweight="bold")
ax.text(3.8, 1.3, "매끈한 벽", ha="center", va="center", fontsize=12, fontweight="bold")
ax.text(3.8, 0.5, "짧은 테두리", ha="center", va="center", fontsize=11, color=RED)
ax.plot([8.8, 8.8], [0.2, 7.4], color=GREY, lw=1.2, ls="--")
ax.add_patch(Rectangle((10.2, 2.0), 6.6, 0.5, fc=CELL, ec="none"))
ax.plot([10.2, 16.8], [2.0, 2.0], color=INK, lw=1.2)
for k in range(8):
    x0 = 10.4 + k * 0.8
    ax.add_patch(FancyBboxPatch((x0, 2.5), 0.45, 2.6, boxstyle="round,pad=0.12", fc=CELL, ec=RED, lw=2.6))
    ax.plot([x0 + 0.22, x0 + 0.22], [2.2, 4.9], color="#c0392b", lw=0.9)
ax.text(17.4, 4.6, "돌기", ha="left", va="center", fontsize=12, fontweight="bold")
arrow(ax, (17.3, 4.6), (16.75, 4.4), color=INK, lw=1.2, ms=10)
ax.text(17.4, 3.4, "핏줄", ha="left", va="center", fontsize=12, color="#c0392b", fontweight="bold")
arrow(ax, (17.3, 3.4), (16.4, 3.4), color="#c0392b", lw=1.2, ms=10)
for k in range(10):
    ax.add_patch(Circle((10.6 + k * 0.62, 6.4 + 0.25 * (k % 2)), 0.08, fc=RED, ec=RED))
ax.text(13.5, 7.3, "영양", ha="center", va="center", fontsize=12, color=RED, fontweight="bold")
ax.text(13.5, 1.3, "돌기가 솟은 벽", ha="center", va="center", fontsize=12, fontweight="bold")
ax.text(13.5, 0.5, "긴 테두리", ha="center", va="center", fontsize=11, color=RED, fontweight="bold")
save(fig, "b03-villi.svg")

# 8. 큰창자: 물을 거둬들이고 남은 것은 똥으로
fig, ax = canvas(11.0, 3.8, 18.0, 6.2)
ax.add_patch(FancyBboxPatch((0.8, 2.2), 14.0, 1.6, boxstyle="round,pad=0.3", fc="#efe2cf", ec="#b58b5a", lw=2))
for k, x in enumerate([2.0, 5.6, 9.2, 12.8]):
    n = 5 - k
    for j in range(n):
        ax.add_patch(Circle((x + (j - (n - 1) / 2) * 0.22, 3.0), 0.09, fc=WATER, ec=WATER))
    ax.add_patch(Ellipse((x, 3.0), 1.3, 0.8, fc="none", ec="#8b6b43", lw=1.2, ls="--"))
    ax.text(x, 1.4, f"물 {n}", ha="center", va="center", fontsize=11)
for x in [3.8, 7.4, 11.0]:
    arrow(ax, (x, 4.2), (x, 5.4), color=WATER, lw=1.6, ms=12)
ax.text(7.4, 5.85, "몸으로", ha="center", va="center", fontsize=12, color=WATER, fontweight="bold")
arrow(ax, (15.2, 3.0), (16.6, 3.0), color=INK, lw=2)
ax.text(16.9, 3.0, "똥", ha="left", va="center", fontsize=13, fontweight="bold")
ax.text(2.0, 0.6, "묽음", ha="center", va="center", fontsize=11)
ax.text(12.8, 0.6, "단단함", ha="center", va="center", fontsize=11, color=RED, fontweight="bold")
save(fig, "b03-large.svg")
