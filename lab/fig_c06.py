"""컴퓨터 6편 그림 만들기. 실행: python lab/fig_c06.py  → docs/computer/img/06/*.svg

글자는 SVG 안에 글자로 남긴다(글꼴 모양을 파일에 넣지 않는다). 보는 쪽 글꼴로 그려진다.
쪽지는 1편과 같은 연노랑, 강조(반복 횟수)는 빨강 하나만 쓴다.
"""
import os

import matplotlib

matplotlib.use("svg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch, Rectangle

OUT = os.path.join(os.path.dirname(__file__), "..", "docs", "computer", "img", "06")
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

# 2. 이 편의 지도
fig, ax = canvas(9.4, 2.8, 14.4, 4.4)
for i, t in enumerate(["쪽지 다섯 장", "반복 쪽지 한 장", "블록 코드"]):
    x = 0.3 + i * 4.9
    box(ax, x, 0.4, 3.8, 3.4)
    ax.text(x + 1.9, 0.95, t, ha="center", va="center", fontsize=13, fontweight="bold")
    if i == 0:
        for k in range(5):
            box(ax, x + 0.7 + k * 0.12, 1.7 + k * 0.28, 2.2, 0.5, fc=NOTE, lw=1.2)
    elif i == 1:
        repeat_note(ax, x + 0.4, 1.5, 3.0, 5, size=10)
    else:
        ax.add_patch(FancyBboxPatch((x + 0.5, 1.6), 2.8, 1.8, boxstyle="round,pad=0.05", fc=YEL, ec="#b8901e"))
        ax.text(x + 0.7, 3.05, "반복하기 5번", fontsize=10, va="center")
        ax.add_patch(FancyBboxPatch((x + 0.9, 1.85), 2.0, 0.6, boxstyle="round,pad=0.05", fc="#7fb3d5", ec="#2e86ab"))
        ax.text(x + 1.9, 2.15, "오른쪽으로 한 칸", fontsize=8, ha="center", va="center")
    if i < 2:
        arrow(ax, (x + 3.95, 2.1), (x + 4.75, 2.1))
save(fig, "c06-map.svg")

# 3. 코드: 쪽지 다섯 장과 한 칸씩 가는 캐릭터
fig, ax = canvas(9.6, 5.0, 16.0, 8.2)
for k in range(5):
    y = 6.9 - k * 1.5
    note(ax, 0.9, y, 3.6, 0.95, "오른쪽으로 한 칸", num=k + 1)
    path(ax, 5.6, y - 0.25, 6, 1.45, hero_at=k + 1, star_at=5 if k < 4 else None, numbers=True)
    ax.text(14.6, y + 0.45, f"{k + 1}칸 감", ha="left", va="center", fontsize=12, color=INK)
save(fig, "c06-notes.svg")

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
    ax.text(x + 2.0, 0.9, f"캐릭터가 {label}", ha="center", fontsize=13)
    ax.text(x + 2.0, 0.3, "쪽지는 한 장", ha="center", fontsize=11, color=INK)
save(fig, "c06-more.svg")

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
ax.text(11.05, 3.2, "5", fontsize=13, color=RED, family="monospace", va="center", fontweight="bold")
ax.text(11.35, 3.2, "):", fontsize=13, color="white", family="monospace", va="center")
ax.text(8.3, 2.0, "move_right()", fontsize=13, color="white", family="monospace", va="center")
ax.text(10.6, 0.1, "글로 쓴 코드", ha="center", fontsize=12, color=INK)
save(fig, "c06-real.svg")

print("ok")
