"""인체 1편 그림 만들기. 실행: python lab/fig_b01.py  → docs/body/img/01/*.svg

글자는 SVG 안에 글자로 남긴다(글꼴 모양을 파일에 넣지 않는다). 보는 쪽 글꼴로 그려진다.
그림 안 글씨는 낱말과 숫자만 둔다. 문장은 본문과 그림 설명에 쓴다.
강조색은 빨강 하나로, 지금 볼 곳에만 칠한다.
검토용 PNG가 필요하면 FIG_FMT=png FIG_OUT=<폴더> 로 실행한다.
"""
import math
import os
import random

import matplotlib

matplotlib.use("svg")
import matplotlib.pyplot as plt
from matplotlib.patches import (Circle, Ellipse, FancyArrowPatch, FancyBboxPatch, PathPatch, Polygon,
                                Rectangle)
from matplotlib.path import Path

FMT = os.environ.get("FIG_FMT", "svg")
OUT = os.environ.get("FIG_OUT") or os.path.join(os.path.dirname(__file__), "..", "docs", "body", "img", "01")
os.makedirs(OUT, exist_ok=True)

plt.rcParams.update({
    "font.family": ["Apple SD Gothic Neo", "Noto Sans KR", "Malgun Gothic", "sans-serif"],
    "svg.fonttype": "none",
    "text.color": "#222",
    "figure.facecolor": "white",
    "savefig.facecolor": "white",
})

RED, GREY, INK, YEL = "#e4572e", "#c9ccd1", "#555", "#f6c445"
SKIN = "#f6d8c4"
CELL = "#f3e6df"
NEW = "#fbd3c6"


def save(fig, name):
    if FMT != "svg":
        name = name.rsplit(".", 1)[0] + "." + FMT
    fig.savefig(os.path.join(OUT, name), bbox_inches="tight", pad_inches=0.25, dpi=90)
    plt.close(fig)


def canvas(w, h, xmax, ymax):
    fig, ax = plt.subplots(figsize=(w, h))
    ax.set_xlim(0, xmax); ax.set_ylim(0, ymax); ax.axis("off")
    return fig, ax


def arrow(ax, a, b, color=INK, lw=2, rad=0.0, ms=18):
    ax.add_patch(FancyArrowPatch(a, b, arrowstyle="-|>", mutation_scale=ms, color=color, lw=lw,
                                 connectionstyle=f"arc3,rad={rad}"))


def word(ax, x, y, t, fs=12, color="#222", bold=True):
    ax.text(x, y, t, ha="center", va="center", fontsize=fs, color=color, fontweight="bold" if bold else "normal")


def blob(ax, cx, cy, rx, ry, fc=CELL, ec=INK, lw=1.6, z=1, ls="-"):
    ax.add_patch(Ellipse((cx, cy), 2 * rx, 2 * ry, fc=fc, ec=ec, lw=lw, zorder=z, ls=ls))


def lego(ax, x, y, w=1.0, h=0.6, fc=YEL, ec=INK):
    ax.add_patch(Rectangle((x, y), w, h, fc=fc, ec=ec, lw=1.2))
    for k in range(2):
        ax.add_patch(Rectangle((x + 0.15 * w + k * 0.45 * w, y + h), 0.25 * w, 0.12 * w / 1.0, fc=fc, ec=ec, lw=1.0))


def tiles(ax, x0, y0, cols, rows, s=0.9, fc=NEW, ec=RED, clip=None, seed=1):
    """다닥다닥 붙은 세포. 모양이 조금씩 다른 다각형으로 그린다."""
    rnd = random.Random(seed)
    for r in range(rows):
        for c in range(cols):
            cx = x0 + c * s + (s * 0.5 if r % 2 else 0)
            cy = y0 + r * s * 0.86
            n = rnd.choice([5, 6, 6, 7])
            pts = [(cx + s * rnd.uniform(0.45, 0.6) * math.cos(math.radians(rnd.uniform(-8, 8) + 360 / n * k)),
                    cy + s * rnd.uniform(0.4, 0.55) * math.sin(math.radians(rnd.uniform(-8, 8) + 360 / n * k)))
                   for k in range(n)]
            pg = Polygon(pts, closed=True, fc=fc, ec=ec, lw=1.2)
            ax.add_patch(pg)
            if clip is not None:
                pg.set_clip_path(clip)


def hand(ax, hx, hy):
    ax.add_patch(FancyBboxPatch((hx, hy), 2.2, 2.4, boxstyle="round,pad=0.25", fc=SKIN, ec=INK, lw=1.4))
    for k in range(4):
        ax.add_patch(FancyBboxPatch((hx + 0.1 + k * 0.55, hy + 2.5), 0.38, 1.5 - abs(k - 1.5) * 0.25,
                                    boxstyle="round,pad=0.12", fc=SKIN, ec=INK, lw=1.2))
    ax.add_patch(FancyBboxPatch((hx - 0.75, hy + 1.2), 0.5, 1.3, boxstyle="round,pad=0.12", fc=SKIN, ec=INK, lw=1.2))


# 1. 레고 집과 블록 하나 / 손과 물음표
fig, ax = canvas(11.0, 4.8, 18.0, 7.8)
for r in range(5):
    for c in range(6 - (1 if r == 4 else 0)):
        lego(ax, 0.6 + c * 1.0 + (0.5 if r == 4 else 0), 0.6 + r * 0.72)
ax.add_patch(Polygon([(0.5, 4.2), (3.6, 6.2), (6.7, 4.2)], closed=True, fc=GREY, ec=INK, lw=1.2))
ax.add_patch(Circle((8.2, 5.6), 1.2, fc="white", ec=INK, lw=2))
lego(ax, 7.6, 5.3, w=1.2, h=0.7)
ax.plot([4.6, 7.1], [2.4, 4.8], color=INK, lw=1.2, ls="--")
word(ax, 3.6, 0.0, "레고 집")
word(ax, 8.2, 3.9, "블록")
hand(ax, 12.2, 0.8)
ax.add_patch(Circle((16.4, 5.6), 1.2, fc="white", ec=RED, lw=2.4))
word(ax, 16.4, 5.6, "?", fs=30, color=RED)
ax.plot([13.4, 15.4], [2.6, 4.9], color=INK, lw=1.2, ls="--")
word(ax, 13.3, 0.0, "손")
ax.set_ylim(-0.6, 7.8)
save(fig, "b01-lego.svg")

# 2. 크게 보면: 손등 → 돋보기 → 현미경
fig, ax = canvas(11.6, 4.6, 19.0, 7.4)
ax.set_ylim(-0.2, 6.4)
ax.add_patch(FancyBboxPatch((0.6, 1.8), 3.2, 2.6, boxstyle="round,pad=0.3", fc=SKIN, ec=INK, lw=1.4))
word(ax, 2.2, 0.6, "손등")
ax.add_patch(Circle((8.6, 3.2), 2.0, fc=SKIN, ec=INK, lw=2))
for k in range(6):
    ax.plot([7.1 + k * 0.3, 7.6 + k * 0.4], [2.2 + k * 0.35, 2.0 + k * 0.4], color="#c99a80", lw=1.2)
word(ax, 8.6, 0.6, "돋보기")
lens = Circle((15.4, 3.4), 2.4, fc="white", ec=INK, lw=2.4)
ax.add_patch(lens)
tiles(ax, 13.0, 1.0, 6, 7, s=0.82, clip=lens)
ax.add_patch(Circle((15.4, 3.4), 2.4, fc="none", ec=INK, lw=2.4))
word(ax, 15.4, 0.6, "현미경", color=RED)
arrow(ax, (4.2, 3.2), (6.4, 3.2), lw=1.8)
arrow(ax, (10.8, 3.2), (12.8, 3.2), lw=1.8)
save(fig, "b01-zoom.svg")

# 3. 세포는 살아 있어요: 레고와 나란히
fig, ax = canvas(11.6, 4.4, 19.0, 7.2)
lego(ax, 1.4, 2.8, w=2.4, h=1.4)
word(ax, 2.6, 1.6, "블록")
ax.plot([6.2, 6.2], [0.4, 6.6], color=GREY, lw=1.2, ls="--")
blob(ax, 12.6, 3.6, 1.8, 1.4)
word(ax, 12.6, 3.6, "세포", fs=14)
arrow(ax, (8.2, 5.2), (10.9, 4.3), color=RED, lw=2)
word(ax, 8.0, 5.7, "영양", color=RED)
arrow(ax, (8.2, 2.2), (10.9, 3.0), color=RED, lw=2)
word(ax, 8.0, 1.7, "산소", color=RED)
arrow(ax, (14.4, 3.6), (17.0, 3.6), color=RED, lw=2)
word(ax, 17.6, 4.3, "쓰레기", color=RED)
save(fig, "b01-alive.svg")

# 4. 일마다 모양이 달라요
fig, ax = canvas(12.4, 4.2, 20.4, 6.8)
ax.set_ylim(1.2, 7.0)
for r in range(3):
    for c in range(3):
        blob(ax, 1.2 + c * 1.1 + (0.55 if r % 2 else 0), 4.6 + r * 0.45, 0.6, 0.22)
word(ax, 2.6, 3.0, "피부 세포")
word(ax, 2.6, 2.2, "납작", color=RED)
for r in range(3):
    blob(ax, 7.6, 4.6 + r * 0.55, 1.6, 0.2)
word(ax, 7.6, 3.0, "근육 세포")
word(ax, 7.6, 2.2, "길쭉", color=RED)
blob(ax, 11.8, 5.2, 0.45, 0.45)
for ang in (100, 140, 200, 240, 60):
    a = math.radians(ang)
    ax.plot([11.8 + 0.45 * math.cos(a), 11.8 + 1.1 * math.cos(a)], [5.2 + 0.45 * math.sin(a), 5.2 + 1.1 * math.sin(a)],
            color=INK, lw=1.6)
ax.plot([12.25, 14.2], [5.2, 4.4], color=INK, lw=1.8)
word(ax, 12.6, 3.0, "신경 세포")
word(ax, 12.6, 2.2, "긴 가지", color=RED)
blob(ax, 17.2, 5.6, 0.6, 0.6)
blob(ax, 17.2, 5.6, 0.28, 0.28, fc="#fbf5f2", ec="none")
ax.text(18.0, 5.6, "위", ha="left", va="center", fontsize=10)
vs = Path([(16.6, 4.3), (16.6, 4.6), (16.9, 4.6), (17.2, 4.45), (17.5, 4.6), (17.8, 4.6),
           (17.8, 4.3), (17.8, 4.0), (17.5, 4.0), (17.2, 4.15), (16.9, 4.0), (16.6, 4.0), (16.6, 4.3)],
          [Path.MOVETO] + [Path.CURVE4] * 12)
ax.add_patch(PathPatch(vs, fc=CELL, ec=INK, lw=1.4))
ax.text(18.0, 4.3, "옆", ha="left", va="center", fontsize=10)
word(ax, 17.2, 3.0, "산소를 나르는 세포")
word(ax, 17.2, 2.2, "동글납작", color=RED)
save(fig, "b01-shapes.svg")

# 5. 둘로 나뉘어 늘어나요
fig, ax = canvas(11.0, 3.8, 14.0, 5.6)
blob(ax, 1.2, 3.2, 0.7, 0.7)
arrow(ax, (2.1, 3.2), (3.1, 3.2), lw=1.6)
blob(ax, 4.4, 3.2, 1.0, 0.7)
ax.plot([4.4, 4.4], [2.3, 4.1], color=RED, lw=2, ls="--")
arrow(ax, (5.6, 3.2), (6.6, 3.2), lw=1.6)
blob(ax, 7.4, 3.9, 0.6, 0.6)
blob(ax, 7.4, 2.5, 0.6, 0.6)
arrow(ax, (8.3, 3.2), (9.3, 3.2), lw=1.6)
for dx, dy in ((0, 0.7), (0, -0.7), (1.2, 0.7), (1.2, -0.7)):
    blob(ax, 10.2 + dx, 3.2 + dy, 0.55, 0.55)
for x, t in ((1.2, "1"), (4.4, "1"), (7.4, "2"), (10.8, "4")):
    word(ax, x, 0.9, t, fs=16)
save(fig, "b01-divide.svg")

# 6. 상처 둘레의 세포가 나뉘어 빈자리를 메워요
fig, ax = canvas(12.0, 3.8, 20.0, 6.0)


def skin(ax, x0, gap, new):
    for r in range(2):
        for c in range(7):
            x, y = x0 + c * 1.15, 2.0 + r * 1.15
            if c in gap:
                ax.add_patch(FancyBboxPatch((x, y), 0.95, 0.95, boxstyle="round,pad=0.05", fc="white",
                                            ec=RED, lw=1.6, ls="--"))
            else:
                fc, ec = (NEW, RED) if c in new else (CELL, INK)
                ax.add_patch(FancyBboxPatch((x, y), 0.95, 0.95, boxstyle="round,pad=0.05", fc=fc, ec=ec, lw=1.6))


skin(ax, 0.6, gap=(3, 4), new=())
arrow(ax, (2.5, 1.5), (3.9, 1.5), color=RED, lw=1.6, ms=12)
arrow(ax, (7.2, 1.5), (5.8, 1.5), color=RED, lw=1.6, ms=12)
word(ax, 4.6, 0.6, "상처")
skin(ax, 11.4, gap=(), new=(3, 4))
word(ax, 15.4, 0.6, "며칠 지나")
arrow(ax, (8.9, 3.2), (10.9, 3.2), lw=1.8)
save(fig, "b01-heal.svg")
