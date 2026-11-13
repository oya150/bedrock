"""알고리즘 7편 그림 만들기. 실행: python lab/fig_07.py  → docs/algorithms/img/07/*.svg

예시는 친구 둘이 정리한 카드 64장(홀수 32장 줄 + 짝수 32장 줄)을 편 끝까지 잇는다.
그림 안 글씨는 낱말과 숫자만 둔다. 문장은 본문과 그림 설명에 둔다(쉬운글-정책 5장).
숫자는 모두 독자가 그림에서 셀 수 있는 것이다. 검토용 PNG는 FIG_FMT=png FIG_OUT=<폴더>.
"""
import os
import random
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "es"))
from figkit import BLUE, GREY, INK, NOTE, PINK, RED, arrow, canvas, cells, label, outdir, save  # noqa: E402
from matplotlib.patches import Circle, FancyBboxPatch, Rectangle  # noqa: E402

OUT = outdir("07", "algorithms")


def frame(ax, x0, x1, y, h, color, lw=2.2):
    """이어진 줄 하나를 감싸는 둥근 테두리."""
    ax.add_patch(FancyBboxPatch((x0 - 0.08, y - 0.08), x1 - x0 + 0.16, h + 0.16, boxstyle="round,pad=0.04",
                                fc="none", ec=color, lw=lw))


def dot_cell(ax, x, y, w, h):
    label(ax, x + w / 2, y + h / 2, "…", fs=13, color=INK)
    return x + w


def short_row(ax, x, y, head, tail, w=0.5, h=0.55, gap=0.06, hot=(), fs=10.5):
    """head 카드 몇 장, …, tail 카드 몇 장. 끝 x를 돌려준다."""
    x = cells(ax, x, y, head, w=w, h=h, gap=gap, hot=hot, fs=fs) + gap
    x = dot_cell(ax, x, y, w, h) + gap
    return cells(ax, x, y, tail, w=w, h=h, gap=gap, fs=fs)


def neighbor_dots(ax, x, y, n, w, gap, color=RED):
    """이웃한 두 장 사이 위마다 점 하나(비교 한 번)."""
    for k in range(n - 1):
        ax.add_patch(Circle((x + k * (w + gap) + w + gap / 2, y), 0.09, fc=color, ec=color))


# 1. 친구 둘이 정리한 카드를 이어 놓았다
fig, ax = canvas(7.2, 3.0, 12, 5.0)
label(ax, 2.9, 4.6, "친구 1: 홀수 32장", fs=11, bold=True)
short_row(ax, 0.9, 3.5, [1, 3, 5], [63])
label(ax, 9.1, 4.6, "친구 2: 짝수 32장", fs=11, bold=True)
short_row(ax, 7.1, 3.5, [2, 4, 6], [64])
x0 = 3.08
arrow(ax, (2.9, 3.35), (4.4, 1.6), lw=1.5, ms=13)
arrow(ax, (9.1, 3.35), (7.6, 1.6), lw=1.5, ms=13)
x1 = short_row(ax, x0, 0.85, [1, 3, 5], [63])
frame(ax, x0, x1, 0.85, 0.55, RED)
x2 = short_row(ax, x1 + 0.35, 0.85, [2, 4, 6], [64])
frame(ax, x1 + 0.35, x2, 0.85, 0.55, BLUE)
label(ax, 6.0, 0.25, "64장", fs=11, color=INK)
save(fig, OUT, "a07-friends.svg")

# 2. 이미 차례대로: 이웃끼리 7번 비교하면 끝
W, G = 1.0, 0.35
fig, ax = canvas(7.2, 2.1, 12, 3.4)
cells(ax, 0.6, 1.1, list(range(1, 9)), w=W, h=1.0, gap=G, fs=15)
neighbor_dots(ax, 0.6, 2.45, 8, W, G)
label(ax, 6.0, 0.45, "비교 7번", fs=12.5, color=RED, bold=True)
save(fig, OUT, "a07-asc.svg")

# 3. 거꾸로 이어진 줄: 7번 비교하고 통째로 뒤집기
fig, ax = canvas(7.2, 4.0, 12, 6.6)
cells(ax, 0.6, 4.6, list(range(8, 0, -1)), w=W, h=1.0, gap=G, fs=15)
neighbor_dots(ax, 0.6, 5.95, 8, W, G)
label(ax, 11.6, 6.35, "비교 7번", fs=11, color=RED, ha="right", bold=True)
for k in range(4):
    a = 0.6 + k * (W + G) + W / 2
    b = 0.6 + (7 - k) * (W + G) + W / 2
    arrow(ax, (a, 4.45), (b, 4.45), color=RED, lw=1.3, rad=0.22 + k * 0.06, ms=11, style="<|-|>")
label(ax, 6.0, 2.0, "뒤집기", fs=12, color=RED, bold=True)
cells(ax, 0.6, 0.4, list(range(1, 9)), w=W, h=1.0, gap=G, hot=range(8), fs=15)
save(fig, OUT, "a07-desc.svg")

# 4. 친구 카드 64장에서 이어진 줄 찾기: 63 다음 2에서 끊긴다
fig, ax = canvas(7.2, 2.6, 12, 4.3)
w, gap, y = 0.62, 0.08, 1.6
x = xa0 = 1.5
x = cells(ax, x, y, [1, 3, 5], w=w, h=0.7, gap=gap, fs=11) + gap
x = dot_cell(ax, x, y, w, 0.7) + gap
xa1 = x = cells(ax, x, y, [61, 63], w=w, h=0.7, gap=gap, fs=11, hot=(1,))
x = xb0 = x + 0.35
x = cells(ax, x, y, [2, 4], w=w, h=0.7, gap=gap, fs=11, hot=(0,)) + gap
x = dot_cell(ax, x, y, w, 0.7) + gap
xb1 = cells(ax, x, y, [62, 64], w=w, h=0.7, gap=gap, fs=11)
frame(ax, xa0, xa1, y, 0.7, RED)
frame(ax, xb0, xb1, y, 0.7, BLUE)
ax.add_patch(Rectangle((xa1 + 0.135, y - 0.3), 0.08, 1.3, fc=RED, ec=RED))
label(ax, xa1 + 0.175, 3.55, "63 > 2", fs=11.5, color=RED, bold=True)
label(ax, (xa0 + xa1) / 2, 0.9, "줄 1: 32장", fs=11, color=INK)
label(ax, (xb0 + xb1) / 2, 0.9, "줄 2: 32장", fs=11, color=INK)
label(ax, 6.0, 0.25, "이웃 비교 63번", fs=11.5, color=RED, bold=True)
save(fig, OUT, "a07-find.svg")

# 5. 줄 둘을 맨 앞끼리 비교하며 합치기
fig, ax = canvas(7.2, 3.3, 12, 5.4)
xa = short_row(ax, 1.5, 4.3, [1, 3, 5], [63], w=0.55, h=0.6, hot=(0,))
frame(ax, 1.5, xa, 4.3, 0.6, RED)
xb = short_row(ax, 7.5, 4.3, [2, 4, 6], [64], w=0.55, h=0.6, hot=(0,))
frame(ax, 7.5, xb, 4.3, 0.6, BLUE)
label(ax, 6.0, 4.6, "1 < 2", fs=11.5, color=RED, bold=True)
arrow(ax, (3.0, 4.05), (4.6, 2.35), lw=1.5, ms=13)
arrow(ax, (9.0, 4.05), (7.4, 2.35), lw=1.5, ms=13)
x = cells(ax, 3.28, 1.4, [1, 2, 3, 4, 5], w=0.55, h=0.6, gap=0.06, hot=(0,), fs=10.5) + 0.06
x = dot_cell(ax, x, 1.4, 0.55, 0.6) + 0.06
x = cells(ax, x, 1.4, [62, 63, 64], w=0.55, h=0.6, gap=0.06, fs=10.5)
frame(ax, 3.28, x, 1.4, 0.6, INK, lw=1.6)
label(ax, 6.0, 0.55, "합치기 비교 63번", fs=11.5, color=RED, bold=True)
save(fig, OUT, "a07-merge.svg")

# 6. 5편 방법은 합치기 여섯 층, 팀 정렬은 한 번
fig, ax = canvas(7.2, 3.6, 12, 6.0)
label(ax, 2.9, 5.65, "5편 방법", fs=11.5, bold=True)
LW, LX = 5.2, 0.3
for lv in range(7):                       # 1덩이, 2덩이, …, 64덩이
    n = 2 ** lv
    yy = 4.8 - lv * 0.68
    bw = LW / n
    for k in range(n):
        ax.add_patch(Rectangle((LX + k * bw, yy), bw, 0.42, fc=NOTE, ec=INK, lw=0.4 if n > 16 else 0.9))
label(ax, 2.9, 0.25, "합치기 6층", fs=11.5, color=RED, bold=True)
ax.plot([6.45, 6.45], [0.3, 5.7], color=GREY, lw=1)
label(ax, 9.3, 5.65, "팀 정렬", fs=11.5, bold=True)
ax.add_patch(Rectangle((7.0, 4.8), 4.6, 0.42, fc=NOTE, ec=INK, lw=0.9))
ax.add_patch(Rectangle((7.0, 4.12), 2.3, 0.42, fc=NOTE, ec=RED, lw=1.6))
ax.add_patch(Rectangle((9.3, 4.12), 2.3, 0.42, fc=NOTE, ec=BLUE, lw=1.6))
label(ax, 9.3, 0.25, "합치기 1번", fs=11.5, color=RED, bold=True)
save(fig, OUT, "a07-layers.svg")

# 7. 짧은 줄은 끼워서 늘려요
fig, ax = canvas(7.2, 1.6, 12, 2.6)
cells(ax, 0.4, 0.4, [3, 7], w=0.8, h=0.9, gap=0.1, fs=14)
frame(ax, 0.4, 2.1, 0.4, 0.9, RED)
cells(ax, 2.5, 0.4, [5, 1, 9], w=0.8, h=0.9, gap=0.1, hot=range(3), fs=14)
label(ax, 1.25, 2.1, "줄 2장", fs=11, color=INK)
label(ax, 3.85, 2.1, "끼우기", fs=11, color=RED, bold=True)
arrow(ax, (5.4, 0.85), (6.3, 0.85), lw=1.6, ms=14)
cells(ax, 6.6, 0.4, [1, 3, 5, 7, 9], w=0.8, h=0.9, gap=0.1, fs=14)
frame(ax, 6.6, 6.6 + 5 * 0.9 - 0.1, 0.4, 0.9, RED)
label(ax, 8.85, 2.1, "줄 5장", fs=11, color=INK)
save(fig, OUT, "a07-extend.svg")

# 8. 뒤죽박죽 64장: 짧은 줄 → 32장씩 늘리기 → 한 번 합치기
random.seed(3)                            # lab/07_timsort.py 와 같은 뒤죽박죽 순서
MIXED = random.sample(range(1, 65), 64)
RUNS = [[MIXED[0]]]
for a, b in zip(MIXED, MIXED[1:]):
    if a < b:
        RUNS[-1].append(b)
    else:
        RUNS.append([b])
fig, ax = canvas(7.2, 3.5, 12, 5.8)
cw = 11.2 / 64
x = 0.4
for r in RUNS:
    rw = len(r) * cw
    ax.add_patch(Rectangle((x, 4.6), rw - 0.04, 0.55, fc=NOTE, ec=INK, lw=0.7))
    x += rw
label(ax, 6.0, 5.5, f"뒤죽박죽 64장 (나누면 줄 {len(RUNS)}개)", fs=11, color=INK)
arrow(ax, (6.0, 4.45), (6.0, 3.6), lw=1.5, ms=13)
label(ax, 6.3, 4.0, "첫 줄부터 32장까지 끼우기", fs=10.5, color=RED, ha="left", bold=True)
ax.add_patch(Rectangle((0.4, 2.8), 5.56, 0.6, fc=PINK, ec=RED, lw=1.8))
ax.add_patch(Rectangle((6.04, 2.8), 5.56, 0.6, fc=PINK, ec=RED, lw=1.8))
label(ax, 3.18, 3.1, "32장", fs=11.5, color=RED, bold=True)
label(ax, 8.82, 3.1, "32장", fs=11.5, color=RED, bold=True)
arrow(ax, (6.0, 2.65), (6.0, 1.8), lw=1.5, ms=13)
label(ax, 6.3, 2.2, "합치기", fs=10.5, color=INK, ha="left", bold=True)
ax.add_patch(Rectangle((0.4, 1.0), 11.2, 0.6, fc=NOTE, ec=INK, lw=1.4))
label(ax, 6.0, 1.3, "64장", fs=11.5, bold=True)
save(fig, OUT, "a07-random.svg")
