"""물질과 에너지 9편 그림 만들기. 실행: python lab/fig_m09.py  → docs/matter/img/09/*.svg

글자는 SVG 안에 글자로 남긴다(글꼴 모양을 파일에 넣지 않는다). 보는 쪽 글꼴로 그려진다.
카드는 차분한 색으로, 강조(새로 받은 카드, 비교 화살표, 많이 든 일)만 빨강으로 칠한다.
"""
import itertools
import os

import matplotlib

matplotlib.use("svg")
import matplotlib.pyplot as plt
from matplotlib.patches import Arc, Circle, FancyArrowPatch, FancyBboxPatch, Rectangle

OUT = os.path.join(os.path.dirname(__file__), "..", "docs", "matter", "img", "09")
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


BOXC, BAND, SKIN = "#e8d3b0", "#c0504d", "#f6d8c4"


def band(ax, x0, x1, y, amp=0.3, n=3, color=BAND):
    for k in range(n):
        a = amp * (1 - 2 * k / max(n - 1, 1))
        xs = [x0 + (x1 - x0) * t / 30 for t in range(31)]
        ys = [y + a * math.sin(math.pi * t / 30) for t in range(31)]
        ax.plot(xs, ys, color=color, lw=1.6, alpha=1.0 if k == n // 2 else 0.45)


def ear(ax, x, y, s=1.0):
    ax.add_patch(Arc((x, y), 1.2 * s, 1.8 * s, theta1=-100, theta2=100, color=INK, lw=2))
    ax.add_patch(Arc((x - 0.05, y), 0.5 * s, 0.8 * s, theta1=-80, theta2=80, color=INK, lw=1.4))


def sound(ax, x, y, n=3, r0=0.4, color=INK):
    for k in range(n):
        ax.add_patch(Arc((x, y), 2 * (r0 + k * 0.35), 2 * (r0 + k * 0.35), theta1=-40, theta2=40, color=color, lw=1.4))


def wave(ax, x0, x1, y, amp, cyc, color=INK):
    xs = [x0 + (x1 - x0) * t / 200 for t in range(201)]
    ys = [y + amp * math.sin(2 * math.pi * cyc * t / 200) for t in range(201)]
    ax.plot(xs, ys, color=color, lw=1.6)


def chain(ax, x0, y, n, r=0.16, base=0.42, comp=0.18, phase=0.0, fc=WATER):
    xs = []
    x = x0
    for k in range(n):
        xs.append(x)
        x += base + comp * math.sin(2 * math.pi * k / 7 + phase)
    for xx in xs:
        ax.add_patch(Circle((xx, y), r, fc=fc, ec=INK, lw=0.6))
    return xs


# 1. 여는 장면: 고무줄 상자
fig, ax = canvas(9.0, 4.0, 15.0, 6.6)
ax.add_patch(Rectangle((1.0, 1.0), 5.0, 2.0, fc=BOXC, ec=INK, lw=1.4))
ax.add_patch(Rectangle((1.2, 1.2), 4.6, 1.6, fc="#c9b28c", ec="none"))
band(ax, 1.0, 6.0, 2.0, 0.35, 3)
ax.add_patch(Ellipse((4.3, 2.9), 0.5, 0.3, fc=SKIN, ec=INK, lw=1, angle=30))
sound(ax, 6.6, 2.2, 3, 0.5)
ear(ax, 11.5, 2.2, 1.4)
ax.text(11.5, 0.6, "귀", ha="center", va="center", fontsize=10)
ax.text(7.5, 6.1, "소리는 어떻게 귀까지 올까?", ha="center", va="center", fontsize=12, color=RED, fontweight="bold")
save(fig, "m09-band.svg")

# 2. 이 편의 지도
fig, ax = canvas(11.6, 2.9, 19.4, 4.6)
titles = ["소리는 떨림", "공기 알갱이가 밀고 당겨요", "크고 작게, 높고 낮게", "공기 말고도 전해져요"]
for i, t in enumerate(titles):
    x = 0.3 + i * 4.8
    box(ax, x, 0.4, 3.8, 3.6)
    ax.text(x + 1.9, 0.95, t, ha="center", va="center", fontsize=10, fontweight="bold")
    cx = x + 1.9
    if i == 0:
        band(ax, cx - 1.3, cx + 1.3, 2.5, 0.3, 3)
    elif i == 1:
        chain(ax, cx - 1.5, 2.5, 8, r=0.1, base=0.42, comp=0.13)
    elif i == 2:
        wave(ax, cx - 1.4, cx + 1.4, 3.0, 0.35, 2)
        wave(ax, cx - 1.4, cx + 1.4, 2.0, 0.15, 5)
    else:
        cup(ax, cx - 1.6, 2.1, 0.7, 0.8, fc="white")
        cup(ax, cx + 0.9, 2.1, 0.7, 0.8, fc="white")
        ax.plot([cx - 0.9, cx + 0.9], [2.5, 2.5], color=INK, lw=1)
    if i < 3:
        arrow(ax, (x + 3.95, 2.2), (x + 4.65, 2.2))
save(fig, "m09-map.svg")

# 3. 떨리는 것들
fig, ax = canvas(11.0, 3.6, 18.0, 6.0)
for i, lab in enumerate(["고무줄", "북", "목"]):
    x = 0.3 + i * 6.0
    box(ax, x, 0.5, 5.4, 4.6, fc=NOTE)
    cx = x + 2.7
    if i == 0:
        band(ax, cx - 1.8, cx + 1.8, 3.0, 0.4, 3)
    elif i == 1:
        ax.add_patch(Rectangle((cx - 1.4, 1.6), 2.8, 1.4, fc="#e9a96b", ec=INK, lw=1.2))
        for k, a in enumerate([0.25, 0, -0.25]):
            ax.add_patch(Arc((cx, 3.0), 2.8, 2 * abs(a) + 0.05, theta1=0 if a >= 0 else 180, theta2=180 if a >= 0 else 360,
                             color=INK, lw=1.4, alpha=1.0 if a == 0 else 0.45))
    else:
        kid(ax, cx, 1.3, 1.5)
        ax.add_patch(Ellipse((cx + 0.55, 2.9), 0.45, 0.28, fc=SKIN, ec=INK, lw=1))
        for k in range(3):
            ax.plot([cx - 0.15 + k * 0.15, cx - 0.15 + k * 0.15], [2.75, 3.05], color=RED, lw=1)
        ax.text(cx + 1.3, 4.1, "아—", ha="center", va="center", fontsize=11)
    ax.text(cx, 1.0, lab, ha="center", va="center", fontsize=11, fontweight="bold")
ax.text(9.0, 5.6, "소리가 나는 곳은 모두 떨려요", ha="center", va="center", fontsize=11, color=RED, fontweight="bold")
save(fig, "m09-shake.svg")

# 4. 공기 알갱이가 차례로 밀어요
fig, ax = canvas(11.0, 3.8, 18.0, 6.2)
band(ax, 0.6, 0.6, 2.6, 0.0, 1)
ax.plot([1.0, 1.0], [1.4, 3.8], color=BAND, lw=2.4)
ax.plot([0.8, 0.8], [1.4, 3.8], color=BAND, lw=1.4, alpha=0.4)
ax.plot([1.2, 1.2], [1.4, 3.8], color=BAND, lw=1.4, alpha=0.4)
xs = chain(ax, 1.7, 2.6, 30, r=0.14, base=0.48, comp=0.16)
k = 10
ax.annotate("", (xs[k] + 0.35, 2.15), (xs[k] - 0.35, 2.15), arrowprops=dict(arrowstyle="<|-|>", color=INK, lw=1.2))
ax.text(xs[k], 1.6, "조금 밀렸다\n돌아와요", ha="center", va="center", fontsize=10)
dense = min(range(3, 25), key=lambda i: xs[i + 1] - xs[i])
sparse = max(range(3, 25), key=lambda i: xs[i + 1] - xs[i])
ax.text((xs[dense] + xs[dense + 1]) / 2, 3.2, "촘촘해요", ha="center", va="center", fontsize=9.5)
ax.text((xs[sparse] + xs[sparse + 1]) / 2, 3.2, "듬성해요", ha="center", va="center", fontsize=9.5)
arrow(ax, (3.0, 4.0), (14.0, 4.0), color=RED, lw=2.2)
ax.text(8.5, 4.6, "촘촘한 곳과 듬성한 곳이 귀까지 가요", ha="center", va="center", fontsize=11, color=RED, fontweight="bold")
ear(ax, 16.8, 2.6, 1.4)
ax.text(16.8, 1.0, "귀", ha="center", va="center", fontsize=10)
save(fig, "m09-push.svg")

# 5. 크고 작게, 높고 낮게
fig, ax = canvas(11.0, 4.4, 18.0, 7.2)
wave(ax, 0.6, 6.0, 5.4, 0.8, 2)
wave(ax, 7.0, 12.4, 5.4, 0.3, 2)
ax.text(3.3, 4.1, "세게 떨면 큰 소리", ha="center", va="center", fontsize=10.5, fontweight="bold", color=RED)
ax.text(9.7, 4.1, "살살 떨면 작은 소리", ha="center", va="center", fontsize=10.5, fontweight="bold")
wave(ax, 0.6, 6.0, 2.0, 0.5, 7)
wave(ax, 7.0, 12.4, 2.0, 0.5, 2)
ax.text(3.3, 0.8, "빨리 떨면 높은 소리", ha="center", va="center", fontsize=10.5, fontweight="bold", color=RED)
ax.text(9.7, 0.8, "천천히 떨면 낮은 소리", ha="center", va="center", fontsize=10.5, fontweight="bold")
ax.text(6.5, 0.0, "물결은 떨림의 크기와 빠르기를 나타낸 그림이에요", ha="center", va="center", fontsize=9)
save(fig, "m09-loud-high.svg")

# 6. 실 전화기
fig, ax = canvas(10.0, 3.6, 16.0, 6.0)
kid(ax, 1.2, 0.8, 1.6)
kid(ax, 14.8, 0.8, 1.6)
ax.add_patch(Polygon([(2.0, 3.2), (2.0, 3.8), (2.8, 3.65), (2.8, 3.35)], closed=True, fc="white", ec=INK, lw=1.2))
ax.add_patch(Polygon([(14.0, 3.2), (14.0, 3.8), (13.2, 3.65), (13.2, 3.35)], closed=True, fc="white", ec=INK, lw=1.2))
ax.plot([2.8, 13.2], [3.5, 3.5], color=INK, lw=1.2)
for k in range(5):
    xx = 4.0 + k * 1.8
    wave(ax, xx, xx + 0.9, 4.0, 0.12, 2, color=RED)
arrow(ax, (4.0, 4.5), (12.0, 4.5), color=RED, lw=1.6)
ax.text(8.0, 2.6, "실이 떨림을 전해요", ha="center", va="center", fontsize=11, color=RED, fontweight="bold")
save(fig, "m09-phone.svg")

# 7. 귀가 떨림을 받아요
fig, ax = canvas(10.0, 4.0, 16.0, 6.6)
ax.add_patch(Polygon([(5.0, 1.0), (5.0, 5.6), (12.0, 5.6), (12.0, 1.0)], closed=True, fc=SKIN, ec="none"))
ax.add_patch(Rectangle((5.0, 2.8), 4.2, 1.0, fc="white", ec=INK, lw=1.2))
ax.plot([5.0, 5.0], [1.0, 2.8], color=INK, lw=1.2); ax.plot([5.0, 5.0], [3.8, 5.6], color=INK, lw=1.2)
for k in range(3):
    ax.add_patch(Arc((9.2, 3.3), 0.25 + k * 0.12, 1.0, theta1=-90, theta2=90, color=INK, lw=1.6, alpha=1.0 if k == 1 else 0.4))
ax.annotate("고막", (9.25, 3.8), (9.0, 6.2), fontsize=11, fontweight="bold", ha="center",
            arrowprops=dict(arrowstyle="-", color=INK, lw=1))
xs = chain(ax, 0.6, 3.3, 13, r=0.12, base=0.6, comp=0.18)
arrow(ax, (9.6, 3.3), (11.4, 3.3), color=RED, lw=2)
ax.text(12.4, 3.3, "뇌로", ha="left", va="center", fontsize=11, color=RED, fontweight="bold")
ax.text(2.6, 2.3, "귓구멍으로 들어오는\n촘촘한 곳과 듬성한 곳", ha="center", va="center", fontsize=9.5)
save(fig, "m09-ear.svg")
