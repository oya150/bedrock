"""물질과 에너지 10편 그림 만들기. 실행: python lab/fig_m10.py  → docs/matter/img/10/*.svg
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

OUT = os.environ.get("FIG_OUT") or os.path.join(os.path.dirname(__file__), "..", "docs", "matter", "img", "10")
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


LIGHT_C = "#e8b923"
RAINBOW = ["#e4572e", "#f28c28", "#f2c12e", "#5aa469", "#3b7dd8", "#7b4fb3"]


def ray(ax, a, b, color=LIGHT_C, lw=2.2, head=True):
    if head:
        ax.add_patch(FancyArrowPatch(a, b, arrowstyle="-|>", mutation_scale=14, color=color, lw=lw))
    else:
        ax.plot([a[0], b[0]], [a[1], b[1]], color=color, lw=lw)


def torch(ax, x, y, ang=0, s=1.0):
    c, sn = math.cos(math.radians(ang)), math.sin(math.radians(ang))
    pts = [(-1.0, -0.25), (0.0, -0.25), (0.35, -0.45), (0.35, 0.45), (0.0, 0.25), (-1.0, 0.25)]
    ax.add_patch(Polygon([(x + s * (px * c - py * sn), y + s * (px * sn + py * c)) for px, py in pts], closed=True,
                         fc=GREY, ec=INK, lw=1.2))


def eye(ax, x, y, s=1.0, facing=-1):
    ax.add_patch(Ellipse((x, y), 0.9 * s, 0.5 * s, fc="white", ec=INK, lw=1.2))
    ax.add_patch(Circle((x + facing * 0.15 * s, y), 0.15 * s, fc=INK))


def apple(ax, x, y, r=0.45):
    ax.add_patch(Circle((x, y), r, fc="#d9463a", ec=INK, lw=1.2))
    ax.plot([x, x + 0.05], [y + r, y + r + 0.25], color=INK, lw=1.5)


STICK = "#b5835a"


def stick(ax, a, b, alpha=1.0):
    ax.plot([a[0], b[0]], [a[1], b[1]], color=STICK, lw=5, solid_capstyle="round", alpha=alpha)


# 1. 컵 속 젓가락은 꺾여 보이고 꺼내면 곧아요
fig, ax = canvas(9.0, 3.9, 15.0, 6.6)
cup(ax, 2.0, 0.6, 3.6, 4.4, fc="white")
ax.add_patch(Polygon([(2.18, 2.8), (5.42, 2.8), (5.3, 0.65), (2.3, 0.65)], closed=True, fc="#cfe3f3", ec="none"))
stick(ax, (1.6, 5.6), (3.3, 2.8))
stick(ax, (3.3, 2.8), (4.9, 1.5))
ax.plot([2.1, 5.5], [2.8, 2.8], color=WATER, lw=1.2)
ax.add_patch(Circle((3.3, 2.8), 0.45, fc="none", ec=RED, lw=2))
stick(ax, (8.6, 1.0), (12.4, 5.0))
ax.text(3.8, 0.05, "물컵 속", ha="center", va="center", fontsize=11, fontweight="bold")
ax.text(10.5, 0.05, "꺼낸 젓가락", ha="center", va="center", fontsize=11, fontweight="bold")
save(fig, "m10-chopstick.svg")


# 2. 그림자: 머리 꼭대기를 스친 빛이 닿는 곳까지가 그림자
def shadow_row(ax, y0, src, hot):
    ax.plot([0.5, 15.5], [y0, y0], color=INK, lw=1.2)
    kx, kh = 6.0, 2.15
    kid(ax, kx, y0, 1.15)
    top = (kx, y0 + kh)
    t = (src[1] - y0) / (src[1] - top[1])
    end = (src[0] + (top[0] - src[0]) * t, y0)
    ax.add_patch(Rectangle((kx, y0 - 0.08), end[0] - kx, 0.22, fc="#444", ec="none", alpha=0.75))
    ax.add_patch(Circle(src, 0.32, fc=YEL, ec=INK, lw=1.2))
    ray(ax, src, end, color=RED if hot else LIGHT_C, lw=1.6, head=False)
    for dy in (-1.4, -0.9):
        ray(ax, src, (kx - 0.35, y0 + kh + dy), lw=1.4)
    ax.text((kx + end[0]) / 2, y0 - 0.45, "그림자", ha="center", va="center", fontsize=10,
            color=RED if hot else "#222", fontweight="bold" if hot else "normal")


fig, ax = canvas(10.0, 6.0, 16.0, 9.8)
ax.text(0.5, 9.4, "높이", ha="left", va="center", fontsize=11, fontweight="bold")
shadow_row(ax, 5.8, (5.0, 9.4), False)
ax.text(0.5, 4.4, "낮게", ha="left", va="center", fontsize=11, fontweight="bold", color=RED)
shadow_row(ax, 0.8, (1.8, 4.4), True)
save(fig, "m10-shadow.svg")

# 3. 튕겨요: 거울과 사과
fig, ax = canvas(11.0, 3.8, 18.0, 6.2)
box(ax, 0.3, 0.4, 8.2, 5.0, fc=NOTE)
ax.add_patch(Rectangle((2.0, 1.0), 5.0, 0.35, fc="#dde6ee", ec=INK, lw=1))
ax.plot([2.0, 7.0], [1.35, 1.35], color=INK, lw=3)
torch(ax, 1.6, 4.6, ang=-45, s=0.9)
ray(ax, (2.0, 4.2), (4.5, 1.4), head=False)
ray(ax, (4.5, 1.4), (7.2, 4.4), color=RED)
ax.text(4.5, 0.75, "거울", ha="center", va="center", fontsize=11, fontweight="bold")
box(ax, 9.3, 0.4, 8.4, 5.0, fc=NOTE)
ax.add_patch(Circle((10.6, 4.4), 0.4, fc=YEL, ec=INK, lw=1))
apple(ax, 12.6, 1.8)
ray(ax, (10.9, 4.1), (12.4, 2.3))
ray(ax, (13.0, 2.1), (15.8, 3.6), color=RED)
for (dx, dy) in [(-1.6, 0.9), (-1.0, 1.6), (0.9, -0.6), (1.4, 0.3), (0.2, 1.8)]:
    ray(ax, (12.6 + dx * 0.3, 1.8 + dy * 0.3), (12.6 + dx, 1.8 + dy), color=RED, lw=1.0)
eye(ax, 16.4, 3.9, 1.0, facing=-1)
ax.text(12.6, 0.75, "사과", ha="center", va="center", fontsize=11, fontweight="bold")
save(fig, "m10-bounce.svg")

# 4. 손잡은 두 친구가 땅에서 모래밭으로 비스듬히 들어가요
fig, ax = canvas(10.0, 5.6, 16.0, 9.0)
Y = 4.0
ax.add_patch(Rectangle((0.3, 0.3), 15.4, Y - 0.3, fc="#efe0bf", ec="none"))
ax.plot([0.3, 15.7], [Y, Y], color=INK, lw=1.2)
ax.text(15.4, 8.4, "땅", ha="right", va="center", fontsize=11, fontweight="bold")
ax.text(15.4, 0.8, "모래밭", ha="right", va="center", fontsize=11, fontweight="bold")
th1 = math.radians(50)
th2 = math.asin(0.55 * math.sin(th1))
d1 = (math.sin(th1), -math.cos(th1))
d2 = (math.sin(th2), -math.cos(th2))
perp = (math.cos(th1), math.sin(th1))
start = (3.0, 7.6)
H = 0.8
ends = [(start[0] - perp[0] * H, start[1] - perp[1] * H), (start[0] + perp[0] * H, start[1] + perp[1] * H)]


def where(p0, t):
    tc = (p0[1] - Y) / -d1[1]
    if t <= tc:
        return (p0[0] + d1[0] * t, p0[1] + d1[1] * t)
    q = (p0[0] + d1[0] * tc, Y)
    r = (t - tc) * 0.55
    return (q[0] + d2[0] * r, q[1] + d2[1] * r)


T = [0, 1.6, 3.2, 4.2, 5.2, 6.2, 8.2]
for t in T:
    a, b = where(ends[0], t), where(ends[1], t)
    mixed = (a[1] < Y) != (b[1] < Y)
    col = RED if mixed else INK
    ax.plot([a[0], b[0]], [a[1], b[1]], color=col, lw=2.2 if mixed else 1.6)
    for p in (a, b):
        ax.add_patch(Circle(p, 0.17, fc=RED if mixed else WATER, ec=INK, lw=0.8))
for p0 in ends:
    pts = [where(p0, t / 10) for t in range(0, 83)]
    ax.plot([p[0] for p in pts], [p[1] for p in pts], color=GREY, lw=1, ls=(0, (3, 3)))
save(fig, "m10-sand.svg")

# 5. 꺾여요: 물속 젓가락 끝이 떠 보여요
fig, ax = canvas(8.0, 5.0, 12.0, 8.0)
ax.add_patch(Rectangle((0.6, 0.6), 7.6, 3.4, fc="#cfe3f3", ec="none"))
ax.plot([0.6, 8.2], [4.0, 4.0], color=WATER, lw=1.4)
stick(ax, (2.4, 7.4), (3.7, 4.0))
stick(ax, (3.7, 4.0), (4.8, 1.2), alpha=0.9)
tip, A = (4.8, 1.2), (5.0, 2.5)
for P in [(5.6, 4.0), (6.2, 4.0)]:
    ray(ax, tip, P, head=False)
    d = (P[0] - A[0], P[1] - A[1])
    ray(ax, P, (P[0] + d[0] * 1.3, P[1] + d[1] * 1.3))
    ax.plot([P[0], A[0]], [P[1], A[1]], color=RED, lw=1.3, ls="--")
ax.add_patch(Ellipse((7.1, 6.6), 1.8, 0.7, fc="white", ec=INK, lw=1.2))
ax.add_patch(Circle((6.9, 6.5), 0.2, fc=INK))
ax.add_patch(Circle(A, 0.14, fc="none", ec=RED, lw=1.8))
ax.annotate("보이는 끝", A, (1.2, 2.6), fontsize=10.5, color=RED, fontweight="bold",
            arrowprops=dict(arrowstyle="-", color=RED, lw=1))
ax.annotate("실제 끝", tip, (1.2, 1.2), fontsize=10.5, arrowprops=dict(arrowstyle="-", color=INK, lw=1))
ax.text(9.0, 4.0, "물 표면", ha="left", va="center", fontsize=10)
save(fig, "m10-bend.svg")

# 6. 무지개: 빗방울 속에서 색이 나뉘어요
fig, ax = canvas(10.0, 4.6, 16.0, 7.4)
cx, cy, R = 9.0, 4.2, 2.0
ax.add_patch(Circle((cx, cy), R, fc="#e6f0f8", ec=INK, lw=1.4))
entry = (cx - R * math.cos(math.radians(30)), cy + R * math.sin(math.radians(30)))
back = (cx + R * 0.95, cy - R * 0.3)
ray(ax, (1.0, entry[1]), entry, color="#888", lw=3, head=False)
ax.text(1.6, entry[1] + 0.4, "햇빛", ha="center", va="center", fontsize=10.5, fontweight="bold")
ray(ax, entry, back, color="#888", lw=2, head=False)
ends = []
for k, c in enumerate(RAINBOW):
    ex = (cx - R * math.cos(math.radians(-35 - k * 3)), cy + R * math.sin(math.radians(-35 - k * 3)))
    ray(ax, back, ex, color=c, lw=1.1, head=False)
    ang = math.radians(200 + k * 3.2)
    end = (ex[0] + 4.2 * math.cos(ang), ex[1] + 4.2 * math.sin(ang))
    ray(ax, ex, end, color=c, lw=1.5)
    ends.append(end)
ax.text(ends[0][0] - 0.3, ends[0][1] + 0.1, "빨강", ha="right", va="center", fontsize=10, color=RAINBOW[0],
        fontweight="bold")
ax.text(ends[-1][0] - 0.3, ends[-1][1] - 0.1, "보라", ha="right", va="center", fontsize=10, color=RAINBOW[-1],
        fontweight="bold")
ax.text(cx, cy + R + 0.4, "빗방울", ha="center", va="center", fontsize=10.5, fontweight="bold")
save(fig, "m10-rainbow.svg")

# 7. 사과 색
fig, ax = canvas(9.0, 3.4, 15.0, 5.6)
ax.add_patch(Circle((1.6, 4.4), 0.45, fc=YEL, ec=INK, lw=1))
apple(ax, 7.0, 2.2, 0.8)
for k, c in enumerate([RED, "#5aa469", "#3b7dd8"]):
    ray(ax, (2.1, 4.3 - k * 0.25), (6.3, 2.6 - k * 0.2 + 0.3), color=c, lw=1.6, head=(c != RED))
ray(ax, (7.6, 2.8), (11.6, 4.6), color=RED, lw=1.8)
ax.add_patch(Ellipse((12.4, 4.9), 1.2, 0.55, fc="white", ec=INK, lw=1.2))
ax.add_patch(Circle((12.2, 4.85), 0.17, fc=INK))
ax.text(1.6, 3.6, "전등", ha="center", va="center", fontsize=10)
ax.text(7.0, 0.9, "사과", ha="center", va="center", fontsize=11, fontweight="bold")
ax.text(9.9, 4.4, "빨강", ha="center", va="center", fontsize=10, color=RED, fontweight="bold")
ax.text(4.0, 2.2, "초록, 파랑", ha="center", va="center", fontsize=10)
save(fig, "m10-apple.svg")
