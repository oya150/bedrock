"""알고리즘 2편 그림 만들기. 실행: python lab/fig_02.py  → docs/algorithms/img/02/*.svg

글자는 SVG 안에 글자로 남긴다(글꼴 모양을 파일에 넣지 않는다). 보는 쪽 글꼴로 그려진다.
사물함과 칸은 차분한 색으로 칠하고, 강조(찾는 칸, 옮기는 일)만 빨강으로 칠한다.
"""
import os

import matplotlib

matplotlib.use("svg")
import matplotlib.pyplot as plt
from matplotlib.patches import Arc, Circle, FancyArrowPatch, FancyBboxPatch, Rectangle

OUT = os.path.join(os.path.dirname(__file__), "..", "docs", "algorithms", "img", "02")
os.makedirs(OUT, exist_ok=True)

plt.rcParams.update({
    "font.family": ["Apple SD Gothic Neo", "Noto Sans KR", "Malgun Gothic", "sans-serif"],
    "svg.fonttype": "none",
    "text.color": "#222",
    "figure.facecolor": "white",
    "savefig.facecolor": "white",
})

RED, GREY, INK, PAPER, NOTE, YEL = "#e4572e", "#c9ccd1", "#555", "#f4f6f8", "#fffdf5", "#f6c445"
BLUE, GREEN, PURPLE, WOOD = "#7da2c8", "#8fb58f", "#b59cc8", "#e8d3b0"
BOOKS = [BLUE, GREEN, YEL, PURPLE, WOOD]


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


def locker(ax, x, y, w, h, num, hot=False, fs=11):
    ax.add_patch(Rectangle((x, y), w, h, fc="#fbe3dc" if hot else PAPER, ec=RED if hot else INK, lw=2.2 if hot else 1.2))
    ax.add_patch(Rectangle((x + w * 0.72, y + h * 0.4), w * 0.1, h * 0.2, fc=INK, ec=INK, lw=0))
    ax.text(x + w * 0.4, y + h * 0.72, str(num), ha="center", va="center", fontsize=fs,
            color=RED if hot else INK, fontweight="bold")


def kid(ax, cx, y, s=1.0):
    ax.add_patch(Circle((cx, y + 1.55 * s), 0.32 * s, fc="white", ec=INK, lw=1.6))
    ax.add_patch(Circle((cx - 0.11 * s, y + 1.6 * s), 0.035 * s, fc=INK))
    ax.add_patch(Circle((cx + 0.11 * s, y + 1.6 * s), 0.035 * s, fc=INK))
    ax.add_patch(Arc((cx, y + 1.5 * s), 0.3 * s, 0.2 * s, theta1=200, theta2=340, color=INK, lw=1.4))
    ax.plot([cx, cx], [y + 1.23 * s, y + 0.55 * s], color=INK, lw=2)
    ax.plot([cx, cx - 0.3 * s], [y + 0.55 * s, y], color=INK, lw=2)
    ax.plot([cx, cx + 0.3 * s], [y + 0.55 * s, y], color=INK, lw=2)
    ax.plot([cx - 0.35 * s, cx + 0.35 * s], [y + 1.0 * s, y + 1.0 * s], color=INK, lw=2)


def cell(ax, x, y, w, h, num, name=None, hot=False, fs=12, empty=False):
    ax.add_patch(Rectangle((x, y), w, h, fc="white" if empty else ("#fbe3dc" if hot else NOTE),
                           ec=RED if hot else INK, lw=2.2 if hot else 1.4,
                           ls="--" if empty else "-"))
    ax.text(x + w / 2, y - 0.25, str(num), ha="center", va="top", fontsize=11,
            color=RED if hot else INK, fontweight="bold")
    if name:
        ax.text(x + w / 2, y + h / 2, name, ha="center", va="center", fontsize=fs,
                color=RED if hot else "#222", fontweight="bold" if hot else "normal")


# 1. 여는 장면: 내 사물함 17번으로 곧장
fig, ax = canvas(10.0, 4.4, 16.0, 7.0)
w, h = 1.35, 1.55
for k in range(20):
    r, c = divmod(k, 10)
    locker(ax, 1.0 + c * w, 4.0 - r * h, w, h, k + 1, hot=(k + 1 == 17))
kid(ax, 1.0 + 6.5 * w, 0.0, 0.85)
arrow(ax, (1.0 + 6.5 * w, 1.6), (1.0 + 6.5 * w, 2.4), color=RED, lw=2.4)
ax.text(1.0 + 6.5 * w + 0.6, 0.6, "곧장 17번으로", ha="left", va="center", fontsize=13, color=RED, fontweight="bold")
save(fig, "a02-locker.svg")

# 2. 이 편의 지도
fig, ax = canvas(11.6, 2.9, 19.4, 4.6)
titles = ["번호로 바로 찾기", "크기가 같아야 해요", "메모리 칸도 똑같이", "맨 앞에 넣으면?"]
for i, t in enumerate(titles):
    x = 0.3 + i * 4.8
    box(ax, x, 0.4, 3.8, 3.6)
    ax.text(x + 1.9, 0.95, t, ha="center", va="center", fontsize=12, fontweight="bold")
    if i == 0:
        for k in range(4):
            locker(ax, x + 0.3 + k * 0.8, 1.7, 0.8, 1.2, k + 1, hot=(k == 2), fs=10)
        arrow(ax, (x + 2.3, 3.75), (x + 2.3, 3.0), color=RED, lw=2)
    elif i == 1:
        for k in range(4):
            ax.add_patch(Rectangle((x + 0.3 + k * 0.8, 2.6), 0.8, 0.8, fc=PAPER, ec=INK, lw=1.2))
        bx = x + 0.3
        for k, bw in enumerate([0.35, 0.9, 0.5, 1.2]):
            ax.add_patch(Rectangle((bx, 1.5), bw, 0.9, fc=BOOKS[k], ec=INK, lw=1.2))
            bx += bw
    elif i == 2:
        for k in range(5):
            cell(ax, x + 0.3 + k * 0.64, 2.2, 0.64, 0.9, k + 1, hot=(k == 3))
        arrow(ax, (x + 0.3 + 3.5 * 0.64, 3.85), (x + 0.3 + 3.5 * 0.64, 3.15), color=RED, lw=2)
    else:
        for k in range(5):
            cell(ax, x + 0.3 + k * 0.64, 2.2, 0.64, 0.9, k + 1)
        for k in range(4):
            arrow(ax, (x + 0.3 + (k + 0.5) * 0.64, 3.15), (x + 0.3 + (k + 1.5) * 0.64, 3.15),
                  color=RED, lw=1.4, rad=-0.6, ms=10)
    if i < 3:
        arrow(ax, (x + 3.95, 2.2), (x + 4.65, 2.2))
save(fig, "a02-map.svg")

# 3. 사물함은 뼘으로 바로, 책은 하나씩 세기
fig, ax = canvas(10.4, 5.4, 17.0, 8.8)
w = 0.78
for k in range(20):
    locker(ax, 0.6 + k * w, 5.4, w, 1.3, k + 1, hot=(k + 1 == 17), fs=9)
for k in range(21):
    ax.plot([0.6 + k * w] * 2, [5.05, 5.25], color=INK, lw=1.2)
ax.plot([0.6, 0.6 + 20 * w], [5.15, 5.15], color=INK, lw=1.2)
ax.text(0.6, 4.75, "칸 폭이 한 걸음이면, 1번 칸 앞에서 열여섯 걸음 가면 17번 칸 앞", ha="left", va="center", fontsize=12, color=RED, fontweight="bold")
arrow(ax, (0.6 + 16.5 * w, 8.2), (0.6 + 16.5 * w, 6.85), color=RED, lw=2.4)
widths = [0.35, 0.9, 0.5, 1.15, 0.4, 0.7, 0.3, 1.0, 0.55, 0.8, 0.45, 1.1, 0.35, 0.6, 0.95, 0.4, 0.75]
bx = 0.6
for k, bw in enumerate(widths):
    ax.add_patch(Rectangle((bx, 0.9), bw, 2.2 - (k % 3) * 0.25, fc=BOOKS[k % 5], ec=INK, lw=1.2))
    if k < 5:
        arrow(ax, (bx + bw / 2, 3.35), (bx + bw + widths[k + 1] / 2, 3.35), lw=1.3, rad=-0.6, ms=10)
        ax.text(bx + bw / 2, 3.85, str(k + 1), ha="center", va="center", fontsize=11, fontweight="bold")
    bx += bw
ax.text(bx + 0.3, 2.0, "17번째 책은\n어디쯤?", ha="left", va="center", fontsize=12, fontweight="bold")
ax.text(0.6, 0.35, "책은 두께가 달라서 1, 2, 3… 세어 가야 해요", ha="left", va="center", fontsize=12)
save(fig, "a02-books.svg")

# 4. 컴퓨터 칸(배열): 칸이 많아도 한 번
fig, ax = canvas(10.6, 5.0, 17.4, 8.2)
names = ["지우", "민준", "서연", "하준", "도윤", "수아", "시우", "하린"]
cw = 1.45
for k, nm in enumerate(names):
    cell(ax, 0.6 + k * cw, 5.2, cw, 1.2, k + 1, nm, hot=(k == 4))
ax.text(0.6 + 8 * cw + 0.45, 5.8, "…", ha="center", va="center", fontsize=20, fontweight="bold")
cell(ax, 0.6 + 8 * cw + 0.9, 5.2, cw, 1.2, "1,000", "보람")
arrow(ax, (0.6 + 4.5 * cw, 7.9), (0.6 + 4.5 * cw, 6.55), color=RED, lw=2.4)
ax.text(0.6 + 4.5 * cw + 0.3, 7.55, "5번 칸 꺼내 와!", ha="left", va="center", fontsize=12, color=RED, fontweight="bold")
for k, (label, x) in enumerate([("칸 20개", 3.2), ("칸 1,000개", 10.2)]):
    ax.add_patch(Rectangle((x, 1.0), 1.4, 1.0, fc=RED, ec=INK, lw=1.2))
    ax.text(x + 0.7, 2.25, "한 번", ha="center", va="bottom", fontsize=13, color=RED, fontweight="bold")
    ax.text(x + 0.7, 0.6, label, ha="center", va="top", fontsize=12, fontweight="bold")
ax.plot([1.0, 16.4], [1.0, 1.0], color=INK, lw=1.4)
ax.text(1.0, 3.4, "꺼내는 일은 몇 번?", ha="left", va="center", fontsize=12, fontweight="bold")
save(fig, "a02-memory.svg")

# 5. 끝에 넣기 vs 맨 앞에 끼우기
fig, ax = canvas(11.6, 4.4, 19.0, 7.2)
five = ["지우", "민준", "서연", "하준", "도윤"]
cw = 1.25
ax.text(0.4, 6.6, "맨 끝에 넣기", ha="left", va="center", fontsize=13, fontweight="bold")
for k, nm in enumerate(five):
    cell(ax, 0.4 + k * cw, 3.6, cw, 1.1, k + 1, nm, fs=11)
cell(ax, 0.4 + 5 * cw, 3.6, cw, 1.1, 6, "새봄", hot=True, fs=11)
arrow(ax, (0.4 + 5.5 * cw, 6.1), (0.4 + 5.5 * cw, 4.85), color=RED, lw=2.2)
ax.text(0.4 + 3 * cw, 1.9, "한 번 넣으면 끝", ha="center", va="center", fontsize=13, color=RED, fontweight="bold")

x0 = 10.4
ax.text(x0, 6.6, "맨 앞에 넣기", ha="left", va="center", fontsize=13, fontweight="bold")
for k, nm in enumerate(five):
    cell(ax, x0 + k * cw, 3.6, cw, 1.1, k + 1, nm, fs=11)
cell(ax, x0 + 5 * cw, 3.6, cw, 1.1, 6, empty=True)
for k in range(4, -1, -1):
    arrow(ax, (x0 + (k + 0.5) * cw, 4.85), (x0 + (k + 1.5) * cw, 4.85), color=RED, lw=1.6, rad=-0.6, ms=12)
ax.text(x0 - 0.9, 6.0, "새봄", ha="center", va="center", fontsize=12, color=RED, fontweight="bold",
        bbox=dict(boxstyle="round,pad=0.3", fc="#fbe3dc", ec=RED, lw=1.6))
arrow(ax, (x0 - 0.6, 5.6), (x0 + 0.2, 4.3), color=RED, lw=2, rad=0.3)
ax.text(x0 + 3 * cw, 1.9, "다섯 번 옮기고 나서야 1번 칸이 비어요", ha="center", va="center", fontsize=13, color=RED,
        fontweight="bold")
save(fig, "a02-insert.svg")
