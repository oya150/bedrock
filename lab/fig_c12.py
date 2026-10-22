"""컴퓨터 12편 그림 만들기. 실행: python lab/fig_c12.py  → docs/computer/img/12/*.svg

글자는 SVG 안에 글자로 남긴다(글꼴 모양을 파일에 넣지 않는다). 보는 쪽 글꼴로 그려진다.
찾는 낱말("바다")과 찾은 것만 빨강으로 칠한다. 휴대폰·도감은 특정 제품이 아닌 일반 모양이다.
"""
import os

import matplotlib

matplotlib.use("svg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch, Rectangle

OUT = os.path.join(os.path.dirname(__file__), "..", "docs", "computer", "img", "12")
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


def arrow(ax, a, b, color=INK, lw=2, rad=0.0):
    ax.add_patch(FancyArrowPatch(a, b, arrowstyle="-|>", mutation_scale=18, color=color, lw=lw,
                                 connectionstyle=f"arc3,rad={rad}"))


def phone_frame(ax, cx, y, h):
    w = h * 0.55
    ax.add_patch(FancyBboxPatch((cx - w / 2, y), w, h, boxstyle="round,pad=0.06", fc=PAPER, ec=INK, lw=2))
    ax.add_patch(Rectangle((cx - w / 2 + 0.12, y + 0.25), w - 0.24, h - 0.45, fc="white", ec=INK, lw=1))
    return cx - w / 2 + 0.12, y + 0.25, w - 0.24, h - 0.45


def msg(ax, x, y, w, h, text, red=False, size=10):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.04", fc=RED if red else PAPER,
                                ec=RED if red else GREY, lw=1))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=size,
            color="white" if red else "#222", fontweight="bold" if red else "normal")


def card(ax, x, y, w, h, num, text=None, red=False):
    """번호 붙은 메시지 카드."""
    ax.add_patch(Rectangle((x, y), w, h, fc=NOTE, ec=RED if red else INK, lw=2 if red else 1.2))
    ax.text(x + 0.12, y + h - 0.12, f"{num}번", ha="left", va="top", fontsize=9, color=INK)
    if text:
        ax.text(x + w / 2, y + h * 0.38, text, ha="center", va="center", fontsize=11,
                color=RED if red else "#222", fontweight="bold" if red else "normal")


def magnifier(ax, cx, cy, r, color=INK):
    ax.add_patch(Circle((cx, cy), r, fc="none", ec=color, lw=2.4))
    ax.plot([cx + r * 0.7, cx + r * 1.6], [cy - r * 0.7, cy - r * 1.6], color=color, lw=3.5,
            solid_capstyle="round")


def question(ax, x, y, size=28):
    ax.text(x, y, "?", ha="center", va="center", fontsize=size, color=RED, fontweight="bold")


# 1. 여는 장면: 위로 한참 올리기 vs 검색 칸에 "바다"
fig, ax = canvas(9.0, 4.4, 15.0, 7.4)
x, y, w, h = phone_frame(ax, 3.0, 0.5, 6.4)
for k in range(8):
    msg(ax, x + 0.2 + (0.6 if k % 2 else 0), y + 0.3 + k * 0.68, w - 1.0, 0.45, "…")
arrow(ax, (x + w + 0.55, y + 1.0), (x + w + 0.55, y + h - 0.6))
ax.text(x + w + 0.75, y + h / 2, "계속\n위로", ha="left", va="center", fontsize=11, color=INK)
question(ax, 7.5, 3.8)
x, y, w, h = phone_frame(ax, 12.0, 0.5, 6.4)
ax.add_patch(FancyBboxPatch((x + 0.15, y + h - 0.75), w - 0.3, 0.5, boxstyle="round,pad=0.04", fc="white",
                            ec=INK, lw=1.4))
magnifier(ax, x + 0.45, y + h - 0.5, 0.12)
ax.text(x + 0.75, y + h - 0.5, "바다", ha="left", va="center", fontsize=12, color=RED, fontweight="bold")
msg(ax, x + 0.2, y + h - 1.65, w - 0.4, 0.55, "바다 가자", red=True, size=11)
save(fig, "c12-find.svg")

# 2. 이 편의 지도: 하나씩 다 보기 → 찾아보기 → 표에서 찾기 → 바로 그 메시지
fig, ax = canvas(11.6, 2.9, 19.4, 4.6)
titles = ["하나씩 다 보기", "도감 찾아보기", "휴대폰 색인", "찾은 메시지"]
for i, t in enumerate(titles):
    x = 0.3 + i * 4.8
    box(ax, x, 0.4, 3.8, 3.6)
    ax.text(x + 1.9, 0.95, t, ha="center", va="center", fontsize=13, fontweight="bold")
    if i == 0:
        for k in range(5):
            ax.add_patch(Rectangle((x + 0.35 + k * 0.65, 1.9), 0.5, 0.7, fc=NOTE, ec=INK, lw=1))
        magnifier(ax, x + 0.6, 3.2, 0.25)
    elif i == 1:
        ax.add_patch(Rectangle((x + 0.9, 1.5), 2.0, 2.2, fc="white", ec=INK, lw=1.4))
        for k in range(4):
            yy = 3.3 - k * 0.42
            ax.plot([x + 1.1, x + 2.2], [yy, yy], color=GREY, lw=2)
            ax.text(x + 2.6, yy, str(12 + 9 * k), ha="right", va="center", fontsize=8, color=INK)
    elif i == 2:
        for k, (word, nums) in enumerate([("가자", "3, 8"), ("바다", "3, 17"), ("파란", "17")]):
            yy = 3.2 - k * 0.55
            red = word == "바다"
            ax.text(x + 0.7, yy, word, ha="left", va="center", fontsize=11, color=RED if red else "#222",
                    fontweight="bold" if red else "normal")
            ax.text(x + 2.1, yy, nums, ha="left", va="center", fontsize=11, color=RED if red else "#222",
                    fontweight="bold" if red else "normal")
    else:
        msg(ax, x + 0.5, 2.3, 2.8, 0.6, "바다 가자", red=True, size=12)
    if i < 3:
        arrow(ax, (x + 3.95, 2.2), (x + 4.65, 2.2))
save(fig, "c12-map.svg")

# 3. 하나씩 다 보기: 1번부터 차례로 돋보기가 옮겨 간다
fig, ax = canvas(11.0, 3.0, 18.4, 5.0)
for k in range(8):
    card(ax, 0.4 + k * 1.9, 1.6, 1.5, 1.6, k + 1)
ax.text(15.9, 2.4, "…", ha="center", va="center", fontsize=22, color=INK)
card(ax, 16.6, 1.6, 1.5, 1.6, 300)
magnifier(ax, 1.15, 2.3, 0.35)
for k in range(3):
    arrow(ax, (1.1 + k * 1.9, 3.5), (2.9 + k * 1.9, 3.5), rad=-0.4, lw=1.6)
ax.text(9.2, 0.7, "메시지가 300개면 300번 봐요", ha="center", fontsize=14, fontweight="bold")
save(fig, "c12-scan.svg")

# 4. 도감 맨 뒤 찾아보기
fig, ax = canvas(9.6, 4.2, 16.0, 7.0)
ax.add_patch(Rectangle((0.6, 0.6), 6.4, 5.8, fc="white", ec=INK, lw=2))
ax.text(3.8, 5.8, "찾아보기", ha="center", va="center", fontsize=15, fontweight="bold")
rows = [("브라키오사우루스", 18), ("스테고사우루스", 30), ("트리케라톱스", 36), ("티라노사우루스", 42)]
for k, (name, page) in enumerate(rows):
    yy = 4.8 - k * 0.95
    red = page == 42
    col = RED if red else "#222"
    ax.text(1.0, yy, name, ha="left", va="center", fontsize=12, color=col, fontweight="bold" if red else "normal")
    ax.plot([4.75, 5.95], [yy, yy], color=GREY, lw=1.2, ls=":")
    ax.text(6.6, yy, str(page), ha="right", va="center", fontsize=12, color=col,
            fontweight="bold" if red else "normal")
ax.text(3.8, 0.2, "도감 맨 뒤", ha="center", va="center", fontsize=12, color=INK)
arrow(ax, (7.2, 1.95), (9.4, 3.3), color=RED)
ax.add_patch(Rectangle((9.6, 0.6), 5.8, 5.8, fc="white", ec=INK, lw=2))
ax.text(12.5, 5.7, "42쪽", ha="center", va="center", fontsize=14, fontweight="bold", color=RED)
ax.text(12.5, 3.2, "티라노사우루스", ha="center", va="center", fontsize=14)
save(fig, "c12-book.svg")

# 5. 색인: 메시지에서 낱말을 떼어 표에 적고, "바다"만 찾는다
fig, ax = canvas(11.6, 4.6, 19.4, 7.6)
cards = [(3, "바다 가자"), (8, "같이 가자"), (17, "파란 바다")]
for k, (num, text) in enumerate(cards):
    card(ax, 0.4, 5.2 - k * 2.1, 3.6, 1.6, num, text)
arrow(ax, (4.3, 3.6), (6.6, 3.6))
ax.text(5.45, 4.1, "낱말로\n나눠 적기", ha="center", va="bottom", fontsize=11, color=INK)
ax.add_patch(Rectangle((6.9, 1.0), 5.6, 5.6, fc="white", ec=INK, lw=2))
ax.text(9.7, 6.15, "색인", ha="center", va="center", fontsize=14, fontweight="bold")
ax.plot([6.9, 12.5], [5.7, 5.7], color=INK, lw=1.2)
ax.plot([9.0, 9.0], [1.0, 5.7], color=GREY, lw=1)
index_rows = [("가자", "3, 8"), ("같이", "8"), ("바다", "3, 17"), ("파란", "17")]
for k, (word, nums) in enumerate(index_rows):
    yy = 5.1 - k * 1.1
    red = word == "바다"
    if red:
        ax.add_patch(Rectangle((6.95, yy - 0.45), 5.5, 0.9, fc="#fde4dc", ec=RED, lw=2))
    col = RED if red else "#222"
    ax.text(8.0, yy, word, ha="center", va="center", fontsize=13, color=col, fontweight="bold" if red else "normal")
    ax.text(10.75, yy, nums, ha="center", va="center", fontsize=13, color=col,
            fontweight="bold" if red else "normal")
ax.add_patch(FancyBboxPatch((14.2, 4.6), 3.6, 0.8, boxstyle="round,pad=0.05", fc="white", ec=INK, lw=1.6))
magnifier(ax, 14.65, 5.0, 0.18)
ax.text(15.2, 5.0, "바다", ha="left", va="center", fontsize=13, color=RED, fontweight="bold")
ax.text(16.0, 5.85, "검색 칸", ha="center", va="center", fontsize=11, color=INK)
arrow(ax, (14.1, 4.7), (12.6, 3.0), color=RED)
ax.text(16.0, 2.1, "3번, 17번", ha="center", va="center", fontsize=15, color=RED, fontweight="bold")
arrow(ax, (12.6, 2.6), (14.6, 2.2), color=RED)
save(fig, "c12-index.svg")

print("ok")
