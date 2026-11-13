"""컴퓨터 5편 그림 만들기. 실행: python lab/fig_c05.py  → docs/computer/img/05/*.svg

확인용 PNG: FIG_FMT=png FIG_OUT=<폴더> python lab/fig_c05.py
글자는 SVG 안에 글자로 남긴다(글꼴 모양을 파일에 넣지 않는다). 보는 쪽 글꼴로 그려진다.
칠판은 짙은 초록, 공책은 흰 종이. 강조(지금 볼 곳)는 빨강 하나만 쓴다.
그림 안 글씨는 낱말과 숫자만 둔다.
"""
import os

import matplotlib

FMT = os.environ.get("FIG_FMT", "svg")
matplotlib.use("svg" if FMT == "svg" else "agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch, Rectangle

OUT = os.environ.get("FIG_OUT") or os.path.join(os.path.dirname(__file__), "..", "docs", "computer", "img", "05")
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
    name = name.rsplit(".", 1)[0] + "." + FMT
    fig.savefig(os.path.join(OUT, name), bbox_inches="tight", pad_inches=0.25, dpi=110)
    plt.close(fig)


def canvas(w, h, xmax, ymax):
    fig, ax = plt.subplots(figsize=(w, h))
    ax.set_xlim(0, xmax); ax.set_ylim(0, ymax); ax.axis("off")
    return fig, ax


def box(ax, x, y, w, h, fc="white", ec=INK, lw=1.8):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.08", fc=fc, ec=ec, lw=lw))


def arrow(ax, a, b, color=INK, lw=2, ms=18):
    ax.add_patch(FancyArrowPatch(a, b, arrowstyle="-|>", mutation_scale=ms, color=color, lw=lw))


def phone(ax, x, y, score, best, gone=False):
    box(ax, x, y, 3.2, 4.6, fc=PAPER)
    ax.add_patch(FancyBboxPatch((x + 1.2, y + 4.35), 0.8, 0.1, boxstyle="round,pad=0.02", fc=INK, ec=INK))
    ax.add_patch(Circle((x + 1.6, y + 0.25), 0.15, fc="white", ec=INK, lw=1.2))
    ax.text(x + 0.3, y + 3.9, f"점수 {score}", fontsize=14, fontweight="bold",
            color=RED if gone else "#222")
    ax.text(x + 0.3, y + 3.2, f"최고 기록 {best}", fontsize=13)
    if gone:
        ax.add_patch(Rectangle((x + 0.2, y + 3.65), 2.2, 0.6, fc="none", ec=RED, lw=2.5))


def chalkboard(ax, x, y, w, h, text=None, size=20, color="white"):
    ax.add_patch(Rectangle((x, y), w, h, fc=BOARD, ec="#7a5a3a", lw=5))
    if text:
        ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=size, color=color)


def notebook(ax, x, y, w, h, text=None, size=18, color="#222"):
    ax.add_patch(Rectangle((x, y), w, h, fc="white", ec=INK, lw=1.8))
    for k in range(1, 5):
        ax.plot([x + 0.2, x + w - 0.2], [y + k * h / 5.5, y + k * h / 5.5], color=GREY, lw=0.8)
    ax.add_patch(Rectangle((x - 0.15, y), 0.15, h, fc=INK, ec=INK))
    if text:
        ax.text(x + w / 2, y + h * 0.6, text, ha="center", va="center", fontsize=size, color=color)


def bulb(ax, cx, cy, r, on):
    ax.add_patch(Circle((cx, cy), r, fc=YEL if on else "#e6e8eb", ec="#b8901e" if on else "#9aa0a6", lw=1.2))
    ax.add_patch(Rectangle((cx - r * 0.45, cy - r * 1.45), r * 0.9, r * 0.5, fc="#9aa0a6", ec="none"))


# 1. 여는 장면: 끄기 전과 다시 켠 뒤
fig, ax = canvas(7.4, 3.8, 11, 5.8)
phone(ax, 0.4, 0.6, 40, 70)
ax.text(2.0, 0.1, "끄기 전", ha="center", fontsize=13)
arrow(ax, (3.9, 2.9), (6.9, 2.9))
ax.text(5.4, 3.3, "끄고 다시 켜기", ha="center", fontsize=12, color=INK)
phone(ax, 7.3, 0.6, 0, 70, gone=True)
ax.text(8.9, 0.1, "다시 켠 뒤", ha="center", fontsize=13)
save(fig, "c05-game.svg")

# 2. 숫자를 적어 두는 두 곳: 칠판(메모리)에 점수, 공책(저장 장치)에 최고 기록
fig, ax = canvas(8.4, 3.4, 13, 5.2)
for x, kind, name, what, num in [(0.4, "board", "메모리", "점수", "40"),
                                 (6.8, "note", "저장 장치", "최고 기록", "70")]:
    box(ax, x, 0.4, 5.8, 4.4)
    if kind == "board":
        chalkboard(ax, x + 0.5, 1.4, 2.6, 2.0, num, size=22)
    else:
        notebook(ax, x + 0.7, 1.4, 2.4, 2.0, num, size=22)
    ax.text(x + 3.6, 3.0, name, fontsize=17, fontweight="bold", va="center")
    ax.text(x + 3.6, 2.1, what, fontsize=14, va="center", color=INK)
ax.text(2.2, 0.85, "칠판", fontsize=11, color=INK, ha="center")
ax.text(8.7, 0.85, "공책", fontsize=11, color=INK, ha="center")
save(fig, "c05-map.svg")

# 3. 메모리 = 칠판: 40 → 50 → 60
fig, ax = canvas(9.0, 2.8, 14.2, 4.2)
for k, n in enumerate([40, 50, 60]):
    x = 0.3 + k * 5.0
    chalkboard(ax, x, 0.9, 3.4, 2.6, str(n), size=26)
    if k < 2:
        arrow(ax, (x + 3.6, 2.2), (x + 4.8, 2.2), color=RED, lw=2.2)
        ax.text(x + 4.2, 2.5, "+10", ha="center", va="bottom", fontsize=12, color=RED, fontweight="bold")
ax.text(7.1, 0.2, "메모리", ha="center", fontsize=14, fontweight="bold")
save(fig, "c05-board.svg")

# 4. 전원을 끄면 메모리가 지워진다
fig, ax = canvas(7.2, 3.0, 11, 4.6)
chalkboard(ax, 0.4, 0.8, 4.0, 2.8, "40", size=26)
arrow(ax, (4.8, 2.2), (6.2, 2.2), color=RED, lw=2.5)
ax.text(5.5, 2.6, "전원 끄기", ha="center", va="bottom", fontsize=12, color=RED, fontweight="bold")
chalkboard(ax, 6.6, 0.8, 4.0, 2.8)
ax.add_patch(Rectangle((6.6, 0.8), 4.0, 2.8, fc="none", ec=RED, lw=2.5, ls="--"))
ax.text(2.4, 0.3, "메모리", ha="center", fontsize=13)
ax.text(8.6, 0.3, "메모리", ha="center", fontsize=13)
save(fig, "c05-off.svg")

# 5. 언제 옮겨 적나: 게임 중에는 칠판만 바뀌고, 끝난 뒤 한 번만 공책에
fig, ax = canvas(9.4, 4.4, 14.4, 6.8)
ax.text(0.2, 5.4, "메모리", fontsize=13, fontweight="bold", va="center")
ax.text(0.2, 1.4, "저장 장치", fontsize=13, fontweight="bold", va="center")
for k, n in enumerate([60, 70, 80]):
    x = 2.4 + k * 3.6
    chalkboard(ax, x, 4.4, 2.4, 2.0, str(n), size=20)
    if k < 2:
        arrow(ax, (x + 2.55, 5.4), (x + 3.45, 5.4), color=INK, lw=1.6, ms=14)
ax.text(13.6, 5.4, "게임 끝", ha="center", va="center", fontsize=12, color=INK)
notebook(ax, 9.7, 0.4, 2.6, 2.0, "70 → 80", size=16, color=RED)
arrow(ax, (10.0, 4.25), (11.0, 2.55), color=RED, lw=2.5, ms=20)
ax.text(11.0, 3.4, "옮겨 적기", fontsize=12, color=RED, fontweight="bold", va="center")
save(fig, "c05-when.svg")

# 6. 진짜 휴대폰 속: 전원을 끄면 메모리 전구는 다 꺼지고, 저장 장치 전구는 그대로
fig, ax = canvas(9.0, 4.4, 13.6, 6.6)
ax.text(6.9, 6.2, "켜져 있을 때", ha="center", fontsize=12, color=INK)
ax.text(11.4, 6.2, "전원 끈 뒤", ha="center", fontsize=12, color=RED, fontweight="bold")
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
ax.text(7.2, 0.4, "전구(비트)", ha="center", fontsize=12, color=INK)
save(fig, "c05-chips.svg")

# 7. 두 곳 나란히: 빠르기, 끄면, 적는 것, 휴대폰 사양
fig, ax = canvas(8.6, 3.6, 13, 5.4)
rows = [("빠르기", "빠름", "느림"),
        ("전원 끄면", "지워짐", "남음"),
        ("적는 것", "점수", "최고 기록"),
        ("사양 표", "램 8GB", "저장 공간 128GB")]
cols = [0.2, 3.6, 8.0]
widths = [3.4, 4.4, 4.8]
ax.add_patch(Rectangle((cols[1], 4.4), widths[1], 0.9, fc=BOARD, ec="white"))
ax.add_patch(Rectangle((cols[2], 4.4), widths[2], 0.9, fc="white", ec=INK, lw=1.4))
ax.text(cols[1] + widths[1] / 2, 4.85, "메모리", ha="center", va="center", fontsize=15, color="white", fontweight="bold")
ax.text(cols[2] + widths[2] / 2, 4.85, "저장 장치", ha="center", va="center", fontsize=15, fontweight="bold")
for i, (head, a, b) in enumerate(rows):
    y = 3.4 - i * 1.0
    hot = i == 3
    ax.add_patch(Rectangle((cols[0], y), sum(widths), 1.0, fc=PAPER if i % 2 == 0 else "white", ec=GREY, lw=0.8))
    ax.text(cols[0] + 0.3, y + 0.5, head, va="center", fontsize=13, color=INK)
    for c, w, t in [(cols[1], widths[1], a), (cols[2], widths[2], b)]:
        ax.text(c + w / 2, y + 0.5, t, ha="center", va="center", fontsize=14,
                color=RED if hot else "#222", fontweight="bold" if hot else "normal")
save(fig, "c05-compare.svg")

print("ok")
