"""알고리즘 9편 그림 만들기. 실행: python lab/fig_09.py  → docs/algorithms/img/09/*.svg

글자는 SVG 안에 글자로 남긴다(글꼴 모양을 파일에 넣지 않는다). 보는 쪽 글꼴로 그려진다.
그림 안 글씨는 낱말과 숫자만 둔다. 강조(지금 볼 칸)만 빨강으로 칠한다.
FIG_FMT=png FIG_OUT=폴더 로 확인용 PNG 사본을 만든다.
"""
import os

import matplotlib

matplotlib.use("svg")
import matplotlib.pyplot as plt
from matplotlib.patches import Arc, Circle, FancyArrowPatch, Rectangle

OUT = os.path.join(os.path.dirname(__file__), "..", "docs", "algorithms", "img", "09")

plt.rcParams.update({
    "font.family": ["Apple SD Gothic Neo", "Noto Sans KR", "Malgun Gothic", "sans-serif"],
    "svg.fonttype": "none",
    "text.color": "#222",
    "figure.facecolor": "white",
    "savefig.facecolor": "white",
})

RED, INK, NOTE, LIGHT, PINK = "#e4572e", "#555", "#fffdf5", "#e9ecef", "#fbe3dc"
BLUE = "#7da2c8"


def save(fig, name):
    fmt = os.environ.get("FIG_FMT", "svg")
    out = os.environ.get("FIG_OUT", OUT)
    os.makedirs(out, exist_ok=True)
    if fmt != "svg":
        name = name.rsplit(".", 1)[0] + "." + fmt
    fig.savefig(os.path.join(out, name), bbox_inches="tight", pad_inches=0.25, dpi=110)
    plt.close(fig)


def canvas(w, h, xmax, ymax, ymin=0):
    fig, ax = plt.subplots(figsize=(w, h))
    ax.set_xlim(0, xmax); ax.set_ylim(ymin, ymax); ax.axis("off")
    return fig, ax


def arrow(ax, a, b, color=INK, lw=2, rad=0.0, ms=18, ls="-"):
    ax.add_patch(FancyArrowPatch(a, b, arrowstyle="-|>", mutation_scale=ms, color=color, lw=lw, ls=ls,
                                 connectionstyle=f"arc3,rad={rad}"))


def kid(ax, cx, y, s=1.0):
    ax.add_patch(Circle((cx, y + 1.55 * s), 0.32 * s, fc="white", ec=INK, lw=1.6))
    ax.add_patch(Circle((cx - 0.11 * s, y + 1.6 * s), 0.035 * s, fc=INK))
    ax.add_patch(Circle((cx + 0.11 * s, y + 1.6 * s), 0.035 * s, fc=INK))
    ax.add_patch(Arc((cx, y + 1.5 * s), 0.3 * s, 0.2 * s, theta1=200, theta2=340, color=INK, lw=1.4))
    ax.plot([cx, cx], [y + 1.23 * s, y + 0.55 * s], color=INK, lw=2)
    ax.plot([cx, cx - 0.3 * s], [y + 0.55 * s, y], color=INK, lw=2)
    ax.plot([cx, cx + 0.3 * s], [y + 0.55 * s, y], color=INK, lw=2)
    ax.plot([cx - 0.35 * s, cx + 0.35 * s], [y + 1.0 * s, y + 1.0 * s], color=INK, lw=2)


def locker(ax, x, y, num, name=None, w=1.3, h=1.8, hot=False, closed=False, fs=11):
    if closed:
        fc = LIGHT
    else:
        fc = PINK if hot else (NOTE if name else "white")
    ax.add_patch(Rectangle((x, y), w, h, fc=fc, ec=RED if hot else INK, lw=2.4 if hot else 1.4))
    ax.text(x + w / 2, y + h + 0.3, f"{num}번", ha="center", va="center", fontsize=9,
            color=RED if hot else INK, fontweight="bold" if hot else "normal")
    if name:
        ax.text(x + w / 2, y + h / 2, name, ha="center", va="center", fontsize=fs, color=RED if hot else "#222",
                fontweight="bold")
    elif closed:
        ax.add_patch(Circle((x + w - 0.25, y + h / 2), 0.07, fc=INK))


def lockers(ax, x, y, names, w=1.9, h=1.9, gap=0.4, hot=(), fs=12, closed=False):
    for k, nm in enumerate(names):
        locker(ax, x + k * (w + gap), y, k, nm, w=w, h=h, hot=(k in hot), closed=closed, fs=fs)


def mid(k, x0=0.5, w=1.9, gap=0.4):
    return x0 + k * (w + gap) + w / 2


SOUNDS = "ㄱㄴㄷㄹㅁㅂㅅㅇㅈㅊㅋㅌㅍㅎ"
CLASS4 = ["지우", None, None, None, "민준", "하준", "서연", None]
CLASS5 = ["지우", None, None, None, "민준", "하준", "서연", "서준"]

# 1. 이름표 없는 사물함 8칸
fig, ax = canvas(11.0, 4.6, 18.0, 7.6)
kid(ax, 1.3, 0.6, 1.4)
lockers(ax, 3.4, 1.4, [None] * 8, w=1.3, h=1.8, gap=0.15, closed=True)
ax.text(1.3, 0.1, "나", ha="center", va="center", fontsize=12, fontweight="bold")
ax.text(9.4, 5.6, "하준 공책?", ha="center", va="center", fontsize=13,
        bbox=dict(boxstyle="round,pad=0.4", fc="white", ec=INK, lw=1.2))
ax.text(16.6, 2.4, "?", ha="center", va="center", fontsize=34, color=RED, fontweight="bold")
save(fig, "a09-lockers.svg")

# 2. 첫소리 번호 표와 하준 계산
fig, ax = canvas(12.0, 3.6, 19.6, 5.6)
for k, c in enumerate(SOUNDS):
    x = 0.3 + k * 1.37
    hot = c == "ㅎ"
    ax.add_patch(Rectangle((x, 3.4), 1.25, 1.6, fc=PINK if hot else NOTE, ec=RED if hot else INK,
                           lw=2.2 if hot else 1.0))
    ax.text(x + 0.62, 4.5, c, ha="center", va="center", fontsize=14, fontweight="bold",
            color=RED if hot else "#222")
    ax.text(x + 0.62, 3.8, str(k), ha="center", va="center", fontsize=12, fontweight="bold",
            color=RED if hot else BLUE)
ax.text(1.0, 1.6, "하준", ha="left", va="center", fontsize=14, fontweight="bold")
ax.text(3.2, 1.6, "ㅎ 13", ha="left", va="center", fontsize=14)
arrow(ax, (5.3, 1.6), (6.6, 1.6), lw=1.6, ms=14)
ax.text(7.0, 1.6, "13 − 8 = 5", ha="left", va="center", fontsize=14)
arrow(ax, (10.6, 1.6), (11.9, 1.6), lw=1.6, ms=14)
ax.text(12.3, 1.6, "5번", ha="left", va="center", fontsize=15, color=RED, fontweight="bold")
ax.text(14.4, 1.6, "(8 이상이면 − 8)", ha="left", va="center", fontsize=11, color=INK)
save(fig, "a09-sounds.svg")

# 3. 규칙대로 넣은 사물함
fig, ax = canvas(12.0, 2.9, 19.6, 4.0)
lockers(ax, 0.5, 0.4, CLASS4, hot=(5,))
for k, s in [(0, "ㅈ 8"), (4, "ㅁ 4"), (5, "ㅎ 13"), (6, "ㅅ 6")]:
    ax.text(mid(k), 0.0, s, ha="center", va="center", fontsize=10, color=RED if k == 5 else INK)
save(fig, "a09-rule.svg")

# 4. 같은 칸을 받으면: 서준 → 6번은 서연, 다음 칸 7번
fig, ax = canvas(12.0, 4.2, 19.6, 6.0, ymin=-1.6)
lockers(ax, 0.5, 0.6, CLASS5, hot=(7,))
ax.text(mid(6), 4.6, "서준 ㅅ 6", ha="center", va="center", fontsize=12, fontweight="bold")
arrow(ax, (mid(6), 4.2), (mid(6), 3.0), lw=1.6, ms=13)
arrow(ax, (mid(6) + 0.3, 3.0), (mid(7), 3.0), color=RED, lw=2.0, ms=15, rad=-0.6)
arrow(ax, (mid(7), 0.4), (mid(0), 0.4), lw=1.2, ms=12, rad=-0.08, ls="--")
ax.text(9.8, -1.3, "7번 다음은 0번", ha="center", va="center", fontsize=10, color=INK)
save(fig, "a09-collide.svg")

# 5. 없는 이름 찾기: 도윤 → 2번 칸이 비어 있음
fig, ax = canvas(12.0, 3.6, 19.6, 5.4)
lockers(ax, 0.5, 0.4, CLASS5, hot=(2,))
ax.text(mid(2), 4.6, "도윤 ㄷ 2", ha="center", va="center", fontsize=12, fontweight="bold")
arrow(ax, (mid(2), 4.2), (mid(2), 2.9), color=RED, lw=2.0, ms=15)
ax.text(mid(2), 1.35, "빈 칸", ha="center", va="center", fontsize=11, color=RED, fontweight="bold")
save(fig, "a09-missing.svg")

# 6. 한 칸에 몰리면: 모두 ㄱ
fig, ax = canvas(12.0, 3.9, 19.6, 6.0, ymin=-0.6)
lockers(ax, 0.5, 0.6, ["가온", "건우", "고은", "규리", "기현", None, None, None], hot=(4,))
ax.text(mid(0), 4.6, "모두 ㄱ 0", ha="center", va="center", fontsize=12, fontweight="bold")
arrow(ax, (mid(0), 4.2), (mid(0), 3.0), lw=1.6, ms=13)
for k in range(4):
    arrow(ax, (mid(k) + 0.3, 3.0), (mid(k + 1), 3.0), color=RED, lw=1.6, ms=12, rad=-0.6)
for k in range(5):
    ax.text(mid(k), 0.05, str(k + 1), ha="center", va="center", fontsize=11, color=RED if k == 4 else INK,
            fontweight="bold")
ax.text(mid(6), 0.05, "연 칸 수", ha="center", va="center", fontsize=10, color=INK)
save(fig, "a09-crowd.svg")

# 7. 칸을 늘리고 다시 넣기: 8칸 → 16칸
fig, ax = canvas(12.0, 6.2, 19.6, 10.0)
ax.text(0.3, 9.6, "8칸", ha="left", va="center", fontsize=13, fontweight="bold")
lockers(ax, 0.5, 6.6, CLASS5, hot=(5,))
arrow(ax, (9.8, 6.0), (9.8, 4.8), color=INK, lw=2.0)
ax.text(10.3, 5.4, "16칸으로 늘리고 다시 넣기", ha="left", va="center", fontsize=11, color=INK)
ax.text(0.3, 4.6, "16칸", ha="left", va="center", fontsize=13, fontweight="bold")
big = [None, None, "도윤", None, "민준", None, "서연", "서준", "지우", None, None, None, None, "하준", None, None]
lockers(ax, 0.3, 1.6, big, w=1.05, h=2.0, gap=0.15, hot=(13,), fs=10)
save(fig, "a09-grow.svg")
