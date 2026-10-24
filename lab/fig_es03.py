"""Elasticsearch 3편 그림 만들기. 실행: python lab/fig_es03.py  → docs/elasticsearch/img/03/*.svg"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "es"))
from figkit import (BLUE, GREEN, GREY, INK, NOTE, PAPER, PINK, RED, YEL, arrow, box, canvas, cell,  # noqa: E402
                    cells, label, outdir, save)

OUT = outdir("03")
SC = [BLUE, GREEN, YEL, "#c6a0d8"]


def open_():
    fig, ax = canvas(9, 3.4, 13, 4.8)
    label(ax, 0.3, 4.4, "orders 인덱스", fs=12, ha="left", bold=True)
    for k in range(3):
        box(ax, 0.3 + k * 2.0, 2.0, 1.7, 1.8, fc=NOTE)
        label(ax, 1.15 + k * 2.0, 2.9, f"샤드 {k}", fs=11)
    box(ax, 7.6, 2.3, 5.0, 1.3, fc=PINK, ec=RED)
    label(ax, 10.1, 2.95, '"number_of_shards": 4', fs=12, color=RED)
    arrow(ax, (7.5, 2.95), (6.3, 2.95), color=RED)
    label(ax, 10.1, 1.6, "바꿀 수 없다는 오류", fs=12, color=RED, bold=True)
    label(ax, 3.3, 1.3, "처음 만들 때 3개로 정했어요", fs=11, color=INK)
    save(fig, OUT, "es03-open.svg")


def map_():
    steps = ["인덱스는\n샤드로 나뉘어요", "샤드 번호는\n계산으로 정해요", "샤드 수를 바꾸면\n다 섞여요", "배수로는\n쪼갤 수 있어요", "라우팅 값을\n직접 주기"]
    fig, ax = canvas(11, 2.2, 20, 3)
    for k, s in enumerate(steps):
        x = 0.2 + k * 4.0
        hot = k == 2
        box(ax, x, 0.6, 3.2, 1.8, fc=PINK if hot else NOTE, ec=RED if hot else INK)
        label(ax, x + 1.6, 1.5, s, fs=11, color=RED if hot else "#222")
        label(ax, x + 0.22, 2.15, str(k + 1), fs=10, color=INK, ha="left")
        if k < 4:
            arrow(ax, (x + 3.3, 1.5), (x + 3.9, 1.5), ms=14)
    save(fig, OUT, "es03-map.svg")


def route():
    fig, ax = canvas(10.5, 3.8, 17, 5.8)
    rows = [("order-8", "-207443486", 226, 0), ("order-4", "-1039169787", 261, 1), ("order-1", "-1419791865", 519, 2)]
    for k, (i, h, slot, sh) in enumerate(rows):
        y = 4.1 - k * 1.3
        hot = k == 2
        cell(ax, 0.2, y, 1.8, 0.8, i, hot=hot, fs=11)
        arrow(ax, (2.1, y + 0.4), (2.9, y + 0.4), ms=12)
        box(ax, 3.0, y, 1.9, 0.8, fc=PAPER)
        label(ax, 3.95, y + 0.4, "murmur3", fs=10)
        arrow(ax, (5.0, y + 0.4), (5.8, y + 0.4), ms=12)
        cell(ax, 5.9, y, 2.6, 0.8, h, fs=10, hot=hot)
        arrow(ax, (8.6, y + 0.4), (9.9, y + 0.4), ms=12)
        cell(ax, 10.0, y, 1.6, 0.8, f"칸 {slot}", fs=11, hot=hot)
        arrow(ax, (11.7, y + 0.4), (12.6, y + 0.4), ms=12)
        box(ax, 12.7, y - 0.05, 1.9, 0.9, fc=SC[sh])
        label(ax, 13.65, y + 0.4, f"샤드 {sh}", fs=11, bold=hot, color=RED if hot else "#222")
    label(ax, 9.25, 5.2, "768로 나눈 나머지", fs=10, color=INK)
    label(ax, 14.9, 4.5, "칸 0~255", fs=10, color=INK, ha="left")
    label(ax, 14.9, 3.2, "칸 256~511", fs=10, color=INK, ha="left")
    label(ax, 14.9, 1.9, "칸 512~767", fs=10, color=INK, ha="left")
    label(ax, 7.5, 0.45, "어느 노드든 _id만 알면 같은 샤드를 계산해요", fs=11, color=INK)
    save(fig, OUT, "es03-route.svg")


def reshuffle():
    fig, ax = canvas(10.5, 4.0, 16, 6.0)
    label(ax, 0.3, 5.5, "해시값 0~11을 나머지로 샤드 3개, 4개에 나눠 담으면", fs=12, ha="left", bold=True)
    for n, y0 in ((3, 3.4), (4, 0.6)):
        label(ax, 0.3, y0 + 1.4, f"샤드 {n}개", fs=11, ha="left", color=INK)
        for s in range(n):
            x = 1.6 + s * (14.0 / n)
            w = 14.0 / n - 0.25
            box(ax, x, y0, w, 1.15, fc=SC[s] if n == 3 else "white", ec=INK, lw=1.2)
            hs = [h for h in range(12) if h % n == s]
            for j, h in enumerate(hs):
                moved = n == 4 and (h % 3 != h % 4)
                cell(ax, x + 0.15 + j * 0.85, y0 + 0.2, 0.75, 0.75, h, hot=moved, fs=10,
                     fc=None if moved else SC[h % 3])
    label(ax, 15.6, 0.15, "빨강: 샤드가 바뀌는 문서 12개 중 9개", fs=11, color=RED, ha="right")
    save(fig, OUT, "es03-reshuffle.svg")


def split():
    fig, ax = canvas(10.5, 4.4, 16, 6.4)
    label(ax, 0.3, 6.0, "칸을 6개로 줄여 그리면: 샤드 3개가 칸을 2개씩 맡다가, 쪼개면 1개씩", fs=12, ha="left", bold=True)
    W = 2.3
    label(ax, 0.3, 4.75, "칸", fs=11, ha="left", color=INK)
    for slot in range(6):
        cell(ax, 1.4 + slot * W, 4.4, W - 0.1, 0.7, f"칸 {slot}", fs=10, fc=SC[slot // 2])
    label(ax, 0.3, 3.25, "샤드 3개", fs=11, ha="left", color=INK)
    label(ax, 0.3, 1.25, "샤드 6개", fs=11, ha="left", color=INK)
    for p in range(3):
        x = 1.4 + p * 2 * W
        box(ax, x, 2.9, 2 * W - 0.1, 0.75, fc=SC[p], round_=False)
        label(ax, x + W - 0.05, 3.27, f"샤드 {p} (칸 {2*p}, {2*p+1})", fs=10)
        for c in range(2):
            t = 2 * p + c
            xx = 1.4 + t * W
            hot = p == 2
            arrow(ax, (x + W - 0.05, 2.85), (xx + (W - 0.1) / 2, 1.75), color=RED if hot else INK, lw=1.4, ms=12)
            box(ax, xx, 0.9, W - 0.1, 0.75, fc=SC[p], ec=RED if hot else INK, lw=2 if hot else 1.2, round_=False)
            label(ax, xx + (W - 0.1) / 2, 1.27, f"샤드 {t}", fs=10, color=RED if hot else "#222")
    label(ax, 8.0, 0.3, "쪼갤 때 문서는 자기 샤드에서 갈라진 두 샤드 중 하나로만 가요", fs=11, color=RED)
    save(fig, OUT, "es03-split.svg")


if __name__ == "__main__":
    open_(); map_(); route(); reshuffle(); split()
