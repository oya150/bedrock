"""인체 5편 그림 만들기. 실행: python lab/fig_b05.py  → docs/body/img/05/*.svg

확인용 PNG: FIG_FMT=png FIG_OUT=<폴더> python lab/fig_b05.py
글자는 SVG 안에 글자로 남긴다(글꼴 모양을 파일에 넣지 않는다). 보는 쪽 글꼴로 그려진다.
강조는 빨강 하나. 그림 안 글씨는 낱말과 숫자만 둔다.
"""
import os

import matplotlib

FMT = os.environ.get("FIG_FMT", "svg")
matplotlib.use("svg" if FMT == "svg" else "agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Ellipse, FancyArrowPatch, FancyBboxPatch, Rectangle

OUT = os.environ.get("FIG_OUT") or os.path.join(os.path.dirname(__file__), "..", "docs", "body", "img", "05")
os.makedirs(OUT, exist_ok=True)

plt.rcParams.update({
    "font.family": ["Apple SD Gothic Neo", "Noto Sans KR", "Malgun Gothic", "sans-serif"],
    "svg.fonttype": "none",
    "text.color": "#222",
    "figure.facecolor": "white",
    "savefig.facecolor": "white",
})

RED, GREY, INK = "#e4572e", "#c9ccd1", "#555"
BLUE = "#7da2c8"  # 4편과 같이 산소 내려 준 피에만 쓴다
WATER = "#dfe3e8"  # 스포이트 물
MUSCLE = "#f3c9bf"
SKIN = "#f6d8c4"
CELL = "#fbe3dc"


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


def dropper(ax, x, y, squeezed=False):
    """스포이트: 고무 머리 + 유리 관."""
    w = 0.9 if squeezed else 1.5
    ax.add_patch(Ellipse((x, y + 2.4), w, 1.6, fc=GREY, ec=INK, lw=1.6))
    ax.add_patch(Rectangle((x - 0.25, y), 0.5, 1.7, fc="white", ec=INK, lw=1.4))
    ax.add_patch(Rectangle((x - 0.2, y + 0.05), 0.4, 1.0 if squeezed else 1.6, fc=WATER, ec="none"))


def flap(ax, x, y, state, color=INK, lw=3.5, half=0.7):
    """가로 관을 가로지르는 문(날개 둘). 열리면 오른쪽(피가 가는 쪽)으로 젖혀진다."""
    if state == "open":
        ax.plot([x, x + 0.6], [y + half, y + 0.3], color=color, lw=lw, solid_capstyle="round")
        ax.plot([x, x + 0.6], [y - half, y - 0.3], color=color, lw=lw, solid_capstyle="round")
    else:
        ax.plot([x, x + 0.15], [y + half, y + 0.03], color=color, lw=lw, solid_capstyle="round")
        ax.plot([x, x + 0.15], [y - half, y - 0.03], color=color, lw=lw, solid_capstyle="round")


# 1. 짜고 풀기: 스포이트와 심장
fig, ax = canvas(11.0, 4.6, 18.0, 7.6)
dropper(ax, 1.8, 2.0, squeezed=False)
arrow(ax, (1.8, 0.3), (1.8, 1.9), color=INK, lw=2)
ax.text(1.8, 5.4, "놓으면", ha="center", va="center", fontsize=12, fontweight="bold")
dropper(ax, 5.2, 2.0, squeezed=True)
arrow(ax, (5.2, 1.9), (5.2, 0.3), color=INK, lw=2)
ax.text(5.2, 5.4, "쥐면", ha="center", va="center", fontsize=12, fontweight="bold")
ax.text(3.5, 6.9, "스포이트", ha="center", va="center", fontsize=13, fontweight="bold")
ax.plot([7.6, 7.6], [0.3, 7.2], color=GREY, lw=1.2, ls="--")
ax.text(12.9, 6.9, "심장", ha="center", va="center", fontsize=13, fontweight="bold")
ax.add_patch(Ellipse((10.4, 3.2), 2.9, 3.4, fc=MUSCLE, ec=INK, lw=2))
ax.text(10.4, 3.2, "피", ha="center", va="center", fontsize=12)
arrow(ax, (10.4, 0.0), (10.4, 1.4), color=INK, lw=2)
arrow(ax, (12.2, 3.2), (14.0, 3.2), color=INK, lw=1.4, ms=14)
ax.text(10.4, 5.4, "풀려요", ha="center", va="center", fontsize=12, fontweight="bold")
ax.add_patch(Ellipse((15.6, 3.2), 1.8, 2.2, fc=MUSCLE, ec=RED, lw=3))
ax.text(15.6, 3.2, "꽉!", ha="center", va="center", fontsize=12, color=RED, fontweight="bold")
arrow(ax, (15.6, 4.4), (15.6, 6.2), color=RED, lw=2.6)
ax.text(15.6, 1.5, "짜요", ha="center", va="center", fontsize=12, color=RED, fontweight="bold")
save(fig, "b05-squeeze.svg")

# 2. 한쪽으로만 열리는 문: 날개 둘
fig, ax = canvas(11.0, 4.6, 18.0, 7.6)
for x, opened, lab in [(4.0, True, "앞으로 밀 때"), (13.0, False, "거꾸로 밀 때")]:
    ax.add_patch(Rectangle((x - 1.2, 0.9), 2.4, 5.4, fc="#f7e3de", ec=INK, lw=1.4))
    if opened:
        ax.plot([x - 1.2, x - 0.45], [3.0, 4.4], color=INK, lw=4, solid_capstyle="round")
        ax.plot([x + 1.2, x + 0.45], [3.0, 4.4], color=INK, lw=4, solid_capstyle="round")
        arrow(ax, (x, 1.3), (x, 6.0), color=INK, lw=2.6)
        ax.text(x + 1.6, 4.0, "열려요", ha="left", va="center", fontsize=13, fontweight="bold")
    else:
        ax.plot([x - 1.2, x], [3.6, 3.15], color=RED, lw=4, solid_capstyle="round")
        ax.plot([x + 1.2, x], [3.6, 3.15], color=RED, lw=4, solid_capstyle="round")
        arrow(ax, (x, 6.0), (x, 3.9), color=INK, lw=2.6)
        ax.text(x + 1.6, 3.4, "닫혀요", ha="left", va="center", fontsize=13, color=RED, fontweight="bold")
    ax.text(x, 0.3, lab, ha="center", va="center", fontsize=12, fontweight="bold")
save(fig, "b05-valve.svg")

# 3. 들어오는 문과 나가는 문: 짤 때(쿵) / 풀릴 때(쾅)
fig, ax = canvas(12.0, 4.4, 20.0, 7.4)
for x0, title, squeeze in [(0.3, "짜요", True), (10.5, "풀려요", False)]:
    ax.add_patch(Rectangle((x0, 3.0), 2.4, 1.4, fc="white", ec=INK, lw=1.4))
    ax.add_patch(Rectangle((x0 + 6.6, 3.0), 2.4, 1.4, fc="white", ec=INK, lw=1.4))
    w, h = (2.8, 2.0) if squeeze else (3.8, 3.4)
    ax.add_patch(Ellipse((x0 + 4.6, 3.7), w, h, fc=MUSCLE, ec=INK, lw=2))
    in_x, out_x = x0 + 2.4, x0 + 6.6
    if squeeze:
        flap(ax, in_x, 3.7, "shut", color=RED)
        flap(ax, out_x, 3.7, "open")
        arrow(ax, (x0 + 5.2, 3.7), (x0 + 9.0, 3.7), color=INK, lw=2.4)
        ax.text(in_x, 5.6, "쿵", ha="center", va="center", fontsize=17, color=RED, fontweight="bold")
    else:
        flap(ax, in_x, 3.7, "open")
        flap(ax, out_x, 3.7, "shut", color=RED)
        arrow(ax, (x0 + 0.1, 3.7), (x0 + 4.0, 3.7), color=INK, lw=2.4)
        ax.text(out_x, 5.6, "쾅", ha="center", va="center", fontsize=17, color=RED, fontweight="bold")
    ax.text(in_x, 1.9, "들어오는 문", ha="center", va="center", fontsize=10)
    ax.text(out_x, 1.9, "나가는 문", ha="center", va="center", fontsize=10)
    ax.text(x0 + 4.5, 6.8, title, ha="center", va="center", fontsize=13, fontweight="bold")
ax.plot([10.0, 10.0], [0.9, 7.0], color=GREY, lw=1.2, ls="--")
save(fig, "b05-doors.svg")

# 4. 펌프 두 개: 1 온몸→오른쪽, 2 오른쪽→폐, 3 폐→왼쪽, 4 왼쪽→온몸
fig, ax = canvas(11.0, 6.0, 18.0, 9.8)
ax.add_patch(FancyBboxPatch((6.6, 3.4), 2.2, 2.6, boxstyle="round,pad=0.2", fc=MUSCLE, ec=INK, lw=1.6))
ax.add_patch(FancyBboxPatch((9.2, 3.4), 2.2, 2.6, boxstyle="round,pad=0.2", fc=MUSCLE, ec=INK, lw=3.2))
ax.text(7.7, 4.7, "오른쪽\n펌프", ha="center", va="center", fontsize=11, fontweight="bold")
ax.text(10.3, 4.7, "왼쪽\n펌프", ha="center", va="center", fontsize=11, fontweight="bold")
box(ax, 7.0, 7.8, 4.0, 1.4, fc="white")
ax.text(9.0, 8.5, "폐", ha="center", va="center", fontsize=12, fontweight="bold")
box(ax, 6.0, 0.2, 6.0, 1.4, fc=CELL)
ax.text(9.0, 0.9, "온몸", ha="center", va="center", fontsize=12, fontweight="bold")
arrow(ax, (6.8, 1.7), (6.4, 3.8), color=BLUE, lw=2.6, rad=-0.3)
arrow(ax, (7.7, 6.3), (7.9, 7.7), color=BLUE, lw=2.6)
arrow(ax, (10.1, 7.7), (10.3, 6.3), color=RED, lw=2.6)
arrow(ax, (11.6, 3.8), (11.2, 1.7), color=RED, lw=2.6, rad=-0.3)
for n, (x, y) in enumerate([(5.6, 2.6), (7.1, 7.0), (10.9, 7.0), (12.4, 2.6)], start=1):
    ax.add_patch(Circle((x, y), 0.36, fc="white", ec=INK, lw=1.4))
    ax.text(x, y, str(n), ha="center", va="center", fontsize=12, fontweight="bold")
ax.plot([14.0, 14.9], [6.0, 6.0], color=RED, lw=3)
ax.text(15.1, 6.0, "산소 실은 피", ha="left", va="center", fontsize=10)
ax.plot([14.0, 14.9], [5.2, 5.2], color=BLUE, lw=3)
ax.text(15.1, 5.2, "산소 내려 준 피", ha="left", va="center", fontsize=10)
save(fig, "b05-pumps.svg")

# 5. 박자를 만드는 곳: 신호가 퍼져요
fig, ax = canvas(7.0, 5.6, 11.0, 9.0)
ax.add_patch(FancyBboxPatch((2.6, 1.0), 3.4, 5.6, boxstyle="round,pad=0.3", fc=MUSCLE, ec=INK, lw=1.6))
ax.add_patch(FancyBboxPatch((6.4, 1.0), 3.4, 5.6, boxstyle="round,pad=0.3", fc=MUSCLE, ec=INK, lw=1.6))
ax.text(4.3, 0.1, "오른쪽 펌프", ha="center", va="center", fontsize=10)
ax.text(8.1, 0.1, "왼쪽 펌프", ha="center", va="center", fontsize=10)
sx, sy = 3.4, 6.0
ax.add_patch(Circle((sx, sy), 0.32, fc=RED, ec=RED))
ax.text(sx - 0.6, 7.9, "박자 만드는 곳", ha="left", va="center", fontsize=11, color=RED, fontweight="bold")
ax.plot([sx, sx], [sy + 0.35, 7.6], color=RED, lw=1.2)
for tx, ty in [(3.2, 2.0), (5.0, 3.0), (7.0, 4.8), (8.6, 2.2)]:
    arrow(ax, (sx + 0.1, sy - 0.3), (tx, ty), color=RED, lw=1.8, ms=14)
ax.text(sx + 1.0, sy + 0.45, "지금!", ha="left", va="center", fontsize=14, color=RED, fontweight="bold")
save(fig, "b05-signal.svg")

# 6. 쉬는 틈: 짜는 때와 풀린 때 (가만히 있을 때)
fig, ax = canvas(11.0, 3.0, 18.0, 4.8)
x = 0.6
for k in range(4):
    ax.add_patch(Rectangle((x, 2.0), 1.35, 1.2, fc="#f7e3de", ec=INK, lw=1))
    ax.add_patch(Rectangle((x + 1.35, 2.0), 2.15, 1.2, fc="white", ec=RED if k == 0 else INK,
                           lw=2.6 if k == 0 else 1))
    if k == 0:
        ax.text(x + 0.67, 3.7, "짜요", ha="center", va="center", fontsize=11, fontweight="bold")
        ax.text(x + 2.4, 3.7, "풀려요", ha="center", va="center", fontsize=11, color=RED, fontweight="bold")
    x += 3.5
arrow(ax, (0.6, 1.4), (14.6, 1.4), color=INK, lw=1.4)
ax.text(7.6, 0.8, "시간", ha="center", va="center", fontsize=10)
save(fig, "b05-rest.svg")

# 7. 맥박 찾기: 손목 엄지 쪽
fig, ax = canvas(9.0, 3.6, 14.0, 5.6)
ax.add_patch(FancyBboxPatch((1.0, 1.6), 9.0, 2.0, boxstyle="round,pad=0.5", fc=SKIN, ec=INK, lw=1.6))
ax.plot([1.6, 9.6], [2.2, 2.2], color="#d98b7e", lw=2, alpha=0.6)
for k in range(2):
    ax.add_patch(FancyBboxPatch((3.2 + k * 1.2, 1.9), 0.9, 2.4, boxstyle="round,pad=0.25", fc="#fbe7dc", ec=INK,
                                lw=1.4))
ax.text(4.25, 5.1, "검지와 가운뎃손가락", ha="center", va="center", fontsize=11)
ax.text(11.2, 2.6, "엄지 쪽", ha="left", va="center", fontsize=11, fontweight="bold")
arrow(ax, (11.1, 2.6), (10.2, 2.3), color=INK, lw=1.4, ms=12)
ax.text(5.5, 0.4, "톡, 톡, 톡", ha="center", va="center", fontsize=13, color=RED, fontweight="bold")
save(fig, "b05-pulse.svg")
