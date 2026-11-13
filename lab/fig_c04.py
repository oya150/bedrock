"""컴퓨터 4편 그림 만들기. 실행: python lab/fig_c04.py  → docs/computer/img/04/*.svg

확인용 PNG: FIG_FMT=png FIG_OUT=<폴더> python lab/fig_c04.py
글자는 SVG 안에 글자로 남긴다(글꼴 모양을 파일에 넣지 않는다). 보는 쪽 글꼴로 그려진다.
켜진 전구는 노랑, 꺼진 전구는 회색. 강조(지금 볼 값)는 빨강 하나만 쓴다.
"""
import os

import matplotlib

matplotlib.use("svg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyBboxPatch, Rectangle

FMT = os.environ.get("FIG_FMT", "svg")
OUT = os.environ.get("FIG_OUT") or os.path.join(os.path.dirname(__file__), "..", "docs", "computer", "img", "04")
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
    fig.savefig(os.path.join(OUT, name.replace(".svg", "." + FMT)), bbox_inches="tight", pad_inches=0.25,
                dpi=110)
    plt.close(fig)


def canvas(w, h, xmax, ymax):
    fig, ax = plt.subplots(figsize=(w, h))
    ax.set_xlim(0, xmax); ax.set_ylim(0, ymax); ax.axis("off")
    return fig, ax


def box(ax, x, y, w, h, fc="white", ec=INK, lw=1.8):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.08", fc=fc, ec=ec, lw=lw))


def bulb(ax, cx, cy, r, on):
    """전구 하나: 둥근 유리와 아래 받침."""
    ax.add_patch(Circle((cx, cy), r, fc=YEL if on else "#e6e8eb", ec="#b8901e" if on else "#9aa0a6", lw=1.5))
    ax.add_patch(Rectangle((cx - r * 0.45, cy - r * 1.45), r * 0.9, r * 0.5, fc="#9aa0a6", ec="none"))


def dots(ax, cx, cy, n, size=4.0, width=1.2):
    """점 n개를 줄 맞춰 찍는다."""
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


vals = [8, 4, 2, 1]

# 1. 여는 장면: 벽 스위치 켜짐/꺼짐
fig, ax = canvas(6.4, 3.6, 10, 5.6)
for x, on, label in [(1.0, True, "켜짐"), (5.6, False, "꺼짐")]:
    box(ax, x, 0.9, 1.6, 2.4, fc=PAPER)
    ax.add_patch(Rectangle((x + 0.45, 1.25), 0.7, 1.8, fc="white", ec=INK, lw=1.5))
    ax.add_patch(Rectangle((x + 0.5, 2.15 if on else 1.3), 0.6, 0.85, fc=INK, ec=INK))
    bulb(ax, x + 3.0, 3.4, 0.6, on)
    ax.text(x + 1.9, 0.3, label, ha="center", fontsize=15, fontweight="bold")
save(fig, "c04-switch.svg")

# 2. 전구 하나: 꺼짐 0, 켜짐 1
fig, ax = canvas(5.0, 3.0, 8, 4.8)
for x, on, v in [(2.0, False, "0"), (6.0, True, "1")]:
    bulb(ax, x, 3.0, 0.8, on)
    ax.text(x, 0.6, v, ha="center", fontsize=30, fontweight="bold", color=RED if on else "#222")
    ax.text(x, 4.3, "켜짐" if on else "꺼짐", ha="center", fontsize=13, color=INK)
save(fig, "c04-one.svg")

# 3. 켜진 전구 개수만 세면: 0, 1, 2, 3, 4 다섯 가지뿐
fig, ax = canvas(5.6, 6.6, 9, 10.6)
for n in range(5):
    y = 9.4 - n * 2.1
    bulb_row(ax, 0.9, y, vals, [k < n for k in range(4)], r=0.38, step=1.2, label_dots=False)
    ax.text(6.6, y, str(n), va="center", ha="center", fontsize=20, fontweight="bold", color=RED if n == 4 else "#222")
save(fig, "c04-count.svg")

# 4. 전구 네 개로 5: 4와 1이 켜짐
fig, ax = canvas(6.6, 3.8, 10, 5.8)
bulb_row(ax, 1.6, 3.9, vals, [False, True, False, True], r=0.55, step=2.2)
ax.text(5.0, 0.4, "4 + 1 = 5", ha="center", fontsize=22, color=RED, fontweight="bold")
save(fig, "c04-five.svg")

# 5. 여러 수: 0, 3, 6, 15
fig, ax = canvas(6.4, 6.0, 10, 9.6)
rows = [(0, [False] * 4, "0"), (3, [False, False, True, True], "2 + 1 = 3"),
        (6, [False, True, True, False], "4 + 2 = 6"), (15, [True] * 4, "8 + 4 + 2 + 1 = 15")]
for k in range(4):
    ax.text(0.8 + k * 1.2, 9.1, f"점 {vals[k]}", ha="center", va="center", fontsize=11, color=INK)
for j, (n, on, label) in enumerate(rows):
    y = 7.6 - j * 2.1
    bulb_row(ax, 0.8, y, vals, on, r=0.38, step=1.2, label_dots=False)
    ax.text(5.6, y, label, va="center", fontsize=15, color=RED if n == 15 else "#222", fontweight="bold")
save(fig, "c04-many.svg")

# 6. 전구 하나를 더 놓으면 16
fig, ax = canvas(7.4, 3.2, 12, 5.0)
vals5 = [16, 8, 4, 2, 1]
for i, v in enumerate(vals5):
    cx = 1.2 + i * 1.8
    new = i == 0
    bulb(ax, cx, 3.4, 0.5, new)
    ax.text(cx, 2.0, f"점 {v}", ha="center", va="center", fontsize=13, color=RED if new else INK,
            fontweight="bold" if new else "normal")
ax.add_patch(Rectangle((0.4, 1.5), 1.6, 2.7, fill=False, ec=RED, lw=2, ls="--"))
ax.text(5.0, 0.6, "16", ha="center", fontsize=22, color=RED, fontweight="bold")
save(fig, "c04-sixteen.svg")

# 7. 진짜 컴퓨터: 여덟 개 묶음, A = 65 = 64 + 1
fig, ax = canvas(9.0, 3.4, 15, 5.4)
vals8 = [128, 64, 32, 16, 8, 4, 2, 1]
on8 = [v in (64, 1) for v in vals8]
for i, (v, o) in enumerate(zip(vals8, on8)):
    cx = 0.9 + i * 1.5
    bulb(ax, cx, 3.6, 0.5, o)
    ax.text(cx, 2.1, f"점\n{v}", ha="center", va="center", fontsize=12 if o else 10, color=RED if o else INK,
            fontweight="bold" if o else "normal")
ax.text(13.3, 3.6, "A", ha="center", va="center", fontsize=34, fontweight="bold")
ax.text(7.0, 0.5, "64 + 1 = 65", ha="center", fontsize=18, color=RED, fontweight="bold")
save(fig, "c04-letter-a.svg")

# 8. 가(44032)를 적으려면 전구 16개: 32768 + 8192 + 2048 + 1024
fig, ax = canvas(10.0, 5.6, 16, 9.0)
vals16 = [2 ** k for k in range(15, -1, -1)]
lit = {32768, 8192, 2048, 1024}
assert sum(lit) == ord("가")
for i, v in enumerate(vals16):
    row, col = divmod(i, 8)
    cx, cy = 1.0 + col * 1.8, 7.6 - row * 3.2
    o = v in lit
    bulb(ax, cx, cy, 0.45, o)
    ax.text(cx, cy - 1.15, str(v), ha="center", va="center", fontsize=11 if o else 9.5,
            color=RED if o else INK, fontweight="bold" if o else "normal")
ax.text(15.3, 7.6, "가", ha="center", va="center", fontsize=30, fontweight="bold")
ax.text(7.3, 0.5, "32768 + 8192 + 2048 + 1024 = 44032", ha="center", fontsize=16, color=RED, fontweight="bold")
save(fig, "c04-ga.svg")

print("ok")
