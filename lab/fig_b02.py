"""인체 2편 그림 만들기. 실행: python lab/fig_b02.py  → docs/body/img/02/*.svg

글자는 SVG 안에 글자로 남긴다(글꼴 모양을 파일에 넣지 않는다). 보는 쪽 글꼴로 그려진다.
그림 안 글씨는 낱말과 숫자만 둔다. 문장은 본문과 그림 설명에 쓴다.
강조색은 빨강 하나로, 지금 볼 곳에만 칠한다.
검토용 PNG가 필요하면 FIG_FMT=png FIG_OUT=<폴더> 로 실행한다.
"""
import math
import os

import matplotlib

matplotlib.use("svg")
import matplotlib.pyplot as plt
from matplotlib.patches import Arc, Circle, Ellipse, FancyArrowPatch, FancyBboxPatch, Rectangle

FMT = os.environ.get("FIG_FMT", "svg")
OUT = os.environ.get("FIG_OUT") or os.path.join(os.path.dirname(__file__), "..", "docs", "body", "img", "02")
os.makedirs(OUT, exist_ok=True)

plt.rcParams.update({
    "font.family": ["Apple SD Gothic Neo", "Noto Sans KR", "Malgun Gothic", "sans-serif"],
    "svg.fonttype": "none",
    "text.color": "#222",
    "figure.facecolor": "white",
    "savefig.facecolor": "white",
})

RED, GREY, INK, NOTE = "#e4572e", "#c9ccd1", "#555", "#fffdf5"
USED = "#8c9096"  # 다 쓴 숨은 어느 그림에서나 이 회색(4편도 같음)
SKIN = "#f6d8c4"
CELL = "#f3e6df"
BLOOD = "#f0d0c6"


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


def word(ax, x, y, t, fs=12, color="#222", bold=True, ha="center"):
    ax.text(x, y, t, ha=ha, va="center", fontsize=fs, color=color, fontweight="bold" if bold else "normal")


def kid(ax, cx, y, s=1.0):
    ax.add_patch(Circle((cx, y + 1.55 * s), 0.32 * s, fc="white", ec=INK, lw=1.6))
    ax.plot([cx, cx], [y + 1.23 * s, y + 0.55 * s], color=INK, lw=2)
    ax.plot([cx, cx - 0.3 * s], [y + 0.55 * s, y], color=INK, lw=2)
    ax.plot([cx, cx + 0.3 * s], [y + 0.55 * s, y], color=INK, lw=2)
    ax.plot([cx - 0.35 * s, cx + 0.35 * s], [y + 1.0 * s, y + 1.0 * s], color=INK, lw=2)


# 1. 숨 참기 놀이: 처음 → 답답 → 푸하
fig, ax = canvas(11.0, 4.0, 18.0, 6.6)
kid(ax, 2.6, 0.6, 1.6)
hy = 0.6 + 1.55 * 1.6
ax.add_patch(Circle((2.6, hy), 0.62, fc="#fbe3dc", ec=INK, lw=1.6))
ax.plot([2.32, 2.5], [hy + 0.12, hy + 0.12], color=INK, lw=1.6)
ax.plot([2.7, 2.88], [hy + 0.12, hy + 0.12], color=INK, lw=1.6)
ax.plot([2.5, 2.7], [hy - 0.22, hy - 0.22], color=INK, lw=1.8)
ax.add_patch(Circle((2.2, hy - 0.12), 0.13, fc="#f2b8a6", ec="none"))
ax.add_patch(Circle((3.0, hy - 0.12), 0.13, fc="#f2b8a6", ec="none"))
word(ax, 2.6, 0.1, "숨 참기")
for k, (t, x) in enumerate([("처음", 7.4), ("답답", 11.0), ("푸하", 14.6)]):
    hot = k == 2
    ax.add_patch(Circle((x, 3.4), 1.1, fc="white", ec=RED if hot else INK, lw=2.4 if hot else 1.6))
    word(ax, x, 3.4, t, fs=14, color=RED if hot else "#222")
    if k < 2:
        arrow(ax, (x + 1.25, 3.4), (x + 2.35, 3.4))
save(fig, "b02-hold.svg")

# 2. 숨이 가는 길: 코 → 숨관 → 갈라진 길 → 폐
fig, ax = canvas(10.4, 6.6, 17.0, 10.8)
ax.set_ylim(0.2, 10.8)
ax.add_patch(Ellipse((8.5, 9.4), 1.6, 1.8, fc=SKIN, ec=INK, lw=1.4))
word(ax, 9.6, 9.6, "코", ha="left")
ax.plot([8.5, 8.5], [8.5, 6.2], color=INK, lw=6, solid_capstyle="round")
ax.plot([8.5, 8.5], [8.5, 6.2], color="white", lw=3, solid_capstyle="round")
word(ax, 9.0, 7.4, "숨관", ha="left")
ax.add_patch(Ellipse((5.9, 3.6), 4.4, 6.0, fc=CELL, ec=INK, lw=1.6))
ax.add_patch(Ellipse((11.1, 3.6), 4.4, 6.0, fc=CELL, ec=INK, lw=1.6))


def branch(x, y, ang, length, depth):
    if depth == 0:
        ax.add_patch(Circle((x, y), 0.18, fc="white", ec=RED, lw=1.2))
        return
    x2 = x + length * math.cos(math.radians(ang))
    y2 = y + length * math.sin(math.radians(ang))
    ax.plot([x, x2], [y, y2], color=RED, lw=0.6 + depth * 0.5)
    branch(x2, y2, ang - 28, length * 0.7, depth - 1)
    branch(x2, y2, ang + 28, length * 0.7, depth - 1)


branch(8.5, 6.2, -125, 1.5, 4)
branch(8.5, 6.2, -55, 1.5, 4)
word(ax, 3.4, 6.5, "폐", fs=16)
word(ax, 13.6, 6.5, "폐", fs=16)
arrow(ax, (6.3, 10.2), (7.6, 9.6), lw=1.8)
word(ax, 5.5, 10.3, "공기")
save(fig, "b02-path.svg")

# 3. 작은 주머니: 산소는 피로, 다 쓴 숨은 주머니로
fig, ax = canvas(11.0, 5.4, 18.0, 8.8)
ax.plot([4.0, 4.0], [8.2, 6.2], color=INK, lw=2.2)
cluster = [(4.0, 5.6), (3.0, 5.0), (5.0, 5.0), (2.6, 3.9), (3.8, 4.0), (5.0, 3.9), (3.3, 2.9), (4.6, 2.9)]
for (cx, cy) in cluster:
    ax.add_patch(Circle((cx, cy), 0.62, fc="white", ec=INK, lw=1.4))
    ax.add_patch(Arc((cx, cy), 1.42, 1.42, theta1=200, theta2=340, color="#d99a8a", lw=1.6))
    ax.add_patch(Arc((cx, cy), 1.42, 1.42, theta1=20, theta2=160, color="#d99a8a", lw=1.0))
word(ax, 4.0, 1.4, "작은 주머니")
ax.plot([7.2, 7.2], [0.6, 8.2], color=GREY, lw=1.2, ls="--")
ax.add_patch(Circle((10.6, 4.6), 1.6, fc="white", ec=INK, lw=2))
word(ax, 10.6, 4.6, "주머니")
ax.add_patch(Rectangle((12.2, 2.0), 1.0, 5.2, fc=BLOOD, ec=INK, lw=1.6))
word(ax, 12.7, 1.4, "핏줄")
arrow(ax, (11.2, 5.4), (14.6, 5.4), color=RED, lw=2.4)
word(ax, 15.6, 5.4, "산소", color=RED, ha="left")
arrow(ax, (14.6, 3.8), (11.2, 3.8), color=USED, lw=2.4)
word(ax, 15.6, 3.8, "다 쓴 숨", color=USED, ha="left")
save(fig, "b02-sac.svg")

# 4. 큰 풍선 하나와 작은 주머니 여럿: 핏줄과 붙은 벽(빨간 선)
fig, ax = canvas(11.0, 5.0, 18.0, 8.2)
ax.add_patch(Circle((4.4, 4.6), 2.6, fc="white", ec=RED, lw=3.2))
word(ax, 4.4, 1.1, "큰 풍선 1개")
ax.plot([9.0, 9.0], [0.6, 7.8], color=GREY, lw=1.2, ls="--")
ax.add_patch(Circle((13.6, 4.6), 2.6, fc="none", ec=GREY, lw=1.0, ls=":"))
r = 0.52
centers = [(13.6, 4.6)]
centers += [(13.6 + 1.08 * math.cos(math.radians(a)), 4.6 + 1.08 * math.sin(math.radians(a))) for a in range(0, 360, 60)]
centers += [(13.6 + 2.05 * math.cos(math.radians(a)), 4.6 + 2.05 * math.sin(math.radians(a))) for a in range(30, 390, 30)]
for cx, cy in centers:
    ax.add_patch(Circle((cx, cy), r, fc="white", ec=RED, lw=3.2))
word(ax, 13.6, 1.1, f"작은 주머니 {len(centers)}개")
save(fig, "b02-many.svg")

# 5. 한 바퀴: 공기 → 폐 → 피 → 세포 → 피 → 폐 → 밖
fig, ax = canvas(11.0, 5.0, 18.0, 8.2)
nodes = [("공기", 2.0, 6.4), ("폐", 6.6, 6.4), ("피", 11.4, 6.4), ("세포", 15.8, 4.0), ("피", 11.4, 1.6),
         ("폐", 6.6, 1.6), ("밖", 2.0, 1.6)]
for name, x, y in nodes:
    fc = CELL if name == "세포" else (BLOOD if name == "피" else NOTE)
    ax.add_patch(FancyBboxPatch((x - 1.0, y - 0.55), 2.0, 1.1, boxstyle="round,pad=0.15", fc=fc, ec=INK, lw=1.4))
    word(ax, x, y, name, fs=13)
for (a, b, col, lab) in [(0, 1, "#222", "산소"), (1, 2, "#222", "산소"), (2, 3, "#222", "산소"),
                         (3, 4, USED, "다 쓴 숨"), (4, 5, USED, "다 쓴 숨"), (5, 6, USED, "다 쓴 숨")]:
    _, x1, y1 = nodes[a]
    _, x2, y2 = nodes[b]
    sx = 1.15 if x2 > x1 else (-1.15 if x2 < x1 else 0)
    arrow(ax, (x1 + sx, y1 - (0.6 if y2 < y1 else 0)), (x2 - sx, y2 + (0.6 if y2 < y1 else 0)), color=col, lw=2.6 if col == USED else 2)
    word(ax, (x1 + x2) / 2, (y1 + y2) / 2 + 0.5, lab, fs=10, color=col)
save(fig, "b02-loop.svg")

# 6. 숨 참기: 다 쓴 숨이 쌓이면 뇌가 숨 쉬는 근육에 알린다
fig, ax = canvas(11.6, 4.6, 19.0, 7.6)
for k in range(6):
    h = 0.5 + k * 0.75
    ax.add_patch(Rectangle((1.0 + k * 1.3, 1.2), 0.9, h, fc=RED if k == 5 else USED, ec=INK, lw=1.0))
word(ax, 1.45, 0.6, "처음", fs=10, bold=False)
word(ax, 7.95, 0.6, "한참 지나", fs=10, bold=False)
word(ax, 4.6, 6.6, "다 쓴 숨")
ax.add_patch(Ellipse((12.0, 4.4), 3.0, 2.2, fc=NOTE, ec=INK, lw=1.6))
word(ax, 12.0, 4.4, "뇌", fs=16)
arrow(ax, (9.0, 4.4), (10.4, 4.4), lw=1.8)
word(ax, 14.4, 5.3, "숨 쉬어!", fs=13, color=RED)
arrow(ax, (13.6, 4.4), (15.2, 4.4), color=RED, lw=2)
ax.add_patch(FancyBboxPatch((15.4, 3.8), 3.0, 1.2, boxstyle="round,pad=0.15", fc=CELL, ec=INK, lw=1.4))
word(ax, 16.9, 4.4, "숨 쉬는 근육", fs=11)
save(fig, "b02-why.svg")
