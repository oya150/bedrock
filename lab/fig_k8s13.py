"""쿠버네티스 13편 그림 만들기. 실행: python lab/fig_k8s13.py  → docs/kubernetes/img/13/*.svg

예시는 빵집 주문 앱의 주문 장부 디스크. 블록 8칸, 블록 1~5에 주문 1~5, 6~8은 빈칸.
오후 3시에 스냅샷을 찍고, 그 뒤 주문 6이 들어오고 블록 3이 엉망으로 덮어써진다.
그림 안 글씨는 낱말과 숫자만 둔다. 지금 볼 곳만 빨강.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "es"))
from figkit import (GREY, INK, PAPER, PINK, RED, arrow, box, canvas, cell, cylinder,  # noqa: E402
                    label, outdir, save)
from matplotlib.patches import Rectangle  # noqa: E402

OUT = outdir("13", topic="kubernetes")
FILM = "#eaf2fb"
BASE = ["주문 1", "주문 2", "주문 3", "주문 4", "주문 5", "", "", ""]
X0, W, GAP = 2.6, 1.0, 0.1
ROW_W = 8 * (W + GAP) - GAP


def bx(i):
    return X0 + i * (W + GAP)


def row(ax, y, items, name, hot=(), dim=(), film=False, name_hot=False, nums=False, h=0.75):
    """블록 8칸 한 줄. film=투명 필름 층(빈칸은 점선)."""
    label(ax, 0.2, y + h / 2, name, fs=10.5, ha="left", color=RED if name_hot else INK, bold=name_hot)
    for i, s in enumerate(items):
        x = bx(i)
        if nums:
            label(ax, x + W / 2, y + h + 0.4, str(i + 1), fs=9.5, color=INK)
        if film and not s:
            ax.add_patch(Rectangle((x, y), W, h, fc=FILM, ec=RED if i in hot else GREY, lw=1.0, ls="--"))
        elif not s:
            ax.add_patch(Rectangle((x, y), W, h, fc="white", ec=GREY if i in dim else INK, lw=1.0))
        else:
            cell(ax, x, y, W, h, s, hot=i in hot, dim=i in dim, fs=9.5,
                 fc=(PINK if i in hot else (FILM if film else None)))


def frame(ax, y, color=INK, ls="-", lw=1.3, h=0.75):
    ax.add_patch(Rectangle((X0 - 0.12, y - 0.12), ROW_W + 0.24, h + 0.24, fill=False, ec=color, lw=lw, ls=ls))


def one(draw, name, size=(7.2, 3.6), lim=(12, 6)):
    fig, ax = canvas(*size, *lim)
    ax.add_patch(Rectangle((0, 0), *lim, fill=False, ec="none"))
    draw(ax)
    save(fig, OUT, name)


# 그림 1: 디스크는 번호 붙은 블록 칸
def block(ax):
    cylinder(ax, 0.3, 3.9, 2.0, 1.3, "주문 장부")
    row(ax, 1.6, BASE, "블록", nums=True, hot=(2,))
    label(ax, X0 + ROW_W / 2, 3.25, "주문 장부 디스크", fs=11, bold=True)
    arrow(ax, (2.4, 4.4), (bx(2) + W / 2, 2.75), color=RED, ms=14, rad=-0.2)
    label(ax, 4.6, 4.5, "블록 3 읽기", fs=10.5, color=RED, bold=True, ha="left")


# 그림 2: 다 복사하는 중
def copy(ax):
    row(ax, 3.8, BASE, "디스크", nums=True)
    label(ax, 0.2, 1.97, "복사본", fs=10.5, ha="left", color=INK)
    for i in range(8):
        x = bx(i)
        if i < 3:
            cell(ax, x, 1.6, W, 0.75, BASE[i], hot=(i == 2), fs=9.5)
        else:
            ax.add_patch(Rectangle((x, 1.6), W, 0.75, fc="white", ec=GREY, lw=1.0, ls="--"))
    arrow(ax, (bx(2) + W / 2, 3.72), (bx(2) + W / 2, 2.42), color=RED, ms=13)
    label(ax, bx(5) + W / 2 + 0.55, 1.15, "남은 칸 5", fs=10.5, color=RED, bold=True)


# 그림 3: 지금 층을 잠그고 빈 필름을 덮는다
def film(ax):
    row(ax, 3.8, [""] * 8, "새 층", film=True, name_hot=True, hot=range(8), nums=True)
    frame(ax, 3.8, color=RED, ls="--", lw=2.0)
    row(ax, 1.7, BASE, "오후 3시 층")
    frame(ax, 1.7)
    label(ax, bx(7) + W / 2, 1.25, "잠금", fs=10.5, color=INK, bold=True)


# 그림 4: 찍은 뒤의 쓰기
def write(ax):
    top = [""] * 8
    top[2], top[5] = "엉망", "주문 6"
    row(ax, 3.8, top, "새 층", film=True, hot=(2, 5), nums=True)
    frame(ax, 3.8, color="#7da2c8", ls="--")
    row(ax, 1.7, BASE, "오후 3시 층", dim=(2,))
    frame(ax, 1.7)
    label(ax, bx(7) + W / 2, 1.25, "잠금", fs=10.5, color=INK, bold=True)


# 그림 5: 읽기는 위층부터
def read(ax):
    top = [""] * 8
    top[2], top[5] = "엉망", "주문 6"
    row(ax, 3.4, top, "새 층", film=True)
    frame(ax, 3.4, color="#7da2c8", ls="--")
    cell(ax, bx(2), 3.4, W, 0.75, "엉망", hot=True, fs=9.5)
    row(ax, 1.4, BASE, "오후 3시 층", hot=(0,))
    frame(ax, 1.4)
    for i, end in ((0, 2.22), (2, 4.22)):
        x = bx(i) + W / 2
        ax.annotate("", xy=(x, end), xytext=(x, 5.3),
                    arrowprops=dict(arrowstyle="-|>", color=RED, lw=1.8, mutation_scale=13))
    label(ax, bx(0) + W / 2, 5.55, "블록 1 읽기", fs=10, color=RED, bold=True)
    label(ax, bx(2) + W / 2 + 0.3, 5.55, "블록 3 읽기", fs=10, color=RED, bold=True)


# 그림 6: 되돌리기는 위층 떼어 내기
def revert(ax):
    top = [""] * 8
    top[2], top[5] = "엉망", "주문 6"
    row(ax, 3.8, top, "새 층", film=True, dim=(2, 5))
    frame(ax, 3.8, color=RED, ls="--", lw=2.0)
    ax.plot([X0 - 0.1, X0 + ROW_W + 0.1], [3.7, 4.65], color=RED, lw=2.4)
    label(ax, X0 + ROW_W / 2, 5.2, "떼어 냄", fs=11, color=RED, bold=True)
    row(ax, 1.7, BASE, "오후 3시 층", hot=range(5), name_hot=True)
    frame(ax, 1.7)


# 그림 7: 백업은 바깥 보관소로 복사
def backup(ax):
    box(ax, 0.3, 1.2, 6.6, 4.2, fc="white")
    label(ax, 0.55, 5.0, "디스크", fs=11, ha="left", bold=True)
    cell(ax, 0.8, 3.4, 5.6, 0.8, "새 층", fc=FILM, fs=10.5)
    cell(ax, 0.8, 2.1, 5.6, 0.8, "오후 3시 층 (스냅샷)", fs=10.5)
    box(ax, 8.2, 1.2, 3.5, 4.2, fc=PAPER, ec=RED)
    label(ax, 9.95, 5.0, "바깥 보관소", fs=11, color=RED, bold=True)
    arrow(ax, (6.5, 2.5), (8.6, 2.5), color=RED, ms=14)
    label(ax, 7.55, 2.85, "복사", fs=10.5, color=RED, bold=True)
    cell(ax, 8.6, 2.1, 2.75, 0.8, "오후 3시 백업", hot=True, fs=10.5)


# 그림 8·9: 저장소 두 개를 찍는 순서
def orders(ax, x, y, n, title, hot=(), ghost=()):
    label(ax, x + 1.1, y + 2.0, title, fs=10.5, color=INK, bold=True)
    for k in range(6):
        yy = y + 1.5 - k * 0.3
        if k < n:
            on = (k + 1) in hot
            label(ax, x + 0.5, yy, f"주문 {k + 1}", fs=10, ha="left", color=RED if on else "#222", bold=on)
        elif (k + 1) in ghost:
            label(ax, x + 0.5, yy, f"주문 {k + 1}", fs=10, ha="left", color=RED, bold=True)


def pair(right):
    def draw(ax):
        steps = (["① 검색 찍기", "주문 6", "② 장부 찍기"] if right else ["① 장부 찍기", "주문 6", "② 검색 찍기"])
        xs = (3.0, 6.3, 9.6)
        label(ax, 0.2, 5.8, "순서", fs=10.5, ha="left", color=INK, bold=True)
        for k, (x, s) in enumerate(zip(xs, steps)):
            box(ax, x - 1.15, 5.5, 2.3, 0.6, fc=PINK if k != 1 else "white", ec=RED if k != 1 else INK, lw=1.4)
            label(ax, x, 5.8, s, fs=10, color=RED if k != 1 else "#222", bold=(k != 1))
            if k < 2:
                arrow(ax, (x + 1.25, 5.8), (xs[k + 1] - 1.25, 5.8), ms=11)
        cylinder(ax, 0.6, 3.4, 2.2, 1.0, "주문 장부")
        cylinder(ax, 8.4, 3.4, 2.2, 1.0, "주문 검색")
        arrow(ax, (3.0, 3.9), (8.2, 3.9), ms=14)
        label(ax, 5.6, 4.2, "바뀐 주문", fs=10, color=INK)
        if right:
            orders(ax, 0.6, 0.2, 6, "되돌린 장부")
            orders(ax, 8.4, 0.2, 5, "되돌린 검색", ghost=(6,))
            arrow(ax, (2.6, 0.2), (8.7, 0.2), color=RED, ms=13)
            label(ax, 5.65, 0.5, "따라잡기", fs=10.5, color=RED, bold=True)
        else:
            orders(ax, 0.6, 0.2, 5, "되돌린 장부")
            orders(ax, 8.4, 0.2, 6, "되돌린 검색", hot=(6,))
            label(ax, 10.3, 0.2, "← 장부엔 없음", fs=10, ha="left", color=RED, bold=True)
    return draw


if __name__ == "__main__":
    S, L = (7.2, 3.6), (12, 6)
    one(block, "k8s13-block.svg", S, L)
    one(copy, "k8s13-copy.svg", S, L)
    one(film, "k8s13-film.svg", S, L)
    one(write, "k8s13-write.svg", S, L)
    one(read, "k8s13-read.svg", S, L)
    one(revert, "k8s13-revert.svg", S, L)
    one(backup, "k8s13-backup.svg", S, L)
    one(pair(False), "k8s13-order-wrong.svg", (7.6, 3.9), (12.6, 6.4))
    one(pair(True), "k8s13-order-right.svg", (7.6, 3.9), (12.6, 6.4))
