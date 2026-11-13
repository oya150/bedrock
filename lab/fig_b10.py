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

OUT = os.environ.get("FIG_OUT") or os.path.join(os.path.dirname(__file__), "..", "docs", "body", "img", "10")
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
from matplotlib.patches import Ellipse, Polygon, Wedge

CELL = "#fbe3dc"
LIGHT_C = "#f6c445"
NERVE = "#8e5ea2"
IRIS = "#7a9a6b"


def eyeball(ax, cx, cy, r=2.4, pupil=0.5, retina=RED):
    """눈을 옆에서 자른 모습: 왼쪽이 앞."""
    ax.add_patch(Circle((cx, cy), r, fc="white", ec=INK, lw=1.8))
    # 망막: 뒤쪽 호
    ax.add_patch(Arc((cx, cy), 2 * r - 0.2, 2 * r - 0.2, theta1=-110, theta2=110, color=retina, lw=4))
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


# 1. 여는 장면: 불 켠 방과 불 끈 방
fig, ax = canvas(10.0, 3.8, 16.0, 6.4)
for k, (x, dark) in enumerate([(0.6, False), (8.6, True)]):
    ax.add_patch(Rectangle((x, 1.2), 6.6, 5.0, fc="#2f2f3a" if dark else "#fffdf0", ec=INK, lw=1.4))
    ax.add_patch(Rectangle((x + 1.0, 1.6), 1.8, 1.4, fc="#4a4a55" if dark else "#e4572e", ec=INK, lw=1))
    ax.add_patch(Circle((x + 4.8, 2.4), 0.7, fc="#4a4a55" if dark else "#7da2c8", ec=INK, lw=1))
    ax.add_patch(Circle((x + 5.6, 5.4), 0.4, fc="#4a4a55" if dark else LIGHT_C, ec=INK, lw=1))
    ax.text(x + 3.3, 0.6, "불 끔" if dark else "불 켬", ha="center", va="center",
            fontsize=12, fontweight="bold", color=RED if dark else "#222")
save(fig, "b10-dark.svg")

# 2. 빛이 사과에 닿아 눈으로
fig, ax = canvas(11.0, 4.0, 18.0, 6.8)
ax.add_patch(Circle((1.6, 5.4), 0.7, fc=LIGHT_C, ec=INK, lw=1.2))
for a in range(0, 360, 45):
    r = math.radians(a)
    ax.plot([1.6 + 0.9 * math.cos(r), 1.6 + 1.2 * math.cos(r)], [5.4 + 0.9 * math.sin(r), 5.4 + 1.2 * math.sin(r)],
            color=LIGHT_C, lw=2)
ax.add_patch(Circle((6.0, 2.4), 1.1, fc=RED, ec=INK, lw=1.2))
ax.plot([6.0, 6.2], [3.5, 4.1], color=INK, lw=2)
ax.add_patch(Ellipse((6.6, 3.9), 0.7, 0.3, angle=20, fc="#8fb58f", ec=INK, lw=1))
ax.text(6.0, 0.7, "사과", ha="center", va="center", fontsize=11)
arrow(ax, (2.3, 4.8), (5.4, 3.5), color=LIGHT_C, lw=2.4)
arrow(ax, (7.2, 2.7), (12.4, 3.2), color=RED, lw=2.4)
eyeball(ax, 14.6, 3.2, r=1.8, pupil=0.4, retina=INK)
ax.text(9.8, 3.6, "튕긴 빛", ha="center", va="center", fontsize=11, color=RED, fontweight="bold")
ax.text(14.6, 0.7, "눈", ha="center", va="center", fontsize=11)
ax.text(1.6, 3.9, "해", ha="center", va="center", fontsize=11)
ax.text(4.2, 4.7, "빛", ha="center", va="center", fontsize=11, color="#b08800", fontweight="bold")
save(fig, "b10-light.svg")

# 3. 눈동자: 밝으면 작게, 어두우면 크게
fig, ax = canvas(10.0, 3.6, 16.0, 6.0)
for k, (x, pr, lab, bg) in enumerate([(3.6, 0.35, "밝을 때", "#fffdf0"), (12.4, 0.95, "어두울 때", "#d9d9e0")]):
    ax.add_patch(Rectangle((x - 3.0, 1.0), 6.0, 4.6, fc=bg, ec=INK, lw=1.2))
    ax.add_patch(Ellipse((x, 3.3), 4.6, 2.4, fc="white", ec=INK, lw=1.6))
    ax.add_patch(Circle((x, 3.3), 1.1, fc=IRIS, ec=INK, lw=1.2))
    ax.add_patch(Circle((x, 3.3), pr, fc="#222", ec=RED, lw=2.2))
    ax.text(x, 0.5, lab, ha="center", va="center", fontsize=12, fontweight="bold")
ax.text(3.6, 5.1, "눈동자", ha="center", va="center", fontsize=11, color=RED, fontweight="bold")
arrow(ax, (3.6, 4.8), (3.6, 3.75), color=RED, lw=1.4, ms=10)
ax.text(8.0, 5.4, "", ha="center")
save(fig, "b10-pupil.svg")

# 4. 눈 속: 창과 렌즈가 빛을 꺾어 망막에 모아요
fig, ax = canvas(10.0, 4.6, 17.0, 8.0)
eyeball(ax, 10.0, 4.0, r=3.2, pupil=0.6)
for y0 in (5.4, 4.0, 2.6):
    ax.plot([1.0, 7.2], [y0, 4.0 + (y0 - 4.0) * 0.35], color=LIGHT_C, lw=2)
    ax.plot([7.2, 13.0], [4.0 + (y0 - 4.0) * 0.35, 4.0], color=LIGHT_C, lw=2)
ax.add_patch(Circle((13.0, 4.0), 0.18, fc=RED, ec=RED))
ax.text(13.6, 7.6, "망막", ha="center", va="center", fontsize=12, color=RED, fontweight="bold")
arrow(ax, (13.5, 7.3), (12.9, 6.5), color=RED, lw=1.2, ms=10)
ax.text(6.2, 7.2, "렌즈", ha="center", va="center", fontsize=11)
arrow(ax, (6.3, 6.9), (7.6, 5.2), color=INK, lw=1.2, ms=10)
ax.text(4.6, 1.0, "투명한 창", ha="center", va="center", fontsize=11)
arrow(ax, (5.2, 1.3), (6.7, 2.8), color=INK, lw=1.2, ms=10)
ax.text(14.2, 1.4, "신경", ha="left", va="center", fontsize=11, color=NERVE, fontweight="bold")
save(fig, "b10-inside.svg")

# 5. 렌즈 두께: 가까이 보면 불룩, 멀리 보면 납작
fig, ax = canvas(10.0, 3.8, 18.0, 6.8)
for x0, near in [(0.0, True), (9.4, False)]:
    ex, ey, r = x0 + 6.0, 3.4, 1.9
    ax.add_patch(Circle((ex, ey), r, fc="white", ec=INK, lw=1.6))
    ax.add_patch(Arc((ex, ey), 2 * r - 0.2, 2 * r - 0.2, theta1=-110, theta2=110, color=INK, lw=3))
    lw_ = 0.9 if near else 0.35
    ax.add_patch(Ellipse((ex - r + 0.75, ey), lw_, 1.7, fc="#e8f1f8", ec=RED, lw=2.2, zorder=4))
    ox = x0 + (3.0 if near else 0.2)
    ax.add_patch(Circle((ox, ey), 0.35, fc=BLUE, ec=INK, lw=1))
    lx = ex - r + 0.75
    for dy in (0.7, -0.7):
        ax.plot([ox + 0.35, lx], [ey, ey + dy], color=LIGHT_C, lw=1.8)
        ax.plot([lx, ex + r - 0.1], [ey + dy, ey], color=LIGHT_C, lw=1.8)
    ax.text(ox, ey - 0.9, "가까이" if near else "멀리", ha="center", va="center", fontsize=11)
    ax.text(lx, ey + 2.6, "불룩" if near else "납작", ha="center", va="center", fontsize=13, color=RED,
            fontweight="bold")
ax.plot([8.6, 8.6], [0.4, 6.4], color=GREY, lw=1.2, ls="--")
save(fig, "b10-lens.svg")

# 6. 밝은 곳은 색깔로, 어두운 곳은 회색으로
fig, ax = canvas(9.0, 3.6, 16.0, 6.4)
for x, dark in [(0.6, False), (8.6, True)]:
    ax.add_patch(Rectangle((x, 1.2), 6.6, 4.8, fc="#3a3a46" if dark else "#fffdf0", ec=INK, lw=1.4))
    c = "#9a9aa0" if dark else RED
    ax.add_patch(Circle((x + 3.3, 3.4), 1.2, fc=c, ec=INK, lw=1.2))
    ax.plot([x + 3.3, x + 3.5], [4.6, 5.2], color=INK if not dark else "#ccc", lw=2)
    ax.text(x + 3.3, 0.6, "회색" if dark else "빨강", ha="center", va="center", fontsize=12, fontweight="bold",
            color="#222")
ax.text(3.9, 6.3, "밝은 곳", ha="center", va="center", fontsize=11)
ax.text(11.9, 6.3, "어두운 곳", ha="center", va="center", fontsize=11)
save(fig, "b10-gray.svg")

# 7. 맹점: 신경이 나가는 자리
fig, ax = canvas(9.0, 4.6, 15.0, 8.0)
cx, cy, r = 6.0, 4.0, 3.2
ax.add_patch(Circle((cx, cy), r, fc="white", ec=INK, lw=1.8))
gap = (-34, -22)
ax.add_patch(Arc((cx, cy), 2 * r - 0.2, 2 * r - 0.2, theta1=gap[1], theta2=110, color=INK, lw=4))
ax.add_patch(Arc((cx, cy), 2 * r - 0.2, 2 * r - 0.2, theta1=-110, theta2=gap[0], color=INK, lw=4))
ax.add_patch(Arc((cx - r + 0.1, cy), 1.0, 2.0, theta1=90, theta2=270, color=INK, lw=1.6))
ax.add_patch(Ellipse((cx - r + 0.9, cy), 0.55, 1.6, fc="#e8f1f8", ec=INK, lw=1.4))
nx, ny = cx + r * math.cos(math.radians(-28)), cy + r * math.sin(math.radians(-28))
ax.plot([nx - 0.1, nx + 2.0], [ny + 0.05, ny - 0.9], color=NERVE, lw=7, solid_capstyle="round")
ax.add_patch(Circle((nx - 0.05, ny), 0.32, fc="none", ec=RED, lw=2.4, zorder=5))
ax.add_patch(Circle((cx + r - 0.1, cy), 0.16, fc=LIGHT_C, ec=INK, lw=1))
ax.text(nx + 0.6, ny + 0.75, "맹점", ha="left", va="center", fontsize=12, color=RED, fontweight="bold")
ax.text(cx + r + 0.4, cy + 0.6, "한가운데", ha="left", va="center", fontsize=11)
ax.text(nx + 2.2, ny - 1.3, "신경", ha="left", va="center", fontsize=11, color=NERVE, fontweight="bold")
ax.text(cx + 1.0, cy + r + 0.5, "망막", ha="center", va="center", fontsize=11)
save(fig, "b10-blindspot-eye.svg")

# 8. 맹점 찾기 카드
fig, ax = canvas(10.0, 2.6, 16.0, 4.2)
ax.add_patch(Rectangle((0.4, 0.4), 15.2, 3.4, fc="white", ec=GREY, lw=1.2))
ax.text(3.0, 2.1, "+", ha="center", va="center", fontsize=40, fontweight="bold")
ax.add_patch(Circle((12.4, 2.1), 0.55, fc=INK, ec=INK))
save(fig, "b10-blindspot.svg")

# 9. 두 눈은 조금 다른 쪽에서 봐요
fig, ax = canvas(8.0, 5.2, 14.0, 9.0)
ax.set_ylim(-0.4, 9.0)
ax.plot([0.6, 13.4], [8.0, 8.0], color=INK, lw=3)
ax.text(13.4, 8.5, "벽", ha="right", va="center", fontsize=11)
L, R, F = (5.6, 0.8), (8.4, 0.8), (7.0, 4.0)
for (ex, ey), col, lab in [(L, INK, "왼눈"), (R, RED, "오른눈")]:
    ax.add_patch(Ellipse((ex, ey), 1.4, 0.8, fc="white", ec=INK, lw=1.4))
    ax.add_patch(Circle((ex, ey), 0.22, fc="#222"))
    t = (8.0 - ey) / (F[1] - ey)
    wx = ex + (F[0] - ex) * t
    ax.plot([ex, wx], [ey, 8.0], color=col, lw=1.6, ls="--")
    ax.add_patch(Rectangle((wx - 0.12, 7.0), 0.24, 1.0, fc=col, ec=col))
    ax.text(ex, ey - 0.8, lab, ha="center", va="center", fontsize=11, color=col, fontweight="bold")
ax.add_patch(Rectangle((F[0] - 0.15, F[1] - 0.6), 0.3, 1.2, fc=SKIN if "SKIN" in globals() else "#f6d8c4", ec=INK, lw=1.4,
                       zorder=5))
ax.text(F[0] + 0.5, F[1], "손가락", ha="left", va="center", fontsize=11)
save(fig, "b10-twoeyes.svg")
