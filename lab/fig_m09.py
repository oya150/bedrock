"""물질과 에너지 9편 그림 만들기. 실행: python lab/fig_m09.py  → docs/matter/img/09/*.svg
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

OUT = os.environ.get("FIG_OUT") or os.path.join(os.path.dirname(__file__), "..", "docs", "matter", "img", "09")
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
    if FMT != "svg":
        name = name.rsplit(".", 1)[0] + "." + FMT
    fig.savefig(os.path.join(OUT, name), bbox_inches="tight", pad_inches=0.25, dpi=110)
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




def openbox(ax, x, y, w=5.0, h=2.0):
    ax.add_patch(Rectangle((x, y), w, h, fc=BOXC, ec=INK, lw=1.4))
    ax.add_patch(Rectangle((x + 0.2, y + 0.2), w - 0.4, h - 0.4, fc="#c9b28c", ec="none"))


def rest_band(ax, x0, x1, y, color=INK):
    ax.plot([x0, x1], [y, y], color=color, lw=1.8)


def lchain(ax, x0, y, n, phase, d=0.5, a=0.17, q=2 * math.pi / 8, r=0.14, hot=None):
    """앞뒤로 밀렸다 돌아오는 알갱이 줄. k번째 알갱이는 제자리 x0+k*d 에서 a*sin(q*k-phase) 만큼 비켜 있다."""
    xs = [x0 + k * d + a * math.sin(q * k - phase) for k in range(n)]
    for k, xx in enumerate(xs):
        hit = hot is not None and k == hot
        ax.add_patch(Circle((xx, y), r * (1.15 if hit else 1), fc=RED if hit else WATER, ec=RED if hit else INK,
                            lw=0.6))
    return xs


# 1. 튕기면 떨리고 잡으면 멈춰요
fig, ax = canvas(11.0, 3.2, 18.0, 5.2)
for i, lab in enumerate(["튕기면", "잡으면"]):
    x = 0.4 + i * 9.0
    openbox(ax, x, 1.4)
    if i == 0:
        band(ax, x, x + 5.0, 2.4, 0.4, 3, color=RED)
        ax.add_patch(Ellipse((x + 3.4, 3.2), 0.55, 0.32, fc=SKIN, ec=INK, lw=1, angle=30))
        sound(ax, x + 5.4, 2.4, 3, 0.5, color=RED)
    else:
        rest_band(ax, x, x + 5.0, 2.4)
        ax.add_patch(Ellipse((x + 2.5, 2.62), 0.45, 0.32, fc=SKIN, ec=INK, lw=1))
        ax.add_patch(Ellipse((x + 2.5, 2.18), 0.45, 0.32, fc=SKIN, ec=INK, lw=1))
    ax.text(x + 2.5, 0.7, lab, ha="center", va="center", fontsize=12, fontweight="bold",
            color=RED if i == 0 else "#222")
save(fig, "m09-band.svg")

# 2. 소리가 나는 것은 모두 떨려요
fig, ax = canvas(11.0, 3.2, 18.0, 5.4)
for i, lab in enumerate(["고무줄", "북", "목"]):
    x = 0.3 + i * 6.0
    box(ax, x, 0.5, 5.4, 4.6, fc=NOTE)
    cx = x + 2.7
    if i == 0:
        band(ax, cx - 1.8, cx + 1.8, 3.0, 0.4, 3, color=RED)
    elif i == 1:
        ax.add_patch(Rectangle((cx - 1.4, 1.6), 2.8, 1.4, fc="#e9a96b", ec=INK, lw=1.2))
        for a in (0.25, 0, -0.25):
            ax.add_patch(Arc((cx, 3.0), 2.8, 2 * abs(a) + 0.05, theta1=0 if a >= 0 else 180,
                             theta2=180 if a >= 0 else 360, color=RED, lw=1.4, alpha=1.0 if a == 0 else 0.45))
    else:
        kid(ax, cx, 1.3, 1.5)
        ax.add_patch(Ellipse((cx + 0.55, 2.9), 0.45, 0.28, fc=SKIN, ec=INK, lw=1))
        for k in range(3):
            ax.plot([cx - 0.15 + k * 0.15, cx - 0.15 + k * 0.15], [2.75, 3.05], color=RED, lw=1.2)
        ax.text(cx + 1.3, 4.1, "아—", ha="center", va="center", fontsize=11)
    ax.text(cx, 1.0, lab, ha="center", va="center", fontsize=11, fontweight="bold")
save(fig, "m09-shake.svg")

# 3. 촘촘한 곳은 앞으로 가고 알갱이는 제자리 근처에 있어요 (세 줄 띠)
fig, ax = canvas(11.0, 5.0, 18.0, 8.2)
N, X0, D, A, L, HOT = 28, 2.4, 0.5, 0.3, 12, 13
Q = 2 * math.pi / L
rows = [("처음", 6.6, 0), ("조금 뒤", 4.1, 1), ("더 뒤", 1.6, 2)]
ax.plot([X0 + HOT * D] * 2, [0.7, 7.5], color=GREY, lw=1.2, ls=(0, (4, 3)))
for lab, y, step in rows:
    ph = step * math.pi / 2
    ax.text(0.2, y, lab, ha="left", va="center", fontsize=10.5, fontweight="bold")
    bx = X0 - D + A * math.sin(-Q - ph)
    ax.plot([bx, bx], [y - 0.7, y + 0.7], color=BAND, lw=2.4)
    xs = lchain(ax, X0, y, N, ph, d=D, a=A, q=Q, hot=HOT)
    k = round((math.pi + ph) / Q)
    ax.plot([xs[k - 2], xs[k - 2], xs[k + 2], xs[k + 2]], [y + 0.32, y + 0.45, y + 0.45, y + 0.32], color=RED, lw=1.6)
    ax.text((xs[k - 2] + xs[k + 2]) / 2, y + 0.75, "촘촘", ha="center", va="center", fontsize=9.5, color=RED,
            fontweight="bold")
    j = round(ph / Q) + L
    ax.text(xs[j], y - 0.55, "듬성", ha="center", va="center", fontsize=9, color=INK)
ax.text(1.9, 7.75, "고무줄", ha="center", va="center", fontsize=9)
ax.text(X0 + HOT * D, 0.35, "빨간 알갱이 제자리", ha="center", va="center", fontsize=9, color=INK)
arrow(ax, (16.6, 4.1), (17.7, 4.1), color=INK, lw=1.6)
ax.text(17.2, 4.6, "귀 쪽", ha="center", va="center", fontsize=9.5)
save(fig, "m09-push.svg")

# 4. 귀가 떨림을 받아요
fig, ax = canvas(10.0, 3.6, 16.0, 6.2)
ax.add_patch(Polygon([(5.0, 1.0), (5.0, 5.6), (12.0, 5.6), (12.0, 1.0)], closed=True, fc=SKIN, ec="none"))
ax.add_patch(Rectangle((5.0, 2.8), 4.2, 1.0, fc="white", ec=INK, lw=1.2))
ax.plot([5.0, 5.0], [1.0, 2.8], color=INK, lw=1.2); ax.plot([5.0, 5.0], [3.8, 5.6], color=INK, lw=1.2)
for k in range(3):
    ax.add_patch(Arc((9.2, 3.3), 0.25 + k * 0.12, 1.0, theta1=-90, theta2=90, color=RED, lw=1.8,
                     alpha=1.0 if k == 1 else 0.4))
ax.annotate("고막", (9.25, 3.8), (9.4, 6.0), fontsize=11, fontweight="bold", ha="center", color=RED,
            arrowprops=dict(arrowstyle="-", color=RED, lw=1))
chain(ax, 0.6, 3.3, 13, r=0.12, base=0.6, comp=0.18)
ax.text(7.1, 2.3, "귓구멍", ha="center", va="center", fontsize=10)
arrow(ax, (9.6, 3.3), (11.4, 3.3), color=INK, lw=2)
ax.text(12.4, 3.3, "뇌", ha="left", va="center", fontsize=11, fontweight="bold")
save(fig, "m09-ear.svg")

# 5. 크고 작게, 높고 낮게
fig, ax = canvas(11.0, 4.2, 18.0, 7.0)
for (x0, y, amp, cyc, lab, hot) in [
        (3.0, 5.2, 0.8, 2, "큰 소리", True), (10.4, 5.2, 0.3, 2, "작은 소리", False),
        (3.0, 1.9, 0.5, 7, "높은 소리", True), (10.4, 1.9, 0.5, 2, "낮은 소리", False)]:
    ax.plot([x0, x0 + 5.4], [y, y], color=GREY, lw=0.8, ls=(0, (3, 3)))
    wave(ax, x0, x0 + 5.4, y, amp, cyc, color=RED if hot else INK)
    ax.text(x0 + 2.7, y - 1.25, lab, ha="center", va="center", fontsize=11, fontweight="bold",
            color=RED if hot else "#222")
ax.text(0.2, 5.2, "떨림\n크기", ha="left", va="center", fontsize=10)
ax.text(0.2, 1.9, "떨림\n빠르기", ha="left", va="center", fontsize=10)
save(fig, "m09-loud-high.svg")

# 6. 실 전화기: 팽팽하면 건너가고 느슨하면 못 가요
fig, ax = canvas(10.0, 4.2, 16.0, 7.0)


def phone_cup(ax, x, y, left=True):
    if left:
        ax.add_patch(Polygon([(x, y - 0.4), (x, y + 0.4), (x + 0.9, y + 0.25), (x + 0.9, y - 0.25)], closed=True,
                             fc="white", ec=INK, lw=1.3))
    else:
        ax.add_patch(Polygon([(x, y - 0.4), (x, y + 0.4), (x - 0.9, y + 0.25), (x - 0.9, y - 0.25)], closed=True,
                             fc="white", ec=INK, lw=1.3))


for lab, y, tight in [("팽팽", 5.0, True), ("느슨", 1.8, False)]:
    ax.text(0.2, y, lab, ha="left", va="center", fontsize=11, fontweight="bold", color=RED if tight else "#222")
    phone_cup(ax, 1.8, y, True)
    phone_cup(ax, 14.2, y, False)
    ax.text(1.4, y + 0.75, "아", ha="center", va="center", fontsize=10)
    if tight:
        ax.plot([2.7, 13.3], [y, y], color=INK, lw=1.2)
        for k in range(5):
            xx = 3.6 + k * 1.9
            wave(ax, xx, xx + 0.9, y + 0.35, 0.12, 2, color=RED)
        sound(ax, 14.4, y, 2, 0.4, color=RED)
        ear(ax, 15.4, y, 0.8)
    else:
        xs = [2.7 + 10.6 * t / 60 for t in range(61)]
        ax.plot(xs, [y - 1.1 * math.sin(math.pi * t / 60) for t in range(61)], color=INK, lw=1.2)
        wave(ax, 3.0, 3.9, y + 0.1, 0.12, 2, color=RED)
        ear(ax, 15.4, y, 0.8)
save(fig, "m09-phone.svg")

# 7. 밀어 줄 알갱이가 없으면 전해지지 않아요
fig, ax = canvas(11.0, 3.4, 18.0, 5.6)
for i, lab in enumerate(["공기 있음", "공기 없음"]):
    x = 0.3 + i * 9.0
    box(ax, x, 0.4, 8.4, 4.8, fc=NOTE if i == 0 else "white")
    ax.plot([x + 0.8, x + 0.8], [1.8, 4.0], color=RED, lw=2.4)
    ax.plot([x + 0.6, x + 0.6], [1.8, 4.0], color=RED, lw=1.4, alpha=0.4)
    ax.plot([x + 1.0, x + 1.0], [1.8, 4.0], color=RED, lw=1.4, alpha=0.4)
    if i == 0:
        for yy in (2.2, 2.9, 3.6):
            chain(ax, x + 1.5, yy, 11, r=0.11, base=0.42, comp=0.13)
        sound(ax, x + 6.3, 2.9, 2, 0.35, color=INK)
    ear(ax, x + 7.5, 2.9, 1.0)
    ax.text(x + 4.2, 0.95, lab, ha="center", va="center", fontsize=11, fontweight="bold")
save(fig, "m09-empty.svg")
