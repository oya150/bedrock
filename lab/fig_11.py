"""알고리즘 11편 그림 만들기. 실행: python lab/fig_11.py  → docs/algorithms/img/11/*.svg

글자는 SVG 안에 글자로 남긴다(글꼴 모양을 파일에 넣지 않는다). 보는 쪽 글꼴로 그려진다.
카드는 차분한 색으로, 강조(새로 받은 카드, 비교 화살표, 많이 든 일)만 빨강으로 칠한다.
"""
import itertools
import os

import matplotlib

matplotlib.use("svg")
import matplotlib.pyplot as plt
from matplotlib.patches import Arc, Circle, FancyArrowPatch, FancyBboxPatch, Rectangle

OUT = os.path.join(os.path.dirname(__file__), "..", "docs", "algorithms", "img", "11")
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


def crate(ax, x, y, w, h, label=None, hot=False, fs=9, fc=None):
    ax.add_patch(Rectangle((x, y), w, h, fc=fc or ("#fbe3dc" if hot else "#efe6d4"), ec=RED if hot else INK,
                           lw=2.0 if hot else 1.0))
    if label is not None:
        ax.text(x + w / 2, y + h / 2, str(label), ha="center", va="center", fontsize=fs,
                color=RED if hot else "#222", fontweight="bold" if hot else "normal")


# 1. 여는 장면: 책상과 먼 창고
fig, ax = canvas(11.6, 4.8, 19.0, 7.8)
kid(ax, 1.2, 0.8, 1.3)
ax.add_patch(Rectangle((2.2, 1.6), 3.0, 0.25, fc=INK, ec=INK))
ax.plot([2.4, 2.4], [0.6, 1.6], color=INK, lw=2)
ax.plot([5.0, 5.0], [0.6, 1.6], color=INK, lw=2)
crate(ax, 3.0, 1.85, 1.4, 1.0, "상자", fs=10)
ax.text(3.7, 0.2, "책상: 상자 하나만 놓여요", ha="center", va="center", fontsize=10)
ax.add_patch(Rectangle((11.0, 0.6), 7.6, 5.4, fc="white", ec=INK, lw=1.6))
ax.text(14.8, 6.4, "창고: 카드 500장이 상자 50개에", ha="center", va="center", fontsize=11, fontweight="bold")
for k in range(50):
    crate(ax, 11.3 + (k % 10) * 0.72, 4.9 - (k // 10) * 1.0, 0.62, 0.8, k + 1, fs=7)
arrow(ax, (5.6, 3.4), (10.8, 3.4), color=RED, lw=1.8, rad=-0.2)
arrow(ax, (10.8, 2.6), (5.6, 2.6), color=RED, lw=1.8, rad=-0.2)
ax.text(8.2, 4.6, "다녀오는 데 오래 걸려요", ha="center", va="center", fontsize=11, color=RED, fontweight="bold")
ax.text(8.2, 7.2, "카드 230은 몇 번 상자에 있을까?", ha="center", va="center", fontsize=12,
        bbox=dict(boxstyle="round,pad=0.4", fc="white", ec=INK, lw=1.2))
save(fig, "a11-warehouse.svg")

# 2. 이 편의 지도
fig, ax = canvas(13.6, 2.9, 24.2, 4.6)
titles = ["창고는 멀어요", "업다운으로 찾으면", "안내 상자", "안내 따라가기", "데이터베이스 색인"]
for i, t in enumerate(titles):
    x = 0.3 + i * 4.8
    box(ax, x, 0.4, 3.8, 3.6)
    ax.text(x + 1.9, 0.95, t, ha="center", va="center", fontsize=12, fontweight="bold")
    if i == 0:
        for k in range(8):
            crate(ax, x + 0.5 + (k % 4) * 0.7, 2.0 + (k // 4) * 0.7, 0.6, 0.55)
    elif i == 1:
        for k in range(6):
            crate(ax, x + 0.4 + k * 0.5, 2.2, 0.42, 0.6, hot=k in (1, 4))
        ax.text(x + 1.9, 3.3, "왔다 갔다", ha="center", va="center", fontsize=9, color=RED)
    elif i == 2:
        crate(ax, x + 1.5, 3.0, 0.8, 0.5, hot=True)
        for k in range(3):
            crate(ax, x + 0.5 + k * 1.0, 1.9, 0.8, 0.5)
            ax.plot([x + 1.9, x + 0.9 + k * 1.0], [3.0, 2.4], color=GREY, lw=1)
    elif i == 3:
        crate(ax, x + 1.5, 3.1, 0.8, 0.45, hot=True)
        crate(ax, x + 1.5, 2.4, 0.8, 0.45, hot=True)
        crate(ax, x + 1.5, 1.7, 0.8, 0.45, hot=True)
        for y in (3.1, 2.4):
            ax.plot([x + 1.9, x + 1.9], [y, y - 0.25], color=RED, lw=1.2)
    else:
        for r in range(3):
            ax.add_patch(Rectangle((x + 0.5, 1.7 + r * 0.55), 2.8, 0.45, fc=NOTE, ec=INK, lw=0.8))
        ax.text(x + 1.9, 3.5, "찾아보기", ha="center", va="center", fontsize=9)
    if i < 4:
        arrow(ax, (x + 3.95, 2.2), (x + 4.65, 2.2))
save(fig, "a11-map.svg")

# 3. 업다운으로 찾으면: 230 찾기, 상자 25, 13, 7, 10, 11, 12, 13 → 창고 7번
fig, ax = canvas(12.4, 4.8, 20.4, 7.8)
trips = [(25, 498), (13, 232), (7, 104), (10, 178), (11, 204), (12, 216), (13, 224)]
for k in range(50):
    hot = any(b == k + 1 for b, _ in trips)
    crate(ax, 0.3 + k * 0.4, 1.2, 0.34, 0.9, None, hot=hot)
for b in (1, 10, 20, 30, 40, 50):
    ax.text(0.3 + (b - 1) * 0.4 + 0.17, 0.85, str(b), ha="center", va="center", fontsize=8)
for n, (b, seen) in enumerate(trips):
    x = 0.3 + (b - 1) * 0.4 + 0.17
    y = 2.6 + n * 0.62
    ax.plot([x, x], [2.15, y - 0.15], color=RED, lw=0.8, ls=":")
    ax.text(x, y, f"{n + 1}번째: {b}번 상자({seen})", ha="center", va="center", fontsize=9, color=RED,
            bbox=dict(boxstyle="round,pad=0.2", fc="white", ec=RED, lw=0.8))
ax.text(10.2, 0.2, "상자 번호 1~50. 괄호 안은 그 상자에서 본 가운데 카드. 13번 상자는 두 번 가져왔어요", ha="center",
        va="center", fontsize=10)
save(fig, "a11-updown.svg")

# 4. 안내 상자 따라가기: 맨 위 → 가운데 2번 → 카드 상자 13번
fig, ax = canvas(12.4, 6.4, 20.4, 10.6)
TOP = [1, 191, 403, 605, 805]
MID = [191, 206, 224, 248, 265, 287, 312, 337, 360, 387]
LEAF = [224, 225, 227, 230, 232, 234, 236, 240, 244, 245]
ax.text(0.3, 9.9, "① 맨 위 안내 상자(쪽지 5장)", ha="left", va="center", fontsize=11, fontweight="bold", color=RED)
row(ax, 6.0, 9.2, TOP, cw=1.1, ch=1.0, gap=0.15, fs=11, hot=(1,))
ax.text(13.0, 9.7, "230은 191과 403 사이 → 가운데 안내 상자 2번", ha="left", va="center", fontsize=10)
ax.text(0.3, 6.6, "② 가운데 안내\n상자 2번(쪽지 10장)", ha="left", va="center", fontsize=11, fontweight="bold", color=RED)
row(ax, 4.6, 5.9, MID, cw=1.1, ch=1.0, gap=0.15, fs=11, hot=(2,))
ax.text(9.0, 5.4, "230은 224와 248 사이 → 카드 상자 13번", ha="left", va="center", fontsize=10)
ax.text(0.3, 3.3, "③ 카드 상자 13번", ha="left", va="center", fontsize=11, fontweight="bold", color=RED)
row(ax, 4.6, 2.6, LEAF, cw=1.1, ch=1.0, gap=0.15, fs=11, hot=(3,))
arrow(ax, (7.6, 9.1), (7.9, 7.0), color=RED, lw=1.6)
arrow(ax, (7.6, 5.8), (7.6, 3.7), color=RED, lw=1.6)
ax.text(10.2, 1.0, "창고에 3번 다녀오면 230을 찾아요", ha="center", va="center", fontsize=13, color=RED,
        fontweight="bold")
save(fig, "a11-guide.svg")

# 5. 창고 다녀오기 수
fig, ax = canvas(10.4, 5.0, 17.0, 8.2)
base, scale = 1.4, 5.6 / 9
for k, (name, v, col) in enumerate([("업다운\n(운이 나쁘면)", 9, GREY), ("업다운\n(230 찾기)", 7, GREY),
                                    ("안내 상자\n(늘)", 3, RED)]):
    bx = 2.0 + k * 4.6
    ax.add_patch(Rectangle((bx, base), 2.2, v * scale, fc=col, ec=INK, lw=1.2))
    ax.text(bx + 1.1, base + v * scale + 0.15, f"{v}번", ha="center", va="bottom", fontsize=13, fontweight="bold",
            color=RED if col == RED else "#222")
    ax.text(bx + 1.1, base - 0.25, name, ha="center", va="top", fontsize=11, fontweight="bold",
            color=RED if col == RED else "#222")
ax.plot([1.0, 16.0], [base, base], color=INK, lw=1.4)
ax.text(8.5, 7.8, "카드 500장, 상자 50개에서 카드 한 장 찾기: 창고 다녀오기 수", ha="center", va="center", fontsize=11)
save(fig, "a11-bars.svg")
