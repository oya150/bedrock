"""Elasticsearch 11편 그림 만들기. 실행: python lab/fig_es11.py  → docs/elasticsearch/img/11/*.svg"""
import os
import random
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "es"))
from figkit import (BLUE, GREEN, GREY, INK, LIGHT, NOTE, PAPER, PINK, RED, arrow, box, canvas, cell, cells,  # noqa: E402
                    label, outdir, plt, save)
from matplotlib.patches import Rectangle  # noqa: E402

OUT = outdir("11")


def open_():
    fig, ax = canvas(10, 2.8, 16, 4.2)
    label(ax, 0.3, 3.6, "가격 10 이상 25 이하", fs=12, ha="left", bold=True)
    label(ax, 0.3, 2.5, "long 필드", fs=11, ha="left")
    cells(ax, 3.8, 2.15, [10, 25], w=1.3, h=0.7, fs=11)
    label(ax, 0.3, 1.2, "keyword 필드", fs=11, ha="left")
    cells(ax, 3.8, 0.85, ["10", "25", "100", "2000"], w=1.3, h=0.7, fs=11, hot=(2, 3))
    label(ax, 9.6, 1.2, "\"100\"과 \"2000\"도 글자 순서로는\n\"10\"과 \"25\" 사이예요", fs=11, color=RED, ha="left")
    save(fig, OUT, "es11-open.svg")


def map_():
    steps = ["값마다 목록은\n범위에 약해요", "값 순서로\n잎 칸에 담기", "칸마다\n값 범위", "안·걸침·밖으로\n나눠 보기", "여러 차원도\n같은 방법"]
    fig, ax = canvas(11, 2.2, 20, 3)
    for k, s in enumerate(steps):
        x = 0.2 + k * 4.0
        hot = k == 3
        box(ax, x, 0.6, 3.2, 1.8, fc=PINK if hot else NOTE, ec=RED if hot else INK)
        label(ax, x + 1.6, 1.5, s, fs=11, color=RED if hot else "#222")
        label(ax, x + 0.22, 2.15, str(k + 1), fs=10, color=INK, ha="left")
        if k < 4:
            arrow(ax, (x + 3.3, 1.5), (x + 3.9, 1.5), ms=14)
    save(fig, OUT, "es11-map.svg")


def leaves():
    fig, ax = canvas(11, 3.8, 18, 6.0)
    label(ax, 0.3, 5.6, "가격을 정렬해 잎 칸에 나눠 담고 칸마다 값 범위를 알아 둠", fs=12, ha="left", bold=True)
    bounds = [(100, 9_800), (9_900, 19_800), (19_900, 30_100), (30_200, 40_000), (40_100, 50_300), (50_400, 61_000), (61_100, 80_000)]
    LO, HI = 10_000, 50_000
    W = 2.4
    for k, (a, b) in enumerate(bounds):
        x = 0.4 + k * W
        if b < LO or a > HI:
            fc, ec, tag, col = LIGHT, GREY, "건너뜀", GREY
        elif LO <= a and b <= HI:
            fc, ec, tag, col = PINK, RED, "통째로 담기", RED
        else:
            fc, ec, tag, col = NOTE, INK, "하나씩 확인", INK
        box(ax, x, 2.4, W - 0.2, 1.6, fc=fc, ec=ec, round_=False)
        label(ax, x + (W - 0.2) / 2, 3.5, f"잎 칸 {k + 1}", fs=10, color=col)
        label(ax, x + (W - 0.2) / 2, 2.85, f"{a:,}~{b:,}", fs=8.5, color=col)
        label(ax, x + (W - 0.2) / 2, 1.9, tag, fs=10, color=col, bold=ec == RED)
    x1 = 0.4 + 1 * W - 0.1
    x2 = 0.4 + 5 * W - 0.1
    ax.plot([x1 + 0.2, x2 - 0.25], [1.1, 1.1], color=RED, lw=3)
    label(ax, (x1 + x2) / 2, 0.6, "찾는 범위: 10,000 ~ 50,000원", fs=11, color=RED)
    save(fig, OUT, "es11-leaves.svg")


def kd():
    random.seed(4)
    fig, ax = plt.subplots(figsize=(6.2, 5.2))
    pts = [(random.random(), random.random()) for _ in range(80)]
    ax.scatter([p[0] for p in pts], [p[1] for p in pts], s=12, color=INK, zorder=3)
    # k-d 나눔: 세로 → 가로 → 세로
    ax.plot([0.5, 0.5], [0, 1], color=BLUE, lw=2)
    ax.plot([0, 0.5], [0.45, 0.45], color=BLUE, lw=1.6)
    ax.plot([0.5, 1], [0.6, 0.6], color=BLUE, lw=1.6)
    for x, y0, y1 in ((0.25, 0, 0.45), (0.22, 0.45, 1), (0.75, 0, 0.6), (0.78, 0.6, 1)):
        ax.plot([x, x], [y0, y1], color=BLUE, lw=1.0, ls="--")
    ax.add_patch(Rectangle((0.56, 0.08), 0.33, 0.45, fc=PINK, ec=RED, lw=2, alpha=0.5, zorder=2))
    ax.text(0.725, 0.56, "찾는 네모", color=RED, ha="center", fontsize=11)
    ax.text(0.25, 0.97, "① 세로로 반", color=BLUE, fontsize=10, ha="center", va="top")
    ax.text(0.02, 0.47, "② 가로로 반", color=BLUE, fontsize=10)
    ax.text(0.04, 0.02, "왼쪽 절반은 네모와 안 겹치니 통째로 건너뛰어요", color=INK, fontsize=10)
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    ax.set_xticks([]); ax.set_yticks([])
    ax.set_xlabel("경도"); ax.set_ylabel("위도")
    save(fig, OUT, "es11-kd.svg")


if __name__ == "__main__":
    open_(); map_(); leaves(); kd()
