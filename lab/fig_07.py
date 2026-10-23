"""알고리즘 7편 그림 만들기. 실행: python lab/fig_07.py  → docs/algorithms/img/07/*.svg

글자는 SVG 안에 글자로 남긴다(글꼴 모양을 파일에 넣지 않는다). 보는 쪽 글꼴로 그려진다.
카드는 차분한 색으로, 강조(새로 받은 카드, 비교 화살표, 많이 든 일)만 빨강으로 칠한다.
"""
import os

import matplotlib

matplotlib.use("svg")
import matplotlib.pyplot as plt
from matplotlib.patches import Arc, Circle, FancyArrowPatch, FancyBboxPatch, Rectangle

OUT = os.path.join(os.path.dirname(__file__), "..", "docs", "algorithms", "img", "07")
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



def dots(ax, x, y, w=0.9, h=1.1, fs=14, color=INK):
    ax.text(x + w / 2, y + h / 2, "…", ha="center", va="center", fontsize=fs, color=color)
    return x + w + 0.1


def run_box(ax, x0, x1, y, h, color, label=None, fs=11):
    ax.add_patch(FancyBboxPatch((x0 - 0.12, y - 0.12), x1 - x0 + 0.24, h + 0.24, boxstyle="round,pad=0.05",
                                fc="none", ec=color, lw=2.4))
    if label:
        ax.text((x0 + x1) / 2, y + h + 0.45, label, ha="center", va="center", fontsize=fs, color=color,
                fontweight="bold")


ODD = list(range(1, 65, 2))
EVEN = list(range(2, 65, 2))


def friends_row(ax, x, y, cw=0.8, ch=1.0, fs=11, labels=True):
    """홀수 줄 1, 3, 5, …, 63 다음에 짝수 줄 2, 4, 6, …, 64를 이어 놓은 64장."""
    x0 = x
    x = row(ax, x, y, [1, 3, 5], cw=cw, ch=ch, fs=fs) + 0.1
    x = dots(ax, x, y, w=cw, h=ch)
    x = row(ax, x, y, [63], cw=cw, ch=ch, fs=fs)
    run_box(ax, x0, x, y, ch, RED, "홀수 32장 줄" if labels else None)
    x += 0.5
    x1 = x
    x = row(ax, x, y, [2, 4, 6], cw=cw, ch=ch, fs=fs) + 0.1
    x = dots(ax, x, y, w=cw, h=ch)
    x = row(ax, x, y, [64], cw=cw, ch=ch, fs=fs)
    run_box(ax, x1, x, y, ch, BLUE, "짝수 32장 줄" if labels else None)
    return x0, x1 - 0.5, x1, x


# 1. 여는 장면: 친구 둘이 정리한 카드를 이어 놓았다. 파이썬은 먼저 무엇을 볼까?
fig, ax = canvas(11.0, 4.8, 18.0, 7.8)
kid(ax, 1.4, 2.6, 1.4)
ax.text(1.4, 1.9, "나", ha="center", va="center", fontsize=12, fontweight="bold")
row(ax, 3.4, 5.6, [1, 3, 5], cw=0.8, ch=1.0)
dots(ax, 5.8, 5.6, w=0.8, h=1.0)
row(ax, 6.7, 5.6, [63], cw=0.8, ch=1.0)
ax.text(5.5, 7.2, "친구 1이 정리한 홀수 카드", ha="center", va="center", fontsize=11, fontweight="bold")
row(ax, 10.6, 5.6, [2, 4, 6], cw=0.8, ch=1.0)
dots(ax, 13.0, 5.6, w=0.8, h=1.0)
row(ax, 13.9, 5.6, [64], cw=0.8, ch=1.0)
ax.text(12.7, 7.2, "친구 2가 정리한 짝수 카드", ha="center", va="center", fontsize=11, fontweight="bold")
arrow(ax, (5.5, 5.4), (7.3, 3.4), color=INK, lw=1.6, rad=0.15)
arrow(ax, (12.7, 5.4), (10.9, 3.4), color=INK, lw=1.6, rad=-0.15)
friends_row(ax, 3.4, 1.6, labels=False)
ax.text(9.1, 0.9, "그냥 이어 놓은 카드 64장", ha="center", va="center", fontsize=11)
ax.text(17.3, 2.1, "?", ha="center", va="center", fontsize=34, color=RED, fontweight="bold")
save(fig, "a07-friends.svg")

# 2. 이 편의 지도
fig, ax = canvas(13.6, 2.9, 24.2, 4.6)
titles = ["이어진 줄 찾기", "거꾸로 줄 뒤집기", "줄 둘 합치기", "짧은 줄 늘리기", "뒤죽박죽이면"]
for i, t in enumerate(titles):
    x = 0.3 + i * 4.8
    box(ax, x, 0.4, 3.8, 3.6)
    ax.text(x + 1.9, 0.95, t, ha="center", va="center", fontsize=12, fontweight="bold")
    if i == 0:
        row(ax, x + 0.4, 2.3, [1, 2, 3, 4], cw=0.5, ch=0.6, fs=9)
        stones(ax, x + 0.95, 3.2, 3, color=RED, r=0.09, gap=0.6)
    elif i == 1:
        row(ax, x + 0.4, 2.9, [4, 3, 2, 1], cw=0.5, ch=0.6, fs=9)
        row(ax, x + 0.4, 1.7, [1, 2, 3, 4], cw=0.5, ch=0.6, fs=9, hot=range(4))
        arrow(ax, (x + 3.2, 3.1), (x + 3.2, 2.0), color=RED, lw=1.4, rad=-0.5, ms=10)
    elif i == 2:
        for k, col in enumerate([RED, BLUE]):
            ax.add_patch(Rectangle((x + 0.4 + k * 1.6, 2.9), 1.4, 0.5, fc=NOTE, ec=col, lw=1.8))
        ax.add_patch(Rectangle((x + 0.4, 1.7), 3.0, 0.5, fc=NOTE, ec=INK, lw=1.2))
    elif i == 3:
        row(ax, x + 0.4, 2.9, [3, 7], cw=0.5, ch=0.6, fs=9)
        row(ax, x + 1.8, 2.9, [5], cw=0.5, ch=0.6, fs=9, hot=(0,))
        row(ax, x + 0.4, 1.7, [3, 5, 7], cw=0.5, ch=0.6, fs=9)
    else:
        for k, (v, col) in enumerate([(307, GREY), (306, RED)]):
            ax.add_patch(Rectangle((x + 1.0 + k * 1.2, 1.5), 0.7, v / 307 * 1.9, fc=col, ec=INK, lw=1))
    if i < 4:
        arrow(ax, (x + 3.95, 2.2), (x + 4.65, 2.2))
save(fig, "a07-map.svg")


def neighbor_stones(ax, x, y, n, cw, gap, ch):
    for k in range(n - 1):
        cx = x + k * (cw + gap) + cw + gap / 2
        ax.add_patch(Circle((cx, y + ch + 0.35), 0.15, fc=RED, ec=RED))


# 3. 이미 차례대로: 이웃끼리 7번 비교하면 끝
fig, ax = canvas(10.4, 3.4, 17.0, 5.6)
cw, gap = 1.3, 0.55
row(ax, 0.8, 1.8, list(range(1, 9)), cw=cw, ch=1.4, gap=gap, fs=15)
neighbor_stones(ax, 0.8, 1.8, 8, cw, gap, 1.4)
ax.text(0.8, 4.4, "이웃한 두 장마다 바둑돌 하나: 1과 2, 2와 3, … 7과 8", ha="left", va="center", fontsize=11)
ax.text(8.5, 0.8, "비교 7번. 처음부터 끝까지 이어진 줄이에요. 끝!", ha="center", va="center", fontsize=13,
        color=RED, fontweight="bold")
save(fig, "a07-asc.svg")

# 4. 거꾸로 이어진 줄: 7번 비교하고 통째로 뒤집기
fig, ax = canvas(10.4, 6.0, 17.0, 9.8)
row(ax, 0.8, 6.6, list(range(8, 0, -1)), cw=cw, ch=1.4, gap=gap, fs=15)
neighbor_stones(ax, 0.8, 6.6, 8, cw, gap, 1.4)
ax.text(0.8, 9.2, "이웃끼리 비교하면 계속 작아져요. 비교 7번", ha="left", va="center", fontsize=11)
for k in range(4):
    a = 0.8 + k * (cw + gap) + cw / 2
    b = 0.8 + (7 - k) * (cw + gap) + cw / 2
    ax.add_patch(FancyArrowPatch((a, 6.4), (b, 6.4), arrowstyle="<|-|>", mutation_scale=12, color=RED, lw=1.4,
                                 connectionstyle=f"arc3,rad={0.25 + k * 0.08}"))
ax.text(8.5, 3.9, "양 끝부터 맞바꿔 통째로 뒤집어요", ha="center", va="center", fontsize=12, color=RED,
        fontweight="bold")
row(ax, 0.8, 1.6, list(range(1, 9)), cw=cw, ch=1.4, gap=gap, fs=15, hot=range(8))
ax.text(8.5, 0.6, "모두 7번 (4편 방법은 28번)", ha="center", va="center", fontsize=13, color=RED, fontweight="bold")
save(fig, "a07-desc.svg")

# 5. 줄 둘을 찾아 합치기 (64장)
fig, ax = canvas(11.6, 5.4, 19.0, 8.8)
a0, a1, b0, b1 = friends_row(ax, 0.8, 6.0)
ax.text(a1 + 0.25, 5.3, "여기서 끊겼어요(63 다음 2)", ha="center", va="center", fontsize=10, color=INK)
arrow(ax, ((a0 + a1) / 2, 5.6), (5.0, 3.6), color=RED, lw=1.6, rad=0.1)
arrow(ax, ((b0 + b1) / 2, 5.6), (7.6, 3.6), color=BLUE, lw=1.6, rad=-0.1)
x = row(ax, 2.4, 2.0, [1, 2, 3, 4, 5], cw=0.8, ch=1.0, fs=11) + 0.1
x = dots(ax, x, 2.0, w=0.8, h=1.0)
row(ax, x, 2.0, [63, 64], cw=0.8, ch=1.0, fs=11)
ax.text(6.0, 1.2, "5편처럼 맨 앞끼리 비교하며 합쳐요", ha="center", va="center", fontsize=11, color=RED,
        fontweight="bold")
base, scale = 1.0, 5.6 / 559
for k, (name, v, col) in enumerate([("4편 방법", 559, GREY), ("5편 방법", 223, GREY), ("팀 정렬", 126, RED)]):
    bx = 12.6 + k * 2.1
    ax.add_patch(Rectangle((bx, base), 1.5, v * scale, fc=col, ec=INK, lw=1.2))
    ax.text(bx + 0.75, base + v * scale + 0.15, f"{v}번", ha="center", va="bottom", fontsize=12, fontweight="bold",
            color=RED if col == RED else "#222")
    ax.text(bx + 0.75, base - 0.3, name, ha="center", va="top", fontsize=11, fontweight="bold",
            color=RED if col == RED else "#222")
save(fig, "a07-merge.svg")

# 6. 짧은 줄은 끼워서 늘려요
fig, ax = canvas(10.4, 4.6, 17.0, 7.6)
ax.text(0.5, 7.0, "뒤죽박죽 카드: 이어진 줄이 짧아요", ha="left", va="center", fontsize=12, fontweight="bold")
row(ax, 0.8, 4.8, [3, 7], cw=1.2, ch=1.4, fs=15)
run_box(ax, 0.8, 0.8 + 2.5, 4.8, 1.4, RED)
row(ax, 4.6, 4.8, [5, 1, 9], cw=1.2, ch=1.4, fs=15, hot=range(3))
ax.text(5.0 + 1.9, 6.6, "한 장씩 끼워 넣어요", ha="center", va="center", fontsize=11, color=RED, fontweight="bold")
arrow(ax, (8.6, 5.5), (10.4, 5.5), color=INK, lw=1.8)
row(ax, 10.8, 4.8, [1, 3, 5, 7, 9], cw=1.0, ch=1.4, fs=14)
run_box(ax, 10.8, 10.8 + 5 * 1.1 - 0.1, 4.8, 1.4, RED)
ax.text(8.5, 2.6, "한 장씩 끼워서 줄을 길게 만든 다음", ha="center", va="center", fontsize=12)
ax.text(8.5, 1.6, "긴 줄끼리 5편처럼 합쳐요", ha="center", va="center", fontsize=12, color=RED, fontweight="bold")
save(fig, "a07-extend.svg")

# 7. 비교 수: 5편 방법 vs 팀 정렬 (막대 높이는 실제 비율대로)
fig, ax = canvas(10.4, 5.6, 17.0, 9.2)
base = 1.4
scale = 6.6 / 307
for k, (name, a, b) in enumerate([("친구 둘이 정리한 카드 64장", 223, 126), ("뒤죽박죽 카드 64장", 307, 306)]):
    gx = 2.0 + k * 7.0
    for j, (v, col) in enumerate([(a, GREY), (b, RED)]):
        bx = gx + j * 2.2
        h = v * scale
        ax.add_patch(Rectangle((bx, base), 1.7, h, fc=col, ec=INK, lw=1.2))
        ax.text(bx + 0.85, base + h + 0.15, f"{v}번", ha="center", va="bottom", fontsize=12, fontweight="bold",
                color=RED if col == RED else "#222")
        ax.text(bx + 0.85, base - 0.3, "5편 방법" if j == 0 else "팀 정렬", ha="center", va="top", fontsize=11,
                color=RED if col == RED else "#222", fontweight="bold")
    ax.text(gx + 1.95, base - 1.0, name, ha="center", va="top", fontsize=12, fontweight="bold")
ax.plot([0.8, 16.4], [base, base], color=INK, lw=1.4)
save(fig, "a07-bars.svg")
