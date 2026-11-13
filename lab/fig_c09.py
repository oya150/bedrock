"""컴퓨터 9편 그림 만들기. 실행: python lab/fig_c09.py  → docs/computer/img/09/*.svg

확인용 PNG: FIG_FMT=png FIG_OUT=<폴더> python lab/fig_c09.py
글자는 SVG 안에 글자로 남긴다(글꼴 모양을 파일에 넣지 않는다). 보는 쪽 글꼴로 그려진다.
지금 볼 곳만 빨강으로 칠한다. 휴대폰과 자판은 특정 제품이 아닌 일반 모양이다.
좌표는 (왼쪽에서 몇째, 위에서 몇째)로 쓴다. 이 편의 대표 예시는 멈춤 버튼 칸 "4, 3"을 누르는 것이다.
"""
import os

import matplotlib

FMT = os.environ.get("FIG_FMT", "svg")
matplotlib.use("svg" if FMT == "svg" else "agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch, Rectangle

OUT = os.environ.get("FIG_OUT") or os.path.join(os.path.dirname(__file__), "..", "docs", "computer", "img", "09")
os.makedirs(OUT, exist_ok=True)

plt.rcParams.update({
    "font.family": ["Apple SD Gothic Neo", "Noto Sans KR", "Malgun Gothic", "sans-serif"],
    "svg.fonttype": "none",
    "text.color": "#222",
    "figure.facecolor": "white",
    "savefig.facecolor": "white",
})

RED, GREY, INK, PAPER, NOTE, YEL = "#e4572e", "#c9ccd1", "#555", "#f4f6f8", "#fffdf5", "#f6c445"
SKIN, GLOVE = "#f3dcc8", "#7a8ca8"


def save(fig, name):
    name = name.replace(".svg", "." + FMT)
    fig.savefig(os.path.join(OUT, name), bbox_inches="tight", pad_inches=0.25, dpi=110)
    plt.close(fig)


def canvas(w, h, xmax, ymax):
    fig, ax = plt.subplots(figsize=(w, h))
    ax.set_xlim(0, xmax); ax.set_ylim(0, ymax); ax.axis("off")
    return fig, ax


def box(ax, x, y, w, h, fc="white", ec=INK, lw=1.8):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.08", fc=fc, ec=ec, lw=lw))


def arrow(ax, a, b, color=INK, lw=2):
    ax.add_patch(FancyArrowPatch(a, b, arrowstyle="-|>", mutation_scale=18, color=color, lw=lw))


def finger_down(ax, tip_x, tip_y, w=0.9, length=2.4, fc=SKIN):
    """위에서 내려온 손가락: 끝이 (tip_x, tip_y)."""
    ax.add_patch(FancyBboxPatch((tip_x - w / 2, tip_y), w, length, boxstyle="round,pad=0.0,rounding_size=0.42",
                                fc=fc, ec=INK, lw=1.6, zorder=5))


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


def side_view(ax, x0, touched, who="손가락", labels=True):
    """화면을 옆에서 본 모습. touched 면 손가락 밑 줄이 빨갛다."""
    ax.add_patch(Rectangle((x0, 3.0), 6.4, 0.5, fc="#e8f1f8", ec=INK, lw=1.4))
    ax.plot([x0 + 0.1, x0 + 6.3], [2.73, 2.73], color=GREY, lw=3)
    ax.add_patch(Rectangle((x0, 1.7), 6.4, 0.7, fc=PAPER, ec=INK, lw=1.4))
    tip = x0 + 3.2
    if who == "손가락":
        finger_down(ax, tip, 3.5, w=0.9, length=2.0)
    else:
        ax.add_patch(Rectangle((tip - 0.8, 3.5), 1.6, 0.45, fc=GLOVE, ec=INK, lw=1.4, zorder=5))
        finger_down(ax, tip, 3.95, w=1.6, length=1.55, fc=GLOVE)
    if touched:
        ax.plot([tip - 0.5, tip + 0.5], [2.73, 2.73], color=RED, lw=4.5, zorder=4)
    if labels:
        ax.text(x0 + 6.6, 3.25, "유리", va="center", fontsize=12, color=INK)
        ax.text(x0 + 6.6, 2.73, "가는 줄", va="center", fontsize=12, color=INK)
        ax.text(x0 + 6.6, 2.05, "그림이 나오는 판", va="center", fontsize=12, color=INK)


# 1. 화면 속 세 겹: 유리, 가는 줄, 그림이 나오는 판
fig, ax = canvas(7.4, 3.6, 10.6, 6.0)
side_view(ax, 0.4, touched=True)
ax.text(3.6, 0.9, "옆에서 본 화면", ha="center", fontsize=13, fontweight="bold")
save(fig, "c09-layers.svg")

# 2. 손가락과 두꺼운 장갑
fig, ax = canvas(10.4, 3.6, 15.2, 6.0)
side_view(ax, 0.4, touched=True, labels=False)
side_view(ax, 8.4, touched=False, who="장갑", labels=False)
ax.text(3.6, 0.9, "손가락: 바뀜", ha="center", fontsize=13, fontweight="bold", color=RED)
ax.text(11.6, 0.9, "두꺼운 장갑: 그대로", ha="center", fontsize=13, fontweight="bold")
save(fig, "c09-glove.svg")

# 3. 위에서 본 줄: 손가락 밑 세로줄 셋·가로줄 셋이 바뀌고, 그 가운데(넷째 세로줄·셋째 가로줄)를 고른다
fig, ax = canvas(6.4, 4.6, 10.0, 7.2)
gx, gy, step = 2.0, 1.4, 1.0
ncol, nrow = 6, 4
top = gy + (nrow - 1) * step


def line_style(i, mid):
    """가운데 줄은 진한 빨강, 그 옆 바뀐 줄은 옅은 빨강, 나머지는 회색."""
    if i == mid:
        return dict(color=RED, lw=2.8, zorder=3)
    if abs(i - mid) == 1:
        return dict(color=RED, lw=2.0, alpha=0.45, zorder=3)
    return dict(color=GREY, lw=1.4, zorder=2)


for k in range(ncol):
    x = gx + k * step
    ax.plot([x, x], [gy - 0.5, top + 0.5], **line_style(k, 3))
for r in range(nrow):
    y = top - r * step
    ax.plot([gx - 0.5, gx + (ncol - 1) * step + 0.5], [y, y], **line_style(r, 2))
hx, hy = gx + 3 * step, top - 2 * step
ax.add_patch(Circle((hx, hy), 0.17, fc=RED, zorder=4))
ax.add_patch(Circle((hx, hy), 1.2, fc="none", ec=RED, lw=1.6, ls="--", zorder=4))
ax.text(gx + 2.5 * step, top + 0.75, "세로줄", ha="center", fontsize=12, color=INK)
ax.text(gx - 0.7, hy, "가로줄", ha="right", va="center", fontsize=12, color=INK)
ax.text(gx + 2.5 * step, 0.2, "위에서 본 줄", ha="center", fontsize=13, fontweight="bold")
save(fig, "c09-lines.svg")

# 4. 좌표: 손가락이 덮은 칸들의 한가운데 → (4, 3)
fig, ax = canvas(7.6, 4.6, 12.6, 7.6)
x0, y0, cols, rows, c = 1.0, 1.4, 6, 4, 1.25
grid(ax, x0, y0, cols, rows, c)
cx, cy = cell_center(x0, y0, rows, c, 4, 3)
ax.add_patch(Circle((cx, cy), 0.95, fc=SKIN, ec=INK, lw=1.2, alpha=0.7))
ax.add_patch(Circle((cx, cy), 0.13, fc=RED, zorder=4))
ax.text(9.2, cy + 1.6, "왼쪽에서 넷째\n위에서 셋째", ha="left", va="center", fontsize=12, color=INK, linespacing=1.5)
ax.text(9.2, cy, "4, 3", ha="left", va="center", fontsize=24, color=RED, fontweight="bold")
save(fig, "c09-coord.svg")

# 5. 버튼 칸 안이면 멈춤, 밖이면 그대로
fig, ax = canvas(10.4, 4.4, 17.6, 7.4)
for p, (col, row, label) in enumerate([(4, 3, "멈춤"), (2, 1, "그대로")]):
    x0 = 1.0 + p * 8.8
    grid(ax, x0, 1.4, 6, 4, 1.1)
    for bc in (4, 5):
        for br in (3, 4):
            bx, by = cell_center(x0, 1.4, 4, 1.1, bc, br)
            ax.add_patch(Rectangle((bx - 0.55, by - 0.55), 1.1, 1.1, fc=GREY, ec="white", lw=1.0))
    pause_icon(ax, x0 + 4 * 1.1, 1.4 + 1.0 * 1.1, 0.42)
    px, py = cell_center(x0, 1.4, 4, 1.1, col, row)
    ax.add_patch(Circle((px, py), 0.16, fc=RED, zorder=5))
    ax.text(x0 + 3.3, 0.55, f"{col}, {row} → {label}", ha="center", fontsize=14,
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
ax.text(8.9, 1.75, "좌표", ha="center", fontsize=12, color=INK)
arrow(ax, (10.2, 2.9), (11.2, 2.9))
box(ax, 11.6, 2.35, 1.2, 1.1, fc=NOTE)
ax.text(12.2, 2.9, "ㄱ", ha="center", va="center", fontsize=20)
ax.text(12.2, 1.75, "글자", ha="center", fontsize=12, color=INK)
arrow(ax, (13.2, 2.9), (14.2, 2.9))
box(ax, 14.6, 2.35, 3.4, 1.1, fc=NOTE)
ax.text(16.3, 2.9, "ㄱ의 번호", ha="center", va="center", fontsize=15)
ax.text(16.3, 1.75, "문자 코드", ha="center", fontsize=12, color=INK)
save(fig, "c09-keys.svg")

# 7. 두 손가락: 좌표 두 개 사이가 멀어지면 사진을 키운다
fig, ax = canvas(10.4, 4.2, 17.6, 7.2)
for p, (gap, size) in enumerate([(1.2, 1.0), (3.6, 1.8)]):
    x0 = 0.6 + p * 9.2
    box(ax, x0, 1.4, 6.8, 4.8, fc=PAPER)
    ax.add_patch(Circle((x0 + 3.4, 4.0), 0.7 * size, fc=YEL, ec="#b8901e", lw=1.2))
    for s in (-1, 1):
        ax.add_patch(Circle((x0 + 3.4 + s * gap / 2, 2.2), 0.18, fc=RED, zorder=5))
    if p == 1:
        ax.annotate("", xy=(x0 + 3.4 + gap / 2 - 0.25, 2.2), xytext=(x0 + 3.4 - gap / 2 + 0.25, 2.2),
                    arrowprops=dict(arrowstyle="<->", color=RED, lw=1.8))
    ax.text(x0 + 3.4, 0.7, "좌표 2개" if p == 0 else "멀어짐 → 키움", ha="center", fontsize=13,
            fontweight="bold", color=INK if p == 0 else RED)
arrow(ax, (7.7, 3.8), (9.5, 3.8))
save(fig, "c09-pinch.svg")

print("ok")
