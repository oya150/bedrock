"""인체 7편 그림 만들기. 실행: python lab/fig_b07.py  → docs/body/img/07/*.svg

글자는 SVG 안에 글자로 남긴다(글꼴 모양을 파일에 넣지 않는다). 보는 쪽 글꼴로 그려진다.
강조는 빨강 하나. 물(땀)은 파랑, 피부는 살구색으로 칠한다. 그림 안 글씨는 낱말과 숫자만.
확인용 PNG: FIG_FMT=png FIG_OUT=/어딘가 python lab/fig_b07.py
"""
import math
import os

import matplotlib

matplotlib.use("svg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Ellipse, FancyArrowPatch, FancyBboxPatch, Polygon, Rectangle

FMT = os.environ.get("FIG_FMT", "svg")
OUT = os.environ.get("FIG_OUT") or os.path.join(os.path.dirname(__file__), "..", "docs", "body", "img", "07")
os.makedirs(OUT, exist_ok=True)

plt.rcParams.update({
    "font.family": ["Apple SD Gothic Neo", "Noto Sans KR", "Malgun Gothic", "sans-serif"],
    "svg.fonttype": "none",
    "text.color": "#222",
    "figure.facecolor": "white",
    "savefig.facecolor": "white",
})

RED, GREY, INK, YEL = "#e4572e", "#c9ccd1", "#555", "#f6c445"
CELL = "#fbe3dc"
SKIN = "#f6d8c4"
SKIN_TOP = "#f2c9b0"
SKIN_WARM = "#f5c2b0"
BLOOD = "#c0392b"
WATER = "#7da2c8"
WATER_LIGHT = "#dbe7f3"


def save(fig, name):
    name = name.rsplit(".", 1)[0] + "." + FMT
    fig.savefig(os.path.join(OUT, name), bbox_inches="tight", pad_inches=0.25, dpi=110)
    plt.close(fig)


def canvas(w, h, xmax, ymax):
    fig, ax = plt.subplots(figsize=(w, h))
    ax.set_xlim(0, xmax); ax.set_ylim(0, ymax); ax.axis("off")
    return fig, ax


def box(ax, x, y, w, h, fc="white", ec=INK, lw=1.6):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.08", fc=fc, ec=ec, lw=lw))


def arrow(ax, a, b, color=INK, lw=2, rad=0.0, ms=18):
    ax.add_patch(FancyArrowPatch(a, b, arrowstyle="-|>", mutation_scale=ms, color=color, lw=lw,
                                 connectionstyle=f"arc3,rad={rad}"))


def wavy(ax, x, y, h=1.0, color=RED, lw=1.6):
    ys = [y + h * t / 30 for t in range(31)]
    xs = [x + 0.12 * math.sin(t * 0.6) for t in range(31)]
    ax.plot(xs, ys, color=color, lw=lw)


def thermo(ax, x, y, level, h=3.0):
    ax.add_patch(FancyBboxPatch((x - 0.18, y), 0.36, h, boxstyle="round,pad=0.05", fc="white", ec=INK, lw=1.4))
    ax.add_patch(Circle((x, y), 0.36, fc=RED, ec=INK, lw=1.4))
    ax.add_patch(Rectangle((x - 0.1, y), 0.2, h * level, fc=RED, ec="none"))


def drop(ax, x, y, s=1.0, alpha=1.0):
    ax.add_patch(Ellipse((x, y), 0.8 * s, 0.6 * s, fc=WATER, ec=INK, lw=1, alpha=alpha))


def skin(ax, x, y, w, h, top=0.6, fc=SKIN):
    ax.add_patch(Rectangle((x, y), w, h, fc=fc, ec=INK, lw=1.4))
    ax.add_patch(Rectangle((x, y + h - top), w, top, fc=SKIN_TOP, ec="none"))


# 그림 1. 가만히 있을 때와 뛸 때 근육 세포의 열
fig, ax = canvas(10.0, 4.0, 16.0, 6.6)
for x, busy, lab in [(3.8, False, "가만히"), (12.0, True, "뛸 때")]:
    for j in range(3):
        ax.add_patch(Ellipse((x - 1.2 + j * 1.2, 2.6), 1.0, 2.2, fc=CELL, ec=INK, lw=1.2))
    n = 6 if busy else 2
    for j in range(n):
        wavy(ax, x - 1.5 + j * (3.0 / max(n - 1, 1)), 3.9, 1.6 if busy else 0.8,
             color=RED if busy else GREY, lw=1.8 if busy else 1.4)
    ax.text(x, 0.7, lab, ha="center", va="center", fontsize=13, fontweight="bold",
            color=RED if busy else "#222")
ax.text(3.8, 5.3, "열", ha="center", va="center", fontsize=11, color="#777")
ax.text(12.0, 6.1, "열", ha="center", va="center", fontsize=11, color=RED, fontweight="bold")
ax.plot([8.0, 8.0], [0.3, 6.3], color=GREY, lw=1.2, ls="--")
ax.text(8.0, 0.0, "근육 세포", ha="center", va="center", fontsize=10, color="#777")
ax.set_ylim(-0.4, 6.6)
save(fig, "b07-heat.svg")

# 그림 2. 온도 지킴이가 37도쯤을 지켜요
fig, ax = canvas(11.0, 4.8, 18.0, 8.0)
thermo(ax, 9.0, 2.0, 0.55, h=4.0)
ax.text(9.0, 1.0, "37도쯤", ha="center", va="center", fontsize=14, fontweight="bold")
ax.text(9.0, 7.4, "온도 지킴이 (뇌)", ha="center", va="center", fontsize=12)
box(ax, 0.6, 2.6, 6.2, 3.6, fc="#fdecea", ec=RED, lw=2.0)
ax.text(3.7, 5.5, "더울 때", ha="center", va="center", fontsize=13, color=RED, fontweight="bold")
ax.text(3.7, 4.3, "핏줄 넓게", ha="center", va="center", fontsize=12)
ax.text(3.7, 3.3, "땀", ha="center", va="center", fontsize=12)
box(ax, 11.2, 2.6, 6.2, 3.6, fc="#f4f6f8")
ax.text(14.3, 5.5, "추울 때", ha="center", va="center", fontsize=13, fontweight="bold")
ax.text(14.3, 4.3, "핏줄 좁게", ha="center", va="center", fontsize=12)
ax.text(14.3, 3.3, "떨림", ha="center", va="center", fontsize=12)
arrow(ax, (6.95, 4.4), (8.5, 4.4), color=RED, lw=2)
arrow(ax, (11.05, 4.4), (9.5, 4.4), color=INK, lw=2)
save(fig, "b07-keep.svg")

# 그림 3. 피부 핏줄: 더울 때 넓게, 추울 때 좁게
fig, ax = canvas(11.0, 4.6, 18.0, 7.6)
for x0, hot in [(0.6, True), (9.6, False)]:
    w = 7.8
    skin(ax, x0, 0.8, w, 3.6, fc=SKIN_WARM if hot else SKIN)
    ax.plot([x0 + 0.3, x0 + w - 0.3], [3.0, 3.0], color=BLOOD, lw=14 if hot else 3.5, solid_capstyle="round")
    n = 5 if hot else 1
    for j in range(n):
        xx = x0 + w / 2 + (j - (n - 1) / 2) * 1.25
        wavy(ax, xx, 4.6, 1.5 if hot else 0.8, color=RED if hot else GREY, lw=1.8 if hot else 1.4)
    ax.text(x0 + w / 2, 7.1, "더울 때" if hot else "추울 때", ha="center", va="center", fontsize=13,
            fontweight="bold", color=RED if hot else "#222")
    ax.text(x0 + w / 2, 1.6, "핏줄 넓게" if hot else "핏줄 좁게", ha="center", va="center", fontsize=11)
ax.text(0.2, 3.0, "핏줄", ha="right", va="center", fontsize=10, color="#777")
ax.text(0.2, 4.1, "피부 겉", ha="right", va="center", fontsize=10, color="#777")
ax.text(7.4, 5.6, "열", ha="left", va="center", fontsize=11, color=RED, fontweight="bold")
ax.text(14.0, 5.2, "열", ha="left", va="center", fontsize=11, color="#777")
ax.set_xlim(-1.4, 18.0)
save(fig, "b07-vessel.svg")

# 그림 4. 땀방울이 마르며 열을 가져가요
fig, ax = canvas(11.0, 4.2, 18.0, 6.8)
skin(ax, 1.0, 0.9, 16.0, 1.6, top=0.4)
ax.text(9.0, 1.4, "피부", ha="center", va="center", fontsize=11)
sizes = [1.0, 0.8, 0.55, 0.3]
for k, x in enumerate([3.0, 7.0, 11.0, 15.0]):
    drop(ax, x, 2.5 + 0.27 * sizes[k], s=sizes[k])
for x in [7.0, 11.0, 15.0]:
    for j in range(2):
        wavy(ax, x - 0.3 + j * 0.6, 3.3, 1.4, color=RED, lw=1.6)
    arrow(ax, (x, 4.8), (x, 5.9), color=RED, lw=1.6, ms=12)
ax.text(3.0, 3.7, "땀방울", ha="center", va="center", fontsize=11)
ax.text(11.0, 6.4, "열", ha="center", va="center", fontsize=12, color=RED, fontweight="bold")
arrow(ax, (2.0, 0.4), (16.0, 0.4), color=INK, lw=1.2, ms=10)
ax.text(9.0, 0.0, "시간", ha="center", va="center", fontsize=10)
ax.set_ylim(-0.4, 6.8)
save(fig, "b07-dry.svg")

# 그림 5. 마르는 땀과 흘러 떨어진 땀
fig, ax = canvas(11.0, 4.8, 18.0, 7.8)
skin(ax, 0.6, 1.4, 7.6, 2.2, top=0.5)
drop(ax, 4.4, 3.8, s=0.7)
for j in range(3):
    wavy(ax, 3.7 + j * 0.7, 4.3, 1.5, color=RED, lw=1.8)
arrow(ax, (4.4, 6.0), (4.4, 6.9), color=RED, lw=1.6, ms=12)
ax.text(4.4, 0.7, "마름", ha="center", va="center", fontsize=13, fontweight="bold", color=RED)
ax.text(5.6, 6.5, "열", ha="left", va="center", fontsize=11, color=RED, fontweight="bold")
skin(ax, 9.8, 1.4, 5.4, 2.2, top=0.5)
ax.plot([14.2, 15.3, 15.35, 15.35], [3.68, 3.68, 3.5, 2.3], color=WATER, lw=3, solid_capstyle="round")
ax.add_patch(Ellipse((15.4, 1.75), 0.45, 0.65, fc=WATER, ec=INK, lw=1))
arrow(ax, (15.4, 1.3), (15.4, 0.4), color=INK, lw=1.4, ms=12)
wavy(ax, 12.5, 3.9, 0.7, color=GREY, lw=1.4)
ax.text(13.6, 0.7, "떨어짐", ha="center", va="center", fontsize=13, fontweight="bold")
ax.text(13.0, 5.0, "열", ha="left", va="center", fontsize=11, color="#777")
ax.plot([9.0, 9.0], [0.3, 7.3], color=GREY, lw=1.2, ls="--")
save(fig, "b07-drip.svg")

# 그림 6. 땀샘에서 땀구멍까지
fig, ax = canvas(9.0, 5.0, 14.0, 8.2)
skin(ax, 1.0, 0.6, 12.0, 5.6, top=0.8)
ax.text(1.4, 5.8, "피부 겉", ha="left", va="center", fontsize=10, color="#777")
ys = [1.9 + 4.3 * t / 39 for t in range(40)]
xs = [7.0 + 0.35 * math.sin(t * 0.8) for t in range(40)]
ax.plot(xs, ys, color=WATER, lw=2.4)
for k in range(5):
    ax.add_patch(Ellipse((7.0 + 0.35 * math.cos(k * 1.3), 1.5 + 0.2 * math.sin(k * 1.3)), 1.4, 0.7,
                         angle=k * 36, fc="none", ec=WATER, lw=2))
ax.text(8.4, 1.4, "땀샘", ha="left", va="center", fontsize=13, fontweight="bold")
ax.text(7.7, 3.8, "관", ha="left", va="center", fontsize=11)
top_x = xs[-1]
drop(ax, top_x, 6.45, s=0.6)
arrow(ax, (top_x + 1.9, 7.4), (top_x + 0.35, 6.4), color=RED, lw=1.6, ms=12)
ax.text(top_x + 2.0, 7.5, "땀구멍", ha="left", va="center", fontsize=13, color=RED, fontweight="bold")
ax.set_ylim(0.2, 8.2)
save(fig, "b07-gland.svg")

# 그림 7. 모공과 땀구멍
fig, ax = canvas(11.0, 5.0, 18.0, 8.4)
skin(ax, 1.0, 1.0, 16.0, 5.0, top=0.8)
ax.add_patch(Polygon([(4.6, 6.0), (5.4, 6.0), (5.3, 2.4), (4.7, 2.4)], closed=True, fc=SKIN_TOP, ec=INK, lw=1.2))
ax.plot([5.0, 5.0, 5.9], [2.6, 6.0, 7.9], color=INK, lw=2.6)
ax.add_patch(Ellipse((6.1, 3.8), 1.0, 0.8, fc=YEL, ec=INK, lw=1))
arrow(ax, (5.65, 3.95), (5.3, 4.5), color=INK, lw=1.2, ms=9)
ax.text(6.8, 3.8, "기름", ha="left", va="center", fontsize=11)
ax.text(6.2, 7.6, "털", ha="left", va="center", fontsize=11)
arrow(ax, (3.0, 7.3), (4.55, 6.1), color=RED, lw=1.6, ms=12)
ax.text(2.9, 7.6, "모공", ha="center", va="center", fontsize=13, color=RED, fontweight="bold")
xs = [12.0 + 0.3 * math.sin(t * 0.9) for t in range(20)]
ys = [2.2 + 3.8 * t / 19 for t in range(20)]
ax.plot(xs, ys, color=WATER, lw=2)
ax.add_patch(Circle((12.0, 2.0), 0.6, fc=WATER_LIGHT, ec=WATER, lw=1.6))
ax.text(12.8, 2.0, "땀샘", ha="left", va="center", fontsize=11)
drop(ax, xs[-1], 6.2, s=0.5)
ax.text(xs[-1] + 0.6, 7.0, "땀구멍", ha="left", va="center", fontsize=13, fontweight="bold")
ax.text(5.0, 0.4, "털, 기름", ha="center", va="center", fontsize=12)
ax.text(12.3, 0.4, "땀", ha="center", va="center", fontsize=12)
ax.set_ylim(-0.1, 8.4)
save(fig, "b07-pores.svg")
