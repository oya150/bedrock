"""알고리즘 6편 그림 만들기. 실행: python lab/fig_06.py  → docs/algorithms/img/06/*.svg

글자는 SVG 안에 글자로 남긴다(글꼴 모양을 파일에 넣지 않는다). 보는 쪽 글꼴로 그려진다.
카드는 차분한 색으로, 강조(기준 카드, 지금 볼 곳)만 빨강으로 칠한다. 그림 안 글씨는 낱말과 숫자만 둔다.
확인용 PNG: FIG_FMT=png FIG_OUT=<폴더> python lab/fig_06.py
"""
import os

import matplotlib

matplotlib.use("svg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch, Rectangle

FMT = os.environ.get("FIG_FMT", "svg")
OUT = os.environ.get("FIG_OUT") or os.path.join(os.path.dirname(__file__), "..", "docs", "algorithms", "img", "06")
os.makedirs(OUT, exist_ok=True)

plt.rcParams.update({
    "font.family": ["Apple SD Gothic Neo", "Noto Sans KR", "Malgun Gothic", "sans-serif"],
    "svg.fonttype": "none",
    "text.color": "#222",
    "figure.facecolor": "white",
    "savefig.facecolor": "white",
})

RED, GREY, INK, NOTE = "#e4572e", "#c9ccd1", "#555", "#fffdf5"
LIGHT = "#e9ecef"


def save(fig, name):
    fig.savefig(os.path.join(OUT, f"{name}.{FMT}"), bbox_inches="tight", pad_inches=0.25, dpi=110)
    plt.close(fig)


def canvas(w, h, xmax, ymax):
    fig, ax = plt.subplots(figsize=(w, h))
    ax.set_xlim(0, xmax); ax.set_ylim(0, ymax); ax.axis("off")
    return fig, ax


def arrow(ax, a, b, color=INK, lw=2, rad=0.0, ms=18):
    ax.add_patch(FancyArrowPatch(a, b, arrowstyle="-|>", mutation_scale=ms, color=color, lw=lw,
                                 connectionstyle=f"arc3,rad={rad}"))


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


def pivot_card(ax, x, y, w, h, num, fs=12):
    ax.add_patch(Rectangle((x, y), w, h, fc=RED, ec=RED, lw=2.2))
    ax.text(x + w / 2, y + h / 2, str(num), ha="center", va="center", fontsize=fs, color="white", fontweight="bold")


def split_row(ax, x, y, left, pivot, right, cw=0.9, ch=1.1, gap=0.1, sep=0.5, fs=12):
    """[왼쪽 더미] 기준 [오른쪽 더미]를 한 줄로 그린다. 끝 x를 돌려준다."""
    if left:
        x = row(ax, x, y, left, cw=cw, ch=ch, gap=gap, fs=fs) + sep
    pivot_card(ax, x, y, cw, ch, pivot, fs=fs)
    x += cw + sep
    if right:
        x = row(ax, x, y, right, cw=cw, ch=ch, gap=gap, fs=fs)
    return x


def seq(ax, x, y, tokens, cw=0.9, ch=1.0, gap=0.1, sep=0.45, fs=12):
    """정수는 보통 카드, ("p", n)은 기준 카드, "|"는 더미 사이 틈."""
    for t in tokens:
        if t == "|":
            x += sep
        elif isinstance(t, tuple):
            pivot_card(ax, x, y, cw, ch, t[1], fs=fs); x += cw + gap
        else:
            card(ax, x, y, cw, ch, t, fs=fs); x += cw + gap
    return x


P = lambda n: ("p", n)


def tree_fig(name, rows, total):
    """줄마다 나눈 결과와 그때 놓은 바둑돌."""
    fig, ax = canvas(12.4, 7.0, 20.4, 11.4)
    for k, (label, tokens, n, note) in enumerate(rows):
        y = 9.6 - k * 2.3
        ax.text(0.1, y + 0.5, label, ha="left", va="center", fontsize=11, color=INK, fontweight="bold")
        seq(ax, 1.6, y, tokens)
        if n:
            stones(ax, 14.6, y + 0.75, n, color=RED)
            ax.text(14.45, y + 0.15, note, ha="left", va="center", fontsize=11, color=RED, fontweight="bold")
    ax.text(10.2, 0.6, total, ha="center", va="center", fontsize=13, color=RED, fontweight="bold")
    save(fig, name)


# 1. 첫 나누기: 5와 나머지 일곱 장을 한 번씩 비교 → 바둑돌 7개, 5는 제자리
fig, ax = canvas(11.6, 5.4, 19.0, 8.8)
pivot_card(ax, 0.4, 6.6, 1.2, 1.4, 5, fs=15)
ax.text(1.0, 6.2, "기준", ha="center", va="center", fontsize=11, color=RED, fontweight="bold")
rest = [2, 8, 7, 3, 6, 1, 4]
for k, n in enumerate(rest):
    x = 3.4 + k * 2.1
    card(ax, x, 6.6, 1.2, 1.4, n, fs=15)
    ax.text(x + 0.6, 5.85, "작아요" if n < 5 else "커요", ha="center", va="center", fontsize=11,
            color=INK if n < 5 else "#222", fontweight="bold")
    ax.add_patch(Circle((x + 0.6, 5.2), 0.18, fc=RED, ec=RED))
ax.text(18.6, 5.2, "비교 7번", ha="right", va="center", fontsize=12, color=RED, fontweight="bold")
ax.plot([0.3, 18.7], [4.4, 4.4], color=GREY, lw=1.2, ls="--")
split_row(ax, 3.0, 1.6, [2, 3, 1, 4], 5, [8, 7, 6], cw=1.2, ch=1.4, sep=0.9, fs=15)
ax.text(3.0 + 2.4, 1.1, "5보다 작은 카드", ha="center", va="top", fontsize=11)
px = 3.0 + 4 * 1.3 - 0.1 + 0.9
ax.text(px + 0.6, 3.4, "제자리", ha="center", va="center", fontsize=12, color=RED, fontweight="bold")
arrow(ax, (px + 0.6, 3.15), (px + 0.6, 3.05), color=RED, lw=1.6, ms=12)
ax.text(px + 1.2 + 0.9 + 1.9, 1.1, "5보다 큰 카드", ha="center", va="top", fontsize=11)
save(fig, "a06-split")

# 2. 또 나누기: 맨 앞 기준, 모두 14번
tree_fig("a06-tree", [
    ("처음", [5, 2, 8, 7, 3, 6, 1, 4], 0, ""),
    ("1번째", [2, 3, 1, 4, "|", P(5), "|", 8, 7, 6], 7, "5로 7번"),
    ("2번째", [1, "|", P(2), "|", 3, 4, "|", P(5), "|", 7, 6, "|", P(8)], 5, "2로 3번, 8로 2번"),
    ("3번째", [1, "|", P(2), "|", P(3), "|", 4, "|", P(5), "|", 6, "|", P(7), "|", P(8)], 2, "3으로 1번, 7로 1번"),
], "7 + 5 + 2 = 14번")

# 3. 컴퓨터는 한 줄 안에서 바꿔요: 양 끝에서 다가오며 자리 바꾸기
fig, ax = canvas(11.6, 7.4, 19.0, 12.2)
CW, CH = 1.2, 1.2


def line(ax, y, nums, hot=(), piv=0):
    for k, n in enumerate(nums):
        x = 2.2 + k * 1.4
        if k == piv:
            pivot_card(ax, x, y, CW, CH, n, fs=14)
        else:
            card(ax, x, y, CW, CH, n, hot=(k in hot), fs=14)


def finger(ax, k, y, label):
    x = 2.2 + k * 1.4 + 0.6
    ax.annotate("", xy=(x, y - 0.05), xytext=(x, y - 0.75),
                arrowprops=dict(arrowstyle="-|>", color=RED, lw=1.8, mutation_scale=14))
    ax.text(x, y - 1.0, label, ha="center", va="center", fontsize=10, color=RED)


steps = [  # (이름, 줄, 손가락이 멈춘 자리(왼쪽 손가락, 오른쪽 손가락), 기준 위치, 설명)
    ("①", [5, 2, 8, 7, 3, 6, 1, 4], (2, 7), 0, "8 ↔ 4"),
    ("②", [5, 2, 4, 7, 3, 6, 1, 8], (3, 6), 0, "7 ↔ 1"),
    ("③", [5, 2, 4, 1, 3, 6, 7, 8], (5, 4), 0, "지나침, 5 ↔ 3"),
    ("끝", [3, 2, 4, 1, 5, 6, 7, 8], (), 4, "5 제자리"),
]
for k, (name, nums, hot, piv, note) in enumerate(steps):
    y = 10.4 - k * 2.9
    ax.text(0.3, y + 0.6, name, ha="left", va="center", fontsize=13, color=INK, fontweight="bold")
    line(ax, y, nums, hot=hot, piv=piv)
    if k < 3:
        finger(ax, hot[0], y, "큰 카드")
        finger(ax, hot[1], y, "작은 카드")
    ax.text(13.6, y + 0.6, note, ha="left", va="center", fontsize=12, color=RED if k == 3 else "#222",
            fontweight="bold")
save(fig, "a06-inplace")

# 4. 운이 나쁘면: 차례대로인 카드를 맨 앞 기준으로 → 한 장씩만 떨어져요
fig, ax = canvas(9.6, 7.4, 14.6, 12.0)
for k in range(8):
    y = 10.0 - k * 1.3
    x = 0.4 + k * 0.6
    toks = [("p", k + 1)] + list(range(k + 2, 9)) if k < 7 else [("p", 8)]
    seq(ax, x, y, toks, cw=0.8, ch=0.95, gap=0.08)
    if k < 7:
        stones(ax, 9.2, y + 0.48, 7 - k, color=RED, r=0.14, gap=0.36)
        ax.text(8.9, y + 0.48, f"{7 - k}", ha="right", va="center", fontsize=11, color=RED, fontweight="bold")
ax.text(7.3, -0.2, "7 + 6 + 5 + 4 + 3 + 2 + 1 = 28번", ha="center", va="center", fontsize=13, color=RED,
        fontweight="bold")
ax.text(0.4, 11.6, "차례대로 8장, 맨 앞 기준", ha="left", va="center", fontsize=12, fontweight="bold")
save(fig, "a06-stairs")

# 5. 가운데 기준으로 차례대로인 카드 나누기: 모두 13번
tree_fig("a06-middle", [
    ("처음", [1, 2, 3, 4, 5, 6, 7, 8], 0, ""),
    ("1번째", [1, 2, 3, "|", P(4), "|", 5, 6, 7, 8], 7, "4로 7번"),
    ("2번째", [1, "|", P(2), "|", 3, "|", P(4), "|", 5, "|", P(6), "|", 7, 8], 5, "2로 2번, 6으로 3번"),
    ("3번째", [1, "|", P(2), "|", 3, "|", P(4), "|", 5, "|", P(6), "|", P(7), "|", 8], 1, "7로 1번"),
], "7 + 5 + 1 = 13번")

# 6. 기준을 잘 고르면: 막대 높이를 실제 비율대로
fig, ax = canvas(10.4, 5.6, 17.0, 9.2)
base = 1.4
scale = 6.6 / 120
for k, (n, a, b) in enumerate([(8, 28, 13), (16, 120, 38)]):
    gx = 2.0 + k * 7.0
    for j, (v, col) in enumerate([(a, GREY), (b, RED)]):
        bx = gx + j * 2.2
        h = v * scale
        ax.add_patch(Rectangle((bx, base), 1.7, h, fc=col, ec=INK, lw=1.2))
        ax.text(bx + 0.85, base + h + 0.15, f"{v}번", ha="center", va="bottom", fontsize=12, fontweight="bold",
                color=RED if col == RED else "#222")
        ax.text(bx + 0.85, base - 0.3, "맨 앞 기준" if j == 0 else "가운데 기준", ha="center", va="top", fontsize=11,
                color=RED if col == RED else "#222", fontweight="bold")
    ax.text(gx + 1.95, base - 1.0, f"차례대로 {n}장", ha="center", va="top", fontsize=12, fontweight="bold")
ax.plot([0.8, 16.4], [base, base], color=INK, lw=1.4)
save(fig, "a06-bars")
