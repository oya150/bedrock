"""컴퓨터 10편 그림 만들기. 실행: python lab/fig_c10.py  → docs/computer/img/10/*.svg

글자는 SVG 안에 글자로 남긴다(글꼴 모양을 파일에 넣지 않는다). 보는 쪽 글꼴로 그려진다.
바뀐 글자(암호)와 열쇠만 빨강으로 칠한다.
확인용 PNG: FIG_FMT=png FIG_OUT=<폴더> python lab/fig_c10.py
"""
import os

import matplotlib

FMT = os.environ.get("FIG_FMT", "svg")
matplotlib.use("svg" if FMT == "svg" else "agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch, Rectangle

OUT = os.environ.get("FIG_OUT") or os.path.join(os.path.dirname(__file__), "..", "docs", "computer", "img", "10")
os.makedirs(OUT, exist_ok=True)

plt.rcParams.update({
    "font.family": ["Apple SD Gothic Neo", "Noto Sans KR", "Malgun Gothic", "sans-serif"],
    "svg.fonttype": "none",
    "text.color": "#222",
    "figure.facecolor": "white",
    "savefig.facecolor": "white",
})

RED, GREY, INK, PAPER, NOTE, YEL = "#e4572e", "#c9ccd1", "#555", "#f4f6f8", "#fffdf5", "#f6c445"
ROW = "가나다라마바사아자차카타파하"


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


def arrow(ax, a, b, color=INK, lw=2, rad=0.0):
    ax.add_patch(FancyArrowPatch(a, b, arrowstyle="-|>", mutation_scale=18, color=color, lw=lw,
                                 connectionstyle=f"arc3,rad={rad}"))


def kid(ax, cx, ground, h):
    """앉은 아이: 머리와 몸통."""
    ax.add_patch(Circle((cx, ground + h * 0.78), h * 0.17, fc="white", ec=INK, lw=1.6))
    ax.add_patch(FancyBboxPatch((cx - h * 0.2, ground), h * 0.4, h * 0.5, boxstyle="round,pad=0.04",
                                fc=PAPER, ec=INK, lw=1.6))


def note(ax, x, y, w, h, text="", color="#222", size=12, folded=False):
    ax.add_patch(Rectangle((x, y), w, h, fc=NOTE, ec=INK, lw=1.4))
    if folded:
        ax.plot([x, x + w], [y + h / 2, y + h / 2], color=GREY, lw=1)
    if text:
        ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=size, color=color,
                fontweight="bold")


def nums(ax, cx, cy, values, color="#222", c=0.55, gap=0.12, space=0.35):
    """번호 쪽지: 번호마다 칸 하나. None 은 띄어쓰기 자리."""
    w = sum(space if v is None else c + gap for v in values) - gap
    x = cx - w / 2
    ax.add_patch(Rectangle((x - 0.25, cy - c / 2 - 0.25), w + 0.5, c + 0.5, fc=NOTE, ec=INK, lw=1.4))
    for v in values:
        if v is None:
            x += space
            continue
        ax.add_patch(Rectangle((x, cy - c / 2), c, c, fc="white", ec=GREY, lw=1))
        ax.text(x + c / 2, cy, str(v), ha="center", va="center", fontsize=13, color=color, fontweight="bold")
        x += c + gap


def question(ax, x, y, size=26):
    ax.text(x, y, "?", ha="center", va="center", fontsize=size, color=RED, fontweight="bold")


def strip(ax, x, y, letters, c=0.62, hl=(), hl_color=RED, nums=False, size=13):
    """글자 띠: 칸마다 글자 하나. hl 에 든 칸은 굵은 테두리."""
    for i, ch in enumerate(letters):
        on = i in hl
        ax.add_patch(Rectangle((x + i * c, y), c, c, fc="white", ec=hl_color if on else INK,
                               lw=2.2 if on else 1.0, zorder=2 if on else 1))
        ax.text(x + i * c + c / 2, y + c / 2, ch, ha="center", va="center", fontsize=size,
                color=hl_color if on else "#222", fontweight="bold" if on else "normal")
        if nums:
            ax.text(x + i * c + c / 2, y - 0.12, str(i + 1), ha="center", va="top", fontsize=9, color=INK)


def shift(word, k):
    return "".join(ch if ch == " " else ROW[(ROW.index(ch) + k) % len(ROW)] for ch in word)


# 1. 여는 장면: 쪽지가 친구들 손을 거쳐 뒤로 간다. 가운데 친구가 펼쳐 본다
fig, ax = canvas(9.0, 3.6, 15.0, 6.0)
xs = [1.6, 5.3, 9.0, 12.7]
for i, cx in enumerate(xs):
    ax.add_patch(Rectangle((cx - 1.2, 0.9), 2.4, 0.35, fc=GREY, ec=INK, lw=1.2))
    kid(ax, cx, 1.25, 2.6)
ax.text(xs[0], 0.45, "보내는 나", ha="center", fontsize=12, color=INK)
ax.text(xs[3], 0.45, "받을 친구", ha="center", fontsize=12, color=INK)
note(ax, xs[0] + 0.5, 2.0, 0.5, 0.4, folded=True)
arrow(ax, (xs[0] + 0.9, 4.6), (xs[1] - 0.6, 4.6), rad=-0.25)
arrow(ax, (xs[1] + 0.9, 4.6), (xs[2] - 0.6, 4.6), rad=-0.25)
arrow(ax, (xs[2] + 0.9, 4.6), (xs[3] - 0.6, 4.6), color=GREY, rad=-0.25)
note(ax, xs[2] - 0.75, 2.05, 1.5, 0.9, "바다 가자", size=11)
question(ax, xs[2] + 1.3, 4.0)
save(fig, "c10-note.svg")

# 3. 번호로만 쓰면: 번호표를 가진 사람은 누구나 읽는다
fig, ax = canvas(10.4, 3.6, 17.4, 6.0)
strip(ax, 4.2, 4.3, ROW, c=0.66, hl=(0, 2, 5, 8), hl_color=INK, nums=True)
ax.text(4.2 + 14 * 0.66 / 2, 5.35, "연습용 번호표", ha="center", fontsize=12, color=INK)
nums(ax, 1.9, 1.7, [6, 3, None, 1, 9])
ax.text(1.9, 0.55, "번호로 쓴 쪽지", ha="center", fontsize=12, color=INK)
kid(ax, 9.3, 0.5, 2.4)
arrow(ax, (3.6, 1.7), (8.5, 1.7))
note(ax, 11.0, 1.0, 3.0, 1.4, "바다 가자", size=16)
arrow(ax, (10.1, 1.7), (10.9, 1.7))
ax.text(12.5, 0.55, "중간 친구", ha="center", fontsize=12, color=INK)
save(fig, "c10-plain.svg")

# 4. 한 칸씩 밀기: 윗줄 글자를 바로 아래 글자로
fig, ax = canvas(10.4, 4.2, 17.4, 7.0)
c, x0 = 0.95, 2.0
sel = [ROW.index(ch) for ch in "바다가자"]
strip(ax, x0, 4.6, ROW, c=c, hl=sel, hl_color=INK)
strip(ax, x0, 2.6, ROW[1:] + ROW[0], c=c, hl=sel)
ax.text(x0 - 0.3, 4.6 + c / 2, "원래 글자", ha="right", va="center", fontsize=12, color=INK)
ax.text(x0 - 0.3, 2.6 + c / 2, "바꿀 글자", ha="right", va="center", fontsize=12, color=RED)
for i in sel:
    arrow(ax, (x0 + i * c + c / 2, 4.55), (x0 + i * c + c / 2, 2.6 + c + 0.05), lw=1.6)
ax.text(x0 + 13.5 * c, 2.45, "하 → 가", ha="center", va="top", fontsize=10, color=INK)
ax.text(5.0, 1.0, "바다 가자", ha="center", va="center", fontsize=18, fontweight="bold")
arrow(ax, (7.0, 1.0), (9.4, 1.0))
ax.text(11.6, 1.0, shift("바다 가자", 1), ha="center", va="center", fontsize=18, fontweight="bold",
        color=RED)
save(fig, "c10-shift.svg")

# 5. 열쇠: 같은 말도 열쇠가 다르면 다른 암호가 된다
fig, ax = canvas(9.0, 3.4, 15.0, 5.6)
for row, k in enumerate((1, 3)):
    y = 3.9 - row * 2.3
    ax.text(2.0, y, "바다 가자", ha="center", va="center", fontsize=18, fontweight="bold")
    arrow(ax, (3.9, y), (8.4, y))
    ax.add_patch(Circle((6.15, y + 0.75), 0.45, fc="white", ec=RED, lw=2))
    ax.text(6.15, y + 0.75, str(k), ha="center", va="center", fontsize=16, color=RED, fontweight="bold")
    ax.text(6.15, y - 0.45, f"열쇠 {k}: {k}칸 밀기", ha="center", va="center", fontsize=11, color=INK)
    ax.text(11.0, y, shift("바다 가자", k), ha="center", va="center", fontsize=18, fontweight="bold",
            color=RED)
save(fig, "c10-key.svg")

# 6. 컴퓨터는 번호에 열쇠를 더하고, 받는 쪽은 뺀다
fig, ax = canvas(11.6, 3.4, 19.4, 5.6)
cols = [
    (1.4, "바다 가자", "글자", "#222"),
    (5.6, [6, 3, None, 1, 9], "번호", "#222"),
    (9.8, [7, 4, None, 2, 10], "열쇠 1 더하기", RED),
    (14.0, [6, 3, None, 1, 9], "열쇠 1 빼기", "#222"),
    (18.0, "바다 가자", "글자", "#222"),
]
for i, (x, t, lab, col) in enumerate(cols):
    if isinstance(t, list):
        nums(ax, x, 3.0, t, color=col, c=0.5, gap=0.08, space=0.25)
    else:
        note(ax, x - 1.3, 2.4, 2.6, 1.2, t, color=col, size=14)
    ax.text(x, 1.95, lab, ha="center", va="top", fontsize=12, color=RED if col == RED else INK,
            fontweight="bold" if col == RED else "normal")
    if i < 4:
        nx = cols[i + 1][0]
        arrow(ax, (x + 1.4, 3.0), (nx - 1.4, 3.0), color=RED if i == 2 else INK)
ax.text((9.8 + 14.0) / 2, 3.55, "보내기", ha="center", va="bottom", fontsize=12, color=RED)
ax.text(5.6, 4.6, "내 휴대폰", ha="center", fontsize=12, color=INK)
ax.text(16.0, 4.6, "친구 휴대폰", ha="center", fontsize=12, color=INK)
save(fig, "c10-add.svg")

# 7. 글자 바퀴: 하 다음은 다시 가, 14칸 밀면 제자리
import math
fig, ax = canvas(5.6, 5.6, 9.0, 9.0)
cx, cy, R = 4.5, 4.5, 3.3
for i, ch in enumerate(ROW):
    ang = math.pi / 2 - 2 * math.pi * i / len(ROW)
    x, y = cx + R * math.cos(ang), cy + R * math.sin(ang)
    on = ch in "하가"
    ax.add_patch(Circle((x, y), 0.46, fc="white", ec=RED if on else INK, lw=2.2 if on else 1.2))
    ax.text(x, y, ch, ha="center", va="center", fontsize=15, color=RED if on else "#222",
            fontweight="bold" if on else "normal")
    ax.text(cx + (R - 0.95) * math.cos(ang), cy + (R - 0.95) * math.sin(ang), str(i + 1),
            ha="center", va="center", fontsize=10, color=INK)
a0 = math.pi / 2 - 2 * math.pi * 13 / len(ROW)
a1 = math.pi / 2
R2 = R + 0.85
arrow(ax, (cx + R2 * math.cos(a0), cy + R2 * math.sin(a0)), (cx + R2 * math.cos(a1) - 0.2, cy + R2 * math.sin(a1)),
      color=RED, rad=-0.3)
ax.text(cx, cy, "14글자", ha="center", va="center", fontsize=16, fontweight="bold", color=INK)
save(fig, "c10-wheel.svg")

# 8. 열쇠를 모르면 하나씩 되돌려 본다: 자바 라타
fig, ax = canvas(8.4, 4.0, 14.0, 6.6)
secret = shift("바다 가자", 3)
ax.text(2.0, 5.6, secret, ha="center", va="center", fontsize=18, fontweight="bold", color=RED)
ax.text(2.0, 4.8, "받은 쪽지", ha="center", va="center", fontsize=11, color=INK)
for row, k in enumerate((1, 2, 3)):
    y = 3.6 - row * 1.2
    on = k == 3
    ax.text(5.6, y, f"{k}칸 되돌리기", ha="right", va="center", fontsize=13, color=RED if on else INK,
            fontweight="bold" if on else "normal")
    arrow(ax, (6.0, y), (7.6, y), color=RED if on else INK)
    ax.text(9.9, y, shift(secret, -k), ha="center", va="center", fontsize=17, color=RED if on else "#222",
            fontweight="bold" if on else "normal")
    ax.text(12.4, y, "O" if on else "X", ha="center", va="center", fontsize=16, color=RED if on else GREY,
            fontweight="bold")
save(fig, "c10-try.svg")

print("ok")
