"""알고리즘 3편 그림 만들기. 실행: python lab/fig_03.py  → docs/algorithms/img/03/*.svg

글자는 SVG 안에 글자로 남긴다(글꼴 모양을 파일에 넣지 않는다). 보는 쪽 글꼴로 그려진다.
남은 숫자는 차분한 색으로, 버린 숫자는 회색으로, 강조(부른 숫자, 정답)만 빨강으로 칠한다.
"""
import os

import matplotlib

matplotlib.use("svg")
import matplotlib.pyplot as plt
from matplotlib.patches import Arc, Circle, FancyArrowPatch, FancyBboxPatch, Rectangle

OUT = os.path.join(os.path.dirname(__file__), "..", "docs", "algorithms", "img", "03")
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


def bubble(ax, x, y, text, color=INK, fc="white", fs=12):
    ax.text(x, y, text, ha="center", va="center", fontsize=fs, color=color, fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.35", fc=fc, ec=color, lw=1.4))


def card(ax, x, y, w, h, num, hot=False, gone=False, fs=11):
    fc = LIGHT if gone else ("#fbe3dc" if hot else NOTE)
    ax.add_patch(Rectangle((x, y), w, h, fc=fc, ec=RED if hot else (GREY if gone else INK), lw=2.2 if hot else 1.2))
    ax.text(x + w / 2, y + h / 2, str(num), ha="center", va="center", fontsize=fs,
            color=RED if hot else (GREY if gone else "#222"), fontweight="bold")


# 1. 여는 장면: 하나씩 부르기 vs 가운데 부르기
fig, ax = canvas(11.0, 4.6, 18.0, 7.6)
kid(ax, 2.0, 0.4, 1.2)
for k, t in enumerate(["1?", "2?", "3?", "4?", "5?", "6?", "…"]):
    bubble(ax, 3.6 + (k % 4) * 1.15, 6.4 - (k // 4) * 1.0, t, fs=12)
ax.text(5.3, 3.6, "운 나쁘면 100번", ha="center", va="center", fontsize=13, fontweight="bold")
kid(ax, 11.0, 0.4, 1.2)
for k, (t, a) in enumerate([("50?", "업!"), ("75?", "업!"), ("88?", "업!")]):
    bubble(ax, 13.0, 6.5 - k * 1.05, t, color=RED, fc="#fbe3dc", fs=12)
    bubble(ax, 15.0, 6.5 - k * 1.05, a, fs=12)
ax.text(14.0, 3.0, "일곱 번 안에 꼭!", ha="center", va="center", fontsize=13, color=RED, fontweight="bold")
ax.plot([9.0, 9.0], [0.3, 7.2], color=GREY, lw=1.2, ls="--")
save(fig, "a03-game.svg")

# 2. 이 편의 지도
fig, ax = canvas(11.6, 2.9, 19.4, 4.6)
titles = ["하나씩 부르기", "가운데 부르기", "반씩 버리면 몇 번?", "차례대로 놓여야"]
for i, t in enumerate(titles):
    x = 0.3 + i * 4.8
    box(ax, x, 0.4, 3.8, 3.6)
    ax.text(x + 1.9, 0.95, t, ha="center", va="center", fontsize=12, fontweight="bold")
    if i == 0:
        for k in range(5):
            card(ax, x + 0.35 + k * 0.62, 2.2, 0.6, 0.8, k + 1, fs=10)
        for k in range(4):
            arrow(ax, (x + 0.65 + k * 0.62, 3.15), (x + 1.27 + k * 0.62, 3.15), lw=1.3, rad=-0.6, ms=10)
    elif i == 1:
        for k in range(5):
            card(ax, x + 0.35 + k * 0.62, 2.2, 0.6, 0.8, (k + 1) * 20, hot=(k == 2), gone=(k < 2), fs=10)
        arrow(ax, (x + 0.35 + 2.5 * 0.62, 3.8), (x + 0.35 + 2.5 * 0.62, 3.1), color=RED, lw=2)
    elif i == 2:
        for k, wid in enumerate([3.0, 1.5, 0.75, 0.38]):
            ax.add_patch(Rectangle((x + 0.4, 3.3 - k * 0.42), wid, 0.3, fc=BLUE, ec=INK, lw=1))
    else:
        for k, n in enumerate([3, 8, 12, 20, 31]):
            card(ax, x + 0.35 + k * 0.62, 2.7, 0.6, 0.6, n, fs=9)
        for k, n in enumerate([20, 3, 31, 8, 12]):
            card(ax, x + 0.35 + k * 0.62, 1.6, 0.6, 0.6, n, fs=9)
    if i < 3:
        arrow(ax, (x + 3.95, 2.2), (x + 4.65, 2.2))
save(fig, "a03-map.svg")

# 3. 가운데를 부르면 반씩 버린다 (운이 제일 나쁠 때: 정답 100, 늘 "업!")
steps = [(1, 100, 50, "업!"), (51, 100, 75, "업!"), (76, 100, 88, "업!"), (89, 100, 94, "업!"),
         (95, 100, 97, "업!"), (98, 100, 99, "업!"), (100, 100, 100, "정답!")]
fig, ax = canvas(11.6, 6.6, 19.0, 10.8)
X0, W = 1.6, 12.0
u = W / 100
for r, (lo, hi, mid, ans) in enumerate(steps):
    y = 9.6 - r * 1.4
    ax.add_patch(Rectangle((X0, y), W, 0.55, fc=LIGHT, ec=GREY, lw=0.8))
    ax.add_patch(Rectangle((X0 + (lo - 1) * u, y), (hi - lo + 1) * u, 0.55, fc=BLUE, ec=INK, lw=1.2))
    ax.add_patch(Rectangle((X0 + (mid - 1) * u, y - 0.1), u, 0.75, fc=RED, ec=RED, lw=0.5))
    ax.text(0.2, y + 0.27, f"{r + 1}번째", ha="left", va="center", fontsize=11, fontweight="bold")
    ax.text(X0 + (mid - 0.5) * u, y + 0.95, str(mid), ha="center", va="center", fontsize=11, color=RED,
            fontweight="bold")
    ax.text(14.2, y + 0.27, f"{mid}? {ans}", ha="left", va="center", fontsize=12,
            color=RED if r == 6 else "#222", fontweight="bold")
    nxt = steps[r + 1] if r < 6 else None
    if nxt:
        ax.text(16.6, y + 0.27, f"→ 남은 숫자 {nxt[1] - nxt[0] + 1}개", ha="left", va="center", fontsize=11)
ax.text(X0, 10.55, "1", ha="center", va="bottom", fontsize=10)
ax.text(X0 + W, 10.55, "100", ha="center", va="bottom", fontsize=10)
save(fig, "a03-halves.svg")

# 4. 늘 "업!"일 때 남은 숫자: 100개는 일곱 번째, 1,000개는 열 번째에 맞힌다
fig, ax = canvas(11.6, 3.9, 19.4, 6.4)
rows = [("1~100", [100, 50, 25, 12, 6, 3, 1], 4.3), ("1~1,000", [1000, 500, 250, 125, 62, 31, 15, 7, 3, 1], 1.6)]
for label, seq, y in rows:
    ax.text(0.1, y + 0.35, label, ha="left", va="center", fontsize=12, fontweight="bold")
    for k, v in enumerate(seq):
        x = 2.0 + k * 1.55
        box(ax, x, y, 1.05, 0.7, fc="white" if k == 0 else NOTE, ec=INK, lw=1.4)
        ax.text(x + 0.52, y + 0.35, f"{v:,}", ha="center", va="center", fontsize=11, fontweight="bold")
        if k > 0:
            ax.text(x - 0.25, y + 0.95, f"{k}번", ha="center", va="center", fontsize=9, color=INK)
            arrow(ax, (x - 0.47, y + 0.35), (x - 0.05, y + 0.35), lw=1.4, ms=10)
    x = 2.0 + len(seq) * 1.55
    arrow(ax, (x - 0.47, y + 0.35), (x - 0.05, y + 0.35), color=RED, lw=1.6, ms=12)
    ax.text(x - 0.25, y + 0.95, f"{len(seq)}번", ha="center", va="center", fontsize=9, color=RED, fontweight="bold")
    ax.text(x + 0.05, y + 0.35, "정답!", ha="left", va="center", fontsize=12, color=RED, fontweight="bold")
ax.text(2.0, 6.15, "부를 때마다 남은 숫자 (친구가 늘 \"업!\"이라고 할 때)", ha="left", va="center", fontsize=11, color=INK)
for _, _, y in rows:
    ax.text(2.52, y - 0.3, "부르기 전", ha="center", va="center", fontsize=9, color=INK)
save(fig, "a03-steps.svg")

# 5. 하나씩 vs 반씩: 100개와 1,000개
fig, ax = canvas(10.4, 5.4, 17.0, 8.8)
base = 1.2
scale = 6.4 / 1000
groups = [("하나씩 부르기", [(100, "100번"), (1000, "1,000번")], GREY, 1.2),
          ("가운데 부르기", [(7, "7번"), (10, "10번")], RED, 9.6)]
for title, bars, col, gx in groups:
    for k, (v, lab) in enumerate(bars):
        bx = gx + k * 2.6
        h = max(v * scale, 0.08)
        ax.add_patch(Rectangle((bx, base), 1.6, h, fc=col, ec=INK, lw=1.2))
        ax.text(bx + 0.8, base + h + 0.15, lab, ha="center", va="bottom",
                fontsize=12, fontweight="bold", color=RED if col == RED else "#222")
        ax.text(bx + 0.8, base - 0.3, "숫자 100개" if k == 0 else "숫자 1,000개", ha="center", va="top", fontsize=11)
    ax.text(gx + 2.1, 0.05, title, ha="center", va="bottom", fontsize=13, fontweight="bold")
ax.plot([0.6, 16.4], [base, base], color=INK, lw=1.4)
save(fig, "a03-bars.svg")

# 6. 차례대로 놓여 있어야 반을 버린다
fig, ax = canvas(11.6, 4.6, 19.0, 7.6)
sorted_nums = [3, 8, 12, 15, 20, 26, 31, 40, 44, 51, 57, 63, 70, 82, 95]
mixed = [44, 8, 70, 15, 95, 26, 3, 40, 63, 51, 12, 82, 31, 57, 20]
cw = 1.1
ax.text(0.3, 7.1, "차례대로 놓인 카드에서 57 찾기", ha="left", va="center", fontsize=13, fontweight="bold")
for k, n in enumerate(sorted_nums):
    card(ax, 0.6 + k * cw, 5.2, cw, 1.1, n, hot=(k == 7), gone=(k < 7))
ax.text(0.6 + 3.5 * cw, 4.75, "40보다 작은 쪽은 버려요", ha="center", va="center", fontsize=11, color=INK)
ax.text(0.3, 3.4, "뒤죽박죽 카드에서 57 찾기", ha="left", va="center", fontsize=13, fontweight="bold")
for k, n in enumerate(mixed):
    card(ax, 0.6 + k * cw, 1.5, cw, 1.1, n, hot=(k == 7))
ax.text(0.6 + 7.5 * cw, 0.9, "가운데가 40이어도, 57이 어느 쪽에 있는지 몰라요", ha="center", va="center",
        fontsize=11, color=RED, fontweight="bold")
save(fig, "a03-sorted.svg")

# 7. 정렬된 카드 사이에 25 넣기: 뒤 카드를 한 칸씩 옮긴다
fig, ax = canvas(11.0, 3.4, 18.0, 5.6)
row = [3, 8, 12, 20, 31, 44, 57]
cw = 1.5
for k, n in enumerate(row):
    card(ax, 1.0 + k * cw, 1.6, cw, 1.2, n)
ax.add_patch(Rectangle((1.0 + 7 * cw, 1.6), cw, 1.2, fc="white", ec=INK, lw=1.4, ls="--"))
for k in range(6, 3, -1):
    arrow(ax, (1.0 + (k + 0.5) * cw, 2.95), (1.0 + (k + 1.5) * cw, 2.95), color=RED, lw=1.6, rad=-0.6, ms=12)
ax.text(1.0 + 3.7 * cw, 4.9, "25", ha="center", va="center", fontsize=13, color=RED, fontweight="bold",
        bbox=dict(boxstyle="round,pad=0.3", fc="#fbe3dc", ec=RED, lw=1.6))
arrow(ax, (1.0 + 3.9 * cw, 4.5), (1.0 + 4.4 * cw, 3.1), color=RED, lw=2, rad=-0.2)
ax.text(1.0 + 4 * cw, 0.9, "20과 31 사이에 넣으려면, 31·44·57을 한 칸씩 옮겨야 해요", ha="center", va="center",
        fontsize=12, color=RED, fontweight="bold")
save(fig, "a03-insert.svg")
