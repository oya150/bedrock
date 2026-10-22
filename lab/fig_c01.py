"""컴퓨터 1편 그림 만들기. 실행: python lab/fig_c01.py  → docs/computer/img/01/*.svg

글자는 SVG 안에 글자로 남긴다(글꼴 모양을 파일에 넣지 않는다). 보는 쪽 글꼴로 그려진다.
강조색은 빨강 하나만 쓴다. 지금 보는 것에만 칠한다.
"""
import os

import matplotlib

matplotlib.use("svg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch, Rectangle

OUT = os.path.join(os.path.dirname(__file__), "..", "docs", "computer", "img", "01")
os.makedirs(OUT, exist_ok=True)

plt.rcParams.update({
    "font.family": ["Apple SD Gothic Neo", "Noto Sans KR", "Malgun Gothic", "sans-serif"],
    "svg.fonttype": "none",
    "text.color": "#222",
    "figure.facecolor": "white",
    "savefig.facecolor": "white",
})

RED, GREY, INK, PAPER, NOTE = "#e4572e", "#c9ccd1", "#555", "#f4f6f8", "#fffdf5"


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


def score_box(ax, x, y, label, value, color="#222", ec=INK):
    """이름표가 붙은 칸 하나. 이름표는 칸 바로 위에 둔다."""
    ax.text(x + 1.1, y + 1.75, label, ha="center", fontsize=13)
    box(ax, x, y, 2.2, 1.4, ec=ec, lw=2.2 if ec != INK else 1.8)
    ax.text(x + 1.1, y + 0.7, value, ha="center", va="center", fontsize=28, color=color, fontweight="bold")


# 1. 여는 장면: 게임이 끝나고 최고 기록이 바뀐 화면
fig, ax = canvas(6.4, 4.2, 10, 6.6)
box(ax, 0.3, 0.3, 9.4, 6.0, fc=PAPER)
ax.text(0.8, 5.5, "점수 70", fontsize=15, fontweight="bold")
ax.text(9.2, 5.5, "최고 기록 70", fontsize=15, ha="right")
ax.text(5.0, 3.6, "게임 끝", ha="center", fontsize=18, color=INK)
ax.text(5.0, 2.0, "새 기록!", ha="center", fontsize=28, color=RED, fontweight="bold")
save(fig, "c01-game.svg")

# 2. 이 편의 지도: 더하기 → 어느 쪽이 클까 → 바꿔 적기
fig, ax = canvas(9.0, 2.6, 13, 3.6)
steps = [("1", "더하기", "별을 먹으면"), ("2", "어느 쪽이 클까", "게임이 끝나면"), ("3", "바꿔 적기", "더 크면")]
for i, (n, name, ex) in enumerate(steps):
    x = 0.3 + i * 4.4
    box(ax, x, 0.4, 3.4, 2.6)
    ax.text(x + 0.35, 2.55, n, fontsize=13, color=INK, fontweight="bold")
    ax.text(x + 1.7, 2.0, name, ha="center", fontsize=17, fontweight="bold")
    ax.text(x + 1.7, 1.0, ex, ha="center", fontsize=14, color=INK)
    if i < 2:
        arrow(ax, (x + 3.55, 1.7), (x + 4.25, 1.7))
save(fig, "c01-map.svg")

# 3. 더하기: 점수 60에 10을 더해 70
fig, ax = canvas(8.0, 2.8, 11, 3.8)
score_box(ax, 0.4, 0.5, "점수", "60")
arrow(ax, (2.9, 1.2), (7.0, 1.2))
ax.plot(4.95, 2.2, marker="*", markersize=24, color=GREY)
ax.text(4.95, 1.45, "별 하나: 10 더하기", ha="center", fontsize=13)
score_box(ax, 7.3, 0.5, "점수", "70", color=RED, ec=RED)
save(fig, "c01-add.svg")

# 4. 비교: 70과 50 중 어느 쪽이 더 클까
fig, ax = canvas(7.4, 3.6, 10, 5.2)
ax.text(5.0, 4.6, "어느 쪽이 더 클까?", ha="center", fontsize=15, color=INK)
score_box(ax, 0.6, 1.2, "내 점수", "70", color=RED, ec=RED)
score_box(ax, 7.2, 1.2, "최고 기록", "50")
ax.text(1.7, 0.45, "70이 더 커요", ha="center", fontsize=14, color=RED, fontweight="bold")
save(fig, "c01-compare.svg")

# 5. 적기: 최고 기록 칸의 50을 지우고 70을 적는다(전과 후)
fig, ax = canvas(7.4, 3.2, 10, 4.4)
score_box(ax, 0.6, 1.2, "최고 기록 칸", "50", color=GREY)
arrow(ax, (3.2, 1.9), (6.8, 1.9), color=RED)
score_box(ax, 7.2, 1.2, "최고 기록 칸", "70", color=RED, ec=RED)
ax.text(5.0, 0.45, "50을 지우고 70을 적어요", ha="center", fontsize=13)
save(fig, "c01-write.svg")

# 6. 명령어: 미리 적어 둔 쪽지 네 장. 쪽지 한 장이 명령어 하나
fig, ax = canvas(8.4, 5.6, 11.5, 7.9)
orders = [("별을 먹을 때마다", "점수에 10 더하기"), ("게임이 끝나면", "점수와 최고 기록 비교하기"),
          ("점수가 더 크면", "최고 기록 바꿔 적기"), ("바꿔 적었으면", "화면에 새 기록! 띄우기")]
for i, t in enumerate(orders):
    y = 6.3 - i * 1.9
    box(ax, 0.9, y, 6.0, 1.1, fc=NOTE, ec=RED if i == 0 else INK, lw=2.2 if i == 0 else 1.8)
    ax.add_patch(Circle((0.35, y + 0.55), 0.3, fc="white", ec=INK, lw=1.5))
    ax.text(0.35, y + 0.55, str(i + 1), ha="center", va="center", fontsize=13, fontweight="bold")
    ax.text(1.2, y + 0.78, t[0], va="center", fontsize=11, color=INK)
    ax.text(1.2, y + 0.33, t[1], va="center", fontsize=14)
# 이름표는 쪽지 바로 옆에
arrow(ax, (8.6, 6.85), (7.15, 6.85), color=RED)
ax.text(8.75, 6.85, "쪽지 한 장\n= 명령어 하나", va="center", fontsize=14, color=RED, fontweight="bold")
save(fig, "c01-orders.svg")

# 7. 빠르기: 같은 1초 동안, 사람은 한 번, 컴퓨터는 셀 수 없이 많이
fig, ax = canvas(7.6, 4.8, 10.5, 7.6)
ax.text(4.0, 7.0, "같은 1초 동안", ha="center", fontsize=15, color=INK)
ax.add_patch(Circle((1.6, 3.6), 0.45, fc="white", ec=INK, lw=2))
ax.plot([1.6, 1.6], [3.15, 1.9], color=INK, lw=2.5)
ax.plot([1.0, 2.2], [2.8, 2.8], color=INK, lw=2.5)
ax.plot([1.6, 1.1], [1.9, 1.0], color=INK, lw=2.5)
ax.plot([1.6, 2.1], [1.9, 1.0], color=INK, lw=2.5)
box(ax, 2.6, 1.6, 1.3, 0.5, fc=NOTE)
ax.text(3.25, 1.85, "더하기", ha="center", va="center", fontsize=10)
ax.text(2.2, 0.3, "사람은 더하기 한 번", ha="center", fontsize=13)
box(ax, 5.3, 1.0, 2.6, 1.8, fc=PAPER)
ax.add_patch(Rectangle((6.3, 0.55), 0.6, 0.45, color=INK))
ax.text(6.6, 1.9, "컴퓨터", ha="center", va="center", fontsize=14)
# 쪽지 더미는 그림 위쪽 끝을 넘어가서 몇 장인지 셀 수 없게 그린다
for k in range(30):
    box(ax, 8.5, 1.0 + k * 0.4, 1.4, 0.3, fc=NOTE, ec=RED, lw=1.2)
    ax.text(9.2, 1.15 + k * 0.4, "더하기", ha="center", va="center", fontsize=8, clip_on=True)
ax.text(10.1, 6.2, "끝이\n안 보여요", fontsize=11, color=RED, va="center")
ax.text(7.4, 0.0, "컴퓨터는 셀 수 없이 많이", ha="center", fontsize=13, color=RED, fontweight="bold")
save(fig, "c01-speed.svg")

print("ok")
