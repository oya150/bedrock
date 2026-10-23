"""알고리즘 8편 그림 만들기. 실행: python lab/fig_08.py  → docs/algorithms/img/08/*.svg

글자는 SVG 안에 글자로 남긴다(글꼴 모양을 파일에 넣지 않는다). 보는 쪽 글꼴로 그려진다.
카드는 차분한 색으로, 강조(새로 받은 카드, 비교 화살표, 많이 든 일)만 빨강으로 칠한다.
"""
import itertools
import os

import matplotlib

matplotlib.use("svg")
import matplotlib.pyplot as plt
from matplotlib.patches import Arc, Circle, FancyArrowPatch, FancyBboxPatch, Rectangle

OUT = os.path.join(os.path.dirname(__file__), "..", "docs", "algorithms", "img", "08")
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



def back(ax, x, y, w, h, label, fs=14):
    """뒤집어 놓은 카드. 뒷면에 글자만 보인다."""
    ax.add_patch(Rectangle((x, y), w, h, fc=BLUE, ec=INK, lw=1.4))
    ax.text(x + w / 2, y + h / 2, label, ha="center", va="center", fontsize=fs, color="white", fontweight="bold")


def bubble(ax, x, y, text, fs=11, color="#222"):
    ax.text(x, y, text, ha="center", va="center", fontsize=fs, color=color,
            bbox=dict(boxstyle="round,pad=0.4", fc="white", ec=INK, lw=1.2))


# 1. 여는 장면: 뒤집은 카드 세 장, 물을 수 있는 건 "작아?"뿐
fig, ax = canvas(11.0, 4.6, 18.0, 7.6)
kid(ax, 1.4, 0.6, 1.4)
ax.text(1.4, 0.1, "나", ha="center", va="center", fontsize=12, fontweight="bold")
kid(ax, 16.6, 0.6, 1.4)
ax.text(16.6, 0.1, "친구", ha="center", va="center", fontsize=12, fontweight="bold")
for k, lab in enumerate("가나다"):
    back(ax, 6.2 + k * 2.0, 1.2, 1.5, 2.0, lab, fs=18)
bubble(ax, 5.2, 5.6, "가 카드가 나 카드보다 작아?", fs=12)
bubble(ax, 13.6, 5.6, "응!", fs=12, color=RED)
ax.text(9.0, 4.0, "?", ha="center", va="center", fontsize=30, color=RED, fontweight="bold")
save(fig, "a08-guess.svg")

# 2. 이 편의 지도
fig, ax = canvas(13.6, 2.9, 24.2, 4.6)
titles = ["순서 세기", "비교 한 번은 반씩", "넘을 수 없는 벽", "상자에 나눠 담기", "상자가 너무 많으면"]
for i, t in enumerate(titles):
    x = 0.3 + i * 4.8
    box(ax, x, 0.4, 3.8, 3.6)
    ax.text(x + 1.9, 0.95, t, ha="center", va="center", fontsize=12, fontweight="bold")
    if i == 0:
        for r, p in enumerate([(1, 2, 3), (1, 3, 2), (2, 1, 3)]):
            row(ax, x + 0.9, 3.15 - r * 0.55, p, cw=0.42, ch=0.45, gap=0.08, fs=8)
    elif i == 1:
        for r, w in enumerate([2.8, 1.4, 0.7]):
            ax.add_patch(Rectangle((x + 0.5, 3.2 - r * 0.55), w, 0.38, fc=NOTE if r else GREY, ec=INK, lw=1))
    elif i == 2:
        ax.add_patch(Rectangle((x + 1.7, 1.5), 0.35, 2.2, fc=RED, ec=INK, lw=1))
        arrow(ax, (x + 0.4, 2.6), (x + 1.6, 2.6), color=INK, lw=1.4, ms=12)
    elif i == 3:
        for k in range(3):
            ax.add_patch(Rectangle((x + 0.5 + k * 1.0, 1.8), 0.8, 0.9, fc="white", ec=INK, lw=1.2))
            ax.text(x + 0.9 + k * 1.0, 3.2, str(k + 1), ha="center", va="center", fontsize=9)
            card(ax, x + 0.65 + k * 1.0, 1.95, 0.5, 0.55, k + 1, hot=True, fs=8)
    else:
        for k in range(10):
            ax.add_patch(Rectangle((x + 0.35 + k * 0.32, 2.2), 0.26, 0.6, fc="white", ec=INK, lw=0.8))
        ax.text(x + 1.9, 3.3, "…", ha="center", va="center", fontsize=14)
    if i < 4:
        arrow(ax, (x + 3.95, 2.2), (x + 4.65, 2.2))
save(fig, "a08-map.svg")

# 3. 카드 세 장은 순서가 6가지
fig, ax = canvas(9.0, 4.6, 14.0, 7.2)
for r, p in enumerate(itertools.permutations([1, 2, 3])):
    cx = 1.0 + (r % 3) * 4.4
    cy = 4.2 - (r // 3) * 2.6
    row(ax, cx, cy, p, cw=1.0, ch=1.3, gap=0.15, fs=14, hot=range(3) if p == (1, 2, 3) else ())
ax.text(7.0, 0.5, "카드 1, 2, 3이 놓일 수 있는 순서는 6가지. 그중 정렬된 것은 하나(빨강)", ha="center",
        va="center", fontsize=11)
save(fig, "a08-orders.svg")

# 4. 세 장 나무: 비교 한 번마다 남은 순서가 반쯤으로
fig, ax = canvas(13.6, 7.2, 20.0, 12.0)
ax.set_xlim(-3.8, 20.6)


def node(ax, x, y, text, color=INK):
    ax.text(x, y, text, ha="center", va="center", fontsize=10, color="#222",
            bbox=dict(boxstyle="round,pad=0.4", fc=NOTE, ec=color, lw=1.6))


def leaf(ax, x, y, text):
    ax.text(x, y, text, ha="center", va="center", fontsize=12, color=RED, fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.35", fc="#fbe3dc", ec=RED, lw=1.6))


def edge(ax, a, b, label):
    ax.plot([a[0], b[0]], [a[1], b[1]], color=INK, lw=1.4)
    ax.text((a[0] + b[0]) / 2 + (0.35 if b[0] > a[0] else -0.35), (a[1] + b[1]) / 2 + 0.1, label,
            ha="center", va="center", fontsize=10, color=INK)


node(ax, 10.0, 10.8, "가가 나보다 작아?")
node(ax, 5.0, 8.2, "나가 다보다 작아?")
node(ax, 15.0, 8.2, "가가 다보다 작아?")
edge(ax, (10.0, 10.4), (5.0, 8.6), "응")
edge(ax, (10.0, 10.4), (15.0, 8.6), "아니")
leaf(ax, 2.4, 5.4, "가 나 다")
node(ax, 7.4, 5.4, "가가 다보다 작아?")
edge(ax, (5.0, 7.8), (2.4, 5.8), "응")
edge(ax, (5.0, 7.8), (7.4, 5.8), "아니")
leaf(ax, 12.6, 5.4, "나 가 다")
node(ax, 17.6, 5.4, "나가 다보다 작아?")
edge(ax, (15.0, 7.8), (12.6, 5.8), "응")
edge(ax, (15.0, 7.8), (17.6, 5.8), "아니")
leaf(ax, 5.9, 2.6, "가 다 나")
leaf(ax, 8.9, 2.6, "다 가 나")
edge(ax, (7.4, 5.0), (5.9, 3.0), "응")
edge(ax, (7.4, 5.0), (8.9, 3.0), "아니")
leaf(ax, 16.1, 2.6, "나 다 가")
leaf(ax, 19.1, 2.6, "다 나 가")
edge(ax, (17.6, 5.0), (16.1, 3.0), "응")
edge(ax, (17.6, 5.0), (19.1, 3.0), "아니")
for y, t in [(10.8, "남은 순서 6가지"), (8.2, "3가지씩"), (5.4, "1가지 또는 2가지"), (2.6, "1가지")]:
    ax.text(-3.7, y, t, ha="left", va="center", fontsize=10, color=INK)
ax.text(10.0, 0.9, "빨간 칸은 작은 카드부터 적은 이름이에요. 가 다 나는 가가 제일 작고 다, 나 차례라는 뜻. 어느 길로 가도 질문 세 번 안에 끝나요.", ha="center",
        va="center", fontsize=11)
save(fig, "a08-tree.svg")

# 5. 네 장: 24가지 → 12 → 6 → 3 → 2 → 1, 비교 5번
fig, ax = canvas(10.4, 4.8, 17.0, 7.8)
vals = [24, 12, 6, 3, 2, 1]
for k, v in enumerate(vals):
    y = 6.8 - k * 1.1
    ax.add_patch(Rectangle((2.6, y), v * 0.5, 0.7, fc=RED if v == 1 else NOTE, ec=INK, lw=1.2))
    ax.text(2.3, y + 0.35, f"{v}가지", ha="right", va="center", fontsize=11, fontweight="bold")
    if k:
        ax.add_patch(Circle((15.6, y + 0.35), 0.18, fc=RED, ec=RED))
        ax.text(15.2, y + 0.35, f"{k}번째 비교", ha="right", va="center", fontsize=10, color=RED)
ax.text(8.5, 0.2, "카드 네 장: 순서 24가지를 반씩 줄이면 비교 5번", ha="center", va="center", fontsize=12,
        color=RED, fontweight="bold")
save(fig, "a08-halving.svg")

# 6. 상자에 나눠 담기: 숫자 1~5뿐인 카드 20장
DECK = [2, 3, 4, 2, 2, 1, 1, 2, 2, 5, 2, 4, 1, 4, 4, 4, 4, 4, 5, 2]
fig, ax = canvas(11.6, 7.0, 19.0, 11.4)
for k, v in enumerate(DECK):
    card(ax, 0.4 + k * 0.92, 10.0, 0.8, 0.95, v, fs=10)
ax.text(9.5, 9.4, "숫자가 1~5뿐인 카드 20장", ha="center", va="center", fontsize=11)
counts = [DECK.count(v) for v in range(1, 6)]
for b in range(5):
    bx = 1.0 + b * 3.6
    ax.add_patch(Rectangle((bx, 3.2), 2.8, 4.6, fc="white", ec=INK, lw=1.6))
    ax.text(bx + 1.4, 8.2, f"{b + 1}번 상자", ha="center", va="center", fontsize=11, fontweight="bold")
    for j in range(counts[b]):
        card(ax, bx + 0.9, 3.4 + j * 0.6, 1.0, 0.5, b + 1, hot=True, fs=8)
    ax.text(bx + 1.4, 2.8, f"{counts[b]}장", ha="center", va="center", fontsize=10)
ax.text(9.5, 1.8, "카드마다 제 번호 상자에 넣기만 해요. 비교 0번", ha="center", va="center", fontsize=12,
        color=RED, fontweight="bold")
ax.text(9.5, 0.9, "1번 상자부터 차례로 꺼내면 정렬 끝: 1, 1, 1, 2, 2, … 5, 5", ha="center", va="center", fontsize=11)
save(fig, "a08-boxes.svg")

# 7. 상자가 너무 많으면: 카드 3장에 상자 1,000개
fig, ax = canvas(11.6, 3.8, 19.0, 6.2)
row(ax, 0.6, 4.6, [7, 512, 998], cw=1.2, ch=1.1, fs=12, hot=range(3))
ax.text(5.2, 5.15, "카드 3장, 숫자는 1~1,000 사이", ha="left", va="center", fontsize=11)
for k in range(30):
    x = 0.6 + k * 0.6
    ax.add_patch(Rectangle((x, 2.2), 0.5, 0.9, fc="white", ec=INK, lw=0.9))
ax.text(9.5, 3.5, "상자 1번, 2번, 3번 … 1,000번", ha="center", va="center", fontsize=11)
ax.text(9.5, 1.2, "상자를 1,000개 놓고 하나하나 열어 봐야 해요. 거의 다 비어 있어요", ha="center", va="center",
        fontsize=12, color=RED, fontweight="bold")
save(fig, "a08-manyboxes.svg")

# 4-1. 질문할 때마다 맞지 않는 순서를 지워요 (본문용). 숨은 순서는 가 1, 나 3, 다 2
fig, ax = canvas(12.4, 6.6, 20.4, 10.8)
ORDERS = list(itertools.permutations([1, 2, 3]))   # (가, 나, 다)에 놓인 숫자
steps = [("처음", None, None),
         ("가 카드가 나 카드보다 작아?", "응", lambda p: p[0] < p[1]),
         ("나 카드가 다 카드보다 작아?", "아니", lambda p: not p[1] < p[2]),
         ("가 카드가 다 카드보다 작아?", "응", lambda p: p[0] < p[2])]
alive = set(ORDERS)
for c, (q, ans, keep) in enumerate(steps):
    x0 = 0.4 + c * 5.1
    if keep:
        alive = {p for p in alive if keep(p)}
        ax.text(x0 + 1.9, 10.3, q, ha="center", va="center", fontsize=10, fontweight="bold")
        ax.text(x0 + 1.9, 9.6, f"친구: {ans}", ha="center", va="center", fontsize=10, color=RED, fontweight="bold")
    else:
        ax.text(x0 + 1.9, 10.3, q, ha="center", va="center", fontsize=10, fontweight="bold")
    for k, lab in enumerate("가나다"):
        ax.text(x0 + 0.8 + k * 1.1, 8.8, lab, ha="center", va="center", fontsize=10, color=BLUE, fontweight="bold")
    for r, p in enumerate(ORDERS):
        y = 7.6 - r * 1.15
        on = p in alive
        row(ax, x0 + 0.35, y, p, cw=0.9, ch=0.85, gap=0.2, fs=11, gone=() if on else range(3),
            hot=range(3) if on and len(alive) == 1 else ())
        if not on:
            ax.plot([x0 + 0.25, x0 + 3.55], [y + 0.42, y + 0.42], color=RED, lw=1.6)
    ax.text(x0 + 1.9, 0.5, f"남은 순서 {len(alive)}가지", ha="center", va="center", fontsize=11,
            color=RED if c else "#222", fontweight="bold")
    if c < 3:
        arrow(ax, (x0 + 3.85, 4.6), (x0 + 4.75, 4.6), color=INK, lw=1.6, ms=12)
save(fig, "a08-crossout.svg")
