"""알고리즘 5편 그림 만들기. 실행: python lab/fig_05.py  → docs/algorithms/img/05/*.svg

글자는 SVG 안에 글자로 남긴다(글꼴 모양을 파일에 넣지 않는다). 보는 쪽 글꼴로 그려진다.
카드는 차분한 색으로, 강조(지금 볼 곳)만 빨강으로 칠한다. 그림 안 글씨는 낱말과 숫자만 둔다.
확인용 PNG: FIG_FMT=png FIG_OUT=<폴더> python lab/fig_05.py
"""
import os

import matplotlib

matplotlib.use("svg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch, Rectangle

FMT = os.environ.get("FIG_FMT", "svg")
OUT = os.environ.get("FIG_OUT") or os.path.join(os.path.dirname(__file__), "..", "docs", "algorithms", "img", "05")
os.makedirs(OUT, exist_ok=True)

plt.rcParams.update({
    "font.family": ["Apple SD Gothic Neo", "Noto Sans KR", "Malgun Gothic", "sans-serif"],
    "svg.fonttype": "none",
    "text.color": "#222",
    "figure.facecolor": "white",
    "savefig.facecolor": "white",
})

RED, GREY, INK, NOTE = "#e4572e", "#c9ccd1", "#555", "#fffdf5"
LIGHT = "#e9ecef"


def save(fig, name):
    fig.savefig(os.path.join(OUT, f"{name}.{FMT}"), bbox_inches="tight", pad_inches=0.25, dpi=110)
    plt.close(fig)


def canvas(w, h, xmax, ymax):
    fig, ax = plt.subplots(figsize=(w, h))
    ax.set_xlim(0, xmax); ax.set_ylim(0, ymax); ax.axis("off")
    return fig, ax


def arrow(ax, a, b, color=INK, lw=2, rad=0.0, ms=18):
    ax.add_patch(FancyArrowPatch(a, b, arrowstyle="-|>", mutation_scale=ms, color=color, lw=lw,
                                 connectionstyle=f"arc3,rad={rad}"))


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


def merge_fig(name, mine, friend, compared):
    """정렬된 두 줄을 합친 결과. 비교로 놓인 카드는 빨강과 동그라미 번호, 나머지는 '그대로'."""
    fig, ax = canvas(11.6, 5.0, 19.0, 8.2)
    ax.text(0.2, 7.5, "내 줄", ha="left", va="center", fontsize=12, fontweight="bold")
    row(ax, 0.2, 5.6, mine, cw=1.2, ch=1.4, fs=14)
    ax.text(10.2, 7.5, "친구 줄", ha="left", va="center", fontsize=12, fontweight="bold")
    row(ax, 10.2, 5.6, friend, cw=1.2, ch=1.4, fs=14)
    ax.text(0.2, 2.3, "새 줄", ha="left", va="center", fontsize=12, fontweight="bold")
    merged = sorted(mine + friend)
    row(ax, 2.2, 1.6, merged, cw=1.2, ch=1.4, fs=14, hot=range(compared))
    for k in range(len(merged)):
        x = 2.2 + k * 1.3 + 0.6
        if k < compared:
            ax.text(x, 3.45, "①②③④⑤⑥⑦"[k], ha="center", va="center", fontsize=13, color=RED, fontweight="bold")
        else:
            ax.text(x, 3.45, "그대로", ha="center", va="center", fontsize=10, color=INK)
    ax.text(9.5, 0.7, f"비교 {compared}번", ha="center", va="center", fontsize=13, color=RED, fontweight="bold")
    save(fig, name)


# 1. 정렬된 두 줄 합치기: 2, 5, 7, 8 + 1, 3, 4, 6 → 비교 6번
merge_fig("a05-merge", [2, 5, 7, 8], [1, 3, 4, 6], 6)

# 2·3. 한 장이 될 때까지 나누기, 그리고 합쳐 올라오기
CW, CH, G = 1.0, 1.1, 0.12


def layer(ax, y, piles, hot=False):
    total = sum(len(p) for p in piles) * (CW + G) + (len(piles) - 1) * 0.6
    x = 2.6 + (8 * (CW + G) + 7 * 0.6 - total) / 2
    for p in piles:
        x = row(ax, x, y, p, cw=CW, ch=CH, gap=G, hot=range(len(p)) if hot else ()) + 0.6


fig, ax = canvas(11.6, 6.0, 19.0, 9.6)
split = [[[5, 2, 8, 7, 3, 6, 1, 4]], [[5, 2, 8, 7], [3, 6, 1, 4]], [[5, 2], [8, 7], [3, 6], [1, 4]],
         [[5], [2], [8], [7], [3], [6], [1], [4]]]
for lv, piles in enumerate(split):
    y = 7.6 - lv * 2.2
    layer(ax, y, piles, hot=(lv == 3))
    ax.text(1.2, y + CH / 2, "처음" if lv == 0 else f"{lv}번째", ha="center", va="center", fontsize=11,
            color=RED if lv == 3 else INK, fontweight="bold")
    if lv:
        ax.text(17.2, y + CH / 2, f"{8 // 2 ** lv}장씩", ha="left", va="center", fontsize=11,
                color=RED if lv == 3 else INK, fontweight="bold")
save(fig, "a05-split")

fig, ax = canvas(11.6, 5.6, 19.0, 9.0)
mergeup = [([[2, 5], [7, 8], [3, 6], [1, 4]], 4), ([[2, 5, 7, 8], [1, 3, 4, 6]], 5), ([[1, 2, 3, 4, 5, 6, 7, 8]], 6)]
for lv, (piles, cmp_) in enumerate(mergeup):
    y = 7.2 - lv * 2.4
    layer(ax, y, piles, hot=(lv == 2))
    ax.text(1.2, y + CH / 2, f"{lv + 1}번째", ha="center", va="center", fontsize=11, color=INK, fontweight="bold")
    stones(ax, 15.6, y + CH / 2 + 0.25, cmp_, color=RED, r=0.13, gap=0.36)
    ax.text(15.6, y + CH / 2 - 0.3, f"비교 {cmp_}번", ha="left", va="center", fontsize=11, color=RED, fontweight="bold")
ax.text(9.5, 1.0, "4 + 5 + 6 = 15번", ha="center", va="center", fontsize=13, color=RED, fontweight="bold")
save(fig, "a05-mergeup")

# 4. 거꾸로 받은 카드의 마지막 합치기: 한쪽 줄이 통째로 먼저 놓인다 → 비교 4번
merge_fig("a05-reverse", [5, 6, 7, 8], [1, 2, 3, 4], 4)

# 5. 거꾸로 8장: 삽입 정렬 28번 vs 병합 정렬 12번 (바둑돌)
fig, ax = canvas(11.0, 4.6, 18.0, 7.6)
row(ax, 0.3, 6.2, [8, 7, 6, 5, 4, 3, 2, 1], cw=0.7, ch=0.9, gap=0.08, fs=11)
ax.text(7.0, 6.65, "거꾸로 8장", ha="left", va="center", fontsize=12, fontweight="bold")
ax.text(0.3, 5.0, "삽입 정렬", ha="left", va="center", fontsize=12, fontweight="bold")
for k, n in enumerate(range(1, 8)):
    stones(ax, 0.6, 4.3 - k * 0.42, n, color=GREY, r=0.14, gap=0.36)
ax.text(4.0, 0.9, "1 + 2 + … + 7 = 28번", ha="center", va="center", fontsize=13, fontweight="bold")
ax.plot([8.6, 8.6], [0.4, 5.4], color=GREY, lw=1.2, ls="--")
ax.text(9.3, 5.0, "병합 정렬", ha="left", va="center", fontsize=12, fontweight="bold", color=RED)
for k in range(3):
    ax.text(9.2, 4.3 - k * 0.9, f"{k + 1}번째", ha="left", va="center", fontsize=11)
    stones(ax, 10.6, 4.3 - k * 0.9, 4, color=RED, r=0.18, gap=0.5)
ax.text(12.5, 0.9, "4 + 4 + 4 = 12번", ha="center", va="center", fontsize=13, fontweight="bold", color=RED)
save(fig, "a05-stones")

# 6. 카드가 많아지면: 막대 높이를 실제 비율대로
fig, ax = canvas(10.4, 5.6, 17.0, 9.2)
base = 1.4
scale = 6.6 / 120
for k, (n, ins, mer) in enumerate([(8, 28, 12), (16, 120, 32)]):
    gx = 2.0 + k * 7.0
    for j, (v, col) in enumerate([(ins, GREY), (mer, RED)]):
        bx = gx + j * 2.2
        h = v * scale
        ax.add_patch(Rectangle((bx, base), 1.7, h, fc=col, ec=INK, lw=1.2))
        ax.text(bx + 0.85, base + h + 0.15, f"{v}번", ha="center", va="bottom", fontsize=12, fontweight="bold",
                color=RED if col == RED else "#222")
        ax.text(bx + 0.85, base - 0.3, "삽입 정렬" if j == 0 else "병합 정렬", ha="center", va="top", fontsize=11,
                color=RED if col == RED else "#222", fontweight="bold")
    ax.text(gx + 1.95, base - 1.0, f"거꾸로 {n}장", ha="center", va="top", fontsize=12, fontweight="bold")
ax.plot([0.8, 16.4], [base, base], color=INK, lw=1.4)
save(fig, "a05-bars")

# 7. 합칠 때는 빈자리가 필요하다
fig, ax = canvas(11.0, 4.4, 18.0, 7.2)
ax.text(0.3, 6.8, "삽입 정렬", ha="left", va="center", fontsize=12, fontweight="bold")
row(ax, 0.8, 3.4, [3, 7, 9], cw=1.0, ch=1.3, fs=13)
card(ax, 2.6, 5.1, 0.8, 0.9, 5, hot=True, fs=11)
arrow(ax, (2.6, 5.4), (1.95, 4.85), color=RED, lw=1.6, ms=12)
ax.text(2.4, 2.6, "빈칸 0", ha="center", va="center", fontsize=12, fontweight="bold")
ax.plot([5.6, 5.6], [0.3, 7.0], color=GREY, lw=1.2, ls="--")
ax.text(6.2, 6.8, "병합 정렬", ha="left", va="center", fontsize=12, fontweight="bold")
row(ax, 6.4, 4.0, [2, 5, 7, 8], cw=1.0, ch=1.2, fs=12)
row(ax, 11.4, 4.0, [1, 3, 4, 6], cw=1.0, ch=1.2, fs=12)
for k in range(8):
    ax.add_patch(Rectangle((7.3 + k * 1.1, 1.6), 0.9, 1.2, fc="white", ec=RED, lw=1.4, ls="--"))
ax.text(11.6, 0.9, "빈칸 8", ha="center", va="center", fontsize=12, color=RED, fontweight="bold")
save(fig, "a05-space")
