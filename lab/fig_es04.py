"""Elasticsearch 4편 그림 만들기. 실행: python lab/fig_es04.py  → docs/elasticsearch/img/04/*.svg

본문 절은 장면 띠로 그린다: 같은 무대를 여러 장 그리고 장마다 바뀐 곳만 빨강으로 칠한다.
예시는 1편 게시판을 잇는다. 새 글은 8 환불 요청, "내 글" 목록은 4·6·8.
세그먼트 _0 = 문서 1~3(디스크에 확정), _1 = 문서 4·5, _2 = 문서 6·7, 색인 버퍼 = 문서 8.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "es"))
from figkit import (GREY, INK, LIGHT, NOTE, PAPER, PINK, RED, arrow, board, box, bubble,  # noqa: E402
                    canvas, cell, cells, cylinder, label, moral, outdir, save, stage)
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
    if step == 1:
        myboard(ax, MINE[:2], input_hot=True)
        clock(ax, "0초")
        bubble(ax, *SAY, "문서 8을 넣고\n성공이라고 답했어요", TAIL, hot=True)
    elif step == 2:
        myboard(ax, MINE, miss=(8,))
        clock(ax, "0.3초")
        bubble(ax, *SAY, "내 글을 찾아보니\n4번과 6번만 있어요", TAIL, hot=True)
    else:
        myboard(ax, MINE, hot=(8,))
        clock(ax, "1초쯤")
        bubble(ax, *SAY, "이제 8번도 나와요", TAIL, hot=True)
        moral(ax, 4.0, 0.2, "저장은 끝났는데 검색에는 1초쯤 늦게 나와요")


# ── 정렬된 사전에 끼워 넣기 ───────────────────────────────────────
TERMS = ["감사", "배송", "언제", "완료", "요청", "주문", "환불"]


def insert(ax, step):
    label(ax, 0.3, 6.12, "새 문서 4", fs=10.5, ha="left", color=INK)
    cells(ax, 1.6, 5.8, ["사이즈", "교환", "문의"], w=1.1, h=0.65, gap=0.08, hot=(1,) if step == 1 else (), fs=10.5)
    label(ax, 5.35, 6.12, "5", fs=10.5, ha="left", color=INK)
    cell(ax, 5.65, 5.8, 1.0, 0.65, "주문", fs=10.5)
    cell(ax, 6.73, 5.8, 1.55, 0.65, "취소했어요", fs=10)
    label(ax, 7.0, 5.15, "문서 1~3의 용어 사전", fs=11, ha="right", bold=True)
    cells(ax, 0.3, 4.15, TERMS, w=0.88, h=0.7, gap=0.08, fs=10.5)
    if step == 1:
        arrow(ax, (2.75, 5.75), (1.22, 4.92), color=RED, ms=14)
        label(ax, 7.2, 4.5, "감사와 배송 사이에\n들어가야 해요", fs=10.5, ha="left", color=RED)
    on2 = step == 2
    label(ax, 0.3, 3.45, "끼워 넣으면 교환을 넣고 배송부터 끝까지 다시 써요" if step >= 2 else "끼워 넣으면",
          fs=11, ha="left", bold=on2, color=RED if on2 else (GREY if step > 2 else INK))
    if step == 1:
        empty(ax, 0.3, 2.5, 7.6, 0.7)
    else:
        cells(ax, 0.3, 2.5, ["감사", "교환"] + TERMS[1:], w=0.88, h=0.7, gap=0.08,
              hot=range(1, 8) if on2 else (), dim=range(8) if step > 2 else (), fs=10.5)
        if step > 2:
            ax.plot([0.3, 7.9], [2.5, 3.2], color=GREY, lw=1.5)
    on3 = step == 3
    label(ax, 0.3, 1.85, "Lucene은 문서 4·5로 용어 사전을 하나 더 만들어요" if step >= 3 else "Lucene은",
          fs=11, ha="left", bold=on3, color=RED if on3 else INK)
    if step < 3:
        empty(ax, 0.3, 0.85, 6.0, 0.7)
    else:
        x = 0.3
        for t, w in (("교환", 1.0), ("문의", 1.0), ("사이즈", 1.1), ("주문", 1.0), ("취소했어요", 1.55)):
            cell(ax, x, 0.85, w, 0.7, t, hot=on3, fs=10)
            x += w + 0.08
    if step == 4:
        for y in (4.07, 0.77):
            ax.add_patch(Rectangle((0.2, y), 7.0 if y > 1 else 6.25, 0.86, fill=False, ec=RED, lw=2.2))
        label(ax, 7.45, 4.5, "① 여기서 찾고", fs=11, ha="left", color=RED, bold=True)
        label(ax, 6.7, 1.2, "② 여기서도 찾아서", fs=11, ha="left", color=RED, bold=True)
        moral(ax, 6.0, 0.3, "검색은 두 용어 사전을 다 찾아서 합쳐요")


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
    label(ax, 0.3, 3.95, "검색에 보이는 세그먼트", fs=11, ha="left", bold=True)
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
    refresh_stage(ax, buf=step < 3, slot=True, seg3=("hot" if step == 3 else "on") if step >= 3 else None,
                  hot_buf=(step == 1), card_arrow=RED if step == 1 else GREY)
    if step == 1:
        label(ax, 10.0, 4.3, "아직 검색에 안 보여요", fs=10, color=RED)
    elif step == 2:
        search_arrows(ax, 3, RED)
        label(ax, 6.6, 1.1, "찾은 문서: 1, 3", fs=11.5, ha="left", color=RED, bold=True)
        label(ax, 10.0, 4.3, "버퍼는 안 봐요", fs=10, color=RED)
    elif step == 3:
        arrow(ax, (10.3, 4.55), (10.3, 3.65), color=RED, ms=14)
        label(ax, 10.15, 4.1, "refresh (1초마다)", fs=10.5, ha="right", color=RED, bold=True)
    else:
        search_arrows(ax, 4, RED)
        label(ax, 6.6, 1.1, "찾은 문서: 1, 3, 8", fs=11.5, ha="left", color=RED, bold=True)
        moral(ax, 6.0, 0.25, "refresh가 지나야 검색에 나와요")


# ── 메모리와 디스크: translog와 flush ─────────────────────────────
MSEGX = [0.3, 2.7, 5.1]
DSEGX = [0.55, 1.78, 3.01, 4.24]
TLX = [6.4 + k * 1.06 for k in range(5)]


def machine(ax, buf=("문서 8",), buf_hot=False, mem=True, slot=False, seg3=None,
            disk=1, disk_hot=(), tl=4, tl_hot=False, tl_dim=False, off=False, req=True):
    ax.plot([0.2, 11.8], [3.6, 3.6], color=GREY, lw=1.5, ls="--")
    label(ax, 0.3, 6.3, "메모리 · 꺼지면 사라져요", fs=11, ha="left", bold=True)
    label(ax, 0.3, 3.2, "디스크 · 꺼져도 남아요", fs=11, ha="left", bold=True)
    for k, (n, d) in enumerate(SEGS[1:]):
        if mem:
            seg(ax, MSEGX[k], 4.2, 2.0, 1.25, n, d, fs=10)
        else:
            empty(ax, MSEGX[k], 4.2, 2.0, 1.25)
    if seg3:
        seg(ax, MSEGX[2], 4.2, 2.0, 1.25, "세그먼트 _3", "문서 8", hot=(seg3 == "hot"), fs=10)
    elif slot:
        empty(ax, MSEGX[2], 4.2, 2.0, 1.25)
    label(ax, 3.7, 5.75, "운영체제가 들고 있는 세그먼트", fs=9.5, color=INK)
    box(ax, 7.5, 4.2, 2.4, 1.25, fc=LIGHT)
    label(ax, 8.7, 5.75, "색인 버퍼", fs=10, color=INK)
    if buf:
        cell(ax, 7.75, 4.5, 1.9, 0.65, buf[0], hot=buf_hot, fs=10.5)
    if req:
        box(ax, 10.4, 4.45, 1.35, 0.85, fc=PAPER)
        label(ax, 11.07, 4.87, "문서 8\n넣기", fs=10)
    box(ax, 0.3, 0.9, 5.3, 1.85, fc="white")
    label(ax, 2.95, 2.4, "디스크에 확정한 세그먼트", fs=10, color=INK)
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
    if off:
        ax.add_patch(Rectangle((0.2, 3.7), 11.6, 2.85, fc="white", ec="none", alpha=0.55, zorder=5))
        label(ax, 3.7, 4.85, "✗ 전원이 꺼졌어요", fs=15, color=RED, bold=True, zorder=6,
              bbox=dict(boxstyle="round,pad=0.4", fc="white", ec=RED, lw=1.8))


def translog(ax, step):
    if step == 1:
        machine(ax, buf_hot=True)
        arrow(ax, (10.35, 4.87), (9.95, 4.87), color=RED, ms=12)
        label(ax, 8.7, 3.95, "메모리에만 있어요", fs=10, color=RED)
    elif step == 2:
        machine(ax, tl=5, tl_hot=True)
        arrow(ax, (10.35, 4.87), (9.95, 4.87), color=GREY, ms=12)
        arrow(ax, (11.1, 4.4), (11.1, 2.0), color=RED, ms=13)
        label(ax, 6.0, 0.4, "끝에 적고 fsync 한 뒤에 성공이라고 답해요", fs=11, color=RED, bold=True)
    elif step == 3:
        machine(ax, buf=(), mem=False, tl=5, off=True, req=False)
    else:
        machine(ax, buf=("문서 4~8",), buf_hot=True, mem=False, tl=5, req=False)
        label(ax, 2.95, 0.55, "① 확정한 세그먼트를 읽어요", fs=10, color=INK)
        arrow(ax, (8.0, 2.8), (8.5, 4.15), color=RED, ms=13)
        label(ax, 8.65, 3.25, "② 요청을 다시 실행해요", fs=10, ha="left", color=RED, bold=True)
        moral(ax, 8.9, 0.55, "꺼지기 전으로 돌아가요")


def flush(ax, step):
    if step == 1:
        machine(ax, tl=5, slot=True, req=False)
        label(ax, 9.0, 0.5, "다시 켜면 다시 실행할 요청 5개", fs=11, color=RED, bold=True)
    elif step == 2:
        machine(ax, buf=(), seg3="hot", tl=5, req=False)
        arrow(ax, (8.0, 5.5), (6.5, 5.5), color=RED, ms=13, rad=0.5)
        label(ax, 6.1, 3.9, "검색에는 다음 refresh 뒤에", fs=9.5, color=RED)
    elif step == 3:
        machine(ax, buf=(), seg3="on", disk=4, disk_hot=(1, 2, 3), tl=5, req=False)
        ax.add_patch(Rectangle((0.15, 4.08), 7.1, 1.42, fill=False, ec=RED, lw=2.0, ls="--"))
        arrow(ax, (5.4, 4.05), (4.95, 1.95), color=RED, ms=14)
        label(ax, 5.45, 3.2, "fsync", fs=11, ha="left", color=RED, bold=True)
    else:
        machine(ax, buf=(), seg3="on", disk=4, tl=5, tl_dim=True, req=False)
        label(ax, 9.0, 0.5, "다시 실행할 요청 0개", fs=11, color=RED, bold=True)
        moral(ax, 2.95, 0.5, "flush 뒤엔 다시 할 일이 없어요", fs=11)


# ── GET은 refresh 전에도 찾아요 ────────────────────────────────────
GETB = (9.4, 0.75, 2.3, 0.7)


def get(ax, step):
    refresh_stage(ax)
    box(ax, *GETB, fc=PINK if step == 2 else PAPER, ec=RED if step == 2 else INK)
    label(ax, GETB[0] + GETB[2] / 2, GETB[1] + 0.35, "GET _doc/8", fs=11.5, color=RED if step == 2 else "#222")
    search_arrows(ax, 3, RED if step == 1 else GREY)
    label(ax, 6.6, 1.1, "찾은 문서: 1, 3", fs=11, ha="left", color=RED if step == 1 else INK, bold=(step == 1))
    if step == 2:
        arrow(ax, (10.95, 1.5), (10.95, 4.55), color=RED, ms=14)
        label(ax, 10.8, 3.4, "ID로 따로\n꺼내 와요", fs=10.5, ha="right", color=RED)
        cell(ax, 9.1, 5.0, 1.8, 0.7, "문서 8", hot=True, fs=11)
        moral(ax, 6.0, 0.25, "ID로 꺼내는 GET은 refresh 전에도 찾아요")


# ── refresh=wait_for ───────────────────────────────────────────────
TX = {0: 1.0, 1: 6.0, 2: 11.0}


def waitfor(ax, step):
    ax.plot([0.6, 11.4], [3.0, 3.0], color=INK, lw=1.6)
    for t in (0, 1, 2):
        ax.plot([TX[t], TX[t]], [2.85, 3.15], color=INK, lw=1.6)
        label(ax, TX[t], 2.55, f"{t}초", fs=10, color=INK)
    for t in (1, 2):
        on = step == 2 and t == 1
        label(ax, TX[t], 3.45, "refresh", fs=10.5, color=RED if on else INK, bold=on)
    box(ax, 0.5, 4.6, 3.9, 1.1, fc=PAPER)
    label(ax, 2.45, 5.15, "문서 8 넣기\nrefresh=wait_for", fs=10.5)
    arrow(ax, (1.0, 4.55), (1.0, 3.1), color=GREY, ms=12)
    ax.plot([1.1, 5.9], [3.95, 3.95], color=RED if step == 1 else GREY, lw=2.2)
    ax.plot([5.9, 5.9], [3.8, 4.1], color=RED if step == 1 else GREY, lw=2.2)
    label(ax, 3.5, 4.25, "기다려요", fs=11, color=RED if step == 1 else INK, bold=(step == 1))
    if step >= 2:
        box(ax, 6.6, 4.6, 2.2, 0.8, fc=PINK if step == 2 else NOTE, ec=RED if step == 2 else INK)
        label(ax, 7.7, 5.0, "성공", fs=12, color=RED if step == 2 else "#222", bold=(step == 2))
        arrow(ax, (6.3, 3.75), (6.9, 4.55), color=RED if step == 2 else GREY, ms=12)
    if step == 3:
        box(ax, 6.6, 0.9, 4.6, 0.8, fc=PINK, ec=RED)
        label(ax, 8.9, 1.3, "내 글 검색: 4, 6, 8", fs=11.5, color=RED, bold=True)
        arrow(ax, (7.7, 4.55), (8.4, 1.75), color=RED, ms=12)
        moral(ax, 6.0, 0.3, "답을 받은 뒤에 검색하면 방금 쓴 글이 들어 있어요")


# ── 옮기는 동안 refresh 끄기 ───────────────────────────────────────
def bulk(ax, step):
    on = step == 2
    label(ax, 0.3, 6.1, "refresh_interval: -1" if on else "refresh 1초마다", fs=12, ha="left", bold=True,
          color=RED if on else "#222")
    cell(ax, 0.3, 3.7, 3.0, 1.2, "옛 게시판 글\n수백만 개", fc=PAPER, fs=11)
    arrow(ax, (3.4, 4.3), (4.1, 4.3), ms=12)
    box(ax, 4.2, 3.6, 2.4, 1.4, fc=LIGHT)
    label(ax, 5.4, 4.3, "색인 버퍼", fs=10.5, color=INK)
    arrow(ax, (6.7, 4.3), (7.4, 4.3), ms=12)
    box(ax, 7.5, 1.9, 4.2, 3.6, fc="white")
    label(ax, 9.6, 5.15, "새 인덱스의 세그먼트", fs=10.5, color=INK)
    if not on:
        for r in range(3):
            for c in range(5):
                cell(ax, 7.75 + c * 0.78, 3.95 - r * 0.8, 0.62, 0.6, "", fs=8)
        label(ax, 9.6, 1.45, "1초마다 하나씩 만들어요", fs=10.5, color=INK)
    else:
        cell(ax, 7.8, 3.3, 1.75, 1.3, "", hot=True)
        cell(ax, 9.7, 3.3, 1.75, 1.3, "", hot=True)
        label(ax, 9.6, 1.45, "버퍼가 찰 때만 만들어요", fs=10.5, color=RED)
        moral(ax, 6.0, 0.5, "다 옮긴 뒤에는 원래 간격으로 돌려놓아요")


# ── 판단 (한 장) ───────────────────────────────────────────────────
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


# ── 정리: 처음 장면으로 돌아가기 ───────────────────────────────────
def back(ax, step):
    es(ax)
    if step == 1:
        myboard(ax, MINE, miss=(8,))
        clock(ax, "처음")
        bubble(ax, *SAY, "저장하자마자 찾아서\n8번이 없었어요", TAIL)
    elif step == 2:
        myboard(ax, MINE[:2], tag="+ refresh=wait_for")
        clock(ax, "0초 저장 → 1초 답")
        bubble(ax, *SAY, "다음 refresh가 끝나면\n성공이라고 답할게요", TAIL, hot=True)
    else:
        myboard(ax, MINE, hot=(8,))
        clock(ax, "답을 받은 뒤")
        bubble(ax, *SAY, "내 글을 찾으니\n8번이 있어요", TAIL, hot=True)
        moral(ax, 4.0, 0.2, "refresh를 기다렸다 답하면 바로 보여요")


# ── 정리: 낱말 카드 ────────────────────────────────────────────────
def cards():
    fig, ax = canvas(6.4, 10.4, 9.8, 16.25)
    W, H = 4.6, 3.8

    def card(i, name, line):
        col, row = i % 2, i // 2
        x, y = 0.2 + col * 4.9, 12.25 - row * 4.05
        box(ax, x, y, W, H, fc="white")
        label(ax, x + 0.25, y + H - 0.4, name, fs=12.5, ha="left", bold=True)
        label(ax, x + W / 2, y + 0.6, line, fs=10, color=INK)
        return x, y

    x, y = card(0, "세그먼트", "한 번 만들고 고치지 않는\n작은 역색인")
    cells(ax, x + 0.4, y + 1.6, ["_0", "_1", "_2"], w=1.2, h=0.8, gap=0.1, hot=(2,), fs=11)
    x, y = card(1, "색인 버퍼", "세그먼트로 만들기 전에\n문서를 모으는 메모리 자리")
    box(ax, x + 1.0, y + 1.45, 2.6, 1.15, fc=LIGHT, lw=1.3)
    cell(ax, x + 1.5, y + 1.7, 1.6, 0.65, "문서 8", hot=True, fs=10.5)
    x, y = card(2, "refresh", "버퍼를 세그먼트로 만들어\n검색에 내놓는 일")
    box(ax, x + 0.4, y + 1.5, 1.5, 0.95, fc=LIGHT, lw=1.3)
    label(ax, x + 1.15, y + 1.97, "버퍼", fs=10, color=INK)
    arrow(ax, (x + 2.0, y + 1.97), (x + 2.6, y + 1.97), color=RED, ms=11)
    cell(ax, x + 2.7, y + 1.55, 1.5, 0.85, "_3", hot=True, fs=11)
    x, y = card(3, "fsync", "파일 내용을 지금 당장\n디스크에 쓰게 하는 일")
    cell(ax, x + 0.4, y + 1.6, 1.5, 0.8, "메모리", fc=LIGHT, fs=10)
    arrow(ax, (x + 2.0, y + 2.0), (x + 2.6, y + 2.0), color=RED, ms=11)
    cell(ax, x + 2.7, y + 1.6, 1.5, 0.8, "디스크", hot=True, fs=10)
    x, y = card(4, "translog", "요청을 끝에 덧붙여 적고\nfsync 하는 기록 파일")
    cells(ax, x + 0.3, y + 1.65, ["4", "5", "6", "7", "8"], w=0.72, h=0.7, gap=0.08, hot=(4,), fs=10.5)
    x, y = card(5, "flush", "세그먼트를 디스크에 확정해\n다시 실행할 요청을 없애는 일")
    cells(ax, x + 0.3, y + 2.15, ["_0", "_1", "_2", "_3"], w=0.9, h=0.6, gap=0.08, hot=range(4), fs=10)
    cells(ax, x + 0.3, y + 1.35, ["4", "5", "6", "7", "8"], w=0.66, h=0.55, gap=0.06, dim=range(5), fs=9.5)
    x, y = card(6, "GET", "ID로 문서 하나를 꺼내는 요청\nrefresh를 기다리지 않아요")
    cell(ax, x + 0.3, y + 1.6, 2.0, 0.8, "GET _doc/8", fc=PAPER, fs=10)
    arrow(ax, (x + 2.4, y + 2.0), (x + 2.9, y + 2.0), color=RED, ms=11)
    cell(ax, x + 3.0, y + 1.6, 1.3, 0.8, "문서 8", hot=True, fs=10)
    x, y = card(7, "refresh=wait_for", "다음 refresh가 끝난 뒤에\n성공이라고 답하게 하는 표시")
    ax.plot([x + 0.4, x + 4.2], [y + 1.75, y + 1.75], color=INK, lw=1.3)
    ax.plot([x + 0.9, x + 3.0], [y + 2.2, y + 2.2], color=RED, lw=2.0)
    label(ax, x + 1.95, y + 2.5, "기다려요", fs=9.5, color=RED)
    ax.plot([x + 3.0, x + 3.0], [y + 1.6, y + 1.9], color=RED, lw=2.0)
    label(ax, x + 3.0, y + 1.38, "refresh", fs=9, color=RED)
    save(fig, OUT, "es04-cards.svg")


if __name__ == "__main__":
    S, L = (7.2, 3.8), (12, 6.6)
    stage(opening, 3, OUT, "es04-open", S, L)
    stage(insert, 4, OUT, "es04-insert", S, L)
    stage(refresh, 4, OUT, "es04-refresh", S, L)
    stage(translog, 4, OUT, "es04-translog", S, L)
    stage(flush, 4, OUT, "es04-flush", S, L)
    stage(get, 2, OUT, "es04-get", S, L)
    stage(waitfor, 3, OUT, "es04-wait", S, L)
    decide()
    stage(bulk, 2, OUT, "es04-bulk", S, L)
    stage(back, 3, OUT, "es04-back", S, L)
    cards()
