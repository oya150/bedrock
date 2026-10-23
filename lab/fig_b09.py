"""인체 9편 그림 만들기. 실행: python lab/fig_b09.py  → docs/body/img/09/*.svg

글자는 SVG 안에 글자로 남긴다(글꼴 모양을 파일에 넣지 않는다). 보는 쪽 글꼴로 그려진다.
카드는 차분한 색으로, 강조(새로 받은 카드, 비교 화살표, 많이 든 일)만 빨강으로 칠한다.
"""
import itertools
import os

import matplotlib

matplotlib.use("svg")
import matplotlib.pyplot as plt
from matplotlib.patches import Arc, Circle, FancyArrowPatch, FancyBboxPatch, Rectangle

OUT = os.path.join(os.path.dirname(__file__), "..", "docs", "body", "img", "09")
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

BONE = "#efe6d2"
MUSCLE = "#e8a598"
TENDON = "#c9b79c"
SKIN = "#f6d8c4"
CELL = "#fbe3dc"


def bone(ax, p, q, w=0.5):
    (x1, y1), (x2, y2) = p, q
    L = math.hypot(x2 - x1, y2 - y1)
    a = math.degrees(math.atan2(y2 - y1, x2 - x1))
    ax.add_patch(FancyBboxPatch((0, -w / 2), L, w, boxstyle=f"round,pad=0,rounding_size={w/2}", fc=BONE, ec=INK,
                                lw=1.4, transform=__import__("matplotlib").transforms.Affine2D().rotate_deg(a).translate(x1, y1) + ax.transData))


def muscle(ax, p, q, fat=0.6, fc=MUSCLE, ec=RED, lw=1.4):
    (x1, y1), (x2, y2) = p, q
    cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
    L = math.hypot(x2 - x1, y2 - y1)
    a = math.degrees(math.atan2(y2 - y1, x2 - x1))
    ax.add_patch(Ellipse((cx, cy), L, fat, angle=a, fc=fc, ec=ec, lw=lw))


def arm(ax, sx, sy, ang, upper=4.0, fore=3.6, bent=True, label=True):
    """어깨(sx, sy)에서 위팔은 아래로, 아래팔은 ang 도로."""
    ex, ey = sx, sy - upper
    hx, hy = ex + fore * math.cos(math.radians(ang)), ey + fore * math.sin(math.radians(ang))
    bone(ax, (sx, sy), (ex, ey), w=0.5)
    bone(ax, (ex, ey), (hx, hy), w=0.42)
    ax.add_patch(Circle((ex, ey), 0.38, fc=BONE, ec=INK, lw=1.4))
    # 앞 근육: 어깨 앞 → 아래팔 (팔꿈치 조금 아래)
    ins = (ex + 0.9 * math.cos(math.radians(ang)), ey + 0.9 * math.sin(math.radians(ang)))
    front_fat = 1.1 if bent else 0.55
    back_fat = 0.55 if bent else 1.0
    muscle(ax, (sx + 0.55, sy - 0.4), (ins[0] + 0.1, ins[1] + 0.25), fat=front_fat,
           fc=RED if bent else MUSCLE)
    muscle(ax, (sx - 0.55, sy - 0.4), (ex - 0.45, ey - 0.1), fat=back_fat, fc=MUSCLE if bent else RED)
    return (ex, ey), (hx, hy)


# 1. 여는 장면: 팔을 굽혀 알통
fig, ax = canvas(10.0, 4.8, 16.0, 7.6)
kid(ax, 3.4, 0.6, 3.0)
ax.plot([3.4 + 1.05, 5.2], [0.6 + 3.0, 0.6 + 3.0], color=INK, lw=2)
ax.plot([5.2, 5.2], [3.6, 5.2], color=INK, lw=2)
ax.add_patch(Ellipse((4.75, 3.85), 0.9, 0.55, fc=CELL, ec=RED, lw=1.4))
ax.text(4.75, 2.9, "알통!", ha="center", va="center", fontsize=12, color=RED, fontweight="bold")
ax.text(8.0, 5.4, "팔을 굽히면 위팔 앞이 불룩\n벽을 밀며 펴면 위팔 뒤가 단단", ha="left", va="center", fontsize=12)
ax.text(10.6, 2.4, "어떻게 움직이는 걸까?", ha="center", va="center", fontsize=13, color=RED, fontweight="bold")
save(fig, "b09-flex.svg")

# 2. 이 편의 지도
fig, ax = canvas(11.6, 2.9, 19.4, 4.6)
titles = ["뼈가 하는 일", "뼈에 붙은 근육은\n당기기만 해요", "짝 근육", "관절은 문의 경첩처럼"]
for i, t in enumerate(titles):
    x = 0.3 + i * 4.8
    box(ax, x, 0.4, 3.8, 3.6)
    ax.text(x + 1.9, 0.95, t, ha="center", va="center", fontsize=11, fontweight="bold")
    cx = x + 1.9
    if i == 0:
        bone(ax, (cx - 1.0, 2.6), (cx + 1.0, 2.6), w=0.45)
    elif i == 1:
        muscle(ax, (cx - 1.0, 2.6), (cx + 0.4, 2.6), fat=0.7)
        arrow(ax, (cx + 0.9, 2.6), (cx + 0.3, 2.6), color=RED, lw=1.6, ms=10)
    elif i == 2:
        muscle(ax, (cx - 1.0, 3.0), (cx + 1.0, 3.0), fat=0.5, fc=RED)
        muscle(ax, (cx - 1.0, 2.2), (cx + 1.0, 2.2), fat=0.5)
    else:
        ax.plot([cx - 1.4, cx - 1.4], [1.6, 3.6], color=INK, lw=3)
        ax.plot([cx - 1.4, cx + 1.0], [2.0, 3.2], color="#b58b5a", lw=5)
        ax.add_patch(Circle((cx - 1.4, 2.0), 0.18, fc=YEL, ec=INK, lw=1))
    if i < 3:
        arrow(ax, (x + 3.95, 2.2), (x + 4.65, 2.2))
save(fig, "b09-map.svg")

# 3. 뼈가 하는 일: 받치기, 지키기, 피 세포 만들기
fig, ax = canvas(11.0, 4.6, 18.0, 7.6)
# 받치기: 텐트
ax.add_patch(Polygon([(0.6, 1.4), (2.8, 5.4), (5.0, 1.4)], closed=True, fc=CELL, ec=INK, lw=1.4))
ax.plot([2.8, 2.8], [1.4, 5.4], color=INK, lw=3)
ax.text(2.8, 0.7, "받쳐요", ha="center", va="center", fontsize=12, fontweight="bold")
ax.text(2.8, 6.4, "텐트의 기둥처럼", ha="center", va="center", fontsize=10)
# 지키기: 갈비뼈 우리
for k in range(5):
    ax.add_patch(Arc((9.0, 3.6), 3.4 - k * 0.1, 3.2 - k * 0.5, theta1=200, theta2=340, color=INK, lw=2.4))
    ax.add_patch(Arc((9.0, 3.6 + k * 0.0), 3.4 - k * 0.1, 3.2 - k * 0.5, theta1=20, theta2=160, color=INK, lw=2.4))
ax.add_patch(Ellipse((9.2, 3.5), 0.9, 1.1, fc=MUSCLE, ec=RED, lw=1.4))
ax.text(9.0, 0.7, "지켜요", ha="center", va="center", fontsize=12, fontweight="bold")
ax.text(9.0, 6.4, "갈비뼈가 심장을", ha="center", va="center", fontsize=10)
# 피 세포 만들기
bone(ax, (13.0, 3.6), (17.0, 3.6), w=1.4)
ax.add_patch(Ellipse((15.0, 3.6), 2.6, 0.7, fc="#f2b8a6", ec=RED, lw=1))
for k in range(5):
    ax.add_patch(Circle((14.1 + k * 0.45, 3.6 + 0.12 * (k % 2)), 0.12, fc=RED, ec=RED))
ax.text(15.0, 0.7, "피의 세포를 만들어요", ha="center", va="center", fontsize=12, fontweight="bold")
ax.text(15.0, 6.4, "뼈 속 붉은 곳에서", ha="center", va="center", fontsize=10)
save(fig, "b09-bone.svg")

# 4. 근육은 당기기만: 줄다리기 줄
fig, ax = canvas(11.0, 4.0, 18.0, 6.6)
bone(ax, (1.0, 2.0), (6.0, 2.0), w=0.5)
bone(ax, (6.4, 2.0), (11.0, 2.0), w=0.5)
ax.add_patch(Circle((6.2, 2.0), 0.35, fc=BONE, ec=INK, lw=1.4))
muscle(ax, (1.6, 3.2), (6.9, 3.0), fat=1.0, fc=RED)
ax.plot([6.9, 7.4], [3.0, 2.3], color=TENDON, lw=3)
ax.plot([1.6, 1.4], [3.2, 2.3], color=TENDON, lw=3)
arrow(ax, (6.2, 4.4), (3.6, 4.4), color=RED, lw=2.2)
ax.text(4.2, 5.0, "짧아지면서 당겨요", ha="center", va="center", fontsize=11, color=RED, fontweight="bold")
ax.text(7.9, 3.4, "힘줄", ha="left", va="center", fontsize=10, color="#8a6d3b", fontweight="bold")
ax.plot([12.4, 12.4], [0.6, 6.0], color=GREY, lw=1.2, ls="--")
ax.plot([13.4, 17.4], [3.4, 3.4], color="#b58b5a", lw=4)
arrow(ax, (14.8, 4.3), (13.4, 4.3), color=INK, lw=1.8)
ax.text(15.4, 5.2, "줄은 당길 수만 있어요", ha="center", va="center", fontsize=11)
ax.text(15.4, 2.2, "밀면 휘어져요", ha="center", va="center", fontsize=10)
ax.plot([13.4, 14.4, 15.4, 16.4, 17.4], [1.2, 1.6, 1.2, 1.6, 1.2], color="#b58b5a", lw=4)
save(fig, "b09-pull.svg")

# 5. 짝 근육: 굽히기 / 펴기
fig, ax = canvas(11.0, 5.4, 18.0, 8.8)
arm(ax, 3.0, 7.6, ang=60, bent=True)
ax.text(3.6, -0.5, "굽힐 때: 앞 근육이 당겨요", ha="center", va="center", fontsize=11, fontweight="bold")
ax.text(5.4, 6.2, "앞", ha="left", va="center", fontsize=11, color=RED, fontweight="bold")
ax.text(1.4, 6.2, "뒤", ha="right", va="center", fontsize=11, fontweight="bold")
ax.plot([9.0, 9.0], [0.4, 8.4], color=GREY, lw=1.2, ls="--")
arm(ax, 12.0, 7.6, ang=-90, bent=False)
ax.text(13.0, -0.5, "펼 때: 뒤 근육이 당겨요", ha="center", va="center", fontsize=11, fontweight="bold")
ax.text(14.4, 6.2, "앞", ha="left", va="center", fontsize=11, fontweight="bold")
ax.text(10.4, 6.2, "뒤", ha="right", va="center", fontsize=11, color=RED, fontweight="bold")
ax.text(9.0, 8.6, "빨간 근육이 당기는 근육이에요. 다른 쪽은 풀려서 늘어나요", ha="center", va="center", fontsize=10)
ax.set_ylim(-1.0, 9.0)
save(fig, "b09-pair.svg")

# 6. 관절은 문의 경첩처럼
fig, ax = canvas(11.0, 4.4, 18.0, 7.2)
ax.plot([1.0, 1.0], [0.8, 6.6], color=INK, lw=5)
ax.plot([1.0, 7.6], [1.6, 4.4], color="#b58b5a", lw=8, solid_capstyle="round")
ax.add_patch(Circle((1.0, 1.6), 0.32, fc=YEL, ec=INK, lw=1.4))
ax.text(1.6, 0.9, "경첩", ha="left", va="center", fontsize=10, fontweight="bold")
arrow(ax, (2.3, 1.5), (2.0, 2.4), color=RED, lw=1.8, ms=12)
ax.add_patch(Arc((1.0, 1.6), 14.4, 14.4, theta1=23, theta2=48, color=INK, lw=1.4, ls="--"))
ax.text(5.6, 6.4, "문 끝은 크게 움직여요", ha="center", va="center", fontsize=10)
ax.text(4.5, 0.2, "경첩 옆을 조금만 밀어도 문 끝은 크게 움직여요", ha="center", va="center", fontsize=10, fontweight="bold")
ax.plot([9.4, 9.4], [0.4, 6.8], color=GREY, lw=1.2, ls="--")
bone(ax, (11.4, 6.2), (11.4, 2.4), w=0.5)
bone(ax, (11.4, 2.4), (16.6, 4.6), w=0.42)
ax.add_patch(Circle((11.4, 2.4), 0.42, fc=YEL, ec=INK, lw=1.6))
muscle(ax, (11.9, 5.8), (12.4, 2.95), fat=0.8, fc=RED)
ax.text(10.8, 1.6, "관절(팔꿈치)", ha="center", va="center", fontsize=11, fontweight="bold")
arrow(ax, (12.9, 3.6), (12.6, 4.2), color=RED, lw=1.4, ms=10)
ax.add_patch(Arc((11.4, 2.4), 10.0, 10.0, theta1=10, theta2=40, color=INK, lw=1.4, ls="--"))
ax.text(16.6, 6.2, "손은 크게 움직여요", ha="center", va="center", fontsize=10)
ax.text(14.0, 0.2, "근육은 관절 가까이를 조금만 당겨요", ha="center", va="center", fontsize=10, fontweight="bold")
ax.set_ylim(-0.3, 7.2)
save(fig, "b09-lever.svg")
