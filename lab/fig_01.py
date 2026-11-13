"""알고리즘 1편 그림 만들기. 실행: python lab/fig_01.py  → docs/algorithms/img/01/*.svg

예시는 양말 짝 맞추기 하나를 편 끝까지 잇는다.
그림 안 글씨는 낱말과 숫자만 둔다. 문장은 본문과 그림 설명에 둔다(쉬운글-정책 5장).
숫자는 모두 양말 4개, 8개, 16개로 직접 센 것이다.
검토용 PNG가 필요하면 FIG_FMT=png FIG_OUT=<폴더> 로 실행한다.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "es"))
from figkit import BLUE, GREEN, GREY, INK, NOTE, PINK, RED, YEL, arrow, box, canvas, cell, label, outdir, save  # noqa: E402
from matplotlib.patches import Ellipse, Polygon, Rectangle  # noqa: E402

OUT = outdir("01", "algorithms")
PURPLE, BASKET, SOFT = "#b59cc8", "#e8d3b0", "#f2a08a"
SOCKS = [BLUE, GREEN, YEL, PURPLE]
NAMES = ["파랑", "초록", "노랑", "보라"]


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


def grid(ax, x0, y0, n, c, title):
    for r in range(n):
        for k in range(n):
            ax.add_patch(Rectangle((x0 + k * c, y0 + r * c), c, c, fc="white", ec=GREY, lw=0.8))
    ax.add_patch(Rectangle((x0, y0), n * c, n * c, fc="none", ec=INK, lw=1.6))
    label(ax, x0 + n * c / 2, y0 - 0.4, title, fs=13, bold=True)


# 1. 하나 집고 다 뒤지기: 집은 양말 하나로 바구니 양말 4개를 하나씩 본다
fig, ax = canvas(8.4, 3.2, 14, 5.3)
label(ax, 1.35, 4.75, "집은 양말", fs=11.5, color=INK)
sock(ax, 1.0, 3.6, 0.85, BLUE)
label(ax, 7.9, 4.75, "바구니 속 양말", fs=11.5, color=INK)
for k, col in enumerate([GREEN, YEL, PURPLE, BLUE]):
    x = 4.0 + k * 2.0
    last = k == 3
    ax.add_patch(Rectangle((x, 1.5), 1.6, 2.6, fc=PINK if last else NOTE, ec=RED if last else INK,
                           lw=2.2 if last else 1.2))
    sock(ax, x + 0.45, 3.5, 0.85, col)
    label(ax, x + 0.8, 1.05, str(k + 1), fs=13, color=RED if last else INK, bold=True)
    if k < 3:
        arrow(ax, (x + 1.62, 2.8), (x + 1.98, 2.8), color=GREY, ms=10, lw=1.3)
label(ax, 10.8, 1.85, "짝", fs=14, color=RED, bold=True)
arrow(ax, (2.3, 2.8), (3.85, 2.8), color=INK, ms=14)
label(ax, 12.9, 2.8, "4번", fs=16, color=RED, bold=True)
save(fig, OUT, "a01-scan.svg")

# 2. 칸 그림: 양말 4개는 16칸, 8개는 64칸(16칸 네모가 네 개)
fig, ax = canvas(10.0, 5.0, 16.6, 8.4)
c = 0.62
grid(ax, 1.8, 2.6, 4, c, "양말 4개: 16칸")
grid(ax, 8.2, 1.2, 8, c, "양말 8개: 64칸")
for dx, dy in ((0, 0), (4, 0), (0, 4), (4, 4)):
    ax.add_patch(Rectangle((8.2 + dx * c, 1.2 + dy * c), 4 * c, 4 * c, fc="none", ec=RED, lw=2.4))
label(ax, 1.8 + 2 * c, 5.35, "집은 양말 →", fs=10.5, color=INK, va="bottom")
label(ax, 1.6, 2.6 + 2 * c, "바구니\n속 양말\n↓", fs=10.5, color=INK, ha="right")
arrow(ax, (4.6, 3.85), (7.9, 3.85))
label(ax, 6.25, 4.15, "두 배", fs=12.5, color=INK, va="bottom")
label(ax, 13.4, 3.7, "16칸 × 4", fs=14, color=RED, ha="left", bold=True)
save(fig, OUT, "a01-grid.svg")

# 3. 색깔 자리에 놓기: 하나씩 꺼내 제 색 자리에, 같은 색이 있으면 짝
fig, ax = canvas(10.0, 3.6, 16.6, 6.0)
ax.add_patch(Polygon([(0.3, 3.4), (2.9, 3.4), (2.6, 1.6), (0.6, 1.6)], closed=True, fc=BASKET, ec=INK, lw=1.6))
label(ax, 1.6, 1.15, "바구니", fs=11, color=INK)
for k in range(3):
    sock(ax, 0.65 + k * 0.7, 4.15, 0.45, SOCKS[(k + 1) % 4])
arrow(ax, (3.2, 2.6), (4.6, 2.6))
for k in range(4):
    cx = 6.2 + k * 2.6
    ax.add_patch(Ellipse((cx, 1.4), 2.2, 0.8, fc=SOCKS[k], ec=INK, lw=1.2, alpha=0.45))
    label(ax, cx, 0.6, NAMES[k], fs=11, color=INK)
sock(ax, 5.55, 3.4, 0.65, BLUE)
sock(ax, 6.55, 3.4, 0.65, BLUE, flip=True)
label(ax, 6.2, 4.0, "짝", fs=15, color=RED, bold=True)
sock(ax, 8.5, 3.4, 0.65, GREEN)
sock(ax, 11.1, 3.4, 0.65, YEL)
save(fig, OUT, "a01-spots.svg")

# 4. 두 배면 몇 배: 양말 4, 8, 16개일 때 본 횟수
fig, ax = canvas(10.4, 4.8, 17.4, 8.2)
base, scale = 1.2, 0.022
data = [(4, 16, 4), (8, 64, 8), (16, 256, 16)]
for i, (n, a, b) in enumerate(data):
    x = 1.5 + i * 5.6
    hot = n == 16
    ax.add_patch(Rectangle((x, base), 1.4, a * scale, fc=RED if hot else SOFT, ec=INK, lw=1.2))
    ax.add_patch(Rectangle((x + 1.7, base), 1.4, b * scale, fc=BLUE, ec=INK, lw=1.2))
    label(ax, x + 0.7, base + a * scale + 0.3, str(a), fs=13, color=RED if hot else "#222", bold=True)
    label(ax, x + 2.4, base + b * scale + 0.3, str(b), fs=13, bold=True)
    label(ax, x + 1.55, base - 0.45, f"양말 {n}개", fs=12)
ax.add_patch(Rectangle((1.5, 7.6), 0.5, 0.35, fc=SOFT, ec=INK, lw=1))
label(ax, 2.15, 7.77, "하나 집고 다 뒤지기", fs=11, ha="left")
ax.add_patch(Rectangle((7.6, 7.6), 0.5, 0.35, fc=BLUE, ec=INK, lw=1))
label(ax, 8.25, 7.77, "색깔 자리에 놓기", fs=11, ha="left")
save(fig, OUT, "a01-bars.svg")

# 5. 빅오 표: 양말 n개일 때 보는 횟수, 두 배면 몇 배, 빅오
fig, ax = canvas(9.6, 2.6, 15.4, 4.2)
xs, ws = [0.3, 5.3, 8.6, 11.9], [4.9, 3.2, 3.2, 3.2]
for h, x, w in zip(["방법", "양말 n개", "두 배면", "빅오"], xs, ws):
    label(ax, x + w / 2, 3.75, h, fs=11.5, color=INK, bold=True)
rows = [("하나 집고 다 뒤지기", "n × n", "네 배", "O(n²)"), ("색깔 자리에 놓기", "n", "두 배", "O(n)")]
for r, row in enumerate(rows):
    y = 2.1 - r * 1.3
    for k, (s, x, w) in enumerate(zip(row, xs, ws)):
        cell(ax, x, y, w - 0.1, 1.0, s, hot=(r == 0 and k >= 2), fs=13)
save(fig, OUT, "a01-bigo.svg")

# 6. 양말이 2개뿐이면: 준비 없는 쪽이 먼저 끝난다
fig, ax = canvas(9.6, 3.4, 16.0, 5.6)
box(ax, 0.4, 0.4, 6.8, 4.6, fc="white")
label(ax, 3.8, 4.5, "하나 집고 다 뒤지기", fs=13, bold=True)
sock(ax, 2.5, 3.6, 0.9, BLUE)
sock(ax, 4.6, 3.6, 0.9, BLUE, flip=True)
label(ax, 3.8, 1.2, "끝", fs=16, color=RED, bold=True)
box(ax, 8.8, 0.4, 6.8, 4.6, fc="white")
label(ax, 12.2, 4.5, "색깔 자리에 놓기", fs=13, bold=True)
for k in range(4):
    ax.add_patch(Ellipse((9.9 + k * 1.55, 2.6), 1.3, 0.55, fc=SOCKS[k], ec=INK, lw=1, alpha=0.45))
label(ax, 12.2, 1.2, "자리 까는 중", fs=13, color=INK)
save(fig, OUT, "a01-small.svg")

print("ok")
