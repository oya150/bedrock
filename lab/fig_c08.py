"""컴퓨터 8편 그림 만들기. 실행: python lab/fig_c08.py  → docs/computer/img/08/*.svg

글자는 SVG 안에 글자로 남긴다(글꼴 모양을 파일에 넣지 않는다). 보는 쪽 글꼴로 그려진다.
움직이는 공만 빨강으로 칠한다. 휴대폰은 특정 제품이 아닌 일반 모양이다.
"""
import os

import matplotlib

matplotlib.use("svg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch, Rectangle

OUT = os.path.join(os.path.dirname(__file__), "..", "docs", "computer", "img", "08")
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


def kid(ax, cx, ground, h):
    """공 차는 아이: 머리, 몸통, 다리 둘(한쪽은 앞으로 뻗음)."""
    ax.add_patch(Circle((cx, ground + h * 0.85), h * 0.13, fc="white", ec=INK, lw=1.6))
    ax.plot([cx, cx], [ground + h * 0.72, ground + h * 0.38], color=INK, lw=3)
    ax.plot([cx, cx - h * 0.12], [ground + h * 0.38, ground], color=INK, lw=3)
    ax.plot([cx, cx + h * 0.22], [ground + h * 0.38, ground + h * 0.12], color=INK, lw=3)
    ax.plot([cx - h * 0.18, cx + h * 0.18], [ground + h * 0.62, ground + h * 0.55], color=INK, lw=3)


def ball(ax, cx, cy, r):
    ax.add_patch(Circle((cx, cy), r, fc=RED, ec="#a33a1c", lw=1.2))


def frame(ax, x, y, w, h, ball_x, num=None, lw=1.6):
    """프레임 한 장: 바닥 선과 공 하나. ball_x 는 0~1 사이 위치."""
    ax.add_patch(Rectangle((x, y), w, h, fc="white", ec=INK, lw=lw))
    ax.plot([x + w * 0.08, x + w * 0.92], [y + h * 0.22, y + h * 0.22], color=GREY, lw=1.4)
    ball(ax, x + w * (0.15 + 0.7 * ball_x), y + h * 0.22 + h * 0.13, h * 0.13)
    if num is not None:
        ax.text(x + w / 2, y - h * 0.12, str(num), ha="center", va="top", fontsize=12, color=INK)


def phone(ax, x, y, w, h):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.2", fc=PAPER, ec=INK, lw=2.2))


def pause_icon(ax, cx, cy, s):
    ax.add_patch(Circle((cx, cy), s, fc="white", ec=INK, lw=2))
    for dx in (-0.3, 0.3):
        ax.add_patch(Rectangle((cx + dx * s - 0.12 * s, cy - 0.45 * s), 0.24 * s, 0.9 * s, fc=INK))


# 1. 여는 장면: 휴대폰 영상을 멈추면 공이 공중에 멈춘다
fig, ax = canvas(6.4, 4.2, 10.4, 6.8)
phone(ax, 0.6, 0.5, 9.2, 5.8)
ax.add_patch(Rectangle((1.1, 1.8), 8.2, 4.1, fc="white", ec=INK, lw=1.4))
ax.plot([1.4, 9.0], [2.3, 2.3], color=GREY, lw=1.6)
kid(ax, 3.6, 2.3, 2.8)
ball(ax, 6.2, 4.3, 0.42)
pause_icon(ax, 5.2, 1.1, 0.42)
save(fig, "c08-pause.svg")

# 2. 이 편의 지도: 멈춘 화면 한 장 → 사진 여러 장 → 빨리 넘기기 → 1초에 30장
fig, ax = canvas(11.6, 2.9, 19.4, 4.6)
titles = ["멈춘 화면 한 장", "사진 여러 장", "빨리 넘기기", "1초에 30장"]
for i, t in enumerate(titles):
    x = 0.3 + i * 4.8
    box(ax, x, 0.4, 3.8, 3.6)
    ax.text(x + 1.9, 0.95, t, ha="center", va="center", fontsize=13, fontweight="bold")
    if i == 0:
        frame(ax, x + 0.8, 1.6, 2.2, 1.7, 0.5)
    elif i == 1:
        for k in range(3):
            frame(ax, x + 0.5 + k * 0.35, 1.5 + k * 0.3, 2.2, 1.5, 0.2 + 0.3 * k, lw=1.2)
    elif i == 2:
        for k in range(4):
            ax.add_patch(Rectangle((x + 0.6 + k * 0.12, 1.5 + k * 0.08), 2.3, 1.6, fc="white", ec=GREY, lw=1.0))
        ball(ax, x + 2.2, 2.2, 0.22)
        ax.add_patch(FancyArrowPatch((x + 0.9, 3.55), (x + 3.0, 3.55), arrowstyle="-|>", mutation_scale=14,
                                     color=INK, lw=1.6, connectionstyle="arc3,rad=-0.3"))
    else:
        for k in range(30):
            r, c = divmod(k, 10)
            ax.add_patch(Rectangle((x + 0.35 + c * 0.31, 2.95 - r * 0.42), 0.26, 0.34, fc="white", ec=INK, lw=0.8))
    if i < 3:
        arrow(ax, (x + 3.95, 2.2), (x + 4.65, 2.2))
save(fig, "c08-map.svg")

# 3. 프레임: 멈춘 화면 한 장을 크게 보면 칸이 보인다(2편과 같은 모양)
fig, ax = canvas(8.6, 3.6, 14.4, 6.0)
frame(ax, 0.4, 1.3, 4.6, 3.4, 0.5)
ax.text(2.7, 0.6, "프레임 한 장", ha="center", fontsize=14, fontweight="bold")
ax.add_patch(Circle((2.7, 1.3 + 3.4 * 0.35), 0.75, fc="none", ec=INK, lw=1.6, ls="--"))
arrow(ax, (5.3, 3.0), (7.2, 3.0))
ax.text(6.25, 3.45, "크게 보기", ha="center", fontsize=12, color=INK)
n, c, x0, y0 = 8, 0.6, 7.6, 0.6
for r in range(n):
    for k in range(n):
        dx, dy = k - 3.5, r - 3.5
        inside = dx * dx + dy * dy <= 10
        ground = r == 0
        fc = RED if inside and not ground else (GREY if ground else "white")
        ax.add_patch(Rectangle((x0 + k * c, y0 + r * c), c, c, fc=fc, ec="#d9dce0", lw=0.8))
ax.text(x0 + n * c / 2, y0 + n * c + 0.35, "칸마다 색 번호", ha="center", fontsize=12, color=INK)
save(fig, "c08-frame.svg")

# 4. 공책 귀퉁이 그림: 공이 한 장마다 조금씩 옆으로
fig, ax = canvas(10.4, 2.8, 17.4, 4.6)
for k in range(5):
    frame(ax, 0.4 + k * 3.4, 1.4, 2.8, 2.2, k / 4, num=k + 1)
ax.add_patch(FancyArrowPatch((1.0, 4.2), (16.0, 4.2), arrowstyle="-|>", mutation_scale=18,
                             color=INK, lw=1.8))
ax.text(8.5, 4.45, "휘리릭 넘기기", ha="center", va="bottom", fontsize=13, color=INK)
save(fig, "c08-flip.svg")

# 5. 1초에 30장: "하나" 하고 셀 동안 지나가는 프레임
fig, ax = canvas(10.4, 3.9, 17.4, 6.4)
for k in range(30):
    r, col = divmod(k, 10)
    x, y = 0.4 + col * 1.7, 4.9 - r * 1.6
    frame(ax, x, y, 1.4, 1.1, k / 29, lw=1.0)
    ax.text(x + 0.7, y - 0.12, str(k + 1), ha="center", va="top", fontsize=9, color=INK)
ax.text(8.7, 0.1, "\"하나\" 하고 셀 동안 프레임 30장", ha="center", fontsize=14, fontweight="bold")
save(fig, "c08-second.svg")

# 6. 10초 영상: 1초마다 30장씩 쌓여 300장
fig, ax = canvas(10.4, 3.6, 17.4, 6.0)
for i in range(10):
    x = 0.4 + i * 1.7
    h = 0.42 * (i + 1)
    ax.add_patch(Rectangle((x, 1.2), 1.3, h, fc="white", ec=INK, lw=1.2))
    for k in range(1, i + 1):
        ax.plot([x, x + 1.3], [1.2 + 0.42 * k, 1.2 + 0.42 * k], color=GREY, lw=0.8)
    ax.text(x + 0.65, 1.2 + h + 0.12, f"{30 * (i + 1)}장", ha="center", va="bottom", fontsize=10,
            color=RED if i == 9 else INK, fontweight="bold" if i == 9 else "normal")
    ax.text(x + 0.65, 0.95, f"{i + 1}초", ha="center", va="top", fontsize=11, color=INK)
ax.text(8.65, 0.05, "1초마다 프레임이 30장씩 늘어나요", ha="center", fontsize=13, fontweight="bold")
save(fig, "c08-size.svg")

print("ok")
