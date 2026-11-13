"""인체 8편 그림 만들기. 실행: python lab/fig_b08.py  → docs/body/img/08/*.svg

글자는 SVG 안에 글자로 남긴다(글꼴 모양을 파일에 넣지 않는다). 보는 쪽 글꼴로 그려진다.
강조는 빨강 하나. 신경은 보라, 핏줄은 짙은 빨강, 굳은 세포는 베이지로 칠한다. 그림 안 글씨는 낱말과 숫자만.
확인용 PNG: FIG_FMT=png FIG_OUT=/어딘가 python lab/fig_b08.py
"""
import math
import os

import matplotlib

matplotlib.use("svg")
import matplotlib.pyplot as plt
from matplotlib.patches import Arc, Circle, Ellipse, FancyArrowPatch, FancyBboxPatch, Polygon, Rectangle

FMT = os.environ.get("FIG_FMT", "svg")
OUT = os.environ.get("FIG_OUT") or os.path.join(os.path.dirname(__file__), "..", "docs", "body", "img", "08")
os.makedirs(OUT, exist_ok=True)

plt.rcParams.update({
    "font.family": ["Apple SD Gothic Neo", "Noto Sans KR", "Malgun Gothic", "sans-serif"],
    "svg.fonttype": "none",
    "text.color": "#222",
    "figure.facecolor": "white",
    "savefig.facecolor": "white",
})

RED, GREY, INK, NOTE = "#e4572e", "#c9ccd1", "#555", "#fffdf5"
SKIN = "#f6d8c4"
SKIN_TOP = "#f2c9b0"
CELL = "#fbe3dc"
NAIL = "#f3ece2"
HARD = "#d9cbb5"
NERVE = "#8e5ea2"
BLOOD = "#c0392b"


def save(fig, name):
    name = name.rsplit(".", 1)[0] + "." + FMT
    fig.savefig(os.path.join(OUT, name), bbox_inches="tight", pad_inches=0.25, dpi=110)
    plt.close(fig)


def canvas(w, h, xmax, ymax):
    fig, ax = plt.subplots(figsize=(w, h))
    ax.set_xlim(0, xmax); ax.set_ylim(0, ymax); ax.axis("off")
    return fig, ax


def arrow(ax, a, b, color=INK, lw=2, rad=0.0, ms=18):
    ax.add_patch(FancyArrowPatch(a, b, arrowstyle="-|>", mutation_scale=ms, color=color, lw=lw,
                                 connectionstyle=f"arc3,rad={rad}"))


def finger_top(ax, x, y, w=2.4, h=4.4):
    """손가락을 손등 쪽에서 본 모습. 위쪽에 손톱."""
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.4", fc=SKIN, ec=INK, lw=1.6))
    ax.add_patch(FancyBboxPatch((x + 0.4, y + h - 1.6), w - 0.8, 1.8, boxstyle="round,pad=0.2", fc=NAIL, ec=INK,
                                lw=1.2))


def hair_root(ax, cx, base, top, nerve_color=NERVE, lift=0.0):
    """피부 속 머리카락 뿌리: 주머니, 둥근 끝, 둘레를 감싼 신경."""
    ax.add_patch(Polygon([(cx - 0.7, top), (cx + 0.7, top), (cx + 0.5, base + 0.1), (cx - 0.5, base + 0.1)],
                         closed=True, fc=SKIN_TOP, ec=INK, lw=1.2))
    ax.add_patch(Ellipse((cx, base + lift), 1.3, 1.0, fc=CELL, ec=INK, lw=1.4))
    for k in range(3):
        ax.add_patch(Arc((cx, base + 0.3 + k * 0.4), 1.9, 0.5, theta1=180, theta2=360, color=nerve_color, lw=1.6))


# 그림 1. 손톱 끝 깎기와 손톱 밑 살 누르기
fig, ax = canvas(9.0, 4.6, 14.0, 7.6)
finger_top(ax, 2.0, 1.6)
ax.add_patch(Rectangle((2.2, 6.3), 2.0, 0.35, fc=GREY, ec=INK, lw=1))
ax.text(3.2, 0.7, "손톱 끝 깎기", ha="center", va="center", fontsize=12)
ax.text(3.2, 7.3, "안 아픔", ha="center", va="center", fontsize=13, fontweight="bold")
finger_top(ax, 9.6, 1.6)
arrow(ax, (10.8, 3.0), (10.8, 4.2), color=RED, lw=2.4)
ax.text(10.8, 0.7, "손톱 밑 살 누르기", ha="center", va="center", fontsize=12)
ax.text(10.8, 7.3, "아픔", ha="center", va="center", fontsize=13, fontweight="bold", color=RED)
ax.plot([7.0, 7.0], [0.4, 7.4], color=GREY, lw=1.2, ls="--")
save(fig, "b08-clip.svg")

# 그림 2. 신경이 있는 곳과 없는 곳
fig, ax = canvas(10.0, 5.0, 16.0, 8.4)
# 위: 손가락 살 → 신경 → 뇌
ax.add_patch(FancyBboxPatch((0.6, 5.2), 2.2, 1.6, boxstyle="round,pad=0.2", fc=SKIN, ec=INK, lw=1.4))
ax.add_patch(Circle((1.7, 6.0), 0.22, fc=RED, ec=RED))
xs = [1.9 + 10.0 * t / 60 for t in range(61)]
ys = [6.0 + 0.6 * math.sin(math.pi * t / 60) + 0.1 * math.sin(t * 0.7) for t in range(61)]
ax.plot(xs, ys, color=NERVE, lw=2.4)
for t in (15, 30, 45):
    arrow(ax, (xs[t], ys[t]), (xs[t + 3], ys[t + 3]), color=NERVE, lw=1.6, ms=14)
ax.text(7.0, 7.3, "신경", ha="center", va="center", fontsize=12, color=NERVE, fontweight="bold")
ax.add_patch(Ellipse((13.6, 6.0), 2.8, 1.8, fc=NOTE, ec=INK, lw=1.6))
ax.text(13.6, 6.0, "뇌", ha="center", va="center", fontsize=14, fontweight="bold")
ax.text(15.4, 7.2, "아야!", ha="left", va="center", fontsize=13, color=RED, fontweight="bold")
ax.text(1.7, 4.6, "손가락 살", ha="center", va="center", fontsize=11)
# 아래: 손톱 끝 → (줄 없음) → 뇌
ax.add_patch(Rectangle((0.7, 1.6), 2.0, 0.7, fc=HARD, ec=INK, lw=1.2))
ax.plot([2.9, 11.9], [1.95, 1.95], color=GREY, lw=1.4, ls=(0, (2, 4)))
ax.add_patch(Ellipse((13.6, 1.95), 2.8, 1.8, fc=NOTE, ec=INK, lw=1.6))
ax.text(13.6, 1.95, "뇌", ha="center", va="center", fontsize=14, fontweight="bold")
ax.text(15.4, 3.1, "…", ha="left", va="center", fontsize=14, color="#777")
ax.text(7.0, 2.6, "신경 없음", ha="center", va="center", fontsize=11, color="#777")
ax.text(1.7, 0.9, "손톱 끝", ha="center", va="center", fontsize=11)
ax.plot([0.3, 16.0], [3.9, 3.9], color=GREY, lw=1.0, ls="--")
ax.set_xlim(0, 16.6)
save(fig, "b08-nerve.svg")

# 그림 3. 손가락 끝을 옆에서 자른 모습
fig, ax = canvas(11.0, 4.8, 18.0, 7.8)
ax.add_patch(FancyBboxPatch((0.8, 1.0), 13.0, 3.8, boxstyle="round,pad=0.0,rounding_size=1.2", fc=SKIN, ec=INK,
                            lw=1.6))
ax.add_patch(Polygon([(4.2, 4.8), (14.6, 4.8), (15.2, 4.4), (14.6, 4.3), (4.4, 4.3)], closed=True, fc=HARD, ec=INK,
                     lw=1.4))
ax.add_patch(Ellipse((4.0, 4.1), 1.6, 0.9, fc=CELL, ec=INK, lw=1.4))
ax.plot([1.4, 12.6], [3.4, 3.6], color=NERVE, lw=1.8)
for x in (5.0, 7.0, 9.0, 11.0, 12.6):
    ax.plot([x, x + 0.3], [3.55, 4.1], color=NERVE, lw=1.2)
ax.plot([1.4, 12.6], [2.6, 2.8], color=BLOOD, lw=1.8)
ax.plot([14.3, 14.3], [3.7, 5.5], color=RED, lw=2, ls="--")
ax.text(14.3, 5.9, "깎는 곳", ha="center", va="center", fontsize=12, color=RED, fontweight="bold")
ax.text(9.0, 5.5, "굳은 세포", ha="center", va="center", fontsize=11)
arrow(ax, (9.0, 5.2), (9.0, 4.85), color=INK, lw=1.2, ms=10)
ax.text(3.2, 6.0, "손톱 뿌리", ha="center", va="center", fontsize=11)
arrow(ax, (3.4, 5.7), (3.9, 4.6), color=INK, lw=1.2, ms=10)
ax.text(12.9, 3.6, "신경", ha="left", va="center", fontsize=11, color=NERVE, fontweight="bold")
ax.text(12.9, 2.75, "핏줄", ha="left", va="center", fontsize=11, color=BLOOD, fontweight="bold")
ax.text(9.0, 1.6, "손가락 살", ha="center", va="center", fontsize=11)
ax.set_xlim(-0.6, 18.0)
save(fig, "b08-nail.svg")

# 그림 4. 뿌리에서 새 세포가 생겨 손톱을 밀어내요
fig, ax = canvas(11.0, 5.0, 18.0, 8.2)
CW, GAP = 1.2, 0.12
SKIN_X = 4.9
rows = [
    (6.2, ["root", "h", "h", "h", "h"]),
    (3.8, ["root", "new", "h", "h", "h", "h"]),
    (1.4, ["root", "new", "mid", "h", "h", "h", "h"]),
]
for i, (y, cells) in enumerate(rows):
    ax.text(0.3, y + 0.5, f"{i + 1}", ha="center", va="center", fontsize=13, fontweight="bold")
    for k, kind in enumerate(cells):
        x = 1.0 + k * (CW + GAP)
        fc = {"root": CELL, "new": CELL, "mid": "#ead9cb", "h": HARD}[kind]
        ec = RED if kind == "new" else INK
        ax.add_patch(Rectangle((x, y), CW, 1.0, fc=fc, ec=ec, lw=2.4 if kind == "new" else 1.2))
    out = sum(1 for k in range(len(cells)) if 1.0 + k * (CW + GAP) >= SKIN_X)
    ax.text(1.0 + len(cells) * (CW + GAP) + 0.3, y + 0.5, f"밖으로 {out}칸", ha="left", va="center", fontsize=11)
ax.plot([SKIN_X, SKIN_X], [0.9, 7.6], color=INK, lw=1.4, ls="--")
ax.text(SKIN_X, 7.9, "피부 끝", ha="center", va="center", fontsize=11)
ax.text(1.6, 7.6, "뿌리", ha="center", va="center", fontsize=11)
ax.text(2.9, 5.3, "새 세포", ha="center", va="center", fontsize=11, color=RED, fontweight="bold")
ax.text(9.5, 7.6, "굳은 세포", ha="center", va="center", fontsize=11)
ax.set_ylim(0.8, 8.2)
save(fig, "b08-grow.svg")

# 그림 5. 손톱 점 일기
fig, ax = canvas(11.0, 4.4, 18.0, 7.2)
for k, (x, d, lab) in enumerate([(1.0, 0.0, "오늘"), (7.0, 0.5, "2주 뒤"), (13.0, 1.0, "한 달 뒤")]):
    ax.add_patch(FancyBboxPatch((x, 0.8), 3.2, 4.8, boxstyle="round,pad=0.4", fc=SKIN, ec=INK, lw=1.4))
    ax.add_patch(FancyBboxPatch((x + 0.5, 2.6), 2.2, 2.8, boxstyle="round,pad=0.2", fc=NAIL, ec=INK, lw=1.2))
    if d:
        ax.add_patch(Circle((x + 1.6, 2.9), 0.14, fc="none", ec=GREY, lw=1.2, ls="--"))
        arrow(ax, (x + 1.6, 3.05), (x + 1.6, 2.75 + d), color=RED, lw=1.4, ms=9)
    ax.add_patch(Circle((x + 1.6, 2.9 + d), 0.14, fc=INK, ec=INK))
    ax.text(x + 1.6, -0.2, lab, ha="center", va="center", fontsize=12, fontweight="bold")
    if k < 2:
        arrow(ax, (x + 3.8, 3.2), (x + 5.6, 3.2))
ax.text(16.8, 3.4, "3mm쯤", ha="left", va="center", fontsize=12, color=RED, fontweight="bold")
ax.set_ylim(-0.8, 6.4)
ax.set_xlim(0, 19.0)
save(fig, "b08-dot.svg")

# 그림 6. 머리카락 뿌리를 옆에서 자른 모습
fig, ax = canvas(10.0, 5.0, 16.0, 8.0)
ax.add_patch(Rectangle((1.0, 1.0), 14.0, 4.6, fc=SKIN, ec=INK, lw=1.4))
ax.add_patch(Rectangle((1.0, 5.0), 14.0, 0.6, fc=SKIN_TOP, ec="none"))
hair_root(ax, 8.0, 2.3, 5.6)
ax.add_patch(Ellipse((8.0, 2.3), 1.3, 1.0, fc=CELL, ec=RED, lw=2.2))
ax.plot([8.0, 8.0, 8.6], [2.6, 5.6, 7.6], color=INK, lw=3)
ax.plot([2.0, 7.0], [3.0, 3.0], color=NERVE, lw=1.6)
ax.plot([2.0, 7.4], [1.8, 2.1], color=BLOOD, lw=1.6)
ax.text(9.2, 7.0, "굳은 세포", ha="left", va="center", fontsize=11)
ax.text(11.0, 2.2, "둥근 끝", ha="left", va="center", fontsize=12, color=RED, fontweight="bold")
arrow(ax, (10.9, 2.2), (8.8, 2.3), color=RED, lw=1.4, ms=10)
ax.text(2.0, 3.4, "신경", ha="left", va="center", fontsize=11, color=NERVE, fontweight="bold")
ax.text(2.0, 1.4, "핏줄", ha="left", va="center", fontsize=11, color=BLOOD, fontweight="bold")
ax.text(1.4, 5.3, "피부 겉", ha="left", va="center", fontsize=10, color="#777")
ax.set_ylim(0.6, 8.0)
save(fig, "b08-hair.svg")

# 그림 7. 머리카락 자르기와 뽑기
fig, ax = canvas(11.0, 5.0, 18.0, 8.2)
for x0, pull in [(0.6, False), (9.6, True)]:
    w = 7.8
    cx = x0 + w / 2
    ax.add_patch(Rectangle((x0, 1.4), w, 3.6, fc=SKIN, ec=INK, lw=1.4))
    ax.add_patch(Rectangle((x0, 4.5), w, 0.5, fc=SKIN_TOP, ec="none"))
    lift = 0.5 if pull else 0.0
    hair_root(ax, cx, 2.3, 5.0, nerve_color=RED if pull else NERVE, lift=lift)
    if pull:
        ax.plot([cx, cx], [2.6 + lift, 7.0], color=INK, lw=3)
        arrow(ax, (cx + 0.6, 6.2), (cx + 0.6, 7.6), color=RED, lw=2.2)
        ax.text(cx, 0.7, "뽑기", ha="center", va="center", fontsize=12)
        ax.text(cx + 1.2, 7.4, "따끔", ha="left", va="center", fontsize=13, color=RED, fontweight="bold")
    else:
        ax.plot([cx, cx], [2.6, 6.2], color=INK, lw=3)
        ax.plot([cx, cx], [6.6, 7.6], color=INK, lw=3)
        ax.plot([cx - 0.8, cx + 0.8], [6.4, 6.4], color=INK, lw=1.4, ls="--")
        ax.text(cx, 0.7, "자르기", ha="center", va="center", fontsize=12)
        ax.text(cx + 1.2, 7.4, "안 아픔", ha="left", va="center", fontsize=13, fontweight="bold")
ax.plot([9.0, 9.0], [0.4, 7.9], color=GREY, lw=1.2, ls="--")
ax.set_ylim(0.2, 8.2)
save(fig, "b08-pull.svg")
