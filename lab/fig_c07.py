"""컴퓨터 7편 그림 만들기. 실행: python lab/fig_c07.py  → docs/computer/img/07/*.svg

글자는 SVG 안에 글자로 남긴다(글꼴 모양을 파일에 넣지 않는다). 보는 쪽 글꼴로 그려진다.
쪽지는 1편과 같은 연노랑, 강조(틀린 숫자·버그)는 빨강 하나만 쓴다.
"""
import os

import matplotlib

matplotlib.use("svg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch, Rectangle

OUT = os.environ.get("FIG_OUT") or os.path.join(os.path.dirname(__file__), "..", "docs", "computer", "img", "07")
FMT = os.environ.get("FIG_FMT", "svg")
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
    fig.savefig(os.path.join(OUT, name.replace(".svg", "." + FMT)), bbox_inches="tight", pad_inches=0.25)
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


def bug(ax, cx, cy, s=1.0):
    """버그: 몸통 타원, 머리, 다리 여섯, 더듬이 둘."""
    from matplotlib.patches import Ellipse
    for dy in (-0.18, 0.0, 0.18):
        ax.plot([cx - 0.42 * s, cx + 0.42 * s], [cy + dy * s, cy + dy * s * 1.6], color="#3a3a3a", lw=1.6)
    ax.add_patch(Ellipse((cx, cy), 0.55 * s, 0.75 * s, fc="#3a3a3a"))
    ax.add_patch(Circle((cx, cy + 0.45 * s), 0.16 * s, fc="#3a3a3a"))
    ax.plot([cx - 0.05 * s, cx - 0.22 * s], [cy + 0.55 * s, cy + 0.82 * s], color="#3a3a3a", lw=1.4)
    ax.plot([cx + 0.05 * s, cx + 0.22 * s], [cy + 0.55 * s, cy + 0.82 * s], color="#3a3a3a", lw=1.4)


def question(ax, x, y, size=26):
    ax.text(x, y, "?", ha="center", va="center", fontsize=size, color=RED, fontweight="bold")


def start_label(ax, x0, y0, c):
    ax.text(x0 + c / 2, y0 - c * 0.18, "출발", ha="center", va="top", fontsize=11, color=INK)


# 1. 여는 장면: 별 바로 앞에서 멈춘 캐릭터
fig, ax = canvas(7.2, 2.6, 12.4, 4.0)
path(ax, 0.2, 1.0, 6, 2.0, hero_at=4, star_at=5, numbers=True)
start_label(ax, 0.2, 1.0, 2.0)
question(ax, 0.2 + 4.5 * 2.0, 3.55)
save(fig, "c07-stuck.svg")

# 2. 적힌 대로: "4번 반복" 쪽지와 네 칸만 간 캐릭터
fig, ax = canvas(9.6, 2.6, 17.0, 4.2)
repeat_note(ax, 0.3, 1.0, 4.4, 4)
path(ax, 5.4, 1.1, 6, 1.9, hero_at=4, star_at=5, numbers=True)
start_label(ax, 5.4, 1.1, 1.9)
save(fig, "c07-wrong.svg")

# 3. 버그: 쪽지의 4에 빨간 동그라미와 벌레
fig, ax = canvas(6.4, 3.0, 10.4, 4.8)
box(ax, 0.6, 1.2, 5.2, 2.0, fc=NOTE)
ax.text(2.35, 2.75, "4", ha="center", va="center", fontsize=16, color=RED, fontweight="bold")
ax.text(3.45, 2.75, "번 반복", ha="center", va="center", fontsize=14, color=RED, fontweight="bold")
ax.add_patch(Circle((2.35, 2.75), 0.4, fc="none", ec=RED, lw=2.4))
box(ax, 0.9, 1.45, 4.6, 0.85, fc="white", ec=RED, lw=1.6)
ax.text(3.2, 1.88, "오른쪽으로 한 칸", ha="center", va="center", fontsize=13)
bug(ax, 8.4, 2.9, 1.3)
arrow(ax, (7.6, 3.75), (2.8, 3.05), color=RED)
ax.text(8.4, 1.0, "버그", ha="center", fontsize=15, fontweight="bold", color=RED)
save(fig, "c07-bug.svg")

# 4. 따라가며 세기: 손가락은 4번 칸, 별은 5번 칸, 한 칸 모자람
fig, ax = canvas(8.4, 3.0, 14.0, 5.0)
c, x0, y0 = 2.0, 0.6, 1.6
for k in range(6):
    ax.add_patch(Rectangle((x0 + k * c, y0), c, c, fc="white", ec=GREY, lw=1.2))
    if k > 0:
        ax.text(x0 + k * c + c * 0.12, y0 + c * 0.85, str(k), fontsize=11, color=INK)
start_label(ax, x0, y0, c)
star(ax, x0 + 5.5 * c, y0 + c * 0.5)
for k, w in enumerate(["하나", "둘", "셋", "넷"], start=1):
    ax.text(x0 + (k + 0.5) * c, y0 + c * 0.45, w, ha="center", va="center", fontsize=13, color=INK)
ax.add_patch(FancyArrowPatch((x0 + 0.5 * c, y0 + c + 0.15), (x0 + 4.5 * c, y0 + c + 0.15), arrowstyle="-|>",
                             mutation_scale=16, color=INK, lw=1.8, connectionstyle="arc3,rad=-0.18"))
# 손가락이 멈춘 곳과 별 사이의 빈틈
bx0, bx1 = x0 + 4.5 * c, x0 + 5.5 * c
ax.plot([bx0, bx0, bx1, bx1], [y0 - 0.35, y0 - 0.6, y0 - 0.6, y0 - 0.35], color=RED, lw=2.2)
ax.text((bx0 + bx1) / 2, y0 - 0.75, "1칸", ha="center", va="top", fontsize=14, color=RED, fontweight="bold")
save(fig, "c07-trace.svg")

# 5. 고치기: 4에 줄을 긋고 5, 캐릭터가 별 칸에 닿음
fig, ax = canvas(9.8, 2.8, 17.6, 4.6)
box(ax, 0.3, 1.0, 4.4, 2.0, fc=NOTE)
ax.text(1.2, 2.55, "4", ha="center", va="center", fontsize=15, color=INK, fontweight="bold")
ax.plot([0.95, 1.45], [2.25, 2.85], color=RED, lw=2.4)
ax.text(1.75, 2.55, "5번 반복", ha="left", va="center", fontsize=14, color=RED, fontweight="bold")
box(ax, 0.6, 1.25, 3.8, 0.85, fc="white", ec=RED, lw=1.6)
ax.text(2.5, 1.68, "오른쪽으로 한 칸", ha="center", va="center", fontsize=12)
path(ax, 5.4, 1.1, 6, 1.9, hero_at=5, numbers=True)
start_label(ax, 5.4, 1.1, 1.9)
star(ax, 5.4 + 5.5 * 1.9, 1.1 + 1.9 + 0.75, size=22)
save(fig, "c07-fix.svg")

# 6. 앱 업데이트 알림 (특정 제품 화면이 아닌 일반 모양)
fig, ax = canvas(4.2, 4.6, 6.6, 7.4)
ax.add_patch(FancyBboxPatch((1.4, 0.3), 3.8, 6.8, boxstyle="round,pad=0.25", fc=PAPER, ec=INK, lw=2.2))
box(ax, 1.75, 3.7, 3.1, 2.4, fc="white")
ax.add_patch(FancyBboxPatch((2.0, 5.15), 0.6, 0.6, boxstyle="round,pad=0.05", fc=YEL, ec="#b8901e"))
ax.text(2.85, 5.45, "업데이트", va="center", fontsize=12, fontweight="bold")
ax.text(3.3, 4.3, "버그 수정", ha="center", va="center", fontsize=14, color=RED, fontweight="bold")
bug(ax, 3.3, 2.2, 0.8)
ax.plot([2.6, 4.0], [1.5, 2.9], color=RED, lw=2.6)
save(fig, "c07-update.svg")

print("ok")
