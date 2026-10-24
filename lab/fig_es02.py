"""Elasticsearch 2편 그림 만들기. 실행: python lab/fig_es02.py  → docs/elasticsearch/img/02/*.svg"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "es"))
from figkit import (GREY, INK, NOTE, PAPER, PINK, RED, arrow, box, canvas, cell, cells,  # noqa: E402
                    label, outdir, save)

OUT = outdir("02")


def miss():
    fig, ax = canvas(9, 3.6, 13, 5.2)
    label(ax, 0.3, 4.75, "글: 환불했어요", fs=12, ha="left", bold=True)
    label(ax, 0.3, 4.2, "띄어쓰기로 자르면", fs=11, ha="left", color=INK)
    cell(ax, 0.3, 3.0, 2.4, 0.8, "환불했어요")
    arrow(ax, (2.9, 3.4), (4.2, 3.4))
    label(ax, 6.0, 4.75, "용어 사전", fs=12, bold=True)
    for k, t in enumerate(["배송", "주문", "환불했어요"]):
        cell(ax, 4.6, 3.75 - k * 0.85, 2.6, 0.75, t)
    box(ax, 9.0, 3.0, 2.6, 1.0, fc=PINK, ec=RED)
    label(ax, 10.3, 3.5, "검색어: 환불", fs=12, color=RED, bold=True)
    arrow(ax, (8.9, 3.3), (7.35, 2.35), color=RED)
    label(ax, 9.6, 1.85, "글자가 다르니\n없는 낱말이에요", fs=11, color=RED, ha="left")
    label(ax, 6.0, 1.2, "사전에는 '환불했어요'만 있어요", fs=11, color=INK)
    save(fig, OUT, "es02-miss.svg")


def map_():
    steps = ["글자가 똑같아야\n찾아요", "분석기\n세 단계", "한국어는\n낱말 안쪽까지 자르기", "검색어도\n같은 길로", "한번 자르면\n바꾸기 어려워요"]
    fig, ax = canvas(11, 2.2, 20, 3)
    for k, s in enumerate(steps):
        x = 0.2 + k * 4.0
        hot = k == 1
        box(ax, x, 0.6, 3.2, 1.8, fc=PINK if hot else NOTE, ec=RED if hot else INK)
        label(ax, x + 1.6, 1.5, s, fs=11, color=RED if hot else "#222")
        label(ax, x + 0.22, 2.15, str(k + 1), fs=10, color=INK, ha="left")
        if k < 4:
            arrow(ax, (x + 3.3, 1.5), (x + 3.9, 1.5), ms=14)
    save(fig, OUT, "es02-map.svg")


def pipeline():
    fig, ax = canvas(11, 4.6, 20, 7.4)
    stages = ["문자 필터", "토크나이저", "토큰 필터"]
    xs = [3.6, 8.6, 13.6]
    for x, s in zip(xs, stages):
        box(ax, x, 5.3, 3.4, 1.1, fc=PAPER)
        label(ax, x + 1.7, 5.85, s, fs=12, bold=True)
    label(ax, 3.6 + 1.7, 4.8, "html_strip:\n태그 지우기", fs=10, color=INK, va="top")
    label(ax, 8.6 + 1.7, 4.8, "standard:\n띄어쓰기·문장부호로 자르기", fs=10, color=INK, va="top")
    label(ax, 13.6 + 1.7, 4.8, "lowercase:\n소문자로", fs=10, color=INK, va="top")
    for x in xs[:-1]:
        arrow(ax, (x + 3.5, 5.85), (x + 4.9, 5.85), ms=14)
    arrow(ax, (17.1, 5.85), (18.4, 5.85), ms=14)
    label(ax, 19.2, 5.85, "역색인", fs=12, bold=True)

    y = 2.4
    label(ax, 0.2, y + 1.15, "글", fs=12, ha="left", bold=True)
    cell(ax, 0.2, y, 3.0, 0.8, "<b>Refund</b> 요청", fs=10)
    cell(ax, 3.9, y, 2.6, 0.8, "Refund 요청", fs=11)
    cells(ax, 8.6, y, ["Refund", "요청"], w=1.5, h=0.8, fs=11)
    cells(ax, 13.6, y, ["refund", "요청"], w=1.5, h=0.8, fs=11, hot=(0,))
    y = 0.6
    label(ax, 0.2, y + 1.15, "검색어", fs=12, ha="left", bold=True)
    cell(ax, 0.2, y, 3.0, 0.8, "REFUND", fs=11)
    cell(ax, 3.9, y, 2.6, 0.8, "REFUND", fs=11)
    cells(ax, 8.6, y, ["REFUND"], w=1.5, h=0.8, fs=11)
    cells(ax, 13.6, y, ["refund"], w=1.5, h=0.8, fs=11, hot=(0,))
    label(ax, 17.4, 1.85, "같은 낱말이 돼서\n찾을 수 있어요", fs=11, color=RED, ha="left")
    save(fig, OUT, "es02-pipeline.svg")


def nori():
    fig, ax = canvas(10, 3.6, 15, 5.4)
    label(ax, 0.3, 4.85, "환불했어요", fs=13, ha="left", bold=True)
    parts = [("환불", "명사"), ("하", "접미사"), ("았", "어미"), ("어요", "어미")]
    x = 0.3
    for k, (m, pos) in enumerate(parts):
        hot = k == 0
        cell(ax, x, 3.2, 1.5, 0.85, m, hot=hot)
        label(ax, x + 0.75, 2.85, pos, fs=10, color=RED if hot else INK)
        x += 1.65
    label(ax, 3.6, 2.15, "① 형태소로 자르기 (했 = 하 + 았)", fs=11, color=INK)
    arrow(ax, (7.2, 3.6), (8.6, 3.6))
    cell(ax, 8.8, 3.2, 1.5, 0.85, "환불", hot=True)
    for k, m in enumerate(["하", "았", "어요"]):
        cell(ax, 10.5 + k * 1.05, 3.2, 0.95, 0.85, m, dim=True, fs=11)
        ax.plot([10.5 + k * 1.05, 11.45 + k * 1.05], [3.2, 4.05], color=GREY, lw=1.5)
    label(ax, 11.6, 2.15, "② 검색에 쓸모없는 품사 버리기", fs=11, color=INK)
    label(ax, 8.8, 1.2, "역색인에는 '환불'만 올라가요", fs=12, color=RED, ha="left", bold=True)
    save(fig, OUT, "es02-nori.svg")


def termmatch():
    fig, ax = canvas(10.5, 4.2, 16, 6.4)
    label(ax, 12.9, 5.95, "용어 사전", fs=12, bold=True)
    cell(ax, 11.6, 4.7, 2.6, 0.8, "refund", hot=False)
    cell(ax, 11.6, 3.8, 2.6, 0.8, "request")
    # match
    label(ax, 0.2, 4.95, "match", fs=12, ha="left", bold=True, color=RED)
    cell(ax, 1.8, 4.7, 1.8, 0.8, "Refund")
    arrow(ax, (3.7, 5.1), (4.6, 5.1), ms=14)
    box(ax, 4.7, 4.65, 2.6, 0.9, fc=PAPER)
    label(ax, 6.0, 5.1, "분석기", fs=11)
    arrow(ax, (7.4, 5.1), (8.3, 5.1), ms=14)
    cell(ax, 8.4, 4.7, 1.8, 0.8, "refund", hot=True)
    arrow(ax, (10.3, 5.1), (11.5, 5.1), color=RED, ms=14)
    label(ax, 14.5, 5.1, "1건", fs=12, color=RED, ha="left", bold=True)
    # term
    label(ax, 0.2, 2.15, "term", fs=12, ha="left", bold=True)
    cell(ax, 1.8, 1.9, 1.8, 0.8, "Refund")
    arrow(ax, (3.7, 2.3), (8.3, 2.3), ms=14)
    label(ax, 6.0, 2.75, "그대로", fs=11, color=INK)
    cell(ax, 8.4, 1.9, 1.8, 0.8, "Refund")
    arrow(ax, (10.3, 2.4), (11.5, 3.75), color=INK, ms=14)
    label(ax, 11.6, 2.0, "Refund ≠ refund\n0건", fs=12, ha="left", color=INK)
    save(fig, OUT, "es02-termmatch.svg")


if __name__ == "__main__":
    miss(); map_(); pipeline(); nori(); termmatch()
