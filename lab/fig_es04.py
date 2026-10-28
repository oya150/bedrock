"""Elasticsearch 4편 그림 만들기. 실행: python lab/fig_es04.py  → docs/elasticsearch/img/04/*.svg"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "es"))
from figkit import (GREY, INK, LIGHT, NOTE, PAPER, PINK, RED, arrow, box, canvas, cells, label, outdir,  # noqa: E402
                    save, story)

OUT = outdir("04")


def open_():
    fig, ax = canvas(10, 2.8, 16, 4.2)
    ax.plot([0.8, 15.2], [1.6, 1.6], color=INK, lw=1.6)
    for x, t in ((1.5, "0초"), (6.0, "0.3초"), (12.5, "1초쯤")):
        ax.plot([x, x], [1.45, 1.75], color=INK, lw=1.6)
        label(ax, x, 1.1, t, fs=10, color=INK)
    box(ax, 0.4, 2.2, 2.2, 1.0, fc=NOTE); label(ax, 1.5, 2.85, "글 저장", fs=11); label(ax, 1.5, 2.45, "(환불 요청)", fs=9.5, color=INK)
    box(ax, 4.6, 2.2, 2.8, 1.0, fc=PINK, ec=RED); label(ax, 6.0, 2.7, "검색: 0건", fs=11, color=RED, bold=True)
    box(ax, 11.1, 2.2, 2.8, 1.0, fc=NOTE); label(ax, 12.5, 2.7, "검색: 1건", fs=11)
    label(ax, 8.0, 0.35, "저장은 끝났다는데 검색에는 잠깐 안 보여요", fs=11, color=INK)
    save(fig, OUT, "es04-open.svg")


def map_():
    """정리 절: 이 편이 한 말을 결론 문장으로."""
    story(["Lucene은 만든 역색인은 그대로 두고 새 문서로 세그먼트를 하나 더 만들어요",
           "ES는 새 문서를 메모리에 모았다가 refresh 때 세그먼트로 만들어요",
           "검색은 세그먼트만 보니 새 문서는 다음 refresh까지(기본 1초) 안 보여요",
           "요청마다 translog에 적고 fsync 하니 서버가 꺼져도 되살려요",
           "flush가 세그먼트를 디스크에 확정하면 그 전 translog 요청은 다시 실행하지 않아도 돼요",
           "ID로 꺼내는 GET은 refresh 전에도 문서를 찾아요"], 2, OUT, "es04-map.svg")


def immutable():
    fig, ax = canvas(11, 4.0, 17, 6.0)
    label(ax, 0.3, 5.5, "새 문서에 처음 보는 낱말 '교환'이 있으면 용어 사전 중간에 끼워야 해요", fs=12, ha="left", bold=True)
    terms = ["감사", "배송", "언제", "완료", "요청", "주문", "환불"]
    cells(ax, 0.3, 4.0, terms, w=0.95, h=0.8, fs=11)
    label(ax, 7.9, 4.4, "→", fs=16, color=INK)
    cells(ax, 8.3, 4.0, ["감사", "교환"] + terms[1:], w=0.95, h=0.8, fs=10, hot=range(1, 8))
    label(ax, 12.1, 3.45, "그 칸을 모두 다시 써야 해요 (압축한 덩어리까지)", fs=11, color=RED)
    label(ax, 0.3, 2.3, "Lucene은 그대로 두고 세그먼트를 하나 더 만들어요", fs=12, ha="left", bold=True)
    box(ax, 0.6, 0.4, 7.4, 1.4, fc=NOTE)
    label(ax, 1.0, 1.45, "세그먼트 _0 (그대로 둠)", fs=10, ha="left", color=INK)
    cells(ax, 1.0, 0.55, terms, w=0.9, h=0.65, fs=9)
    box(ax, 8.6, 0.4, 3.4, 1.4, fc=PINK, ec=RED)
    label(ax, 9.0, 1.45, "세그먼트 _1 (새로)", fs=10, ha="left", color=RED)
    cells(ax, 9.0, 0.55, ["교환", "주문"], w=0.9, h=0.65, fs=9, hot=(0,))
    label(ax, 12.4, 1.1, "검색은 두 세그먼트를\n다 찾아서 합쳐요", fs=11, color=INK, ha="left")
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
    label(ax, 9.2, 2.35, "검색은 세그먼트마다 찾아서\n결과를 합쳐요", fs=11, ha="right", color=INK)
    save(fig, OUT, "es04-buffer.svg")


def get():
    """검색은 세그먼트만, GET은 아직 refresh 안 된 ID 기록 → 숨은 세그먼트."""
    fig, ax = canvas(11, 4.6, 17, 7.0)
    label(ax, 0.3, 6.6, "메모리의 색인 버퍼", fs=11, ha="left", bold=True)
    box(ax, 0.3, 4.8, 3.6, 1.4, fc=LIGHT)
    label(ax, 2.1, 5.5, "문서 8\n환불 요청", fs=10.5, color=INK)
    label(ax, 7.3, 6.6, "세그먼트 (검색에 보임)", fs=11, ha="left", bold=True)
    for k, n in enumerate(("_0", "_1", "_2")):
        box(ax, 7.3 + k * 2.2, 5.0, 1.9, 1.1, fc=NOTE)
        label(ax, 8.25 + k * 2.2, 5.55, n, fs=10.5)
    box(ax, 4.4, 3.0, 2.6, 1.0, fc=PAPER); label(ax, 5.7, 3.5, "검색: 환불", fs=10.5)
    for k in range(3):
        arrow(ax, (7.05, 3.7), (8.25 + k * 2.2, 4.9), lw=1.2, ms=10)
    ax.plot([5.2, 3.0], [4.05, 4.7], color=GREY, lw=1.4, ls="--")
    label(ax, 3.4, 4.05, "안 봐요", fs=9.5, color=GREY)
    arrow(ax, (7.1, 3.5), (14.1, 3.5), lw=1.2, ms=10)
    box(ax, 14.2, 3.0, 2.4, 1.0, fc=PINK, ec=RED); label(ax, 15.4, 3.5, "0건", fs=11, color=RED, bold=True)
    box(ax, 0.3, 0.3, 2.6, 1.0, fc=PAPER); label(ax, 1.6, 0.8, "GET _doc/8", fs=10.5)
    arrow(ax, (3.0, 0.8), (4.3, 0.8))
    box(ax, 4.4, 0.3, 9.0, 1.0, fc=NOTE)
    label(ax, 8.9, 0.8, "아직 refresh 안 된 문서도 ID로 따로 꺼내 와요", fs=10.5)
    arrow(ax, (13.5, 0.8), (14.1, 0.8))
    box(ax, 14.2, 0.3, 2.4, 1.0, fc=NOTE); label(ax, 15.4, 0.8, "찾음", fs=11, bold=True)
    save(fig, OUT, "es04-get.svg")


def translog():
    fig, ax = canvas(11, 5.0, 17, 7.6)
    box(ax, 0.3, 5.3, 2.6, 1.5, fc=PAPER); label(ax, 1.6, 6.05, "요청\n(문서 넣기)", fs=10.5)
    label(ax, 3.6, 7.2, "메모리 (전원이 꺼지면 사라져요)", fs=12, ha="left", bold=True)
    arrow(ax, (3.0, 6.05), (3.6, 6.05))
    box(ax, 3.7, 5.3, 3.4, 1.5, fc=LIGHT); label(ax, 5.4, 6.05, "색인 버퍼", fs=11)
    arrow(ax, (7.2, 6.05), (8.6, 6.05)); label(ax, 7.9, 6.5, "refresh", fs=10, color=INK)
    box(ax, 8.7, 5.3, 6.0, 1.5, fc=NOTE); label(ax, 11.7, 6.05, "세그먼트\n(운영체제가 메모리에 들고 있음)", fs=10.5)
    ax.plot([0.2, 16.8], [4.6, 4.6], color=GREY, lw=1.5, ls="--")
    label(ax, 3.6, 4.15, "디스크 (전원이 꺼져도 남아요)", fs=12, ha="left", bold=True)
    box(ax, 5.2, 2.1, 6.0, 1.5, fc=NOTE); label(ax, 8.2, 2.85, "디스크에 확정한 세그먼트", fs=10.5)
    box(ax, 12.2, 1.6, 4.5, 2.5, fc=PINK, ec=RED)
    label(ax, 14.45, 3.7, "translog", fs=12, color=RED, bold=True)
    for k, t in enumerate(("1: 문서 1 넣기", "2: 문서 2 넣기", "3: 문서 3 넣기")):
        label(ax, 12.6, 3.1 - k * 0.5, t, fs=10, ha="left", color=INK)
    ax.plot([1.2, 1.2, 11.2], [5.2, 1.0, 1.0], color=RED, lw=1.6)
    arrow(ax, (11.2, 1.0), (12.1, 1.7), color=RED, lw=1.6, ms=14)
    label(ax, 1.5, 3.0, "요청마다 끝에 적고 fsync한 뒤에\n성공이라고 답해요", fs=10, color=RED, ha="left")
    label(ax, 8.6, 0.35, "꺼졌다 켜지면: 디스크의 세그먼트 + translog의 요청을 다시 실행", fs=11, color=INK)
    save(fig, OUT, "es04-translog.svg")


def flush():
    fig, ax = canvas(11, 3.6, 17, 5.6)
    for x0, title, done in ((0.3, "flush 전", False), (9.6, "flush 뒤", True)):
        label(ax, x0, 5.2, title, fs=12, ha="left", bold=True)
        label(ax, x0, 4.5, "세그먼트", fs=10.5, ha="left", color=INK)
        cells(ax, x0, 3.3, ["_0", "_1", "_2"], w=1.2, h=0.9, fs=10.5, dim=() if done else (0, 1, 2))
        label(ax, x0 + 4.5, 3.75, "디스크에 확정" if done else "아직 확정 안 됨", fs=10, ha="left",
              color=INK if done else GREY)
        label(ax, x0, 2.5, "translog에서 다시 실행할 요청", fs=10.5, ha="left", color=INK)
        if done:
            cells(ax, x0, 1.3, ["1", "2", "3"], w=1.2, h=0.9, fs=10.5, dim=(0, 1, 2))
            label(ax, x0 + 4.0, 1.75, "0개", fs=11, ha="left", color=RED, bold=True)
        else:
            cells(ax, x0, 1.3, ["1", "2", "3"], w=1.2, h=0.9, fs=10.5)
            label(ax, x0 + 4.0, 1.75, "3개", fs=11, ha="left", color=INK)
    arrow(ax, (7.2, 2.8), (9.2, 2.8), color=RED, lw=2.5)
    label(ax, 8.2, 3.3, "flush", fs=12, color=RED, bold=True)
    label(ax, 8.5, 0.4, "세그먼트를 모두 fsync 하면 그 전 요청은 다시 실행할 필요가 없어요", fs=10.5, color=INK)
    save(fig, OUT, "es04-flush.svg")


def decide():
    fig, ax = canvas(10, 4.2, 15, 6.4)
    box(ax, 0.3, 4.6, 6.0, 1.3, fc=NOTE)
    label(ax, 3.3, 5.25, "방금 넣은 문서를 바로 봐야 하나요?", fs=10.5, bold=True)
    arrow(ax, (6.4, 5.25), (8.4, 5.25))
    label(ax, 7.4, 5.55, "아니요", fs=10, color=INK)
    box(ax, 8.5, 4.6, 6.2, 1.3, fc=PAPER)
    label(ax, 11.6, 5.25, "그대로 둬요 (1초쯤 뒤 보여요)", fs=10.5)
    arrow(ax, (3.3, 4.5), (3.3, 3.5)); label(ax, 3.6, 4.0, "예", fs=10, color=INK, ha="left")
    box(ax, 0.3, 2.2, 6.0, 1.2, fc=NOTE)
    label(ax, 3.3, 2.8, "그 문서 하나만 다시 보여 주나요?", fs=10.5, bold=True)
    arrow(ax, (6.4, 2.8), (8.4, 2.8)); label(ax, 7.4, 3.1, "예", fs=10, color=INK)
    box(ax, 8.5, 2.2, 6.2, 1.2, fc=PAPER)
    label(ax, 11.6, 2.8, "ID로 꺼내요 (GET)", fs=10.5)
    arrow(ax, (3.3, 2.1), (3.3, 1.3), color=RED); label(ax, 3.6, 1.7, "아니요, 목록 검색에 나와야 해요", fs=10, color=RED, ha="left")
    box(ax, 0.3, 0.1, 6.0, 1.1, fc=PINK, ec=RED)
    label(ax, 3.3, 0.65, "그 요청에만 refresh=wait_for", fs=10.5, color=RED, bold=True)
    save(fig, OUT, "es04-decide.svg")


if __name__ == "__main__":
    open_(); map_(); immutable(); buffer(); get(); translog(); flush(); decide()
