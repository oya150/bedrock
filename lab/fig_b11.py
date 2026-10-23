"""인체 11편 그림 만들기. 실행: python lab/fig_b11.py  → docs/body/img/11/*.svg

글자는 SVG 안에 글자로 남긴다(글꼴 모양을 파일에 넣지 않는다). 보는 쪽 글꼴로 그려진다.
카드는 차분한 색으로, 강조(새로 받은 카드, 비교 화살표, 많이 든 일)만 빨강으로 칠한다.
"""
import itertools
import os

import matplotlib

matplotlib.use("svg")
import matplotlib.pyplot as plt
from matplotlib.patches import Arc, Circle, FancyArrowPatch, FancyBboxPatch, Rectangle

OUT = os.path.join(os.path.dirname(__file__), "..", "docs", "body", "img", "11")
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

NERVE = "#8e5ea2"
CMD = "#e4572e"
IN_C = "#7da2c8"
BONE = "#efe6d2"
SKIN = "#f6d8c4"


def brain(ax, cx, cy, w=3.0, h=2.0, label=True):
    ax.add_patch(Ellipse((cx, cy), w, h, fc=NOTE, ec=INK, lw=1.6))
    for k in range(3):
        ax.add_patch(Arc((cx - w * 0.2 + k * w * 0.2, cy + 0.1), w * 0.3, h * 0.5, theta1=200, theta2=340, color=GREY, lw=1))
    if label:
        ax.text(cx, cy - 0.15, "뇌", ha="center", va="center", fontsize=13, fontweight="bold")


# 1. 여는 장면: 공 받기
fig, ax = canvas(10.0, 4.6, 16.0, 7.4)
kid(ax, 3.4, 0.6, 3.0)
ax.plot([3.4 + 1.05, 5.4], [0.6 + 3.0, 0.6 + 4.2], color=INK, lw=2)
ax.add_patch(Circle((12.6, 5.4), 0.5, fc=YEL, ec=INK, lw=1.4))
for k in range(3):
    ax.plot([13.4 + k * 0.5, 13.8 + k * 0.5], [5.5 - k * 0.2, 5.6 - k * 0.2], color=GREY, lw=2)
arrow(ax, (12.0, 5.3), (6.2, 4.9), color=INK, lw=1.4, rad=0.15)
ax.text(9.0, 2.0, "공을 보고 손을 뻗어 잡기까지\n눈 깜짝할 사이에 무슨 일이?", ha="center", va="center", fontsize=12,
        color=RED, fontweight="bold")
save(fig, "b11-catch.svg")

# 2. 이 편의 지도
fig, ax = canvas(11.6, 2.9, 19.4, 4.6)
titles = ["알림이 들어와요", "뇌가 정해요", "명령이 나가요", "급할 땐 지름길"]
for i, t in enumerate(titles):
    x = 0.3 + i * 4.8
    box(ax, x, 0.4, 3.8, 3.6)
    ax.text(x + 1.9, 0.95, t, ha="center", va="center", fontsize=11, fontweight="bold")
    cx = x + 1.9
    if i == 0:
        arrow(ax, (x + 0.5, 2.5), (x + 3.2, 2.5), color=IN_C, lw=2, ms=10)
    elif i == 1:
        brain(ax, cx, 2.6, w=2.2, h=1.4, label=False)
    elif i == 2:
        arrow(ax, (x + 3.2, 2.5), (x + 0.5, 2.5), color=CMD, lw=2, ms=10)
    else:
        ax.plot([x + 0.6, cx, x + 3.2], [2.1, 3.2, 2.1], color=GREY, lw=1.4, ls="--")
        arrow(ax, (x + 0.6, 2.1), (x + 3.2, 2.1), color=CMD, lw=2, ms=10, rad=0.4)
    if i < 3:
        arrow(ax, (x + 3.95, 2.2), (x + 4.65, 2.2))
save(fig, "b11-map.svg")

# 3. 몸 한 바퀴: 알림이 뇌로, 명령이 근육으로 (척수는 등뼈 속)
fig, ax = canvas(10.0, 6.0, 16.0, 9.6)
brain(ax, 4.0, 8.2, w=3.4, h=2.0)
for k in range(9):
    ax.add_patch(FancyBboxPatch((3.5, 6.6 - k * 0.62), 1.0, 0.5, boxstyle="round,pad=0.04", fc=BONE, ec=INK, lw=1))
ax.plot([4.0, 4.0], [7.2, 1.2], color=NERVE, lw=4)
ax.text(2.2, 4.0, "척수\n(등뼈 속)", ha="center", va="center", fontsize=11, color=NERVE, fontweight="bold")
# 손 쪽
ax.add_patch(FancyBboxPatch((12.6, 3.4), 1.6, 1.8, boxstyle="round,pad=0.3", fc=SKIN, ec=INK, lw=1.4))
ax.text(13.4, 2.6, "손", ha="center", va="center", fontsize=11, fontweight="bold")
ax.plot([4.0, 12.6], [4.6, 4.6], color=IN_C, lw=2.4)
ax.plot([4.0, 12.6], [3.8, 3.8], color=CMD, lw=2.4)
arrow(ax, (9.0, 4.6), (7.6, 4.6), color=IN_C, lw=2, ms=14)
arrow(ax, (7.6, 3.8), (9.0, 3.8), color=CMD, lw=2, ms=14)
arrow(ax, (4.5, 5.6), (4.5, 7.0), color=IN_C, lw=2, ms=14)
arrow(ax, (3.5, 7.0), (3.5, 5.6), color=CMD, lw=2, ms=14)
ax.text(8.3, 5.2, "들어오는 알림", ha="center", va="center", fontsize=10, color=IN_C, fontweight="bold")
ax.text(8.3, 3.2, "나가는 명령", ha="center", va="center", fontsize=10, color=CMD, fontweight="bold")
ax.text(8.0, 0.4, "모양과 크기는 실제와 맞추지 않았어요", ha="center", va="center", fontsize=10)
save(fig, "b11-loop.svg")

# 4. 뇌는 일을 나눠 맡아요
fig, ax = canvas(10.0, 4.6, 16.0, 7.4)
ax.add_patch(Ellipse((7.0, 4.2), 9.0, 5.6, fc=NOTE, ec=INK, lw=1.8))
ax.add_patch(Ellipse((9.6, 1.9), 2.6, 1.4, fc="#f1e6c8", ec=INK, lw=1.4))
ax.add_patch(Wedge((7.0, 4.2), 4.4, 70, 100, fc="#fbe3dc", ec="none")) if False else None
ax.add_patch(Polygon([(6.0, 7.0), (6.6, 7.0), (5.6, 3.4), (5.0, 3.4)], closed=True, fc="#f6c9bd", ec=RED, lw=1.4))
ax.text(2.4, 5.6, "움직이라고\n명령하는 띠", ha="center", va="center", fontsize=10, color=RED, fontweight="bold")
ax.text(10.4, 4.4, "보는 일을\n맡은 곳", ha="center", va="center", fontsize=10, color=IN_C, fontweight="bold")
ax.text(9.6, 1.9, "균형", ha="center", va="center", fontsize=10, fontweight="bold")
ax.text(3.0, 2.0, "앞쪽(이마)", ha="center", va="center", fontsize=10)
ax.text(12.4, 5.6, "뒤쪽\n(뒤통수)", ha="center", va="center", fontsize=10)
ax.text(8.0, 7.2, "뇌를 옆에서 본 모습 (자리는 대강만 나타냈어요)", ha="center", va="center", fontsize=10)
save(fig, "b11-parts.svg")

# 5. 급할 땐 지름길: 뜨거운 냄비
fig, ax = canvas(11.0, 5.0, 18.0, 8.2)
brain(ax, 4.0, 7.0, w=3.0, h=1.6)
ax.plot([4.0, 4.0], [6.2, 1.0], color=NERVE, lw=4)
ax.text(3.0, 2.0, "척수", ha="center", va="center", fontsize=11, color=NERVE, fontweight="bold")
ax.add_patch(Rectangle((13.2, 1.2), 3.0, 1.4, fc=GREY, ec=INK, lw=1.4))
for k in range(3):
    ax.plot([13.8 + k * 0.9, 14.0 + k * 0.9, 13.8 + k * 0.9], [2.8, 3.3, 3.8], color=RED, lw=1.6)
ax.add_patch(FancyBboxPatch((11.4, 3.6), 1.4, 1.2, boxstyle="round,pad=0.25", fc=SKIN, ec=INK, lw=1.4))
ax.text(12.1, 5.4, "앗 뜨거워!", ha="center", va="center", fontsize=11, color=RED, fontweight="bold")
ax.plot([4.0, 11.4], [4.6, 4.6], color=IN_C, lw=2.4)
ax.plot([4.0, 11.4], [3.8, 3.8], color=CMD, lw=2.4)
arrow(ax, (8.4, 4.6), (6.8, 4.6), color=IN_C, lw=2, ms=14)
arrow(ax, (6.8, 3.8), (8.4, 3.8), color=CMD, lw=2, ms=14)
ax.add_patch(Circle((4.0, 4.2), 0.32, fc=YEL, ec=INK, lw=1.2))
ax.text(5.0, 2.8, "척수에서 바로 돌려보내요", ha="left", va="center", fontsize=10, color=RED, fontweight="bold")
ax.plot([4.4, 4.4], [4.9, 6.1], color=GREY, lw=1.2, ls="--")
ax.text(5.4, 5.6, "알림은 뇌로도 가요", ha="left", va="center", fontsize=10, color=INK)
arrow(ax, (12.1, 4.9), (12.1, 6.6), color=CMD, lw=1.8, ms=12)
ax.text(13.2, 7.2, "손이 저절로 떨어져요", ha="center", va="center", fontsize=10, fontweight="bold")
save(fig, "b11-reflex.svg")

# 6. 해 보기: 자 떨어뜨려 잡기
fig, ax = canvas(10.0, 4.4, 16.0, 7.0)
ax.add_patch(Rectangle((7.4, 1.6), 0.8, 5.0, fc="#fff8e1", ec=INK, lw=1.4))
for k in range(11):
    ax.plot([7.4, 7.4 + (0.4 if k % 5 == 0 else 0.22)], [1.8 + k * 0.45, 1.8 + k * 0.45], color=INK, lw=1)
ax.add_patch(FancyBboxPatch((7.0, 6.3), 1.6, 0.9, boxstyle="round,pad=0.15", fc=SKIN, ec=INK, lw=1.2))
ax.text(9.8, 6.8, "친구가 잡고 있다가 놓아요", ha="left", va="center", fontsize=10)
ax.plot([6.6, 7.3], [1.9, 1.9], color=INK, lw=3)
ax.plot([8.3, 9.0], [1.9, 1.9], color=INK, lw=3)
ax.text(9.8, 1.9, "엄지와 검지를 벌리고 기다렸다가\n떨어지는 걸 보면 잡아요", ha="left", va="center", fontsize=10)
arrow(ax, (6.4, 5.2), (6.4, 3.0), color=RED, lw=1.8)
ax.text(5.8, 4.1, "툭", ha="right", va="center", fontsize=12, color=RED, fontweight="bold")
ax.text(3.0, 0.6, "잡은 곳의 눈금을 적어요", ha="center", va="center", fontsize=10, fontweight="bold")
ax.set_ylim(0.0, 7.8)
save(fig, "b11-ruler.svg")
