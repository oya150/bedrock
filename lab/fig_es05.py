"""Elasticsearch 5편 그림 만들기. 실행: python lab/fig_es05.py  → docs/elasticsearch/img/05/*.svg"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "es"))
from figkit import (GREY, INK, LIGHT, NOTE, PAPER, PINK, RED, arrow, box, canvas, cell, cells,  # noqa: E402
                    label, outdir, save)
from matplotlib.patches import Rectangle  # noqa: E402

OUT = outdir("05")


def open_():
    fig, ax = canvas(9, 3.4, 13, 5.0)
    for k, (t, n, h) in enumerate((("지우기 전", "문서 300개", 3.0), ("100개 지운 뒤", "문서 200개", 3.0))):
        x = 1.5 + k * 5.0
        ax.add_patch(Rectangle((x, 0.8), 1.6, h, fc=NOTE if k == 0 else PINK, ec=RED if k else INK, lw=1.6))
        label(ax, x + 0.8, 0.4, t, fs=11)
        label(ax, x + 0.8, h + 1.1, n, fs=11, color=RED if k else "#222")
        label(ax, x + 0.8, 2.3, "20.7 kb", fs=10, color=RED if k else INK)
    arrow(ax, (3.4, 2.3), (6.2, 2.3))
    label(ax, 10.0, 2.3, "디스크는\n그대로예요", fs=12, color=RED, ha="left", bold=True)
    save(fig, OUT, "es05-open.svg")


def map_():
    steps = ["세그먼트는\n못 고쳐요", "지우기는\n표시만", "고치기는\n지우고 새로 넣기", "병합 때\n실제로 빠져요", "강제 병합의\n함정"]
    fig, ax = canvas(11, 2.2, 20, 3)
    for k, s in enumerate(steps):
        x = 0.2 + k * 4.0
        hot = k == 3
        box(ax, x, 0.6, 3.2, 1.8, fc=PINK if hot else NOTE, ec=RED if hot else INK)
        label(ax, x + 1.6, 1.5, s, fs=11, color=RED if hot else "#222")
        label(ax, x + 0.22, 2.15, str(k + 1), fs=10, color=INK, ha="left")
        if k < 4:
            arrow(ax, (x + 3.3, 1.5), (x + 3.9, 1.5), ms=14)
    save(fig, OUT, "es05-map.svg")


def livedocs():
    fig, ax = canvas(10, 3.6, 15, 5.4)
    label(ax, 0.3, 5.0, "세그먼트 _0", fs=12, ha="left", bold=True)
    label(ax, 0.3, 4.05, "문서", fs=11, ha="left", color=INK)
    label(ax, 0.3, 2.85, "살아 있나", fs=11, ha="left", color=INK)
    dead = {2, 4}
    for i in range(6):
        x = 2.4 + i * 1.3
        cell(ax, x, 3.7, 1.1, 0.75, f"문서 {i+1}", fs=10, dim=i in dead)
        if i in dead:
            ax.plot([x, x + 1.1], [3.7, 4.45], color=GREY, lw=1.5)
        cell(ax, x, 2.5, 1.1, 0.75, 0 if i in dead else 1, hot=i in dead, fs=12)
    label(ax, 10.5, 2.85, "← 지우면 이 칸만 0으로", fs=11, color=RED, ha="left")
    label(ax, 7.5, 1.4, "역색인과 문서는 그대로 두고, 검색할 때 0인 문서를 건너뛰어요", fs=11, color=INK)
    label(ax, 7.5, 0.6, "자리도 차지하고 doc_freq에도 그대로 세어져요", fs=11, color=INK)
    save(fig, OUT, "es05-livedocs.svg")


def update():
    fig, ax = canvas(10, 3.2, 15, 4.8)
    box(ax, 0.3, 1.6, 6.2, 2.4, fc=NOTE)
    label(ax, 0.6, 3.6, "세그먼트 _1 (옛것)", fs=11, ha="left")
    cell(ax, 0.8, 2.2, 2.5, 0.9, "101: 환불 문의", dim=True, fs=10)
    ax.plot([0.8, 3.3], [2.2, 3.1], color=GREY, lw=1.5)
    label(ax, 4.9, 2.65, "지웠다고\n표시", fs=10, color=RED)
    box(ax, 8.3, 1.6, 6.2, 2.4, fc=PINK, ec=RED)
    label(ax, 8.6, 3.6, "세그먼트 _3 (새로)", fs=11, ha="left", color=RED)
    cell(ax, 8.8, 2.2, 3.4, 0.9, "101: 환불 문의 수정", hot=True, fs=10)
    arrow(ax, (6.7, 2.65), (8.1, 2.65), color=RED)
    label(ax, 7.4, 0.8, "고치기 = 옛 문서에 지움 표시 + 새 문서를 새 세그먼트에", fs=11, color=INK)
    save(fig, OUT, "es05-update.svg")


def merge():
    fig, ax = canvas(10.5, 4.2, 16, 6.4)
    segs = [("_0", 6, {1, 3, 4}), ("_1", 6, {0}), ("_2", 6, set())]
    for k, (n, c, dead) in enumerate(segs):
        x = 0.3 + k * 3.4
        box(ax, x, 3.7, 3.1, 2.0, fc=NOTE)
        label(ax, x + 1.55, 5.35, f"세그먼트 {n}", fs=11)
        for i in range(c):
            xx = x + 0.2 + (i % 3) * 0.95
            yy = 4.55 - (i // 3) * 0.7
            cell(ax, xx, yy, 0.8, 0.55, "", dim=i in dead, fc=None if i in dead else "white")
            if i in dead:
                ax.plot([xx, xx + 0.8], [yy, yy + 0.55], color=GREY, lw=1.2)
    for k in range(3):
        arrow(ax, (1.85 + k * 3.4, 3.6), (5.35, 2.35), lw=1.4, ms=12)
    label(ax, 7.9, 3.1, "병합", fs=12, color=RED, bold=True, ha="left")
    box(ax, 2.3, 0.3, 6.1, 1.9, fc=PINK, ec=RED)
    label(ax, 5.35, 1.9, "세그먼트 _3 (살아 있는 문서만 새로 씀)", fs=11, color=RED)
    for i in range(14):
        cell(ax, 2.55 + (i % 7) * 0.8, 0.95 - (i // 7) * 0.55, 0.7, 0.45, "", fc="white")
    label(ax, 10.6, 4.6, "지운 문서 4개는\n새 세그먼트에\n옮겨 적지 않아요", fs=11, color=RED, ha="left")
    label(ax, 10.6, 1.4, "옛 세그먼트 셋은\n검색이 다 끝나면 지워요", fs=11, color=INK, ha="left")
    save(fig, OUT, "es05-merge.svg")


if __name__ == "__main__":
    open_(); map_(); livedocs(); update(); merge()
