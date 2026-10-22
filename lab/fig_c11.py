"""컴퓨터 11편 그림 만들기. 실행: python lab/fig_c11.py  → docs/computer/img/11/*.svg

글자는 SVG 안에 글자로 남긴다(글꼴 모양을 파일에 넣지 않는다). 보는 쪽 글꼴로 그려진다.
길을 가는 메시지만 빨강으로 칠한다. 휴대폰·컴퓨터·택배는 특정 제품이 아닌 일반 모양이다.
"""
import os

import matplotlib

matplotlib.use("svg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch, Polygon, Rectangle

OUT = os.path.join(os.path.dirname(__file__), "..", "docs", "computer", "img", "11")
os.makedirs(OUT, exist_ok=True)

plt.rcParams.update({
    "font.family": ["Apple SD Gothic Neo", "Noto Sans KR", "Malgun Gothic", "sans-serif"],
    "svg.fonttype": "none",
    "text.color": "#222",
    "figure.facecolor": "white",
    "savefig.facecolor": "white",
})

RED, GREY, INK, PAPER, NOTE, YEL = "#e4572e", "#c9ccd1", "#555", "#f4f6f8", "#fffdf5", "#f6c445"
BOX = "#e8d3b0"


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


def phone(ax, cx, y, h, on=True, text=None):
    """휴대폰: 켜져 있으면 흰 화면, 꺼져 있으면 어두운 화면."""
    w = h * 0.55
    ax.add_patch(FancyBboxPatch((cx - w / 2, y), w, h, boxstyle="round,pad=0.06", fc=PAPER, ec=INK, lw=2))
    ax.add_patch(Rectangle((cx - w / 2 + 0.12, y + 0.25), w - 0.24, h - 0.45,
                           fc="white" if on else "#3a3d42", ec=INK, lw=1))
    if text:
        bubble(ax, cx, y + h * 0.6, text, size=10)


def bubble(ax, cx, cy, text, size=11):
    w = 0.22 * len(text) * size / 10 + 0.3
    ax.add_patch(FancyBboxPatch((cx - w / 2, cy - 0.22), w, 0.44, boxstyle="round,pad=0.06",
                                fc=RED, ec=RED, lw=1))
    ax.text(cx, cy, text, ha="center", va="center", fontsize=size, color="white", fontweight="bold")


def parcel(ax, x, y, w, h, label, inner=None, red=False, size=10):
    """상자: 겉에 받는 사람 딱지. red 면 메시지 상자."""
    ax.add_patch(Rectangle((x, y), w, h, fc=RED if red else BOX, ec=INK, lw=1.6))
    ax.add_patch(Rectangle((x + w * 0.12, y + h * 0.5), w * 0.76, h * 0.36, fc="white", ec=INK, lw=1))
    ax.text(x + w / 2, y + h * 0.68, label, ha="center", va="center", fontsize=size, color="#222")
    if inner:
        ax.text(x + w / 2, y + h * 0.25, inner, ha="center", va="center", fontsize=11,
                color="white" if red else "#222", fontweight="bold")


def computer(ax, cx, y, s=1.0, label=None):
    """인터넷 위의 컴퓨터: 상자에 선 세 줄."""
    w, h = 1.3 * s, 1.0 * s
    ax.add_patch(FancyBboxPatch((cx - w / 2, y), w, h, boxstyle="round,pad=0.05", fc=PAPER, ec=INK, lw=1.6))
    for k in range(3):
        yy = y + h * (0.25 + 0.25 * k)
        ax.plot([cx - w * 0.32, cx + w * 0.32], [yy, yy], color=GREY, lw=1.6)
    if label:
        ax.text(cx, y - 0.15, label, ha="center", va="top", fontsize=10, color=INK)


def server(ax, x, y, w, h):
    """서버: 키 큰 장. 선반 세 칸."""
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.06", fc=PAPER, ec=INK, lw=2))
    for k in range(1, 3):
        ax.plot([x + 0.1, x + w - 0.1], [y + h * k / 3, y + h * k / 3], color=INK, lw=1.4)


def house(ax, cx, y, s, label):
    ax.add_patch(Rectangle((cx - 0.5 * s, y), s, 0.7 * s, fc="white", ec=INK, lw=1.6))
    ax.add_patch(Polygon([(cx - 0.65 * s, y + 0.7 * s), (cx, y + 1.15 * s), (cx + 0.65 * s, y + 0.7 * s)],
                         closed=True, fc=GREY, ec=INK, lw=1.6))
    ax.text(cx, y - 0.15, label, ha="center", va="top", fontsize=10, color=INK)


def warehouse(ax, cx, y, s, label):
    ax.add_patch(Rectangle((cx - 0.9 * s, y), 1.8 * s, 0.8 * s, fc="white", ec=INK, lw=1.6))
    ax.add_patch(Polygon([(cx - 0.9 * s, y + 0.8 * s), (cx - 0.9 * s, y + 1.05 * s), (cx + 0.9 * s, y + 1.05 * s),
                          (cx + 0.9 * s, y + 0.8 * s)], closed=True, fc=GREY, ec=INK, lw=1.6))
    ax.text(cx, y - 0.15, label, ha="center", va="top", fontsize=10, color=INK)


def moon(ax, cx, cy, r, bg="white"):
    """초승달: 노란 동그라미 위에 배경색 동그라미를 비껴 덮는다."""
    ax.add_patch(Circle((cx, cy), r, fc=YEL, ec=INK, lw=1.2))
    ax.add_patch(Circle((cx + r * 0.45, cy + r * 0.2), r * 0.85, fc=bg, ec="none"))


def sun(ax, cx, cy, r):
    ax.add_patch(Circle((cx, cy), r, fc=YEL, ec=INK, lw=1.2))


def question(ax, x, y, size=28):
    ax.text(x, y, "?", ha="center", va="center", fontsize=size, color=RED, fontweight="bold")


# 1. 여는 장면: 밤에 보낸 메시지가 꺼진 휴대폰을 지나 아침에 도착
fig, ax = canvas(9.6, 3.8, 16.0, 6.4)
ax.add_patch(Rectangle((0.2, 0.2), 7.2, 5.9, fc="#eef0f4", ec=GREY, lw=1))
ax.add_patch(Rectangle((8.6, 0.2), 7.2, 5.9, fc="white", ec=GREY, lw=1))
moon(ax, 0.9, 5.4, 0.35, bg="#eef0f4"); ax.text(1.5, 5.4, "밤", va="center", fontsize=13, fontweight="bold")
sun(ax, 9.3, 5.4, 0.35); ax.text(9.9, 5.4, "아침", va="center", fontsize=13, fontweight="bold")
phone(ax, 1.9, 0.9, 3.2, on=True, text="바다 가자")
ax.text(1.9, 0.6, "나", ha="center", va="top", fontsize=12, color=INK)
phone(ax, 5.8, 0.9, 3.2, on=False)
ax.text(5.8, 0.6, "친구 (꺼짐)", ha="center", va="top", fontsize=12, color=INK)
arrow(ax, (3.0, 3.0), (4.6, 3.0), color=RED)
question(ax, 8.0, 3.2)
phone(ax, 12.2, 0.9, 3.2, on=True, text="바다 가자")
ax.text(12.2, 0.6, "친구 (켬)", ha="center", va="top", fontsize=12, color=INK)
save(fig, "c11-night.svg")

# 2. 이 편의 지도: 받는 사람 적기 → 여러 곳 거치기 → 맡아 두기 → 친구 휴대폰
fig, ax = canvas(11.6, 2.9, 19.4, 4.6)
titles = ["받는 사람 적기", "여러 곳 거치기", "맡아 두기", "친구 휴대폰"]
for i, t in enumerate(titles):
    x = 0.3 + i * 4.8
    box(ax, x, 0.4, 3.8, 3.6)
    ax.text(x + 1.9, 0.95, t, ha="center", va="center", fontsize=13, fontweight="bold")
    if i == 0:
        parcel(ax, x + 0.8, 1.6, 2.2, 1.8, "받는 사람: 친구", red=True, size=7.5)
    elif i == 1:
        for k in range(3):
            computer(ax, x + 0.75 + k * 1.15, 2.0, s=0.7)
    elif i == 2:
        server(ax, x + 1.2, 1.45, 1.4, 2.2)
        ax.add_patch(Rectangle((x + 1.5, 1.45 + 2.2 / 3 + 0.08), 0.8, 0.5, fc=RED, ec=INK, lw=1.2))
    else:
        phone(ax, x + 1.9, 1.4, 2.3, on=True)
        ax.add_patch(FancyBboxPatch((x + 1.6, 2.5), 0.6, 0.3, boxstyle="round,pad=0.05", fc=RED, ec=RED))
    if i < 3:
        arrow(ax, (x + 3.95, 2.2), (x + 4.65, 2.2))
save(fig, "c11-map.svg")

# 3. 받는 사람 적기: 택배 상자와 메시지 상자
fig, ax = canvas(8.4, 3.4, 14.0, 5.6)
parcel(ax, 1.0, 1.2, 4.2, 3.4, "받는 사람: 친구", inner="장난감")
ax.text(3.1, 0.6, "택배 상자", ha="center", fontsize=13, fontweight="bold")
parcel(ax, 8.6, 1.2, 4.2, 3.4, "받는 사람: 친구", inner="바다 가자", red=True)
ax.text(10.7, 0.6, "메시지", ha="center", fontsize=13, fontweight="bold")
save(fig, "c11-label.svg")

# 4. 여러 곳 거치기: 택배 길과 메시지 길을 나란히
fig, ax = canvas(11.0, 4.6, 18.4, 7.6)
ax.text(0.3, 6.9, "택배", fontsize=13, fontweight="bold")
house(ax, 2.2, 4.6, 1.2, "우리 동네")
warehouse(ax, 9.2, 4.6, 1.4, "큰 물류 센터")
house(ax, 16.2, 4.6, 1.2, "친구 동네")
arrow(ax, (3.2, 5.1), (7.7, 5.1)); arrow(ax, (10.7, 5.1), (15.2, 5.1))
ax.text(9.2, 6.6, "하루쯤", ha="center", fontsize=11, color=INK)
ax.plot([0.3, 18.1], [3.6, 3.6], color=GREY, lw=1, ls="--")
ax.text(0.3, 3.0, "메시지", fontsize=13, fontweight="bold")
phone(ax, 1.4, 0.4, 2.0, on=True)
for k, cx in enumerate((5.4, 9.2, 13.0)):
    computer(ax, cx, 0.8)
phone(ax, 17.0, 0.4, 2.0, on=True)
for a, b in ((2.2, 4.6), (6.2, 8.4), (10.0, 12.2), (13.8, 16.3)):
    arrow(ax, (a, 1.3), (b, 1.3), color=RED)
ax.text(9.2, 2.35, "어디로 가는지만 보고 넘겨요", ha="center", fontsize=11, color=INK)
ax.text(9.2, 0.15, "눈 깜짝할 사이", ha="center", fontsize=11, color=RED)
save(fig, "c11-route.svg")

# 5. 서버가 맡아 둔다: 밤에는 선반에, 아침에 친구 휴대폰으로
fig, ax = canvas(9.6, 4.0, 16.0, 6.6)
server(ax, 6.2, 0.9, 3.6, 4.6)
ax.text(8.0, 0.45, "서버", ha="center", fontsize=13, fontweight="bold")
ax.add_patch(Rectangle((6.6, 0.9 + 4.6 / 3 + 0.12), 1.2, 0.8, fc=BOX, ec=INK, lw=1.2))
ax.add_patch(Rectangle((8.1, 0.9 + 4.6 / 3 + 0.12), 1.3, 0.8, fc=RED, ec=INK, lw=1.4))
ax.text(8.75, 0.9 + 4.6 / 3 + 0.52, "친구", ha="center", va="center", fontsize=10, color="white",
        fontweight="bold")
ax.add_patch(Rectangle((6.6, 0.9 + 2 * 4.6 / 3 + 0.12), 1.5, 0.8, fc=BOX, ec=INK, lw=1.2))
moon(ax, 0.9, 5.9, 0.3); ax.text(1.4, 5.9, "밤", va="center", fontsize=12, fontweight="bold")
phone(ax, 2.4, 1.2, 3.4, on=False)
ax.text(2.4, 0.85, "꺼져 있어요", ha="center", va="top", fontsize=11, color=INK)
ax.add_patch(FancyArrowPatch((6.05, 3.0), (3.5, 3.0), arrowstyle="-|>", mutation_scale=16, color=GREY, lw=1.8,
                             ls="--"))
ax.text(4.78, 3.0, "×", ha="center", va="center", fontsize=22, color=INK, fontweight="bold")
ax.text(4.78, 2.4, "못 건네요", ha="center", va="top", fontsize=10, color=INK)
sun(ax, 12.6, 5.9, 0.3); ax.text(13.1, 5.9, "아침", va="center", fontsize=12, fontweight="bold")
phone(ax, 13.8, 1.2, 3.4, on=True, text="바다 가자")
ax.text(13.8, 0.85, "켜면 건네요", ha="center", va="top", fontsize=11, color=INK)
arrow(ax, (9.95, 3.0), (12.7, 3.0), color=RED)
save(fig, "c11-server.svg")

print("ok")
