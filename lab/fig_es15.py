"""Elasticsearch 15편 그림 만들기. 실행: python lab/fig_es15.py  → docs/elasticsearch/img/15/*.svg"""
import importlib
import os
import random
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "es"))
from figkit import (BLUE, GREY, INK, LIGHT, NOTE, PAPER, PINK, RED, arrow, box, canvas, cell, cells,  # noqa: E402
                    label, outdir, plt, save)

hnsw = importlib.import_module("15_hnsw")
OUT = outdir("15")


def open_():
    fig, ax = canvas(11, 3.0, 20, 5.4)
    box(ax, 0.4, 1.4, 5.0, 3.0, fc=PAPER)
    label(ax, 2.9, 3.7, "질문", fs=11, bold=True)
    label(ax, 2.9, 2.8, "\"비밀번호를\n잊어버렸어요\"", fs=11)
    label(ax, 2.9, 1.8, "[0.12, -0.80, 0.33, …]", fs=9, color=INK)
    arrow(ax, (5.6, 2.9), (7.4, 2.9), ms=14)
    box(ax, 7.6, 1.4, 5.4, 3.0, fc=NOTE)
    label(ax, 10.3, 3.7, "저장된 질문 20,000개", fs=11, bold=True)
    label(ax, 10.3, 2.8, "\"암호 재설정은\n어디서 하나요\"", fs=11)
    label(ax, 10.3, 1.8, "글자는 하나도 안 겹쳐요", fs=9, color=INK)
    arrow(ax, (13.2, 2.9), (15.0, 2.9), ms=14)
    box(ax, 15.2, 1.4, 4.4, 3.0, fc=PINK, ec=RED)
    label(ax, 17.4, 3.4, "숫자 목록끼리", fs=11, color=RED, bold=True)
    label(ax, 17.4, 2.5, "가장 가까운 10개", fs=11, color=RED)
    label(ax, 10.0, 0.6, "20,000개와 모두 거리를 재야 할까요?", fs=11, color=INK)
    save(fig, OUT, "es15-open.svg")


def map_():
    steps = ["글을 숫자\n목록으로", "전부 재면\n느려요", "이웃 따라\n걸어가기", "층을 쌓아\n크게 건너뛰기", "후보 수로\n정확도 고르기"]
    fig, ax = canvas(11, 2.2, 20, 3)
    for k, s in enumerate(steps):
        x = 0.2 + k * 4.0
        hot = k == 3
        box(ax, x, 0.6, 3.2, 1.8, fc=PINK if hot else NOTE, ec=RED if hot else INK)
        label(ax, x + 1.6, 1.5, s, fs=11, color=RED if hot else "#222")
        label(ax, x + 0.22, 2.15, str(k + 1), fs=10, color=INK, ha="left")
        if k < 4:
            arrow(ax, (x + 3.3, 1.5), (x + 3.9, 1.5), ms=14)
    save(fig, OUT, "es15-map.svg")


def walk():
    """2차원 점 120개로 이웃 그래프(맨 아래층)를 만들고 먼 점에서 질의까지 욕심껏 걸어가는 길을 그린다."""
    random.seed(7)
    pts = [[random.uniform(0, 10), random.uniform(0, 6)] for _ in range(120)]
    g = hnsw.HNSW(m=4, ef_build=20)
    for p in pts:
        g.add(p)
    q = [8.6, 4.9]
    start = min(range(len(pts)), key=lambda i: hnsw.dist(pts[i], [0.6, 0.8]))
    path, cur = [start], start
    while True:
        nxt = min(g.links[cur][0] + [cur], key=lambda i: hnsw.dist(pts[i], q))
        if nxt == cur:
            break
        path.append(nxt)
        cur = nxt
    fig, ax = plt.subplots(figsize=(9, 5.4))
    for i, p in enumerate(pts):
        for j in g.links[i][0]:
            if i < j:
                ax.plot([p[0], pts[j][0]], [p[1], pts[j][1]], color=LIGHT, lw=0.9, zorder=1)
    ax.scatter([p[0] for p in pts], [p[1] for p in pts], s=16, color=GREY, zorder=2)
    for a, b in zip(path, path[1:]):
        ax.annotate("", xy=pts[b], xytext=pts[a], arrowprops=dict(arrowstyle="-|>", color=RED, lw=2), zorder=3)
    ax.scatter(*pts[start], s=90, color=INK, zorder=4)
    ax.text(pts[start][0], pts[start][1] - 0.45, "출발", ha="center", fontsize=10, color=INK)
    ax.scatter(*q, s=160, marker="*", color=RED, zorder=5)
    ax.text(q[0], q[1] + 0.3, "질문", ha="center", fontsize=10, color=RED)
    ax.set_title(f"이웃 중 질문에 가장 가까운 쪽으로만 걸으면 {len(path) - 1}걸음 만에 멈춰요(더 가까운 이웃이 없음)",
                 fontsize=11, loc="left")
    ax.text(pts[path[-1]][0], pts[path[-1]][1] - 0.45, "멈춘 곳", ha="center", fontsize=10, color=RED)
    ax.set_xlim(-0.3, 10.3); ax.set_ylim(-0.6, 6.4); ax.set_xticks([]); ax.set_yticks([])
    for sp in ax.spines.values():
        sp.set_visible(False)
    save(fig, OUT, "es15-walk.svg")
    return len(path) - 1


def layers():
    fig, ax = canvas(11, 4.4, 20, 8.0)
    random.seed(4)
    rows = [("2층", 3), ("1층", 9), ("0층(모든 점)", 28)]
    xs = {0: sorted(random.uniform(1.2, 18.8) for _ in range(28))}
    xs[1] = sorted(random.sample(xs[0], 9))
    xs[2] = sorted(random.sample(xs[1], 3))
    route = {2: xs[2][1], 1: None, 0: None}
    target = 15.6
    for k, (name, _) in enumerate(rows):
        lvl = 2 - k
        y = 6.6 - k * 2.5
        ax.plot([1.0, 19.0], [y, y], color=LIGHT, lw=1)
        label(ax, 0.2, y + 0.55, name, fs=10, ha="left", color=INK)
        pts = xs[lvl]
        for a, b in zip(pts, pts[1:]):
            ax.plot([a, b], [y, y], color=GREY, lw=1.2)
        ax.scatter(pts, [y] * len(pts), s=30 if lvl == 0 else 60, color=GREY, zorder=3)
    # 위층에서 크게 건너뛰고 내려가며 촘촘히
    y2, y1, y0 = 6.6, 4.1, 1.6
    a2 = xs[2][0]
    b2 = min(xs[2], key=lambda x: abs(x - target))
    b1 = min(xs[1], key=lambda x: abs(x - target))
    b0 = min(xs[0], key=lambda x: abs(x - target))
    for (xa, ya), (xb, yb) in [((a2, y2), (b2, y2)), ((b2, y2), (b2, y1)), ((b2, y1), (b1, y1)),
                               ((b1, y1), (b1, y0)), ((b1, y0), (b0, y0))]:
        if abs(xa - xb) > 1e-6 or abs(ya - yb) > 1e-6:
            arrow(ax, (xa, ya), (xb, yb), color=RED, lw=2.2, ms=14)
    ax.scatter([target], [y0 - 0.7], marker="*", s=180, color=RED, zorder=4)
    label(ax, target, y0 - 1.25, "질문", fs=10, color=RED)
    label(ax, 10.0, 7.6, "위층은 점이 드물어 한 걸음이 길고, 아래로 내려갈수록 촘촘히 찾아요", fs=11, color=INK)
    save(fig, OUT, "es15-layers.svg")


def tradeoff():
    ef = [10, 20, 50, 100, 200]
    work = [284, 431, 780, 1217, 1840]
    hits = [8.8, 9.5, 10.0, 10.0, 10.0]
    fig, ax = plt.subplots(figsize=(8.5, 3.4))
    ax.bar([str(e) for e in ef], work, color=LIGHT, edgecolor=GREY)
    for i, (w, h) in enumerate(zip(work, hits)):
        ax.text(i, w + 60, f"{w:,}번\n정답 {h:.1f}/10", ha="center", fontsize=10, color=RED if h < 10 else INK)
    ax.axhline(5000, color=RED, lw=1.5, ls="--")
    ax.text(4.4, 5000 + 120, "전부 비교 5,000번", ha="right", fontsize=10, color=RED)
    ax.set_xlabel("들고 다니는 후보 수"); ax.set_ylabel("질문 하나당 거리 계산")
    ax.set_ylim(0, 5800)
    ax.set_title("벡터 5,000개: 막대 위는 거리 계산 횟수와 정답 10개 중 찾은 수", fontsize=11, loc="left")
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    save(fig, OUT, "es15-tradeoff.svg")


if __name__ == "__main__":
    open_(); map_(); print("걸음 수", walk()); layers(); tradeoff()
