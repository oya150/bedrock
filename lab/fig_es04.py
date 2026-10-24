"""Elasticsearch 4편 그림 만들기. 실행: python lab/fig_es04.py  → docs/elasticsearch/img/04/*.svg"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "es"))
from figkit import (BLUE, GREEN, GREY, INK, LIGHT, NOTE, PAPER, PINK, RED, YEL, arrow, box, canvas, cell,  # noqa: E402
                    cells, label, outdir, save)

OUT = outdir("04")


def open_():
    fig, ax = canvas(10, 2.8, 16, 4.2)
    ax.plot([0.8, 15.2], [1.6, 1.6], color=INK, lw=1.6)
    for x, t in ((1.5, "0초"), (6.0, "0.3초"), (12.5, "1초쯤")):
        ax.plot([x, x], [1.45, 1.75], color=INK, lw=1.6)
        label(ax, x, 1.1, t, fs=10, color=INK)
    box(ax, 0.4, 2.2, 2.2, 1.0, fc=NOTE); label(ax, 1.5, 2.7, "글 저장", fs=11)
    box(ax, 4.6, 2.2, 2.8, 1.0, fc=PINK, ec=RED); label(ax, 6.0, 2.7, "검색: 0건", fs=11, color=RED, bold=True)
    box(ax, 11.1, 2.2, 2.8, 1.0, fc=NOTE); label(ax, 12.5, 2.7, "검색: 1건", fs=11)
    label(ax, 8.0, 0.35, "저장은 끝났다는데 검색에는 잠깐 안 보여요", fs=11, color=INK)
    save(fig, OUT, "es04-open.svg")


def map_():
    steps = ["정렬된 역색인은\n고치기 비싸요", "새 문서는\n새 세그먼트로", "refresh가\n검색에 보이게", "GET은\n바로 보여요", "꺼져도 남게:\ntranslog와 flush"]
    fig, ax = canvas(11, 2.2, 20, 3)
    for k, s in enumerate(steps):
        x = 0.2 + k * 4.0
        hot = k == 2
        box(ax, x, 0.6, 3.2, 1.8, fc=PINK if hot else NOTE, ec=RED if hot else INK)
        label(ax, x + 1.6, 1.5, s, fs=11, color=RED if hot else "#222")
        label(ax, x + 0.22, 2.15, str(k + 1), fs=10, color=INK, ha="left")
        if k < 4:
            arrow(ax, (x + 3.3, 1.5), (x + 3.9, 1.5), ms=14)
    save(fig, OUT, "es04-map.svg")


def immutable():
    fig, ax = canvas(11, 4.0, 17, 6.0)
    label(ax, 0.3, 5.5, "새 문서에 처음 보는 낱말 '교환'이 있으면 용어 사전 중간에 끼워야 해요", fs=12, ha="left", bold=True)
    terms = ["감사", "배송", "언제", "완료", "요청", "주문", "환불"]
    cells(ax, 0.3, 4.0, terms, w=1.0, h=0.8, fs=11)
    label(ax, 7.75, 4.4, "→", fs=16, color=INK)
    cells(ax, 8.3, 4.0, ["감사", "교환"] + terms[1:], w=0.95, h=0.8, fs=10, hot=range(1, 8))
    label(ax, 12.1, 3.45, "그 뒤 칸을 모두 다시 써야 해요 (압축·FST까지)", fs=11, color=RED)
    label(ax, 0.3, 2.3, "Lucene은 고치지 않고 새 묶음을 하나 더 만들어요", fs=12, ha="left", bold=True)
    box(ax, 0.6, 0.4, 7.4, 1.4, fc=NOTE)
    label(ax, 1.0, 1.45, "세그먼트 _0 (그대로 둠)", fs=10, ha="left", color=INK)
    cells(ax, 1.0, 0.55, terms, w=0.9, h=0.65, fs=9)
    box(ax, 8.6, 0.4, 3.4, 1.4, fc=PINK, ec=RED)
    label(ax, 9.0, 1.45, "세그먼트 _1 (새로)", fs=10, ha="left", color=RED)
    cells(ax, 9.0, 0.55, ["교환", "주문"], w=0.9, h=0.65, fs=9, hot=(0,))
    label(ax, 12.4, 1.1, "검색은 두 묶음을\n다 보고 합쳐요", fs=11, color=INK, ha="left")
    save(fig, OUT, "es04-immutable.svg")


def buffer():
    fig, ax = canvas(11, 3.6, 17, 7.2)
    ax.set_ylim(1.5, 7.2)
    label(ax, 0.3, 6.8, "메모리", fs=12, ha="left", bold=True)
    box(ax, 0.3, 4.6, 4.6, 1.8, fc=LIGHT)
    label(ax, 2.6, 6.05, "색인 버퍼", fs=11, color=INK)
    cells(ax, 0.6, 4.85, ["문서 6", "문서 7"], w=1.9, h=0.8, fs=10, dim=(0, 1))
    label(ax, 2.6, 4.25, "아직 검색에 안 보여요", fs=10, color=INK)
    arrow(ax, (5.1, 5.5), (7.0, 5.5), color=RED, lw=2.5)
    label(ax, 6.05, 6.0, "refresh", fs=12, color=RED, bold=True)
    label(ax, 6.05, 4.95, "1초마다", fs=10, color=RED)
    label(ax, 7.3, 6.8, "검색할 수 있는 세그먼트", fs=12, ha="left", bold=True)
    for k, (name, docs) in enumerate((("_0", "문서 1"), ("_1", "문서 2, 3"), ("_2", "문서 4, 5"))):
        hot = k == 2
        box(ax, 7.3 + k * 3.2, 4.6, 2.9, 1.8, fc=PINK if hot else NOTE, ec=RED if hot else INK)
        label(ax, 8.75 + k * 3.2, 5.8, f"세그먼트 {name}", fs=11, color=RED if hot else "#222", bold=hot)
        label(ax, 8.75 + k * 3.2, 5.1, docs, fs=10, color=INK)
    box(ax, 9.5, 1.8, 5.0, 1.1, fc=PAPER)
    label(ax, 12.0, 2.35, "검색: 환불", fs=12)
    for k in range(3):
        arrow(ax, (12.0, 3.0), (8.75 + k * 3.2, 4.5), lw=1.4, ms=12)
    label(ax, 0.3, 2.35, "검색은 세그먼트마다 찾아서\n결과를 합쳐요", fs=11, ha="left", color=INK)
    save(fig, OUT, "es04-buffer.svg")


def translog():
    fig, ax = canvas(11, 5.0, 17, 7.6)
    label(ax, 0.3, 7.2, "메모리", fs=12, ha="left", bold=True)
    box(ax, 0.3, 5.3, 4.2, 1.5, fc=LIGHT); label(ax, 2.4, 6.05, "색인 버퍼", fs=11)
    box(ax, 5.6, 5.3, 5.2, 1.5, fc=NOTE); label(ax, 8.2, 6.05, "세그먼트 (OS 캐시에만)", fs=11)
    arrow(ax, (4.6, 6.05), (5.5, 6.05)); label(ax, 5.05, 6.5, "refresh", fs=10, color=INK)
    ax.plot([0.2, 16.8], [4.6, 4.6], color=GREY, lw=1.5, ls="--")
    label(ax, 0.3, 4.15, "디스크 (fsync까지 끝난 것)", fs=12, ha="left", bold=True)
    box(ax, 5.6, 2.1, 5.2, 1.5, fc=NOTE); label(ax, 8.2, 2.85, "세그먼트 (커밋됨)", fs=11)
    arrow(ax, (8.2, 5.2), (8.2, 3.7)); label(ax, 8.4, 4.25, "flush", fs=11, color=INK, ha="left")
    box(ax, 11.6, 1.6, 5.0, 2.5, fc=PINK, ec=RED)
    label(ax, 14.1, 3.7, "translog", fs=12, color=RED, bold=True)
    for k, t in enumerate(("1: 문서 6 넣기", "2: 문서 7 넣기", "3: 문서 2 지우기")):
        label(ax, 12.0, 3.1 - k * 0.5, t, fs=10, ha="left", color=INK)
    arrow(ax, (1.2, 5.2), (11.5, 1.9), color=RED, lw=1.6, rad=0.45)
    label(ax, 0.3, 2.3, "요청마다 바로 기록하고\nfsync한 뒤에 응답해요", fs=10, color=RED, ha="left")
    label(ax, 8.6, 0.8, "꺼졌다 켜지면: 커밋된 세그먼트 + translog를 다시 실행", fs=11, color=INK)
    save(fig, OUT, "es04-translog.svg")


if __name__ == "__main__":
    open_(); map_(); immutable(); buffer(); translog()
