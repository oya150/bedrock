"""인체 11편 그림 만들기. 실행: python lab/fig_b11.py  → docs/body/img/11/*.svg

확인용 PNG: FIG_FMT=png FIG_OUT=<폴더> python lab/fig_b11.py
글자는 SVG 안에 글자로 남긴다(글꼴 모양을 파일에 넣지 않는다). 보는 쪽 글꼴로 그려진다.
그림 안 글씨는 낱말과 숫자만 둔다. 들어오는 알림은 파랑, 나가는 명령은 빨강.
"""
import os

import matplotlib

FMT = os.environ.get("FIG_FMT", "svg")
matplotlib.use("svg" if FMT == "svg" else "agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Arc, Circle, Ellipse, FancyArrowPatch, FancyBboxPatch, Polygon, Rectangle

OUT = os.environ.get("FIG_OUT") or os.path.join(os.path.dirname(__file__), "..", "docs", "body", "img", "11")
os.makedirs(OUT, exist_ok=True)

plt.rcParams.update({
    "font.family": ["Apple SD Gothic Neo", "Noto Sans KR", "Malgun Gothic", "sans-serif"],
    "svg.fonttype": "none",
    "text.color": "#222",
    "figure.facecolor": "white",
    "savefig.facecolor": "white",
})

RED, GREY, INK, NOTE, YEL = "#e4572e", "#c9ccd1", "#555", "#fffdf5", "#f6c445"
NERVE = "#8e5ea2"
IN_C = "#7da2c8"
BONE = "#efe6d2"
SKIN = "#f6d8c4"
MUSCLE = "#f3b7a6"


def save(fig, name):
    if FMT != "svg":
        name = name.replace(".svg", "." + FMT)
    fig.savefig(os.path.join(OUT, name), bbox_inches="tight", pad_inches=0.25, dpi=110)
    plt.close(fig)


def canvas(w, h, xmax, ymax):
    fig, ax = plt.subplots(figsize=(w, h))
    ax.set_xlim(0, xmax); ax.set_ylim(0, ymax); ax.axis("off")
    return fig, ax


def arrow(ax, a, b, color=INK, lw=2, rad=0.0, ms=18):
    ax.add_patch(FancyArrowPatch(a, b, arrowstyle="-|>", mutation_scale=ms, color=color, lw=lw,
                                 connectionstyle=f"arc3,rad={rad}"))


def label(ax, x, y, t, color="#222", fs=11, ha="center", bold=True):
    ax.text(x, y, t, ha=ha, va="center", fontsize=fs, color=color, fontweight="bold" if bold else "normal")


def num(ax, x, y, n, color=RED):
    ax.add_patch(Circle((x, y), 0.32, fc="white", ec=color, lw=1.8))
    ax.text(x, y, str(n), ha="center", va="center", fontsize=11, color=color, fontweight="bold")


def brain(ax, cx, cy, w=3.0, h=2.0, text="뇌"):
    ax.add_patch(Ellipse((cx, cy), w, h, fc=NOTE, ec=INK, lw=1.6))
    for k in range(3):
        ax.add_patch(Arc((cx - w * 0.2 + k * w * 0.2, cy + 0.1), w * 0.3, h * 0.5, theta1=200, theta2=340,
                         color=GREY, lw=1))
    if text:
        label(ax, cx, cy - 0.15, text, fs=13)


def spine(ax, x, top, bottom):
    y = top - 0.55
    while y > bottom:
        ax.add_patch(FancyBboxPatch((x - 0.45, y), 0.9, 0.42, boxstyle="round,pad=0.04", fc=BONE, ec=INK, lw=1))
        y -= 0.6
    ax.plot([x, x], [top, bottom], color=NERVE, lw=4)


def hand(ax, x, y, w=1.4, h=1.2):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.25", fc=SKIN, ec=INK, lw=1.4))


def two_lines(ax, x0, x1, y_in, y_out, ms=14):
    """척수(x0)와 손(x1) 사이: 위 파란 줄은 알림(손→척수), 아래 빨간 줄은 명령(척수→손)."""
    ax.plot([x0, x1], [y_in, y_in], color=IN_C, lw=2.4)
    ax.plot([x0, x1], [y_out, y_out], color=RED, lw=2.4)
    mid = (x0 + x1) / 2
    arrow(ax, (mid + 0.7, y_in), (mid - 0.7, y_in), color=IN_C, lw=2, ms=ms)
    arrow(ax, (mid - 0.7, y_out), (mid + 0.7, y_out), color=RED, lw=2, ms=ms)


# 1. 공을 잡는 길: ① 눈 → ② 뇌 → ③ 척수 → ④ 팔 근육
fig, ax = canvas(10.0, 5.6, 16.0, 9.0)
ax.add_patch(Circle((0.7, 8.3), 0.38, fc=YEL, ec=INK, lw=1.3))
label(ax, 0.7, 7.6, "공", fs=10)
ax.add_patch(Ellipse((1.6, 6.2), 1.0, 0.56, fc="white", ec=INK, lw=1.4))
ax.add_patch(Circle((1.6, 6.2), 0.18, fc=INK))
label(ax, 1.6, 5.55, "눈", fs=11)
ax.plot([0.9, 1.45], [8.0, 6.5], color=GREY, lw=1.2, ls="--")
brain(ax, 5.2, 7.4, w=3.4, h=1.9)
spine(ax, 5.2, 6.45, 1.0)
label(ax, 4.1, 2.0, "척수", color=NERVE, ha="right")
arrow(ax, (2.2, 6.4), (3.6, 7.0), color=IN_C, lw=2.2, ms=16)
num(ax, 2.6, 7.3, 1, color=IN_C)
label(ax, 1.9, 7.75, "알림", color=IN_C, fs=10)
num(ax, 5.2, 8.75, 2)
arrow(ax, (6.0, 6.2), (6.0, 4.5), color=RED, lw=2.2, ms=16)
num(ax, 6.7, 5.4, 3)
ax.plot([5.2, 11.2], [4.2, 4.2], color=RED, lw=2.4)
arrow(ax, (8.0, 4.2), (10.0, 4.2), color=RED, lw=2.2, ms=16)
num(ax, 9.0, 4.85, 4)
label(ax, 9.0, 3.55, "명령", color=RED, fs=10)
hand(ax, 11.4, 3.4, w=3.4, h=1.4)
ax.add_patch(Ellipse((13.1, 4.1), 2.4, 0.8, fc=MUSCLE, ec=INK, lw=1.2))
label(ax, 13.1, 2.7, "팔 근육")
save(fig, "b11-path.svg")

# 2. 손의 알림과 명령은 등뼈 속 척수를 지나요
fig, ax = canvas(10.0, 6.0, 16.0, 9.6)
brain(ax, 4.0, 8.2, w=3.4, h=2.0)
spine(ax, 4.0, 7.2, 1.2)
label(ax, 2.6, 4.2, "척수", color=NERVE, ha="right")
label(ax, 2.6, 3.4, "등뼈", color=INK, ha="right", bold=False)
ax.plot([2.7, 3.45], [3.4, 3.4], color=GREY, lw=1)
hand(ax, 12.6, 3.4, w=1.6, h=1.8)
label(ax, 13.4, 2.6, "손")
two_lines(ax, 4.0, 12.6, 4.6, 3.8)
label(ax, 8.3, 5.2, "알림", color=IN_C, fs=10)
label(ax, 8.3, 3.2, "명령", color=RED, fs=10)
arrow(ax, (4.75, 5.6), (4.75, 7.0), color=IN_C, lw=2, ms=14)
arrow(ax, (3.25, 7.0), (3.25, 5.6), color=RED, lw=2, ms=14)
save(fig, "b11-loop.svg")

# 3. 뇌를 옆에서 본 모습: 명령 띠, 보는 곳, 균형
fig, ax = canvas(10.0, 4.6, 16.0, 7.4)
ax.add_patch(Ellipse((7.0, 4.2), 9.0, 5.6, fc=NOTE, ec=INK, lw=1.8))
ax.add_patch(Ellipse((9.6, 1.9), 2.6, 1.4, fc="#f1e6c8", ec=INK, lw=1.4))
ax.add_patch(Polygon([(6.0, 7.0), (6.6, 7.0), (5.6, 3.4), (5.0, 3.4)], closed=True, fc="#f6c9bd", ec=RED, lw=1.4))
ax.add_patch(Ellipse((10.4, 4.4), 2.4, 1.6, fc="#dde7f1", ec=IN_C, lw=1.2))
label(ax, 2.0, 5.9, "명령 띠", color=RED)
ax.plot([2.9, 5.5], [5.9, 5.4], color=RED, lw=1.2)
label(ax, 10.4, 4.4, "보는 곳", color="#4a6f96", fs=10)
label(ax, 9.6, 1.9, "균형", fs=10)
label(ax, 1.3, 3.0, "이마", bold=False)
label(ax, 12.9, 3.0, "뒤통수", bold=False)
save(fig, "b11-parts.svg")

# 4. 날아오는 공을 보며 손 방향을 고쳐요
fig, ax = canvas(10.0, 5.2, 16.0, 8.4)
balls = [(14.0, 7.2), (11.4, 6.6), (8.8, 5.4)]
for k, (x, y) in enumerate(balls):
    ax.add_patch(Circle((x, y), 0.42, fc=YEL, ec=INK, lw=1.3, alpha=0.35 if k < 2 else 1.0))
    label(ax, x, y + 0.75, f"공 {k + 1}", fs=10, bold=k == 2)
ax.plot([14.0, 11.4, 8.8], [7.2, 6.6, 5.4], color=GREY, lw=1.2, ls=":")
hands = [(2.0, 1.4), (4.6, 2.6), (6.8, 4.0), (8.4, 5.1)]
ax.plot([2.0, 9.2], [1.4, 1.4 + (9.2 - 2.0) * (2.6 - 1.4) / (4.6 - 2.0)], color=GREY, lw=1.2, ls="--")
label(ax, 9.6, 4.9, "처음 방향", color="#888", fs=9, ha="left", bold=False)
for k in range(3):
    arrow(ax, hands[k], hands[k + 1], color=RED if k == 2 else INK, lw=2.2, ms=16)
for k, (x, y) in enumerate(hands):
    ax.add_patch(Circle((x, y), 0.32, fc=SKIN, ec=INK, lw=1.2))
    if k:
        label(ax, x - 0.2, y - 0.65, f"손 {k}", fs=10, bold=k == 3)
label(ax, 2.0, 0.7, "손", fs=10)
label(ax, 7.7, 5.9, "탁", color=RED, fs=13)
save(fig, "b11-correct.svg")

# 5. 뜨거운 냄비: 척수에서 바로 돌려보내요
fig, ax = canvas(11.0, 5.0, 18.0, 8.2)
brain(ax, 4.0, 7.0, w=3.0, h=1.6)
ax.plot([4.0, 4.0], [6.2, 1.0], color=NERVE, lw=4)
label(ax, 3.0, 2.0, "척수", color=NERVE)
ax.add_patch(Rectangle((13.2, 1.2), 3.0, 1.4, fc=GREY, ec=INK, lw=1.4))
label(ax, 14.7, 0.7, "냄비", fs=10)
for k in range(3):
    ax.plot([13.8 + k * 0.9, 14.0 + k * 0.9, 13.8 + k * 0.9], [2.8, 3.3, 3.8], color=RED, lw=1.6)
hand(ax, 11.4, 3.6, w=1.4, h=1.2)
label(ax, 12.1, 5.4, "앗!", color=RED, fs=12)
two_lines(ax, 4.0, 11.4, 4.6, 3.8)
ax.add_patch(Circle((4.0, 4.2), 0.32, fc=YEL, ec=INK, lw=1.2))
ax.plot([4.45, 4.45], [4.9, 6.1], color=GREY, lw=1.4, ls="--")
label(ax, 4.8, 5.6, "뇌로도", color="#888", fs=10, ha="left", bold=False)
arrow(ax, (12.1, 5.8), (12.1, 7.2), color=RED, lw=1.8, ms=12)
save(fig, "b11-reflex.svg")


# 6. 두 길 나란히: 공 잡기(뇌까지) / 냄비(척수에서)
def path_panel(ax, ox, long):
    brain(ax, ox + 2.0, 7.6, w=2.8, h=1.5)
    ax.plot([ox + 2.0, ox + 2.0], [6.85, 1.2], color=NERVE, lw=4)
    hand(ax, ox + 5.6, 3.5, w=1.2, h=1.0)
    ax.plot([ox + 2.0, ox + 5.6], [4.4, 4.4], color=IN_C, lw=2.2)
    if long:
        ax.plot([ox + 2.35, ox + 2.35], [4.4, 6.9], color=IN_C, lw=2.2)
        ax.plot([ox + 1.65, ox + 1.65], [6.9, 3.8], color=RED, lw=2.6)
        ax.plot([ox + 1.65, ox + 5.6], [3.8, 3.8], color=RED, lw=2.6)
        arrow(ax, (ox + 2.35, 5.4), (ox + 2.35, 6.4), color=IN_C, lw=2, ms=12)
        arrow(ax, (ox + 1.65, 6.4), (ox + 1.65, 5.4), color=RED, lw=2, ms=12)
    else:
        ax.plot([ox + 2.0, ox + 5.6], [3.8, 3.8], color=RED, lw=2.6)
        ax.add_patch(Circle((ox + 2.0, 4.1), 0.3, fc=YEL, ec=INK, lw=1.2))
        ax.plot([ox + 2.35, ox + 2.35], [4.6, 6.8], color=GREY, lw=1.4, ls="--")
    arrow(ax, (ox + 4.4, 4.4), (ox + 3.4, 4.4), color=IN_C, lw=2, ms=12)
    arrow(ax, (ox + 3.4, 3.8), (ox + 4.4, 3.8), color=RED, lw=2, ms=12)
    label(ax, ox + 3.6, 9.0, "공 잡기" if long else "냄비", fs=13)
    label(ax, ox + 3.6, 0.5, "뇌에서 명령" if long else "척수에서 명령", color=RED, fs=11)


fig, ax = canvas(11.0, 5.6, 17.0, 9.6)
path_panel(ax, 0.3, True)
ax.plot([8.5, 8.5], [0.4, 9.2], color=GREY, lw=1)
path_panel(ax, 9.3, False)
save(fig, "b11-compare.svg")

# 7. 무릎 반사: 늘어난 허벅지 근육이 척수의 명령으로 다시 당겨요
fig, ax = canvas(10.0, 5.6, 16.0, 9.0)
ax.plot([1.2, 1.2], [8.6, 0.6], color=NERVE, lw=4)
label(ax, 0.6, 8.2, "척수", color=NERVE, ha="left")
ax.add_patch(Rectangle((2.6, 2.6), 5.6, 0.5, fc=GREY, ec=INK, lw=1.2))
ax.plot([3.0, 8.6], [3.6, 3.6], color=SKIN, lw=22, solid_capstyle="round")
ax.add_patch(Ellipse((5.6, 4.0), 4.2, 0.7, fc=MUSCLE, ec=RED, lw=1.6))
label(ax, 5.6, 4.95, "허벅지 근육", color=RED, fs=10)
ax.plot([8.6, 11.0], [3.6, 1.3], color=SKIN, lw=18, solid_capstyle="round", alpha=0.45)
ax.plot([8.6, 8.6], [3.6, 0.6], color=SKIN, lw=18, solid_capstyle="round")
arrow(ax, (9.0, 0.7), (11.1, 1.0), color=RED, lw=2, rad=0.35, ms=16)
ax.add_patch(FancyBboxPatch((9.1, 2.65), 1.0, 0.35, boxstyle="round,pad=0.06", fc="white", ec=INK, lw=1.2))
label(ax, 10.5, 2.85, "톡", color=INK, fs=12, ha="left")
ax.plot([4.6, 4.6, 1.2], [4.3, 7.0, 7.0], color=IN_C, lw=2.2)
ax.plot([6.6, 6.6, 1.2], [4.3, 6.2, 6.2], color=RED, lw=2.4)
arrow(ax, (3.4, 7.0), (2.2, 7.0), color=IN_C, lw=2, ms=13)
arrow(ax, (2.2, 6.2), (3.4, 6.2), color=RED, lw=2, ms=13)
ax.add_patch(Circle((1.2, 6.6), 0.3, fc=YEL, ec=INK, lw=1.2))
label(ax, 4.0, 7.5, "늘어남", color=IN_C, fs=10)
label(ax, 7.2, 5.6, "당김", color=RED, fs=10)
save(fig, "b11-knee.svg")

# 8. 해 보기: 자 떨어뜨려 잡기
fig, ax = canvas(10.0, 4.4, 16.0, 7.0)
ax.add_patch(Rectangle((7.4, 1.6), 0.8, 5.0, fc="#fff8e1", ec=INK, lw=1.4))
for k in range(11):
    ax.plot([7.4, 7.4 + (0.4 if k % 5 == 0 else 0.22)], [1.8 + k * 0.45, 1.8 + k * 0.45], color=INK, lw=1)
label(ax, 7.8, 1.3, "0", fs=9, bold=False)
ax.add_patch(FancyBboxPatch((7.0, 6.3), 1.6, 0.9, boxstyle="round,pad=0.15", fc=SKIN, ec=INK, lw=1.2))
label(ax, 9.4, 6.8, "놓기", ha="left")
ax.plot([6.6, 7.3], [1.9, 1.9], color=INK, lw=3)
ax.plot([8.3, 9.0], [1.9, 1.9], color=INK, lw=3)
label(ax, 9.4, 1.9, "잡기", ha="left")
arrow(ax, (6.2, 5.2), (6.2, 3.0), color=RED, lw=1.8)
label(ax, 5.8, 4.1, "툭", color=RED, fs=12, ha="right")
ax.set_ylim(0.6, 7.8)
save(fig, "b11-ruler.svg")
