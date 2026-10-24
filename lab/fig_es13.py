"""Elasticsearch 13편 그림 만들기. 실행: python lab/fig_es13.py  → docs/elasticsearch/img/13/*.svg"""
import math
import os
import random
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "es"))
from figkit import (BLUE, GREY, INK, LIGHT, NOTE, PAPER, PINK, RED, arrow, box, canvas, cell, cells,  # noqa: E402
                    label, outdir, plt, save)
from matplotlib.patches import Circle  # noqa: E402

OUT = outdir("13")


def open_():
    fig, ax = canvas(10, 2.6, 16, 4.0)
    box(ax, 0.4, 0.8, 6.8, 2.6, fc=PAPER)
    label(ax, 3.8, 2.8, "오늘 방문자 (집계)", fs=12, bold=True)
    label(ax, 3.8, 1.7, "94,707명", fs=20, color=RED, bold=True)
    box(ax, 8.8, 0.8, 6.8, 2.6, fc=PAPER)
    label(ax, 12.2, 2.8, "로그를 직접 세면", fs=12, bold=True)
    label(ax, 12.2, 1.7, "95,062명", fs=20, bold=True)
    label(ax, 8.0, 0.25, "355명이 어디 갔을까요?", fs=11, color=INK)
    save(fig, OUT, "es13-open.svg")


def map_():
    steps = ["정확히 세면\n메모리가 커요", "해시 앞의\n0 줄 길이", "통 여러 개로\n평균 내기(HLL)", "샤드끼리\n합치기 쉬워요", "백분위도\n어림(t-digest)"]
    fig, ax = canvas(11, 2.2, 20, 3)
    for k, s in enumerate(steps):
        x = 0.2 + k * 4.0
        hot = k == 2
        box(ax, x, 0.6, 3.2, 1.8, fc=PINK if hot else NOTE, ec=RED if hot else INK)
        label(ax, x + 1.6, 1.5, s, fs=11, color=RED if hot else "#222")
        label(ax, x + 0.22, 2.15, str(k + 1), fs=10, color=INK, ha="left")
        if k < 4:
            arrow(ax, (x + 3.3, 1.5), (x + 3.9, 1.5), ms=14)
    save(fig, OUT, "es13-map.svg")


def zeros():
    fig, ax = canvas(11, 3.6, 18, 5.6)
    label(ax, 0.3, 5.2, "사용자 ID를 해시하면 0과 1이 동전 던지기처럼 고르게 나와요", fs=12, ha="left", bold=True)
    rows = [("u-1", "1011010…", 0), ("u-2", "0110111…", 1), ("u-3", "0001101…", 3), ("u-4", "0100010…", 1)]
    for k, (u, b, z) in enumerate(rows):
        y = 4.0 - k * 0.85
        label(ax, 0.6, y + 0.3, u, fs=11, ha="left")
        for i, ch in enumerate(b):
            hot = i < z
            cell(ax, 2.0 + i * 0.6, y, 0.55, 0.6, ch, hot=hot, fs=11, fc=None if hot else "white")
        label(ax, 7.0, y + 0.3, f"앞 0이 {z}개", fs=10, color=RED if z == 3 else INK, ha="left")
    box(ax, 9.3, 1.0, 8.2, 3.6, fc=NOTE)
    label(ax, 13.4, 4.1, "앞에 0이 3개 이어질 확률은 1/8", fs=11)
    label(ax, 13.4, 3.3, "그런 값을 봤다면", fs=11)
    label(ax, 13.4, 2.5, "서로 다른 값을 대략 8개쯤 봤을 거예요", fs=11, color=RED, bold=True)
    label(ax, 13.4, 1.6, "같은 사용자는 해시가 같아서 두 번 와도 그대로", fs=10, color=INK)
    save(fig, OUT, "es13-zeros.svg")


def buckets():
    fig, ax = canvas(11, 3.8, 18, 6.0)
    random.seed(3)
    a = [random.choice([0, 1, 1, 2, 2, 3, 4]) for _ in range(8)]
    b = [random.choice([0, 1, 1, 2, 2, 3, 5]) for _ in range(8)]
    m = [max(x, y) for x, y in zip(a, b)]
    label(ax, 0.3, 5.5, "통 8개마다 '가장 긴 앞 0 줄'만 기억 (해시 앞 3비트로 통을 골라요)", fs=12, ha="left", bold=True)
    for k, (name, row) in enumerate((("샤드 A", a), ("샤드 B", b), ("합치기 = 칸마다 큰 값", m))):
        y = 4.2 - k * 1.3
        hot = k == 2
        label(ax, 0.3, y + 0.35, name, fs=11, ha="left", color=RED if hot else "#222", bold=hot)
        cells(ax, 5.0, y, row, w=1.0, h=0.75, hot=range(8) if hot else (), fs=11)
    label(ax, 9.0, 0.5, "통 하나는 운이 크게 끼지만 여러 통을 평균하면 오차가 줄어요", fs=11, color=INK)
    save(fig, OUT, "es13-buckets.svg")


def tdigest():
    random.seed(5)
    xs = sorted(random.lognormvariate(4, 0.8) for _ in range(3000))
    fig, ax = plt.subplots(figsize=(8.5, 3.6))
    ax.hist(xs, bins=60, color=LIGHT, edgecolor=GREY)
    # 중심점: 가운데는 굵게 많이, 꼬리는 작게
    qs = [0.005, 0.02, 0.05, 0.12, 0.25, 0.4, 0.55, 0.7, 0.82, 0.9, 0.95, 0.98, 0.993, 0.998]
    for q in qs:
        v = xs[int(q * len(xs))]
        w = 4 * q * (1 - q)
        ax.scatter([v], [-25], s=30 + 900 * w, color=PINK, edgecolor=RED, lw=1.2, zorder=3, clip_on=False)
    mid, tail = xs[int(0.55 * len(xs))], xs[int(0.95 * len(xs))]
    ax.annotate("가운데는 큰 묶음 몇 개로", xy=(mid, -25), xytext=(mid + 60, 120), color=RED, fontsize=10,
                arrowprops=dict(arrowstyle="->", color=RED, lw=1), annotation_clip=False)
    ax.annotate("꼬리 쪽은 작은 묶음을 촘촘히", xy=(tail, -25), xytext=(tail + 40, 60), color=RED, fontsize=10,
                arrowprops=dict(arrowstyle="->", color=RED, lw=1), annotation_clip=False)
    ax.set_xlabel("응답 시간 (ms)"); ax.set_ylabel("요청 수")
    ax.set_xlim(0, 600); ax.set_ylim(-60, None); ax.axhline(0, color=GREY, lw=0.8)
    ax.text(590, ax.get_ylim()[1] * 0.92, "아래 동그라미 = 묶음(크기는 든 값 수)\n개수는 줄여 그렸어요", color=RED, fontsize=9, ha="right", va="top")
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    save(fig, OUT, "es13-tdigest.svg")


if __name__ == "__main__":
    open_(); map_(); zeros(); buckets(); tdigest()
