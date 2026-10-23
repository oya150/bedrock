"""인체 5편 그림 만들기. 실행: python lab/fig_b05.py  → docs/body/img/05/*.svg

글자는 SVG 안에 글자로 남긴다(글꼴 모양을 파일에 넣지 않는다). 보는 쪽 글꼴로 그려진다.
카드는 차분한 색으로, 강조(새로 받은 카드, 비교 화살표, 많이 든 일)만 빨강으로 칠한다.
"""
import itertools
import os

import matplotlib

matplotlib.use("svg")
import matplotlib.pyplot as plt
from matplotlib.patches import Arc, Circle, FancyArrowPatch, FancyBboxPatch, Rectangle

OUT = os.path.join(os.path.dirname(__file__), "..", "docs", "body", "img", "05")
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
from matplotlib.patches import Ellipse, Polygon

CELL = "#fbe3dc"
BLOOD = "#c0392b"
BACK = "#7da2c8"
MUSCLE = "#e8a598"
SKIN = "#f6d8c4"


def dropper(ax, x, y, squeezed=False):
    """스포이트: 고무 머리 + 유리 관."""
    w = 0.9 if squeezed else 1.5
    ax.add_patch(Ellipse((x, y + 2.4), w, 1.6, fc=GREY, ec=INK, lw=1.6))
    ax.add_patch(Rectangle((x - 0.25, y), 0.5, 1.7, fc="white", ec=INK, lw=1.4))
    ax.add_patch(Rectangle((x - 0.2, y + 0.05), 0.4, 1.0 if squeezed else 1.6, fc=BACK, ec="none"))


def valve(ax, x, y, open_=True, ang=0, color=INK):
    """한쪽으로만 열리는 문: 두 날개."""
    if open_:
        ax.plot([x - 0.5, x - 0.2], [y, y + 0.5], color=color, lw=3, solid_capstyle="round")
        ax.plot([x + 0.5, x + 0.2], [y, y + 0.5], color=color, lw=3, solid_capstyle="round")
    else:
        ax.plot([x - 0.5, x], [y, y + 0.15], color=color, lw=3, solid_capstyle="round")
        ax.plot([x + 0.5, x], [y, y + 0.15], color=color, lw=3, solid_capstyle="round")


# 1. 여는 장면: 가슴에 손, 콩닥콩닥
fig, ax = canvas(10.0, 4.6, 16.0, 7.4)
kid(ax, 4.0, 0.8, 3.0)
ax.plot([4.0 - 1.05, 3.55], [0.8 + 3.0, 0.8 + 1.15 * 3.0], color=INK, lw=2)
ax.add_patch(Circle((3.7, 0.8 + 1.15 * 3.0), 0.32, fc=SKIN, ec=INK, lw=1.4))
ax.text(7.2, 5.0, "콩닥콩닥", ha="left", va="center", fontsize=16, color=RED, fontweight="bold")
ax.text(7.2, 3.6, "가슴에 손을 대면\n무언가 뛰어요", ha="left", va="center", fontsize=12)
ax.text(12.6, 2.0, "자는 동안에도\n뛸까?", ha="center", va="center", fontsize=13, color=RED, fontweight="bold")
save(fig, "b05-chest.svg")

# 2. 이 편의 지도
fig, ax = canvas(11.6, 2.9, 19.4, 4.6)
titles = ["짜고 풀어요", "한쪽으로만 열리는 문", "펌프 두 개", "쉬지 않는 까닭"]
for i, t in enumerate(titles):
    x = 0.3 + i * 4.8
    box(ax, x, 0.4, 3.8, 3.6)
    ax.text(x + 1.9, 0.95, t, ha="center", va="center", fontsize=11, fontweight="bold")
    cx = x + 1.9
    if i == 0:
        ax.add_patch(Ellipse((cx - 0.6, 2.6), 1.0, 1.2, fc=MUSCLE, ec=BLOOD, lw=1.4))
        ax.add_patch(Ellipse((cx + 0.7, 2.6), 0.6, 0.8, fc=MUSCLE, ec=BLOOD, lw=1.4))
    elif i == 1:
        valve(ax, cx, 2.2, True)
        arrow(ax, (cx, 1.8), (cx, 3.3), color=BLOOD, lw=1.6, ms=10)
    elif i == 2:
        ax.add_patch(Ellipse((cx - 0.5, 2.6), 0.9, 1.4, fc=BACK, ec=INK, lw=1.2))
        ax.add_patch(Ellipse((cx + 0.5, 2.6), 0.9, 1.4, fc=BLOOD, ec=INK, lw=1.2))
    else:
        for k in range(4):
            ax.plot([x + 0.5 + k * 0.75, x + 0.75 + k * 0.75, x + 0.9 + k * 0.75, x + 1.05 + k * 0.75],
                    [2.5, 2.5, 3.3, 1.9], color=RED, lw=1.4)
    if i < 3:
        arrow(ax, (x + 3.95, 2.2), (x + 4.65, 2.2))
save(fig, "b05-map.svg")

# 3. 짜고 풀어요: 스포이트와 심장
fig, ax = canvas(11.0, 5.0, 18.0, 8.2)
dropper(ax, 2.0, 2.2, squeezed=False)
dropper(ax, 5.4, 2.2, squeezed=True)
arrow(ax, (5.4, 2.1), (5.4, 1.0), color=BACK, lw=2)
ax.text(2.0, 1.4, "놓으면\n빨려 들어와요", ha="center", va="center", fontsize=10)
ax.text(5.4, 0.4, "쥐면 나가요", ha="center", va="center", fontsize=10)
ax.text(3.7, 6.6, "스포이트", ha="center", va="center", fontsize=12, fontweight="bold")
ax.plot([8.0, 8.0], [0.4, 7.4], color=GREY, lw=1.2, ls="--")
ax.add_patch(Ellipse((11.0, 4.0), 2.8, 3.4, fc=MUSCLE, ec=BLOOD, lw=2))
ax.text(11.0, 4.0, "풀려요\n피가 채워져요", ha="center", va="center", fontsize=10)
ax.add_patch(Ellipse((15.4, 4.0), 1.9, 2.4, fc=MUSCLE, ec=BLOOD, lw=3))
ax.text(15.4, 4.0, "꽉!", ha="center", va="center", fontsize=12, fontweight="bold")
arrow(ax, (15.4, 5.3), (15.4, 6.8), color=BLOOD, lw=2.4)
ax.text(16.2, 6.6, "피가 밀려\n나가요", ha="left", va="center", fontsize=10, color=BLOOD)
arrow(ax, (12.6, 4.0), (14.2, 4.0), color=INK, lw=1.6)
ax.text(13.2, 1.2, "심장은 근육으로 된 주머니예요", ha="center", va="center", fontsize=11, fontweight="bold")
save(fig, "b05-squeeze.svg")

# 4. 한쪽으로만 열리는 문
fig, ax = canvas(11.0, 4.6, 18.0, 7.6)
for k, (x, opened, lab) in enumerate([(4.0, True, "피가 나아가면 문이 열려요"), (13.0, False, "거꾸로 오면 문이 닫혀요")]):
    ax.add_patch(Rectangle((x - 1.2, 0.8), 2.4, 5.6, fc="#f7d6d0", ec=INK, lw=1.4))
    if opened:
        ax.plot([x - 1.2, x - 0.4], [3.2, 4.4], color=INK, lw=4, solid_capstyle="round")
        ax.plot([x + 1.2, x + 0.4], [3.2, 4.4], color=INK, lw=4, solid_capstyle="round")
        arrow(ax, (x, 1.2), (x, 6.0), color=BLOOD, lw=2.6)
    else:
        ax.plot([x - 1.2, x], [3.6, 3.2], color=INK, lw=4, solid_capstyle="round")
        ax.plot([x + 1.2, x], [3.6, 3.2], color=INK, lw=4, solid_capstyle="round")
        arrow(ax, (x, 6.0), (x, 4.0), color=BLOOD, lw=2.6)
        ax.text(x + 1.6, 3.6, "탁!", ha="left", va="center", fontsize=14, color=RED, fontweight="bold")
    ax.text(x, 0.2, lab, ha="center", va="center", fontsize=11, fontweight="bold")
save(fig, "b05-valve.svg")

# 5. 펌프 두 개: 1 온몸→오른쪽, 2 오른쪽→폐, 3 폐→왼쪽, 4 왼쪽→온몸
fig, ax = canvas(11.0, 6.0, 18.0, 9.8)
ax.add_patch(FancyBboxPatch((6.6, 3.4), 2.2, 2.6, boxstyle="round,pad=0.2", fc=MUSCLE, ec=INK, lw=1.6))
ax.add_patch(FancyBboxPatch((9.2, 3.4), 2.2, 2.6, boxstyle="round,pad=0.2", fc=MUSCLE, ec=INK, lw=1.6))
ax.text(7.7, 4.7, "오른쪽\n펌프", ha="center", va="center", fontsize=11, fontweight="bold")
ax.text(10.3, 4.7, "왼쪽\n펌프", ha="center", va="center", fontsize=11, fontweight="bold")
box(ax, 7.0, 7.8, 4.0, 1.4, fc="white")
ax.text(9.0, 8.5, "폐", ha="center", va="center", fontsize=12, fontweight="bold")
box(ax, 6.0, 0.2, 6.0, 1.4, fc=CELL)
ax.text(9.0, 0.9, "온몸의 세포", ha="center", va="center", fontsize=12, fontweight="bold")
arrow(ax, (6.8, 1.7), (6.4, 3.8), color=BACK, lw=2.6, rad=-0.3)
arrow(ax, (7.7, 6.3), (7.9, 7.7), color=BACK, lw=2.6)
arrow(ax, (10.1, 7.7), (10.3, 6.3), color=BLOOD, lw=2.6)
arrow(ax, (11.6, 3.8), (11.2, 1.7), color=BLOOD, lw=2.6, rad=-0.3)
for n, (x, y) in enumerate([(5.6, 2.6), (7.1, 7.0), (10.9, 7.0), (12.4, 2.6)], start=1):
    ax.add_patch(Circle((x, y), 0.36, fc="white", ec=INK, lw=1.4))
    ax.text(x, y, str(n), ha="center", va="center", fontsize=12, fontweight="bold")
ax.text(15.4, 5.0, "파랑: 산소를 많이\n내려 준 피\n빨강: 산소를 실은 피", ha="center", va="center", fontsize=10)
save(fig, "b05-pumps.svg")

# 6. 쉬지 않는 까닭: 짜는 때와 풀린 틈
fig, ax = canvas(11.0, 3.6, 18.0, 5.8)
x = 0.6
for k in range(4):
    ax.add_patch(Rectangle((x, 2.2), 1.35, 1.2, fc=BLOOD, ec=INK, lw=1))
    ax.add_patch(Rectangle((x + 1.35, 2.2), 2.15, 1.2, fc="white", ec=INK, lw=1))
    if k == 0:
        ax.text(x + 0.67, 3.9, "짜요", ha="center", va="center", fontsize=11, color=BLOOD, fontweight="bold")
        ax.text(x + 2.4, 3.9, "풀려서 쉬어요", ha="center", va="center", fontsize=11, fontweight="bold")
    x += 3.5
arrow(ax, (0.6, 1.6), (14.6, 1.6), color=INK, lw=1.4)
ax.text(7.6, 1.0, "시간", ha="center", va="center", fontsize=10)
ax.text(9.0, 5.2, "한 번 뛸 때마다 짜는 때보다 풀려 있는 때가 조금 더 길어요(가만히 있을 때)", ha="center",
        va="center", fontsize=10)
save(fig, "b05-rest.svg")

# 7. 맥박 찾기: 손목 엄지 쪽
fig, ax = canvas(9.0, 4.0, 14.0, 6.2)
ax.add_patch(FancyBboxPatch((1.0, 2.0), 9.0, 2.0, boxstyle="round,pad=0.5", fc=SKIN, ec=INK, lw=1.6))
ax.plot([1.6, 9.6], [2.6, 2.6], color=BACK, lw=2, alpha=0.6)
for k in range(2):
    ax.add_patch(FancyBboxPatch((3.2 + k * 1.2, 2.3), 0.9, 2.4, boxstyle="round,pad=0.25", fc="#fbe7dc", ec=INK,
                                lw=1.4))
ax.text(11.2, 3.0, "엄지 쪽", ha="left", va="center", fontsize=11, fontweight="bold")
arrow(ax, (11.1, 3.0), (10.2, 2.7), color=INK, lw=1.4, ms=12)
ax.text(5.5, 5.6, "검지와 가운뎃손가락을 살짝 대요", ha="center", va="center", fontsize=11)
ax.text(5.5, 0.6, "톡, 톡, 톡: 심장이 밀어낸 피가 핏줄을 두드려요", ha="center", va="center", fontsize=11,
        color=RED, fontweight="bold")
save(fig, "b05-pulse.svg")
