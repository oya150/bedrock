"""알고리즘 6편 그림 만들기. 실행: python lab/fig_06.py  → docs/algorithms/img/06/*.svg

글자는 SVG 안에 글자로 남긴다(글꼴 모양을 파일에 넣지 않는다). 보는 쪽 글꼴로 그려진다.
카드는 차분한 색으로, 강조(새로 받은 카드, 비교 화살표, 많이 든 일)만 빨강으로 칠한다.
"""
import os

import matplotlib

matplotlib.use("svg")
import matplotlib.pyplot as plt
from matplotlib.patches import Arc, Circle, FancyArrowPatch, FancyBboxPatch, Rectangle

OUT = os.path.join(os.path.dirname(__file__), "..", "docs", "algorithms", "img", "06")
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


# 1. 여는 장면: 5를 기준으로, 작은 카드는 왼쪽 큰 카드는 오른쪽
fig, ax = canvas(11.0, 4.8, 18.0, 7.8)
row(ax, 5.0, 6.0, [5, 2, 8, 7, 3, 6, 1, 4], cw=0.9, ch=1.1, hot=(0,))
row(ax, 0.6, 1.4, [2, 3, 1, 4], cw=1.0, ch=1.3, fs=13)
pivot_card(ax, 8.5, 1.4, 1.0, 1.3, 5, fs=13)
row(ax, 13.6, 1.4, [8, 7, 6], cw=1.0, ch=1.3, fs=13)
ax.text(2.6, 3.2, "5보다 작아요", ha="center", va="center", fontsize=12, fontweight="bold")
ax.text(9.0, 3.2, "기준", ha="center", va="center", fontsize=12, fontweight="bold", color=RED)
ax.text(15.2, 3.2, "5보다 커요", ha="center", va="center", fontsize=12, fontweight="bold")
arrow(ax, (7.5, 5.8), (4.0, 3.7), color=INK, lw=1.6, rad=0.15)
arrow(ax, (9.0, 5.8), (9.0, 3.6), color=RED, lw=1.8)
arrow(ax, (10.5, 5.8), (14.4, 3.7), color=INK, lw=1.6, rad=-0.15)
ax.text(17.4, 6.5, "?", ha="center", va="center", fontsize=34, color=RED, fontweight="bold")
save(fig, "a06-pivot.svg")

# 2. 이 편의 지도
fig, ax = canvas(13.6, 2.9, 24.2, 4.6)
titles = ["기준 카드로 나누기", "또 나누기", "4·5편과 나란히", "운이 나쁘면", "기준 잘 고르기"]
for i, t in enumerate(titles):
    x = 0.3 + i * 4.8
    box(ax, x, 0.4, 3.8, 3.6)
    ax.text(x + 1.9, 0.95, t, ha="center", va="center", fontsize=12, fontweight="bold")
    if i == 0:
        row(ax, x + 0.25, 2.3, [2, 3], cw=0.5, ch=0.6, fs=9)
        pivot_card(ax, x + 1.65, 2.3, 0.5, 0.6, 5, fs=9)
        row(ax, x + 2.5, 2.3, [8, 7], cw=0.5, ch=0.6, fs=9)
    elif i == 1:
        for lv, (cnt, w) in enumerate([(1, 2.8), (2, 1.3), (4, 0.55)]):
            for k in range(cnt):
                ax.add_patch(Rectangle((x + 0.5 + k * (w + 0.12), 3.3 - lv * 0.55), w, 0.38, fc=NOTE, ec=INK, lw=1))
    elif i == 2:
        for k, (v, col) in enumerate([(22, GREY), (15, GREY), (14, RED)]):
            ax.add_patch(Rectangle((x + 0.7 + k * 0.9, 1.5), 0.6, v / 22 * 1.9, fc=col, ec=INK, lw=1))
    elif i == 3:
        for k in range(5):
            ax.add_patch(Rectangle((x + 0.5 + k * 0.5, 3.3 - k * 0.38), 2.8 - k * 0.5, 0.3, fc=NOTE, ec=INK, lw=1))
    else:
        for k, (v, col) in enumerate([(120, GREY), (38, RED)]):
            ax.add_patch(Rectangle((x + 1.0 + k * 1.2, 1.5), 0.7, 0.1 + v / 120 * 1.9, fc=col, ec=INK, lw=1))
    if i < 4:
        arrow(ax, (x + 3.95, 2.2), (x + 4.65, 2.2))
save(fig, "a06-map.svg")

# 3. 첫 나누기: 5와 나머지 일곱 장을 한 번씩 비교 → 바둑돌 7개
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
end = split_row(ax, 3.0, 1.6, [2, 3, 1, 4], 5, [8, 7, 6], cw=1.2, ch=1.4, sep=0.9, fs=15)
ax.text(3.0 + 2.4, 1.1, "5보다 작은 카드", ha="center", va="top", fontsize=11)
px = 3.0 + 4 * 1.3 - 0.1 + 0.9
ax.text(px + 0.6, 3.4, "제자리", ha="center", va="center", fontsize=12, color=RED, fontweight="bold")
arrow(ax, (px + 0.6, 3.15), (px + 0.6, 3.05), color=RED, lw=1.6, ms=12)
ax.text(px + 1.2 + 0.9 + 1.9, 1.1, "5보다 큰 카드", ha="center", va="top", fontsize=11)
save(fig, "a06-split.svg")

# 4. 또 나누기: 줄마다 나눈 결과와 그때 놓은 바둑돌, 모두 14번
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


fig, ax = canvas(12.4, 7.6, 20.4, 12.4)
P = lambda n: ("p", n)
rows = [
    ("처음", [5, 2, 8, 7, 3, 6, 1, 4], 0, ""),
    ("1번째", [2, 3, 1, 4, "|", P(5), "|", 8, 7, 6], 7, "5로 7번"),
    ("2번째", [1, "|", P(2), "|", 3, 4, "|", P(5), "|", 7, 6, "|", P(8)], 5, "2로 3번, 8로 2번"),
    ("3번째", [1, "|", P(2), "|", P(3), "|", 4, "|", P(5), "|", 6, "|", P(7), "|", P(8)], 2, "3으로 1번, 7로 1번"),
]
for k, (name, tokens, n, note) in enumerate(rows):
    y = 10.6 - k * 2.3
    ax.text(0.1, y + 0.5, name, ha="left", va="center", fontsize=11, color=INK, fontweight="bold")
    seq(ax, 1.6, y, tokens)
    if n:
        stones(ax, 14.6, y + 0.75, n, color=RED)
        ax.text(14.45, y + 0.15, note, ha="left", va="center", fontsize=11, color=RED, fontweight="bold")
ax.text(10.2, 1.3, "7 + 5 + 2 = 비교 14번", ha="center", va="center", fontsize=13, color=RED, fontweight="bold")
ax.text(10.2, 0.4, "빨간 카드는 기준 카드예요. 기준 카드와 한 장만 남은 카드는 다시 움직이지 않아요.", ha="center", va="center",
        fontsize=11, color=INK)
save(fig, "a06-tree.svg")

# 5. 컴퓨터는 한 줄 안에서 바꿔요: 양 끝에서 다가오며 자리 바꾸기
fig, ax = canvas(11.6, 7.4, 19.0, 12.2)
cw, ch = 1.2, 1.2


def line(ax, y, nums, hot=(), piv=0, done=False):
    for k, n in enumerate(nums):
        x = 2.2 + k * 1.4
        if k == piv:
            pivot_card(ax, x, y, cw, ch, n, fs=14)
        else:
            card(ax, x, y, cw, ch, n, hot=(k in hot), fs=14)


def finger(ax, k, y, label):
    x = 2.2 + k * 1.4 + 0.6
    ax.annotate("", xy=(x, y - 0.05), xytext=(x, y - 0.75),
                arrowprops=dict(arrowstyle="-|>", color=RED, lw=1.8, mutation_scale=14))
    ax.text(x, y - 1.0, label, ha="center", va="center", fontsize=10, color=RED)


steps = [  # (이름, 줄, 손가락이 멈춘 자리(왼쪽 손가락, 오른쪽 손가락), 기준 위치, 설명)
    ("①", [5, 2, 8, 7, 3, 6, 1, 4], (2, 7), 0, "8과 4를 바꿔요"),
    ("②", [5, 2, 4, 7, 3, 6, 1, 8], (3, 6), 0, "7과 1을 바꿔요"),
    ("③", [5, 2, 4, 1, 3, 6, 7, 8], (5, 4), 0, "손가락이 지나쳤어요. 5와 3을 바꿔요"),
    ("끝", [3, 2, 4, 1, 5, 6, 7, 8], (), 4, "5가 제자리에 왔어요"),
]
for k, (name, nums, hot, piv, note) in enumerate(steps):
    y = 10.4 - k * 2.9
    ax.text(0.3, y + 0.6, name, ha="left", va="center", fontsize=13, color=INK, fontweight="bold")
    line(ax, y, nums, hot=hot, piv=piv)
    if k < 3:
        finger(ax, hot[0], y, "큰 카드")
        finger(ax, hot[1], y, "작은 카드")
    ax.text(13.6, y + 0.6, note, ha="left", va="center", fontsize=11, color=RED if k == 3 else "#222",
            fontweight="bold", wrap=True)
save(fig, "a06-inplace.svg")

# 6. 운이 나쁘면: 차례대로인 카드를 맨 앞 기준으로 → 한 장씩만 떨어져요
fig, ax = canvas(9.6, 7.4, 14.6, 12.0)
for k in range(8):
    y = 10.0 - k * 1.3
    x = 0.4 + k * 0.6
    toks = [("p", k + 1)] + list(range(k + 2, 9)) if k < 7 else [("p", 8)]
    seq(ax, x + k * 0.0, y, toks, cw=0.8, ch=0.95, gap=0.08)
    if k < 7:
        stones(ax, 9.2, y + 0.48, 7 - k, color=RED, r=0.14, gap=0.36)
        ax.text(8.9, y + 0.48, f"{7 - k}", ha="right", va="center", fontsize=11, color=RED, fontweight="bold")
ax.text(7.3, 0.4, "7 + 6 + 5 + 4 + 3 + 2 + 1 = 28번", ha="center", va="center", fontsize=13, color=RED,
        fontweight="bold")
ax.text(0.4, 11.6, "차례대로인 카드 8장, 맨 앞 카드가 기준", ha="left", va="center", fontsize=12, fontweight="bold")
save(fig, "a06-stairs.svg")

# 7. 기준을 잘 고르면: 막대 높이를 실제 비율대로
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
    ax.text(gx + 1.95, base - 1.0, f"차례대로인 카드 {n}장", ha="center", va="top", fontsize=12, fontweight="bold")
ax.plot([0.8, 16.4], [base, base], color=INK, lw=1.4)
save(fig, "a06-bars.svg")
