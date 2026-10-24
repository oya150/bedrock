"""Elasticsearch 8편 그림 만들기. 실행: python lab/fig_es08.py  → docs/elasticsearch/img/08/*.svg"""
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "es"))
from figkit import (BLUE, GREY, INK, LIGHT, NOTE, PAPER, PINK, RED, arrow, box, canvas, cell, cells,  # noqa: E402
                    label, outdir, plt, save)

OUT = outdir("08")
K1, B = 1.2, 0.75


def open_():
    fig, ax = canvas(10, 3.2, 16, 4.8)
    for k, (env, note, order) in enumerate((("배송 문의가 많은 때", "배송 언제 와요 ×30", ["환불 환불 문의", "배송 지연 문의"]),
                                            ("환불 문의가 많은 때", "환불 언제 돼요 ×30", ["배송 지연 문의", "환불 환불 문의"]))):
        x = 0.4 + k * 8.0
        box(ax, x, 0.4, 7.0, 3.6, fc=NOTE)
        label(ax, x + 3.5, 3.6, env, fs=12, bold=True)
        label(ax, x + 3.5, 3.05, note, fs=10, color=INK)
        for r, t in enumerate(order):
            hot = t.startswith("환불")
            label(ax, x + 0.5, 2.2 - r * 0.9, f"{r + 1}위", fs=11, ha="left", color=RED if hot else "#222")
            cell(ax, x + 1.5, 1.85 - r * 0.9, 4.8, 0.7, t, hot=hot, fs=11)
    label(ax, 8.0, 0.05, "검색어 \"환불 배송\", 두 문서는 그대로인데 순위가 뒤집혀요", fs=11, color=INK)
    save(fig, OUT, "es08-open.svg")


def map_():
    steps = ["점수는 낱말마다\n곱해서 더해요", "많이 나올수록,\n하지만 금방 배불러요", "드문 낱말일수록\n무거워요", "짧은 문서가\n유리해요", "통계는\n샤드마다 따로"]
    fig, ax = canvas(11, 2.2, 20, 3)
    for k, s in enumerate(steps):
        x = 0.2 + k * 4.0
        hot = k == 2
        box(ax, x, 0.6, 3.2, 1.8, fc=PINK if hot else NOTE, ec=RED if hot else INK)
        label(ax, x + 1.6, 1.5, s, fs=10.5, color=RED if hot else "#222")
        label(ax, x + 0.22, 2.15, str(k + 1), fs=10, color=INK, ha="left")
        if k < 4:
            arrow(ax, (x + 3.3, 1.5), (x + 3.9, 1.5), ms=14)
    save(fig, OUT, "es08-map.svg")


def tf():
    fig, ax = plt.subplots(figsize=(8, 3.6))
    fs = list(range(0, 21))
    ax.plot(fs, [f / 20 for f in fs], color=GREY, lw=2, ls="--")
    ax.plot(fs, [f / (f + K1) for f in fs], color=RED, lw=2.5)
    ax.text(14, 0.62, "그냥 횟수였다면(20번에 맞춰 줄임)", color=INK, fontsize=10)
    ax.text(9, 0.95, "BM25: 1에 가까워질 뿐 넘지 않아요", color=RED, fontsize=11)
    for f in (1, 2, 5):
        v = f / (f + K1)
        ax.plot([f], [v], "o", color=RED)
        ax.text(f + 0.3, v - 0.07, f"{f}번: {v:.2f}", color=RED, fontsize=10)
    ax.set_xlabel("문서 안에서 낱말이 나온 횟수 (문서 길이가 평균일 때)"); ax.set_ylabel("횟수 몫")
    ax.set_ylim(0, 1.05); ax.set_xlim(0, 20)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    save(fig, OUT, "es08-tf.svg")


def idf():
    fig, ax = plt.subplots(figsize=(8, 3.6))
    N = 52
    ns = list(range(1, N + 1))
    ax.plot(ns, [math.log(1 + (N - n + 0.5) / (n + 0.5)) for n in ns], color=BLUE, lw=2.5)
    for n, t in ((1, "환불이 1개 문서에만"), (31, "환불이 31개 문서에")):
        v = math.log(1 + (N - n + 0.5) / (n + 0.5))
        t = f"{t}: {v:.2f}"
        ax.plot([n], [v], "o", color=RED)
        ax.text(n + 1.0, v + 0.12, t, color=RED, fontsize=10)
    ax.set_xlabel("낱말이 든 문서 수 (전체 52개 중)"); ax.set_ylabel("IDF")
    ax.set_xlim(0, 53); ax.set_ylim(0, 4)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    save(fig, OUT, "es08-idf.svg")


def shards():
    fig, ax = canvas(10.5, 4.0, 17, 6.4)
    for k, (title, filler, score) in enumerate((("샤드 A", "환불 언제 돼요 ×40", "0.014"), ("샤드 B", "상품 문의 드려요 ×40", "3.848"))):
        x = 0.4 + k * 6.0
        box(ax, x, 1.8, 5.4, 3.8, fc=NOTE)
        label(ax, x + 2.7, 5.2, title, fs=12, bold=True)
        cell(ax, x + 0.5, 3.8, 4.4, 0.8, "환불 문의", hot=True, fs=11)
        label(ax, x + 2.7, 2.7, filler, fs=10, color=INK)
        label(ax, x + 2.7, 1.2, f"점수 {score}", fs=12, color=RED, bold=True)
    box(ax, 12.8, 2.2, 3.9, 3.0, fc=PINK, ec=RED)
    label(ax, 14.75, 4.6, "dfs_query_then_fetch", fs=10, color=RED, bold=True)
    label(ax, 14.75, 3.6, "두 샤드 통계를\n먼저 모아서", fs=10, color=INK)
    label(ax, 14.75, 2.6, "둘 다 0.773", fs=12, color=RED, bold=True)
    label(ax, 6.2, 0.3, "똑같은 글인데 샤드마다 '환불이 드문가'가 달라서 점수가 달라요", fs=11, color=INK)
    save(fig, OUT, "es08-shards.svg")


if __name__ == "__main__":
    open_(); map_(); tf(); idf(); shards()
