"""물질과 에너지 12편 그림 만들기. 실행: python lab/fig_m12.py  → docs/matter/img/12/*.svg
확인용 PNG: FIG_FMT=png FIG_OUT=<폴더> python lab/fig_m12.py

글자는 SVG 안에 글자로 남긴다(글꼴 모양을 파일에 넣지 않는다). 보는 쪽 글꼴로 그려진다.
그림 안 글씨는 낱말과 숫자만 둔다. 강조(지금 볼 곳)만 빨강으로 칠한다.
자석의 N극·S극은 흔히 쓰는 대로 붉은색·파란색으로 칠하되 강조 빨강보다 흐리게 둔다.
"""
import math
import os

import matplotlib

matplotlib.use("svg" if os.environ.get("FIG_FMT", "svg") == "svg" else "agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Ellipse, FancyArrowPatch, FancyBboxPatch, Polygon, Rectangle

OUT = os.environ.get("FIG_OUT") or os.path.join(os.path.dirname(__file__), "..", "docs", "matter", "img", "12")
FMT = os.environ.get("FIG_FMT", "svg")
os.makedirs(OUT, exist_ok=True)

plt.rcParams.update({
    "font.family": ["Apple SD Gothic Neo", "Noto Sans KR", "Malgun Gothic", "sans-serif"],
    "svg.fonttype": "none",
    "text.color": "#222",
    "figure.facecolor": "white",
    "savefig.facecolor": "white",
})

RED, GREY, INK = "#e4572e", "#c9ccd1", "#555"
NCOL, SCOL = "#d9837a", "#7b9fd1"
STEEL = "#9aa3ad"
WIRE = "#b87333"


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
    ax.text(x, y, s, ha=ha, va="center", fontsize=fs, color=color, fontweight="bold" if bold else "normal", zorder=9)


def magnet(ax, x, y, w=3.0, h=0.8, flip=False, text=True, z=3):
    """flip=False면 왼쪽 S, 오른쪽 N."""
    left, right = (SCOL, NCOL) if not flip else (NCOL, SCOL)
    ax.add_patch(Rectangle((x, y), w / 2, h, fc=left, ec=INK, lw=1.2, zorder=z))
    ax.add_patch(Rectangle((x + w / 2, y), w / 2, h, fc=right, ec=INK, lw=1.2, zorder=z))
    if text:
        ax.text(x + w * 0.15, y + h / 2, "S" if not flip else "N", ha="center", va="center", fontsize=11,
                color="white", fontweight="bold", zorder=z + 1)
        ax.text(x + w * 0.85, y + h / 2, "N" if not flip else "S", ha="center", va="center", fontsize=11,
                color="white", fontweight="bold", zorder=z + 1)


def vmagnet(ax, x, y, w=0.8, h=2.6):
    """세운 막대자석, 아래가 N."""
    ax.add_patch(Rectangle((x, y + h / 2), w, h / 2, fc=SCOL, ec=INK, lw=1.2, zorder=3))
    ax.add_patch(Rectangle((x, y), w, h / 2, fc=NCOL, ec=INK, lw=1.2, zorder=3))
    ax.text(x + w / 2, y + h * 0.82, "S", ha="center", va="center", fontsize=11, color="white", fontweight="bold",
            zorder=4)
    ax.text(x + w / 2, y + h * 0.18, "N", ha="center", va="center", fontsize=11, color="white", fontweight="bold",
            zorder=4)


def clip(ax, x, y, s=1.0, ang=0, color=STEEL):
    """(x, y)는 클립 가운데. ang=90이면 눕힌 클립."""
    w, h = (0.3 * s, 0.9 * s) if ang == 0 else (0.9 * s, 0.3 * s)
    ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h, boxstyle="round,pad=0.08", fc="none", ec=color, lw=2.6,
                                zorder=4))


def tiny(ax, x, y, ang, L=0.45, color=INK):
    dx, dy = L / 2 * math.cos(ang), L / 2 * math.sin(ang)
    ax.add_patch(FancyArrowPatch((x - dx, y - dy), (x + dx, y + dy), arrowstyle="-|>", mutation_scale=9, color=color,
                                 lw=1.4))


def battery(ax, x, y, w=2.0, h=0.8):
    ax.add_patch(Rectangle((x, y), w, h, fc="#4a4a4a", ec=INK, lw=1.2, zorder=4))
    ax.add_patch(Rectangle((x + w * 0.7, y), w * 0.3, h, fc="#f2c12e", ec=INK, lw=1.2, zorder=4))
    ax.text(x + w * 0.85, y + h / 2, "+", ha="center", va="center", fontsize=11, fontweight="bold", zorder=5)
    ax.text(x + w * 0.3, y + h / 2, "−", ha="center", va="center", fontsize=11, color="white", fontweight="bold",
            zorder=5)


def compass(ax, x, y, ang, r=0.75, z=5):
    """ang: N 끝이 가리키는 각(도). 90이 위쪽."""
    ax.add_patch(Circle((x, y), r, fc="white", ec=INK, lw=1.4, zorder=z))
    t = math.radians(ang)
    tip = (x + 0.8 * r * math.cos(t), y + 0.8 * r * math.sin(t))
    tail = (x - 0.8 * r * math.cos(t), y - 0.8 * r * math.sin(t))
    side = (0.14 * r * math.cos(t + math.pi / 2), 0.14 * r * math.sin(t + math.pi / 2))
    ax.add_patch(Polygon([tip, (x + side[0], y + side[1]), (x - side[0], y - side[1])], closed=True, fc=NCOL, ec=INK,
                         lw=0.6, zorder=z + 1))
    ax.add_patch(Polygon([tail, (x + side[0], y + side[1]), (x - side[0], y - side[1])], closed=True, fc=SCOL, ec=INK,
                         lw=0.6, zorder=z + 1))
    ax.add_patch(Circle((x, y), 0.05, fc=INK, zorder=z + 2))


# 1. 여는 장면: 냉장고 문의 자석과 클립 줄
fig, ax = canvas(9.0, 4.2, 15.0, 7.0)
ax.add_patch(Rectangle((0.8, 0.9), 4.6, 5.6, fc="#eef1f4", ec=INK, lw=1.4))
ax.add_patch(Rectangle((1.6, 2.4), 2.6, 2.4, fc="white", ec=INK, lw=1))
ax.plot([1.9, 3.9], [3.2, 3.2], color=GREY, lw=1); ax.plot([1.9, 3.5], [3.6, 3.6], color=GREY, lw=1)
ax.add_patch(Circle((2.9, 4.6), 0.35, fc=NCOL, ec=RED, lw=2))
label(ax, 3.1, 0.35, "냉장고 문", fs=11, bold=True)
magnet(ax, 7.6, 4.6, 3.4, 0.8)
for k in range(3):
    clip(ax, 11.35, 4.55 - k * 1.05)
ax.add_patch(Ellipse((11.35, 3.5), 1.3, 3.6, fc="none", ec=RED, lw=2, zorder=6))
label(ax, 9.3, 6.0, "막대자석", fs=11, bold=True)
label(ax, 12.6, 3.5, "클립", fs=11, bold=True, ha="left")
save(fig, "m12-fridge.svg")

# 2. 붙는 것과 안 붙는 것
fig, ax = canvas(10.0, 4.4, 16.4, 7.0)
magnet(ax, 0.6, 4.8, 2.6, 0.7)
clip(ax, 3.45, 5.15, 0.8, ang=90)
ax.plot([3.9, 5.6], [5.15, 5.15], color=STEEL, lw=3); ax.add_patch(Rectangle((3.85, 4.95), 0.15, 0.4, fc=STEEL, ec=INK,
                                                                            lw=0.8))
ax.add_patch(Rectangle((6.4, 4.6), 1.6, 1.1, fc="#eef1f4", ec=INK, lw=1))
for (x, lab) in [(3.45, "클립"), (4.8, "쇠못"), (7.2, "냉장고 문 조각")]:
    label(ax, x, 4.0, lab, fs=10)
label(ax, 9.6, 5.15, "붙음", fs=12, color=RED, bold=True, ha="left")
magnet(ax, 0.6, 1.6, 2.6, 0.7)
ax.add_patch(Rectangle((4.0, 1.2), 0.8, 1.4, fc="#d6dde3", ec=INK, lw=1))
ax.add_patch(Circle((5.8, 1.9), 0.4, fc="#c9a96e", ec=INK, lw=1))
ax.add_patch(FancyBboxPatch((6.8, 1.6), 0.9, 0.55, boxstyle="round,pad=0.08", fc="#f3c6cf", ec=INK, lw=1))
ax.add_patch(Rectangle((8.2, 1.8), 1.6, 0.18, fc="#c8a27a", ec=INK, lw=1))
for (x, lab) in [(4.4, "알루미늄 캔"), (5.8, "동전"), (7.25, "지우개"), (9.0, "나무젓가락")]:
    label(ax, x, 0.6, lab, fs=10)
label(ax, 10.6, 1.9, "안 붙음", fs=12, bold=True, ha="left")
save(fig, "m12-stick.svg")

# 3. 두 극
fig, ax = canvas(10.0, 3.8, 16.0, 6.2)
magnet(ax, 0.8, 4.0, 3.0, 0.8)
magnet(ax, 5.0, 4.0, 3.0, 0.8)
arrow(ax, (3.95, 4.4), (4.4, 4.4), color=RED, lw=2); arrow(ax, (4.85, 4.4), (4.45, 4.4), color=RED, lw=2)
label(ax, 9.0, 4.4, "N과 S", fs=11, ha="left")
label(ax, 11.4, 4.4, "당김", fs=12, color=RED, bold=True, ha="left")
magnet(ax, 0.8, 1.2, 3.0, 0.8)
magnet(ax, 5.6, 1.2, 3.0, 0.8, flip=True)
arrow(ax, (4.5, 1.6), (3.95, 1.6), color=INK, lw=2); arrow(ax, (4.9, 1.6), (5.45, 1.6), color=INK, lw=2)
label(ax, 9.0, 1.6, "N과 N", fs=11, ha="left")
label(ax, 11.4, 1.6, "밀어냄", fs=12, bold=True, ha="left")
save(fig, "m12-poles.svg")

# 4. 쇠 속 작은 자석들
fig, ax = canvas(10.0, 4.0, 16.4, 6.4)
ax.add_patch(FancyBboxPatch((0.6, 1.4), 5.6, 4.2, boxstyle="round,pad=0.08", fc="#eef1f4", ec=INK, lw=1.6))
for gi, gj, ang in [(0, 0, 0.3), (0, 1, 2.0), (1, 0, 3.6), (1, 1, 5.0)]:
    gx, gy = 1.0 + gi * 2.6, 1.8 + gj * 1.9
    ax.add_patch(Rectangle((gx - 0.1, gy - 0.15), 2.4, 1.7, fc="none", ec=GREY, lw=1, ls="--"))
    for i in range(2):
        for j in range(3):
            tiny(ax, gx + 0.4 + j * 0.75, gy + 0.35 + i * 0.75, ang)
label(ax, 3.4, 0.7, "자석 없음", fs=11.5, bold=True)
arrow(ax, (6.6, 3.5), (8.0, 3.5))
magnet(ax, 8.4, 3.1, 2.0, 0.8, flip=True)
ax.add_patch(FancyBboxPatch((10.8, 1.4), 4.8, 4.2, boxstyle="round,pad=0.08", fc="#eef1f4", ec=INK, lw=1.6))
for i in range(4):
    for j in range(6):
        tiny(ax, 11.25 + j * 0.75, 1.95 + i * 0.95, math.pi, color=RED)
label(ax, 13.2, 0.7, "자석 가까이", fs=11.5, bold=True, color=RED)
save(fig, "m12-domains.svg")

# 5. 클립 줄: 자석이 있을 때와 뗐을 때
fig, ax = canvas(10.0, 4.6, 15.6, 7.2)
vmagnet(ax, 2.6, 4.0)
for k in range(3):
    clip(ax, 3.0, 3.45 - k * 1.05)
label(ax, 3.0, 0.2, "자석 있음", fs=11.5, bold=True)
clip(ax, 11.0, 3.45, color=RED)
label(ax, 11.6, 3.45, "잡은 클립", fs=10.5, ha="left")
clip(ax, 10.3, 0.9, ang=90)
clip(ax, 11.7, 0.75, ang=90)
arrow(ax, (12.9, 2.6), (12.9, 1.3), color=RED, lw=2)
label(ax, 11.0, 0.2, "자석 뗌", fs=11.5, bold=True)
arrow(ax, (5.6, 3.4), (8.4, 3.4))
save(fig, "m12-chain.svg")

# 6. 보이지 않는 힘: 철가루 무늬
fig, ax = canvas(10.0, 4.6, 16.0, 7.4)
ax.add_patch(Rectangle((0.6, 0.4), 11.4, 6.6, fc="#fbfaf6", ec=GREY, lw=1))
magnet(ax, 4.8, 3.3, 3.0, 0.8)
qN, qS = (7.35, 3.7), (5.25, 3.7)


def fld(x, y):
    ex = ey = 0.0
    for (qx, qy), q in ((qN, 1), (qS, -1)):
        dx, dy = x - qx, y - qy
        r3 = (dx * dx + dy * dy) ** 1.5 + 1e-9
        ex += q * dx / r3; ey += q * dy / r3
    return ex, ey


for a0 in range(-165, 166, 22):
    t = math.radians(a0)
    x, y = qN[0] + 0.3 * math.cos(t), qN[1] + 0.3 * math.sin(t)
    pts = [(x, y)]
    for _ in range(4000):
        ex, ey = fld(x, y)
        n = math.hypot(ex, ey)
        x += 0.02 * ex / n; y += 0.02 * ey / n
        pts.append((x, y))
        if math.hypot(x - qS[0], y - qS[1]) < 0.25 or not (0.7 < x < 11.9 and 0.5 < y < 6.9):
            break
    for k in range(0, len(pts) - 6, 12):
        (x1, y1), (x2, y2) = pts[k], pts[k + 6]
        if not (4.8 < x1 < 7.8 and abs(y1 - 3.7) < 0.42):
            ax.plot([x1, x2], [y1, y2], color=INK, lw=1.1)
            if x1 > 7.8 or x2 > 7.8:
                ax.plot([12.6 - x1, 12.6 - x2], [y1, y2], color=INK, lw=1.1)
for cx in (4.5, 8.1):
    ax.add_patch(Circle((cx, 3.7), 0.9, fc="none", ec=RED, lw=2, zorder=6))
ax.annotate("가장 강함", (8.9, 3.4), (13.0, 2.0), fontsize=11, color=RED, fontweight="bold", va="center",
            arrowprops=dict(arrowstyle="-", color=RED, lw=1.2))
save(fig, "m12-field.svg")

# 7. 지구와 나침반
fig, ax = canvas(9.0, 4.6, 13.0, 7.4)
for a_ in (0.9, 1.4, 1.9):
    for d in (-1, 1):
        ax.add_patch(Ellipse((4.0 + d * a_, 3.8), 2 * a_, 2.0 + a_ * 2.2, fc="none", ec=INK, lw=1, ls=(0, (1, 2))))
ax.add_patch(Circle((4.0, 3.8), 1.6, fc="#bfe0c8", ec=INK, lw=1.4, zorder=3))
label(ax, 4.0, 7.1, "북쪽", fs=11, bold=True)
arrow(ax, (4.0, 5.6), (4.0, 6.7), color=INK, lw=1.4)
compass(ax, 9.6, 3.8, 90, r=1.1)
arrow(ax, (9.6, 5.1), (9.6, 6.4), color=RED, lw=2)
label(ax, 9.6, 6.9, "북쪽", fs=11, bold=True, color=RED)
label(ax, 10.2, 4.5, "N", fs=11, bold=True, ha="left")
label(ax, 9.6, 2.2, "나침반", fs=11, bold=True)
label(ax, 4.0, 1.0, "지구", fs=11, bold=True)
save(fig, "m12-earth.svg")

# 8. 전선 위 나침반 (외르스테드 배치): 전선을 바늘과 나란히(남북, 그림에서 세로) 놓는다.
# 전기가 북쪽(위)으로 흐르면 전선 위쪽의 힘은 동쪽(오른쪽)을 향해 N 끝이 오른쪽으로 돈다.
fig, ax = canvas(9.0, 4.6, 15.0, 7.6)
arrow(ax, (0.6, 3.4), (0.6, 5.4), color=INK, lw=1.4)
label(ax, 0.6, 5.9, "북쪽", fs=10.5, bold=True)
for cx, on in [(4.2, False), (10.8, True)]:
    ax.plot([cx, cx], [1.5, 6.6], color=WIRE, lw=4, zorder=2)
    compass(ax, cx, 4.1, 90 if not on else 35, r=1.0)
    if on:
        arrow(ax, (cx + 0.45, 1.6), (cx + 0.45, 2.7), color=INK, lw=1.6)
        ax.add_patch(Circle((cx, 4.1), 1.25, fc="none", ec=RED, lw=2, zorder=8))
    label(ax, cx, 0.8, "전기 켬" if on else "전기 끔", fs=11.5, bold=True, color=RED if on else "#222")
label(ax, 4.45, 6.3, "전선", fs=10.5, ha="left")
save(fig, "m12-wire.svg")

# 9. 전자석: 켬과 끔
fig, ax = canvas(10.4, 4.4, 17.6, 7.4)
for x0, on in [(0.6, True), (9.4, False)]:
    bx, by, bw, bh = x0 + 0.4, 4.6, 6.0, 0.7
    ax.add_patch(Rectangle((bx, by), bw, bh, fc="#d6dde3", ec=INK, lw=1.2, zorder=2))
    c0, c1 = bx + 1.3, bx + bw - 0.4
    turns = 9
    for k in range(turns):
        xx = c0 + k * (c1 - c0) / (turns - 1)
        ax.add_patch(Ellipse((xx, by + bh / 2), 0.32, bh + 0.5, fc="none", ec=WIRE, lw=2, zorder=3))
    ax.plot([c0, c0, x0 + 2.9], [by + bh / 2, 2.0, 2.0], color=WIRE, lw=2, zorder=1)
    ax.plot([c1, c1, x0 + 5.3], [by + bh / 2, 2.0, 2.0], color=WIRE, lw=2, zorder=1)
    if not on:
        ax.plot([x0 + 5.3, x0 + 5.8], [2.0, 2.4], color=WIRE, lw=2, zorder=1)
        ax.add_patch(Circle((x0 + 5.6, 2.05), 0.45, fc="none", ec=RED, lw=2, zorder=7))
    battery(ax, x0 + 3.0, 1.6)
    if on:
        for k in range(2):
            clip(ax, bx + 0.3, by - 0.5 - k * 1.05)
        ax.add_patch(Ellipse((bx + 0.3, by - 1.0), 1.0, 2.6, fc="none", ec=RED, lw=2, zorder=7))
    else:
        clip(ax, bx + 0.2, 0.9, ang=90)
        clip(ax, bx + 1.4, 0.8, ang=90)
    label(ax, x0 + 3.4, 0.2, "전기 켬" if on else "전기 끔", fs=11.5, bold=True, color=RED if on else "#222")
label(ax, 4.0, 6.4, "쇠막대에 감은 전선", fs=10.5)
save(fig, "m12-coil.svg")
