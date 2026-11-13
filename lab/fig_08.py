"""알고리즘 8편 그림 만들기. 실행: python lab/fig_08.py  → docs/algorithms/img/08/*.svg

예시는 뒤집은 카드 세 장(가, 나, 다 = 1, 3, 2)과 숫자가 1~5뿐인 카드 20장이다.
그림 안 글씨는 낱말과 숫자만 둔다. 문장은 본문과 그림 설명에 둔다(쉬운글-정책 5장).
숫자는 모두 독자가 그림에서 셀 수 있는 것이다. 검토용 PNG는 FIG_FMT=png FIG_OUT=<폴더>.
"""
import itertools
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "es"))
from figkit import BLUE, INK, NOTE, PINK, RED, arrow, box, canvas, cells, label, outdir, save  # noqa: E402
from matplotlib.patches import Circle, Rectangle  # noqa: E402

OUT = outdir("08", "algorithms")
ORDERS = list(itertools.permutations([1, 2, 3]))   # (가, 나, 다)에 놓인 숫자


def back(ax, x, y, w, h, name, fs=14):
    """뒤집어 놓은 카드. 뒷면 이름만 보인다."""
    ax.add_patch(Rectangle((x, y), w, h, fc=BLUE, ec=INK, lw=1.4))
    label(ax, x + w / 2, y + h / 2, name, fs=fs, color="white", bold=True)


# 1. 여는 장면: 뒤집은 카드 세 장, 물을 수 있는 건 "작아?"뿐
fig, ax = canvas(7.2, 2.6, 12, 4.3)
for k, name in enumerate("가나다"):
    back(ax, 0.6 + k * 1.5, 0.5, 1.2, 1.7, name, fs=16)
box(ax, 5.6, 2.3, 3.6, 0.9, fc="white")
label(ax, 7.4, 2.75, "가 < 나 ?", fs=14, bold=True)
box(ax, 9.7, 2.3, 1.7, 0.9, fc=PINK, ec=RED)
label(ax, 10.55, 2.75, "응", fs=14, color=RED, bold=True)
box(ax, 5.6, 0.7, 3.6, 0.9, fc="white")
label(ax, 7.4, 1.15, "나 < 다 ?", fs=14, bold=True)
box(ax, 9.7, 0.7, 1.7, 0.9, fc="white")
label(ax, 10.55, 1.15, "아니", fs=14, color=INK, bold=True)
label(ax, 7.4, 3.85, "질문", fs=11, color=INK)
label(ax, 10.55, 3.85, "대답", fs=11, color=INK)
save(fig, OUT, "a08-guess.svg")

# 2. 카드 세 장은 순서가 6가지
fig, ax = canvas(7.2, 2.8, 12, 4.6)
for r, p in enumerate(ORDERS):
    cx = 0.9 + (r % 3) * 3.75
    cy = 2.7 - (r // 3) * 1.7
    cells(ax, cx, cy, p, w=0.75, h=0.95, gap=0.1, fs=14, hot=range(3) if p == (1, 2, 3) else ())
label(ax, 6.0, 0.35, "6가지", fs=12, color=INK, bold=True)
save(fig, OUT, "a08-orders.svg")

# 3. 질문할 때마다 맞지 않는 순서를 지워요. 숨은 순서는 가 1, 나 3, 다 2
fig, ax = canvas(7.2, 4.6, 12, 7.6)
steps = [("처음", None, None),
         ("가 < 나 ?", "응", lambda p: p[0] < p[1]),
         ("나 < 다 ?", "아니", lambda p: not p[1] < p[2]),
         ("가 < 다 ?", "응", lambda p: p[0] < p[2])]
alive = set(ORDERS)
for c, (q, ans, keep) in enumerate(steps):
    x0 = 0.15 + c * 3.0
    if keep:
        alive = {p for p in alive if keep(p)}
    label(ax, x0 + 1.25, 7.25, q, fs=11, bold=True)
    if ans:
        label(ax, x0 + 1.25, 6.75, ans, fs=11, color=RED, bold=True)
    for k, name in enumerate("가나다"):
        label(ax, x0 + 0.5 + k * 0.75, 6.2, name, fs=10, color=BLUE, bold=True)
    for r, p in enumerate(ORDERS):
        y = 5.35 - r * 0.8
        on = p in alive
        cells(ax, x0 + 0.2, y, p, w=0.6, h=0.6, gap=0.15, fs=11, dim=() if on else range(3),
              hot=range(3) if on and len(alive) == 1 else ())
        if not on:
            ax.plot([x0 + 0.1, x0 + 2.4], [y + 0.3, y + 0.3], color=RED, lw=1.5)
    label(ax, x0 + 1.25, 0.3, f"{len(alive)}가지", fs=11.5, color=RED if c else "#222", bold=True)
    if c < 3:
        arrow(ax, (x0 + 2.55, 3.4), (x0 + 2.95, 3.4), lw=1.4, ms=11)
save(fig, OUT, "a08-crossout.svg")

# 4. 세 장 나무: 어떤 대답이 와도 질문 세 번 안에 끝난다
fig, ax = canvas(7.2, 3.8, 14, 7.8)
ax.set_ylim(1.1, 7.8)


def node(x, y, text):
    ax.text(x, y, text, ha="center", va="center", fontsize=10.5, color="#222",
            bbox=dict(boxstyle="round,pad=0.35", fc=NOTE, ec=INK, lw=1.4))


def leaf(x, y, text):
    ax.text(x, y, text, ha="center", va="center", fontsize=10.5, color=RED, fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.3", fc=PINK, ec=RED, lw=1.4))


def edge(a, b, s):
    ax.plot([a[0], b[0]], [a[1], b[1]], color=INK, lw=1.2)
    label(ax, (a[0] + b[0]) / 2 + (0.3 if b[0] > a[0] else -0.3), (a[1] + b[1]) / 2 + 0.1, s, fs=9.5, color=INK)


node(8.0, 7.3, "가 < 나 ?")
node(5.0, 5.5, "나 < 다 ?")
node(11.0, 5.5, "가 < 다 ?")
edge((8.0, 7.0), (5.0, 5.8), "응")
edge((8.0, 7.0), (11.0, 5.8), "아니")
leaf(3.4, 3.6, "가 나 다")
node(6.6, 3.6, "가 < 다 ?")
edge((5.0, 5.2), (3.4, 3.9), "응")
edge((5.0, 5.2), (6.6, 3.9), "아니")
leaf(9.4, 3.6, "나 가 다")
node(12.6, 3.6, "나 < 다 ?")
edge((11.0, 5.2), (9.4, 3.9), "응")
edge((11.0, 5.2), (12.6, 3.9), "아니")
leaf(5.6, 1.7, "가 다 나")
leaf(7.6, 1.7, "다 가 나")
edge((6.6, 3.3), (5.6, 2.0), "응")
edge((6.6, 3.3), (7.6, 2.0), "아니")
leaf(11.6, 1.7, "나 다 가")
leaf(13.6, 1.7, "다 나 가")
edge((12.6, 3.3), (11.6, 2.0), "응")
edge((12.6, 3.3), (13.6, 2.0), "아니")
for y, t in [(7.3, "6가지"), (5.5, "3가지"), (3.6, "1~2가지"), (1.7, "1가지")]:
    label(ax, 0.2, y, t, fs=10.5, color=INK, ha="left")
for y, t in [(6.4, "질문 1"), (4.55, "질문 2"), (2.65, "질문 3")]:
    label(ax, 0.2, y, t, fs=9.5, color=RED, ha="left", bold=True)
save(fig, OUT, "a08-tree.svg")

# 5. 네 장: 24가지 → 12 → 6 → 3 → 2 → 1, 비교 5번
fig, ax = canvas(7.2, 3.4, 12, 5.6)
vals = [24, 12, 6, 3, 2, 1]
for k, v in enumerate(vals):
    y = 4.9 - k * 0.8
    ax.add_patch(Rectangle((1.6, y), v * 0.36, 0.5, fc=RED if v == 1 else NOTE, ec=INK, lw=1.1))
    label(ax, 1.4, y + 0.25, f"{v}가지", fs=10.5, ha="right", bold=True)
    if k:
        ax.add_patch(Circle((11.0, y + 0.25), 0.13, fc=RED, ec=RED))
        label(ax, 10.75, y + 0.25, f"비교 {k}", fs=10, ha="right", color=RED)
label(ax, 6.0, 0.25, "카드 4장: 비교 5번", fs=11.5, color=RED, bold=True)
save(fig, OUT, "a08-halving.svg")

# 6. 상자에 나눠 담기: 숫자 1~5뿐인 카드 20장 (lab/08_counting.py 의 random.seed(8) 카드)
DECK = [2, 3, 4, 2, 2, 1, 1, 2, 2, 5, 2, 4, 1, 4, 4, 4, 4, 4, 5, 2]
fig, ax = canvas(7.2, 4.4, 12, 7.3)
for k, v in enumerate(DECK):
    cells(ax, 0.2 + k * 0.58, 6.3, [v], w=0.5, h=0.6, fs=10)
label(ax, 6.0, 5.85, "카드 20장", fs=10.5, color=INK)
counts = [DECK.count(v) for v in range(1, 6)]
for b in range(5):
    bx = 0.5 + b * 2.25
    ax.add_patch(Rectangle((bx, 1.3), 1.8, 3.6, fc="white", ec=INK, lw=1.5))
    label(ax, bx + 0.9, 5.25, f"{b + 1}번 상자", fs=10.5, bold=True)
    for j in range(counts[b]):
        cells(ax, bx + 0.55, 1.45 + j * 0.48, [b + 1], w=0.7, h=0.4, hot=(0,), fs=8)
    label(ax, bx + 0.9, 0.95, f"{counts[b]}장", fs=10.5)
label(ax, 6.0, 0.3, "비교 0번", fs=12, color=RED, bold=True)
save(fig, OUT, "a08-boxes.svg")

# 7. 상자가 너무 많으면: 카드 3장에 상자 1,000개
fig, ax = canvas(7.2, 2.6, 12, 4.3)
cells(ax, 0.4, 3.0, [7, 512, 998], w=0.9, h=0.8, gap=0.12, hot=range(3), fs=12)
label(ax, 3.9, 3.4, "카드 3장", fs=11, ha="left", color=INK)
for k in range(28):
    ax.add_patch(Rectangle((0.4 + k * 0.4, 1.3), 0.32, 0.6, fc="white", ec=INK, lw=0.8))
for k in (0, 14, 26):                     # 7, 512, 998이 들어간 상자(1,000개를 28칸으로 줄여 그림)
    ax.add_patch(Rectangle((0.4 + k * 0.4, 1.3), 0.32, 0.6, fc=PINK, ec=RED, lw=1.4))
label(ax, 0.56, 1.0, "1", fs=9.5, color=INK)
label(ax, 11.36, 1.0, "1,000", fs=9.5, color=INK)
label(ax, 6.0, 0.35, "상자 1,000개", fs=11.5, color=RED, bold=True)
save(fig, OUT, "a08-manyboxes.svg")
