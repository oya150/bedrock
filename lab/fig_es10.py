"""Elasticsearch 10편 그림 만들기. 실행: python lab/fig_es10.py  → docs/elasticsearch/img/10/*.svg"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "es"))
from figkit import (GREY, INK, LIGHT, NOTE, PAPER, PINK, RED, arrow, box, canvas, cell, cells,  # noqa: E402
                    label, outdir, save)

OUT = outdir("10")


def open_():
    fig, ax = canvas(10, 3.0, 16, 4.6)
    box(ax, 0.4, 2.4, 7.2, 1.7, fc=PAPER)
    label(ax, 0.8, 3.7, '"sort": [{"title": "asc"}]', fs=11, ha="left", family="monospace")
    label(ax, 0.8, 2.9, "→ Text fields are not optimised…", fs=10, ha="left", color=RED)
    box(ax, 8.4, 2.4, 7.2, 1.7, fc=PAPER)
    label(ax, 8.8, 3.7, '"sort": [{"order_no_kw": "asc"}]', fs=11, ha="left", family="monospace")
    label(ax, 8.8, 2.9, '→ "10", "100", "25", "3", "9"', fs=11, ha="left", color=RED)
    label(ax, 4.0, 1.6, "제목으로는 정렬이 안 돼요", fs=11, color=INK)
    label(ax, 12.0, 1.6, "주문번호가 3보다 10이 먼저예요", fs=11, color=INK)
    save(fig, OUT, "es10-open.svg")


def map_():
    steps = ["역색인은\n방향이 반대", "뒤집어 쓰기는\n비싸요", "미리 열로\n적어 둬요", "문자열은\n순번으로", "숫자는\n숫자 필드에"]
    fig, ax = canvas(11, 2.2, 20, 3)
    for k, s in enumerate(steps):
        x = 0.2 + k * 4.0
        hot = k == 2
        box(ax, x, 0.6, 3.2, 1.8, fc=PINK if hot else NOTE, ec=RED if hot else INK)
        label(ax, x + 1.6, 1.5, s, fs=11, color=RED if hot else "#222")
        label(ax, x + 0.22, 2.15, str(k + 1), fs=10, color=INK, ha="left")
        if k < 4:
            arrow(ax, (x + 3.3, 1.5), (x + 3.9, 1.5), ms=14)
    save(fig, OUT, "es10-map.svg")


def direction():
    fig, ax = canvas(11, 4.4, 18, 7.0)
    label(ax, 0.3, 6.6, "역색인: 값 → 문서", fs=12, ha="left", bold=True)
    rows = [("나이키", [1, 4, 7]), ("아디다스", [2, 5]), ("푸마", [3, 6])]
    for k, (b, ds) in enumerate(rows):
        y = 5.5 - k * 1.0
        hot = 7 in ds
        cell(ax, 0.3, y, 1.8, 0.75, b, fs=11)
        arrow(ax, (2.2, y + 0.37), (2.8, y + 0.37), lw=1.2, ms=10)
        cells(ax, 2.9, y, ds, w=0.75, h=0.75, hot=[ds.index(7)] if hot else (), fs=11)
    label(ax, 3.2, 2.2, "문서 7의 브랜드는?\n→ 목록을 다 뒤져야 알아요", fs=11, color=RED)
    ax.plot([8.4, 8.4], [0.5, 6.8], color=GREY, lw=1.2, ls="--")
    label(ax, 9.0, 6.6, "doc values: 문서 → 값 (열 하나)", fs=12, ha="left", bold=True)
    vals = ["나이키", "아디다스", "푸마", "나이키", "아디다스", "푸마", "나이키"]
    for d, v in enumerate(vals, start=1):
        y = 6.0 - d * 0.72
        hot = d == 7
        cell(ax, 9.0, y, 1.0, 0.62, f"문서 {d}", fs=9, fc=PAPER)
        cell(ax, 10.1, y, 2.2, 0.62, v, hot=hot, fs=10)
    label(ax, 14.6, 1.3, "문서 번호로\n바로 읽어요", fs=11, color=RED, ha="left")
    save(fig, OUT, "es10-direction.svg")


def ordinals():
    fig, ax = canvas(11, 4.0, 18, 6.4)
    label(ax, 0.3, 6.0, "값 사전 (글자 순서, 한 번씩)", fs=12, ha="left", bold=True)
    for k, v in enumerate(["나이키", "아디다스", "푸마"]):
        cell(ax, 0.3, 4.6 - k * 0.9, 0.9, 0.75, k, fc=PAPER, fs=11)
        cell(ax, 1.3, 4.6 - k * 0.9, 2.2, 0.75, v, fs=11)
    label(ax, 1.9, 1.7, "순번 → 값", fs=10, color=INK)
    label(ax, 6.0, 6.0, "문서마다 순번(ordinal)만 적은 열", fs=12, ha="left", bold=True)
    ords = [0, 1, 2, 0, 1, 2, 0]
    for d, o in enumerate(ords, start=1):
        x = 6.0 + (d - 1) * 1.6
        cell(ax, x, 4.9, 1.4, 0.6, f"문서 {d}", fc=PAPER, fs=9)
        cell(ax, x, 4.1, 1.4, 0.75, o, hot=True, fs=12)
    label(ax, 11.5, 3.0, "정렬: 순번(작은 정수)끼리 비교 = 이름순", fs=11, color=RED)
    label(ax, 11.5, 2.2, "집계: 순번마다 칸 하나에 세기", fs=11, color=RED)
    label(ax, 11.5, 1.2, "값이 문서 수만큼 반복돼도 글자는 사전에 한 번만", fs=11, color=INK)
    save(fig, OUT, "es10-ordinals.svg")


def kwsort():
    fig, ax = canvas(10, 2.8, 16, 4.2)
    label(ax, 0.3, 3.6, "keyword(글자)로 정렬", fs=12, ha="left", bold=True)
    cells(ax, 4.6, 3.2, ['"10"', '"100"', '"25"', '"3"', '"9"'], w=1.6, h=0.75, hot=(0, 1), fs=11)
    label(ax, 0.3, 1.9, "long(숫자)으로 정렬", fs=12, ha="left", bold=True)
    cells(ax, 4.6, 1.5, [3, 9, 10, 25, 100], w=1.6, h=0.75, fs=11)
    label(ax, 8.0, 0.5, "글자는 첫 글자부터 비교해서 \"1…\"이 \"3\"보다 앞서요", fs=11, color=INK)
    save(fig, OUT, "es10-kwsort.svg")


if __name__ == "__main__":
    open_(); map_(); direction(); ordinals(); kwsort()
