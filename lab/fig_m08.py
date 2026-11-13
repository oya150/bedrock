"""물질과 에너지 8편 그림 만들기. 실행: python lab/fig_m08.py  → docs/matter/img/08/*.svg
검토용 PNG가 필요하면 FIG_FMT=png FIG_OUT=<폴더> 로 실행한다.

글자는 SVG 안에 글자로 남긴다(글꼴 모양을 파일에 넣지 않는다). 보는 쪽 글꼴로 그려진다.
카드는 차분한 색으로, 강조(새로 받은 카드, 비교 화살표, 많이 든 일)만 빨강으로 칠한다.
"""
import itertools
import os

import matplotlib

matplotlib.use("svg" if os.environ.get("FIG_FMT", "svg") == "svg" else "agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Arc, Circle, FancyArrowPatch, FancyBboxPatch, Rectangle

OUT = os.environ.get("FIG_OUT") or os.path.join(os.path.dirname(__file__), "..", "docs", "matter", "img", "08")
FMT = os.environ.get("FIG_FMT", "svg")
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
    name = name.rsplit(".", 1)[0] + "." + FMT
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
import random
from matplotlib.patches import Ellipse, Polygon

random.seed(2)
WATER = "#7da2c8"
ICE = "#dbeaf5"


def particle(ax, x, y, r=0.24, fc=WATER):
    ax.add_patch(Circle((x, y), r, fc=fc, ec=INK, lw=0.7))


def jig(ax, x, y, s=0.12):
    for a in (0, 180):
        r = math.radians(a)
        ax.plot([x + 0.28 * math.cos(r), x + (0.28 + s) * math.cos(r)], [y, y], color=INK, lw=0.7)


def solid(ax, x0, y0, rows=4, cols=5, gap=0.5):
    for i in range(rows):
        for j in range(cols):
            particle(ax, x0 + j * gap, y0 + i * gap)
            jig(ax, x0 + j * gap, y0 + i * gap)


def liquid(ax, x0, y0, w, h, n=None, gap=0.5):
    pts = []
    y = y0 + 0.3
    while y < y0 + h - 0.25:
        x = x0 + 0.3 + random.uniform(0, gap / 2)
        while x < x0 + w - 0.25:
            if random.random() > 0.06:
                pts.append((x + random.uniform(-0.07, 0.07), y + random.uniform(-0.07, 0.07)))
            x += gap * random.uniform(0.98, 1.1)
        y += gap * random.uniform(0.9, 1.0)
    for p in pts:
        particle(ax, *p)
    for p in pts[::5]:
        arrow(ax, p, (p[0] + random.uniform(-0.4, 0.4), p[1] + random.uniform(-0.25, 0.25)), color=INK, lw=0.8, ms=6)


def gas(ax, x0, y0, w, h, n=6):
    pts = []
    for _ in range(5000):
        if len(pts) >= n:
            break
        p = (x0 + random.uniform(0.4, w - 1.0), y0 + random.uniform(0.4, h - 1.0))
        if all((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2 > 1.4 ** 2 for q in pts):
            pts.append(p)
    for p in pts:
        particle(ax, *p)
        a = random.uniform(0, 2 * math.pi)
        arrow(ax, p, (p[0] + 0.8 * math.cos(a), p[1] + 0.8 * math.sin(a)), color=RED, lw=1.0, ms=8)


def mover(ax, x, y, strength, r=0.24, fc=WATER, color=None):
    """알갱이 하나와 꿈틀거림 세기만큼의 화살표."""
    particle(ax, x, y, r=r, fc=fc)
    a = random.uniform(0, 2 * math.pi)
    L = r + strength
    arrow(ax, (x + (r + 0.02) * math.cos(a), y + (r + 0.02) * math.sin(a)), (x + L * math.cos(a), y + L * math.sin(a)),
          color=color or (RED if strength > 0.5 else INK), lw=1.2 if strength > 0.5 else 0.9, ms=8)


def cup(ax, x, y, w, h, fc="#eef5fb"):
    ax.add_patch(Polygon([(x, y + h), (x + w, y + h), (x + w - 0.3, y), (x + 0.3, y)], closed=True, fc=fc, ec=INK,
                         lw=1.6))


def hand(ax, x, y, s=1.0):
    ax.add_patch(FancyBboxPatch((x, y), 2.6 * s, 2.0 * s, boxstyle="round,pad=0.25", fc="#f6d8c4", ec=INK, lw=1.4))
    for k in range(4):
        ax.add_patch(FancyBboxPatch((x + 0.1 * s + k * 0.65 * s, y + 2.05 * s), 0.42 * s, 0.9 * s,
                                    boxstyle="round,pad=0.12", fc="#f6d8c4", ec=INK, lw=1.2))


BALL = "#f08c6c"
SUN = YEL


def ball(ax, x, y, r=0.35):
    ax.add_patch(Circle((x, y), r, fc=BALL, ec=INK, lw=1.2))


def waves(ax, x, y, ang, L=1.0, color=RED):
    xs = [x + t * L / 12 * math.cos(ang) - 0.08 * math.sin(t * 1.3) * math.sin(ang) for t in range(13)]
    ys = [y + t * L / 12 * math.sin(ang) + 0.08 * math.sin(t * 1.3) * math.cos(ang) for t in range(13)]
    ax.plot(xs, ys, color=color, lw=1.4)


def sound(ax, x, y, n=3, r0=0.4):
    for k in range(n):
        ax.add_patch(Arc((x, y), 2 * (r0 + k * 0.3), 2 * (r0 + k * 0.3), theta1=-40, theta2=40, color=INK, lw=1.2))


def sun(ax, x, y, r=0.6):
    ax.add_patch(Circle((x, y), r, fc=SUN, ec=INK, lw=1))
    for a in range(0, 360, 45):
        t = math.radians(a)
        ax.plot([x + (r + 0.15) * math.cos(t), x + (r + 0.4) * math.cos(t)],
                [y + (r + 0.15) * math.sin(t), y + (r + 0.4) * math.sin(t)], color=INK, lw=1)


# 1. 여러 모습
fig, ax = canvas(12.0, 3.4, 22.0, 6.2)
labs = ["움직임", "높이", "따뜻함", "빛", "소리"]
for i, lab in enumerate(labs):
    x = 0.3 + i * 4.35
    box(ax, x, 0.5, 3.9, 4.4, fc=NOTE)
    cx = x + 1.95
    if i == 0:
        ball(ax, cx - 0.5, 2.6, 0.45)
        arrow(ax, (cx + 0.05, 2.6), (cx + 1.3, 2.6), color=RED, lw=2)
    elif i == 1:
        ax.add_patch(Rectangle((cx - 1.2, 3.3), 2.4, 0.2, fc="#c8a27a", ec=INK, lw=1))
        ball(ax, cx, 3.85, 0.35)
        ax.plot([cx - 1.2, cx - 1.2], [1.2, 3.3], color=INK, lw=1)
    elif i == 2:
        cup(ax, cx - 0.8, 1.4, 1.6, 1.8, fc="#fbe9e3")
        for k in range(3):
            waves(ax, cx - 0.4 + k * 0.4, 3.4, math.pi / 2, 0.9)
    elif i == 3:
        ax.add_patch(Circle((cx, 3.0), 0.6, fc=SUN, ec=INK, lw=1.2))
        ax.add_patch(Rectangle((cx - 0.3, 2.0), 0.6, 0.45, fc=GREY, ec=INK, lw=1))
        for a in range(0, 181, 30):
            t = math.radians(a)
            ax.plot([cx + 0.8 * math.cos(t), cx + 1.15 * math.cos(t)], [3.0 + 0.8 * math.sin(t), 3.0 + 1.15 * math.sin(t)],
                    color=INK, lw=1)
    else:
        ax.add_patch(Rectangle((cx - 1.2, 1.6), 1.6, 1.3, fc="#e9a96b", ec=INK, lw=1.2))
        sound(ax, cx + 0.4, 2.5, 3, 0.4)
    ax.text(cx, 1.0, lab, ha="center", va="center", fontsize=11, fontweight="bold")
ax.text(11.0, 5.7, "모두 에너지", ha="center", va="center", fontsize=12, color=RED, fontweight="bold")
save(fig, "m08-forms.svg")

# 2. 떨어지며 바뀌어요
fig, ax = canvas(8.0, 5.0, 13.0, 8.2)
ax.plot([3.5, 9.5], [0.6, 0.6], color=INK, lw=1.6)
for (y, L, lab) in [(7.0, 0, "높이 많음"), (4.6, 0.7, ""), (2.2, 1.2, "움직임 많음")]:
    ball(ax, 6.5, y, 0.4)
    if L:
        arrow(ax, (7.2, y + 0.4), (7.2, y + 0.4 - L), color=RED, lw=2, ms=12)
    if lab:
        ax.text(7.9, y, lab, ha="left", va="center", fontsize=11, fontweight="bold", color=RED if L else "#222")
ax.annotate("", (2.8, 1.0), (2.8, 7.2), arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.4))
ax.text(2.3, 4.1, "높이\n↓\n움직임", ha="right", va="center", fontsize=11)
save(fig, "m08-fall.svg")

# 3. 튀는 공: 처음 높이까지 못 올라가요
fig, ax = canvas(10.0, 4.4, 16.0, 7.2)
ax.plot([0.5, 15.5], [0.8, 0.8], color=INK, lw=1.6)
ax.add_patch(FancyBboxPatch((0.9, 5.7), 1.2, 0.6, boxstyle="round,pad=0.12", fc="#f6d8c4", ec=INK, lw=1.2))
ball(ax, 1.5, 5.25)
ax.plot([0.6, 13.0], [5.25, 5.25], color=RED, lw=1.4, ls="--")
ax.text(13.2, 5.25, "처음 높이", ha="left", va="center", fontsize=10.5, color=RED, fontweight="bold")
ax.plot([1.5, 1.5], [4.85, 1.2], color=INK, lw=1, ls="--")
x = 1.5
for n, (h, w) in enumerate([(3.6, 3.2), (2.5, 2.7), (1.6, 2.2), (0.9, 1.7)], start=1):
    t = [i / 30 for i in range(31)]
    ax.plot([x + w * u for u in t], [1.15 + h * 4 * u * (1 - u) for u in t], color=INK, lw=1, ls="--")
    ax.text(x + w / 2, 1.15 + h + 0.3, str(n), ha="center", va="center", fontsize=10.5)
    x += w
ball(ax, x + 0.8, 1.15)
save(fig, "m08-bounce.svg")

# 4. 소리와 열로 흩어져요
fig, ax = canvas(10.0, 4.6, 16.0, 7.4)
ax.add_patch(Rectangle((0.5, 0.6), 7.0, 1.0, fc="#d9d2c5", ec=INK, lw=1.2))
ax.add_patch(Ellipse((3.5, 2.05), 1.9, 0.9, fc=BALL, ec=INK, lw=1.2))
sound(ax, 4.8, 2.4, 3, 0.5)
ax.text(5.6, 3.9, "통!", ha="center", va="center", fontsize=13, fontweight="bold")
ax.text(6.7, 3.4, "소리", ha="left", va="center", fontsize=11.5, color=RED, fontweight="bold")
ax.plot([3.9, 10.2], [2.2, 3.4], color=RED, lw=1, ls="--")
ax.add_patch(Circle((12.2, 3.8), 2.4, fc="#fde3d9", ec=RED, lw=2))
for i in range(5):
    for j in range(5):
        x, y = 10.9 + j * 0.65, 2.5 + i * 0.65
        if (x - 12.2) ** 2 + (y - 3.8) ** 2 < 2.0 ** 2:
            mover(ax, x, y, 0.6, r=0.18, fc=BALL, color=RED)
ax.text(12.2, 0.8, "공 속 알갱이", ha="center", va="center", fontsize=10.5)
ax.text(12.2, 6.7, "열", ha="center", va="center", fontsize=11.5, color=RED, fontweight="bold")
save(fig, "m08-spread.svg")

# 5. 튈 때마다: 전체는 같고 나눠 가진 몫만 바뀌어요
fig, ax = canvas(9.0, 4.4, 15.0, 7.4)
labs = ["처음", "1번 튄 뒤", "2번 튄 뒤", "3번 튄 뒤"]
ball_part = [5.0, 3.6, 2.5, 1.6]
for k, (lab, b) in enumerate(zip(labs, ball_part)):
    x = 1.0 + k * 2.6
    ax.add_patch(Rectangle((x, 1.0), 1.4, b, fc=BALL, ec=INK, lw=1.2))
    if b < 5.0:
        ax.add_patch(Rectangle((x, 1.0 + b), 1.4, 5.0 - b, fc="#fbe3dc", ec=RED, lw=1.6))
    ax.text(x + 0.7, 0.5, lab, ha="center", va="center", fontsize=10)
ax.plot([0.6, 11.4], [6.0, 6.0], color=INK, lw=1, ls="--")
ax.text(11.6, 6.0, "전체", ha="left", va="center", fontsize=10.5)
ax.add_patch(Rectangle((11.6, 3.6), 0.5, 0.5, fc="#fbe3dc", ec=RED, lw=1.6))
ax.text(12.3, 3.85, "소리와 열", ha="left", va="center", fontsize=10.5, color=RED, fontweight="bold")
ax.add_patch(Rectangle((11.6, 2.4), 0.5, 0.5, fc=BALL, ec=INK, lw=1.2))
ax.text(12.3, 2.65, "공", ha="left", va="center", fontsize=10.5)
save(fig, "m08-total.svg")

# 6. 거슬러 올라가면 햇빛
fig, ax = canvas(12.0, 4.2, 22.0, 7.6)
sun(ax, 1.4, 3.8, 0.8)
ax.text(1.4, 2.3, "햇빛", ha="center", va="center", fontsize=11, color=RED, fontweight="bold")
for y, items in [(5.6, ["풀과 밀", "빵", "뛰는 아이"]), (2.0, ["오래전\n식물과 생물", "땅속 기름", "초", "열과 빛"])]:
    arrow(ax, (2.6, 3.8 + (0.5 if y > 4 else -0.5)), (3.6, y), color=RED, lw=1.6)
    for k, lab in enumerate(items):
        x = 5.0 + k * 4.3
        box(ax, x - 1.3, y - 0.7, 2.6, 1.4, fc=NOTE)
        ax.text(x, y, lab, ha="center", va="center", fontsize=10.5, fontweight="bold")
        if k < len(items) - 1:
            arrow(ax, (x + 1.45, y), (x + 2.85, y), color=INK, lw=1.4)
save(fig, "m08-sun.svg")
