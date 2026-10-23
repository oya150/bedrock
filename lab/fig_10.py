"""알고리즘 10편 그림 만들기. 실행: python lab/fig_10.py  → docs/algorithms/img/10/*.svg

글자는 SVG 안에 글자로 남긴다(글꼴 모양을 파일에 넣지 않는다). 보는 쪽 글꼴로 그려진다.
카드는 차분한 색으로, 강조(새로 받은 카드, 비교 화살표, 많이 든 일)만 빨강으로 칠한다.
"""
import itertools
import os

import matplotlib

matplotlib.use("svg")
import matplotlib.pyplot as plt
from matplotlib.patches import Arc, Circle, FancyArrowPatch, FancyBboxPatch, Rectangle

OUT = os.path.join(os.path.dirname(__file__), "..", "docs", "algorithms", "img", "10")
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


# 힙 나무: 배열 자리 k의 아래 두 자리는 2k+1, 2k+2
POS = {0: (8.0, 8.4), 1: (4.0, 6.0), 2: (12.0, 6.0), 3: (2.0, 3.6), 4: (6.0, 3.6), 5: (10.0, 3.6), 6: (14.0, 3.6),
       7: (1.0, 1.2), 8: (3.0, 1.2)}


def tree(ax, a, dx=0.0, dy=0.0, s=1.0, hot=(), gone=(), fs=14, pos=POS):
    for k in range(len(a)):
        for c in (2 * k + 1, 2 * k + 2):
            if c < len(a):
                (x1, y1), (x2, y2) = pos[k], pos[c]
                ax.plot([dx + x1 * s, dx + x2 * s], [dy + y1 * s, dy + y2 * s], color=GREY, lw=1.6, zorder=0)
    w, h = 1.3 * s, 1.5 * s
    for k, v in enumerate(a):
        x, y = pos[k]
        card(ax, dx + x * s - w / 2, dy + y * s - h / 2, w, h, v, hot=(k in hot), gone=(k in gone), fs=fs)


# 1. 여는 장면: 할 일 카드, 숫자는 남은 날
fig, ax = canvas(11.0, 4.6, 18.0, 7.6)
kid(ax, 1.4, 0.6, 1.4)
ax.text(1.4, 0.1, "나", ha="center", va="center", fontsize=12, fontweight="bold")
cards = [(5, "그림"), (3, "받아쓰기"), (8, "독서록"), (1, "준비물"), (9, "만들기"), (4, "줄넘기"), (7, "일기")]
for k, (d, t) in enumerate(cards):
    x = 3.6 + k * 1.95
    card(ax, x, 2.0, 1.6, 2.0, d, fs=18)
    ax.text(x + 0.8, 1.6, t, ha="center", va="center", fontsize=10)
ax.text(10.2, 1.0, "숫자는 남은 날 수. 작을수록 급해요", ha="center", va="center", fontsize=11)
ax.text(10.2, 5.8, "제일 급한 것부터 하고 싶은데, 새 숙제도 자꾸 생겨요", ha="center", va="center", fontsize=12,
        bbox=dict(boxstyle="round,pad=0.4", fc="white", ec=INK, lw=1.2))
ax.text(17.4, 3.0, "?", ha="center", va="center", fontsize=30, color=RED, fontweight="bold")
save(fig, "a10-todo.svg")

# 2. 이 편의 지도
fig, ax = canvas(13.6, 2.9, 24.2, 4.6)
titles = ["다 뒤지기", "늘 정렬해 두기", "대진표 모양", "넣으면 올라가기", "꺼내면 내려가기"]
mini = {0: (1.9, 3.3), 1: (1.1, 2.5), 2: (2.7, 2.5), 3: (0.7, 1.7), 4: (1.5, 1.7), 5: (2.3, 1.7)}
for i, t in enumerate(titles):
    x = 0.3 + i * 4.8
    box(ax, x, 0.4, 3.8, 3.6)
    ax.text(x + 1.9, 0.95, t, ha="center", va="center", fontsize=12, fontweight="bold")
    if i == 0:
        row(ax, x + 0.3, 2.3, [5, 3, 8, 1], cw=0.6, ch=0.7, gap=0.15, fs=9, hot=(3,))
    elif i == 1:
        row(ax, x + 0.3, 2.3, [1, 3, 5, 8], cw=0.6, ch=0.7, gap=0.15, fs=9, hot=(0,))
    else:
        vals = [1, 3, 4, 5, 9] if i == 2 else ([1, 3, 4, 5, 9, 2] if i == 3 else [3, 5, 4, 9])
        hot = () if i == 2 else ((5,) if i == 3 else (0, 1))
        for k in range(len(vals)):
            for c in (2 * k + 1, 2 * k + 2):
                if c < len(vals):
                    ax.plot([x + mini[k][0], x + mini[c][0]], [mini[k][1] + 0.3, mini[c][1] + 0.3], color=GREY, lw=1)
            card(ax, x + mini[k][0] - 0.25, mini[k][1], 0.5, 0.55, vals[k], hot=(k in hot), fs=8)
        if i == 3:
            arrow(ax, (x + mini[5][0] + 0.35, mini[5][1] + 0.3), (x + mini[2][0] + 0.35, mini[2][1] + 0.1), color=RED,
                  lw=1.2, ms=9, rad=0.4)
    if i < 4:
        arrow(ax, (x + 3.95, 2.2), (x + 4.65, 2.2))
save(fig, "a10-map.svg")

# 3. 대진표 모양: 위 카드는 아래 두 카드보다 작아요
fig, ax = canvas(10.4, 6.0, 16.0, 10.4)
tree(ax, [1, 3, 4, 5, 9, 8, 7], dy=-0.6)
ax.text(8.0, 9.6, "맨 위 1이 제일 작아요", ha="center", va="center", fontsize=12, color=RED, fontweight="bold")
ax.text(8.0, 0.6, "선으로 이어진 위 카드는 늘 아래 두 카드보다 작아요. 아래 두 카드끼리는 순서가 없어요", ha="center",
        va="center", fontsize=11)
save(fig, "a10-heap.svg")

# 4. 넣으면 올라가기: 2를 넣기
fig, ax = canvas(13.6, 5.2, 27.0, 10.4)
stages = [([1, 3, 4, 5, 9, 8, 7, 2], (7,), "① 맨 아래 빈자리에 2"),
          ([1, 3, 4, 2, 9, 8, 7, 5], (3,), "② 위 카드 5보다 작아서 바꿔요"),
          ([1, 2, 4, 3, 9, 8, 7, 5], (1,), "③ 위 카드 3보다 작아서 바꿔요")]
for k, (a, hot, cap) in enumerate(stages):
    tree(ax, a, dx=0.3 + k * 9.0, dy=1.2, s=0.52, hot=hot, fs=10)
    ax.text(4.5 + k * 9.0, 0.6, cap, ha="center", va="center", fontsize=11, fontweight="bold")
    if k < 2:
        arrow(ax, (8.6 + k * 9.0, 4.0), (9.3 + k * 9.0, 4.0))
ax.text(13.5, 9.8, "위 카드 1보다는 크니까 멈춰요. 비교 3번", ha="center", va="center", fontsize=12, color=RED,
        fontweight="bold")
save(fig, "a10-push.svg")

# 5. 꺼내면 내려가기: 맨 위 1을 꺼내기
fig, ax = canvas(13.6, 5.2, 27.0, 10.4)
stages = [([5, 2, 4, 3, 9, 8, 7], (0,), "① 1을 꺼내고 맨 끝 5를 맨 위로"),
          ([2, 5, 4, 3, 9, 8, 7], (1,), "② 아래 2, 4 중 작은 2와 바꿔요"),
          ([2, 3, 4, 5, 9, 8, 7], (3,), "③ 아래 3, 9 중 작은 3과 바꿔요")]
for k, (a, hot, cap) in enumerate(stages):
    tree(ax, a, dx=0.3 + k * 9.0, dy=1.2, s=0.52, hot=hot, fs=10)
    ax.text(4.5 + k * 9.0, 0.6, cap, ha="center", va="center", fontsize=11, fontweight="bold")
    if k < 2:
        arrow(ax, (8.6 + k * 9.0, 4.0), (9.3 + k * 9.0, 4.0))
ax.text(13.5, 9.8, "아래에 카드가 없으면 멈춰요. 한 줄마다 비교 2번씩, 모두 4번", ha="center", va="center",
        fontsize=12, color=RED, fontweight="bold")
save(fig, "a10-pop.svg")

# 6. 카드 1,000장이면: 막대 (실제 비율)
fig, ax = canvas(10.4, 5.6, 17.0, 9.2)
base, scale = 1.4, 6.6 / 999
for k, (name, v, col) in enumerate([("다 뒤지기", 999, GREY), ("힙에서 꺼내기", 18, RED), ("힙에 넣기", 9, RED)]):
    bx = 2.0 + k * 4.6
    h = max(v * scale, 0.08)
    ax.add_patch(Rectangle((bx, base), 2.2, h, fc=col, ec=INK, lw=1.2))
    ax.text(bx + 1.1, base + h + 0.15, f"{v}번", ha="center", va="bottom", fontsize=13, fontweight="bold",
            color=RED if col == RED else "#222")
    ax.text(bx + 1.1, base - 0.3, name, ha="center", va="top", fontsize=12, fontweight="bold",
            color=RED if col == RED else "#222")
ax.plot([1.0, 16.0], [base, base], color=INK, lw=1.4)
ax.text(8.5, 0.2, "카드 1,000장에서 한 장을 꺼내거나 넣을 때 비교 수(많아야)", ha="center", va="center", fontsize=11)
save(fig, "a10-bars.svg")
