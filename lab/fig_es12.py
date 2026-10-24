"""Elasticsearch 12편 그림 만들기. 실행: python lab/fig_es12.py  → docs/elasticsearch/img/12/*.svg"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "es"))
from figkit import (BLUE, GREEN, GREY, INK, LIGHT, NOTE, PAPER, PINK, RED, YEL, arrow, box, canvas, cell, cells,  # noqa: E402
                    label, outdir, save)

OUT = outdir("12")


def open_():
    fig, ax = canvas(10, 2.8, 16, 4.2)
    box(ax, 0.3, 1.6, 7.2, 2.2, fc=PAPER)
    label(ax, 3.9, 3.4, "브랜드별 판매 1위", fs=12, bold=True)
    label(ax, 3.9, 2.6, "ES 응답: w 10건", fs=11, color=RED)
    label(ax, 3.9, 2.0, "실제: y 27건", fs=11, color=INK)
    box(ax, 8.4, 1.6, 7.2, 2.2, fc=PAPER)
    label(ax, 12.0, 3.4, "1,001쪽째 목록", fs=12, bold=True)
    label(ax, 12.0, 2.5, "Result window is too large…", fs=11, color=RED)
    label(ax, 8.0, 0.7, "샤드가 여럿일 때 결과를 합치는 방법에서 둘 다 나와요", fs=11, color=INK)
    save(fig, OUT, "es12-open.svg")


def map_():
    steps = ["검색은\n두 번 오가요", "조율 노드가\n위 10개를 합쳐요", "깊은 페이지는\n샤드마다 많이", "집계도\n샤드마다 위 몇 개", "오차 다루기"]
    fig, ax = canvas(11, 2.2, 20, 3)
    for k, s in enumerate(steps):
        x = 0.2 + k * 4.0
        hot = k == 3
        box(ax, x, 0.6, 3.2, 1.8, fc=PINK if hot else NOTE, ec=RED if hot else INK)
        label(ax, x + 1.6, 1.5, s, fs=11, color=RED if hot else "#222")
        label(ax, x + 0.22, 2.15, str(k + 1), fs=10, color=INK, ha="left")
        if k < 4:
            arrow(ax, (x + 3.3, 1.5), (x + 3.9, 1.5), ms=14)
    save(fig, OUT, "es12-map.svg")


def phases():
    fig, ax = canvas(11, 4.8, 18, 7.6)
    box(ax, 6.5, 6.0, 5.0, 1.1, fc=PINK, ec=RED)
    label(ax, 9.0, 6.55, "조율 노드", fs=12, color=RED, bold=True)
    for k in range(3):
        x = 0.8 + k * 6.0
        box(ax, x, 1.0, 4.4, 2.4, fc=NOTE)
        label(ax, x + 2.2, 3.0, f"샤드 {k}", fs=12, bold=True)
        label(ax, x + 2.2, 2.3, "위 10개: 번호·점수만", fs=10, color=INK)
        label(ax, x + 2.2, 1.6, "뽑힌 문서: 원문", fs=10, color=INK)
        arrow(ax, (9.0, 5.9), (x + 2.2, 3.5), color=INK, lw=1.4, ms=12, rad=0.0)
    label(ax, 1.0, 5.2, "① query: 각 샤드가 자기 위 10개의\n번호와 점수만 보내요", fs=10.5, ha="left", color=INK)
    label(ax, 12.3, 5.2, "② 조율 노드가 30개를 합쳐 위 10개를 고르고\nfetch: 그 10개의 원문만 해당 샤드에 받아 와요", fs=10.5, ha="left", color=RED)
    label(ax, 9.0, 0.4, "원문(_source)은 최종 10개만 오가요", fs=11, color=INK)
    save(fig, OUT, "es12-phases.svg")


def deep():
    fig, ax = canvas(10.5, 3.8, 17, 6.0)
    label(ax, 0.3, 5.5, "1,000쪽째(from 9990, size 10)를 보려면", fs=12, ha="left", bold=True)
    for k in range(3):
        x = 0.5 + k * 4.0
        box(ax, x, 2.2, 3.4, 2.4, fc=NOTE)
        label(ax, x + 1.7, 4.15, f"샤드 {k}", fs=11, bold=True)
        label(ax, x + 1.7, 3.2, "위 10,000개를\n골라 보내요", fs=10, color=RED)
    arrow(ax, (12.4, 3.4), (13.4, 3.4))
    box(ax, 13.5, 2.2, 3.2, 2.4, fc=PINK, ec=RED)
    label(ax, 15.1, 3.75, "조율 노드", fs=11, color=RED, bold=True)
    label(ax, 15.1, 2.9, "30,000개 합쳐\n10개만 씀", fs=10, color=RED)
    label(ax, 8.5, 1.1, "쪽이 깊어질수록 샤드마다 보내는 수가 늘어요. 그래서 기본 상한이 1만이에요", fs=11, color=INK)
    save(fig, OUT, "es12-deep.svg")


def terms():
    fig, ax = canvas(11, 4.6, 18, 7.2)
    data = [("샤드 0", [("x", 10), ("y", 9)]), ("샤드 1", [("z", 10), ("y", 9)]), ("샤드 2", [("w", 10), ("y", 9)])]
    for k, (name, rows) in enumerate(data):
        x = 0.4 + k * 4.2
        box(ax, x, 3.3, 3.8, 3.2, fc=NOTE)
        label(ax, x + 1.9, 6.1, name, fs=12, bold=True)
        for r, (b, c) in enumerate(rows):
            sent = r == 0
            cell(ax, x + 0.4, 5.0 - r * 1.0, 3.0, 0.75, f"{b}: {c}건", hot=sent, dim=not sent, fs=11)
        label(ax, x + 1.9, 3.55, "1위만 보내요", fs=10, color=RED)
    arrow(ax, (12.9, 4.9), (13.6, 4.9))
    box(ax, 13.7, 3.3, 4.0, 3.2, fc=PINK, ec=RED)
    label(ax, 15.7, 6.1, "합친 결과", fs=12, color=RED, bold=True)
    label(ax, 15.7, 5.1, "x 10 · z 10 · w 10", fs=11, color=RED)
    label(ax, 15.7, 4.2, "→ 1위 w 10건", fs=11, color=RED, bold=True)
    label(ax, 9.0, 2.4, "y는 모든 샤드에서 2위라 한 번도 안 올라왔어요. 실제 합계는 9 × 3 = 27건으로 1위", fs=11, color=INK)
    label(ax, 9.0, 1.4, "샤드마다 위 몇 개를 더 보내면(shard_size) 맞아져요", fs=11, color=INK)
    save(fig, OUT, "es12-terms.svg")


if __name__ == "__main__":
    open_(); map_(); phases(); deep(); terms()
