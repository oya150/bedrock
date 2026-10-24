"""Elasticsearch 7편 그림 만들기. 실행: python lab/fig_es07.py  → docs/elasticsearch/img/07/*.svg"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "es"))
from figkit import (GREY, INK, LIGHT, NOTE, PAPER, PINK, RED, arrow, box, canvas, cell, cells,  # noqa: E402
                    label, outdir, save)
from matplotlib.patches import Rectangle  # noqa: E402

OUT = outdir("07")


def open_():
    fig, ax = canvas(10, 2.8, 16, 4.2)
    label(ax, 0.3, 3.5, "검색어: 환불 신청 (둘 다 든 문서)", fs=12, ha="left", bold=True)
    label(ax, 0.3, 2.45, "환불", fs=11, ha="left")
    ax.add_patch(Rectangle((1.6, 2.2), 0.5, 0.5, fc=PINK, ec=RED, lw=1.5))
    label(ax, 2.3, 2.45, "문서 1천 개", fs=10, ha="left", color=RED)
    label(ax, 0.3, 1.25, "신청", fs=11, ha="left")
    ax.add_patch(Rectangle((1.6, 1.0), 13.5, 0.5, fc=NOTE, ec=INK, lw=1.2))
    label(ax, 8.35, 1.25, "문서 100만 개", fs=10, color=INK)
    label(ax, 8.0, 0.3, "긴 목록을 처음부터 끝까지 걸어야 할까요?", fs=11, color=INK)
    save(fig, OUT, "es07-open.svg")


def map_():
    steps = ["두 손가락은\n긴 목록을 다 걸어요", "짧은 목록이\n앞장서요", "건너뛰기 표로\n껑충", "ES에서\n세어 보기", "OR와 구문 검색은\n다르게"]
    fig, ax = canvas(11, 2.2, 20, 3)
    for k, s in enumerate(steps):
        x = 0.2 + k * 4.0
        hot = k == 2
        box(ax, x, 0.6, 3.2, 1.8, fc=PINK if hot else NOTE, ec=RED if hot else INK)
        label(ax, x + 1.6, 1.5, s, fs=11, color=RED if hot else "#222")
        label(ax, x + 0.22, 2.15, str(k + 1), fs=10, color=INK, ha="left")
        if k < 4:
            arrow(ax, (x + 3.3, 1.5), (x + 3.9, 1.5), ms=14)
    save(fig, OUT, "es07-map.svg")


def leap():
    fig, ax = canvas(11, 5.0, 18, 8.0)
    label(ax, 0.3, 7.5, "짧은 목록(환불): 5, 70, 77", fs=12, ha="left", bold=True)
    cells(ax, 6.2, 7.1, [5, 70, 77], w=0.9, h=0.7, hot=(1,))
    label(ax, 0.3, 6.1, "건너뛰기 표(묶음마다 마지막 번호)", fs=11, ha="left", color=INK)
    blocks = [(0, 12), (13, 31), (32, 47), (48, 66), (67, 80), (81, 99)]
    W = 2.75
    for k, (a, b) in enumerate(blocks):
        x = 0.3 + k * W
        hot = k == 4
        seen = k <= 4
        cell(ax, x + 0.6, 5.0, 1.4, 0.7, b, hot=hot, fc=None if seen else LIGHT, fs=11)
    label(ax, 0.3, 3.85, "긴 목록(신청): 묶음 여섯 개", fs=11, ha="left", color=INK)
    for k, (a, b) in enumerate(blocks):
        x = 0.3 + k * W
        hot = k == 4
        box(ax, x, 1.6, W - 0.25, 1.9, fc=PINK if hot else (NOTE if k == 0 else LIGHT), ec=RED if hot else (INK if k == 0 else GREY), round_=False)
        label(ax, x + (W - 0.25) / 2, 2.85, f"묶음 {k + 1}", fs=10, color=RED if hot else (INK if k == 0 else GREY))
        label(ax, x + (W - 0.25) / 2, 2.2, f"{a} … {b}", fs=10, color=RED if hot else (INK if k == 0 else GREY))
    arrow(ax, (0.3 + 3 * W + 1.3, 4.95), (0.3 + 4 * W + 1.3, 4.95), color=RED, rad=-0.4)
    label(ax, 0.3 + 3.5 * W + 1.3, 6.2, "31, 47, 66 < 70: 넘어가요", fs=10, color=RED)
    arrow(ax, (0.3 + 4 * W + 1.3, 4.9), (0.3 + 4 * W + 1.3, 3.6), color=RED)
    label(ax, 0.3 + 4 * W + 1.5, 4.25, "80 ≥ 70: 이 묶음만 풀어요", fs=10, color=RED, ha="left")
    label(ax, 9.0, 0.8, "advance(70): 묶음 2~4는 풀지도 않고 지나가요 (회색)", fs=11, color=INK)
    save(fig, OUT, "es07-leap.svg")


def orheap():
    fig, ax = canvas(11, 4.4, 18, 7.0)
    label(ax, 0.3, 6.5, "환불 OR 교환 OR 반품: 목록마다 지금 손가락이 가리키는 번호", fs=12, ha="left", bold=True)
    rows = [("환불", [3, 9, 14]), ("교환", [5, 9, 21]), ("반품", [8, 30])]
    for k, (t, ids) in enumerate(rows):
        y = 5.2 - k * 1.1
        label(ax, 0.3, y + 0.35, t, fs=11, ha="left")
        cells(ax, 1.6, y, ids, w=0.9, h=0.7, hot=(0,) if t == "환불" else ())
        ax.plot([1.6, 2.5], [y - 0.12, y - 0.12], color=RED if t == "환불" else INK, lw=2)
    # heap
    box(ax, 7.0, 1.0, 6.0, 5.0, fc=NOTE)
    label(ax, 10.0, 5.6, "힙: 손가락 번호 중 가장 작은 것이 맨 위", fs=11)
    cell(ax, 9.5, 4.2, 1.0, 0.75, 3, hot=True)
    cell(ax, 8.2, 2.7, 1.0, 0.75, 5)
    cell(ax, 10.8, 2.7, 1.0, 0.75, 8)
    ax.plot([9.9, 8.8], [4.2, 3.45], color=INK, lw=1.2); ax.plot([10.1, 11.2], [4.2, 3.45], color=INK, lw=1.2)
    arrow(ax, (10.6, 4.6), (14.0, 4.6), color=RED)
    label(ax, 15.6, 4.6, "다음 결과: 문서 3", fs=11, color=RED, ha="center")
    label(ax, 15.6, 3.2, "꺼낸 목록은 손가락을\n한 칸 옮겨 힙에 다시 넣어요", fs=10, color=INK, ha="center")
    label(ax, 10.0, 1.5, "알고리즘 10편의 힙", fs=10, color=INK)
    save(fig, OUT, "es07-or.svg")


if __name__ == "__main__":
    open_(); map_(); leap(); orheap()
