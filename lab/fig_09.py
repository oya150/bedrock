"""알고리즘 9편 그림 만들기. 실행: python lab/fig_09.py  → docs/algorithms/img/09/*.svg

글자는 SVG 안에 글자로 남긴다(글꼴 모양을 파일에 넣지 않는다). 보는 쪽 글꼴로 그려진다.
카드는 차분한 색으로, 강조(새로 받은 카드, 비교 화살표, 많이 든 일)만 빨강으로 칠한다.
"""
import itertools
import os

import matplotlib

matplotlib.use("svg")
import matplotlib.pyplot as plt
from matplotlib.patches import Arc, Circle, FancyArrowPatch, FancyBboxPatch, Rectangle

OUT = os.path.join(os.path.dirname(__file__), "..", "docs", "algorithms", "img", "09")
os.makedirs(OUT, exist_ok=True)

plt.rcParams.update({
    "font.family": ["Apple SD Gothic Neo", "Noto Sans KR", "Malgun Gothic", "sans-serif"],
    "svg.fonttype": "none",
    "text.color": "#222",
    "figure.facecolor": "white",
    "savefig.facecolor": "white",
})

RED, GREY, INK, PAPER, NOTE, YEL = "#e4572e", "#c9ccd1", "#555", "#f4f6f8", "#fffdf5", "#f6c445"
BLUE, GREEN = "#7da2c8", "#8fb58f"
LIGHT = "#e9ecef"


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), bbox_inches="tight", pad_inches=0.25)
    plt.close(fig)


def canvas(w, h, xmax, ymax):
    fig, ax = plt.subplots(figsize=(w, h))
    ax.set_xlim(0, xmax); ax.set_ylim(0, ymax); ax.axis("off")
    return fig, ax


def box(ax, x, y, w, h, fc="white", ec=INK, lw=1.8):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.08", fc=fc, ec=ec, lw=lw))


def arrow(ax, a, b, color=INK, lw=2, rad=0.0, ms=18):
    ax.add_patch(FancyArrowPatch(a, b, arrowstyle="-|>", mutation_scale=ms, color=color, lw=lw,
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


def card(ax, x, y, w, h, num, hot=False, gone=False, fs=12):
    fc = LIGHT if gone else ("#fbe3dc" if hot else NOTE)
    ax.add_patch(Rectangle((x, y), w, h, fc=fc, ec=RED if hot else (GREY if gone else INK), lw=2.2 if hot else 1.2))
    ax.text(x + w / 2, y + h / 2, str(num), ha="center", va="center", fontsize=fs,
            color=RED if hot else (GREY if gone else "#222"), fontweight="bold")


def stones(ax, x, y, n, color=INK, r=0.13, gap=0.34):
    for k in range(n):
        ax.add_patch(Circle((x + k * gap, y), r, fc=color, ec=color))


def row(ax, x, y, nums, cw=0.9, ch=1.1, gap=0.1, hot=(), fs=12, gone=()):
    for k, n in enumerate(nums):
        card(ax, x + k * (cw + gap), y, cw, ch, n, hot=(k in hot), gone=(k in gone), fs=fs)
    return x + len(nums) * (cw + gap) - gap


def locker(ax, x, y, num, name=None, w=1.3, h=1.8, hot=False, open_=False, fs=11):
    fc = "#fbe3dc" if hot else (NOTE if name else ("white" if open_ else LIGHT))
    ax.add_patch(Rectangle((x, y), w, h, fc=fc, ec=RED if hot else INK, lw=2.2 if hot else 1.4))
    ax.text(x + w / 2, y + h + 0.3, f"{num}번", ha="center", va="center", fontsize=9, color=INK)
    if name:
        ax.text(x + w / 2, y + h / 2, name, ha="center", va="center", fontsize=fs, color=RED if hot else "#222",
                fontweight="bold")
    elif not open_:
        ax.add_patch(Circle((x + w - 0.25, y + h / 2), 0.07, fc=INK))


def lockers(ax, x, y, names, w=1.3, h=1.8, gap=0.15, hot=(), fs=11, closed=False):
    for k, nm in enumerate(names):
        locker(ax, x + k * (w + gap), y, k, None if closed else nm, w=w, h=h, hot=(k in hot), open_=not closed, fs=fs)


SOUNDS = "ㄱㄴㄷㄹㅁㅂㅅㅇㅈㅊㅋㅌㅍㅎ"

# 1. 여는 장면: 이름표 없는 사물함 8칸
fig, ax = canvas(11.0, 4.6, 18.0, 7.6)
kid(ax, 1.3, 0.6, 1.4)
lockers(ax, 3.4, 1.4, [None] * 8, closed=True)
ax.text(1.3, 0.1, "나", ha="center", va="center", fontsize=12, fontweight="bold")
ax.text(9.4, 5.6, "하준이 공책은 몇 번 칸에 있지?", ha="center", va="center", fontsize=13,
        bbox=dict(boxstyle="round,pad=0.4", fc="white", ec=INK, lw=1.2))
ax.text(16.6, 2.4, "?", ha="center", va="center", fontsize=34, color=RED, fontweight="bold")
save(fig, "a09-lockers.svg")

# 2. 이 편의 지도
fig, ax = canvas(13.6, 2.9, 24.2, 4.6)
titles = ["이름을 칸 번호로", "바로 찾기", "칸이 겹치면", "한 칸에 몰리면", "꽉 차기 전에 늘리기"]
for i, t in enumerate(titles):
    x = 0.3 + i * 4.8
    box(ax, x, 0.4, 3.8, 3.6)
    ax.text(x + 1.9, 0.95, t, ha="center", va="center", fontsize=12, fontweight="bold")
    if i == 0:
        ax.text(x + 1.0, 2.7, "하준", ha="center", va="center", fontsize=11)
        arrow(ax, (x + 1.6, 2.7), (x + 2.4, 2.7), color=RED, lw=1.4, ms=10)
        ax.text(x + 2.9, 2.7, "5", ha="center", va="center", fontsize=13, color=RED, fontweight="bold")
    elif i == 1:
        for k in range(6):
            ax.add_patch(Rectangle((x + 0.4 + k * 0.5, 2.1), 0.4, 1.2, fc=NOTE if k != 3 else "#fbe3dc",
                                   ec=RED if k == 3 else INK, lw=1.4 if k == 3 else 0.9))
    elif i == 2:
        for k in range(4):
            ax.add_patch(Rectangle((x + 0.6 + k * 0.65, 2.1), 0.55, 1.2, fc=NOTE, ec=INK, lw=0.9))
        arrow(ax, (x + 1.6, 3.6), (x + 2.3, 3.6), color=RED, lw=1.3, ms=9, rad=-0.6)
    elif i == 3:
        for k in range(6):
            ax.add_patch(Rectangle((x + 0.4 + k * 0.5, 2.1), 0.4, 1.2, fc=NOTE if k < 5 else "white", ec=INK, lw=0.9))
    else:
        for k in range(4):
            ax.add_patch(Rectangle((x + 0.4 + k * 0.4, 2.8), 0.32, 0.6, fc=NOTE, ec=INK, lw=0.8))
        for k in range(8):
            ax.add_patch(Rectangle((x + 0.4 + k * 0.38, 1.7), 0.3, 0.6, fc="white", ec=INK, lw=0.8))
    if i < 4:
        arrow(ax, (x + 3.95, 2.2), (x + 4.65, 2.2))
save(fig, "a09-map.svg")

# 3. 규칙 표와 넣기
fig, ax = canvas(12.0, 6.6, 19.6, 10.8)
ax.text(0.3, 10.2, "첫소리 번호", ha="left", va="center", fontsize=12, fontweight="bold")
for k, c in enumerate(SOUNDS):
    x = 0.3 + k * 1.37
    ax.add_patch(Rectangle((x, 8.4), 1.25, 1.3, fc=NOTE, ec=INK, lw=1.0))
    ax.text(x + 0.62, 9.3, c, ha="center", va="center", fontsize=13, fontweight="bold")
    ax.text(x + 0.62, 8.75, str(k), ha="center", va="center", fontsize=11, color=BLUE, fontweight="bold")
ax.text(0.3, 7.6, "사물함은 0번부터 7번까지 8칸. 번호가 8보다 크거나 같으면 8을 빼요.", ha="left", va="center",
        fontsize=11, color=RED, fontweight="bold")
rows = [("민준", "ㅁ 4", "4번"), ("서연", "ㅅ 6", "6번"), ("하준", "ㅎ 13", "13 - 8 = 5번"), ("지우", "ㅈ 8", "8 - 8 = 0번")]
for r, (nm, s_, to) in enumerate(rows):
    y = 6.6 - r * 0.75
    ax.text(0.6, y, nm, ha="left", va="center", fontsize=11, fontweight="bold")
    ax.text(2.3, y, s_, ha="left", va="center", fontsize=11)
    ax.text(4.0, y, "→  " + to, ha="left", va="center", fontsize=11, color=RED, fontweight="bold")
lockers(ax, 0.5, 0.4, ["지우", None, None, None, "민준", "하준", "서연", None], w=1.9, h=1.9, gap=0.4, hot=(5,), fs=12)
ax.text(13.3, 5.4, "하준을 찾을 때도 같은 규칙:\nㅎ 13 → 5번 칸을 바로 열어요", ha="left", va="center", fontsize=11,
        color=RED, fontweight="bold")
save(fig, "a09-rule.svg")

# 4. 칸이 겹치면: 서준 → 6번은 서연, 다음 칸 7번
fig, ax = canvas(12.0, 4.4, 19.6, 7.2)
ax.set_ylim(-1.5, 7.2)
lockers(ax, 0.5, 1.4, ["지우", None, None, None, "민준", "하준", "서연", "서준"], w=1.9, h=1.9, gap=0.4, hot=(7,), fs=12)
ax.text(0.5, 6.3, "서준: ㅅ 6 → 6번 칸에는 서연이 있어요 → 다음 칸 7번에 넣어요", ha="left", va="center",
        fontsize=12, fontweight="bold")
x6 = 0.5 + 6 * 2.3 + 0.95
x7 = 0.5 + 7 * 2.3 + 0.95
arrow(ax, (x6, 3.9), (x7, 3.9), color=RED, lw=1.8, ms=14, rad=-0.6)
ax.add_patch(FancyArrowPatch((0.5 + 7 * 2.3 + 0.95, 1.3), (0.5 + 0.95, 1.3), arrowstyle="-|>", mutation_scale=12,
                             color=INK, lw=1.2, ls="--", connectionstyle="arc3,rad=-0.12"))
ax.text(9.8, -0.25, "7번 다음은 다시 0번", ha="center", va="center", fontsize=10, color=INK)
ax.text(9.8, -1.0, "서준을 찾을 때: 6번 열어 보고(서연) → 7번 열어 보기(서준). 2칸", ha="center", va="center",
        fontsize=11, color=RED, fontweight="bold")
save(fig, "a09-collide.svg")

# 5. 한 칸에 몰리면: 모두 ㄱ
fig, ax = canvas(12.0, 4.4, 19.6, 7.2)
lockers(ax, 0.5, 1.4, ["가온", "건우", "고은", "규리", "기현", None, None, None], w=1.9, h=1.9, gap=0.4, hot=(4,), fs=12)
ax.text(0.5, 6.3, "가온, 건우, 고은, 규리, 기현: 모두 ㄱ 0 → 0번부터 한 칸씩 밀려요", ha="left", va="center",
        fontsize=12, fontweight="bold")
for k in range(4):
    a = 0.5 + k * 2.3 + 0.95
    arrow(ax, (a, 3.9), (a + 2.3, 3.9), color=RED, lw=1.4, ms=11, rad=-0.6)
ax.text(9.8, 0.6, "기현을 찾을 때: 0번부터 4번까지 5칸을 열어 봐야 해요", ha="center", va="center", fontsize=11,
        color=RED, fontweight="bold")
save(fig, "a09-crowd.svg")

# 6. 꽉 차기 전에 늘려요: 8칸 → 16칸
fig, ax = canvas(12.0, 6.6, 19.6, 10.8)
ax.text(0.3, 10.3, "8칸에 다섯 명. 여섯째 도윤이 오면", ha="left", va="center", fontsize=12, fontweight="bold")
lockers(ax, 0.5, 7.2, ["지우", None, None, None, "민준", "하준", "서연", "서준"], w=1.9, h=1.9, gap=0.4, fs=12)
arrow(ax, (9.8, 6.8), (9.8, 5.6), color=RED, lw=2.0)
ax.text(10.2, 6.2, "16칸으로 바꾸고 모두 다시 넣어요 (16보다 크거나 같으면 16을 빼요)", ha="left", va="center",
        fontsize=11, color=RED, fontweight="bold")
big = [None, None, "도윤", None, "민준", None, "서연", "서준", "지우", None, None, None, None, "하준", None, None]
lockers(ax, 0.3, 2.2, big, w=1.05, h=2.0, gap=0.15, hot=(2,), fs=10)
ax.text(9.8, 0.8, "빈 칸이 넉넉해서 겹치는 일이 줄어요", ha="center", va="center", fontsize=12)
save(fig, "a09-grow.svg")
