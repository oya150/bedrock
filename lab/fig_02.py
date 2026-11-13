"""알고리즘 2편 그림 만들기. 실행: python lab/fig_02.py  → docs/algorithms/img/02/*.svg

예시는 사물함에서 시작해 이름을 담은 배열 칸으로 편 끝까지 잇는다.
그림 안 글씨는 낱말과 숫자만 둔다. 문장은 본문과 그림 설명에 둔다(쉬운글-정책 5장).
숫자는 모두 그림 속 칸과 이름으로 직접 센 것이다.
검토용 PNG가 필요하면 FIG_FMT=png FIG_OUT=<폴더> 로 실행한다.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "es"))
from figkit import BLUE, GREEN, GREY, INK, NOTE, PAPER, PINK, RED, YEL, arrow, canvas, cell, label, outdir, save  # noqa: E402
from matplotlib.patches import Rectangle  # noqa: E402

OUT = outdir("02", "algorithms")
PURPLE, WOOD = "#b59cc8", "#e8d3b0"
BOOKS = [BLUE, GREEN, YEL, PURPLE, WOOD]


def locker(ax, x, y, w, h, num, hot=False, fs=11):
    ax.add_patch(Rectangle((x, y), w, h, fc=PINK if hot else PAPER, ec=RED if hot else INK, lw=2.2 if hot else 1.2))
    ax.add_patch(Rectangle((x + w * 0.72, y + h * 0.4), w * 0.1, h * 0.2, fc=INK, ec=INK, lw=0))
    label(ax, x + w * 0.4, y + h * 0.72, str(num), fs=fs, color=RED if hot else INK, bold=True)


def slot(ax, x, y, w, h, num, name=None, hot=False, fs=12, empty=False, gone=False):
    """번호 달린 배열 칸. 번호는 칸 아래에. gone=지워진 이름(빨간 줄)."""
    if empty:
        ax.add_patch(Rectangle((x, y), w, h, fc="white", ec=GREY, lw=1.2, ls="--"))
    else:
        cell(ax, x, y, w, h, name or "", hot=hot, fs=fs)
    label(ax, x + w / 2, y - 0.3, str(num), fs=11, color=RED if hot else INK, bold=True)
    if gone:
        ax.plot([x + 0.15, x + w - 0.15], [y + 0.15, y + h - 0.15], color=RED, lw=2.4)
        ax.plot([x + 0.15, x + w - 0.15], [y + h - 0.15, y + 0.15], color=RED, lw=2.4)


def hop(ax, x1, x2, y, color=RED, lw=1.6, ms=12):
    """칸 위로 넘어가는 굽은 화살표."""
    arrow(ax, (x1, y), (x2, y), color=color, lw=lw, rad=-0.6, ms=ms)


# 1. 사물함 한 줄: 칸 폭이 한 걸음이면 1번 앞에서 16걸음 가면 17번
fig, ax = canvas(10.4, 2.9, 17.0, 4.8)
w = 0.78
for k in range(20):
    locker(ax, 0.6 + k * w, 2.2, w, 1.3, k + 1, hot=(k + 1 == 17), fs=9)
for k in range(21):
    ax.plot([0.6 + k * w] * 2, [1.75, 1.95], color=INK, lw=1.2)
ax.plot([0.6, 0.6 + 20 * w], [1.85, 1.85], color=INK, lw=1.2)
arrow(ax, (0.6 + 0.5 * w, 1.3), (0.6 + 16.5 * w, 1.3), color=RED, lw=2.4)
label(ax, 0.6 + 8.5 * w, 0.75, "16걸음", fs=13, color=RED, bold=True)
save(fig, OUT, "a02-steps.svg")

# 2. 책장: 두께가 제각각이라 하나씩 센다
fig, ax = canvas(10.4, 3.1, 17.0, 5.0)
widths = [0.35, 0.9, 0.5, 1.15, 0.4, 0.7, 0.3, 1.0, 0.55, 0.8, 0.45, 1.1, 0.35, 0.6, 0.95, 0.4, 0.75]
bx = 0.6
for k, bw in enumerate(widths):
    ax.add_patch(Rectangle((bx, 0.6), bw, 2.2 - (k % 3) * 0.25, fc=BOOKS[k % 5], ec=INK, lw=1.2))
    if k < 5:
        hop(ax, bx + bw / 2, bx + bw + widths[k + 1] / 2, 3.05, color=INK, lw=1.3, ms=10)
        label(ax, bx + bw / 2, 3.6, str(k + 1), fs=11, bold=True)
    bx += bw
label(ax, bx - widths[-1] / 2, 3.25, "17?", fs=14, color=RED, bold=True)
save(fig, OUT, "a02-books.svg")

# 3. 배열: 5번 칸을 바로 꺼낸다, 칸이 20개든 1,000개든 한 번
fig, ax = canvas(10.6, 4.4, 17.4, 7.2)
names = ["지우", "민준", "서연", "하준", "도윤", "수아", "시우", "하린"]
cw = 1.45
for k, nm in enumerate(names):
    slot(ax, 0.6 + k * cw, 4.6, cw, 1.2, k + 1, nm, hot=(k == 4))
label(ax, 0.6 + 8 * cw + 0.45, 5.2, "…", fs=20, bold=True)
slot(ax, 0.6 + 8 * cw + 0.9, 4.6, cw, 1.2, "1,000", "보람")
arrow(ax, (0.6 + 4.5 * cw, 7.0), (0.6 + 4.5 * cw, 5.95), color=RED, lw=2.4)
label(ax, 0.6 + 4.5 * cw + 0.3, 6.65, "5번", fs=13, color=RED, ha="left", bold=True)
for nm, x in [("칸 20개", 4.2), ("칸 1,000개", 11.2)]:
    ax.add_patch(Rectangle((x, 1.0), 1.4, 1.0, fc=RED, ec=INK, lw=1.2))
    label(ax, x + 0.7, 2.35, "1번", fs=13, color=RED, bold=True)
    label(ax, x + 0.7, 0.55, nm, fs=12, bold=True)
ax.plot([1.0, 16.4], [1.0, 1.0], color=INK, lw=1.4)
label(ax, 1.0, 2.0, "꺼내기", fs=12.5, ha="left", bold=True)
save(fig, OUT, "a02-memory.svg")

# 4. 맨 끝에 넣기와 맨 앞에 넣기
fig, ax = canvas(11.6, 3.9, 19.0, 6.4)
five = ["지우", "민준", "서연", "하준", "도윤"]
cw = 1.25
label(ax, 0.4, 5.9, "맨 끝에 넣기", fs=13, ha="left", bold=True)
for k, nm in enumerate(five):
    slot(ax, 0.4 + k * cw, 2.6, cw, 1.1, k + 1, nm, fs=11)
slot(ax, 0.4 + 5 * cw, 2.6, cw, 1.1, 6, "새봄", hot=True, fs=11)
arrow(ax, (0.4 + 5.5 * cw, 5.2), (0.4 + 5.5 * cw, 3.85), color=RED, lw=2.2)
label(ax, 0.4 + 3 * cw, 0.9, "1번", fs=14, color=RED, bold=True)
x0 = 10.6
label(ax, x0, 5.9, "맨 앞에 넣기", fs=13, ha="left", bold=True)
for k, nm in enumerate(five):
    slot(ax, x0 + k * cw, 2.6, cw, 1.1, k + 1, nm, fs=11)
slot(ax, x0 + 5 * cw, 2.6, cw, 1.1, 6, empty=True)
for k in range(4, -1, -1):
    hop(ax, x0 + (k + 0.5) * cw, x0 + (k + 1.5) * cw, 3.85)
    label(ax, x0 + (k + 1.0) * cw, 4.75, "①②③④⑤"[4 - k], fs=11, color=RED)
cell(ax, x0 - 1.35, 4.5, 1.0, 0.6, "새봄", hot=True, fs=11)
arrow(ax, (x0 - 0.6, 4.45), (x0 + 0.25, 3.8), color=RED, lw=2, rad=0.3)
label(ax, x0 + 3 * cw, 0.9, "5번 옮기기", fs=14, color=RED, bold=True)
save(fig, OUT, "a02-insert.svg")

# 5. 앞에서부터 옮기면: 지우를 2번에 넣는 순간 민준이 지워진다
fig, ax = canvas(7.4, 2.9, 12.0, 4.8)
cw = 1.25
slot(ax, 0.6, 1.4, cw, 1.1, 1, empty=True)
slot(ax, 0.6 + cw, 1.4, cw, 1.1, 2, "지우", hot=True, fs=11)
for k, nm in enumerate(["서연", "하준", "도윤"]):
    slot(ax, 0.6 + (k + 2) * cw, 1.4, cw, 1.1, k + 3, nm, fs=11)
slot(ax, 0.6 + 5 * cw, 1.4, cw, 1.1, 6, empty=True)
hop(ax, 0.6 + 0.5 * cw, 0.6 + 1.5 * cw, 2.65)
cell(ax, 0.6 + cw + 0.05, 3.65, cw - 0.1, 0.6, "민준", fs=11)
ax.plot([0.6 + cw + 0.05, 0.6 + 2 * cw - 0.05], [3.95, 3.95], color=RED, lw=2.2)
label(ax, 0.6 + 2 * cw + 0.2, 3.95, "지워짐", fs=12, color=RED, ha="left", bold=True)
save(fig, OUT, "a02-overwrite.svg")

# 6. 가나다 차례 가운데에 넣기: 3번 자리부터 뒤만 옮긴다
fig, ax = canvas(9.4, 3.3, 15.2, 5.4)
six = ["도윤", "민준", "서연", "시우", "지우", "하준"]
cw = 1.3
x0 = 2.4
for k, nm in enumerate(six):
    slot(ax, x0 + k * cw, 1.4, cw, 1.1, k + 1, nm, fs=11, hot=False)
slot(ax, x0 + 6 * cw, 1.4, cw, 1.1, 7, empty=True)
for k in range(5, 1, -1):
    hop(ax, x0 + (k + 0.5) * cw, x0 + (k + 1.5) * cw, 2.65)
for k in (0, 1):
    label(ax, x0 + (k + 0.5) * cw, 3.0, "그대로", fs=10, color=INK)
cell(ax, 0.3, 3.8, 1.2, 0.6, "새봄", hot=True, fs=11)
arrow(ax, (1.5, 3.95), (x0 + 2.4 * cw, 2.62), color=RED, lw=2, rad=-0.15)
label(ax, x0 + 4.5 * cw, 0.4, "4번 옮기기", fs=13.5, color=RED, bold=True)
save(fig, OUT, "a02-middle.svg")

# 7. 빅오 표: 번호로 꺼내기와 맨 앞에 넣기
fig, ax = canvas(9.6, 2.6, 15.4, 4.2)
xs, ws = [0.3, 5.3, 8.6, 11.9], [4.9, 3.2, 3.2, 3.2]
for h, x, w in zip(["일", "이름 n개", "두 배면", "빅오"], xs, ws):
    label(ax, x + w / 2, 3.75, h, fs=11.5, color=INK, bold=True)
rows = [("번호로 꺼내기", "1번", "그대로", "O(1)"), ("맨 앞에 넣기", "n번", "두 배", "O(n)")]
for r, row in enumerate(rows):
    y = 2.1 - r * 1.3
    for k, (s, x, w) in enumerate(zip(row, xs, ws)):
        cell(ax, x, y, w - 0.1, 1.0, s, hot=(r == 0 and k >= 2), fs=13)
save(fig, OUT, "a02-bigo.svg")

print("ok")
