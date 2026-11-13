"""Elasticsearch 2편 그림 만들기. 실행: python lab/fig_es02.py  → docs/elasticsearch/img/02/*.svg

그림마다 한 장. 그림 안 글씨는 낱말과 숫자만 두고 지금 볼 곳만 빨강으로 칠한다.
예시는 1편 게시판을 잇는다(글 1 주문 환불 요청, 3 환불 완료 감사, 9 환불했어요 감사).
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "es"))
from figkit import (BOARD_ROW_Y, GREY, INK, NOTE, PAPER, PINK, RED, arrow, board, box,  # noqa: E402
                    canvas, cell, cells, cylinder, label, outdir, save)
from matplotlib.patches import Rectangle  # noqa: E402

OUT = outdir("02")
POSTS = [(1, "주문 환불 요청"), (2, "주문 배송 언제"), (3, "환불 완료 감사"), None, (9, "환불했어요 감사")]
ROW9 = BOARD_ROW_Y[4]
CYL = (8.0, 3.0, 3.9, 1.7)
STD = [("환불", [1, 3, "⋯"]), ("환불했어요", [9])]
NORI = [("환불", [1, 3, 9, "⋯"]), ("감사", [3, 9])]


def empty(ax, x, y, w, h):
    ax.add_patch(Rectangle((x, y), w, h, fc="white", ec=GREY, lw=1.0, ls="--"))


def dictionary(ax, rows, hot_word=None, hot_nums=(), lost_word=None, name="ES (용어 사전)", name_hot=False):
    """원통 안에 용어 사전 두 줄."""
    x, y, w, h = CYL
    cylinder(ax, *CYL, name, ec=RED if name_hot else "#555", color=RED if name_hot else "#222")
    for k, (t, ds) in enumerate(rows):
        yy = y + 0.95 - k * 0.65
        cell(ax, x + 0.15, yy, 1.7, 0.5, t, hot=(t == hot_word), fs=10)
        if t == lost_word:
            ax.add_patch(Rectangle((x + 0.15, yy), 1.7, 0.5, fill=False, ec=RED, lw=1.8, ls="--"))
        cells(ax, x + 1.95, yy, ds, w=0.42, h=0.5, gap=0.04,
              hot=[i for i, d in enumerate(ds) if (t, d) in hot_nums], fs=9.5)


S, L = (7.2, 3.8), (12, 6.6)


def one(draw, name, size=S, lim=L):
    fig, ax = canvas(*size, *lim)
    ax.add_patch(Rectangle((0, 0), *lim, fill=False, ec="none"))
    draw(ax)
    save(fig, OUT, name)


# ── 1. 환불로 찾았는데 9번이 안 나와요 ─────────────────────────────
def miss(ax):
    board(ax, POSTS, hot=(1, 3), miss=(9,))
    dictionary(ax, STD, hot_word="환불", hot_nums={("환불", 1), ("환불", 3)}, lost_word="환불했어요")


# ── 2. 분석기 세 단계 ──────────────────────────────────────────────
COLX = [0.15, 3.1, 6.05, 9.0]
STATIONS = [("문자 필터", "태그 지우기"), ("토크나이저", "띄어쓰기에서 자르기"), ("토큰 필터", "소문자로")]
DOC = [["<b>Refund</b> 요청"], ["Refund 요청"], ["Refund", "요청"], ["refund", "요청"]]
ASK = [["REFUND"], ["REFUND"], ["REFUND"], ["refund"]]


def row_cells(ax, col, items, y, hot=False):
    x, W = COLX[col], 2.7
    if len(items) == 1:
        cell(ax, x, y, W, 0.7, items[0], hot=hot, fs=9.5 if col == 0 else 10.5)
    else:
        cells(ax, x, y, items, w=1.3, h=0.7, gap=0.1, hot=(0,) if hot else (), fs=10.5)


def pipeline(ax):
    for i, (name, what) in enumerate(STATIONS):
        box(ax, COLX[i + 1], 5.55, 2.7, 0.75, fc=PAPER, ec="#555")
        label(ax, COLX[i + 1] + 1.35, 5.92, name, fs=11.5, bold=True)
        label(ax, COLX[i + 1] + 1.35, 5.2, what, fs=10, color=INK)
    label(ax, 0.2, 4.55, "글", fs=11.5, ha="left", bold=True)
    label(ax, 0.2, 2.55, "검색어", fs=11.5, ha="left", bold=True)
    for c in range(4):
        row_cells(ax, c, DOC[c], 3.5, hot=(c == 3))
        row_cells(ax, c, ASK[c], 1.5, hot=(c == 3))
        if c < 3:
            arrow(ax, (COLX[c] + 2.75, 3.85), (COLX[c + 1] - 0.05, 3.85), ms=11, lw=1.3)
            arrow(ax, (COLX[c] + 2.75, 1.85), (COLX[c + 1] - 0.05, 1.85), ms=11, lw=1.3)


# ── 2. match와 term ───────────────────────────────────────────────
def termmatch(ax):
    label(ax, 10.4, 6.0, "용어 사전", fs=11.5, bold=True)
    cell(ax, 9.2, 4.9, 2.4, 0.7, "refund", fs=11)
    cell(ax, 9.2, 4.1, 2.4, 0.7, "request", fs=11)
    label(ax, 0.2, 5.95, "match", fs=12, ha="left", bold=True)
    cell(ax, 0.2, 4.9, 1.8, 0.7, "Refund", fs=11)
    arrow(ax, (2.1, 5.25), (2.9, 5.25), ms=12)
    box(ax, 3.0, 4.85, 2.2, 0.8, fc=PAPER)
    label(ax, 4.1, 5.25, "분석기", fs=11)
    arrow(ax, (5.3, 5.25), (6.1, 5.25), ms=12)
    cell(ax, 6.2, 4.9, 1.8, 0.7, "refund", hot=True, fs=11)
    arrow(ax, (8.1, 5.25), (9.1, 5.25), color=RED, ms=12)
    label(ax, 10.4, 3.6, "1건", fs=12, color=RED, bold=True)
    label(ax, 0.2, 3.05, "term", fs=12, ha="left", bold=True)
    cell(ax, 0.2, 2.0, 1.8, 0.7, "Refund", fs=11)
    arrow(ax, (2.1, 2.35), (6.1, 2.35), ms=12)
    label(ax, 4.1, 2.75, "그대로", fs=11, color=INK)
    cell(ax, 6.2, 2.0, 1.8, 0.7, "Refund", hot=True, fs=11)
    label(ax, 8.4, 2.35, "사전에 없음", fs=11, ha="left", color=INK)
    label(ax, 11.2, 2.35, "0건", fs=12, color=RED, bold=True)


# ── 3. 기본 분석기 ────────────────────────────────────────────────
def standard():
    fig, ax = canvas(10, 1.6, 15, 2.4)
    cell(ax, 0.3, 1.0, 4.8, 0.8, "환불했어요. Refund-Request!", fc=PAPER, fs=11)
    arrow(ax, (5.2, 1.4), (6.4, 1.4))
    label(ax, 5.8, 1.95, "기본 분석기", fs=10, color=INK)
    cells(ax, 6.5, 1.0, ["환불했어요", "refund", "request"], w=2.5, h=0.8, hot=(0,), fs=11)
    label(ax, 7.75, 0.5, "덩어리째", fs=10, color=RED)
    label(ax, 11.4, 0.5, "하이픈에서 자름 · 소문자", fs=10, color=INK)
    save(fig, OUT, "es02-standard.svg")


# ── 4. 형태소로 자르기 ────────────────────────────────────────────
PARTS = [("환불", "명사"), ("하", "접미사"), ("았", "어미"), ("어요", "어미")]


def nori(ax):
    label(ax, 0.3, 6.1, "글 9의 낱말", fs=11.5, ha="left", color=INK)
    cell(ax, 0.3, 5.0, 2.6, 0.75, "환불했어요", fc=PAPER, fs=12)
    label(ax, 0.3, 4.35, "띄어쓰기", fs=10.5, ha="left", color=INK)
    cell(ax, 3.7, 4.05, 2.6, 0.75, "환불했어요", fs=11.5, dim=True)
    label(ax, 0.3, 3.0, "형태소", fs=10.5, ha="left", color=RED)
    x = 3.7
    for k, (m, pos) in enumerate(PARTS):
        gone = k > 0
        cell(ax, x, 2.6, 1.3, 0.75, m, hot=not gone, dim=gone, fs=12)
        label(ax, x + 0.65, 2.3, pos, fs=10, color=GREY if gone else RED)
        if gone:
            ax.plot([x, x + 1.3], [2.6, 3.35], color=GREY, lw=1.5)
        x += 1.45
    label(ax, 6.6, 1.5, "했 = 하 + 았", fs=11, color=INK)
    label(ax, 10.3, 1.5, "회색 = 버림", fs=10.5, color=INK)


# ── 4. nori로 자른 사전에서 다시 찾기 ─────────────────────────────
def back(ax):
    board(ax, POSTS, hot=(1, 3, 9), dim=(2,))
    dictionary(ax, NORI, hot_word="환불", hot_nums={("환불", 9)}, name="ES (nori로 자른 사전)")
    x, y, _, _ = CYL
    for r in (0, 2, 4):
        arrow(ax, (x - 0.05, y + 1.2), (6.8, BOARD_ROW_Y[r]), color=RED, ms=12)


# ── 4. 사용자 사전 ────────────────────────────────────────────────
def userdict(ax):
    label(ax, 0.3, 6.1, "형태소 사전만", fs=11, ha="left", color=INK)
    cell(ax, 0.3, 4.9, 2.0, 0.75, "킹받네", fc=PAPER, fs=12)
    arrow(ax, (2.4, 5.27), (3.3, 5.27), ms=12)
    for k in range(3):
        x = 3.4 + k * 1.3
        ax.add_patch(Rectangle((x, 4.9), 1.0, 0.75, fc="white", ec=GREY, lw=1.2, ls="--"))
        label(ax, x + 0.5, 5.27, "?", fs=12, color=GREY)
    label(ax, 5.25, 4.5, "엉뚱한 조각", fs=10, color=INK)
    label(ax, 0.3, 3.5, "사용자 사전 추가", fs=11, ha="left", color=RED)
    box(ax, 0.3, 2.3, 2.0, 0.75, fc=NOTE, ec=RED)
    label(ax, 1.3, 2.67, "킹받네", fs=12, color=RED)
    arrow(ax, (2.4, 2.67), (3.3, 2.67), ms=12, color=RED)
    cell(ax, 3.4, 2.3, 2.6, 0.75, "킹받네", hot=True, fs=12)


# ── 5. 통째로 둬야 하는 값 ────────────────────────────────────────
def keyword(ax):
    rows = [("text 필드", 5.0), ("keyword 필드", 3.1), ("keyword + normalizer", 1.2)]
    for k, (name, y) in enumerate(rows):
        label(ax, 0.3, y + 0.95, name, fs=11, ha="left", bold=True)
        if k == 0:
            cell(ax, 0.3, y, 3.6, 0.7, "ORD-2024-00153", fc=PAPER, fs=11)
            arrow(ax, (4.0, y + 0.35), (4.9, y + 0.35), ms=12)
            cells(ax, 5.0, y, ["ord", "2024", "00153"], w=1.25, h=0.7, gap=0.07, hot=(1,), fs=11)
            label(ax, 9.2, y + 0.35, "2024로도 걸림", fs=10.5, ha="left", color=RED)
        elif k == 1:
            cell(ax, 0.3, y, 3.6, 0.7, "ORD-2024-00153", fc=PAPER, fs=11)
            arrow(ax, (4.0, y + 0.35), (4.9, y + 0.35), ms=12)
            cell(ax, 5.0, y, 3.9, 0.7, "ORD-2024-00153", fs=11)
            label(ax, 9.2, y + 0.35, "토큰 1개", fs=10.5, ha="left", color=INK)
        else:
            for j, (who, v) in enumerate([("저장", "ORD-2024-00153"), ("검색어", "ord-2024-00153")]):
                yy = y + 0.1 - j * 0.75
                label(ax, 0.3, yy + 0.3, who, fs=9.5, ha="left", color=INK)
                cell(ax, 1.25, yy, 2.65, 0.6, v, fc=PAPER, fs=10)
                arrow(ax, (4.0, yy + 0.3), (4.9, yy + 0.3), ms=10)
                cell(ax, 5.0, yy, 3.9, 0.6, "ord-2024-00153", hot=True, fs=10.5)
            label(ax, 9.2, y - 0.05, "같은 낱말", fs=10.5, ha="left", color=RED)


# ── 6. 한번 자르면 바꾸기 어려워요 ────────────────────────────────
def reindex(ax):
    box(ax, 0.3, 2.3, 4.2, 3.0, fc=NOTE)
    label(ax, 2.4, 4.9, "옛 인덱스 (기본 분석기)", fs=11, bold=True)
    cells(ax, 0.6, 3.55, ["환불했어요", "감사"], w=1.75, h=0.7, gap=0.1, fs=10.5)
    label(ax, 2.4, 3.05, "용어 사전", fs=9.5, color=INK)
    box(ax, 4.9, 0.55, 2.4, 0.9, fc=PAPER)
    label(ax, 6.1, 1.0, "원본 (_source)", fs=10.5)
    arrow(ax, (4.85, 1.2), (3.2, 2.25), ms=10, lw=1.2)
    arrow(ax, (7.5, 4.0), (4.6, 4.0), ms=12, lw=1.3)
    label(ax, 6.05, 4.0, "✗", fs=22, color=INK, bold=True)
    label(ax, 6.05, 4.7, "분석기만 교체", fs=10, color=INK)
    box(ax, 7.6, 2.3, 4.2, 3.0, fc=PINK, ec=RED)
    label(ax, 9.7, 4.9, "새 인덱스 (nori)", fs=11, bold=True, color=RED)
    cells(ax, 7.9, 3.55, ["환불", "감사"], w=1.75, h=0.7, gap=0.1, hot=(0,), fs=10.5)
    label(ax, 9.7, 3.05, "용어 사전", fs=9.5, color=INK)
    arrow(ax, (7.35, 1.2), (8.8, 2.25), color=RED, ms=14)
    label(ax, 9.0, 1.2, "재색인", fs=11, color=RED, ha="left", bold=True)


if __name__ == "__main__":
    one(miss, "es02-miss.svg")
    one(pipeline, "es02-pipeline.svg")
    one(termmatch, "es02-termmatch.svg")
    standard()
    one(nori, "es02-nori.svg")
    one(back, "es02-back.svg")
    one(userdict, "es02-userdict.svg")
    one(keyword, "es02-keyword.svg")
    one(reindex, "es02-reindex.svg")
