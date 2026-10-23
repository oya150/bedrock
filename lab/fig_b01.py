"""인체 1편 그림 만들기. 실행: python lab/fig_b01.py  → docs/body/img/01/*.svg

글자는 SVG 안에 글자로 남긴다(글꼴 모양을 파일에 넣지 않는다). 보는 쪽 글꼴로 그려진다.
카드는 차분한 색으로, 강조(새로 받은 카드, 비교 화살표, 많이 든 일)만 빨강으로 칠한다.
"""
import itertools
import os

import matplotlib

matplotlib.use("svg")
import matplotlib.pyplot as plt
from matplotlib.patches import Arc, Circle, FancyArrowPatch, FancyBboxPatch, Rectangle

OUT = os.path.join(os.path.dirname(__file__), "..", "docs", "body", "img", "01")
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

from matplotlib.patches import Ellipse, Polygon, PathPatch
from matplotlib.path import Path
import math

SKIN = "#f6d8c4"
CELL = "#fbe3dc"


def blob(ax, cx, cy, rx, ry, fc=CELL, ec=RED, lw=1.6, z=1):
    ax.add_patch(Ellipse((cx, cy), 2 * rx, 2 * ry, fc=fc, ec=ec, lw=lw, zorder=z))


def lego(ax, x, y, w=1.0, h=0.6, fc=YEL, ec=INK):
    ax.add_patch(Rectangle((x, y), w, h, fc=fc, ec=ec, lw=1.2))
    for k in range(2):
        ax.add_patch(Rectangle((x + 0.15 + k * 0.45, y + h), 0.25, 0.12, fc=fc, ec=ec, lw=1.0))


def tiles(ax, x0, y0, cols, rows, s=0.9, fc=CELL, ec=RED, clip=None, seed=1):
    """다닥다닥 붙은 세포. 모양이 조금씩 다른 다각형으로 그린다."""
    import random
    rnd = random.Random(seed)
    for r in range(rows):
        for c in range(cols):
            cx = x0 + c * s * 1.0 + (s * 0.5 if r % 2 else 0)
            cy = y0 + r * s * 0.86
            n = rnd.choice([5, 6, 6, 7])
            pts = [(cx + s * rnd.uniform(0.45, 0.6) * math.cos(math.radians(rnd.uniform(-8, 8) + 360 / n * k)),
                    cy + s * rnd.uniform(0.4, 0.55) * math.sin(math.radians(rnd.uniform(-8, 8) + 360 / n * k)))
                   for k in range(n)]
            pg = Polygon(pts, closed=True, fc=fc, ec=ec, lw=1.2)
            ax.add_patch(pg)
            if clip is not None:
                pg.set_clip_path(clip)


# 1. 여는 장면: 레고 집과 블록 하나 / 손과 물음표
fig, ax = canvas(11.0, 4.8, 18.0, 7.8)
for r in range(5):
    for c in range(6 - (1 if r == 4 else 0)):
        lego(ax, 0.6 + c * 1.0 + (0.5 if r == 4 else 0), 0.6 + r * 0.72)
ax.add_patch(Polygon([(0.5, 4.2), (3.6, 6.2), (6.7, 4.2)], closed=True, fc=RED, ec=INK, lw=1.2))
ax.add_patch(Circle((8.2, 5.6), 1.2, fc="white", ec=INK, lw=2))
lego(ax, 7.6, 5.3, w=1.2, h=0.7)
ax.plot([4.6, 7.1], [2.4, 4.8], color=INK, lw=1.2, ls="--")
ax.text(8.2, 3.9, "가까이 보면 블록 하나", ha="center", va="center", fontsize=11)
# 손
hx, hy = 12.2, 0.8
ax.add_patch(FancyBboxPatch((hx, hy), 2.2, 2.4, boxstyle="round,pad=0.25", fc=SKIN, ec=INK, lw=1.4))
for k in range(4):
    ax.add_patch(FancyBboxPatch((hx + 0.1 + k * 0.55, hy + 2.5), 0.38, 1.5 - abs(k - 1.5) * 0.25,
                                boxstyle="round,pad=0.12", fc=SKIN, ec=INK, lw=1.2))
ax.add_patch(FancyBboxPatch((hx - 0.75, hy + 1.2), 0.5, 1.3, boxstyle="round,pad=0.12", fc=SKIN, ec=INK, lw=1.2))
ax.add_patch(Circle((16.4, 5.6), 1.2, fc="white", ec=INK, lw=2))
ax.text(16.4, 5.6, "?", ha="center", va="center", fontsize=30, color=RED, fontweight="bold")
ax.plot([13.4, 15.4], [2.6, 4.9], color=INK, lw=1.2, ls="--")
ax.text(16.4, 3.9, "우리 몸을 가까이 보면?", ha="center", va="center", fontsize=11, color=RED, fontweight="bold")
save(fig, "b01-lego.svg")

# 2. 이 편의 지도
fig, ax = canvas(11.6, 2.9, 19.4, 4.6)
titles = ["작은 방이 보여요", "세포는 살아 있어요", "일마다 모양이 달라요", "둘로 나뉘기도 해요"]
for i, t in enumerate(titles):
    x = 0.3 + i * 4.8
    box(ax, x, 0.4, 3.8, 3.6)
    ax.text(x + 1.9, 0.95, t, ha="center", va="center", fontsize=12, fontweight="bold")
    if i == 0:
        tiles(ax, x + 0.8, 1.8, 3, 3, s=0.6)
    elif i == 1:
        blob(ax, x + 1.9, 2.6, 0.6, 0.5)
        arrow(ax, (x + 0.4, 2.9), (x + 1.35, 2.75), color=INK, lw=1.2, ms=9)
        arrow(ax, (x + 2.45, 2.45), (x + 3.4, 2.3), color=INK, lw=1.2, ms=9)
    elif i == 2:
        blob(ax, x + 0.8, 2.6, 0.45, 0.18)
        blob(ax, x + 1.9, 2.6, 0.15, 0.6)
        blob(ax, x + 3.0, 2.6, 0.32, 0.32)
    else:
        blob(ax, x + 0.8, 2.6, 0.38, 0.38)
        arrow(ax, (x + 1.25, 2.6), (x + 1.75, 2.6), color=INK, lw=1.2, ms=9)
        blob(ax, x + 2.3, 2.95, 0.3, 0.3)
        blob(ax, x + 2.3, 2.25, 0.3, 0.3)
    if i < 3:
        arrow(ax, (x + 3.95, 2.2), (x + 4.65, 2.2))
save(fig, "b01-map.svg")

# 3. 크게 보면: 손등 → 돋보기 → 현미경
fig, ax = canvas(11.6, 4.6, 19.0, 7.4)
ax.set_ylim(-0.6, 6.4)
ax.add_patch(FancyBboxPatch((0.6, 1.8), 3.2, 2.6, boxstyle="round,pad=0.3", fc=SKIN, ec=INK, lw=1.4))
ax.text(2.2, 0.9, "손등", ha="center", va="center", fontsize=12, fontweight="bold")
ax.add_patch(Circle((8.6, 3.2), 2.0, fc=SKIN, ec=INK, lw=2))
for k in range(6):
    ax.plot([7.1 + k * 0.3, 7.6 + k * 0.4], [2.2 + k * 0.35, 2.0 + k * 0.4], color="#d9b39c", lw=1)
ax.text(8.6, 0.6, "돋보기로 보면\n주름이 보여요", ha="center", va="center", fontsize=11)
lens = Circle((15.4, 3.4), 2.4, fc="white", ec=INK, lw=2.4)
ax.add_patch(lens)
tiles(ax, 13.0, 1.0, 6, 7, s=0.82, clip=lens)
ax.add_patch(Circle((15.4, 3.4), 2.4, fc="none", ec=INK, lw=2.4))
ax.text(15.4, 0.2, "얇게 떼어 현미경으로 보면\n작은 방이 다닥다닥", ha="center", va="center", fontsize=11, color=RED,
        fontweight="bold")
arrow(ax, (4.2, 3.2), (6.4, 3.2), color=INK, lw=1.8)
arrow(ax, (10.8, 3.2), (12.8, 3.2), color=INK, lw=1.8)
save(fig, "b01-zoom.svg")

# 4. 세포는 살아 있어요: 레고와 비교
fig, ax = canvas(11.6, 4.4, 19.0, 7.2)
lego(ax, 1.4, 2.6, w=2.4, h=1.4)
ax.text(2.6, 1.4, "레고 블록\n혼자서 아무것도 안 해요", ha="center", va="center", fontsize=11)
ax.plot([6.2, 6.2], [0.4, 6.6], color=GREY, lw=1.2, ls="--")
blob(ax, 12.6, 3.6, 1.8, 1.4)
arrow(ax, (8.2, 5.2), (10.9, 4.3), color=INK, lw=1.8)
ax.text(8.0, 5.6, "밥(영양)", ha="center", va="center", fontsize=11, fontweight="bold")
arrow(ax, (8.2, 2.2), (10.9, 3.0), color=INK, lw=1.8)
ax.text(8.0, 1.8, "산소", ha="center", va="center", fontsize=11, fontweight="bold")
arrow(ax, (14.4, 3.6), (17.0, 3.6), color=RED, lw=1.8)
ax.text(17.6, 4.3, "쓰레기", ha="center", va="center", fontsize=11, color=RED, fontweight="bold")
ax.text(12.6, 3.6, "세포", ha="center", va="center", fontsize=14, color=RED, fontweight="bold")
ax.text(12.6, 1.2, "세포는 살아 있어요", ha="center", va="center", fontsize=11, color=RED, fontweight="bold")
save(fig, "b01-alive.svg")

# 5. 일마다 모양이 달라요
fig, ax = canvas(12.4, 4.8, 20.4, 7.8)
# 피부: 납작하게 겹겹이
for r in range(3):
    for c in range(3):
        blob(ax, 1.2 + c * 1.1 + (0.55 if r % 2 else 0), 4.6 + r * 0.45, 0.6, 0.22)
ax.text(2.6, 2.9, "피부 세포", ha="center", va="center", fontsize=12, fontweight="bold")
ax.text(2.6, 2.1, "납작하게 겹겹이\n덮어요", ha="center", va="center", fontsize=10)
# 근육: 길쭉
for r in range(3):
    blob(ax, 7.6, 4.6 + r * 0.55, 1.6, 0.2)
ax.text(7.6, 2.9, "근육 세포", ha="center", va="center", fontsize=12, fontweight="bold")
ax.text(7.6, 2.1, "길쭉해서\n당겨요", ha="center", va="center", fontsize=10)
# 신경: 가지와 긴 꼬리
blob(ax, 11.8, 5.2, 0.45, 0.45)
for ang in (100, 140, 200, 240, 60):
    a = math.radians(ang)
    ax.plot([11.8 + 0.45 * math.cos(a), 11.8 + 1.1 * math.cos(a)], [5.2 + 0.45 * math.sin(a), 5.2 + 1.1 * math.sin(a)],
            color=RED, lw=1.6)
ax.plot([12.25, 14.2], [5.2, 4.4], color=RED, lw=1.8)
ax.text(12.6, 2.9, "신경 세포", ha="center", va="center", fontsize=12, fontweight="bold")
ax.text(12.6, 2.1, "가지를 길게 뻗어\n신호를 전해요", ha="center", va="center", fontsize=10)
# 적혀구: 동글납작
blob(ax, 17.2, 5.6, 0.6, 0.6)
blob(ax, 17.2, 5.6, 0.28, 0.28, fc="#fdf1ec", ec="none")
ax.text(18.0, 5.6, "위에서", ha="left", va="center", fontsize=9)
vs = Path.make_compound_path(Path([(16.6, 4.3), (16.6, 4.6), (16.9, 4.6), (17.2, 4.45), (17.5, 4.6), (17.8, 4.6),
                                   (17.8, 4.3), (17.8, 4.0), (17.5, 4.0), (17.2, 4.15), (16.9, 4.0), (16.6, 4.0),
                                   (16.6, 4.3)],
                                  [Path.MOVETO] + [Path.CURVE4] * 12))
ax.add_patch(PathPatch(vs, fc=CELL, ec=RED, lw=1.4))
ax.text(18.0, 4.3, "옆에서", ha="left", va="center", fontsize=9)
ax.text(17.2, 2.9, "산소를 나르는 세포", ha="center", va="center", fontsize=12, fontweight="bold")
ax.text(17.2, 2.1, "동글납작하고 말랑해서\n좁은 핏줄도 휘며 지나가요", ha="center", va="center", fontsize=10)
ax.text(10.2, 0.6, "모양을 보면 하는 일이 보여요 (크기는 실제와 맞추지 않았어요)", ha="center", va="center", fontsize=12, color=RED, fontweight="bold")
save(fig, "b01-shapes.svg")

# 6. 둘로 나뉘어 늘어나요
fig, ax = canvas(12.0, 4.4, 19.8, 7.2)
blob(ax, 1.4, 4.2, 0.7, 0.7)
arrow(ax, (2.3, 4.2), (3.3, 4.2), color=INK, lw=1.6)
blob(ax, 4.6, 4.2, 1.0, 0.7)
ax.plot([4.6, 4.6], [3.5, 4.9], color=RED, lw=1.4, ls="--")
arrow(ax, (5.8, 4.2), (6.8, 4.2), color=INK, lw=1.6)
blob(ax, 7.6, 4.9, 0.6, 0.6)
blob(ax, 7.6, 3.5, 0.6, 0.6)
arrow(ax, (8.4, 4.2), (9.4, 4.2), color=INK, lw=1.6)
for dx, dy in ((0, 0.7), (0, -0.7), (1.2, 0.7), (1.2, -0.7)):
    blob(ax, 10.2 + dx, 4.2 + dy, 0.55, 0.55)
ax.text(6.0, 1.8, "하나가 커져서 둘로, 둘이 넷으로", ha="center", va="center", fontsize=12, color=RED, fontweight="bold")
ax.plot([12.6, 12.6], [0.4, 6.8], color=GREY, lw=1.2, ls="--")
ax.add_patch(FancyBboxPatch((13.6, 3.4), 2.0, 1.6, boxstyle="round,pad=0.25", fc=SKIN, ec=INK, lw=1.2))
ax.add_patch(Ellipse((14.6, 4.2), 1.0, 0.6, fc="#e9a08a", ec=RED, lw=1.2))
arrow(ax, (16.0, 4.2), (16.6, 4.2), color=INK, lw=1.4, ms=12)
ax.add_patch(FancyBboxPatch((16.9, 3.4), 2.0, 1.6, boxstyle="round,pad=0.25", fc=SKIN, ec=INK, lw=1.2))
ax.add_patch(Ellipse((17.9, 4.2), 0.9, 0.5, fc="#fbe8df", ec=RED, lw=1.0, ls="--"))
ax.text(16.25, 1.8, "까진 무릎에\n새살이 돋아요", ha="center", va="center", fontsize=12, fontweight="bold")
save(fig, "b01-divide.svg")
