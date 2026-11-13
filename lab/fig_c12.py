"""컴퓨터 12편 그림 만들기. 실행: python lab/fig_c12.py  → docs/computer/img/12/*.svg

글자는 SVG 안에 글자로 남긴다(글꼴 모양을 파일에 넣지 않는다). 보는 쪽 글꼴로 그려진다.
찾는 낱말("바다")과 찾은 것만 빨강으로 칠한다. 휴대폰·도감은 특정 제품이 아닌 일반 모양이다.
"""
import os

import matplotlib

matplotlib.use("svg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch, Rectangle

OUT = os.path.join(os.path.dirname(__file__), "..", "docs", "computer", "img", "12")
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
    # FIG_FMT=png FIG_OUT=폴더 로 확인용 PNG 사본을 만든다.
    fmt = os.environ.get("FIG_FMT", "svg")
    out = os.environ.get("FIG_OUT", OUT)
    os.makedirs(out, exist_ok=True)
    if fmt != "svg":
        name = name.rsplit(".", 1)[0] + "." + fmt
    fig.savefig(os.path.join(out, name), bbox_inches="tight", pad_inches=0.25, dpi=110)
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


def phone_frame(ax, cx, y, h):
    w = h * 0.55
    ax.add_patch(FancyBboxPatch((cx - w / 2, y), w, h, boxstyle="round,pad=0.06", fc=PAPER, ec=INK, lw=2))
    ax.add_patch(Rectangle((cx - w / 2 + 0.12, y + 0.25), w - 0.24, h - 0.45, fc="white", ec=INK, lw=1))
    return cx - w / 2 + 0.12, y + 0.25, w - 0.24, h - 0.45


def msg(ax, x, y, w, h, text, red=False, size=10):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.04", fc=RED if red else PAPER,
                                ec=RED if red else GREY, lw=1))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=size,
            color="white" if red else "#222", fontweight="bold" if red else "normal")


def card(ax, x, y, w, h, num, text=None, red=False):
    """번호 붙은 메시지 카드."""
    ax.add_patch(Rectangle((x, y), w, h, fc=NOTE, ec=RED if red else INK, lw=2 if red else 1.2))
    ax.text(x + 0.12, y + h - 0.12, f"{num}번", ha="left", va="top", fontsize=9, color=INK)
    if text:
        ax.text(x + w / 2, y + h * 0.38, text, ha="center", va="center", fontsize=11,
                color=RED if red else "#222", fontweight="bold" if red else "normal")


def magnifier(ax, cx, cy, r, color=INK):
    ax.add_patch(Circle((cx, cy), r, fc="none", ec=color, lw=2.4))
    ax.plot([cx + r * 0.7, cx + r * 1.6], [cy - r * 0.7, cy - r * 1.6], color=color, lw=3.5,
            solid_capstyle="round")


def question(ax, x, y, size=28):
    ax.text(x, y, "?", ha="center", va="center", fontsize=size, color=RED, fontweight="bold")


# 1. 여는 장면: 위로 한참 올리기 vs 검색 칸에 "바다"
fig, ax = canvas(9.0, 4.4, 15.0, 7.4)
x, y, w, h = phone_frame(ax, 3.0, 0.5, 6.4)
for k in range(8):
    msg(ax, x + 0.2 + (0.6 if k % 2 else 0), y + 0.3 + k * 0.68, w - 1.0, 0.45, "…")
arrow(ax, (x + w + 0.55, y + 1.0), (x + w + 0.55, y + h - 0.6))
ax.text(x + w + 0.75, y + h / 2, "계속\n위로", ha="left", va="center", fontsize=11, color=INK)
question(ax, 7.5, 3.8)
x, y, w, h = phone_frame(ax, 12.0, 0.5, 6.4)
ax.add_patch(FancyBboxPatch((x + 0.15, y + h - 0.75), w - 0.3, 0.5, boxstyle="round,pad=0.04", fc="white",
                            ec=INK, lw=1.4))
magnifier(ax, x + 0.45, y + h - 0.5, 0.12)
ax.text(x + 0.75, y + h - 0.5, "바다", ha="left", va="center", fontsize=12, color=RED, fontweight="bold")
msg(ax, x + 0.2, y + h - 1.65, w - 0.4, 0.55, "바다 가자", red=True, size=11)
save(fig, "c12-find.svg")

# 3. 하나씩 다 보기: 1번부터 차례로 돋보기가 옮겨 간다
fig, ax = canvas(11.0, 3.0, 18.4, 5.0)
for k in range(8):
    card(ax, 0.4 + k * 1.9, 1.6, 1.5, 1.6, k + 1)
ax.text(15.9, 2.4, "…", ha="center", va="center", fontsize=22, color=INK)
card(ax, 16.6, 1.6, 1.5, 1.6, 300)
magnifier(ax, 1.15, 2.3, 0.35)
for k in range(3):
    arrow(ax, (1.1 + k * 1.9, 3.5), (2.9 + k * 1.9, 3.5), rad=-0.4, lw=1.6)
ax.text(9.2, 0.7, "메시지 300개 → 돋보기 300번", ha="center", fontsize=14, fontweight="bold")
save(fig, "c12-scan.svg")

# 4. 도감 맨 뒤 찾아보기
fig, ax = canvas(9.6, 4.2, 16.0, 7.0)
ax.add_patch(Rectangle((0.6, 0.6), 6.4, 5.8, fc="white", ec=INK, lw=2))
ax.text(3.8, 5.8, "찾아보기", ha="center", va="center", fontsize=15, fontweight="bold")
rows = [("브라키오사우루스", 18), ("스테고사우루스", 30), ("트리케라톱스", 36), ("티라노사우루스", 42)]
for k, (name, page) in enumerate(rows):
    yy = 4.8 - k * 0.95
    red = page == 42
    col = RED if red else "#222"
    ax.text(1.0, yy, name, ha="left", va="center", fontsize=12, color=col, fontweight="bold" if red else "normal")
    ax.plot([4.75, 5.95], [yy, yy], color=GREY, lw=1.2, ls=":")
    ax.text(6.6, yy, str(page), ha="right", va="center", fontsize=12, color=col,
            fontweight="bold" if red else "normal")
ax.text(3.8, 0.2, "도감 맨 뒤", ha="center", va="center", fontsize=12, color=INK)
arrow(ax, (7.2, 1.95), (9.4, 3.3), color=RED)
ax.add_patch(Rectangle((9.6, 0.6), 5.8, 5.8, fc="white", ec=INK, lw=2))
ax.text(12.5, 5.7, "42쪽", ha="center", va="center", fontsize=14, fontweight="bold", color=RED)
ax.text(12.5, 3.2, "티라노사우루스", ha="center", va="center", fontsize=14)
save(fig, "c12-book.svg")

# 5. 색인 만들기: 메시지가 올 때마다 낱말로 나눠 줄마다 번호를 적는다 (장면 띠 3장)


def index_table(ax, x, y_top, rows, new_nums, hi_word=None, w=5.6):
    """색인 표. rows=[(낱말, [번호…])], new_nums={(낱말, 번호)} 는 빨강."""
    n = len(rows)
    rh = 0.95
    h = 0.75 + rh * n + 0.2
    ax.add_patch(Rectangle((x, y_top - h), w, h, fc="white", ec=INK, lw=2))
    ax.text(x + w / 2, y_top - 0.38, "색인", ha="center", va="center", fontsize=14, fontweight="bold")
    ax.plot([x, x + w], [y_top - 0.75, y_top - 0.75], color=INK, lw=1.2)
    ax.plot([x + 2.0, x + 2.0], [y_top - h, y_top - 0.75], color=GREY, lw=1)
    for k, (word, nums) in enumerate(rows):
        yy = y_top - 0.75 - rh * (k + 0.5) - 0.1
        hi = word == hi_word
        if hi:
            ax.add_patch(Rectangle((x + 0.05, yy - rh / 2 + 0.05), w - 0.1, rh - 0.1, fc="#fde4dc", ec=RED, lw=2))
        ax.text(x + 1.0, yy, word, ha="center", va="center", fontsize=13, color=RED if hi else "#222",
                fontweight="bold" if hi else "normal")
        xx = x + 2.4
        for j, num in enumerate(nums):
            red = (word, num) in new_nums or hi
            label = str(num) + ("," if j < len(nums) - 1 else "")
            ax.text(xx, yy, label, ha="left", va="center", fontsize=13, color=RED if red else "#222",
                    fontweight="bold" if red else "normal")
            xx += 0.2 * len(label) + 0.25


def chip(ax, cx, cy, text):
    w = 0.42 * len(text) + 0.5
    ax.add_patch(FancyBboxPatch((cx - w / 2, cy - 0.32), w, 0.64, boxstyle="round,pad=0.05", fc=NOTE, ec=INK,
                                lw=1.2))
    ax.text(cx, cy, text, ha="center", va="center", fontsize=12)


steps = [
    (3, "바다 가자", [("가자", [3]), ("바다", [3])]),
    (8, "같이 가자", [("가자", [3, 8]), ("같이", [8]), ("바다", [3])]),
    (17, "파란 바다", [("가자", [3, 8]), ("같이", [8]), ("바다", [3, 17]), ("파란", [17])]),
]
for i, (num, text, rows) in enumerate(steps, start=1):
    fig, ax = canvas(10.4, 3.2, 17.4, 6.4)
    ax.set_ylim(1.2, 6.4)
    card(ax, 0.3, 2.4, 3.4, 1.6, num, text, red=True)
    ax.text(2.0, 1.9, "새 메시지", ha="center", va="top", fontsize=11, color=INK)
    arrow(ax, (3.9, 3.2), (5.1, 3.2))
    for k, word in enumerate(text.split()):
        chip(ax, 6.4, 3.75 - k * 1.1, word)
    arrow(ax, (7.6, 3.2), (8.8, 3.2))
    new = {(word, num) for word in text.split()}
    index_table(ax, 9.3, 6.2, rows, new)
    save(fig, f"c12-build-{i}.svg")

# 6. 색인으로 찾기: 검색 칸 "바다" → 색인 "바다" 줄 → 3번, 17번
fig, ax = canvas(11.6, 4.0, 19.4, 6.6)
ax.add_patch(FancyBboxPatch((0.3, 3.0), 3.4, 0.8, boxstyle="round,pad=0.05", fc="white", ec=INK, lw=1.6))
magnifier(ax, 0.75, 3.4, 0.18)
ax.text(1.3, 3.4, "바다", ha="left", va="center", fontsize=13, color=RED, fontweight="bold")
ax.text(2.0, 4.3, "검색 칸", ha="center", va="center", fontsize=11, color=INK)
arrow(ax, (3.9, 3.4), (5.6, 3.4), color=RED)
rows = [("가자", [3, 8]), ("같이", [8]), ("바다", [3, 17]), ("파란", [17])]
index_table(ax, 5.9, 6.3, rows, set(), hi_word="바다")
arrow(ax, (11.7, 2.3), (13.3, 4.0), color=RED)
arrow(ax, (11.7, 2.3), (13.3, 1.5), color=RED)
card(ax, 13.6, 3.5, 3.6, 1.5, 3, "바다 가자", red=True)
card(ax, 13.6, 0.7, 3.6, 1.5, 17, "파란 바다", red=True)
save(fig, "c12-index.svg")

print("ok")
