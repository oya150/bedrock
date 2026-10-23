"""알고리즘 4편 그림 만들기. 실행: python lab/fig_04.py  → docs/algorithms/img/04/*.svg

글자는 SVG 안에 글자로 남긴다(글꼴 모양을 파일에 넣지 않는다). 보는 쪽 글꼴로 그려진다.
카드는 차분한 색으로, 강조(새로 받은 카드, 비교 화살표, 많이 든 일)만 빨강으로 칠한다.
"""
import os

import matplotlib

matplotlib.use("svg")
import matplotlib.pyplot as plt
from matplotlib.patches import Arc, Circle, FancyArrowPatch, FancyBboxPatch, Rectangle

OUT = os.path.join(os.path.dirname(__file__), "..", "docs", "algorithms", "img", "04")
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


# 1. 여는 장면: 손에 3, 7, 9. 새 카드 5는 어디에?
fig, ax = canvas(9.0, 4.4, 14.0, 6.8)
kid(ax, 2.2, 0.5, 1.5)
cw, ch = 1.2, 1.7
for k, n in enumerate([3, 7, 9]):
    card(ax, 4.6 + k * 1.5, 2.4, cw, ch, n, fs=16)
card(ax, 7.3, 5.0, cw, ch * 0.9, 5, hot=True, fs=16)
arrow(ax, (7.3, 5.4), (6.0, 4.3), color=RED, lw=2.2, rad=0.3)
ax.text(12.0, 4.6, "?", ha="center", va="center", fontsize=40, color=RED, fontweight="bold")
ax.text(6.6, 1.6, "손에 든 카드", ha="center", va="center", fontsize=12, color=INK)
ax.text(10.0, 5.9, "새로 받은 카드", ha="center", va="center", fontsize=12, color=RED, fontweight="bold")
save(fig, "a04-hand.svg")

# 2. 이 편의 지도
fig, ax = canvas(11.6, 2.9, 19.4, 4.6)
titles = ["한 장씩 끼우기", "몇 번 비교할까", "카드가 많아지면", "거의 차례대로면"]
for i, t in enumerate(titles):
    x = 0.3 + i * 4.8
    box(ax, x, 0.4, 3.8, 3.6)
    ax.text(x + 1.9, 0.95, t, ha="center", va="center", fontsize=12, fontweight="bold")
    if i == 0:
        for k, n in enumerate([3, 7, 9]):
            card(ax, x + 0.5 + k * 0.75, 1.9, 0.6, 0.8, n, fs=10)
        card(ax, x + 1.6, 3.0, 0.6, 0.7, 5, hot=True, fs=10)
        arrow(ax, (x + 1.6, 3.2), (x + 1.25, 2.8), color=RED, lw=1.6, ms=10)
    elif i == 1:
        stones(ax, x + 0.6, 3.2, 4, color=BLUE, r=0.12, gap=0.32)
        stones(ax, x + 0.6, 2.6, 10, color=RED, r=0.12, gap=0.28)
        ax.text(x + 0.45, 3.2, "", ha="right")
    elif i == 2:
        for k, v in enumerate([10, 45, 190]):
            h = 0.12 + v / 190 * 1.9
            ax.add_patch(Rectangle((x + 0.7 + k * 0.9, 1.5), 0.6, h, fc=RED, ec=INK, lw=1))
    else:
        for k, n in enumerate([1, 2, 3, 4, 6, 7]):
            card(ax, x + 0.35 + k * 0.5, 2.0, 0.48, 0.7, n, fs=9)
        card(ax, x + 3.0, 3.0, 0.48, 0.6, 5, hot=True, fs=9)
    if i < 3:
        arrow(ax, (x + 3.95, 2.2), (x + 4.65, 2.2))
save(fig, "a04-map.svg")

# 3. 카드를 7, 3, 9, 5 순서로 받으며 손에 끼우기
fig, ax = canvas(11.0, 6.4, 18.0, 10.4)
deal = [(7, [7], 0), (3, [3, 7], 1), (9, [3, 7, 9], 1), (5, [3, 5, 7, 9], 3)]
ax.text(1.4, 9.9, "받은 카드", ha="center", va="center", fontsize=12, fontweight="bold")
ax.text(7.0, 9.9, "끼운 뒤 손", ha="center", va="center", fontsize=12, fontweight="bold")
ax.text(14.5, 9.9, "비교한 횟수", ha="center", va="center", fontsize=12, fontweight="bold")
for r, (new, hand, cmp_) in enumerate(deal):
    y = 7.6 - r * 2.2
    ax.text(0.0, y + 0.6, f"{r + 1}", ha="left", va="center", fontsize=12, color=INK, fontweight="bold")
    card(ax, 0.9, y, 1.0, 1.2, new, hot=True)
    arrow(ax, (2.3, y + 0.6), (3.6, y + 0.6), lw=1.6, ms=12)
    for k, n in enumerate(hand):
        card(ax, 4.2 + k * 1.2, y, 1.0, 1.2, n, hot=(n == new))
    if cmp_:
        stones(ax, 12.6, y + 0.6, cmp_, color=RED, r=0.18, gap=0.5)
    ax.text(14.4, y + 0.6, f"{cmp_}번" if cmp_ else "0번 (첫 장)",
            ha="left", va="center", fontsize=12, fontweight="bold", color=RED if cmp_ else INK)
save(fig, "a04-deal.svg")

# 4. 3, 7, 9에 5 끼우기: 오른쪽 끝부터 비교한다
fig, ax = canvas(11.0, 4.6, 18.0, 7.6)
cw = 1.6
xs = {3: 1.0, 7: 4.0, 9: 6.6}
for n, x in xs.items():
    card(ax, x, 1.8, cw, 2.0, n, fs=18)
card(ax, 10.6, 1.8, cw, 2.0, 5, hot=True, fs=18)
for k, n in enumerate([9, 7, 3]):
    ax.text(xs[n] + cw / 2, 4.3, "①②③"[k], ha="center", va="center", fontsize=15, color=RED, fontweight="bold")
arrow(ax, (11.2, 4.0), (3.3, 4.0), color=RED, lw=1.8, rad=0.25, ms=14)
ax.plot([3.3, 3.3], [1.5, 4.1], color=RED, lw=2.4, ls="--")
ax.text(xs[9] + cw / 2, 1.2, "5가 더 작아요", ha="center", va="center", fontsize=11)
ax.text(xs[7] + cw / 2, 1.2, "5가 더 작아요", ha="center", va="center", fontsize=11)
ax.text(xs[3] + cw / 2, 1.2, "5가 더 커요", ha="center", va="center", fontsize=11, color=RED, fontweight="bold")
ax.text(3.3, 0.45, "3과 7 사이에 끼워요", ha="center", va="center", fontsize=12, color=RED, fontweight="bold")
save(fig, "a04-insert.svg")

# 5. 다섯 장: 차례대로 받으면 4번, 거꾸로 받으면 10번
fig, ax = canvas(11.0, 5.4, 18.0, 8.8)
rows = [("차례대로 받으면", [1, 2, 3, 4, 5], [0, 1, 1, 1, 1], 5.2, BLUE),
        ("거꾸로 받으면", [5, 4, 3, 2, 1], [0, 1, 2, 3, 4], 1.0, RED)]
for title, seq, cnt, y, col in rows:
    ax.text(0.2, y + 2.6, title, ha="left", va="center", fontsize=13, fontweight="bold")
    for k, (n, c) in enumerate(zip(seq, cnt)):
        x = 0.6 + k * 2.4
        card(ax, x, y + 0.9, 1.1, 1.3, n, fs=14)
        for s in range(c):
            ax.add_patch(Circle((x + 0.25 + (s % 2) * 0.6, y + 0.55 - (s // 2) * 0.5), 0.2, fc=col, ec=col))
        if c == 0:
            ax.text(x + 0.55, y + 0.55, "없음", ha="center", va="center", fontsize=10, color=INK)
    ax.text(13.6, y + 1.5, f"모두 {sum(cnt)}번", ha="left", va="center", fontsize=16, fontweight="bold",
            color=RED if col == RED else "#222")
ax.text(0.6, 8.6, "바둑돌 하나 = 두 장을 한 번 비교", ha="left", va="center", fontsize=11, color=INK)
save(fig, "a04-count.svg")

# 6. 카드가 많아지면: 막대 높이를 실제 비율대로
fig, ax = canvas(10.4, 5.6, 17.0, 9.2)
base = 1.4
scale = 6.6 / 190
for k, (n, up, down) in enumerate([(5, 4, 10), (10, 9, 45), (20, 19, 190)]):
    gx = 1.4 + k * 5.2
    for j, (v, col) in enumerate([(up, BLUE), (down, RED)]):
        bx = gx + j * 1.9
        h = max(v * scale, 0.06)
        ax.add_patch(Rectangle((bx, base), 1.5, h, fc=col, ec=INK, lw=1.2))
        ax.text(bx + 0.75, base + h + 0.15, f"{v}번", ha="center", va="bottom", fontsize=12, fontweight="bold",
                color=RED if col == RED else "#222")
    ax.text(gx + 1.7, base - 0.35, f"카드 {n}장", ha="center", va="top", fontsize=12, fontweight="bold")
ax.plot([0.8, 16.4], [base, base], color=INK, lw=1.4)
ax.add_patch(Rectangle((1.4, 8.6), 0.5, 0.35, fc=BLUE, ec=INK, lw=1))
ax.text(2.1, 8.77, "차례대로 받으면", ha="left", va="center", fontsize=11)
ax.add_patch(Rectangle((5.6, 8.6), 0.5, 0.35, fc=RED, ec=INK, lw=1))
ax.text(6.3, 8.77, "거꾸로 받으면", ha="left", va="center", fontsize=11)
save(fig, "a04-bars.svg")

# 7. 거의 차례대로: 1~9에서 5만 맨 끝에 왔다
fig, ax = canvas(11.6, 3.8, 19.0, 6.2)
row = [1, 2, 3, 4, 6, 7, 8, 9]
cw = 1.5
for k, n in enumerate(row):
    card(ax, 0.6 + k * cw, 1.6, cw - 0.15, 1.6, n, fs=15)
card(ax, 0.6 + 8 * cw + 0.6, 1.6, cw - 0.15, 1.6, 5, hot=True, fs=15)
targets = [7, 6, 5, 4, 3]
for k, t in enumerate(targets):
    x = 0.6 + t * cw + (cw - 0.15) / 2
    ax.text(x, 3.75, f"{k + 1}", ha="center", va="center", fontsize=12, color=RED, fontweight="bold",
            bbox=dict(boxstyle="circle,pad=0.2", fc="white", ec=RED, lw=1.4))
arrow(ax, (0.6 + 8 * cw + 1.2, 4.3), (0.6 + 4 * cw - 0.07, 4.3), color=RED, lw=1.6, rad=0.2, ms=12)
ax.plot([0.6 + 4 * cw - 0.07] * 2, [1.4, 4.3], color=RED, lw=2.2, ls="--")
ax.text(0.6 + 1.5 * cw, 0.9, "1, 2, 3은 보지 않아요", ha="center", va="center", fontsize=11, color=INK)
ax.text(0.6 + 6 * cw, 0.9, "비교 5번이면 끝", ha="center", va="center", fontsize=13, color=RED, fontweight="bold")
save(fig, "a04-almost.svg")
