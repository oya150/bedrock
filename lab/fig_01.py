"""1편 그림 만들기. 실행: python lab/fig_01.py  → docs/algorithms/img/01/*.svg

측정값은 lab/01_big_o.py를 한 번 돌린 결과를 그대로 옮겨 적었다.
글자는 SVG 안에 글자로 남긴다(글꼴 모양을 파일에 넣지 않는다). 보는 쪽 글꼴로 그려진다.
"""
import math
import os

import matplotlib

matplotlib.use("svg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Rectangle

OUT = os.path.join(os.path.dirname(__file__), "..", "docs", "algorithms", "img", "01")
os.makedirs(OUT, exist_ok=True)

plt.rcParams.update({
    "font.family": ["Apple SD Gothic Neo", "Noto Sans KR", "Malgun Gothic", "sans-serif"],
    "svg.fonttype": "none",
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.edgecolor": "#888",
    "axes.labelcolor": "#333",
    "xtick.color": "#555",
    "ytick.color": "#555",
    "text.color": "#222",
    "figure.facecolor": "white",
    "savefig.facecolor": "white",
})

SLOW, FAST, GREY, YEL = "#e4572e", "#2e86ab", "#c9ccd1", "#f6c445"


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), bbox_inches="tight", pad_inches=0.25)
    plt.close(fig)


def grid(ax, rows, cols, x0, y0, cell, title):
    for r in range(rows):
        for c in range(cols):
            ax.add_patch(Rectangle((x0 + c * cell, y0 + r * cell), cell * 0.9, cell * 0.9, color=SLOW, alpha=0.8))
    ax.text(x0 + cols * cell / 2, y0 + rows * cell + 0.5, title, ha="center", va="bottom", fontsize=13)


# 1. 느린 방법: 회원마다 탈퇴 명단을 다 본다 → 칸 하나가 비교 한 번
fig, ax = plt.subplots(figsize=(9, 4.6))
ax.set_xlim(-1, 21); ax.set_ylim(-3.2, 20); ax.axis("off")
grid(ax, 8, 2, 1, 0, 1, "회원 8명 × 탈퇴 2명\n= 16번")
grid(ax, 16, 4, 9, 0, 1, "회원 16명 × 탈퇴 4명\n= 64번")
ax.annotate("", xy=(8.4, 4), xytext=(4, 4), arrowprops=dict(arrowstyle="->", color="#555", lw=1.5))
ax.text(6.2, 4.6, "둘 다 두 배", ha="center", fontsize=12, color="#555")
ax.text(15.5, 8, "세로 두 배\n가로 두 배\n→ 칸은 네 배", fontsize=12, color="#333", va="center")
ax.text(0.2, -1.6, "빨간 칸 하나 = 회원 한 명과 탈퇴자 한 명의 이름을 맞대 보는 일 한 번", fontsize=11, color="#555")
save(fig, "slow-grid.svg")

# 2. 빠른 방법: 탈퇴자를 바로 찾는 상자에 넣고, 회원마다 한 번만 물어본다
fig, axes = plt.subplots(1, 2, figsize=(9, 3.2))
for ax, n in zip(axes, (8, 16)):
    ax.set_xlim(-0.5, 17); ax.set_ylim(-1.5, 4); ax.axis("off")
    for i in range(n):
        ax.add_patch(Rectangle((i, 0), 0.8, 0.8, color=FAST, alpha=0.85))
    ax.add_patch(FancyBboxPatch((n / 2 - 2, 2.4), 4, 1.1, boxstyle="round,pad=0.1", color=YEL))
    ax.text(n / 2, 2.95, "탈퇴자 상자", ha="center", va="center", fontsize=11)
    for i in range(n):
        ax.annotate("", xy=(n / 2, 2.35), xytext=(i + 0.4, 0.85), arrowprops=dict(arrowstyle="-", color="#9bb", lw=0.7))
    ax.text(n / 2, -1.0, f"회원 {n}명 → {n}번", ha="center", fontsize=13)
fig.text(0.5, -0.04, "파란 칸 하나 = 회원 한 명이 상자에 \"나 탈퇴했어?\" 하고 한 번 묻는 일", ha="center", fontsize=11, color="#555")
save(fig, "fast-row.svg")

# 3. 실측: 회원이 두 배가 될 때마다
members = [1000, 2000, 4000, 8000]
slow = [0.936, 3.539, 13.272, 52.972]
fast = [0.016, 0.034, 0.063, 0.144]
fig, axes = plt.subplots(1, 2, figsize=(10, 3.8), gridspec_kw={"width_ratios": [1.2, 1]})
ax = axes[0]
xs = range(4)
ax.plot(xs, slow, "o-", color=SLOW, lw=2.5, label="느린 방법")
ax.plot(xs, fast, "o-", color=FAST, lw=2.5, label="빠른 방법")
for x, y in zip(xs, slow):
    ax.annotate(f"{y:.1f}ms", (x, y), textcoords="offset points", xytext=(0, 8), ha="center", fontsize=9, color=SLOW)
ax.annotate("0.14ms\n(바닥에 붙어 보여요)", (3, fast[-1]), textcoords="offset points", xytext=(-10, 22), ha="right", fontsize=9, color=FAST)
ax.set_xticks(list(xs)); ax.set_xticklabels([f"{m:,}명" for m in members])
ax.set_ylim(0, 65); ax.set_ylabel("걸린 시간 (ms)"); ax.set_title("걸린 시간", fontsize=13)
ax.legend(frameon=False, loc="upper left")
ax = axes[1]
labs = ["1,000→2,000", "2,000→4,000", "4,000→8,000"]
rs = [slow[k + 1] / slow[k] for k in range(3)]
rf = [fast[k + 1] / fast[k] for k in range(3)]
w = 0.38
ax.bar([k - w / 2 for k in range(3)], rs, w, color=SLOW, label="느린 방법")
ax.bar([k + w / 2 for k in range(3)], rf, w, color=FAST, label="빠른 방법")
for k in range(3):
    ax.text(k - w / 2, rs[k] + 0.08, f"×{rs[k]:.1f}", ha="center", fontsize=10)
    ax.text(k + w / 2, rf[k] + 0.08, f"×{rf[k]:.1f}", ha="center", fontsize=10)
ax.axhline(4, color=SLOW, ls=":", lw=1); ax.axhline(2, color=FAST, ls=":", lw=1)
ax.text(2.62, 4.08, "4배", fontsize=9, color=SLOW); ax.text(2.62, 2.08, "2배", fontsize=9, color=FAST)
ax.set_xticks(range(3)); ax.set_xticklabels(labs, fontsize=9)
ax.set_ylim(0, 4.8); ax.set_yticks([]); ax.spines["left"].set_visible(False)
ax.set_title("두 배로 늘릴 때마다 몇 배?", fontsize=13)
fig.tight_layout()
save(fig, "measured.svg")

# 4. 3n²+5n+2 에서 앞부분과 뒷부분의 크기
fig, ax = plt.subplots(figsize=(9, 2.8))
rows = [(10, 300, 52, "앞 300번 · 뒤 52번"), (1000, 3_000_000, 5_002, "앞 300만 번 · 뒤 5,002번"),
        (1_000_000, 3e12, 5_000_002, "앞 3조 번 · 뒤 500만 번")]
for i, (n, big, small, lab) in enumerate(rows):
    tot = big + small
    ax.barh(i, big / tot * 100, color=SLOW)
    ax.barh(i, small / tot * 100, left=big / tot * 100, color=GREY)
    ax.text(101, i, lab, va="center", fontsize=10)
ax.set_yticks(range(3)); ax.set_yticklabels([f"n = {n:,}" for n, *_ in rows])
ax.invert_yaxis(); ax.set_xlim(0, 150); ax.set_xticks([])
ax.spines["bottom"].set_visible(False)
ax.legend(["앞부분 3 × n × n", "뒷부분 5 × n + 2"], loc="lower left", fontsize=10, frameon=False, ncol=2, bbox_to_anchor=(0.0, 1.0))
save(fig, "shares.svg")

# 5. 모양: 1, log n, n, n log n, n×n 이 자라는 모습
fig, axes = plt.subplots(1, 2, figsize=(10, 4))
for ax, top in ((axes[0], 16), (axes[1], 64)):
    ns = list(range(1, top + 1))
    lines = [("n × n", [n * n for n in ns], SLOW), ("n × log n", [n * math.log2(n) for n in ns], YEL),
             ("n", ns, FAST), ("log n", [math.log2(n) for n in ns], "#6a994e"), ("1", [1] * top, "#555")]
    for lab, ys, col in lines:
        ax.plot(ns, ys, color=col, lw=2.5)
    ax.set_xlabel("데이터 개수 n")
    if top == 16:
        ax.set_ylim(0, 80); ax.set_title("n이 16까지 (오른쪽 그래프의 왼쪽 아래를 크게)", fontsize=11)
        ax.set_xticks([0, 4, 8, 12, 16])
        for lab, ys, col in lines:
            y = min(ys[-1], 76) if lab != "n × n" else 76
            ax.text(top + 0.4, y if lab != "1" else 1, lab if lab != "1" else "1 (그대로)", va="center", fontsize=10, color=col)
        ax.set_ylabel("일하는 횟수")
    else:
        ax.set_title("n이 64까지", fontsize=12)
        ax.text(top + 1, 64 * 64, "n × n", va="center", fontsize=10, color=SLOW)
        ax.text(top + 1, 64 * 6 + 380, "n × log n", va="center", fontsize=10, color="#b8860b")
        ax.text(top + 1, 280, "n, log n, 1은\n바닥에 붙어요", va="top", fontsize=9, color="#555")
    ax.set_xlim(0, top * 1.25)
fig.tight_layout()
save(fig, "shapes.svg")

# 6. log: 반으로 몇 번 나눠야 하나
fig, ax = plt.subplots(figsize=(9, 2.8))
ax.set_xlim(0, 34); ax.set_ylim(-1.5, 2); ax.axis("off")
x = 0
for k, n in enumerate((16, 8, 4, 2, 1)):
    for i in range(n):
        ax.add_patch(Rectangle((x + i * 0.4, 0), 0.34, 0.8, color=FAST if n > 1 else YEL))
    ax.text(x + n * 0.2, 1.1, f"{n}장", ha="center", fontsize=11)
    if n > 1:
        ax.annotate("", xy=(x + n * 0.4 + 1.2, 0.4), xytext=(x + n * 0.4 + 0.2, 0.4), arrowprops=dict(arrowstyle="->", color="#555"))
        ax.text(x + n * 0.4 + 0.7, -0.35, "반", ha="center", fontsize=10, color="#555")
    x += n * 0.4 + 1.6
ax.text(0, -1.2, "16장 → 1장: 반으로 4번.  1,000장이면 10번쯤, 100만 장이면 20번쯤.  이 '몇 번'이 log n이에요.", fontsize=11, color="#333")
save(fig, "log-halving.svg")

# 7. 작은 데이터: 삽입정렬 vs 병합정렬, 누가 몇 배 빠른가
ns2 = [8, 32, 64, 128, 1024]
ins = [0.9, 9.4, 34.2, 121.8, 10837]
mer = [3.9, 20.4, 44.5, 97.3, 975]
fig, ax = plt.subplots(figsize=(9, 3.6))
for k, (n, a, b) in enumerate(zip(ns2, ins, mer)):
    if a < b:
        v = b / a; ax.barh(k, -v, color=SLOW); ax.text(-v - 0.2, k, f"삽입정렬이 {v:.1f}배 빨라요", ha="right", va="center", fontsize=10)
    else:
        v = a / b; ax.barh(k, v, color=FAST); ax.text(v + 0.2, k, f"병합정렬이 {v:.1f}배 빨라요", ha="left", va="center", fontsize=10)
ax.axvline(0, color="#555", lw=1)
ax.set_yticks(range(5)); ax.set_yticklabels([f"{n}개" for n in ns2]); ax.invert_yaxis()
ax.set_xlim(-12, 19); ax.set_xticks([]); ax.spines["bottom"].set_visible(False)
ax.set_ylabel("정렬할 개수")
save(fig, "sort-small.svg")

# 8. 심부름: 주문마다 창고에 다녀오기 vs 한 번에 모아 다녀오기
fig, axes = plt.subplots(1, 2, figsize=(9, 3.4))
for ax, trips, title in ((axes[0], 6, "주문 6건, 하나씩: 왕복 6번"), (axes[1], 1, "주문 6건, 한 번에 모아서: 왕복 1번")):
    ax.set_xlim(0, 10); ax.set_ylim(0, 7); ax.axis("off")
    ax.add_patch(FancyBboxPatch((0.3, 2.5), 2, 2, boxstyle="round,pad=0.1", color=FAST, alpha=0.85))
    ax.text(1.3, 3.5, "앱", ha="center", va="center", fontsize=13, color="white")
    ax.add_patch(FancyBboxPatch((7.4, 2.5), 2.3, 2, boxstyle="round,pad=0.1", color=YEL))
    ax.text(8.55, 3.5, "데이터\n베이스", ha="center", va="center", fontsize=12)
    for t in range(trips):
        y = 2.7 + (t * 1.6 / max(1, trips - 1) if trips > 1 else 0.8)
        ax.add_patch(FancyArrowPatch((2.5, y), (7.2, y), arrowstyle="<->", mutation_scale=12, color=SLOW if trips > 1 else "#3a7d44", lw=1.4))
    ax.text(5, 6.2, title, ha="center", fontsize=12)
save(fig, "trips.svg")

# 9. 카드로 보는 두 정렬
fig, axes = plt.subplots(1, 2, figsize=(9, 3.4))
ax = axes[0]; ax.set_xlim(0, 10); ax.set_ylim(0, 6); ax.axis("off")
ax.set_title("삽입정렬: 하나씩 제자리에 끼우기", fontsize=12)
for i, v in enumerate([2, 5, 8, 9]):
    ax.add_patch(Rectangle((0.6 + i * 1.5, 1.2), 1.2, 1.7, color=GREY)); ax.text(1.2 + i * 1.5, 2.05, str(v), ha="center", va="center", fontsize=14)
ax.add_patch(Rectangle((3.6, 4.0), 1.2, 1.7, color=YEL)); ax.text(4.2, 4.85, "6", ha="center", va="center", fontsize=14)
ax.annotate("", xy=(3.85, 3.05), xytext=(4.2, 3.95), arrowprops=dict(arrowstyle="->", color="#555", lw=1.5))
ax.annotate("", xy=(6.9, 0.9), xytext=(5.4, 0.9), arrowprops=dict(arrowstyle="->", color=SLOW, lw=1.5))
ax.text(6.2, 0.25, "8, 9는 한 칸씩 밀려나요", ha="center", fontsize=10, color=SLOW)
ax = axes[1]; ax.set_xlim(0, 10); ax.set_ylim(0, 6); ax.axis("off")
ax.set_title("병합정렬: 반씩 정리한 뒤 합치기", fontsize=12)
for i, v in enumerate([2, 6, 9]):
    ax.add_patch(Rectangle((0.4 + i * 1.3, 3.8), 1.1, 1.5, color=FAST, alpha=0.5)); ax.text(0.95 + i * 1.3, 4.55, str(v), ha="center", va="center", fontsize=13)
for i, v in enumerate([3, 5, 8]):
    ax.add_patch(Rectangle((5.6 + i * 1.3, 3.8), 1.1, 1.5, color=FAST, alpha=0.5)); ax.text(6.15 + i * 1.3, 4.55, str(v), ha="center", va="center", fontsize=13)
for i, v in enumerate([2, 3, 5, 6, 8, 9]):
    ax.add_patch(Rectangle((1.1 + i * 1.3, 0.8), 1.1, 1.5, color=FAST)); ax.text(1.65 + i * 1.3, 1.55, str(v), ha="center", va="center", fontsize=13, color="white")
ax.annotate("", xy=(4.5, 2.4), xytext=(2.2, 3.7), arrowprops=dict(arrowstyle="->", color="#555"))
ax.annotate("", xy=(5.6, 2.4), xytext=(7.8, 3.7), arrowprops=dict(arrowstyle="->", color="#555"))
ax.text(5, 3.1, "맨 앞끼리 비교", ha="center", fontsize=10, color="#555")
save(fig, "cards.svg")


# 10. 병합정렬: 나누는 층마다 카드 8장을 다 한 번씩 만진다
fig, ax = plt.subplots(figsize=(9.5, 3.9))
ax.set_xlim(-2.2, 15.5); ax.set_ylim(-0.8, 4.2); ax.axis("off")
layers = [[8], [4, 4], [2, 2, 2, 2], [1] * 8]
for li, groups in enumerate(layers):
    y = 3.3 - li * 1.1
    x = 0
    for g in groups:
        for i in range(g):
            ax.add_patch(Rectangle((x + i * 1.05, y), 0.9, 0.7, color=FAST, alpha=0.35 + 0.15 * li))
        x += g * 1.05 + 0.35
    ax.text(-0.4, y + 0.35, f"{len(groups)}묶음", ha="right", va="center", fontsize=10, color="#555")
for k in range(3):
    ybot, ytop = 3.3 - (k + 1) * 1.1 + 0.7, 3.3 - k * 1.1
    ax.annotate("", xy=(10.4, ytop + 0.05), xytext=(10.4, ybot - 0.05), arrowprops=dict(arrowstyle="->", color=SLOW, lw=1.5))
    ax.text(10.7, (ybot + ytop) / 2, f"합치기 {3 - k}: 8장 만짐", va="center", fontsize=10, color=SLOW)
ax.text(4.8, -0.6, "아래에서 위로 세 번 합쳐요. 합칠 때마다 8장을 한 번씩 만지니 8 × 3 = 24번", ha="center", fontsize=11)
save(fig, "merge-levels.svg")

# 11. 삽입정렬: 미는 장수를 계단으로 쌓고, 같은 계단을 거꾸로 얹으면 (n-1) × n 네모
fig, ax = plt.subplots(figsize=(5.6, 4.6))
n = 8
ax.set_xlim(0.5, n + 4.6); ax.set_ylim(-1.4, n + 0.6); ax.set_aspect("equal"); ax.axis("off")
ax.add_patch(Rectangle((1, 0), n - 1, n, fill=False, ec="#888", lw=1.2, ls="--"))
for k in range(1, n):
    for h in range(n):
        ax.add_patch(Rectangle((k + 0.04, h + 0.04), 0.92, 0.92, color=SLOW if h < k else GREY, alpha=0.85))
    ax.text(k + 0.5, -0.45, str(k + 1), ha="center", fontsize=9, color="#555")
ax.text((n + 1) / 2, -1.2, "몇 번째 카드", ha="center", fontsize=10, color="#555")
ax.text(n + 0.3, n - 0.2, "회색: 같은 계단을\n거꾸로 얹은 것\n\n점선 네모:\n7 × 8 = 56칸", fontsize=10, color="#555", va="top")
ax.text(n + 0.3, 3, "빨간 계단:\n1+2+…+7\n= 28칸\n(네모의 반)", fontsize=10, color=SLOW, va="top")
save(fig, "insertion-steps.svg")

print("ok", sorted(os.listdir(OUT)))
