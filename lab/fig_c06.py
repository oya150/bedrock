"""컴퓨터 6편 그림 만들기. 실행: python lab/fig_c06.py  → docs/computer/img/06/*.svg

확인용 PNG: FIG_FMT=png FIG_OUT=<폴더> python lab/fig_c06.py
그림 안 글씨는 낱말과 숫자만 둔다.

글자는 SVG 안에 글자로 남긴다(글꼴 모양을 파일에 넣지 않는다). 보는 쪽 글꼴로 그려진다.
쪽지는 1편과 같은 연노랑, 강조(반복 횟수)는 빨강 하나만 쓴다.
"""
import os

import matplotlib

FMT = os.environ.get("FIG_FMT", "svg")
matplotlib.use("svg" if FMT == "svg" else "agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch, Rectangle

OUT = os.environ.get("FIG_OUT") or os.path.join(os.path.dirname(__file__), "..", "docs", "computer", "img", "06")
os.makedirs(OUT, exist_ok=True)

plt.rcParams.update({
    "font.family": ["Apple SD Gothic Neo", "Noto Sans KR", "Malgun Gothic", "sans-serif"],
    "svg.fonttype": "none",
    "text.color": "#222",
    "figure.facecolor": "white",
    "savefig.facecolor": "white",
})

RED, GREY, INK, PAPER, NOTE, YEL = "#e4572e", "#c9ccd1", "#555", "#f4f6f8", "#fffdf5", "#f6c445"


def save(fig, name):
    name = name.rsplit(".", 1)[0] + "." + FMT
    fig.savefig(os.path.join(OUT, name), bbox_inches="tight", pad_inches=0.25, dpi=110)
    plt.close(fig)


def canvas(w, h, xmax, ymax):
    fig, ax = plt.subplots(figsize=(w, h))
    ax.set_xlim(0, xmax); ax.set_ylim(0, ymax); ax.axis("off")
    return fig, ax


def box(ax, x, y, w, h, fc="white", ec=INK, lw=1.8):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.08", fc=fc, ec=ec, lw=lw))


def arrow(ax, a, b, color=INK, lw=2):
    ax.add_patch(FancyArrowPatch(a, b, arrowstyle="-|>", mutation_scale=18, color=color, lw=lw))


def hero(ax, cx, cy, r):
    """캐릭터: 동그란 머리에 몸통."""
    ax.add_patch(Rectangle((cx - r * 0.6, cy - r * 1.6), r * 1.2, r * 1.2, fc=INK))
    ax.add_patch(Circle((cx, cy), r * 0.6, fc="white", ec=INK, lw=1.6))


def star(ax, cx, cy, size=26):
    ax.plot(cx, cy, marker="*", markersize=size, color=YEL, markeredgecolor="#b8901e")


def path(ax, x0, y0, n, c, hero_at=0, star_at=None, numbers=False):
    for k in range(n):
        ax.add_patch(Rectangle((x0 + k * c, y0), c, c, fc="white", ec=GREY, lw=1.2))
        if numbers and k > 0:
            ax.text(x0 + k * c + c * 0.12, y0 + c * 0.85, str(k), fontsize=11, color=INK)
    hero(ax, x0 + (hero_at + 0.5) * c, y0 + c * 0.68, c * 0.4)
    if star_at is not None:
        star(ax, x0 + (star_at + 0.5) * c, y0 + c * 0.5)


def note(ax, x, y, w, h, text, size=13, num=None):
    box(ax, x, y, w, h, fc=NOTE)
    ax.text(x + w / 2 + (0.2 if num else 0), y + h / 2, text, ha="center", va="center", fontsize=size)
    if num is not None:
        ax.add_patch(Circle((x - 0.35, y + h / 2), 0.25, fc="white", ec=INK, lw=1.3))
        ax.text(x - 0.35, y + h / 2, str(num), ha="center", va="center", fontsize=11, fontweight="bold")


def repeat_note(ax, x, y, w, times, inner="오른쪽으로 한 칸", size=13):
    box(ax, x, y, w, 2.0, fc=NOTE)
    ax.text(x + w / 2, y + 1.55, f"{times}번 반복", ha="center", va="center", fontsize=size + 1,
            color=RED, fontweight="bold")
    box(ax, x + 0.3, y + 0.25, w - 0.6, 0.85, fc="white", ec=RED, lw=1.6)
    ax.text(x + w / 2, y + 0.68, inner, ha="center", va="center", fontsize=size)


# 1. 여는 장면: 별까지 다섯 칸
fig, ax = canvas(7.2, 1.8, 12.4, 2.6)
path(ax, 0.2, 0.4, 6, 2.0, hero_at=0, star_at=5, numbers=True)
save(fig, "c06-path.svg")

# 3. 코드: 쪽지 다섯 장과 한 칸씩 가는 캐릭터
fig, ax = canvas(9.6, 5.0, 16.0, 8.2)
for k in range(5):
    y = 6.9 - k * 1.5
    note(ax, 0.9, y, 3.6, 0.95, "오른쪽으로 한 칸", num=k + 1)
    path(ax, 5.6, y - 0.25, 6, 1.45, hero_at=k + 1, star_at=5 if k < 4 else None, numbers=True)
    ax.text(14.6, y + 0.45, f"{k + 1}칸", ha="left", va="center", fontsize=12, color=INK)
save(fig, "c06-notes.svg")

# 3-1. 쪽지 백 장: 별이 백 칸 떨어져 있으면
fig, ax = canvas(6.4, 4.0, 10.0, 6.2)
for k in range(9):
    box(ax, 0.6 + k * 0.12, 0.4 + k * 0.55, 3.8, 0.7, fc=NOTE, lw=1.4)
ax.text(0.6 + 8 * 0.12 + 1.9, 0.4 + 8 * 0.55 + 0.35, "오른쪽으로 한 칸", ha="center", va="center", fontsize=11)
ax.text(2.9, 5.95, "⋮", ha="center", va="center", fontsize=18, color=INK)
ax.text(6.4, 3.0, "100장", ha="left", va="center", fontsize=26, color=RED, fontweight="bold")
save(fig, "c06-hundred.svg")

# 4. 반복: 쪽지 다섯 장 → 반복 쪽지 한 장
fig, ax = canvas(8.4, 3.6, 13.0, 5.6)
for k in range(5):
    note(ax, 0.3, 4.3 - k * 0.95, 3.6, 0.7, "오른쪽으로 한 칸", size=11)
arrow(ax, (4.4, 2.6), (6.6, 2.6))
ax.text(5.5, 3.0, "줄이기", ha="center", fontsize=12, color=INK)
repeat_note(ax, 7.2, 1.6, 5.0, 5)
ax.text(9.7, 0.6, "쪽지 한 장", ha="center", fontsize=13)
save(fig, "c06-repeat.svg")

# 5. 숫자만 바꾸면 된다
fig, ax = canvas(9.0, 3.0, 14.4, 4.6)
for i, (n, label) in enumerate([(5, "5칸"), (10, "10칸"), (100, "100칸")]):
    x = 0.3 + i * 4.8
    repeat_note(ax, x, 1.8, 4.0, n, size=12)
    ax.text(x + 2.0, 0.9, label, ha="center", fontsize=14, fontweight="bold")
    ax.text(x + 2.0, 0.3, "쪽지 1장", ha="center", fontsize=11, color=INK)
save(fig, "c06-more.svg")

# 5-1. 반복 안의 반복: 3번 반복 안에 5번 반복 → 15칸
fig, ax = canvas(10.9, 3.6, 17.8, 5.8)
box(ax, 0.3, 0.6, 5.4, 4.6, fc=NOTE)
ax.text(3.0, 4.7, "3번 반복", ha="center", va="center", fontsize=14, color=RED, fontweight="bold")
box(ax, 0.6, 0.9, 4.8, 3.2, fc="white", ec=RED, lw=1.6)
ax.text(3.0, 3.6, "5번 반복", ha="center", va="center", fontsize=13, color=INK, fontweight="bold")
box(ax, 0.95, 1.2, 4.1, 1.0, fc=NOTE, ec=INK, lw=1.4)
ax.text(3.0, 1.7, "오른쪽으로 한 칸", ha="center", va="center", fontsize=12)
c = 0.68
x0 = 6.6
for k in range(15):
    ax.add_patch(Rectangle((x0 + k * c, 2.6), c, c, fc="white", ec=GREY, lw=1.0))
for g in range(3):
    gx = x0 + g * 5 * c
    ax.plot([gx + 0.08, gx + 5 * c - 0.08], [2.35, 2.35], color=RED, lw=2)
    ax.plot([gx + 0.08, gx + 0.08], [2.35, 2.5], color=RED, lw=2)
    ax.plot([gx + 5 * c - 0.08, gx + 5 * c - 0.08], [2.35, 2.5], color=RED, lw=2)
    ax.text(gx + 2.5 * c, 1.9, "5칸", ha="center", va="center", fontsize=12, color=RED)
hero(ax, x0 + 0.5 * c, 2.6 + c * 0.68, c * 0.4)
star(ax, x0 + 15.5 * c, 2.6 + c * 0.5, size=20)
ax.text(x0 + 7.5 * c, 0.9, "3 × 5 = 15칸", ha="center", va="center", fontsize=15, fontweight="bold")
save(fig, "c06-nested.svg")

# 6. 진짜 코드: 블록 코드와 글 코드 (특정 제품 화면이 아닌 일반 모양)
fig, ax = canvas(9.0, 3.4, 14.4, 5.4)
# 블록 코드
ax.add_patch(FancyBboxPatch((0.4, 0.8), 5.6, 3.6, boxstyle="round,pad=0.1", fc="#f6c445", ec="#b8901e", lw=1.5))
ax.text(0.8, 3.8, "반복하기", fontsize=14, fontweight="bold", va="center")
ax.add_patch(FancyBboxPatch((3.3, 3.5), 1.0, 0.6, boxstyle="round,pad=0.05", fc="white", ec="#b8901e"))
ax.text(3.8, 3.8, "5", ha="center", va="center", fontsize=13, color=RED, fontweight="bold")
ax.text(4.5, 3.8, "번", fontsize=14, va="center")
ax.add_patch(FancyBboxPatch((1.2, 1.5), 4.4, 1.2, boxstyle="round,pad=0.08", fc="#7fb3d5", ec="#2e86ab", lw=1.5))
ax.text(3.4, 2.1, "오른쪽으로 한 칸", ha="center", va="center", fontsize=13)
ax.text(3.2, 0.1, "블록 코드", ha="center", fontsize=12, color=INK)
# 글 코드
ax.add_patch(Rectangle((7.2, 1.2), 6.8, 2.8, fc="#2b2b2b"))
ax.text(7.6, 3.2, "for i in range(", fontsize=13, color="white", family="monospace", va="center")
ax.text(10.88, 3.2, "5", fontsize=13, color=RED, family="monospace", va="center", fontweight="bold")
ax.text(11.18, 3.2, "):", fontsize=13, color="white", family="monospace", va="center")
ax.text(8.3, 2.0, "move_right()", fontsize=13, color="white", family="monospace", va="center")
ax.text(10.6, 0.1, "글로 쓴 코드", ha="center", fontsize=12, color=INK)
save(fig, "c06-real.svg")

print("ok")
