"""Elasticsearch 1편 그림 만들기. 실행: python lab/fig_es01.py  → docs/elasticsearch/img/01/*.svg"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "es"))
from figkit import (GREY, INK, LIGHT, NOTE, PAPER, PINK, RED, arrow, box, canvas, cell, cells,  # noqa: E402
                    label, outdir, save)

OUT = outdir("01")


def scan():
    rows = ["배송은 언제 오나요", "환불 요청합니다", "사이즈 교환 문의", "주문 취소했어요",
            "환불 언제 들어오나요", "색상이 달라요"]
    fig, ax = canvas(8.4, 4.6, 12, 6.6)
    label(ax, 0.3, 6.25, "posts 표", fs=12, ha="left", bold=True)
    cell(ax, 0.3, 5.45, 0.8, 0.6, "id", fc=PAPER); cell(ax, 1.1, 5.45, 5.0, 0.6, "body", fc=PAPER)
    for k, r in enumerate(rows):
        y = 4.75 - k * 0.7
        hot = "환불" in r
        cell(ax, 0.3, y, 0.8, 0.6, k + 1, hot=hot); cell(ax, 1.1, y, 5.0, 0.6, r, hot=hot)
    label(ax, 3.6, 0.55, "⋮  (글이 백만 개)", fs=12, color=INK)
    for k in range(5):
        y = 4.75 - k * 0.7 + 0.3
        arrow(ax, (6.4, y), (6.4, y - 0.62), color=RED, lw=1.6, ms=12)
    label(ax, 6.75, 4.0, "1번 글부터\n한 줄씩 다 읽어요", fs=12, ha="left", color=RED)
    box(ax, 6.7, 1.0, 5.1, 1.1, fc=NOTE)
    label(ax, 9.25, 1.55, "WHERE body LIKE '%환불%'", fs=12)
    save(fig, OUT, "es01-scan.svg")


def map_():
    steps = ["한 줄씩\n다 보기", "글마다\n낱말 목록", "뒤집기:\n낱말마다 글 목록", "목록 꺼내서\n합치기"]
    fig, ax = canvas(10, 2.3, 16, 3)
    for k, s in enumerate(steps):
        x = 0.3 + k * 4.0
        box(ax, x, 0.6, 3.1, 1.8, fc=PINK if k == 2 else NOTE, ec=RED if k == 2 else INK)
        label(ax, x + 1.55, 1.5, s, fs=12, color=RED if k == 2 else "#222")
        label(ax, x + 0.25, 2.15, str(k + 1), fs=10, color=INK, ha="left")
        if k < 3:
            arrow(ax, (x + 3.2, 1.5), (x + 3.9, 1.5))
    save(fig, OUT, "es01-map.svg")


DOCS = {1: ["주문", "환불", "요청"], 2: ["주문", "배송", "언제"], 3: ["환불", "완료", "감사"]}


def flip():
    fig, ax = canvas(10, 5.0, 15, 7.9)
    label(ax, 2.6, 6.8, "글마다 낱말 목록", fs=13, bold=True)
    for k, (d, ws) in enumerate(DOCS.items()):
        y = 5.4 - k * 1.3
        cell(ax, 0.3, y, 1.0, 0.8, f"글 {d}", fc=PAPER)
        cells(ax, 1.5, y, ws, w=1.1, hot=[i for i, w in enumerate(ws) if w == "환불"])
    arrow(ax, (5.3, 3.8), (6.9, 3.8), lw=3, ms=26, color=RED)
    label(ax, 6.1, 4.4, "뒤집기", fs=13, color=RED, bold=True)

    inv = {}
    for d, ws in DOCS.items():
        for w in ws:
            inv.setdefault(w, []).append(d)
    terms = sorted(inv)
    label(ax, 10.0, 7.55, "낱말마다 글 목록 (역색인)", fs=13, bold=True)
    for k, t in enumerate(terms):
        y = 6.05 - k * 0.78
        hot = t == "환불"
        cell(ax, 7.6, y, 1.3, 0.66, t, hot=hot)
        arrow(ax, (9.0, y + 0.33), (9.6, y + 0.33), lw=1.4, ms=10, color=RED if hot else INK)
        cells(ax, 9.7, y, inv[t], w=0.7, h=0.66, hot=range(len(inv[t])) if hot else ())
    label(ax, 8.25, 6.85, "용어 사전 (가나다순)", fs=10, color=INK)
    label(ax, 11.6, 6.85, "포스팅 목록 (글 번호순)", fs=10, color=INK)
    save(fig, OUT, "es01-flip.svg")


def lookup():
    terms = ["감사", "배송", "언제", "완료", "요청", "주문", "환불"]
    fig, ax = canvas(10, 3.6, 15, 5.2)
    cells(ax, 0.3, 3.2, terms, w=1.3, h=0.8, hot=(6,))
    # 이진 탐색: 가운데(완료) → 남은 반의 가운데(주문) → 환불
    for n, i in enumerate((3, 5, 6)):
        x = 0.3 + i * 1.38 + 0.65
        hot = i == 6
        arrow(ax, (x, 2.0), (x, 3.1), color=RED if hot else INK, lw=1.6, ms=12)
        label(ax, x, 1.55, f"{'①②③'[n]} {terms[i]}", fs=11, color=RED if hot else INK, bold=hot)
    label(ax, 0.3 + 3 * 1.38 + 0.65, 0.95, "가나다순이라 볼 때마다 반씩 버려요", fs=11, color=INK)
    x_end = 0.3 + 6 * 1.38 + 1.3
    arrow(ax, (x_end + 0.1, 3.6), (x_end + 1.0, 3.6), color=RED)
    cells(ax, x_end + 1.1, 3.2, [1, 3], w=0.8, h=0.8, hot=(0, 1))
    label(ax, x_end + 1.95, 2.7, "글 1, 3", fs=11, color=RED)
    save(fig, OUT, "es01-lookup.svg")


def and_():
    a = [2, 5, 9, 14, 20]
    b = [1, 5, 8, 14, 21, 30]
    fig, ax = canvas(10, 3.4, 15, 4.6)
    label(ax, 0.3, 3.55, "환불", fs=12, ha="left", bold=True)
    label(ax, 0.3, 1.55, "주문", fs=12, ha="left", bold=True)
    cells(ax, 1.6, 3.15, a, w=1.0, h=0.8, hot=(1, 3))
    cells(ax, 1.6, 1.15, b, w=1.0, h=0.8, hot=(1, 3))
    for x0 in (1.6 + 1 * 1.08 + 0.5, 1.6 + 3 * 1.08 + 0.5):
        ax.plot([x0, x0], [2.0, 3.1], color=RED, lw=2)
    label(ax, 8.4, 2.55, "둘 다 있는 글: 5, 14", fs=12, color=RED, ha="left", bold=True)
    label(ax, 8.4, 0.5, "작은 번호 쪽을 한 칸씩 앞으로.\n두 목록을 한 번씩만 훑어요.", fs=11, ha="left", color=INK)
    save(fig, OUT, "es01-and.svg")


if __name__ == "__main__":
    scan(); map_(); flip(); lookup(); and_()
