"""알고리즘 1편 그림 만들기. 실행: python lab/fig_01.py  → docs/algorithms/img/01/*.svg

글자는 SVG 안에 글자로 남긴다(글꼴 모양을 파일에 넣지 않는다). 보는 쪽 글꼴로 그려진다.
양말은 차분한 색으로 칠하고, 강조(짝, 늘어나는 칸, 256)만 빨강으로 칠한다.
"""
import os

import matplotlib

matplotlib.use("svg")
import matplotlib.pyplot as plt
from matplotlib.patches import Arc, Circle, Ellipse, FancyArrowPatch, FancyBboxPatch, Polygon, Rectangle

OUT = os.path.join(os.path.dirname(__file__), "..", "docs", "algorithms", "img", "01")
os.makedirs(OUT, exist_ok=True)

plt.rcParams.update({
    "font.family": ["Apple SD Gothic Neo", "Noto Sans KR", "Malgun Gothic", "sans-serif"],
    "svg.fonttype": "none",
    "text.color": "#222",
    "figure.facecolor": "white",
    "savefig.facecolor": "white",
})

RED, GREY, INK, PAPER, NOTE, YEL = "#e4572e", "#c9ccd1", "#555", "#f4f6f8", "#fffdf5", "#f6c445"
BLUE, GREEN, PURPLE, BASKET = "#7da2c8", "#8fb58f", "#b59cc8", "#e8d3b0"
SOCKS = [BLUE, GREEN, YEL, PURPLE]


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


def sock(ax, x, y, s, color, flip=False):
    """양말 한 짝: 발목 기둥과 발. (x, y)는 발목 위 왼쪽. flip 이면 발이 왼쪽으로."""
    if flip:
        pts = [(x, y), (x + 0.45 * s, y), (x + 0.45 * s, y - 1.05 * s), (x - 0.45 * s, y - 1.05 * s),
               (x - 0.45 * s, y - 0.75 * s), (x, y - 0.75 * s)]
    else:
        pts = [(x, y), (x + 0.45 * s, y), (x + 0.45 * s, y - 0.75 * s), (x + 0.9 * s, y - 0.75 * s),
               (x + 0.9 * s, y - 1.05 * s), (x, y - 1.05 * s)]
    ax.add_patch(Polygon(pts, closed=True, fc=color, ec=INK, lw=1.2))
    ax.plot([x, x + 0.45 * s], [y - 0.15 * s, y - 0.15 * s], color="white", lw=1.5)


def basket(ax, cx, y, w, h):
    ax.add_patch(Polygon([(cx - w / 2, y + h), (cx + w / 2, y + h), (cx + w * 0.4, y), (cx - w * 0.4, y)],
                         closed=True, fc=BASKET, ec=INK, lw=1.8))
    for k in range(1, 4):
        yy = y + h * k / 4
        half = w * (0.4 + 0.1 * k / 4)
        ax.plot([cx - half, cx + half], [yy, yy], color="#c9b28c", lw=1)


def face(ax, cx, cy, r, happy=True):
    ax.add_patch(Circle((cx, cy), r, fc="white", ec=INK, lw=1.6))
    ax.add_patch(Circle((cx - r * 0.35, cy + r * 0.2), r * 0.09, fc=INK))
    ax.add_patch(Circle((cx + r * 0.35, cy + r * 0.2), r * 0.09, fc=INK))
    if happy:
        ax.add_patch(Arc((cx, cy - r * 0.1), r, r * 0.7, theta1=200, theta2=340, color=INK, lw=1.6))
    else:
        ax.add_patch(Arc((cx, cy - r * 0.55), r * 0.8, r * 0.5, theta1=20, theta2=160, color=INK, lw=1.6))
        ax.add_patch(Ellipse((cx + r * 1.15, cy + r * 0.5), r * 0.25, r * 0.4, fc="#9cc9e8", ec=INK, lw=0.8))


def question(ax, x, y, size=28):
    ax.text(x, y, "?", ha="center", va="center", fontsize=size, color=RED, fontweight="bold")


def grid(ax, x0, y0, n, c, label):
    for r in range(n):
        for k in range(n):
            ax.add_patch(Rectangle((x0 + k * c, y0 + r * c), c, c, fc="white", ec=GREY, lw=0.8))
    ax.add_patch(Rectangle((x0, y0), n * c, n * c, fc="none", ec=INK, lw=1.6))
    ax.text(x0 + n * c / 2, y0 - 0.3, label, ha="center", va="top", fontsize=13, fontweight="bold")


# 1. 여는 장면: 양말이 적을 땐 금방, 많아지면 한참
fig, ax = canvas(9.0, 3.8, 15.0, 6.4)
basket(ax, 3.0, 0.8, 3.0, 1.6)
for k in range(4):
    sock(ax, 1.6 + k * 0.95 + (0.4 if k % 2 else 0), 3.3, 0.6, SOCKS[k // 2], flip=k % 2)
face(ax, 3.0, 5.1, 0.55, happy=True)
question(ax, 7.5, 3.2)
basket(ax, 12.0, 0.8, 4.4, 2.2)
for k in range(12):
    r, col = divmod(k, 6)
    sock(ax, 10.1 + col * 0.75, 3.75 + r * 0.6, 0.5, SOCKS[k % 4])
face(ax, 12.0, 5.75, 0.5, happy=False)
save(fig, "a01-basket.svg")

# 2. 이 편의 지도
fig, ax = canvas(11.6, 2.9, 19.4, 4.6)
titles = ["하나 집고 다 뒤지기", "색깔 자리에 놓기", "두 배면 몇 배", "빅오"]
for i, t in enumerate(titles):
    x = 0.3 + i * 4.8
    box(ax, x, 0.4, 3.8, 3.6)
    ax.text(x + 1.9, 0.95, t, ha="center", va="center", fontsize=12, fontweight="bold")
    if i == 0:
        basket(ax, x + 2.4, 1.6, 1.8, 1.0)
        sock(ax, x + 0.5, 3.6, 0.55, BLUE)
        arrow(ax, (x + 1.15, 3.0), (x + 1.7, 2.6), lw=1.5)
    elif i == 1:
        for k in range(4):
            ax.add_patch(Ellipse((x + 0.65 + k * 0.85, 2.0), 0.7, 0.35, fc=SOCKS[k], ec=INK, lw=1, alpha=0.6))
        sock(ax, x + 0.45, 3.55, 0.5, BLUE)
        sock(ax, x + 1.25, 3.55, 0.5, BLUE, flip=True)
    elif i == 2:
        for k, (h1, h2) in enumerate([(0.3, 0.2), (1.2, 0.4)]):
            bx = x + 0.6 + k * 1.5
            ax.add_patch(Rectangle((bx, 1.5), 0.5, h1 * 1.6, fc=RED, ec=INK, lw=1))
            ax.add_patch(Rectangle((bx + 0.55, 1.5), 0.5, h2 * 1.6, fc=BLUE, ec=INK, lw=1))
    else:
        ax.text(x + 1.9, 2.8, "두 배 → 네 배", ha="center", va="center", fontsize=12, color=RED, fontweight="bold")
        ax.text(x + 1.9, 2.1, "두 배 → 두 배", ha="center", va="center", fontsize=12, color=INK, fontweight="bold")
    if i < 3:
        arrow(ax, (x + 3.95, 2.2), (x + 4.65, 2.2))
save(fig, "a01-map.svg")

# 3. 방법 1의 칸 그림: 양말 4개는 16칸, 8개는 64칸(16칸 네모가 네 개)
fig, ax = canvas(10.0, 5.0, 16.6, 8.4)
c = 0.62
grid(ax, 0.8, 2.6, 4, c, "양말 4개: 16칸")
grid(ax, 7.4, 1.2, 8, c, "양말 8개: 64칸")
for dx, dy in ((0, 0), (4, 0), (0, 4), (4, 4)):
    ax.add_patch(Rectangle((7.4 + dx * c, 1.2 + dy * c), 4 * c, 4 * c, fc="none", ec=RED, lw=2.4))
ax.text(2.04, 5.3, "가로: 집은 양말", ha="center", va="bottom", fontsize=10, color=INK)
ax.text(0.65, 2.6 + 2 * c, "세로: 바구니 속 양말", ha="right", va="center", fontsize=10, color=INK)
arrow(ax, (3.6, 3.85), (7.1, 3.85))
ax.text(5.35, 4.15, "양말 두 배", ha="center", va="bottom", fontsize=12, color=INK)
ax.text(12.6, 4.3, "16칸 네모가\n네 개", ha="left", va="center", fontsize=12, color=RED, fontweight="bold")
save(fig, "a01-grid.svg")

# 4. 방법 2: 색깔 자리에 하나씩 놓고, 같은 색이 오면 짝
fig, ax = canvas(10.0, 3.8, 16.6, 6.4)
basket(ax, 1.8, 0.8, 2.6, 1.5)
for k in range(3):
    sock(ax, 0.8 + k * 0.75, 3.1, 0.45, SOCKS[(k + 1) % 4])
arrow(ax, (3.4, 2.6), (4.9, 2.6))
names = ["파랑", "초록", "노랑", "보라"]
for k in range(4):
    cx = 6.2 + k * 2.6
    ax.add_patch(Ellipse((cx, 1.4), 2.2, 0.8, fc=SOCKS[k], ec=INK, lw=1.2, alpha=0.45))
    ax.text(cx, 0.85, names[k] + " 자리", ha="center", va="top", fontsize=11, color=INK)
sock(ax, 5.55, 3.0, 0.65, BLUE)
sock(ax, 6.55, 3.0, 0.65, BLUE, flip=True)
ax.text(6.2, 3.25, "짝!", ha="center", va="bottom", fontsize=16, color=RED, fontweight="bold")
sock(ax, 8.6, 3.0, 0.65, GREEN)
sock(ax, 11.2, 3.0, 0.65, YEL)
ax.text(10.0, 5.6, "양말 하나에 한 번씩만 봐요", ha="center", va="center", fontsize=13, fontweight="bold")
save(fig, "a01-spots.svg")

# 5. 두 배면 몇 배: 양말 4, 8, 16개일 때 할 일
fig, ax = canvas(10.4, 4.6, 17.4, 7.8)
base, scale = 1.2, 0.022
data = [(4, 16, 4), (8, 64, 8), (16, 256, 16)]
for i, (n, a, b) in enumerate(data):
    x = 1.5 + i * 5.2
    ax.add_patch(Rectangle((x, base), 1.4, a * scale, fc=RED if n == 16 else "#f2a08a", ec=INK, lw=1.2))
    ax.add_patch(Rectangle((x + 1.7, base), 1.4, b * scale, fc=BLUE, ec=INK, lw=1.2))
    ax.text(x + 0.7, base + a * scale + 0.12, f"{a}", ha="center", va="bottom", fontsize=13,
            color=RED if n == 16 else "#222", fontweight="bold")
    ax.text(x + 2.4, base + b * scale + 0.12, f"{b}", ha="center", va="bottom", fontsize=13, fontweight="bold")
    ax.text(x + 1.55, base - 0.2, f"양말 {n}개", ha="center", va="top", fontsize=12)
ax.add_patch(Rectangle((1.5, 7.2), 0.5, 0.35, fc="#f2a08a", ec=INK, lw=1))
ax.text(2.15, 7.37, "하나 집고 다 뒤지기", va="center", fontsize=11)
ax.add_patch(Rectangle((7.6, 7.2), 0.5, 0.35, fc=BLUE, ec=INK, lw=1))
ax.text(8.25, 7.37, "색깔 자리에 놓기", va="center", fontsize=11)
save(fig, "a01-bars.svg")

# 6. 양말이 2개뿐이면: 그냥 맞추는 게 빠르다
fig, ax = canvas(9.6, 3.4, 16.0, 5.6)
box(ax, 0.4, 0.4, 6.8, 4.6, fc="white")
ax.text(3.8, 4.5, "하나 집고 다 뒤지기", ha="center", fontsize=13, fontweight="bold")
sock(ax, 2.5, 3.6, 0.9, BLUE)
sock(ax, 4.6, 3.6, 0.9, BLUE, flip=True)
ax.text(3.8, 1.2, "끝!", ha="center", fontsize=16, color=RED, fontweight="bold")
box(ax, 8.8, 0.4, 6.8, 4.6, fc="white")
ax.text(12.2, 4.5, "색깔 자리에 놓기", ha="center", fontsize=13, fontweight="bold")
for k in range(4):
    ax.add_patch(Ellipse((9.9 + k * 1.55, 2.6), 1.3, 0.55, fc=SOCKS[k], ec=INK, lw=1, alpha=0.45))
ax.text(12.2, 1.2, "아직 자리 까는 중…", ha="center", fontsize=13, color=INK)
save(fig, "a01-small.svg")

print("ok")
