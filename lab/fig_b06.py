"""인체 6편 그림 만들기. 실행: python lab/fig_b06.py  → docs/body/img/06/*.svg

확인용 PNG: FIG_FMT=png FIG_OUT=<폴더> python lab/fig_b06.py
글자는 SVG 안에 글자로 남긴다(글꼴 모양을 파일에 넣지 않는다). 보는 쪽 글꼴로 그려진다.
강조는 빨강 하나. 그림 안 글씨는 낱말과 숫자만 둔다.
"""
import math
import os
import random

import matplotlib

FMT = os.environ.get("FIG_FMT", "svg")
matplotlib.use("svg" if FMT == "svg" else "agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Arc, Circle, Ellipse, FancyArrowPatch, Polygon, Rectangle

OUT = os.environ.get("FIG_OUT") or os.path.join(os.path.dirname(__file__), "..", "docs", "body", "img", "06")
os.makedirs(OUT, exist_ok=True)

plt.rcParams.update({
    "font.family": ["Apple SD Gothic Neo", "Noto Sans KR", "Malgun Gothic", "sans-serif"],
    "svg.fonttype": "none",
    "text.color": "#222",
    "figure.facecolor": "white",
    "savefig.facecolor": "white",
})

RED, GREY, INK = "#e4572e", "#c9ccd1", "#555"
WALL = "#9b6b63"       # 핏줄 벽
INSIDE = "#f7e3de"     # 핏줄 안
CELLRED = "#c96a5e"    # 빨간 세포(차분한 색)
PLATE = "#f6c445"      # 혈소판
FIBER = "#8a6d3b"      # 실
SKIN = "#f6d8c4"
SCAB = "#7a3b2e"
NEW = "#fbe3dc"

random.seed(6)


def save(fig, name):
    if FMT != "svg":
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


def vessel(ax, x0, x1, y, h, gap=None, rough=False):
    """가로 핏줄: 위아래 벽. gap=(xa, xb)면 위 벽에 구멍. rough면 구멍 가장자리에 빨간 거친 곳."""
    ax.add_patch(Rectangle((x0, y), x1 - x0, h, fc=INSIDE, ec="none"))
    ax.plot([x0, x1], [y, y], color=WALL, lw=3)
    if gap:
        ax.plot([x0, gap[0]], [y + h, y + h], color=WALL, lw=3)
        ax.plot([gap[1], x1], [y + h, y + h], color=WALL, lw=3)
        if rough:
            for gx, d in ((gap[0], -1), (gap[1], 1)):
                xs = [gx + d * k * 0.12 for k in range(5)]
                ys = [y + h + (0.12 if k % 2 else -0.12) for k in range(5)]
                ax.plot(xs, ys, color=RED, lw=2.4)
    else:
        ax.plot([x0, x1], [y + h, y + h], color=WALL, lw=3)


def rbc(ax, x, y, r=0.22):
    ax.add_patch(Ellipse((x, y), 2 * r, 1.6 * r, fc=CELLRED, ec=INK, lw=0.6))


def plate(ax, x, y, spiky=False, s=1.0, ec=INK):
    if spiky:
        pts = []
        for k in range(12):
            a = 2 * math.pi * k / 12
            rr = (0.19 if k % 2 == 0 else 0.10) * s
            pts.append((x + rr * math.cos(a), y + rr * math.sin(a)))
        ax.add_patch(Polygon(pts, closed=True, fc=PLATE, ec=ec, lw=0.8))
    else:
        ax.add_patch(Ellipse((x, y), 0.3 * s, 0.16 * s, fc=PLATE, ec=ec, lw=0.6))


# 1. 다친 핏줄이 오므라들어요
fig, ax = canvas(11.0, 3.8, 18.0, 6.2)
vessel(ax, 0.6, 7.6, 2.0, 2.0, gap=(3.6, 4.6))
for k in range(8):
    rbc(ax, 1.0 + k * 0.8, 3.0)
for k in range(5):
    rbc(ax, 4.1 + 0.15 * k, 4.4 + k * 0.35)
ax.text(4.1, 1.0, "다친 핏줄", ha="center", va="center", fontsize=12, fontweight="bold")
arrow(ax, (8.3, 3.0), (9.6, 3.0))
xs = [10.2, 12.4, 13.3, 14.3, 15.2, 17.4]
top = [4.0, 4.0, 3.5, 3.5, 4.0, 4.0]
bot = [2.0, 2.0, 2.5, 2.5, 2.0, 2.0]
ax.add_patch(Polygon(list(zip(xs, top)) + list(zip(xs[::-1], bot[::-1])), closed=True, fc=INSIDE, ec="none"))
ax.plot(xs[:3], top[:3], color=RED, lw=3)
ax.plot(xs[3:], top[3:], color=RED, lw=3)
ax.plot(xs, bot, color=RED, lw=3)
for k in range(2):
    rbc(ax, 13.7 + 0.12 * k, 4.0 + k * 0.35, r=0.18)
for x in (10.8, 11.8, 13.8, 15.8, 16.8):
    rbc(ax, x, 3.0, r=0.2)
ax.text(13.8, 1.0, "오므라든 핏줄", ha="center", va="center", fontsize=12, color=RED, fontweight="bold")
save(fig, "b06-squeeze.svg")

# 2. 평소 vs 다치면: 혈소판이 거친 곳에 달라붙어요
fig, ax = canvas(11.0, 4.4, 18.0, 7.2)
for x0, hurt, lab in [(0.6, False, "평소"), (9.6, True, "다치면")]:
    vessel(ax, x0, x0 + 7.6, 1.6, 2.6, gap=(x0 + 3.4, x0 + 4.6) if hurt else None, rough=hurt)
    for k in range(7):
        rbc(ax, x0 + 0.6 + k * 1.1, 2.3)
    if not hurt:
        for k in range(6):
            plate(ax, x0 + 1.0 + k * 1.2, 3.3)
    else:
        for k in range(4):
            plate(ax, x0 + 0.8 + k * 0.7, 3.3)
        plate(ax, x0 + 3.45, 4.05, spiky=True, s=1.3, ec=RED)
        plate(ax, x0 + 4.55, 4.05, spiky=True, s=1.3, ec=RED)
        ax.text(x0 + 4.0, 5.4, "거친 곳", ha="center", va="center", fontsize=11, color=RED, fontweight="bold")
    ax.text(x0 + 3.8, 0.7, lab, ha="center", va="center", fontsize=12, fontweight="bold")
ax.plot([8.9, 8.9], [0.4, 6.6], color=GREY, lw=1.2, ls="--")
ax.text(1.6, 4.6, "혈소판", ha="center", va="center", fontsize=11, fontweight="bold")
ax.plot([1.6, 1.9], [4.35, 3.45], color=INK, lw=1)
save(fig, "b06-plug.svg")

# 3. 붙어요 → 불러요 → 막아요 (구멍 둘레만 크게)
fig, ax = canvas(12.0, 3.8, 21.0, 6.6)
for i, (x0, lab) in enumerate([(0.4, "붙어요"), (7.4, "불러요"), (14.4, "막아요")]):
    vessel(ax, x0, x0 + 6.2, 1.4, 2.4, gap=(x0 + 2.6, x0 + 3.6), rough=(i < 2))
    cx, cy = x0 + 3.1, 3.8
    if i == 0:
        plate(ax, cx - 0.4, cy, spiky=True, s=1.4)
        for k in range(4):
            plate(ax, x0 + 0.6 + k * 1.4, 2.6)
    elif i == 1:
        plate(ax, cx - 0.4, cy, spiky=True, s=1.4)
        plate(ax, cx + 0.4, cy, spiky=True, s=1.4)
        for r in (0.6, 0.95):
            ax.add_patch(Arc((cx, cy), 2 * r, 2 * r, theta1=200, theta2=340, color=RED, lw=1.6))
        for k, px in enumerate((x0 + 0.7, x0 + 5.4)):
            plate(ax, px, 2.6, spiky=True, s=1.2)
            arrow(ax, (px + (0.3 if k == 0 else -0.3), 2.75), (cx + (-0.6 if k == 0 else 0.6), 3.3),
                  color=RED, lw=1.6, ms=12)
    else:
        for k in range(14):
            plate(ax, cx - 0.55 + (k % 5) * 0.28, cy - 0.3 + (k // 5) * 0.3, spiky=True, s=1.1, ec=RED)
        ax.text(cx, 5.3, "마개", ha="center", va="center", fontsize=12, color=RED, fontweight="bold")
    ax.text(x0 + 3.1, 0.6, lab, ha="center", va="center", fontsize=12, fontweight="bold")
for x in (6.9, 13.9):
    arrow(ax, (x - 0.2, 2.6), (x + 0.4, 2.6), lw=1.6, ms=14)
save(fig, "b06-call.svg")

# 4. 실 그물에 빨간 세포가 걸려요
fig, ax = canvas(10.0, 5.0, 16.4, 8.0)
clipbox = Rectangle((1.6, 1.2), 12.0, 5.6, fc="#fdf1ee", ec=GREY, lw=1)
ax.add_patch(clipbox)
for k in range(22):
    x1, y1 = random.uniform(2.0, 13.2), random.uniform(1.4, 6.6)
    a = random.uniform(0, math.pi)
    L = random.uniform(3.0, 6.0)
    ln, = ax.plot([x1 - L / 2 * math.cos(a), x1 + L / 2 * math.cos(a)],
                  [y1 - L / 2 * math.sin(a), y1 + L / 2 * math.sin(a)], color=FIBER, lw=1.0)
    ln.set_clip_path(clipbox)
for k in range(18):
    rbc(ax, random.uniform(2.8, 12.4), random.uniform(2.0, 6.0), r=0.32)
for k in range(10):
    plate(ax, random.uniform(2.8, 12.4), random.uniform(2.0, 6.0), spiky=True)
ax.plot([14.0, 14.6], [5.6, 5.6], color=FIBER, lw=1.8)
ax.text(14.8, 5.6, "실", ha="left", va="center", fontsize=11, fontweight="bold")
rbc(ax, 14.3, 4.4, r=0.25)
ax.text(14.8, 4.4, "빨간 세포", ha="left", va="center", fontsize=11, fontweight="bold")
plate(ax, 14.3, 3.2, spiky=True)
ax.text(14.8, 3.2, "혈소판", ha="left", va="center", fontsize=11, fontweight="bold")
save(fig, "b06-mesh.svg")

# 5. 그물이 오므라들어요: 처음 → 조금 지나서
fig, ax = canvas(11.0, 4.2, 18.0, 7.0)
for i, (cx, w, h, lab) in enumerate([(4.2, 6.0, 4.4, "처음"), (13.6, 3.8, 2.8, "조금 지나서")]):
    clip = Ellipse((cx, 3.8), w, h, fc="#fdf1ee", ec=RED if i else GREY, lw=2.4 if i else 1)
    ax.add_patch(clip)
    rng = random.Random(3)
    for k in range(16):
        x1, y1 = cx + rng.uniform(-w / 2, w / 2), 3.8 + rng.uniform(-h / 2, h / 2)
        a = rng.uniform(0, math.pi)
        ln, = ax.plot([x1 - w * math.cos(a), x1 + w * math.cos(a)],
                      [y1 - w * math.sin(a), y1 + w * math.sin(a)], color=FIBER, lw=1.0)
        ln.set_clip_path(clip)
    for k in range(9):
        rbc(ax, cx + rng.uniform(-w / 3, w / 3), 3.8 + rng.uniform(-h / 3.2, h / 3.2), r=0.3 if i == 0 else 0.26)
    ax.text(cx, 0.7, lab, ha="center", va="center", fontsize=12, color=RED if i else "#222", fontweight="bold")
arrow(ax, (8.0, 3.8), (10.6, 3.8), lw=2)
for dx, dy in ((-1, 1), (1, 1), (-1, -1), (1, -1)):
    arrow(ax, (13.6 + dx * 2.6, 3.8 + dy * 2.1), (13.6 + dx * 1.7, 3.8 + dy * 1.3), color=RED, lw=1.6, ms=12)
save(fig, "b06-shrink.svg")

# 6. 덩어리 → 딱지와 새살 → 딱지가 떨어져요
fig, ax = canvas(11.0, 4.4, 18.0, 7.2)
for k, (x0, stage) in enumerate([(0.4, 0), (6.4, 1), (12.4, 2)]):
    ax.add_patch(Rectangle((x0, 1.4), 5.2, 3.0, fc=SKIN, ec=INK, lw=1.2))
    if stage == 0:
        ax.add_patch(Polygon([(x0 + 1.8, 4.4), (x0 + 3.4, 4.4), (x0 + 2.9, 2.6), (x0 + 2.3, 2.6)], closed=True,
                             fc=CELLRED, ec=INK, lw=1))
        lab = "덩어리"
    elif stage == 1:
        ax.add_patch(Ellipse((x0 + 2.6, 4.5), 2.2, 0.6, fc=SCAB, ec=INK, lw=1))
        ax.add_patch(Polygon([(x0 + 1.9, 4.4), (x0 + 3.3, 4.4), (x0 + 2.9, 3.3), (x0 + 2.3, 3.3)], closed=True,
                             fc=NEW, ec=RED, lw=1.4))
        for j in range(4):
            ax.add_patch(Circle((x0 + 2.2 + j * 0.25, 3.7), 0.1, fc=NEW, ec=RED, lw=0.8))
        ax.text(x0 + 2.6, 5.4, "딱지", ha="center", va="center", fontsize=11, fontweight="bold")
        lab = "새살"
    else:
        ax.add_patch(Ellipse((x0 + 4.4, 5.8), 1.2, 0.4, fc=SCAB, ec=INK, lw=1))
        arrow(ax, (x0 + 3.2, 4.8), (x0 + 3.9, 5.5), color=INK, lw=1.2, ms=10)
        lab = "떨어져요"
    ax.text(x0 + 2.6, 0.7, lab, ha="center", va="center", fontsize=12, fontweight="bold",
            color=RED if stage == 1 else "#222")
for x0 in (0.4, 6.4):
    arrow(ax, (x0 + 5.3, 3.0), (x0 + 6.3, 3.0), lw=2.4)
save(fig, "b06-scab.svg")
