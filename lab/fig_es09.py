"""Elasticsearch 9편 그림 만들기. 실행: python lab/fig_es09.py  → docs/elasticsearch/img/09/*.svg"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "es"))
from figkit import (BLUE, GREY, INK, LIGHT, NOTE, PAPER, PINK, RED, arrow, box, canvas, cell, cells,  # noqa: E402
                    label, outdir, plt, save)

OUT = outdir("09")


def open_():
    fig, ax = canvas(9, 2.8, 14, 4.4)
    box(ax, 0.4, 0.6, 8.0, 3.2, fc=PAPER)
    for k, t in enumerate(['"hits": {', '  "total": {', '    "value": 10000,', '    "relation": "gte"', '  }, ...']):
        hot = k in (2, 3)
        label(ax, 0.9, 3.3 - k * 0.55, t, fs=11, ha="left", color=RED if hot else "#222", family="monospace")
    arrow(ax, (8.6, 2.2), (9.6, 2.2), color=RED)
    label(ax, 9.8, 2.6, "맞는 문서는 20만 개인데", fs=11, ha="left", color=RED)
    label(ax, 9.8, 1.8, "\"1만 개 이상\"이래요", fs=11, ha="left", color=RED)
    save(fig, OUT, "es09-open.svg")


def map_():
    steps = ["상위 10개는\n힙으로", "문턱을 못 넘으면\n계산 안 해요", "낱말별 최고 점수\n(WAND)", "묶음별 최고 점수\n(block-max)", "건수 세기와\n맞바꿔요"]
    fig, ax = canvas(11, 2.2, 20, 3)
    for k, s in enumerate(steps):
        x = 0.2 + k * 4.0
        hot = k == 3
        box(ax, x, 0.6, 3.2, 1.8, fc=PINK if hot else NOTE, ec=RED if hot else INK)
        label(ax, x + 1.6, 1.5, s, fs=10.5, color=RED if hot else "#222")
        label(ax, x + 0.22, 2.15, str(k + 1), fs=10, color=INK, ha="left")
        if k < 4:
            arrow(ax, (x + 3.3, 1.5), (x + 3.9, 1.5), ms=14)
    save(fig, OUT, "es09-map.svg")


def heap():
    fig, ax = canvas(10, 4.0, 16, 6.4)
    label(ax, 0.3, 6.0, "지금까지 본 점수 중 상위 3개 (힙, 가장 작은 게 맨 위)", fs=12, ha="left", bold=True)
    cell(ax, 3.2, 4.4, 1.2, 0.8, "4.2", hot=True)
    cell(ax, 1.6, 2.8, 1.2, 0.8, "6.0")
    cell(ax, 4.8, 2.8, 1.2, 0.8, "7.5")
    ax.plot([3.6, 2.2], [4.4, 3.6], color=INK, lw=1.2); ax.plot([4.0, 5.4], [4.4, 3.6], color=INK, lw=1.2)
    label(ax, 3.8, 1.9, "맨 위 4.2가 문턱", fs=11, color=RED)
    box(ax, 8.4, 4.2, 3.0, 1.0, fc=LIGHT, ec=GREY)
    label(ax, 9.9, 4.7, "새 문서 3.1", fs=11, color=GREY)
    arrow(ax, (8.3, 4.7), (4.6, 4.8), color=GREY, rad=0.0)
    label(ax, 6.5, 5.25, "4.2보다 작으니 버려요", fs=10, color=INK)
    box(ax, 8.4, 2.4, 3.0, 1.0, fc=PINK, ec=RED)
    label(ax, 9.9, 2.9, "새 문서 5.1", fs=11, color=RED)
    arrow(ax, (8.3, 2.9), (4.6, 4.5), color=RED, rad=-0.2)
    label(ax, 11.6, 2.9, "4.2를 밀어내고 들어가요\n새 문턱은 5.1", fs=10, color=RED, ha="left")
    label(ax, 8.0, 0.6, "문턱은 시간이 갈수록 올라가기만 해요", fs=11, color=INK)
    save(fig, OUT, "es09-heap.svg")


def wand():
    fig, ax = canvas(11, 4.6, 18, 7.4)
    label(ax, 0.3, 7.0, "검색어: rare common, 지금 문턱 4.2", fs=12, ha="left", bold=True)
    label(ax, 0.3, 5.95, "common이 낼 수 있는 최고 점수 1.2", fs=11, ha="left")
    label(ax, 0.3, 5.35, "rare가 낼 수 있는 최고 점수 8.5", fs=11, ha="left", color=RED)
    docs = [("common", False), ("common", False), ("rare common", True), ("common", False), ("common", False), ("rare common", True), ("common", False)]
    for k, (t, has_rare) in enumerate(docs):
        x = 0.4 + k * 2.4
        cell(ax, x, 3.4, 2.1, 0.8, t, hot=has_rare, dim=not has_rare, fs=10)
        if has_rare:
            label(ax, x + 1.05, 2.8, "최고 9.7 > 4.2\n점수 계산", fs=9, color=RED)
        else:
            label(ax, x + 1.05, 2.8, "최고 1.2 ≤ 4.2\n건너뜀", fs=9, color=GREY)
    label(ax, 9.0, 1.3, "rare가 없는 문서는 common만으로 문턱을 넘을 수 없어요", fs=11, color=INK)
    label(ax, 9.0, 0.6, "그래서 rare 목록이 앞장서고 common은 advance만 해요(7편)", fs=11, color=INK)
    save(fig, OUT, "es09-wand.svg")


def counts():
    fig, ax = plt.subplots(figsize=(8.5, 3.6))
    names = ["track_total_hits\ntrue", "기본값 1만\n(9.2, 7.17은 11,635)", "false\n(7.17)", "false\n(9.2)"]
    vals = [200_000, 10_022, 2_446, 604]
    colors = [GREY, BLUE, "#e4572e", "#e4572e"]
    bars = ax.bar(range(4), vals, color=colors)
    ax.set_yscale("log")
    for i, v in enumerate(vals):
        ax.text(i, v * 1.15, f"{v:,}", ha="center", fontsize=11)
    ax.set_xticks(range(4)); ax.set_xticklabels(names, fontsize=10)
    ax.set_ylabel("점수를 계산한 문서 수 (로그 눈금)")
    ax.set_ylim(100, 600_000)
    ax.text(1.6, 250_000, "문서 20만 개, 상위 10개, 1위 점수는 모두 같음", fontsize=10, color=INK, ha="center")
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    save(fig, OUT, "es09-counts.svg")


if __name__ == "__main__":
    open_(); map_(); heap(); wand(); counts()
