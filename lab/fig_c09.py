"""컴퓨터 9편 그림 만들기. 실행: python lab/fig_c09.py  → docs/computer/img/09/*.svg

글자는 SVG 안에 글자로 남긴다(글꼴 모양을 파일에 넣지 않는다). 보는 쪽 글꼴로 그려진다.
손가락이 닿은 자리만 빨강으로 칠한다. 휴대폰과 자판은 특정 제품이 아닌 일반 모양이다.
좌표는 (왼쪽에서 몇째, 위에서 몇째)로 쓴다.
"""
import os

import matplotlib

matplotlib.use("svg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch, Rectangle

OUT = os.path.join(os.path.dirname(__file__), "..", "docs", "computer", "img", "09")
os.makedirs(OUT, exist_ok=True)

plt.rcParams.update({
    "font.family": ["Apple SD Gothic Neo", "Noto Sans KR", "Malgun Gothic", "sans-serif"],
    "svg.fonttype": "none",
    "text.color": "#222",
    "figure.facecolor": "white",
    "savefig.facecolor": "white",
})

RED, GREY, INK, PAPER, NOTE, YEL = "#e4572e", "#c9ccd1", "#555", "#f4f6f8", "#fffdf5", "#f6c445"
SKIN = "#f3dcc8"


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


def finger(ax, tip_x, tip_y, w=0.9, length=2.6):
    """아래에서 올라온 손가락: 끝이 (tip_x, tip_y)."""
    ax.add_patch(FancyBboxPatch((tip_x - w / 2, tip_y - length), w, length, boxstyle="round,pad=0.0,rounding_size=0.42",
                                fc=SKIN, ec=INK, lw=1.6, zorder=5))
    ax.add_patch(FancyBboxPatch((tip_x - w * 0.3, tip_y - w * 0.75), w * 0.6, w * 0.55,
                                boxstyle="round,pad=0.0,rounding_size=0.15", fc="white", ec=INK, lw=1.0, zorder=6))


def finger_down(ax, tip_x, tip_y, w=0.9, length=2.4):
    """위에서 내려온 손가락: 끝이 (tip_x, tip_y)."""
    ax.add_patch(FancyBboxPatch((tip_x - w / 2, tip_y), w, length, boxstyle="round,pad=0.0,rounding_size=0.42",
                                fc=SKIN, ec=INK, lw=1.6, zorder=5))


def pause_icon(ax, cx, cy, s, color=INK):
    ax.add_patch(Circle((cx, cy), s, fc="white", ec=color, lw=2))
    for dx in (-0.3, 0.3):
        ax.add_patch(Rectangle((cx + dx * s - 0.12 * s, cy - 0.45 * s), 0.24 * s, 0.9 * s, fc=color))


def grid(ax, x0, y0, cols, rows, c, numbers=True):
    """칸 격자. 번호는 위(왼쪽에서 몇째)와 왼쪽(위에서 몇째)."""
    for r in range(rows):
        for k in range(cols):
            ax.add_patch(Rectangle((x0 + k * c, y0 + (rows - 1 - r) * c), c, c, fc="white", ec=GREY, lw=1.2))
    if numbers:
        for k in range(cols):
            ax.text(x0 + (k + 0.5) * c, y0 + rows * c + 0.15, str(k + 1), ha="center", va="bottom", fontsize=12, color=INK)
        for r in range(rows):
            ax.text(x0 - 0.15, y0 + (rows - r - 0.5) * c, str(r + 1), ha="right", va="center", fontsize=12, color=INK)


def cell_center(x0, y0, rows, c, col, row):
    """(왼쪽에서 col째, 위에서 row째) 칸의 한복판."""
    return x0 + (col - 0.5) * c, y0 + (rows - row + 0.5) * c


# 1. 여는 장면: 멈춤 버튼을 누르는 손가락
fig, ax = canvas(5.6, 4.4, 9.2, 7.2)
ax.add_patch(FancyBboxPatch((0.6, 1.0), 8.0, 5.6, boxstyle="round,pad=0.2", fc=PAPER, ec=INK, lw=2.2))
ax.add_patch(Rectangle((1.1, 2.6), 7.0, 3.6, fc="white", ec=INK, lw=1.4))
ax.add_patch(Circle((5.6, 4.2), 0.42, fc=YEL, ec="#b8901e", lw=1.2))
ax.plot([1.4, 7.8], [3.4, 3.4], color=GREY, lw=1.6)
pause_icon(ax, 4.6, 1.75, 0.45)
finger(ax, 4.95, 1.45, length=1.9)
ax.text(5.8, 1.9, "?", fontsize=26, color=RED, fontweight="bold", va="center")
save(fig, "c09-tap.svg")

# 2. 이 편의 지도: 손가락 → 화면 속 줄 → 숫자 두 개 → 버튼 자리인가
fig, ax = canvas(11.6, 2.9, 19.4, 4.6)
titles = ["손가락", "화면 속 줄", "숫자 두 개", "버튼 자리인가?"]
for i, t in enumerate(titles):
    x = 0.3 + i * 4.8
    box(ax, x, 0.4, 3.8, 3.6)
    ax.text(x + 1.9, 0.95, t, ha="center", va="center", fontsize=13, fontweight="bold")
    if i == 0:
        finger(ax, x + 1.9, 3.5, w=0.8, length=1.9)
    elif i == 1:
        for k in range(5):
            ax.plot([x + 0.7 + k * 0.6, x + 0.7 + k * 0.6], [1.5, 3.6], color=GREY, lw=1.2)
        for r in range(4):
            ax.plot([x + 0.5, x + 3.3], [1.7 + r * 0.6, 1.7 + r * 0.6], color=GREY, lw=1.2)
        ax.add_patch(Circle((x + 1.9, 2.9), 0.14, fc=RED))
    elif i == 2:
        ax.text(x + 1.9, 2.55, "3, 2", ha="center", va="center", fontsize=24, color=RED, fontweight="bold")
    else:
        pause_icon(ax, x + 1.9, 2.55, 0.6)
    if i < 3:
        arrow(ax, (x + 3.95, 2.2), (x + 4.65, 2.2))
save(fig, "c09-map.svg")

# 3. 화면 속 줄: 옆에서 본 모습과 위에서 본 모습
fig, ax = canvas(10.4, 4.0, 17.4, 6.6)
# 옆에서 본 모습
ax.add_patch(Rectangle((0.4, 3.0), 6.4, 0.5, fc="#e8f1f8", ec=INK, lw=1.4))
ax.text(7.0, 3.25, "유리", va="center", fontsize=12, color=INK)
ax.plot([0.5, 6.7], [2.73, 2.73], color=GREY, lw=3)
ax.text(7.0, 2.73, "안 보이는 줄", va="center", fontsize=12, color=INK)
ax.add_patch(Rectangle((0.4, 1.7), 6.4, 0.7, fc=PAPER, ec=INK, lw=1.4))
ax.text(7.0, 2.05, "그림이 나오는 판", va="center", fontsize=12, color=INK)
finger_down(ax, 3.575, 3.5, w=0.9, length=2.0)
ax.plot([3.1, 4.05], [2.73, 2.73], color=RED, lw=4)
ax.text(3.6, 0.9, "옆에서 본 모습", ha="center", fontsize=13, fontweight="bold")
# 위에서 본 모습
gx, gy = 11.2, 1.7
for k in range(7):
    ax.plot([gx + k * 0.8, gx + k * 0.8], [gy, gy + 4.0], color=GREY, lw=1.4)
for r in range(6):
    ax.plot([gx - 0.2, gx + 5.0], [gy + r * 0.8, gy + r * 0.8], color=GREY, lw=1.4)
ax.plot([gx + 2 * 0.8, gx + 2 * 0.8], [gy, gy + 4.0], color=RED, lw=2.4, zorder=3)
ax.plot([gx - 0.2, gx + 5.0], [gy + 3 * 0.8, gy + 3 * 0.8], color=RED, lw=2.4, zorder=3)
ax.add_patch(Circle((gx + 2 * 0.8, gy + 3 * 0.8), 0.17, fc=RED, zorder=4))
ax.add_patch(Circle((gx + 2 * 0.8, gy + 3 * 0.8), 0.55, fc="none", ec=RED, lw=1.6, ls="--", zorder=4))
ax.text(gx + 2.4, 0.9, "위에서 본 모습", ha="center", fontsize=13, fontweight="bold")
save(fig, "c09-lines.svg")

# 4. 좌표: 손가락이 덮은 칸들의 한가운데 → (3, 2)
fig, ax = canvas(7.6, 4.6, 12.6, 7.6)
x0, y0, cols, rows, c = 1.0, 1.4, 6, 4, 1.25
grid(ax, x0, y0, cols, rows, c)
cx, cy = cell_center(x0, y0, rows, c, 3, 2)
ax.add_patch(Circle((cx, cy), 0.95, fc=SKIN, ec=INK, lw=1.2, alpha=0.7))
ax.add_patch(Circle((cx, cy), 0.13, fc=RED, zorder=4))
ax.text(9.2, cy, "왼쪽에서 셋째\n위에서 둘째", ha="left", va="center", fontsize=12, color=INK, linespacing=1.5)
ax.text(9.2, cy - 1.5, "3, 2", ha="left", va="center", fontsize=22, color=RED, fontweight="bold")
ax.text(4.75, 0.5, "손가락이 덮은 칸들의 한가운데", ha="center", fontsize=12, color=INK)
save(fig, "c09-coord.svg")

# 5. 버튼 자리인가: 버튼 칸 안을 누르면 멈춤, 밖이면 그대로
fig, ax = canvas(10.4, 4.4, 17.6, 7.4)
for p, (col, row, label) in enumerate([(5, 4, "멈춤!"), (2, 1, "그대로")]):
    x0 = 1.0 + p * 8.8
    grid(ax, x0, 1.4, 6, 4, 1.1)
    for bc in (4, 5):
        for br in (3, 4):
            bx, by = cell_center(x0, 1.4, 4, 1.1, bc, br)
            ax.add_patch(Rectangle((bx - 0.55, by - 0.55), 1.1, 1.1, fc=GREY, ec="white", lw=1.0))
    pause_icon(ax, x0 + 4 * 1.1, 1.4 + 1.0 * 1.1, 0.42)
    px, py = cell_center(x0, 1.4, 4, 1.1, col, row)
    ax.add_patch(Circle((px, py), 0.16, fc=RED, zorder=5))
    ax.text(x0 + 3.3, 0.55, f"{col}, {row} 누름 → {label}", ha="center", fontsize=13,
            fontweight="bold", color=RED if p == 0 else INK)
save(fig, "c09-button.svg")

# 6. 자판: 누른 자리 → 좌표 → 글자 → 글자 번호
fig, ax = canvas(11.6, 3.2, 19.6, 5.4)
keys = [["ㅂ", "ㅈ", "ㄷ", "ㄱ", "ㅅ"], ["ㅁ", "ㄴ", "ㅇ", "ㄹ", "ㅎ"], ["ㅋ", "ㅌ", "ㅊ", "ㅍ", "ㅠ"]]
for r, row in enumerate(keys):
    for k, ch in enumerate(row):
        x, y = 0.4 + k * 1.15 + r * 0.25, 3.6 - r * 1.15
        on = (r, k) == (0, 3)
        box(ax, x, y, 0.95, 0.9, fc="white", ec=RED if on else GREY, lw=2.2 if on else 1.2)
        ax.text(x + 0.48, y + 0.45, ch, ha="center", va="center", fontsize=14, color=RED if on else "#222")
arrow(ax, (6.6, 2.9), (7.6, 2.9))
ax.text(8.9, 2.9, "4, 1", ha="center", va="center", fontsize=20, color=RED, fontweight="bold")
ax.text(8.9, 1.9, "좌표", ha="center", fontsize=12, color=INK)
arrow(ax, (10.2, 2.9), (11.2, 2.9))
box(ax, 11.6, 2.35, 1.2, 1.1, fc=NOTE)
ax.text(12.2, 2.9, "ㄱ", ha="center", va="center", fontsize=20)
ax.text(12.2, 1.9, "글자", ha="center", fontsize=12, color=INK)
arrow(ax, (13.2, 2.9), (14.2, 2.9))
box(ax, 14.6, 2.35, 3.4, 1.1, fc=NOTE)
ax.text(16.3, 2.9, "ㄱ의 번호", ha="center", va="center", fontsize=15)
ax.text(16.3, 1.9, "3편의 문자 코드", ha="center", fontsize=12, color=INK)
save(fig, "c09-keys.svg")

print("ok")
