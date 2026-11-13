"""물질과 에너지 11편 그림 만들기. 실행: python lab/fig_m11.py  → docs/matter/img/11/*.svg
확인용 PNG: FIG_FMT=png FIG_OUT=<폴더> python lab/fig_m11.py

글자는 SVG 안에 글자로 남긴다(글꼴 모양을 파일에 넣지 않는다). 보는 쪽 글꼴로 그려진다.
그림 안 글씨는 낱말과 숫자만 둔다. 강조(지금 볼 곳)만 빨강으로 칠한다.
"""
import math
import os
import random

import matplotlib

matplotlib.use("svg" if os.environ.get("FIG_FMT", "svg") == "svg" else "agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Ellipse, FancyArrowPatch, FancyBboxPatch, Polygon, Rectangle

OUT = os.environ.get("FIG_OUT") or os.path.join(os.path.dirname(__file__), "..", "docs", "matter", "img", "11")
FMT = os.environ.get("FIG_FMT", "svg")
os.makedirs(OUT, exist_ok=True)

plt.rcParams.update({
    "font.family": ["Apple SD Gothic Neo", "Noto Sans KR", "Malgun Gothic", "sans-serif"],
    "svg.fonttype": "none",
    "text.color": "#222",
    "figure.facecolor": "white",
    "savefig.facecolor": "white",
})

RED, GREY, INK, YEL = "#e4572e", "#c9ccd1", "#555", "#f6c445"
ELEC = "#3b7dd8"
COPPER = "#d08a4a"
WIRE = "#9aa3ad"
WATER = "#cfe3f3"

random.seed(2)


def save(fig, name):
    name = name.rsplit(".", 1)[0] + "." + FMT
    fig.savefig(os.path.join(OUT, name), bbox_inches="tight", pad_inches=0.25, dpi=110)
    plt.close(fig)


def canvas(w, h, xmax, ymax):
    fig, ax = plt.subplots(figsize=(w, h))
    ax.set_xlim(0, xmax); ax.set_ylim(0, ymax); ax.set_aspect("equal"); ax.axis("off")
    return fig, ax


def arrow(ax, a, b, color=INK, lw=2, ms=18, z=6):
    ax.add_patch(FancyArrowPatch(a, b, arrowstyle="-|>", mutation_scale=ms, color=color, lw=lw, zorder=z))


def label(ax, x, y, s, fs=11, color="#222", bold=False, ha="center"):
    ax.text(x, y, s, ha=ha, va="center", fontsize=fs, color=color, fontweight="bold" if bold else "normal", zorder=8)


def battery(ax, x, y, w=2.4, h=1.0):
    """왼쪽이 − 쪽, 오른쪽이 + 쪽."""
    ax.add_patch(Rectangle((x, y), w, h, fc="#4a4a4a", ec=INK, lw=1.2, zorder=4))
    ax.add_patch(Rectangle((x + w * 0.7, y), w * 0.3, h, fc="#f2c12e", ec=INK, lw=1.2, zorder=4))
    ax.add_patch(Rectangle((x + w, y + h * 0.3), 0.15, h * 0.4, fc=GREY, ec=INK, lw=1, zorder=4))
    ax.text(x + w * 0.85, y + h / 2, "+", ha="center", va="center", fontsize=13, fontweight="bold", zorder=5)
    ax.text(x + w * 0.25, y + h / 2, "−", ha="center", va="center", fontsize=13, color="white", fontweight="bold",
            zorder=5)


def bulb(ax, x, y, on=True, s=1.0):
    """(x, y)는 받침 아래 가운데."""
    ax.add_patch(Circle((x, y + 0.75 * s), 0.55 * s, fc=YEL if on else "#f4f4f4", ec=INK, lw=1.2, zorder=4))
    ax.add_patch(Rectangle((x - 0.3 * s, y), 0.6 * s, 0.3 * s, fc=GREY, ec=INK, lw=1, zorder=4))
    xs = [x - 0.2 * s + 0.4 * s * t / 20 for t in range(21)]
    ys = [y + 0.75 * s + 0.08 * s * math.sin(t * 1.5) for t in range(21)]
    ax.plot(xs, ys, color=INK, lw=0.8, zorder=5)
    if on:
        for a in range(30, 151, 30):
            t = math.radians(a)
            ax.plot([x + 0.7 * s * math.cos(t), x + 0.95 * s * math.cos(t)],
                    [y + 0.75 * s + 0.7 * s * math.sin(t), y + 0.75 * s + 0.95 * s * math.sin(t)], color=INK, lw=1)


def wire(ax, pts, color=WIRE, lw=3, z=2):
    ax.plot([p[0] for p in pts], [p[1] for p in pts], color=color, lw=lw, solid_joinstyle="round",
            solid_capstyle="round", zorder=z)


def seglen(pts):
    return sum(math.dist(a, b) for a, b in zip(pts[:-1], pts[1:]))


def dots_on(ax, pts, n, r=0.13):
    """꺾은선 pts 위에 고르게 n개의 전자."""
    segs = list(zip(pts[:-1], pts[1:]))
    lens = [math.dist(a, b) for a, b in segs]
    total = sum(lens)
    for k in range(n):
        d = (k + 0.5) / n * total
        for (a, b), L in zip(segs, lens):
            if d <= L:
                p = (a[0] + (b[0] - a[0]) * d / L, a[1] + (b[1] - a[1]) * d / L)
                break
            d -= L
        ax.add_patch(Circle(p, r, fc=ELEC, ec="none", zorder=5))


def circuit(ax, ox, oy, on=True, gap=None, arrows=True, w=8.0, h=4.0):
    """건전지는 아래 가운데, 전구는 위 가운데. gap='right'면 오른쪽 변이 끊긴다."""
    bx, by = ox + w / 2 - 1.2, oy - 0.5
    cx = ox + w / 2
    left = [(bx, oy), (ox, oy), (ox, oy + h), (cx - 0.35, oy + h)]
    if gap == "right":
        segs = [left, [(cx + 0.35, oy + h), (ox + w, oy + h), (ox + w, oy + h * 0.62)],
                [(ox + w + 0.5, oy + h * 0.42), (ox + w, oy + h * 0.32), (ox + w, oy), (bx + 2.55, oy)]]
    else:
        segs = [left, [(cx + 0.35, oy + h), (ox + w, oy + h), (ox + w, oy), (bx + 2.55, oy)]]
    for seg in segs:
        wire(ax, seg)
        dots_on(ax, seg, max(3, int(seglen(seg) / 0.75)))
    battery(ax, bx, by)
    bulb(ax, cx, oy + h - 0.4, on, 0.9)
    if arrows:
        arrow(ax, (ox - 0.6, oy + h * 0.3), (ox - 0.6, oy + h * 0.7), color=RED, lw=2.4)
        arrow(ax, (ox + w * 0.68, oy + h + 0.6), (ox + w * 0.92, oy + h + 0.6), color=RED, lw=2.4)
        arrow(ax, (ox + w + 0.6, oy + h * 0.7), (ox + w + 0.6, oy + h * 0.3), color=RED, lw=2.4)
        arrow(ax, (ox + w * 0.92, oy - 0.6), (ox + w * 0.7, oy - 0.6), color=RED, lw=2.4)
    return bx, by


# 1. 여는 장면: 켜짐과 꺼짐
fig, ax = canvas(10.0, 3.8, 17.0, 6.2)
for x0, on in [(1.0, True), (9.6, False)]:
    w, h = 5.4, 3.4
    bx = x0 + w / 2 - 1.2
    wire(ax, [(bx, 1.3), (x0, 1.3), (x0, 1.3 + h), (x0 + w / 2 - 0.3, 1.3 + h)])
    if on:
        wire(ax, [(x0 + w / 2 + 0.3, 1.3 + h), (x0 + w, 1.3 + h), (x0 + w, 1.3), (bx + 2.55, 1.3)])
    else:
        wire(ax, [(x0 + w / 2 + 0.3, 1.3 + h), (x0 + w, 1.3 + h), (x0 + w, 2.3), (x0 + w + 0.6, 1.9)])
        ax.add_patch(Circle((x0 + w + 0.4, 1.6), 0.7, fc="none", ec=RED, lw=2.2, zorder=6))
    battery(ax, bx, 0.8)
    bulb(ax, x0 + w / 2, 1.3 + h - 0.4, on, 0.9)
    label(ax, x0 + w / 2, 0.2, "켜짐" if on else "꺼짐", fs=12, bold=True)
save(fig, "m11-bulb.svg")

# 2. 원자 속 전자 / 구리 선 속
fig, ax = canvas(10.0, 4.2, 16.4, 6.9)
ax.add_patch(Circle((3.0, 3.8), 2.0, fc="white", ec=INK, lw=1.4))
ax.add_patch(Circle((3.0, 3.8), 0.35, fc=GREY, ec=INK, lw=1))
for a in range(0, 360, 45):
    t = math.radians(a)
    ax.add_patch(Circle((3.0 + 1.4 * math.cos(t), 3.8 + 1.4 * math.sin(t)), 0.11, fc=ELEC, ec="none"))
label(ax, 3.0, 1.2, "원자 하나", fs=12, bold=True)
ax.annotate("전자", (3.0 + 1.4 * math.cos(math.radians(45)), 3.8 + 1.4 * math.sin(math.radians(45))),
            (4.6, 6.4), fontsize=10.5, ha="left", va="center", arrowprops=dict(arrowstyle="-", color=INK, lw=1))
ax.add_patch(FancyBboxPatch((7.4, 2.0), 8.2, 3.6, boxstyle="round,pad=0.1", fc="#f7ebdf", ec=COPPER, lw=2))
for i in range(4):
    for j in range(9):
        ax.add_patch(Circle((8.0 + j * 0.88, 2.5 + i * 0.88), 0.28, fc=COPPER, ec=INK, lw=0.6))
for k in range(16):
    x = 8.44 + random.randrange(8) * 0.88
    y = 2.94 + random.randrange(3) * 0.88
    ax.add_patch(Circle((x, y), 0.12, fc=ELEC, ec="none", zorder=5))
    a = random.uniform(0, 2 * math.pi)
    arrow(ax, (x, y), (x + 0.42 * math.cos(a), y + 0.42 * math.sin(a)), color=RED, lw=1.1, ms=8)
label(ax, 11.5, 1.2, "구리 선 속", fs=12, bold=True)
save(fig, "m11-electron.svg")

# 3. 한 바퀴 이어진 길
fig, ax = canvas(9.0, 5.0, 12.6, 7.0)
bx, by = circuit(ax, 2.2, 1.4, on=True)
label(ax, bx + 0.3, by - 0.45, "− 쪽", fs=10.5, bold=True)
label(ax, bx + 2.1, by - 0.45, "+ 쪽", fs=10.5, bold=True)
label(ax, 6.2, 6.7, "꼬마전구", fs=10.5)
label(ax, 1.0, 3.4, "전선", fs=10.5)
label(ax, 6.2, 2.4, "건전지", fs=10.5)
save(fig, "m11-loop.svg")

# 4. 펌프 물길과 회로
fig, ax = canvas(10.4, 4.4, 17.6, 7.4)
ox, oy, w, h = 1.0, 1.6, 6.4, 4.0
ax.add_patch(Rectangle((ox, oy), w, h, fc=WATER, ec=INK, lw=1.4, zorder=1))
ax.add_patch(Rectangle((ox + 0.5, oy + 0.5), w - 1.0, h - 1.0, fc="white", ec=INK, lw=1.4, zorder=2))
ax.add_patch(Circle((ox + w / 2, oy + 0.25), 0.7, fc="#8aa0b4", ec=INK, lw=1.3, zorder=4))
fx, fy = ox + w / 2, oy + h - 0.25
for a in (20, 140, 260):
    t = math.radians(a)
    ax.add_patch(Polygon([(fx, fy), (fx + 0.7 * math.cos(t), fy + 0.7 * math.sin(t)),
                          (fx + 0.7 * math.cos(t + 0.6), fy + 0.7 * math.sin(t + 0.6))], closed=True,
                         fc="#e9eef3", ec=INK, lw=1.1, zorder=5))
ax.add_patch(Circle((fx, fy), 0.09, fc=INK, zorder=6))
arrow(ax, (ox - 0.5, oy + h * 0.3), (ox - 0.5, oy + h * 0.7), color=RED, lw=2.2)
arrow(ax, (ox + w + 0.5, oy + h * 0.7), (ox + w + 0.5, oy + h * 0.3), color=RED, lw=2.2)
label(ax, ox + w / 2, oy - 1.0, "펌프", fs=11, bold=True)
label(ax, ox + w / 2, oy + h + 1.0, "바람개비", fs=11, bold=True)
label(ax, ox + 1.4, oy + h / 2, "관", fs=11, bold=True)
circuit(ax, 10.2, 1.6, on=True, w=6.4, h=4.0)
label(ax, 13.4, oy - 1.3, "건전지", fs=11, bold=True)
label(ax, 13.4, oy + h + 1.75, "꼬마전구", fs=11, bold=True)
label(ax, 11.6, oy + h / 2, "전선", fs=11, bold=True)
save(fig, "m11-pump.svg")

# 5. 한 곳이 끊긴 회로
fig, ax = canvas(9.0, 5.0, 12.6, 7.0)
circuit(ax, 2.2, 1.4, on=False, gap="right", arrows=False)
ax.add_patch(Circle((10.45, 3.1), 0.8, fc="none", ec=RED, lw=2.4, zorder=7))
label(ax, 11.9, 3.1, "끊김", fs=12, color=RED, bold=True, ha="left")
label(ax, 6.2, 6.7, "꺼짐", fs=11, bold=True)
save(fig, "m11-break.svg")

# 6. 전구 속 가는 선
fig, ax = canvas(10.0, 4.6, 16.0, 7.4)
bulb(ax, 3.5, 1.0, True, 3.0)
ax.plot([3.9, 9.4], [3.25, 3.9], color=RED, lw=1.2, ls="--")
ax.add_patch(Circle((3.9, 3.25), 0.35, fc="none", ec=RED, lw=2, zorder=7))
ax.add_patch(Circle((11.6, 4.0), 2.3, fc="#fff3d6", ec=RED, lw=2))
for i in range(3):
    for j in range(4):
        ax.add_patch(Circle((10.4 + j * 0.8, 3.2 + i * 0.8), 0.25, fc=GREY, ec=INK, lw=0.6))
for (x, y) in [(10.0, 4.4), (11.2, 3.6), (12.0, 4.4), (12.8, 3.6)]:
    ax.add_patch(Circle((x, y), 0.11, fc=ELEC, ec="none", zorder=6))
    arrow(ax, (x - 0.55, y + 0.05), (x - 0.13, y), color=ELEC, lw=1.3, ms=8)
    for a in (40, 100, 160):
        t = math.radians(a)
        ax.plot([x + 0.18 * math.cos(t), x + 0.32 * math.cos(t)], [y + 0.18 * math.sin(t), y + 0.32 * math.sin(t)],
                color=RED, lw=1.2, zorder=7)
ax.annotate("원자", (10.4, 4.8), (9.0, 6.7), fontsize=10.5, arrowprops=dict(arrowstyle="-", color=INK, lw=1))
ax.annotate("전자", (12.0, 4.4), (12.6, 6.7), fontsize=10.5, arrowprops=dict(arrowstyle="-", color=INK, lw=1))
label(ax, 3.5, 0.4, "가는 선", fs=11, bold=True)
save(fig, "m11-glow.svg")

# 7. 굵은 전선과 가는 선: 원자 배치는 같고 전자 수도 같다. 가는 선은 부딪힘이 몰린다.
fig, ax = canvas(10.0, 4.6, 16.0, 7.4)
GAP = 0.9  # 원자 간격(가로세로 같음, 두 선 모두 같음)
NCOL = 12


def channel(y0, rows, hits, x0=3.2):
    """hits: (줄, 칸) 목록. 그 칸 원자 바로 왼쪽에서 전자가 부딪힌다."""
    x1 = x0 + NCOL * GAP
    ax.add_patch(Rectangle((x0, y0), x1 - x0, rows * GAP, fc="#f7ebdf", ec=COPPER, lw=1.8))
    for i in range(rows):
        for j in range(NCOL):
            ax.add_patch(Circle((x0 + 0.45 + j * GAP, y0 + 0.45 + i * GAP), 0.13, fc=COPPER, ec="none"))
    for (i, j) in hits:
        ax_, ay = x0 + 0.45 + j * GAP, y0 + 0.45 + i * GAP
        ex = ax_ - 0.3
        ax.add_patch(Circle((ex, ay), 0.1, fc=ELEC, ec="none", zorder=6))
        arrow(ax, (ex - 0.42, ay), (ex - 0.1, ay), color=ELEC, lw=1.2, ms=7)
        ax.add_patch(Circle((ax_ - 0.13, ay), 0.3, fc="none", ec=RED, lw=1.6, zorder=7))
    label(ax, x1 + 0.35, y0 + rows * GAP / 2, "전자 8", fs=10, ha="left")


channel(2.9, 4, [(0, 2), (1, 7), (2, 4), (3, 10), (0, 9), (1, 1), (2, 11), (3, 5)])
channel(1.0, 1, [(0, 1), (0, 2), (0, 4), (0, 5), (0, 7), (0, 8), (0, 10), (0, 11)])
label(ax, 1.5, 4.7, "굵은 전선", fs=11, bold=True)
label(ax, 1.5, 1.45, "가는 선", fs=11, bold=True, color=RED)
label(ax, 8.6, 0.45, "부딪힘 몰림", fs=10.5, color=RED, bold=True)
label(ax, 8.6, 6.95, "부딪힘 흩어짐", fs=10.5, bold=True)
save(fig, "m11-thin.svg")

# 8. 틈에 물건 끼워 보기
fig, ax = canvas(10.4, 4.0, 18.6, 6.9)
for x0, on, thing in [(1.0, True, "클립"), (10.4, False, "지우개")]:
    w, h = 6.0, 3.6
    bx = x0 + w / 2 - 1.2
    wire(ax, [(bx, 1.4), (x0, 1.4), (x0, 1.4 + h), (x0 + w / 2 - 0.3, 1.4 + h)])
    wire(ax, [(x0 + w / 2 + 0.3, 1.4 + h), (x0 + w, 1.4 + h), (x0 + w, 3.9)])
    wire(ax, [(x0 + w, 2.5), (x0 + w, 1.4), (bx + 2.55, 1.4)])
    if on:
        ax.add_patch(FancyBboxPatch((x0 + w - 0.25, 2.55), 0.5, 1.3, boxstyle="round,pad=0.12", fc="none", ec=GREY,
                                    lw=3.2, zorder=4))
    else:
        ax.add_patch(FancyBboxPatch((x0 + w - 0.4, 2.55), 0.8, 1.3, boxstyle="round,pad=0.08", fc="#f3c6cf",
                                    ec=INK, lw=1.2, zorder=4))
    ax.add_patch(Circle((x0 + w, 3.2), 1.05, fc="none", ec=RED, lw=2, zorder=7))
    label(ax, x0 + w + 1.3, 3.2, thing, fs=11, bold=True, ha="left")
    battery(ax, bx, 0.9)
    bulb(ax, x0 + w / 2, 1.4 + h - 0.4, on, 0.9)
    label(ax, x0 + w / 2, 0.3, "켜짐" if on else "꺼짐", fs=12, bold=True)
save(fig, "m11-test.svg")

# 9. 잘 흐르는 것 안 흐르는 것, 전선 자른 면
fig, ax = canvas(10.4, 4.8, 17.0, 7.8)
ax.add_patch(FancyBboxPatch((0.9, 5.9), 1.6, 0.6, boxstyle="round,pad=0.2", fc="none", ec=GREY, lw=3))
ax.add_patch(Ellipse((4.1, 6.2), 1.6, 0.8, fc=GREY, ec=INK, lw=1)); ax.plot([4.9, 6.5], [6.2, 6.2], color=GREY, lw=4)
ax.add_patch(Rectangle((7.4, 5.8), 1.8, 0.9, fc="#dfe3e6", ec=INK, lw=1))
for (x, lab) in [(1.7, "클립"), (4.7, "숟가락"), (8.3, "알루미늄 포일")]:
    label(ax, x, 5.2, lab, fs=10)
ax.add_patch(FancyBboxPatch((0.9, 3.5), 1.6, 0.8, boxstyle="round,pad=0.1", fc="#f3c6cf", ec=INK, lw=1))
ax.add_patch(Rectangle((3.3, 3.7), 3.0, 0.4, fc="#cde8f7", ec=INK, lw=1))
ax.add_patch(Rectangle((7.4, 3.8), 1.8, 0.25, fc="#c8a27a", ec=INK, lw=1))
for (x, lab) in [(1.7, "지우개"), (4.8, "플라스틱 자"), (8.3, "나무젓가락")]:
    label(ax, x, 2.9, lab, fs=10)
label(ax, 10.6, 6.2, "잘 흐름", fs=12, color=RED, bold=True, ha="left")
label(ax, 10.6, 3.9, "거의 안 흐름", fs=12, bold=True, ha="left")
ax.plot([0.4, 16.6], [2.2, 2.2], color=GREY, lw=1, ls=":")
ax.add_patch(Circle((5.0, 1.0), 0.8, fc="#2c8a3a", ec=INK, lw=1.2))
ax.add_patch(Circle((5.0, 1.0), 0.35, fc=COPPER, ec=INK, lw=1))
ax.annotate("구리 선", (5.1, 1.1), (7.2, 1.4), fontsize=10.5, va="center",
            arrowprops=dict(arrowstyle="-", color=INK, lw=1))
ax.annotate("플라스틱 껍질", (5.6, 0.5), (7.2, 0.4), fontsize=10.5, va="center",
            arrowprops=dict(arrowstyle="-", color=INK, lw=1))
label(ax, 2.4, 1.0, "전선 자른 면", fs=10.5, bold=True)
save(fig, "m11-conduct.svg")
