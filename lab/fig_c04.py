"""컴퓨터 4편 그림 만들기. 실행: python lab/fig_c04.py  → docs/computer/img/04/*.svg

글자는 SVG 안에 글자로 남긴다(글꼴 모양을 파일에 넣지 않는다). 보는 쪽 글꼴로 그려진다.
켜진 전구는 노랑, 꺼진 전구는 회색. 강조(더한 값)는 빨강 하나만 쓴다.
"""
import os

import matplotlib

matplotlib.use("svg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch, Rectangle

OUT = os.path.join(os.path.dirname(__file__), "..", "docs", "computer", "img", "04")
os.makedirs(OUT, exist_ok=True)

plt.rcParams.update({
    "font.family": ["Apple SD Gothic Neo", "Noto Sans KR", "Malgun Gothic", "sans-serif"],
    "svg.fonttype": "none",
    "text.color": "#222",
    "figure.facecolor": "white",
    "savefig.facecolor": "white",
})

RED, GREY, INK, PAPER, YEL = "#e4572e", "#c9ccd1", "#555", "#f4f6f8", "#f6c445"


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), bbox_inches="tight", pad_inches=0.25)
    plt.close(fig)


def canvas(w, h, xmax, ymax):
    fig, ax = plt.subplots(figsize=(w, h))
    ax.set_xlim(0, xmax); ax.set_ylim(0, ymax); ax.axis("off")
    return fig, ax


def box(ax, x, y, w, h, fc="white", ec=INK, lw=1.8):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.08", fc=fc, ec=ec, lw=lw))


def arrow(ax, a, b, color=INK, lw=2):
    ax.add_patch(FancyArrowPatch(a, b, arrowstyle="-|>", mutation_scale=18, color=color, lw=lw))


def bulb(ax, cx, cy, r, on):
    """전구 하나: 둥근 유리와 아래 받침."""
    ax.add_patch(Circle((cx, cy), r, fc=YEL if on else "#e6e8eb", ec="#b8901e" if on else "#9aa0a6", lw=1.5))
    ax.add_patch(Rectangle((cx - r * 0.45, cy - r * 1.45), r * 0.9, r * 0.5, fc="#9aa0a6", ec="none"))


def dots(ax, cx, cy, n, size=4.0, width=1.2):
    """점 n개를 줄 맞춰 찍는다. 많으면 숫자로만 적는다."""
    if n > 8:
        ax.text(cx, cy, f"점 {n}", ha="center", va="center", fontsize=11, color=INK)
        return
    cols = min(n, 4)
    rows = (n + cols - 1) // cols
    gap = width / 4
    for i in range(n):
        r, c = divmod(i, cols)
        x = cx + (c - (cols - 1) / 2) * gap
        y = cy - (r - (rows - 1) / 2) * gap
        ax.plot(x, y, "o", ms=size, color="#222")


def bulb_row(ax, x0, y, values, on, r=0.45, step=1.4, label_dots=True):
    """values 순서대로 전구를 놓고, 전구 아래에 점(값)을 붙인다."""
    for i, (v, o) in enumerate(zip(values, on)):
        cx = x0 + i * step
        bulb(ax, cx, y, r, o)
        if label_dots:
            dots(ax, cx, y - r * 2.4, v)


# 1. 여는 장면: 벽 스위치 켜짐/꺼짐
fig, ax = canvas(6.4, 3.6, 10, 5.6)
for x, on, label in [(1.0, True, "켜짐"), (5.6, False, "꺼짐")]:
    box(ax, x, 0.9, 1.6, 2.4, fc=PAPER)
    ax.add_patch(Rectangle((x + 0.45, 1.25), 0.7, 1.8, fc="white", ec=INK, lw=1.5))
    ax.add_patch(Rectangle((x + 0.5, 2.15 if on else 1.3), 0.6, 0.85, fc=INK, ec=INK))
    bulb(ax, x + 3.0, 3.4, 0.6, on)
    ax.text(x + 1.9, 0.3, label, ha="center", fontsize=15, fontweight="bold")
save(fig, "c04-switch.svg")

# 2. 이 편의 지도
fig, ax = canvas(10.4, 2.8, 16.8, 4.4)
steps = ["전구 하나", "전구 네 개", "켜진 전구\n더하기", "컴퓨터 속 A"]
for i, t in enumerate(steps):
    x = 0.3 + i * 4.2
    box(ax, x, 0.4, 3.2, 3.4)
    ax.text(x + 1.6, 1.0, t, ha="center", va="center", fontsize=13, fontweight="bold")
    if i == 0:
        bulb(ax, x + 1.6, 2.7, 0.4, True)
    elif i == 1:
        for k in range(4):
            bulb(ax, x + 0.65 + k * 0.63, 2.7, 0.24, k in (1, 3))
    elif i == 2:
        ax.text(x + 1.6, 2.6, "4 + 1 = 5", ha="center", va="center", fontsize=15, color=RED, fontweight="bold")
    else:
        box(ax, x + 0.8, 2.0, 1.6, 1.2, fc=PAPER)
        ax.text(x + 1.6, 2.6, "A", ha="center", va="center", fontsize=18, color=INK, fontweight="bold")
    if i < 3:
        arrow(ax, (x + 3.35, 2.1), (x + 4.05, 2.1))
save(fig, "c04-map.svg")

# 3. 전구 하나: 꺼짐 0, 켜짐 1
fig, ax = canvas(5.0, 3.0, 8, 4.8)
for x, on, v in [(2.0, False, "0"), (6.0, True, "1")]:
    bulb(ax, x, 3.0, 0.8, on)
    ax.text(x, 0.6, v, ha="center", fontsize=30, fontweight="bold", color=RED if on else "#222")
    ax.text(x, 4.3, "켜짐" if on else "꺼짐", ha="center", fontsize=13, color=INK)
save(fig, "c04-one.svg")

# 4. 전구 네 개로 5: 4와 1이 켜짐
fig, ax = canvas(6.6, 3.8, 10, 5.8)
vals = [8, 4, 2, 1]
bulb_row(ax, 1.6, 3.9, vals, [False, True, False, True], r=0.55, step=2.2)
ax.text(5.0, 0.4, "4 + 1 = 5", ha="center", fontsize=22, color=RED, fontweight="bold")
save(fig, "c04-five.svg")

# 5. 여러 수: 0, 3, 6, 15
fig, ax = canvas(6.4, 6.0, 10, 9.6)
rows = [(0, [False] * 4, "모두 꺼짐 = 0"), (3, [False, False, True, True], "2 + 1 = 3"),
        (6, [False, True, True, False], "4 + 2 = 6"), (15, [True] * 4, "8 + 4 + 2 + 1 = 15")]
for k in range(4):
    ax.text(0.8 + k * 1.2, 9.1, f"점 {vals[k]}", ha="center", va="center", fontsize=11, color=INK)
for j, (n, on, label) in enumerate(rows):
    y = 7.6 - j * 2.1
    bulb_row(ax, 0.8, y, vals, on, r=0.38, step=1.2, label_dots=False)
    ax.text(5.6, y, label, va="center", fontsize=15, color=RED if n else INK, fontweight="bold")
save(fig, "c04-many.svg")

# 6. 진짜 컴퓨터: 여덟 개 묶음, A = 65 = 64 + 1
fig, ax = canvas(9.0, 3.4, 15, 5.4)
vals8 = [128, 64, 32, 16, 8, 4, 2, 1]
on8 = [v in (64, 1) for v in vals8]
for i, (v, o) in enumerate(zip(vals8, on8)):
    cx = 0.9 + i * 1.5
    bulb(ax, cx, 3.6, 0.5, o)
    # 켜진 전구(64, 1)만 또렷하게, 나머지 점 수는 흐리게 적는다
    ax.text(cx, 2.1, f"점\n{v}", ha="center", va="center", fontsize=12 if o else 10, color=RED if o else GREY,
            fontweight="bold" if o else "normal")
ax.text(13.3, 3.6, "A", ha="center", va="center", fontsize=34, fontweight="bold")
ax.text(7.0, 0.5, "64 + 1 = 65,  65번은 A", ha="center", fontsize=18, color=RED, fontweight="bold")
save(fig, "c04-letter-a.svg")

print("ok")
