"""컴퓨터 2편 그림 만들기. 실행: python lab/fig_c02.py  → docs/computer/img/02/*.svg

글자는 SVG 안에 글자로 남긴다(글꼴 모양을 파일에 넣지 않는다). 보는 쪽 글꼴로 그려진다.
그림 속 노랑·검정·흰색은 사진 내용이고, 강조는 빨강 하나만 쓴다.
"""
import os

import matplotlib

matplotlib.use("svg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch, Rectangle, Wedge

OUT = os.path.join(os.path.dirname(__file__), "..", "docs", "computer", "img", "02")
os.makedirs(OUT, exist_ok=True)

plt.rcParams.update({
    "font.family": ["Apple SD Gothic Neo", "Noto Sans KR", "Malgun Gothic", "sans-serif"],
    "svg.fonttype": "none",
    "text.color": "#222",
    "figure.facecolor": "white",
    "savefig.facecolor": "white",
})

RED, GREY, INK, PAPER = "#e4572e", "#c9ccd1", "#555", "#f4f6f8"
# 색 번호표: 0 흰색, 1 검정, 2 노랑
PALETTE = {0: "#ffffff", 1: "#222222", 2: "#f6c445"}
NAMES = {0: "흰색", 1: "검정", 2: "노랑"}

SMILE = [
    [0, 0, 2, 2, 2, 2, 0, 0],
    [0, 2, 2, 2, 2, 2, 2, 0],
    [2, 2, 1, 2, 2, 1, 2, 2],
    [2, 2, 1, 2, 2, 1, 2, 2],
    [2, 2, 2, 2, 2, 2, 2, 2],
    [2, 1, 2, 2, 2, 2, 1, 2],
    [0, 2, 1, 1, 1, 1, 2, 0],
    [0, 0, 2, 2, 2, 2, 0, 0],
]


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


def grid(ax, cells, x0, y0, size, numbers=False, lines=True):
    """cells[줄][칸]을 왼쪽 위부터 그린다. numbers=True면 색 대신 번호를 적는다."""
    n = len(cells)
    c = size / n
    for r, row in enumerate(cells):
        for k, v in enumerate(row):
            x, y = x0 + k * c, y0 + size - (r + 1) * c
            fc = "white" if numbers else PALETTE[v]
            ax.add_patch(Rectangle((x, y), c, c, fc=fc, ec=GREY if lines else fc, lw=0.8 if lines else 0))
            if numbers:
                ax.text(x + c / 2, y + c / 2, str(v), ha="center", va="center", fontsize=12)
    return c


def smooth_face(ax, cx, cy, r):
    ax.add_patch(Circle((cx, cy), r, fc=PALETTE[2], ec="none"))
    for dx in (-0.35, 0.35):
        ax.add_patch(Circle((cx + dx * r, cy + 0.25 * r), 0.11 * r, fc=PALETTE[1]))
    ax.add_patch(Wedge((cx, cy - 0.05 * r), 0.55 * r, 200, 340, width=0.12 * r, fc=PALETTE[1]))


def raster_face(n):
    """동그란 웃는 얼굴을 n칸 × n칸으로 나눠 칸마다 번호를 정한다."""
    import math
    cells = []
    for r in range(n):
        row = []
        for k in range(n):
            x = (k + 0.5) / n * 2 - 1
            y = 1 - (r + 0.5) / n * 2
            v = 0
            if x * x + y * y <= 0.95:
                v = 2
                for ex in (-0.35, 0.35):
                    if (x - ex) ** 2 + (y - 0.25) ** 2 <= 0.11 ** 2 * 1.6:
                        v = 1
                d = math.hypot(x, y + 0.05)
                ang = math.degrees(math.atan2(y + 0.05, x)) % 360
                if 0.43 * 0.97 <= d <= 0.55 * 1.0 and 200 <= ang <= 340:
                    v = 1
            row.append(v)
        cells.append(row)
    return cells


# 1. 여는 장면: 사진을 끝까지 키우면 네모 칸이 보인다
fig, ax = canvas(8.0, 3.6, 12, 5.4)
box(ax, 0.6, 0.3, 2.8, 4.8, fc=PAPER)
smooth_face(ax, 2.0, 2.7, 1.0)
ax.text(2.0, 0.75, "휴대폰 사진", ha="center", fontsize=12)
arrow(ax, (3.8, 2.7), (6.6, 2.7))
ax.text(5.2, 3.15, "끝까지 키우면", ha="center", fontsize=13)
grid(ax, SMILE, 7.2, 0.6, 4.2, lines=True)
ax.text(9.3, 0.1, "작은 네모 칸이 보여요", ha="center", fontsize=12)
save(fig, "c02-zoom.svg")

# 2. 이 편의 지도: 네모 칸 → 칸마다 색 하나 → 색마다 번호 → 칸마다 번호 적기 (본문 목록과 같은 말)
fig, ax = canvas(11.0, 3.2, 17.6, 5.0)
steps = ["사진은 네모 칸", "칸마다 색 하나", "색마다 번호", "칸마다 번호 적기"]
mini = [[2, 2], [1, 2]]
for i, t in enumerate(steps):
    x = 0.3 + i * 4.4
    box(ax, x, 0.4, 3.4, 4.2)
    ax.text(x + 0.3, 4.2, str(i + 1), fontsize=12, color=INK, fontweight="bold")
    cx = x + 0.95
    if i == 0:
        grid(ax, mini, cx, 1.6, 1.5)
    elif i == 1:
        ax.add_patch(Rectangle((cx + 0.35, 1.95), 0.8, 0.8, fc=PALETTE[2], ec=GREY))
    elif i == 2:
        for k, v in enumerate((2, 1)):
            yy = 2.75 - k * 1.0
            ax.add_patch(Rectangle((cx, yy), 0.7, 0.7, fc=PALETTE[v], ec=GREY))
            ax.text(cx + 1.0, yy + 0.35, f"= {v}", va="center", fontsize=14)
    else:
        grid(ax, mini, cx, 1.6, 1.5, numbers=True)
    ax.text(x + 1.7, 0.9, t, ha="center", va="center", fontsize=13, fontweight="bold")
    if i < 3:
        arrow(ax, (x + 3.55, 2.5), (x + 4.25, 2.5))
save(fig, "c02-map.svg")

# 3. 픽셀: 8칸 × 8칸 웃는 얼굴, 칸 하나에 이름표
fig, ax = canvas(6.6, 4.6, 10, 7.0)
c = grid(ax, SMILE, 0.5, 0.5, 6.0)
# 셋째 줄 셋째 칸(눈)을 가리킨다
px, py = 0.5 + 2 * c, 0.5 + 6.0 - 3 * c
ax.add_patch(Rectangle((px, py), c, c, fc="none", ec=RED, lw=3))
arrow(ax, (8.0, py + c / 2), (px + c + 0.1, py + c / 2), color=RED)
ax.text(8.1, py + c / 2, "픽셀 하나", va="center", fontsize=15, color=RED, fontweight="bold")
save(fig, "c02-pixel.svg")

# 4. 색 번호표
fig, ax = canvas(7.0, 2.4, 11, 3.6)
ax.text(5.5, 3.1, "색 번호표", ha="center", fontsize=14, color=INK)
for i in range(3):
    x = 0.4 + i * 3.6
    ax.add_patch(Rectangle((x, 0.6), 1.4, 1.4, fc=PALETTE[i], ec=INK, lw=1.5))
    ax.text(x + 1.7, 1.55, f"{i}번", fontsize=16, fontweight="bold", va="center")
    ax.text(x + 1.7, 0.95, NAMES[i], fontsize=13, color=INK, va="center")
save(fig, "c02-palette.svg")

# 5. 숫자 판과 칠한 그림: 같은 자리를 잇는다
fig, ax = canvas(9.4, 4.4, 15, 7.0)
c = grid(ax, SMILE, 0.4, 0.6, 5.6, numbers=True)
grid(ax, SMILE, 9.0, 0.6, 5.6)
ax.text(3.2, 0.05, "컴퓨터가 적어 둔 번호", ha="center", fontsize=13)
ax.text(11.8, 0.05, "화면에 칠한 모습", ha="center", fontsize=13)
# 맨 윗줄 셋째 칸
lx, ly = 0.4 + 2 * c, 0.6 + 5.6 - c
rx = 9.0 + 2 * c
ax.add_patch(Rectangle((lx, ly), c, c, fc="none", ec=RED, lw=3))
ax.add_patch(Rectangle((rx, ly), c, c, fc="none", ec=RED, lw=3))
ax.add_patch(FancyArrowPatch((lx + c, ly + c * 0.5), (rx, ly + c * 0.5), arrowstyle="-|>",
                             mutation_scale=18, color=RED, lw=2, connectionstyle="arc3,rad=-0.25"))
ax.text(7.5, 3.2, "2번은\n노랑", ha="center", va="center", fontsize=13, color=RED, fontweight="bold")
save(fig, "c02-numbers.svg")

# 6. 칸이 많을수록 부드럽다
fig, ax = canvas(10.0, 3.8, 16, 6.0)
for i, (n, label) in enumerate([(8, "칸이 적으면"), (16, "칸이 더 많으면"), (48, "칸이 아주 많으면")]):
    x = 0.5 + i * 5.3
    # 칸이 적은 그림은 앞에서 본 8칸 얼굴과 같게 그린다
    grid(ax, SMILE if n == 8 else raster_face(n), x, 1.0, 4.4, lines=(n <= 16))
    ax.text(x + 2.2, 0.35, label, ha="center", fontsize=13)
save(fig, "c02-more.svg")

# 7. 그림 전화 놀이: 번호를 부르는 순서(색 번호와 헷갈리지 않게 숫자 없이 화살표로)
fig, ax = canvas(3.6, 3.6, 5, 5)
for r in range(4):
    for k in range(4):
        ax.add_patch(Rectangle((0.5 + k, 4.5 - (r + 1)), 1, 1, fc="white", ec=GREY, lw=1.2))
for r in range(4):
    y = 4.5 - r - 0.5
    arrow(ax, (0.65, y), (4.35, y), color=RED if r == 0 else INK)
    if r < 3:
        ax.plot([4.35, 0.65], [y - 0.15, y - 0.85], color=GREY, lw=1.2, ls="--")
ax.text(0.5, 4.75, "시작", fontsize=11, color=RED)
save(fig, "c02-order.svg")

print("ok")
