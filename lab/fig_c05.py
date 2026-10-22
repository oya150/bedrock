"""컴퓨터 5편 그림 만들기. 실행: python lab/fig_c05.py  → docs/computer/img/05/*.svg

글자는 SVG 안에 글자로 남긴다(글꼴 모양을 파일에 넣지 않는다). 보는 쪽 글꼴로 그려진다.
칠판은 짙은 초록, 공책은 흰 종이. 강조(사라지는 것, 옮기는 것)는 빨강 하나만 쓴다.
"""
import os

import matplotlib

matplotlib.use("svg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch, Rectangle

OUT = os.path.join(os.path.dirname(__file__), "..", "docs", "computer", "img", "05")
os.makedirs(OUT, exist_ok=True)

plt.rcParams.update({
    "font.family": ["Apple SD Gothic Neo", "Noto Sans KR", "Malgun Gothic", "sans-serif"],
    "svg.fonttype": "none",
    "text.color": "#222",
    "figure.facecolor": "white",
    "savefig.facecolor": "white",
})

RED, GREY, INK, PAPER, YEL = "#e4572e", "#c9ccd1", "#555", "#f4f6f8", "#f6c445"
BOARD = "#2f5d50"


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


def phone(ax, x, y, score, best, gone=False):
    box(ax, x, y, 3.2, 4.6, fc=PAPER)
    ax.add_patch(FancyBboxPatch((x + 1.2, y + 4.35), 0.8, 0.1, boxstyle="round,pad=0.02", fc=INK, ec=INK))
    ax.add_patch(Circle((x + 1.6, y + 0.25), 0.15, fc="white", ec=INK, lw=1.2))
    ax.text(x + 0.3, y + 3.9, f"점수 {score}", fontsize=14, fontweight="bold",
            color="#222")
    ax.text(x + 0.3, y + 3.2, f"최고 기록 {best}", fontsize=13)
    if gone:
        ax.add_patch(Rectangle((x + 0.2, y + 3.65), 2.2, 0.6, fc="none", ec=RED, lw=2.5))


def chalkboard(ax, x, y, w, h, text=None, size=20):
    ax.add_patch(Rectangle((x, y), w, h, fc=BOARD, ec="#7a5a3a", lw=5))
    if text:
        ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=size, color="white")


def notebook(ax, x, y, w, h, text=None, size=18):
    ax.add_patch(Rectangle((x, y), w, h, fc="white", ec=INK, lw=1.8))
    for k in range(1, 5):
        ax.plot([x + 0.2, x + w - 0.2], [y + k * h / 5.5, y + k * h / 5.5], color=GREY, lw=0.8)
    ax.add_patch(Rectangle((x - 0.15, y), 0.15, h, fc=INK, ec=INK))
    if text:
        ax.text(x + w / 2, y + h * 0.6, text, ha="center", va="center", fontsize=size)


def bulb(ax, cx, cy, r, on):
    ax.add_patch(Circle((cx, cy), r, fc=YEL if on else "#e6e8eb", ec="#b8901e" if on else "#9aa0a6", lw=1.2))
    ax.add_patch(Rectangle((cx - r * 0.45, cy - r * 1.45), r * 0.9, r * 0.5, fc="#9aa0a6", ec="none"))


# 1. 여는 장면: 끄기 전과 다시 켠 뒤
fig, ax = canvas(7.4, 3.8, 11, 5.8)
phone(ax, 0.4, 0.6, 40, 70, gone=True)
ax.text(2.0, 0.1, "끄기 전", ha="center", fontsize=13)
arrow(ax, (3.9, 2.9), (6.9, 2.9))
ax.text(5.4, 3.3, "끄고 다시 켜기", ha="center", fontsize=12, color=INK)
phone(ax, 7.3, 0.6, 0, 70)
ax.text(8.9, 0.1, "다시 켠 뒤", ha="center", fontsize=13)
save(fig, "c05-game.svg")

# 2. 이 편의 지도: 두 곳을 나란히(흐름 화살표 없이)
fig, ax = canvas(9.0, 3.4, 14, 5.2)
for x, kind, name, lines in [(0.4, "board", "메모리", ["지금 쓰는 숫자", "끄면 지워짐"]),
                             (7.2, "note", "저장 장치", ["오래 둘 숫자", "꺼도 남음"])]:
    box(ax, x, 0.4, 6.4, 4.4)
    if kind == "board":
        chalkboard(ax, x + 0.5, 1.6, 2.4, 1.8, "40", size=16)
    else:
        notebook(ax, x + 0.7, 1.6, 2.2, 1.8, "70", size=16)
    ax.text(x + 3.5, 3.6, name, fontsize=17, fontweight="bold", va="center")
    ax.text(x + 3.5, 2.6, lines[0], fontsize=13, va="center")
    ax.text(x + 3.5, 1.9, lines[1], fontsize=13, va="center", color=RED if "지워짐" in lines[1] else INK)
save(fig, "c05-map.svg")

# 3. 메모리 = 칠판: 40을 지우고 50
fig, ax = canvas(7.2, 3.0, 11, 4.6)
chalkboard(ax, 0.4, 0.8, 4.0, 2.8, "점수 40", size=22)
arrow(ax, (4.8, 2.2), (6.2, 2.2))
ax.text(5.5, 2.6, "지우고\n고쳐 쓰기", ha="center", va="bottom", fontsize=11, color=INK)
chalkboard(ax, 6.6, 0.8, 4.0, 2.8, "점수 50", size=22)
ax.text(5.5, 0.1, "메모리: 빨리 쓰고 빨리 지워요", ha="center", fontsize=13)
save(fig, "c05-board.svg")

# 4. 전원을 끄면 메모리가 지워진다
fig, ax = canvas(7.2, 3.0, 11, 4.6)
chalkboard(ax, 0.4, 0.8, 4.0, 2.8, "점수 40", size=22)
arrow(ax, (4.8, 2.2), (6.2, 2.2), color=RED, lw=2.5)
ax.text(5.5, 2.6, "전원 끄기", ha="center", va="bottom", fontsize=12, color=RED, fontweight="bold")
chalkboard(ax, 6.6, 0.8, 4.0, 2.8)
ax.text(8.6, 0.3, "메모리는 저절로 텅 비어요", ha="center", fontsize=13, color=RED)
ax.text(2.4, 0.3, "메모리", ha="center", fontsize=13)
save(fig, "c05-off.svg")

# 5. 저장 장치 = 공책: 최고 기록 70을 옮겨 적는다
fig, ax = canvas(7.4, 3.2, 11, 4.8)
chalkboard(ax, 0.4, 0.9, 4.0, 2.8, "최고 기록 70", size=18)
ax.add_patch(FancyArrowPatch((4.6, 2.3), (6.4, 2.3), arrowstyle="-|>", mutation_scale=20, color=RED, lw=2.5))
ax.text(5.5, 2.7, "옮겨 적기", ha="center", va="bottom", fontsize=12, color=RED, fontweight="bold")
notebook(ax, 6.8, 0.9, 3.6, 2.8, "최고 기록 70", size=16)
ax.text(8.6, 0.3, "저장 장치: 전원을 꺼도 그대로", ha="center", fontsize=13)
ax.text(2.4, 0.3, "메모리", ha="center", fontsize=13)
save(fig, "c05-notebook.svg")

# 6. 진짜 휴대폰 속: 전원을 끄면 메모리 전구는 다 꺼지고, 저장 장치 전구는 그대로
fig, ax = canvas(9.0, 4.4, 13.6, 6.6)
pattern = [1, 3, 4, 7]
ax.text(6.9, 6.2, "켜져 있을 때", ha="center", fontsize=12, color=INK)
ax.text(11.4, 6.2, "전원을 끈 뒤", ha="center", fontsize=12, color=RED, fontweight="bold")
box(ax, 0.1, 0.9, 2.8, 5.0, fc=PAPER)
ax.add_patch(FancyBboxPatch((1.1, 5.6), 0.8, 0.1, boxstyle="round,pad=0.02", fc=INK, ec=INK))
ax.text(1.5, 0.5, "휴대폰 속", ha="center", fontsize=11, color=INK)
for cy, label, keep in [(4.6, "메모리", False), (2.0, "저장 장치", True)]:
    ax.add_patch(Rectangle((0.4, cy - 0.5), 2.2, 1.0, fc=INK))
    ax.text(1.5, cy, label, ha="center", va="center", fontsize=12, color="white", fontweight="bold")
    for k in range(4):
        bulb(ax, 5.6 + k * 0.85, cy + 0.15, 0.28, k in (1, 3))
    arrow(ax, (9.2, cy + 0.15), (9.9, cy + 0.15), color=RED, lw=1.8)
    for k in range(4):
        bulb(ax, 10.2 + k * 0.85, cy + 0.15, 0.28, keep and k in (1, 3))
    ax.text(11.5, cy - 0.85, "그대로" if keep else "모두 꺼짐", ha="center", fontsize=12,
            color=INK if keep else RED, fontweight="bold")
    ax.add_patch(FancyArrowPatch((2.9, cy), (5.1, cy), arrowstyle="-|>", mutation_scale=14, color=GREY, lw=1.2))
ax.text(7.2, 0.4, "부품 속 전구(비트) 줄", ha="center", fontsize=12, color=INK)
save(fig, "c05-chips.svg")

print("ok")
