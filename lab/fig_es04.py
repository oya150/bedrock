"""Elasticsearch 4편 그림 만들기. 실행: python lab/fig_es04.py  → docs/elasticsearch/img/04/*.svg

그림 10장. 그림 안 글씨는 낱말과 숫자만 둔다. 지금 볼 곳만 빨강.
예시는 1편 게시판을 잇는다. 새 글은 8 환불 요청, "내 글" 목록은 4·6·8.
세그먼트 _0 = 문서 1~3(디스크에 확정), _1 = 문서 4·5, _2 = 문서 6·7, 색인 버퍼 = 문서 8.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "es"))
from figkit import (GREY, INK, LIGHT, NOTE, PAPER, PINK, RED, arrow, board, box, bubble,  # noqa: E402
                    canvas, cell, cells, cylinder, label, outdir, save, stage)
from matplotlib.patches import Rectangle  # noqa: E402

OUT = outdir("04")
MINE = [(4, "사이즈 교환 문의"), (6, "색상이 달라요"), (8, "환불 요청")]
CYL = (8.0, 3.0, 3.9, 1.7)
SAY = (7.3, 0.55, 4.6, 1.3)
TAIL = (9.95, 2.75)


def empty(ax, x, y, w, h):
    ax.add_patch(Rectangle((x, y), w, h, fc="white", ec=GREY, lw=1.0, ls="--"))


def seg(ax, x, y, w, h, name, docs, hot=False, dim=False, fs=10.5):
    """세그먼트 상자 하나: 위에 이름, 아래에 든 문서."""
    ec = RED if hot else (GREY if dim else INK)
    box(ax, x, y, w, h, fc=PINK if hot else (LIGHT if dim else NOTE), ec=ec, lw=2.0 if hot else 1.5)
    c = RED if hot else (GREY if dim else "#222")
    label(ax, x + w / 2, y + h * 0.68, name, fs=fs, color=c, bold=hot)
    label(ax, x + w / 2, y + h * 0.3, docs, fs=fs - 1, color=RED if hot else (GREY if dim else INK))


# ── 게시판 화면: 글쓰기 칸과 "내 글" 목록 ─────────────────────────
def myboard(ax, posts, hot=(), miss=(), input_hot=False, tag=None):
    board(ax, posts, query="", hot=hot, miss=miss, footer="내 글 목록")
    ec = RED if input_hot else INK
    ax.add_patch(Rectangle((0.85, 5.2), 4.6, 0.5, fc="white", ec=ec, lw=1.8 if input_hot else 1.2, zorder=3))
    label(ax, 1.05, 5.45, "환불 요청", fs=12, ha="left", zorder=4)
    if tag:
        label(ax, 7.15, 5.45, tag, fs=9.5, ha="left", color=RED, bold=True,
              bbox=dict(boxstyle="round,pad=0.3", fc=PINK, ec=RED, lw=1.4))
    ax.add_patch(Rectangle((5.55, 5.2), 1.2, 0.5, fc=PINK if input_hot else LIGHT, ec=ec, lw=1.2, zorder=3))
    label(ax, 6.15, 5.45, "저장", fs=11.5, color=RED if input_hot else "#222", zorder=4)


def clock(ax, s, hot=False):
    label(ax, 9.95, 6.15, s, fs=12.5, color=RED if hot else INK, bold=True)


def es(ax):
    cylinder(ax, *CYL, "ES")


# ── 여는 장면: 방금 쓴 글이 목록에 없어요 ─────────────────────────
def opening(ax, step):
    es(ax)
    myboard(ax, MINE, miss=(8,))
    clock(ax, "0.3초")
    bubble(ax, *SAY, "문서 8 저장: 성공\n내 글 검색: 4, 6", TAIL, hot=True)


# ── 정렬된 용어 사전에 끼워 넣기 ───────────────────────────────────
TERMS = ["감사", "배송", "언제", "완료", "요청", "주문", "환불"]


def new_docs(ax, hot_word):
    label(ax, 0.3, 6.12, "새 문서 4", fs=10.5, ha="left", color=INK)
    cells(ax, 1.6, 5.8, ["사이즈", "교환", "문의"], w=1.1, h=0.65, gap=0.08, hot=(1,) if hot_word else (), fs=10.5)
    label(ax, 5.35, 6.12, "5", fs=10.5, ha="left", color=INK)
    cell(ax, 5.65, 5.8, 1.0, 0.65, "주문", fs=10.5)
    cell(ax, 6.73, 5.8, 1.55, 0.65, "취소했어요", fs=10)


def insert(ax, step):
    new_docs(ax, step == 1)
    if step == 1:
        label(ax, 7.2, 4.5, "문서 1~3의 용어 사전", fs=11, ha="left", bold=True)
        cells(ax, 0.3, 4.15, TERMS, w=0.88, h=0.7, gap=0.08, fs=10.5)
        arrow(ax, (2.75, 5.75), (1.22, 4.92), color=RED, ms=14)
        label(ax, 8.2, 2.65, "교환을 끼운 뒤", fs=11, ha="left", bold=True)
        cells(ax, 0.3, 2.3, ["감사", "교환"] + TERMS[1:], w=0.88, h=0.7, gap=0.08, hot=range(1, 8), fs=10.5)
        label(ax, 4.3, 1.75, "다시 쓰는 칸 7개", fs=11, color=RED, bold=True)
        ax.plot([1.26, 7.9], [2.15, 2.15], color=RED, lw=1.6)
    else:
        label(ax, 0.3, 5.15, "문서 1~3의 용어 사전", fs=11, ha="left", bold=True)
        cells(ax, 0.3, 4.15, TERMS, w=0.88, h=0.7, gap=0.08, fs=10.5)
        label(ax, 0.3, 3.3, "문서 4·5의 용어 사전 (새로 만듦)", fs=11, ha="left", bold=True, color=RED)
        x = 0.3
        for t, w in (("교환", 1.0), ("문의", 1.0), ("사이즈", 1.1), ("주문", 1.0), ("취소했어요", 1.55)):
            cell(ax, x, 2.3, w, 0.7, t, hot=True, fs=10)
            x += w + 0.08
        box(ax, 9.0, 1.0, 2.6, 0.75, fc=PAPER)
        label(ax, 10.3, 1.37, "검색", fs=11.5)
        arrow(ax, (10.0, 1.8), (7.0, 4.15), color=INK, ms=12, lw=1.5)
        arrow(ax, (9.6, 1.6), (6.5, 2.65), color=INK, ms=12, lw=1.5)
        label(ax, 9.6, 3.6, "둘 다 찾기", fs=10.5, ha="left", color=INK)


# ── 색인 버퍼와 refresh ────────────────────────────────────────────
SEGX = [0.3, 3.2, 6.1, 9.0]
SEGS = [("세그먼트 _0", "문서 1, 2, 3"), ("세그먼트 _1", "문서 4, 5"), ("세그먼트 _2", "문서 6, 7")]
SEARCH = (3.6, 0.75, 2.8, 0.7)


def refresh_stage(ax, buf=True, slot=False, seg3=None, hot_buf=False, card_arrow=None):
    cell(ax, 0.3, 5.0, 3.4, 0.75, "새 문서 8: 환불 요청", fc=PAPER, fs=11)
    arrow(ax, (3.8, 5.37), (8.3, 5.37), color=card_arrow or GREY, ms=13)
    box(ax, 8.4, 4.6, 3.2, 1.5, fc=LIGHT)
    label(ax, 10.0, 6.4, "메모리의 색인 버퍼", fs=10.5, color=INK)
    if buf:
        cell(ax, 9.1, 5.0, 1.8, 0.7, "문서 8", hot=hot_buf, fs=11)
    label(ax, 0.3, 3.95, "세그먼트", fs=11, ha="left", bold=True)
    for k, (n, d) in enumerate(SEGS):
        seg(ax, SEGX[k], 2.4, 2.6, 1.2, n, d)
    if seg3:
        seg(ax, SEGX[3], 2.4, 2.6, 1.2, "세그먼트 _3", "문서 8", hot=(seg3 == "hot"))
    elif slot:
        empty(ax, SEGX[3], 2.4, 2.6, 1.2)
    box(ax, *SEARCH, fc=PAPER)
    label(ax, SEARCH[0] + SEARCH[2] / 2, SEARCH[1] + 0.35, "검색: 환불", fs=11.5)


def search_arrows(ax, n, color):
    for k in range(n):
        arrow(ax, (5.0, 1.5), (SEGX[k] + 1.3, 2.33), color=color, ms=12, lw=1.6)


def refresh(ax, step):
    if step == 1:
        refresh_stage(ax, slot=True, hot_buf=True, card_arrow=RED)
        search_arrows(ax, 3, INK)
        label(ax, 6.6, 1.1, "찾은 문서: 1, 3", fs=11.5, ha="left", color=INK, bold=True)
    else:
        refresh_stage(ax, buf=False, seg3="hot")
        arrow(ax, (10.3, 4.55), (10.3, 3.65), color=RED, ms=14)
        label(ax, 10.15, 4.1, "refresh · 1초마다", fs=10.5, ha="right", color=RED, bold=True)
        search_arrows(ax, 4, INK)
        label(ax, 6.6, 1.1, "찾은 문서: 1, 3, 8", fs=11.5, ha="left", color=RED, bold=True)


# ── 메모리와 디스크: translog와 flush ─────────────────────────────
MSEGX = [0.3, 2.7, 5.1]
DSEGX = [0.55, 1.78, 3.01, 4.24]
TLX = [6.4 + k * 1.06 for k in range(5)]


def machine(ax, buf=("문서 8",), buf_hot=False, mem=True, slot=False, seg3=None,
            disk=1, disk_hot=(), tl=4, tl_hot=False, tl_dim=False, req=True):
    ax.plot([0.2, 11.8], [3.6, 3.6], color=GREY, lw=1.5, ls="--")
    label(ax, 0.3, 6.3, "메모리 (꺼지면 사라짐)", fs=11, ha="left", bold=True)
    label(ax, 0.3, 3.2, "디스크 (꺼져도 남음)", fs=11, ha="left", bold=True)
    for k, (n, d) in enumerate(SEGS[1:]):
        if mem:
            seg(ax, MSEGX[k], 4.2, 2.0, 1.25, n, d, fs=10)
        else:
            empty(ax, MSEGX[k], 4.2, 2.0, 1.25)
    if seg3:
        seg(ax, MSEGX[2], 4.2, 2.0, 1.25, "세그먼트 _3", "문서 8", hot=(seg3 == "hot"), fs=10)
    elif slot:
        empty(ax, MSEGX[2], 4.2, 2.0, 1.25)
    label(ax, 3.7, 5.75, "fsync 전 세그먼트", fs=9.5, color=INK)
    box(ax, 7.5, 4.2, 2.4, 1.25, fc=LIGHT)
    label(ax, 8.7, 5.75, "색인 버퍼", fs=10, color=INK)
    if buf:
        cell(ax, 7.75, 4.5, 1.9, 0.65, buf[0], hot=buf_hot, fs=10.5)
    if req:
        box(ax, 10.4, 4.45, 1.35, 0.85, fc=PAPER)
        label(ax, 11.07, 4.87, "문서 8\n넣기", fs=10)
    box(ax, 0.3, 0.9, 5.3, 1.85, fc="white")
    label(ax, 2.95, 2.4, "확정한 세그먼트", fs=10, color=INK)
    for k in range(4):
        if k < disk:
            cell(ax, DSEGX[k], 1.15, 1.15, 0.75, f"_{k}", hot=(k in disk_hot), fs=10.5)
        else:
            empty(ax, DSEGX[k], 1.15, 1.15, 0.75)
    box(ax, 6.2, 0.9, 5.6, 1.85, fc="white", ec=RED if tl_hot else INK)
    label(ax, 8.6, 2.4, "translog", fs=11.5, bold=True, color=RED if tl_hot else INK)
    for k in range(5):
        if k < tl:
            cell(ax, TLX[k], 1.15, 0.98, 0.75, f"문서 {k + 4}", hot=(tl_hot and k == 4), dim=tl_dim, fs=9.5)
        else:
            empty(ax, TLX[k], 1.15, 0.98, 0.75)


def translog(ax, step):
    if step == 1:
        machine(ax, tl=5, tl_hot=True)
        arrow(ax, (10.35, 4.87), (9.95, 4.87), color=INK, ms=12)
        arrow(ax, (11.1, 4.4), (11.1, 2.0), color=RED, ms=13)
        label(ax, 11.25, 3.25, "fsync → 성공", fs=10.5, ha="left", color=RED, bold=True)
    else:
        machine(ax, buf=("문서 4~8",), buf_hot=True, mem=False, tl=5, req=False)
        label(ax, 11.7, 6.3, "다시 켠 뒤", fs=11, ha="right", color=INK, bold=True)
        label(ax, 2.95, 0.55, "① 세그먼트 읽기", fs=10.5, color=INK)
        arrow(ax, (8.0, 2.8), (8.5, 4.15), color=RED, ms=13)
        label(ax, 8.65, 3.25, "② 요청 다시 실행", fs=10.5, ha="left", color=RED, bold=True)


def flush(ax, step):
    machine(ax, buf=(), seg3="on", disk=4, disk_hot=(1, 2, 3), tl=5, tl_dim=True, req=False)
    ax.add_patch(Rectangle((0.15, 4.08), 7.1, 1.42, fill=False, ec=RED, lw=2.0, ls="--"))
    arrow(ax, (5.4, 4.05), (4.95, 1.95), color=RED, ms=14)
    label(ax, 5.45, 3.2, "fsync", fs=11, ha="left", color=RED, bold=True)
    label(ax, 9.0, 0.5, "다시 실행할 요청 0개", fs=11, color=RED, bold=True)


# ── GET은 refresh 전에도 찾아요 ────────────────────────────────────
GETB = (9.4, 0.75, 2.3, 0.7)


def get(ax, step):
    refresh_stage(ax)
    box(ax, *GETB, fc=PINK, ec=RED)
    label(ax, GETB[0] + GETB[2] / 2, GETB[1] + 0.35, "GET _doc/8", fs=11.5, color=RED)
    search_arrows(ax, 3, GREY)
    label(ax, 6.6, 1.1, "찾은 문서: 1, 3", fs=11, ha="left", color=INK)
    arrow(ax, (10.95, 1.5), (10.95, 4.55), color=RED, ms=14)
    label(ax, 10.8, 3.4, "ID로\n꺼내기", fs=10.5, ha="right", color=RED)
    cell(ax, 9.1, 5.0, 1.8, 0.7, "문서 8", hot=True, fs=11)


# ── refresh=wait_for ───────────────────────────────────────────────
TX = {0: 1.0, 1: 6.0, 2: 11.0}


def waitfor(ax, step):
    ax.plot([0.6, 11.4], [3.0, 3.0], color=INK, lw=1.6)
    for t in (0, 1, 2):
        ax.plot([TX[t], TX[t]], [2.85, 3.15], color=INK, lw=1.6)
        label(ax, TX[t], 2.55, f"{t}초", fs=10, color=INK)
    for t in (1, 2):
        on = t == 1
        label(ax, TX[t], 3.45, "refresh", fs=10.5, color=RED if on else INK, bold=on)
    box(ax, 0.5, 4.6, 3.9, 1.1, fc=PAPER)
    label(ax, 2.45, 5.15, "문서 8 넣기\nrefresh=wait_for", fs=10.5)
    arrow(ax, (1.0, 4.55), (1.0, 3.1), color=INK, ms=12)
    ax.plot([1.1, 5.9], [3.95, 3.95], color=RED, lw=2.2)
    ax.plot([5.9, 5.9], [3.8, 4.1], color=RED, lw=2.2)
    label(ax, 3.5, 4.25, "기다려요", fs=11, color=RED, bold=True)
    box(ax, 6.6, 4.6, 2.2, 0.8, fc=PINK, ec=RED)
    label(ax, 7.7, 5.0, "성공", fs=12, color=RED, bold=True)
    arrow(ax, (6.3, 3.75), (6.9, 4.55), color=RED, ms=12)
    box(ax, 6.6, 0.9, 4.6, 0.8, fc=NOTE)
    label(ax, 8.9, 1.3, "내 글 검색: 4, 6, 8", fs=11.5)
    arrow(ax, (7.7, 4.55), (8.4, 1.75), color=INK, ms=12)


def one(draw, name, size, lim):
    fig, ax = canvas(*size, *lim)
    ax.add_patch(Rectangle((0, 0), *lim, fill=False, ec="none"))
    draw(ax, 1)
    save(fig, OUT, name)


if __name__ == "__main__":
    S, L = (7.2, 3.8), (12, 6.6)
    one(opening, "es04-open.svg", S, L)
    stage(insert, 2, OUT, "es04-insert", S, L)
    stage(refresh, 2, OUT, "es04-refresh", S, L)
    stage(translog, 2, OUT, "es04-translog", S, L)
    one(flush, "es04-flush.svg", S, L)
    one(get, "es04-get.svg", S, L)
    one(waitfor, "es04-wait.svg", S, L)
