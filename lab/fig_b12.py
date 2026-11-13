"""인체 12편 그림 만들기. 실행: python lab/fig_b12.py  → docs/body/img/12/*.svg

확인용 PNG: FIG_FMT=png FIG_OUT=<폴더> python lab/fig_b12.py
글자는 SVG 안에 글자로 남긴다(글꼴 모양을 파일에 넣지 않는다). 보는 쪽 글꼴로 그려진다.
그림 안 글씨는 낱말과 숫자만 둔다. 강조는 빨강 하나.
"""
import math
import os
import random

import matplotlib

FMT = os.environ.get("FIG_FMT", "svg")
matplotlib.use("svg" if FMT == "svg" else "agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Ellipse, FancyArrowPatch, FancyBboxPatch, Polygon, Rectangle

OUT = os.environ.get("FIG_OUT") or os.path.join(os.path.dirname(__file__), "..", "docs", "body", "img", "12")
os.makedirs(OUT, exist_ok=True)

plt.rcParams.update({
    "font.family": ["Apple SD Gothic Neo", "Noto Sans KR", "Malgun Gothic", "sans-serif"],
    "svg.fonttype": "none",
    "text.color": "#222",
    "figure.facecolor": "white",
    "savefig.facecolor": "white",
})

RED, GREY, INK, NOTE, YEL = "#e4572e", "#c9ccd1", "#555", "#fffdf5", "#f6c445"
SKIN = "#f6d8c4"
CELL = "#fbe3dc"
GUARD = "#ffffff"
GUARD_EC = "#4a6f96"
BUG = "#8fb58f"
BUG_EC = "#4f7a4f"
BLOOD = "#f3c1b8"


def save(fig, name):
    if FMT != "svg":
        name = name.replace(".svg", "." + FMT)
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


def label(ax, x, y, t, color="#222", fs=11, ha="center", bold=True):
    ax.text(x, y, t, ha=ha, va="center", fontsize=fs, color=color, fontweight="bold" if bold else "normal")


def bug(ax, x, y, r=0.22, spikes=10, fc=BUG, ec=BUG_EC):
    """별 모양 침입자. spikes 를 바꾸면 겉모습이 다른 종류가 된다."""
    pts = []
    for k in range(spikes):
        a = 2 * math.pi * k / spikes
        rr = r if k % 2 == 0 else r * 0.7
        pts.append((x + rr * math.cos(a), y + rr * math.sin(a)))
    ax.add_patch(Polygon(pts, closed=True, fc=fc, ec=ec, lw=1))


def square_bug(ax, x, y, r=0.22):
    """겉모습이 다른 침입자(네모)."""
    ax.add_patch(Rectangle((x - r, y - r), 2 * r, 2 * r, fc="#c9b6dc", ec="#6e5a8a", lw=1))


def guard(ax, x, y, r=0.6, eat=False, ec=GUARD_EC, lw=1.6):
    ax.add_patch(Circle((x, y), r, fc=GUARD, ec=ec, lw=lw))
    ax.add_patch(Circle((x - r * 0.3, y + r * 0.25), r * 0.1, fc=INK, ec=INK))
    ax.add_patch(Circle((x + r * 0.15, y + r * 0.25), r * 0.1, fc=INK, ec=INK))
    if eat:
        bug(ax, x + r * 0.1, y - r * 0.25, r=r * 0.28)


def thermo(ax, x, lvl, set_lvl, top_lbl=None):
    """온도계. lvl=지금 체온 높이(0~1), set_lvl=맞춰 둔 온도(빨간 점선)."""
    h = 4.2
    ax.add_patch(FancyBboxPatch((x - 0.25, 1.8), 0.5, h, boxstyle="round,pad=0.05", fc="white", ec=INK, lw=1.4))
    ax.add_patch(Circle((x, 1.8), 0.5, fc="#e98a72", ec=INK, lw=1.4))
    ax.add_patch(Rectangle((x - 0.13, 1.8), 0.26, h * lvl, fc="#e98a72", ec="none"))
    ax.plot([x - 0.8, x + 0.8], [1.8 + h * set_lvl] * 2, color=RED, lw=2, ls="--")
    if top_lbl:
        label(ax, x, 7.0, top_lbl, fs=11)


random.seed(7)

# 1. 세균과 바이러스: 바이러스는 세포 안에 들어가야 늘어나요
fig, ax = canvas(10.0, 4.6, 16.0, 7.4)
ax.add_patch(Circle((9.6, 3.8), 2.6, fc=CELL, ec=INK, lw=1.6))
label(ax, 9.6, 0.7, "세포")
ax.add_patch(FancyBboxPatch((1.4, 3.4), 2.4, 0.9, boxstyle="round,pad=0.4", fc="#d7e8c9", ec=BUG_EC, lw=1.4))
label(ax, 2.6, 1.9, "세균")
for x, y in [(6.0, 6.4), (6.6, 6.8)]:
    bug(ax, x, y, r=0.18)
arrow(ax, (6.9, 6.3), (7.9, 5.6), color=INK, lw=1.4, ms=12)
for k in range(9):
    a = 2 * math.pi * k / 9
    bug(ax, 9.6 + 1.3 * math.cos(a), 3.8 + 1.3 * math.sin(a), r=0.18, fc=RED, ec="#a33a1f")
bug(ax, 9.6, 3.8, r=0.18, fc=RED, ec="#a33a1f")
label(ax, 6.3, 7.3, "바이러스", fs=11)
label(ax, 12.9, 6.2, "늘어남", color=RED, fs=11)
save(fig, "b12-size.svg")

# 2. 성벽: 피부, 코와 목, 위, 입
fig, ax = canvas(11.0, 4.0, 18.0, 6.4)
for k, (x, title, sub) in enumerate([(2.2, "피부", "단단한 벽"), (6.8, "코와 목", "끈적한 물"),
                                    (11.4, "위", "위액"), (15.8, "입", "침")]):
    box(ax, x - 1.9, 1.4, 3.8, 3.8, fc=NOTE)
    label(ax, x, 4.6, title, fs=12)
    label(ax, x, 1.9, sub, fs=10, bold=False)
    if k == 0:
        ax.add_patch(Rectangle((x - 1.4, 2.6), 2.8, 0.7, fc=SKIN, ec=INK, lw=1.2))
        bug(ax, x - 0.4, 3.7, r=0.2)
        bug(ax, x + 0.5, 3.6, r=0.2)
    elif k == 1:
        ax.add_patch(Ellipse((x, 3.1), 2.4, 0.9, fc="#e8f1d8", ec=BUG, lw=1.2))
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
save(fig, "b12-walls.svg")

# 3. 삼키는 흰 세포: 다가가기 → 삼키기 → 녹이기
fig, ax = canvas(11.0, 3.8, 18.0, 6.2)
for k, (x, stage) in enumerate([(2.6, 0), (8.6, 1), (14.6, 2)]):
    if stage == 0:
        guard(ax, x - 0.6, 3.6, r=1.0)
        bug(ax, x + 1.2, 3.6, r=0.35)
        arrow(ax, (x + 0.5, 3.6), (x + 0.85, 3.6), color=INK, lw=1.2, ms=10)
        lab = "다가가기"
    elif stage == 1:
        guard(ax, x, 3.6, r=1.1, ec=RED, lw=2.2)
        bug(ax, x + 0.3, 3.2, r=0.35)
        lab = "삼키기"
    else:
        guard(ax, x, 3.6, r=1.0)
        for j in range(4):
            ax.add_patch(Circle((x - 0.3 + j * 0.2, 3.2 + 0.1 * (j % 2)), 0.06, fc=BUG, ec=BUG))
        lab = "녹이기"
    label(ax, x, 1.6, lab, fs=12, color=RED if stage == 1 else "#222")
    if k < 2:
        arrow(ax, (x + 2.0, 3.6), (x + 3.8, 3.6))
save(fig, "b12-eat.svg")

# 4. 침입자가 들어온 곳: 핏줄이 넓어져 흰 세포가 몰려와요
fig, ax = canvas(11.0, 4.4, 18.0, 7.2)
for k, (ox, wide) in enumerate([(0.6, False), (9.6, True)]):
    hw = 1.5 if wide else 0.7
    ax.add_patch(Rectangle((ox, 3.6 - hw), 7.8, 2 * hw, fc=BLOOD, ec=RED if wide else INK, lw=2 if wide else 1.2))
    n = 7 if wide else 2
    for j in range(n):
        gx = ox + 0.8 + j * (6.4 / max(n - 1, 1)) if n > 1 else ox + 3.9
        gy = 3.6 + (0.6 if j % 2 else -0.6) * (1 if wide else 0)
        guard(ax, gx, gy, r=0.42 if wide else 0.4)
    if wide:
        bug(ax, ox + 3.9, 3.6 + hw + 0.6, r=0.3)
        bug(ax, ox + 5.1, 3.6 + hw + 0.5, r=0.26)
    label(ax, ox + 3.9, 0.9, "침입자가 들어온 곳" if wide else "평소", fs=12, color=RED if wide else "#222")
ax.plot([9.0, 9.0], [0.5, 6.6], color=GREY, lw=1)
save(fig, "b12-swell.svg")

# 5. 열: 맞춘 온도(빨간 점선)가 먼저 오르고 체온이 따라 올라가요
fig, ax = canvas(11.0, 4.8, 18.0, 7.8)
thermo(ax, 2.6, 0.5, 0.5, "평소")
label(ax, 4.0, 1.8 + 4.2 * 0.5, "37도", fs=10, ha="left", bold=False)
thermo(ax, 8.6, 0.5, 0.78, "싸움 시작")
label(ax, 10.0, 1.8 + 4.2 * 0.78, "맞춘 온도", color=RED, fs=10, ha="left")
label(ax, 10.0, 1.8 + 4.2 * 0.5, "체온", fs=10, ha="left", bold=False)
label(ax, 8.6, 0.6, "으슬으슬", fs=11, color=RED)
thermo(ax, 14.6, 0.78, 0.78, "떨린 뒤")
label(ax, 14.6, 0.6, "열", fs=11)
arrow(ax, (4.6, 4.0), (6.6, 4.0))
arrow(ax, (10.8, 4.0), (12.8, 4.0))
save(fig, "b12-fever.svg")

# 6. 기억하는 흰 세포: 처음 / 두 번째
fig, ax = canvas(11.0, 4.6, 18.0, 7.6)
ax.plot([1.0, 17.0], [1.4, 1.4], color=INK, lw=1.4)
label(ax, 16.6, 0.8, "시간", fs=10, bold=False)
xs1 = [1.5 + t * 0.12 for t in range(50)]
ys1 = [1.4 + 2.0 * max(0, math.sin(math.pi * max(0, t - 15) / 35)) for t in range(50)]
ax.plot(xs1, ys1, color=GUARD_EC, lw=2.4)
xs2 = [9.5 + t * 0.12 for t in range(50)]
ys2 = [1.4 + 4.6 * max(0, math.sin(math.pi * max(0, t - 4) / 46)) for t in range(50)]
ax.plot(xs2, ys2, color=RED, lw=2.8)
bug(ax, 1.7, 1.9, r=0.25)
bug(ax, 9.7, 1.9, r=0.25)
label(ax, 4.9, 4.2, "처음", color=GUARD_EC, fs=12)
label(ax, 12.8, 6.6, "두 번째", color=RED, fs=12)
label(ax, 0.6, 4.0, "싸우는\n흰 세포 수", fs=9, bold=False)
save(fig, "b12-memory.svg")

# 7. 겉모습이 다른 바이러스는 기억이 맞지 않아요
fig, ax = canvas(11.0, 4.6, 18.0, 7.4)
for ox, same in [(0.6, True), (9.6, False)]:
    guard(ax, ox + 1.8, 3.6, r=1.0)
    ax.add_patch(Rectangle((ox + 0.3, 5.2), 1.2, 1.2, fc=NOTE, ec=INK, lw=1))
    bug(ax, ox + 0.9, 5.8, r=0.35)
    label(ax, ox + 2.4, 5.8, "기억", fs=10, ha="left", bold=False)
    if same:
        bug(ax, ox + 5.8, 3.6, r=0.5)
        label(ax, ox + 5.8, 2.3, "같은 감기", fs=11)
        arrow(ax, (ox + 3.0, 3.6), (ox + 5.0, 3.6), color=RED, lw=2.2)
        label(ax, ox + 4.0, 4.2, "바로", color=RED, fs=11)
    else:
        square_bug(ax, ox + 5.8, 3.6, r=0.45)
        label(ax, ox + 5.8, 2.3, "다른 감기", fs=11)
        ax.plot([ox + 3.0, ox + 5.0], [3.6, 3.6], color=GREY, lw=2, ls="--")
        label(ax, ox + 4.0, 4.2, "?", color="#888", fs=14)
ax.plot([9.0, 9.0], [1.4, 7.0], color=GREY, lw=1)
save(fig, "b12-kinds.svg")

# 8. 해 보기: 밀가루 손 도장
fig, ax = canvas(10.0, 3.8, 16.0, 6.0)
for k, (x, n, lab) in enumerate([(2.6, 26, "씻기 전"), (8.0, 12, "물로만"), (13.4, 3, "비누로")]):
    ax.add_patch(Rectangle((x - 2.0, 1.4), 4.0, 4.2, fc="#2f2f3a", ec=INK, lw=1.2))
    ax.add_patch(FancyBboxPatch((x - 0.9, 2.0), 1.8, 2.4, boxstyle="round,pad=0.35", fc="none", ec="#6b6b78", lw=1.2))
    for j in range(n):
        ax.add_patch(Circle((x + random.uniform(-0.9, 0.9), random.uniform(2.1, 4.3)), 0.07, fc="white", ec="white"))
    label(ax, x, 0.8, lab)
save(fig, "b12-flour.svg")
