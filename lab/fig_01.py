"""1편 그림 만들기. 실행: python lab/fig_01.py  → docs/algorithms/img/01/*.svg

측정값은 lab/01_big_o.py를 한 번 돌린 결과를 그대로 옮겨 적었다.
글자는 SVG 안에 글자로 남긴다(글꼴 모양을 파일에 넣지 않는다). 보는 쪽 글꼴로 그려진다.
"""
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


def grid(ax, rows, cols, x0, y0, title, cw=2.4, ch=0.5):
    for r in range(rows):
        for c in range(cols):
            ax.add_patch(Rectangle((x0 + c * cw, y0 + r * ch), cw * 0.94, ch * 0.86, color=SLOW, alpha=0.8))
    ax.text(x0 + cols * cw / 2, y0 + rows * ch + 0.4, title, ha="center", va="bottom", fontsize=13)


# 1. 느린 방법: 회원마다 탈퇴 명단을 다 본다 → 칸 하나가 비교 한 번 (탈퇴자는 회원 10명 중 1명꼴)
fig, ax = plt.subplots(figsize=(8.5, 5.4))
ax.set_xlim(-1.5, 22); ax.set_ylim(-2.6, 13); ax.axis("off")
grid(ax, 10, 1, 1.5, 0, "회원 10명 × 탈퇴 1명\n= 10칸")
grid(ax, 20, 2, 10, 0, "회원 20명 × 탈퇴 2명\n= 40칸")
ax.annotate("", xy=(9.3, 2.5), xytext=(4.4, 2.5), arrowprops=dict(arrowstyle="->", color="#555", lw=1.5))
ax.text(6.85, 2.9, "둘 다 두 배", ha="center", fontsize=12, color="#555")
ax.annotate("", xy=(9.4, 10.1), xytext=(9.4, 0), arrowprops=dict(arrowstyle="->", color="#999", lw=1))
ax.text(9.1, 5, "회원 수", rotation=90, ha="right", va="center", fontsize=10, color="#777")
ax.annotate("", xy=(14.9, -0.4), xytext=(10, -0.4), arrowprops=dict(arrowstyle="->", color="#999", lw=1))
ax.text(12.4, -0.8, "탈퇴자 수", ha="center", va="top", fontsize=10, color="#777")
ax.text(15.8, 5, "세로(회원) 두 배\n가로(탈퇴자) 두 배\n→ 칸은 네 배", fontsize=12, color="#333", va="center")
ax.text(-1, -2.2, "빨간 칸 하나 = 회원 한 명과 탈퇴자 한 명의 이름을 맞대 보는 일 한 번", fontsize=11, color="#555")
save(fig, "slow-grid.svg")

# 2. 빠른 방법: 탈퇴자를 바로 찾는 상자에 넣고, 회원마다 한 번만 물어본다
fig, axes = plt.subplots(1, 2, figsize=(9, 3.2))
for ax, n in zip(axes, (8, 16)):
    ax.set_xlim(-0.5, 17); ax.set_ylim(-1.5, 4); ax.axis("off")
    for i in range(n):
        ax.add_patch(Rectangle((i, 0), 0.8, 0.8, color=FAST, alpha=0.85))
    ax.add_patch(FancyBboxPatch((n / 2 - 2, 2.4), 4, 1.1, boxstyle="round,pad=0.1", color=YEL))
    ax.text(n / 2, 2.95, "탈퇴자 사물함", ha="center", va="center", fontsize=11)
    for i in range(n):
        ax.annotate("", xy=(n / 2, 2.35), xytext=(i + 0.4, 0.85), arrowprops=dict(arrowstyle="-", color="#9bb", lw=0.7))
    ax.text(n / 2, -1.0, f"회원 {n}명 → {n}번", ha="center", fontsize=13)
fig.text(0.5, -0.04, "파란 칸 하나 = 회원 한 명이 상자에 \"나 탈퇴했어?\" 하고 한 번 묻는 일", ha="center", fontsize=11, color="#555")
save(fig, "fast-row.svg")

# 3. 실측: 회원이 두 배가 될 때마다
members = [1000, 2000, 4000, 8000]
slow = [0.936, 3.539, 13.272, 52.972]
fast = [0.016, 0.034, 0.063, 0.144]
fig, ax = plt.subplots(figsize=(7.5, 4.2))
xs = range(4)
ax.plot(xs, slow, "o-", color=SLOW, lw=2.5, label="느린 방법")
ax.plot(xs, fast, "o-", color=FAST, lw=2.5, label="빠른 방법")
for x, y in zip(xs, slow):
    ax.annotate(f"{y:.1f}ms", (x, y), textcoords="offset points", xytext=(0, 8), ha="center", fontsize=9, color=SLOW)
ax.annotate("파란 선: 너무 작아서 바닥에 붙어 보여요\n(8,000명일 때 0.14ms, 두 배마다 약 2배)", (3, fast[-1]), textcoords="offset points", xytext=(-10, 22), ha="right", fontsize=9, color=FAST)
ax.set_xticks(list(xs)); ax.set_xticklabels([f"{m:,}명" for m in members])
ax.set_ylim(0, 65); ax.set_ylabel("걸린 시간 (ms = 밀리초)"); ax.set_title("걸린 시간", fontsize=13)
ax.legend(frameon=False, loc="upper left")
for k in range(3):
    ax.text(k + 0.4, (slow[k] + slow[k + 1]) / 2 + 5, "×4", ha="center", fontsize=13, color=SLOW, fontweight="bold")
fig.tight_layout()
save(fig, "measured.svg")

# 4. n×n+5n+2 에서 앞부분과 뒷부분의 크기
fig, ax = plt.subplots(figsize=(9, 2.8))
rows = [(10, 100, 52, "앞 100번 · 뒤 52번"), (1000, 1_000_000, 5_002, "앞 100만 번 · 뒤 5,002번"),
        (1_000_000, 1e12, 5_000_002, "앞 1조 번 · 뒤 500만 번")]
for i, (n, big, small, lab) in enumerate(rows):
    tot = big + small
    ax.barh(i, big / tot * 100, color=SLOW)
    ax.barh(i, small / tot * 100, left=big / tot * 100, color=GREY)
    ax.text(101, i, lab, va="center", fontsize=10)
ax.set_yticks(range(3)); ax.set_yticklabels([f"n = {n:,}" for n, *_ in rows])
ax.invert_yaxis(); ax.set_xlim(0, 150); ax.set_xticks([])
ax.spines["bottom"].set_visible(False)
ax.legend(["앞부분 n × n", "뒷부분 5 × n + 2"], loc="lower left", fontsize=10, frameon=False, ncol=2, bbox_to_anchor=(0.0, 1.0))
save(fig, "shares.svg")


# 8. 심부름: 주문마다 창고에 다녀오기 vs 한 번에 모아 다녀오기 (안에서 찾는 일은 양쪽 다 6번)
fig, axes = plt.subplots(1, 2, figsize=(9.5, 2.9))
for ax, trips, title in ((axes[0], 6, "하나씩 물으면: 왕복 6번"), (axes[1], 1, "모아서 물으면: 왕복 1번")):
    ax.set_xlim(0, 10); ax.set_ylim(1.2, 6.8); ax.axis("off")
    ax.add_patch(FancyBboxPatch((0.3, 2.5), 2, 2, boxstyle="round,pad=0.1", color=FAST, alpha=0.85))
    ax.text(1.3, 3.5, "앱", ha="center", va="center", fontsize=13, color="white")
    ax.add_patch(FancyBboxPatch((7.2, 2.1), 2.5, 2.8, boxstyle="round,pad=0.1", color=YEL))
    ax.text(8.45, 4.35, "데이터베이스", ha="center", va="center", fontsize=10)
    for k in range(6):
        ax.add_patch(Rectangle((7.45 + (k % 3) * 0.72, 2.45 + (k // 3) * 0.75), 0.55, 0.55, color="white", ec="#888"))
    ax.text(8.45, 1.6, "안에서 찾기 6번", ha="center", va="top", fontsize=9, color="#555")
    for t in range(trips):
        y = 2.7 + (t * 1.6 / max(1, trips - 1) if trips > 1 else 0.8)
        ax.add_patch(FancyArrowPatch((2.5, y), (7.0, y), arrowstyle="<->", mutation_scale=12, color=SLOW if trips > 1 else "#3a7d44", lw=1.4))
    ax.text(5, 6.2, title, ha="center", fontsize=12)
fig.text(0.5, -0.06, "주문 6개를 물어볼 때. 찾는 일은 둘 다 6번이라 빅오는 같고, 왕복 횟수만 달라요", ha="center", fontsize=11, color="#555")
save(fig, "trips.svg")

# 12. set 상자: 이름만 보면 칸 번호가 정해진다
fig, ax = plt.subplots(figsize=(9, 3.4))
ax.set_xlim(-0.5, 10.5); ax.set_ylim(-1.3, 4.0); ax.axis("off")
for i in range(10):
    hit = i in (2, 7)
    ax.add_patch(Rectangle((i + 0.05, 0), 0.9, 1.1, color=YEL if hit else GREY, alpha=0.9))
    ax.text(i + 0.5, 0.55, str(i), ha="center", va="center", fontsize=12)
for name, box, x in (("민지", 2, 1.4), ("준호", 7, 7.2)):
    ax.text(x, 3.2, name, ha="center", va="center", fontsize=13, bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="#888"))
    ax.annotate("", xy=(box + 0.5, 1.15), xytext=(x, 2.75), arrowprops=dict(arrowstyle="->", color=SLOW, lw=1.6))
    ax.text((x + box + 0.5) / 2 + 0.25, 2.0, f"늘 {box}번 사물함", fontsize=10, color=SLOW)
ax.text(5, -0.8, "넣을 때도, 물을 때도 같은 이름은 같은 사물함 → 그 사물함 하나만 열어 봐요", ha="center", fontsize=12)
save(fig, "set-lockers.svg")

# 13. 결석한 친구 찾기: 반 친구 한 명마다 결석 명단을 처음부터 끝까지
fig, ax = plt.subplots(figsize=(8, 4.2))
ax.set_xlim(0, 10); ax.set_ylim(-0.8, 6.4); ax.axis("off")
cls = ["민지", "준호", "서연", "도윤", "하은"]
absent = ["준호", "하은"]
ax.text(1.5, 6.0, "반 친구 명단", ha="center", fontsize=12)
ax.text(8.0, 6.0, "결석 명단", ha="center", fontsize=12)
for i, nm in enumerate(cls):
    y = 5.0 - i * 1.0
    ax.text(1.5, y, nm, ha="center", va="center", fontsize=12, bbox=dict(boxstyle="round,pad=0.3", fc="#fde4dc" if i == 0 else "white", ec="#888"))
for j, nm in enumerate(absent):
    y = 4.0 - j * 1.6
    ax.text(8.0, y, nm, ha="center", va="center", fontsize=12, bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="#888"))
    ax.annotate("", xy=(7.3, y), xytext=(2.3, 5.0), arrowprops=dict(arrowstyle="->", color=SLOW, lw=1.4))
    ax.text(6.4, y + 0.35, "같은 이름?", fontsize=10, color=SLOW, ha="center")
ax.text(5, -0.5, "민지 한 명을 확인하려고 결석 명단을 처음부터 끝까지 봐요. 다음 친구도, 그다음 친구도요.", ha="center", fontsize=11, color="#555")
save(fig, "class-scan.svg")

# 14. 연습 때와 진짜 앱: 같은 코드, 1밀리초도 안 걸리던 게 14분
fig, ax = plt.subplots(figsize=(8.5, 3.0))
ax.set_xlim(0, 10); ax.set_ylim(0, 4); ax.axis("off")
for x, who, t, col in ((0.3, "연습: 회원 1,000명", "1밀리초도 안 걸려요\n(눈 깜짝할 새보다 짧아요)", FAST), (6.0, "진짜 앱: 회원 100만 명", "14분", SLOW)):
    ax.add_patch(FancyBboxPatch((x, 0.6), 3.7, 2.4, boxstyle="round,pad=0.1", fc="white", ec=col, lw=2))
    ax.text(x + 1.85, 2.55, who, ha="center", fontsize=12)
    ax.text(x + 1.85, 1.45, t, ha="center", va="center", fontsize=15 if t == "14분" else 11, color=col, fontweight="bold" if t == "14분" else "normal")
ax.annotate("", xy=(5.8, 1.8), xytext=(4.2, 1.8), arrowprops=dict(arrowstyle="->", color="#555", lw=1.8))
ax.text(5.0, 2.15, "같은 코드", ha="center", fontsize=10, color="#555")
save(fig, "small-big.svg")

# 15. 컴퓨터가 달라도 규칙은 같다
fig, axes = plt.subplots(1, 2, figsize=(8.5, 3.4), sharey=True)
for ax, name, base in ((axes[0], "보통 컴퓨터", 2.0), (axes[1], "두 배 빠른 컴퓨터", 1.0)):
    ax.bar([0, 1], [base, base * 4], 0.55, color=[GREY, SLOW])
    ax.set_xticks([0, 1]); ax.set_xticklabels(["회원 1,000명", "회원 2,000명"])
    ax.text(0.5, base * 4 + 0.3, "×4", ha="center", fontsize=15, color=SLOW, fontweight="bold")
    ax.set_title(name, fontsize=12); ax.set_yticks([]); ax.spines["left"].set_visible(False)
    ax.set_ylim(0, 10)
fig.text(0.5, -0.04, "걸린 시간은 컴퓨터마다 달라도, 두 배면 4배라는 규칙은 같아요", ha="center", fontsize=11, color="#555")
fig.tight_layout()
save(fig, "two-computers.svg")

# 16. 빅오 이름표: 두 배면 몇 배?
fig, ax = plt.subplots(figsize=(9, 3.6))
ax.set_xlim(0, 12); ax.set_ylim(0, 4.6); ax.axis("off")
rows = [(3.3, "느린 방법", "일 ×4", "O(n²)", SLOW, "n이 3이면 3×3 = 9칸, n이 6이면 6×6 = 36칸 (4배)"),
        (1.2, "빠른 방법", "일 ×2", "O(n)", FAST, "n이 3이면 3번, n이 6이면 6번 (2배)")]
for y, nm, mul, tag, col, ex in rows:
    ax.text(1.0, y, nm, ha="center", va="center", fontsize=12)
    ax.text(3.4, y, "회원 ×2", ha="center", va="center", fontsize=12, bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="#888"))
    ax.annotate("", xy=(5.2, y), xytext=(4.3, y), arrowprops=dict(arrowstyle="->", color="#555"))
    ax.text(6.1, y, mul, ha="center", va="center", fontsize=13, color=col, fontweight="bold")
    ax.annotate("", xy=(8.0, y), xytext=(7.0, y), arrowprops=dict(arrowstyle="->", color="#555"))
    ax.text(9.2, y, tag, ha="center", va="center", fontsize=16, color="white", fontweight="bold", bbox=dict(boxstyle="round,pad=0.4", fc=col, ec=col))
    ax.text(6.1, y - 0.7, ex, ha="center", va="center", fontsize=11.5, color="#444")
ax.text(9.2, 4.35, "빅오 이름표", ha="center", fontsize=11, color="#555")
save(fig, "bigo-tags.svg")

# 17. 종이 vs 계산기: 둘 다 곧은 선(O(n)), 몇 배인지는 늘 5배
fig, ax = plt.subplots(figsize=(7.5, 4.2))
ns = [0, 20, 40, 60, 80]
ax.plot(ns, [n / 2 for n in ns], color=SLOW, lw=2.5)
ax.plot(ns, [n / 10 for n in ns], color=FAST, lw=2.5)
ax.text(81, 40, "종이로 더하는 친구", va="center", fontsize=11, color=SLOW)
ax.text(81, 8, "계산기로 더하는 친구", va="center", fontsize=11, color=FAST)
for n in (20, 60):
    ax.plot([n, n], [n / 10, n / 2], color="#888", lw=1, ls=":")
    ax.plot([n, n], [n / 10, n / 2], "o", color="#888", ms=4)
    ax.text(n + 1.5, n * 0.3, f"{n // 10}초 대 {n // 2}초\n= 5배", fontsize=11, color="#333")
ax.set_xlabel("더할 숫자 개수 →"); ax.set_ylabel("걸린 시간 →")
ax.set_xticks([]); ax.set_yticks([]); ax.set_xlim(0, 112); ax.set_ylim(0, 44)
ax.set_title("빅오는 둘 다 O(n). 개수가 늘어도 늘 5배 차이", fontsize=12)
save(fig, "paper-calc.svg")

print("ok", sorted(os.listdir(OUT)))
