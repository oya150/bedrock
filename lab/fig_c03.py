"""컴퓨터 3편 그림 만들기. 실행: python lab/fig_c03.py  → docs/computer/img/03/*.svg

확인용 PNG: FIG_FMT=png FIG_OUT=<폴더> python lab/fig_c03.py
글자는 SVG 안에 글자로 남긴다(글꼴 모양을 파일에 넣지 않는다). 보는 쪽 글꼴로 그려진다.
웃는 얼굴은 글꼴마다 모양이 달라서 글자 대신 도형으로 그린다. 강조는 빨강 하나만 쓴다.
"""
import math
import os

import matplotlib

matplotlib.use("svg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch, Polygon, Rectangle, Wedge

FMT = os.environ.get("FIG_FMT", "svg")
OUT = os.environ.get("FIG_OUT") or os.path.join(os.path.dirname(__file__), "..", "docs", "computer", "img", "03")
os.makedirs(OUT, exist_ok=True)

plt.rcParams.update({
    "font.family": ["Apple SD Gothic Neo", "Noto Sans KR", "Malgun Gothic", "sans-serif"],
    "svg.fonttype": "none",
    "text.color": "#222",
    "figure.facecolor": "white",
    "savefig.facecolor": "white",
})

RED, GREY, INK, PAPER, YEL = "#e4572e", "#c9ccd1", "#555", "#f4f6f8", "#f6c445"
SMILE = "😀"  # 표에서 웃는 얼굴 자리를 뜻하는 표시. 그릴 때는 도형으로 바꾼다.
MINE = {"사": 1, "랑": 2, "해": 3, "요": 4, SMILE: 5}
GRANDMA = {1: "고", 2: "래", 3: "해", 4: "요", 5: SMILE}
WORD = ["사", "랑", "해", "요", SMILE]


def save(fig, name):
    fig.savefig(os.path.join(OUT, name.replace(".svg", "." + FMT)), bbox_inches="tight", pad_inches=0.25,
                dpi=110)
    plt.close(fig)


def canvas(w, h, xmax, ymax):
    fig, ax = plt.subplots(figsize=(w, h))
    ax.set_xlim(0, xmax); ax.set_ylim(0, ymax); ax.axis("off")
    return fig, ax


def box(ax, x, y, w, h, fc="white", ec=INK, lw=1.8):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.08", fc=fc, ec=ec, lw=lw))


def arrow(ax, a, b, color=INK, lw=2):
    ax.add_patch(FancyArrowPatch(a, b, arrowstyle="-|>", mutation_scale=18, color=color, lw=lw))


def smiley(ax, cx, cy, r):
    ax.add_patch(Circle((cx, cy), r, fc=YEL, ec="#b8901e", lw=1))
    for dx in (-0.35, 0.35):
        ax.add_patch(Circle((cx + dx * r, cy + 0.22 * r), 0.12 * r, fc="#222"))
    ax.add_patch(Wedge((cx, cy - 0.05 * r), 0.55 * r, 200, 340, width=0.14 * r, fc="#222"))


def star(ax, cx, cy, r):
    """새 이모지 자리에 그리는 별 도형."""
    pts = []
    for k in range(10):
        a = math.pi / 2 + k * math.pi / 5
        rr = r if k % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    ax.add_patch(Polygon(pts, closed=True, fc=YEL, ec="#b8901e", lw=1))


def glyph(ax, ch, cx, cy, size=20, color="#222"):
    """글자 하나를 그린다. 웃는 얼굴 표시는 도형으로 바꾼다."""
    if ch == SMILE:
        smiley(ax, cx, cy, size / 60)
    else:
        ax.text(cx, cy, ch, ha="center", va="center", fontsize=size, color=color)


def cell(ax, x, y, w, h, ch=None, num=None, ec=GREY, lw=1.2, size=20, color="#222"):
    ax.add_patch(Rectangle((x, y), w, h, fc="white", ec=ec, lw=lw))
    if ch is not None:
        glyph(ax, ch, x + w / 2, y + h / 2, size=size, color=color)
    if num is not None:
        ax.text(x + w / 2, y + h / 2, str(num), ha="center", va="center", fontsize=size, color=color)


def bubble(ax, x, y, word):
    box(ax, x, y, 3.4, 0.9, fc="#fff8d6", ec="#b8901e", lw=1.4)
    for i, ch in enumerate(word):
        glyph(ax, ch, x + 0.45 + i * 0.62, y + 0.45, size=16)


# 1. 여는 장면: 내 휴대폰에서 할머니 휴대폰으로
fig, ax = canvas(8.6, 3.8, 13, 5.8)
for x, who in [(0.4, "내 휴대폰"), (8.6, "할머니 휴대폰")]:
    box(ax, x, 0.6, 4.0, 5.0, fc=PAPER)
    bubble(ax, x + 0.3, 3.6, WORD)
    ax.text(x + 2.0, 0.95, who, ha="center", fontsize=12)
arrow(ax, (4.8, 3.1), (8.2, 3.1))
ax.text(6.5, 3.5, "보내기", ha="center", fontsize=13)
save(fig, "c03-send.svg")

# 2. 사진은 칸마다 색 번호가 됐다(2편의 색 번호표: 0 흰색, 1 검정, 2 노랑). 글자는?
fig, ax = canvas(8.6, 3.6, 13.4, 5.6)
ax.text(2.6, 5.15, "사진", ha="center", fontsize=14, fontweight="bold")
ax.text(9.4, 5.15, "글자", ha="center", fontsize=14, fontweight="bold")
colors = {0: "white", 1: "#222", 2: YEL}
pic = [[2, 2, 2], [1, 2, 1], [2, 1, 2]]
for r, row in enumerate(pic):
    for c, v in enumerate(row):
        x, y = 0.5 + c * 1.4, 3.3 - r * 1.4
        ax.add_patch(Rectangle((x, y), 1.4, 1.4, fc=colors[v], ec=GREY, lw=1.2))
        ax.text(x + 0.7, y + 0.7, str(v), ha="center", va="center", fontsize=15,
                color="white" if v == 1 else "#222", fontweight="bold")
for i, ch in enumerate(["사", "랑", "해", "요"]):
    x = 6.8 + i * 1.35
    cell(ax, x, 3.0, 1.2, 1.2, ch=ch, size=20)
    cell(ax, x, 1.4, 1.2, 1.2, ch="?", size=22, ec=RED, lw=2, color=RED)
save(fig, "c03-only-numbers.svg")

# 3. 글자 번호표
fig, ax = canvas(7.4, 2.6, 11, 4.0)
ax.text(5.5, 3.6, "글자 번호표", ha="center", fontsize=14, color=INK)
for i, ch in enumerate(WORD):
    x = 0.5 + i * 2.0
    cell(ax, x, 1.8, 1.6, 1.4, ch=ch, size=24)
    cell(ax, x, 0.4, 1.6, 1.4, num=MINE[ch], size=22)
save(fig, "c03-table.svg")

# 4. 보낼 때는 번호를 보낸다: 글자 → 번호 → (보내기) → 번호 → 글자
fig, ax = canvas(7.8, 6.6, 12, 10.2)
rows = [("내 휴대폰 글자", "ch", 8.6), ("바꾼 번호", "num", 6.9), ("받은 번호", "num", 3.3), ("할머니 휴대폰 글자", "ch", 1.6)]
for label, kind, y in rows:
    ax.text(0.2, y + 0.6, label, va="center", fontsize=12, color=INK)
    for i, ch in enumerate(WORD):
        x = 4.0 + i * 1.5
        if kind == "ch":
            cell(ax, x, y, 1.2, 1.2, ch=ch, size=20)
        else:
            cell(ax, x, y, 1.2, 1.2, num=MINE[ch], size=20)
for i in range(5):
    x = 4.6 + i * 1.5
    ax.plot([x, x], [8.55, 8.15], color=GREY, lw=1.2)
    ax.plot([x, x], [3.25, 2.85], color=GREY, lw=1.2)
arrow(ax, (7.6, 6.7), (7.6, 4.7), color=RED, lw=2.5)
ax.text(8.0, 5.7, "보내기", va="center", fontsize=13, color=RED, fontweight="bold")
save(fig, "c03-numbers.svg")

# 5. 표가 다르면: 같은 번호가 엉뚱한 글자가 된다
fig, ax = canvas(7.8, 4.4, 12, 6.4)
ax.text(0.2, 4.9, "받은 번호", va="center", fontsize=12, color=INK)
ax.text(0.2, 1.4, "다른 표로\n바꾼 글자", va="center", fontsize=12, color=INK)
for i in range(5):
    x = 4.0 + i * 1.5
    cell(ax, x, 4.3, 1.2, 1.2, num=i + 1, size=20)
    wrong = i < 2
    cell(ax, x, 0.8, 1.2, 1.2, ch=GRANDMA[i + 1], size=20, ec=RED if wrong else GREY, lw=3 if wrong else 1.2,
         color=RED if wrong else "#222")
    ax.add_patch(FancyArrowPatch((x + 0.6, 4.2), (x + 0.6, 2.1), arrowstyle="-|>", mutation_scale=14, color=GREY, lw=1.2))
ax.text(7.75, 0.15, "다른 표: 1 → 고, 2 → 래", ha="center", va="center", fontsize=12, color=RED)
save(fig, "c03-wrong.svg")

# 6. 문자 코드(유니코드)의 실제 번호 몇 개. 번호는 파이썬 ord()로 낸 값
fig, ax = canvas(9.4, 3.4, 14.4, 5.0)
ax.text(7.2, 4.4, "유니코드", ha="center", fontsize=13, color=INK)
for k, ch in enumerate(["A", "B", "a", "가", SMILE]):
    x = 0.5 + k * 2.8
    hot = ch == "가"
    cell(ax, x, 2.2, 2.3, 1.6, ch=ch, size=24)
    cell(ax, x, 1.0, 2.3, 1.2, num=ord(ch), size=15, color=RED if hot else INK,
         ec=RED if hot else GREY, lw=2.5 if hot else 1.2)
save(fig, "c03-world.svg")

# 7. 번호는 왔는데 그림이 없으면 빈 네모
fig, ax = canvas(8.6, 4.4, 13, 6.6)
cell(ax, 4.9, 5.0, 3.2, 1.1, num="새 이모지 번호", size=12, color=INK)
for x, has, label in [(0.6, True, "그림 있음"), (8.0, False, "그림 없음")]:
    box(ax, x, 0.5, 4.4, 3.4, fc=PAPER)
    ax.text(x + 2.2, 0.85, label, ha="center", fontsize=12, color=INK if has else RED)
    if has:
        star(ax, x + 2.2, 2.45, 0.75)
    else:
        ax.add_patch(Rectangle((x + 1.6, 1.8), 1.2, 1.3, fc="white", ec=RED, lw=2.5))
    arrow(ax, (6.5, 4.9), (x + 2.2, 4.0))
save(fig, "c03-tofu.svg")

print("ok")
