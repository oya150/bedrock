"""인체 10편 그림 만들기. 실행: python lab/fig_b10.py  → docs/body/img/10/*.svg

글자는 SVG 안에 글자로 남긴다(글꼴 모양을 파일에 넣지 않는다). 보는 쪽 글꼴로 그려진다.
카드는 차분한 색으로, 강조(새로 받은 카드, 비교 화살표, 많이 든 일)만 빨강으로 칠한다.
"""
import itertools
import os

import matplotlib

matplotlib.use("svg")
import matplotlib.pyplot as plt
from matplotlib.patches import Arc, Circle, FancyArrowPatch, FancyBboxPatch, Rectangle

OUT = os.path.join(os.path.dirname(__file__), "..", "docs", "body", "img", "10")
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
from matplotlib.patches import Ellipse, Polygon, Wedge

CELL = "#fbe3dc"
LIGHT_C = "#f6c445"
NERVE = "#8e5ea2"
IRIS = "#7a9a6b"


def eyeball(ax, cx, cy, r=2.4, pupil=0.5):
    """눈을 옆에서 자른 모습: 왼쪽이 앞."""
    ax.add_patch(Circle((cx, cy), r, fc="white", ec=INK, lw=1.8))
    # 망막: 뒤쪽 호
    ax.add_patch(Arc((cx, cy), 2 * r - 0.2, 2 * r - 0.2, theta1=-110, theta2=110, color=RED, lw=4))
    # 각막
    ax.add_patch(Arc((cx - r + 0.1, cy), 1.0, 2.0, theta1=90, theta2=270, color=INK, lw=1.6))
    # 홍채
    ax.plot([cx - r + 0.45, cx - r + 0.45], [cy + pupil, cy + 1.2], color=IRIS, lw=4)
    ax.plot([cx - r + 0.45, cx - r + 0.45], [cy - pupil, cy - 1.2], color=IRIS, lw=4)
    # 렌즈
    ax.add_patch(Ellipse((cx - r + 0.9, cy), 0.55, 1.6, fc="#e8f1f8", ec=INK, lw=1.4))
    # 시신경
    nx, ny = cx + r * math.cos(math.radians(-28)), cy + r * math.sin(math.radians(-28))
    ax.plot([nx - 0.1, nx + 1.5], [ny + 0.05, ny - 0.6], color=NERVE, lw=5, solid_capstyle="round")


# 1. 여는 장면: 불 끈 방
fig, ax = canvas(10.0, 4.4, 16.0, 7.0)
for k, (x, dark) in enumerate([(0.6, False), (8.6, True)]):
    ax.add_patch(Rectangle((x, 1.2), 6.6, 5.0, fc="#2f2f3a" if dark else "#fffdf0", ec=INK, lw=1.4))
    ax.add_patch(Rectangle((x + 1.0, 1.6), 1.8, 1.4, fc="#4a4a55" if dark else "#e4572e", ec=INK, lw=1))
    ax.add_patch(Circle((x + 4.8, 2.4), 0.7, fc="#4a4a55" if dark else "#7da2c8", ec=INK, lw=1))
    if not dark:
        ax.add_patch(Circle((x + 5.6, 5.4), 0.4, fc=LIGHT_C, ec=INK, lw=1))
    ax.text(x + 3.3, 0.6, "불을 켜면 다 보여요" if not dark else "불을 끄면 안 보여요", ha="center", va="center",
            fontsize=11, fontweight="bold")
ax.text(8.0, 6.7, "눈은 그대로인데 왜 달라질까?", ha="center", va="center", fontsize=12, color=RED, fontweight="bold")
save(fig, "b10-dark.svg")

# 2. 이 편의 지도
fig, ax = canvas(11.6, 2.9, 19.4, 4.6)
titles = ["빛이 들어와요", "눈동자가 조절해요", "망막에 모여요", "뇌가 읽어요"]
for i, t in enumerate(titles):
    x = 0.3 + i * 4.8
    box(ax, x, 0.4, 3.8, 3.6)
    ax.text(x + 1.9, 0.95, t, ha="center", va="center", fontsize=11, fontweight="bold")
    cx = x + 1.9
    if i == 0:
        for dy in (-0.4, 0, 0.4):
            arrow(ax, (x + 0.5, 2.6 + dy), (x + 3.2, 2.6), color=LIGHT_C, lw=1.6, ms=9)
    elif i == 1:
        ax.add_patch(Circle((cx - 0.7, 2.6), 0.55, fc=IRIS, ec=INK, lw=1))
        ax.add_patch(Circle((cx - 0.7, 2.6), 0.15, fc=INK, ec=INK))
        ax.add_patch(Circle((cx + 0.7, 2.6), 0.55, fc=IRIS, ec=INK, lw=1))
        ax.add_patch(Circle((cx + 0.7, 2.6), 0.38, fc=INK, ec=INK))
    elif i == 2:
        ax.add_patch(Arc((cx, 2.6), 2.0, 2.0, theta1=-70, theta2=70, color=RED, lw=3))
        arrow(ax, (cx - 1.2, 2.6), (cx + 0.98, 2.6), color=LIGHT_C, lw=1.4, ms=9)
    else:
        ax.add_patch(Ellipse((cx, 2.6), 2.2, 1.5, fc=NOTE, ec=INK, lw=1.2))
        ax.text(cx, 2.6, "뇌", ha="center", va="center", fontsize=12, fontweight="bold")
    if i < 3:
        arrow(ax, (x + 3.95, 2.2), (x + 4.65, 2.2))
save(fig, "b10-map.svg")

# 3. 빛이 물건에 닿아 눈으로
fig, ax = canvas(11.0, 4.4, 18.0, 7.2)
ax.add_patch(Circle((1.6, 5.8), 0.7, fc=LIGHT_C, ec=INK, lw=1.2))
for a in range(0, 360, 45):
    r = math.radians(a)
    ax.plot([1.6 + 0.9 * math.cos(r), 1.6 + 1.2 * math.cos(r)], [5.8 + 0.9 * math.sin(r), 5.8 + 1.2 * math.sin(r)],
            color=LIGHT_C, lw=2)
ax.add_patch(Circle((6.0, 2.4), 1.1, fc=RED, ec=INK, lw=1.2))
ax.plot([6.0, 6.2], [3.5, 4.1], color=INK, lw=2)
ax.add_patch(Ellipse((6.6, 3.9), 0.7, 0.3, angle=20, fc="#8fb58f", ec=INK, lw=1))
ax.text(6.0, 0.6, "사과", ha="center", va="center", fontsize=11)
arrow(ax, (2.3, 5.2), (5.6, 3.6), color=LIGHT_C, lw=2.2)
arrow(ax, (6.8, 3.0), (12.0, 3.4), color=LIGHT_C, lw=2.2)
eyeball(ax, 14.6, 3.4, r=1.8, pupil=0.4)
ax.text(9.4, 4.0, "사과에 닿아 튕긴 빛", ha="center", va="center", fontsize=10)
ax.text(14.6, 0.6, "눈", ha="center", va="center", fontsize=11, fontweight="bold")
ax.text(1.6, 4.3, "해", ha="center", va="center", fontsize=11, fontweight="bold")
ax.text(3.6, 4.9, "빛", ha="center", va="center", fontsize=11, fontweight="bold", color="#b08800")
save(fig, "b10-light.svg")

# 4. 눈 속: 창과 렌즈가 빛을 꺾어 망막에 모아요
fig, ax = canvas(11.0, 5.0, 18.0, 8.2)
eyeball(ax, 10.0, 4.2, r=3.2, pupil=0.6)
for y0 in (5.6, 4.2, 2.8):
    ax.plot([1.0, 7.2], [y0, 4.2 + (y0 - 4.2) * 0.35], color=LIGHT_C, lw=2)
    ax.plot([7.2, 13.0], [4.2 + (y0 - 4.2) * 0.35, 4.2], color=LIGHT_C, lw=2)
ax.add_patch(Circle((13.0, 4.2), 0.18, fc=RED, ec=RED))
ax.text(13.3, 7.4, "망막: 빛을 느끼는 세포가 가득해요", ha="center", va="center", fontsize=10, color=RED,
        fontweight="bold")
arrow(ax, (13.3, 7.1), (12.9, 6.6), color=RED, lw=1.2, ms=10)
ax.text(6.2, 7.2, "렌즈", ha="center", va="center", fontsize=10, fontweight="bold")
arrow(ax, (6.3, 6.9), (7.6, 5.4), color=INK, lw=1.2, ms=10)
ax.text(4.6, 1.2, "투명한 창", ha="center", va="center", fontsize=10, fontweight="bold")
arrow(ax, (5.2, 1.5), (6.7, 3.0), color=INK, lw=1.2, ms=10)
ax.text(14.2, 1.6, "신경", ha="left", va="center", fontsize=10, color=NERVE, fontweight="bold")
ax.text(9.0, 0.3, "눈을 옆에서 자른 모습 (크기는 실제와 맞추지 않았어요)", ha="center", va="center", fontsize=10)
ax.set_ylim(-0.2, 8.2)
save(fig, "b10-inside.svg")

# 5. 눈동자: 밝으면 작게, 어두우면 크게
fig, ax = canvas(10.0, 3.8, 16.0, 6.2)
for k, (x, pr, lab, bg) in enumerate([(3.6, 0.35, "밝을 때: 작아져요", "#fffdf0"), (12.4, 0.95, "어두울 때: 커져요", "#d9d9e0")]):
    ax.add_patch(Rectangle((x - 3.0, 1.0), 6.0, 4.6, fc=bg, ec=INK, lw=1.2))
    ax.add_patch(Ellipse((x, 3.4), 4.6, 2.4, fc="white", ec=INK, lw=1.6))
    ax.add_patch(Circle((x, 3.4), 1.1, fc=IRIS, ec=INK, lw=1.2))
    ax.add_patch(Circle((x, 3.4), pr, fc="#222", ec="#222"))
    ax.text(x, 0.5, lab, ha="center", va="center", fontsize=11, fontweight="bold")
ax.text(8.0, 6.0, "가운데 검은 동그라미가 눈동자예요. 둘레의 색깔 있는 부분이 크기를 바꿔요", ha="center",
        va="center", fontsize=10)
save(fig, "b10-pupil.svg")

# 6. 맹점 찾기 카드
fig, ax = canvas(10.0, 2.6, 16.0, 4.2)
ax.add_patch(Rectangle((0.4, 0.4), 15.2, 3.4, fc="white", ec=GREY, lw=1.2))
ax.text(3.0, 2.1, "+", ha="center", va="center", fontsize=40, fontweight="bold")
ax.add_patch(Circle((12.4, 2.1), 0.55, fc=INK, ec=INK))
save(fig, "b10-blindspot.svg")
