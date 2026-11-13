"""알고리즘 10편 그림 만들기. 실행: python lab/fig_10.py  → docs/algorithms/img/10/*.svg

글자는 SVG 안에 글자로 남긴다(글꼴 모양을 파일에 넣지 않는다). 보는 쪽 글꼴로 그려진다.
그림 안 글씨는 낱말과 숫자만 둔다. 강조(지금 움직이는 카드, 볼 곳)만 빨강으로 칠한다.
FIG_FMT=png FIG_OUT=폴더 로 확인용 PNG 사본을 만든다.
"""
import os

import matplotlib

matplotlib.use("svg")
import matplotlib.pyplot as plt
from matplotlib.patches import Arc, Circle, FancyArrowPatch, Rectangle

OUT = os.path.join(os.path.dirname(__file__), "..", "docs", "algorithms", "img", "10")

plt.rcParams.update({
    "font.family": ["Apple SD Gothic Neo", "Noto Sans KR", "Malgun Gothic", "sans-serif"],
    "svg.fonttype": "none",
    "text.color": "#222",
    "figure.facecolor": "white",
    "savefig.facecolor": "white",
})

RED, GREY, INK, NOTE, LIGHT = "#e4572e", "#c9ccd1", "#555", "#fffdf5", "#e9ecef"


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


def row(ax, x, y, nums, cw=0.9, ch=1.1, gap=0.1, hot=(), fs=12):
    for k, n in enumerate(nums):
        card(ax, x + k * (cw + gap), y, cw, ch, n, hot=(k in hot), fs=fs)


# 힙 나무: 배열 자리 k의 아래 두 자리는 2k+1, 2k+2
POS = {0: (8.0, 8.4), 1: (4.0, 6.0), 2: (12.0, 6.0), 3: (2.0, 3.6), 4: (6.0, 3.6), 5: (10.0, 3.6), 6: (14.0, 3.6),
       7: (1.0, 1.2), 8: (3.0, 1.2)}


def tree(ax, a, dx=0.0, dy=0.0, s=1.0, hot=(), fs=14, pos=POS):
    for k in range(len(a)):
        for c in (2 * k + 1, 2 * k + 2):
            if c < len(a):
                (x1, y1), (x2, y2) = pos[k], pos[c]
                ax.plot([dx + x1 * s, dx + x2 * s], [dy + y1 * s, dy + y2 * s], color=GREY, lw=1.6, zorder=0)
    w, h = 1.3 * s, 1.5 * s
    for k, v in enumerate(a):
        x, y = pos[k]
        card(ax, dx + x * s - w / 2, dy + y * s - h / 2, w, h, v, hot=(k in hot), fs=fs)


# 1. 여는 장면: 숙제 카드, 숫자는 남은 날
fig, ax = canvas(11.0, 4.6, 18.0, 7.6)
kid(ax, 1.4, 0.6, 1.4)
ax.text(1.4, 0.1, "나", ha="center", va="center", fontsize=12, fontweight="bold")
cards = [(5, "그림"), (3, "받아쓰기"), (8, "독서록"), (1, "준비물"), (9, "만들기"), (4, "줄넘기"), (7, "일기")]
for k, (d, t) in enumerate(cards):
    x = 3.6 + k * 1.95
    card(ax, x, 2.0, 1.6, 2.0, d, fs=18)
    ax.text(x + 0.8, 1.6, t, ha="center", va="center", fontsize=10)
ax.text(10.2, 0.9, "숫자 = 남은 날", ha="center", va="center", fontsize=11)
ax.text(10.2, 5.8, "제일 급한 숙제?", ha="center", va="center", fontsize=13,
        bbox=dict(boxstyle="round,pad=0.4", fc="white", ec=INK, lw=1.2))
ax.text(17.4, 3.0, "?", ha="center", va="center", fontsize=30, color=RED, fontweight="bold")
save(fig, "a10-todo.svg")

# 2. 쉬운 두 방법: 아무렇게나 두기 / 늘 정렬해 두기
fig, ax = canvas(13.0, 4.4, 24.0, 8.0)
ax.text(0.3, 7.4, "아무렇게나", ha="left", va="center", fontsize=13, fontweight="bold")
row(ax, 0.3, 4.2, [5, 3, 8, 1, 9, 4, 7], cw=1.2, ch=1.4, gap=0.25, hot=(3,), fs=14)
ax.text(5.3, 2.7, "꺼내기: 비교 6번", ha="center", va="center", fontsize=12, color=RED, fontweight="bold")
ax.text(5.3, 1.7, "넣기: 맨 끝에", ha="center", va="center", fontsize=12)
ax.plot([11.6, 11.6], [0.8, 7.6], color=GREY, lw=1.2)
ax.text(12.6, 7.4, "늘 정렬", ha="left", va="center", fontsize=13, fontweight="bold")
row(ax, 12.6, 4.2, [1, 3, 4, 5, 7, 8, 9], cw=1.2, ch=1.4, gap=0.25, fs=14)
card(ax, 17.65, 6.2, 1.2, 1.2, 6, hot=True, fs=14)
arrow(ax, (18.25, 6.15), (18.25, 5.7), color=RED, lw=2.0, ms=14)
ax.text(17.9, 2.7, "넣기: 자리 찾아 끼우기", ha="center", va="center", fontsize=12, color=RED, fontweight="bold")
ax.text(17.9, 1.7, "꺼내기: 맨 앞", ha="center", va="center", fontsize=12)
save(fig, "a10-twoways.svg")

# 3. 대진표 모양: 위 카드는 아래 두 카드보다 작아요
fig, ax = canvas(10.4, 5.6, 16.0, 9.8)
tree(ax, [1, 3, 4, 5, 9, 8, 7], dy=-0.8, hot=(0,))
ax.text(10.2, 7.6, "제일 작음", ha="left", va="center", fontsize=12, color=RED, fontweight="bold")
arrow(ax, (10.1, 7.6), (9.0, 7.6), color=RED, lw=1.6, ms=13)
ax.text(2.0, 1.2, "5, 9 > 3", ha="center", va="center", fontsize=11, color=INK)
ax.text(14.0, 1.2, "8, 7 > 4", ha="center", va="center", fontsize=11, color=INK)
save(fig, "a10-heap.svg")

# 4. 넣으면 올라가기: 2를 넣기
fig, ax = canvas(13.6, 3.9, 27.0, 7.4)
stages = [([1, 3, 4, 5, 9, 8, 7, 2], (7,), "① 빈자리에 2"),
          ([1, 3, 4, 2, 9, 8, 7, 5], (3,), "② 2 < 5, 바꾸기"),
          ([1, 2, 4, 3, 9, 8, 7, 5], (1,), "③ 2 < 3, 바꾸기")]
for k, (a, hot, cap) in enumerate(stages):
    tree(ax, a, dx=0.3 + k * 9.0, dy=1.2, s=0.52, hot=hot, fs=10)
    ax.text(4.5 + k * 9.0, 0.6, cap, ha="center", va="center", fontsize=12, fontweight="bold")
    if k < 2:
        arrow(ax, (8.6 + k * 9.0, 4.0), (9.3 + k * 9.0, 4.0))
ax.text(22.5, 6.7, "2 > 1, 멈춤", ha="center", va="center", fontsize=12, color=RED, fontweight="bold")
save(fig, "a10-push.svg")

# 5. 꺼내면 내려가기: 맨 위 1을 꺼내기
fig, ax = canvas(13.6, 3.9, 27.0, 7.4)
stages = [([5, 2, 4, 3, 9, 8, 7], (0,), "① 1 꺼내고 5를 위로"),
          ([2, 5, 4, 3, 9, 8, 7], (1,), "② 2 < 4, 2 < 5, 바꾸기"),
          ([2, 3, 4, 5, 9, 8, 7], (3,), "③ 3 < 9, 3 < 5, 바꾸기")]
for k, (a, hot, cap) in enumerate(stages):
    tree(ax, a, dx=0.3 + k * 9.0, dy=1.2, s=0.52, hot=hot, fs=10)
    ax.text(4.5 + k * 9.0, 0.6, cap, ha="center", va="center", fontsize=12, fontweight="bold")
    if k < 2:
        arrow(ax, (8.6 + k * 9.0, 4.0), (9.3 + k * 9.0, 4.0))
ax.text(22.5, 6.7, "아래 없음, 멈춤", ha="center", va="center", fontsize=12, color=RED, fontweight="bold")
save(fig, "a10-pop.svg")

# 6. 카드 1,000장이면: 막대 (실제 비율)
fig, ax = canvas(10.4, 5.6, 17.0, 9.2)
base, scale = 1.4, 6.6 / 999
for k, (name, v, col) in enumerate([("다 뒤지기", 999, GREY), ("힙에서 꺼내기", 18, RED), ("힙에 넣기", 9, RED)]):
    bx = 2.0 + k * 4.6
    h = max(v * scale, 0.08)
    ax.add_patch(Rectangle((bx, base), 2.2, h, fc=col, ec=INK, lw=1.2))
    ax.text(bx + 1.1, base + h + 0.15, f"{v}번", ha="center", va="bottom", fontsize=13, fontweight="bold",
            color=RED if col == RED else "#222")
    ax.text(bx + 1.1, base - 0.3, name, ha="center", va="top", fontsize=12, fontweight="bold",
            color=RED if col == RED else "#222")
ax.plot([1.0, 16.0], [base, base], color=INK, lw=1.4)
ax.text(8.5, 0.2, "카드 1,000장, 비교 수(많아야)", ha="center", va="center", fontsize=11)
save(fig, "a10-bars.svg")

# 7. 대진표를 한 줄로: 자리 k 아래 두 카드는 2k+1, 2k+2
fig, ax = canvas(12.0, 4.2, 19.0, 6.6, ymin=-0.4)
vals = [1, 3, 4, 5, 9, 8, 7]
cw, gap, x0, y0 = 2.0, 0.5, 0.6, 2.4
mids = [x0 + k * (cw + gap) + cw / 2 for k in range(7)]
for k, v in enumerate(vals):
    hot = k in (1, 3, 4)
    card(ax, x0 + k * (cw + gap), y0, cw, 1.6, v, hot=hot, fs=16)
    ax.text(mids[k], y0 + 1.95, f"{k}번", ha="center", va="center", fontsize=11, color=RED if hot else INK,
            fontweight="bold" if hot else "normal")
for p, cs in [(0, (1, 2)), (2, (5, 6))]:
    for c in cs:
        arrow(ax, (mids[p], y0 - 0.1), (mids[c], y0 - 0.1), color=GREY, lw=1.2, ms=11, rad=0.35)
for c in (3, 4):
    arrow(ax, (mids[1], y0 + 2.3), (mids[c], y0 + 2.3), color=RED, lw=1.8, ms=13, rad=-0.35)
ax.text(mids[0] - 0.6, y0 + 3.9, "1번 → 3번, 4번", ha="left", va="center", fontsize=12, color=RED, fontweight="bold")
save(fig, "a10-array.svg")
