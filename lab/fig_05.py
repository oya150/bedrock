"""알고리즘 5편 그림 만들기. 실행: python lab/fig_04.py  → docs/algorithms/img/05/*.svg

글자는 SVG 안에 글자로 남긴다(글꼴 모양을 파일에 넣지 않는다). 보는 쪽 글꼴로 그려진다.
카드는 차분한 색으로, 강조(새로 받은 카드, 비교 화살표, 많이 든 일)만 빨강으로 칠한다.
"""
import os

import matplotlib

matplotlib.use("svg")
import matplotlib.pyplot as plt
from matplotlib.patches import Arc, Circle, FancyArrowPatch, FancyBboxPatch, Rectangle

OUT = os.path.join(os.path.dirname(__file__), "..", "docs", "algorithms", "img", "05")
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


# 1. 여는 장면: 친구와 넷씩 나눠 정리한 뒤 합치면?
fig, ax = canvas(11.0, 4.6, 18.0, 7.6)
kid(ax, 1.4, 0.5, 1.4)
row(ax, 2.6, 4.6, [5, 2, 8, 7], cw=0.9, ch=1.2)
kid(ax, 16.6, 0.5, 1.4)
row(ax, 11.4, 4.6, [3, 6, 1, 4], cw=0.9, ch=1.2)
for k in range(8):
    ax.add_patch(Rectangle((4.6 + k * 1.0, 1.0), 0.9, 1.2, fc="white", ec=INK, lw=1.2, ls="--"))
ax.text(8.6, 3.1, "?", ha="center", va="center", fontsize=34, color=RED, fontweight="bold")
arrow(ax, (4.3, 4.4), (6.0, 2.5), color=RED, lw=1.8, rad=0.2)
arrow(ax, (13.3, 4.4), (11.4, 2.5), color=RED, lw=1.8, rad=-0.2)
ax.text(4.6, 6.3, "나", ha="center", va="center", fontsize=12, fontweight="bold")
ax.text(13.3, 6.3, "친구", ha="center", va="center", fontsize=12, fontweight="bold")
save(fig, "a05-friends.svg")

# 2. 이 편의 지도
fig, ax = canvas(13.6, 2.9, 24.2, 4.6)
titles = ["두 줄 합치기", "반씩 나누기", "4편과 나란히", "카드가 많아지면", "빈자리가 필요해요"]
for i, t in enumerate(titles):
    x = 0.3 + i * 4.8
    box(ax, x, 0.4, 3.8, 3.6)
    ax.text(x + 1.9, 0.95, t, ha="center", va="center", fontsize=12, fontweight="bold")
    if i == 0:
        row(ax, x + 0.4, 3.0, [2, 5], cw=0.5, ch=0.6, fs=9)
        row(ax, x + 2.0, 3.0, [1, 3], cw=0.5, ch=0.6, fs=9)
        row(ax, x + 0.9, 1.8, [1, 2, 3], cw=0.5, ch=0.6, hot=(0, 1, 2), fs=9)
    elif i == 1:
        for lv, (cnt, w) in enumerate([(1, 2.8), (2, 1.3), (4, 0.55)]):
            for k in range(cnt):
                ax.add_patch(Rectangle((x + 0.5 + k * (w + 0.12), 3.3 - lv * 0.55), w, 0.38, fc=NOTE, ec=INK, lw=1))
    elif i == 2:
        stones(ax, x + 0.5, 3.3, 9, color=GREY, r=0.11, gap=0.3)
        stones(ax, x + 0.5, 3.0, 9, color=GREY, r=0.11, gap=0.3)
        stones(ax, x + 0.5, 2.3, 6, color=RED, r=0.11, gap=0.3)
    elif i == 3:
        for k, (v, col) in enumerate([(120, GREY), (32, RED)]):
            h = 0.1 + v / 120 * 1.9
            ax.add_patch(Rectangle((x + 1.0 + k * 1.2, 1.5), 0.7, h, fc=col, ec=INK, lw=1))
    else:
        row(ax, x + 0.5, 3.0, [1, 3, 5], cw=0.5, ch=0.6, fs=9)
        for k in range(3):
            ax.add_patch(Rectangle((x + 0.5 + k * 0.6, 1.8), 0.5, 0.6, fc="white", ec=RED, lw=1.2, ls="--"))
    if i < 4:
        arrow(ax, (x + 3.95, 2.2), (x + 4.65, 2.2))
save(fig, "a05-map.svg")

# 3. 정렬된 두 줄 합치기: 2, 5, 7, 8 + 1, 3, 4, 6 → 비교 6번
fig, ax = canvas(11.6, 5.0, 19.0, 8.2)
ax.text(0.2, 7.5, "내 줄", ha="left", va="center", fontsize=12, fontweight="bold")
row(ax, 0.2, 5.6, [2, 5, 7, 8], cw=1.2, ch=1.4, fs=14)
ax.text(10.2, 7.5, "친구 줄", ha="left", va="center", fontsize=12, fontweight="bold")
row(ax, 10.2, 5.6, [1, 3, 4, 6], cw=1.2, ch=1.4, fs=14)
ax.text(0.2, 3.6, "새 줄", ha="left", va="center", fontsize=12, fontweight="bold")
merged = [1, 2, 3, 4, 5, 6, 7, 8]
end = row(ax, 2.2, 1.6, merged, cw=1.2, ch=1.4, fs=14, hot=range(6))
for k in range(8):
    x = 2.2 + k * 1.3 + 0.6
    if k < 6:
        ax.text(x, 3.45, "①②③④⑤⑥"[k], ha="center", va="center", fontsize=13, color=RED, fontweight="bold")
    else:
        ax.text(x, 3.45, "그대로", ha="center", va="center", fontsize=10, color=INK)
ax.text(9.5, 0.7, "맨 앞 카드끼리 비교해서 작은 쪽을 내려놓아요. 비교 6번", ha="center", va="center",
        fontsize=12, color=RED, fontweight="bold")
save(fig, "a05-merge.svg")

# 4. 한 장이 될 때까지 나누고, 합쳐 올라오기
fig, ax = canvas(11.6, 9.6, 19.0, 15.8)
cw, ch, g = 1.0, 1.1, 0.12
split = [[[5, 2, 8, 7, 3, 6, 1, 4]], [[5, 2, 8, 7], [3, 6, 1, 4]], [[5, 2], [8, 7], [3, 6], [1, 4]],
         [[5], [2], [8], [7], [3], [6], [1], [4]]]
mergeup = [([[2, 5], [7, 8], [3, 6], [1, 4]], 4), ([[2, 5, 7, 8], [1, 3, 4, 6]], 5), ([[1, 2, 3, 4, 5, 6, 7, 8]], 6)]


def layer(ax, y, piles, hot=False):
    x = 2.6
    total = sum(len(p) for p in piles) * (cw + g) + (len(piles) - 1) * 0.6
    x = 2.6 + (8 * (cw + g) + 7 * 0.6 - total) / 2
    for p in piles:
        x = row(ax, x, y, p, cw=cw, ch=ch, gap=g, hot=range(len(p)) if hot else ()) + 0.6


ax.text(0.1, 15.3, "나누기", ha="left", va="center", fontsize=13, fontweight="bold")
for lv, piles in enumerate(split):
    y = 13.6 - lv * 1.8
    layer(ax, y, piles)
    if lv:
        ax.text(1.2, y + ch / 2, f"{lv}번째", ha="center", va="center", fontsize=10, color=INK)
ax.text(16.4, 13.6 - 3 * 1.8 + ch / 2, "한 장이면\n이미 정렬", ha="left", va="center", fontsize=10, color=INK)
ax.plot([0.3, 18.7], [7.6, 7.6], color=GREY, lw=1.2, ls="--")
ax.text(0.1, 7.0, "합치기", ha="left", va="center", fontsize=13, fontweight="bold", color=RED)
for lv, (piles, cmp_) in enumerate(mergeup):
    y = 5.3 - lv * 1.9
    layer(ax, y, piles, hot=(lv == 2))
    ax.text(1.2, y + ch / 2, f"{lv + 1}번째", ha="center", va="center", fontsize=10, color=RED)
    stones(ax, 15.6, y + ch / 2 + 0.2, cmp_, color=RED, r=0.13, gap=0.36)
    ax.text(15.6, y + ch / 2 - 0.3, f"비교 {cmp_}번", ha="left", va="center", fontsize=11, color=RED, fontweight="bold")
ax.text(9.5, -0.4, "4 + 5 + 6 = 비교 15번", ha="center", va="center", fontsize=13, color=RED, fontweight="bold")
save(fig, "a05-tree.svg")

# 5. 거꾸로 8장: 삽입 정렬 28번 vs 병합 정렬 12번 (바둑돌)
fig, ax = canvas(11.0, 4.6, 18.0, 7.6)
row(ax, 0.3, 6.2, [8, 7, 6, 5, 4, 3, 2, 1], cw=0.7, ch=0.9, gap=0.08, fs=11)
ax.text(7.0, 6.65, "거꾸로 받은 카드 8장", ha="left", va="center", fontsize=12, fontweight="bold")
ax.text(0.3, 5.0, "4편 삽입 정렬", ha="left", va="center", fontsize=12, fontweight="bold")
for k, n in enumerate(range(1, 8)):
    stones(ax, 0.6, 4.3 - k * 0.42, n, color=GREY, r=0.14, gap=0.36)
ax.text(4.0, 0.9, "모두 28번", ha="center", va="center", fontsize=14, fontweight="bold")
ax.plot([8.6, 8.6], [0.4, 5.4], color=GREY, lw=1.2, ls="--")
ax.text(9.3, 5.0, "병합 정렬", ha="left", va="center", fontsize=12, fontweight="bold", color=RED)
for k in range(3):
    ax.text(9.2, 4.3 - k * 0.9, f"{k + 1}번째", ha="left", va="center", fontsize=11)
    stones(ax, 10.6, 4.3 - k * 0.9, 4, color=RED, r=0.18, gap=0.5)
ax.text(12.5, 0.9, "4 + 4 + 4 = 12번", ha="center", va="center", fontsize=14, fontweight="bold", color=RED)
save(fig, "a05-stones.svg")

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
    ax.text(gx + 1.95, base - 1.0, f"거꾸로 받은 카드 {n}장", ha="center", va="top", fontsize=12, fontweight="bold")
ax.plot([0.8, 16.4], [base, base], color=INK, lw=1.4)
save(fig, "a05-bars.svg")

# 7. 합칠 때는 빈자리가 필요하다
fig, ax = canvas(11.0, 4.4, 18.0, 7.2)
ax.text(0.3, 6.8, "4편: 손 안에서 끼워요", ha="left", va="center", fontsize=12, fontweight="bold")
row(ax, 0.8, 3.4, [3, 7, 9], cw=1.0, ch=1.3, fs=13)
card(ax, 2.6, 5.1, 0.8, 0.9, 5, hot=True, fs=11)
arrow(ax, (2.6, 5.4), (1.95, 4.85), color=RED, lw=1.6, ms=12)
ax.text(2.4, 2.6, "새 줄이 필요 없어요", ha="center", va="center", fontsize=11)
ax.plot([5.6, 5.6], [0.3, 7.0], color=GREY, lw=1.2, ls="--")
ax.text(6.2, 6.8, "병합 정렬: 새 줄을 놓을 자리가 필요해요", ha="left", va="center", fontsize=12, fontweight="bold")
row(ax, 6.4, 4.0, [2, 5, 7, 8], cw=1.0, ch=1.2, fs=12)
row(ax, 11.4, 4.0, [1, 3, 4, 6], cw=1.0, ch=1.2, fs=12)
for k in range(8):
    ax.add_patch(Rectangle((7.3 + k * 1.1, 1.6), 1.0, 1.2, fc="white", ec=RED, lw=1.4, ls="--"))
ax.text(11.6, 0.9, "카드 8장만큼 빈칸", ha="center", va="center", fontsize=12, color=RED, fontweight="bold")
save(fig, "a05-space.svg")
