"""Elasticsearch 2편 그림 만들기. 실행: python lab/fig_es02.py  → docs/elasticsearch/img/02/*.svg

본문 절은 장면 띠로 그린다: 같은 무대를 여러 장 그리고 장마다 바뀐 곳만 빨강으로 칠한다.
예시는 1편 게시판을 잇는다(글 1 주문 환불 요청, 3 환불 완료 감사, 9 환불했어요 감사).
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "es"))
from figkit import (BOARD_ROW_Y, GREY, INK, NOTE, PAPER, PINK, RED, arrow, board, box, bubble,  # noqa: E402
                    canvas, cell, cells, cylinder, label, moral, outdir, save, stage)
from matplotlib.patches import Rectangle  # noqa: E402

OUT = outdir("02")
POSTS = [(1, "주문 환불 요청"), (2, "주문 배송 언제"), (3, "환불 완료 감사"), None, (9, "환불했어요 감사")]
ROW9 = BOARD_ROW_Y[4]
CYL = (8.0, 3.0, 3.9, 1.7)
SAY = (7.3, 0.55, 4.6, 1.3)
TAIL = (9.95, 2.75)
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


# ── 여는 장면: 환불로 찾았는데 9번이 안 나와요 ─────────────────────
def miss(ax, step):
    board(ax, POSTS, hot=(1, 3) if step == 2 else (), miss=(9,) if step == 3 else ())
    dictionary(ax, STD, hot_word="환불" if step == 2 else None,
               hot_nums={("환불", 1), ("환불", 3)} if step == 2 else (), lost_word="환불했어요" if step == 3 else None)
    if step == 1:
        bubble(ax, *SAY, "띄어쓰기로 잘라 둔 사전에서\n환불을 찾아볼게요", TAIL)
    elif step == 2:
        bubble(ax, *SAY, "환불 줄에 1번과 3번이 있어요", TAIL, hot=True)
    else:
        bubble(ax, *SAY, "9번은 환불했어요 줄에 있어서\n환불로는 못 찾아요", TAIL, hot=True)
        moral(ax, 4.0, 0.2, "사전의 낱말과 글자까지 같아야 찾아요")


# ── 분석기 세 단계 ─────────────────────────────────────────────────
COLX = [0.15, 3.1, 6.05, 9.0]
STATIONS = [("문자 필터", "태그 지우기"), ("토크나이저", "띄어쓰기에서 자르기"), ("토큰 필터", "소문자로")]
DOC = [["<b>Refund</b> 요청"], ["Refund 요청"], ["Refund", "요청"], ["refund", "요청"]]
ASK = [["REFUND"], ["REFUND"], ["REFUND"], ["refund"]]


def row_cells(ax, col, items, y, hot=False):
    x, W = COLX[col], 2.7
    if len(items) == 1:
        cell(ax, x, y, W, 0.7, items[0], hot=hot, fs=9.5 if col == 0 else 10.5)
    else:
        cells(ax, x, y, items, w=1.3, h=0.7, gap=0.1, hot=(0,) if hot and col == 3 else (range(2) if hot else ()), fs=10.5)


def pipeline(ax, step):
    for i, (name, what) in enumerate(STATIONS):
        on = step == i + 2
        box(ax, COLX[i + 1], 5.55, 2.7, 0.75, fc=PINK if on else PAPER, ec=RED if on else "#555")
        label(ax, COLX[i + 1] + 1.35, 5.92, name, fs=11.5, bold=True, color=RED if on else "#222")
        label(ax, COLX[i + 1] + 1.35, 5.2, what, fs=10, color=RED if on else INK)
    label(ax, 0.2, 4.55, "글", fs=11.5, ha="left", bold=True)
    label(ax, 0.2, 2.55, "검색어", fs=11.5, ha="left", bold=True, color=RED if step == 5 else "#222")
    for c in range(4):
        if c <= min(step - 1, 3):
            row_cells(ax, c, DOC[c], 3.5, hot=(step == c + 1 and c > 0))
        else:
            empty(ax, COLX[c], 3.5, 2.7, 0.7)
        if step == 5:
            row_cells(ax, c, ASK[c], 1.5, hot=(c == 3))
        else:
            empty(ax, COLX[c], 1.5, 2.7, 0.7)
        if c < 3:
            arrow(ax, (COLX[c] + 2.75, 3.85), (COLX[c + 1] - 0.05, 3.85), ms=11, lw=1.3)
            arrow(ax, (COLX[c] + 2.75, 1.85), (COLX[c + 1] - 0.05, 1.85), ms=11, lw=1.3)
    if step == 1:
        label(ax, 6.0, 0.55, "웹에서 옮겨 온 글 한 줄을 따라가요", fs=11.5, color=INK)
    elif step == 5:
        moral(ax, 6.0, 0.55, "검색어도 같은 줄을 지나 refund가 돼서 찾아요")


# ── 기본 분석기 (한 장) ────────────────────────────────────────────
def standard():
    fig, ax = canvas(10, 2.8, 15, 4.2)
    cell(ax, 0.3, 2.6, 4.8, 0.8, "환불했어요. Refund-Request!", fc=PAPER, fs=11)
    arrow(ax, (5.2, 3.0), (6.4, 3.0))
    label(ax, 5.8, 3.55, "기본 분석기", fs=10, color=INK)
    cells(ax, 6.5, 2.6, ["환불했어요", "refund", "request"], w=2.5, h=0.8, hot=(1, 2), fs=11)
    label(ax, 7.75, 2.1, "한국어는\n덩어리째", fs=10, color=INK)
    label(ax, 11.4, 2.1, "하이픈에서 잘리고 소문자로", fs=10, color=RED)
    save(fig, OUT, "es02-standard.svg")


# ── 형태소로 자르기 ────────────────────────────────────────────────
PARTS = [("환불", "명사"), ("하", "접미사"), ("았", "어미"), ("어요", "어미")]


def nori(ax, step):
    label(ax, 0.3, 6.1, "글 9의 낱말 하나", fs=11.5, ha="left", color=INK)
    cell(ax, 0.3, 5.0, 2.6, 0.75, "환불했어요", fc=PAPER, fs=12)
    label(ax, 0.3, 4.35, "띄어쓰기로 자르면", fs=10.5, ha="left", color=INK)
    cell(ax, 3.7, 4.05, 2.6, 0.65, "환불했어요", fs=11.5, dim=(step > 1))
    label(ax, 6.6, 4.37, "통째로 한 낱말", fs=10.5, ha="left", color=GREY if step > 1 else INK)
    label(ax, 0.3, 3.0, "형태소로 자르면", fs=10.5, ha="left", color=RED if step == 2 else INK)
    x = 3.7
    for k, (m, pos) in enumerate(PARTS):
        if step == 1:
            empty(ax, x, 2.6, 1.3, 0.75)
        else:
            gone = step == 3 and k > 0
            cell(ax, x, 2.6, 1.3, 0.75, m, hot=(step == 2) or (step == 3 and k == 0), dim=gone, fs=12)
            label(ax, x + 0.65, 2.3, pos, fs=10, color=GREY if gone else (RED if step == 2 or k == 0 else INK))
            if gone:
                ax.plot([x, x + 1.3], [2.6, 3.35], color=GREY, lw=1.5)
        x += 1.45
    if step == 2:
        label(ax, 6.6, 1.55, "했 = 하 + 았", fs=11, color=RED)
    elif step == 3:
        label(ax, 9.75, 1.55, "검색에 쓸모없는 품사는 버려요", fs=10.5, color=RED)
        moral(ax, 6.0, 0.55, "역색인에는 '환불'만 올라가요")


# ── 전환: nori로 자를 때 챙길 것 ──────────────────────────────────
def turn(ax, step):
    cell(ax, 0.3, 4.6, 3.3, 0.75, "환불했어요 감사", fc=PAPER, fs=11.5)
    arrow(ax, (3.7, 4.97), (4.5, 4.97), ms=12)
    box(ax, 4.6, 4.35, 2.4, 1.25, fc=PINK if step == 2 else NOTE, ec=RED if step == 2 else "#555")
    label(ax, 5.8, 4.97, "nori", fs=14, bold=True, color=RED if step == 2 else "#222")
    arrow(ax, (7.1, 4.97), (7.9, 4.97), ms=12)
    cells(ax, 8.0, 4.6, ["환불", "감사"], w=1.4, h=0.75, fs=11.5)
    if step == 1:
        bubble(ax, 2.6, 2.0, 6.4, 1.3, "접미사와 어미를 떼고 '환불'을 꺼냈어요\n이제 9번 글도 찾아요", (5.8, 4.25))
    else:
        bubble(ax, 1.4, 0.3, 9.2, 3.25, "", (5.8, 4.25), hot=True)
        label(ax, 6.0, 3.1, "그런데 자를 때 챙길 것이 있어요", fs=12, color=RED, bold=True)
        for k, t in enumerate(["① 형태소 사전에 없는 새 말은 잘못 자를 수 있어요", "② 검색어도 같은 방식으로 잘라야 해요",
                               "③ 통째로 맞아야 하는 값은 자르면 안 돼요", "④ 한번 자른 결과는 바꾸기 어려워요"]):
            label(ax, 2.0, 2.45 - k * 0.5, t, fs=11, ha="left", color=RED)


# ── ① 사용자 사전 ─────────────────────────────────────────────────
def userdict(ax, step):
    label(ax, 0.3, 6.1, "형태소 사전만으로 자르면", fs=11, ha="left", color=INK)
    cell(ax, 0.3, 4.9, 2.0, 0.75, "킹받네", fc=PAPER, fs=12)
    arrow(ax, (2.4, 5.27), (3.3, 5.27), ms=12)
    for k, (m, pos, keep) in enumerate([("킹", "부사로 읽혀 버림", False), ("받", "남음", True), ("네", "어미라 버림", False)]):
        x = 3.4 + k * 2.3
        cell(ax, x, 4.9, 1.0, 0.75, m, hot=(keep and step == 1), dim=not keep, fs=12)
        if not keep:
            ax.plot([x, x + 1.0], [4.9, 5.65], color=GREY, lw=1.5)
        label(ax, x + 0.5, 4.55, pos, fs=9.5, color=(RED if keep and step == 1 else INK))
    label(ax, 0.3, 3.5, "사용자 사전에 적어 두면", fs=11, ha="left", color=RED if step == 2 else INK)
    if step == 1:
        empty(ax, 0.3, 2.3, 2.0, 0.75)
        empty(ax, 3.4, 2.3, 2.6, 0.75)
        label(ax, 6.0, 1.3, "'킹받네'가 '받'만 남았어요", fs=11.5, color=RED)
    else:
        box(ax, 0.3, 2.3, 2.0, 0.75, fc=NOTE, ec=RED)
        label(ax, 1.3, 2.67, "킹받네", fs=12, color=RED)
        label(ax, 1.3, 1.95, "사용자 사전", fs=9.5, color=RED)
        arrow(ax, (2.4, 2.67), (3.3, 2.67), ms=12, color=RED)
        cell(ax, 3.4, 2.3, 2.6, 0.75, "킹받네", hot=True, fs=12)
        moral(ax, 6.0, 0.8, "사용자 사전에 적은 모양대로 잘라요")


# ── ② match와 term ────────────────────────────────────────────────
def termmatch(ax, step):
    label(ax, 10.4, 6.0, "용어 사전", fs=11.5, bold=True)
    cell(ax, 9.2, 4.9, 2.4, 0.7, "refund", hot=(step == 1), fs=11)
    cell(ax, 9.2, 4.1, 2.4, 0.7, "request", fs=11)
    label(ax, 0.2, 5.95, "match", fs=12, ha="left", bold=True, color=RED if step == 1 else "#222")
    cell(ax, 0.2, 4.9, 1.8, 0.7, "Refund", fs=11)
    arrow(ax, (2.1, 5.25), (2.9, 5.25), ms=12)
    box(ax, 3.0, 4.85, 2.2, 0.8, fc=PAPER)
    label(ax, 4.1, 5.25, "분석기", fs=11)
    arrow(ax, (5.3, 5.25), (6.1, 5.25), ms=12)
    cell(ax, 6.2, 4.9, 1.8, 0.7, "refund", hot=(step == 1), fs=11)
    arrow(ax, (8.1, 5.25), (9.1, 5.25), color=RED if step == 1 else "#555", ms=12)
    label(ax, 10.4, 3.6, "1건" if step == 1 else "", fs=12, color=RED, bold=True)
    label(ax, 0.2, 3.05, "term", fs=12, ha="left", bold=True, color=RED if step == 2 else "#222")
    if step == 1:
        empty(ax, 0.2, 2.0, 1.8, 0.7)
        empty(ax, 6.2, 2.0, 1.8, 0.7)
        moral(ax, 6.0, 0.6, "match는 검색어도 잘라서 소문자 refund로 찾아요")
    else:
        cell(ax, 0.2, 2.0, 1.8, 0.7, "Refund", fs=11)
        arrow(ax, (2.1, 2.35), (6.1, 2.35), ms=12, color=RED)
        label(ax, 4.1, 2.75, "그대로", fs=11, color=RED)
        cell(ax, 6.2, 2.0, 1.8, 0.7, "Refund", hot=True, fs=11)
        label(ax, 8.3, 2.35, "사전에 대문자 Refund는\n없어요 → 0건", fs=11, ha="left", color=RED)
        moral(ax, 6.0, 0.6, "term은 검색어를 자르지 않고 그대로 찾아요")


# ── ③ 통째로 둬야 하는 값 ─────────────────────────────────────────
def keyword(ax, step):
    rows = [("text 필드", 5.0), ("keyword 필드", 3.1), ("keyword + 소문자 손질", 1.2)]
    for k, (name, y) in enumerate(rows):
        on = step == k + 1
        label(ax, 0.3, y + 0.95, name, fs=11, ha="left", bold=True, color=RED if on else "#222")
        if k + 1 > step:
            empty(ax, 0.3, y, 3.6, 0.7)
            empty(ax, 5.0, y, 3.9, 0.7)
            continue
        if k == 0:
            cell(ax, 0.3, y, 3.6, 0.7, "ORD-2024-00153", fc=PAPER, fs=11)
            arrow(ax, (4.0, y + 0.35), (4.9, y + 0.35), ms=12)
            cells(ax, 5.0, y, ["ord", "2024", "00153"], w=1.25, h=0.7, gap=0.07, hot=range(3) if on else (), fs=11)
            label(ax, 9.2, y + 0.35, "'2024'만 쳐도 걸려요", fs=10.5, ha="left", color=RED if on else INK)
        elif k == 1:
            cell(ax, 0.3, y, 3.6, 0.7, "ORD-2024-00153", fc=PAPER, fs=11)
            arrow(ax, (4.0, y + 0.35), (4.9, y + 0.35), ms=12)
            cell(ax, 5.0, y, 3.9, 0.7, "ORD-2024-00153", hot=on, fs=11)
            label(ax, 9.2, y + 0.35, "값 전체가 같을 때만", fs=10.5, ha="left", color=RED if on else INK)
        else:
            for j, (who, v) in enumerate([("저장", "ORD-2024-00153"), ("검색어", "ord-2024-00153")]):
                yy = y + 0.1 - j * 0.75
                label(ax, 0.3, yy + 0.3, who, fs=9.5, ha="left", color=RED)
                cell(ax, 1.25, yy, 2.65, 0.6, v, fc=PAPER, fs=10)
                arrow(ax, (4.0, yy + 0.3), (4.9, yy + 0.3), ms=10, color=RED)
                cell(ax, 5.0, yy, 3.9, 0.6, "ord-2024-00153", hot=True, fs=10.5)
            label(ax, 9.2, y - 0.05, "둘이 같아져서\n찾아요", fs=10.5, ha="left", color=RED)


# ── ④ 한번 자르면 바꾸기 어려워요 ─────────────────────────────────
def reindex(ax, step):
    box(ax, 0.3, 2.3, 4.2, 3.0, fc=NOTE)
    label(ax, 2.4, 4.9, "옛 인덱스 (기본 분석기)", fs=11, bold=True)
    cells(ax, 0.6, 3.55, ["환불했어요", "감사"], w=1.75, h=0.7, gap=0.1, fs=10.5)
    label(ax, 2.4, 3.05, "용어 사전", fs=9.5, color=INK)
    box(ax, 4.9, 0.55, 2.4, 0.9, fc=PAPER)
    label(ax, 6.1, 1.0, "원본 (_source)", fs=10.5)
    arrow(ax, (4.85, 1.2), (3.2, 2.25), ms=10, lw=1.2)
    if step == 2:
        arrow(ax, (6.9, 4.4), (4.6, 4.4), color=RED, ms=14)
        label(ax, 8.3, 4.75, "분석기만 nori로 바꾸기", fs=11, color=RED)
        label(ax, 5.75, 4.4, "✗", fs=24, color=RED, bold=True)
        label(ax, 8.3, 3.6, "이미 있는 필드는\n바꿀 수 없어요", fs=11, color=RED)
    if step < 3:
        if step == 1:
            label(ax, 8.5, 3.8, "nori로 바꾸고 싶어요", fs=12, color=INK)
        return
    box(ax, 7.6, 2.3, 4.2, 3.0, fc=PINK, ec=RED)
    label(ax, 9.7, 4.9, "새 인덱스 (nori)", fs=11, bold=True, color=RED)
    cells(ax, 7.9, 3.55, ["환불", "감사"], w=1.75, h=0.7, gap=0.1, hot=(0,), fs=10.5)
    arrow(ax, (7.35, 1.2), (8.8, 2.25), color=RED, ms=14)
    label(ax, 9.9, 1.2, "글을 다시 넣어요\n(재색인)", fs=10.5, color=RED, ha="left")
    moral(ax, 6.0, 0.15, "원본에서 새 인덱스로 글을 다시 넣어야 해요")


# ── 판단 (한 장) ───────────────────────────────────────────────────
def decide():
    fig, ax = canvas(10, 4.4, 15, 6.6)
    box(ax, 0.3, 4.6, 5.2, 1.4, fc=NOTE)
    label(ax, 2.9, 5.3, "값 전체가 맞아야 하나요?\n(주문번호·이메일)", fs=11, bold=True)
    arrow(ax, (5.6, 5.3), (7.4, 5.3))
    label(ax, 6.5, 5.6, "예", fs=10, color=INK)
    box(ax, 7.5, 4.6, 7.2, 1.4, fc=PAPER)
    label(ax, 11.1, 5.3, "keyword 필드\n대소문자를 무시하려면 소문자 손질", fs=10.5)
    arrow(ax, (2.9, 4.5), (2.9, 3.3))
    label(ax, 3.4, 3.9, "아니요", fs=10, color=INK, ha="left")
    box(ax, 0.3, 1.9, 5.2, 1.3, fc=NOTE)
    label(ax, 2.9, 2.55, "한국어 문장인가요?", fs=11, bold=True)
    arrow(ax, (5.6, 2.55), (7.4, 2.55), color=RED)
    label(ax, 6.5, 2.85, "예", fs=10, color=RED)
    box(ax, 7.5, 1.9, 7.2, 1.3, fc=PINK, ec=RED)
    label(ax, 11.1, 2.55, "text 필드 + nori\n예: 게시판 글", fs=10.5, color=RED)
    arrow(ax, (2.9, 1.8), (2.9, 0.9))
    label(ax, 3.4, 1.35, "아니요", fs=10, color=INK, ha="left")
    label(ax, 2.9, 0.5, "text 필드 + 기본 분석기  예: 영어 상품 설명", fs=10.5, ha="left")
    save(fig, OUT, "es02-decide.svg")


# ── 심화: 길 고르기 ────────────────────────────────────────────────
def lattice(ax, step):
    cell(ax, 0.3, 3.0, 1.9, 0.9, "아버지", fc=PAPER, fs=11)
    on = step == 2
    x = 3.2
    for k, (m, pos, c) in enumerate([("가", "조사", 2), ("방", "명사", 3), ("에", "조사", 1)]):
        cell(ax, x, 4.2, 1.4, 0.8, m, hot=on, fs=11)
        label(ax, x + 0.7, 5.25, f"{pos} {c}", fs=9.5, color=RED if on else INK)
        if k < 2:
            arrow(ax, (x + 1.45, 4.6), (x + 1.95, 4.6), color=RED if on else "#555", ms=11)
        x += 2.0
    arrow(ax, (2.3, 3.6), (3.1, 4.5), color=RED if on else "#555", ms=11)
    label(ax, 9.3, 4.6, "합 6", fs=11.5, color=RED if on else INK, ha="left", bold=on)
    cell(ax, 3.2, 1.9, 2.6, 0.8, "가방", fs=11, dim=on)
    label(ax, 4.5, 1.6, "명사 6", fs=9.5, color=INK)
    arrow(ax, (5.85, 2.3), (6.6, 2.3), ms=11)
    cell(ax, 6.7, 1.9, 1.4, 0.8, "에", fs=11, dim=on)
    label(ax, 7.4, 1.6, "조사 1", fs=9.5, color=INK)
    arrow(ax, (2.3, 3.3), (3.1, 2.6), ms=11)
    label(ax, 9.3, 2.3, "합 7", fs=11.5, color=INK, ha="left")
    if step == 1:
        label(ax, 6.0, 0.6, "자를 수 있는 길이 둘이에요 (숫자는 설명용)", fs=11, color=INK)
    else:
        moral(ax, 6.0, 0.6, "비용 합이 가장 작은 길을 골라요")


# ── 심화: 자동완성 ─────────────────────────────────────────────────
def ngram(ax, step):
    rows = [("저장", 4.9), ("검색어", 3.0), ("검색어까지 edge_ngram으로 자르면", 1.1)]
    for k, (name, y) in enumerate(rows):
        on = step == k + 1
        label(ax, 0.3, y + 1.0, name, fs=10.5, ha="left", bold=True, color=RED if on else "#222")
        if k + 1 > step:
            empty(ax, 0.3, y, 1.8, 0.7)
            empty(ax, 5.6, y, 4.8, 0.7)
            continue
        cell(ax, 0.3, y, 1.8, 0.7, "청바지" if k == 0 else "청바", fc=PAPER, fs=11)
        arrow(ax, (2.2, y + 0.35), (5.5, y + 0.35), ms=11, color=RED if on else "#555")
        label(ax, 3.85, y + 0.6, "edge_ngram" if k != 1 else "기본 분석기", fs=9.5, color=RED if on else INK)
        if k == 0:
            cells(ax, 5.6, y, ["청", "청바", "청바지"], w=1.5, h=0.7, gap=0.1, hot=range(3) if on else (), fs=11)
        elif k == 1:
            cell(ax, 5.6, y, 1.5, 0.7, "청바", hot=on, fs=11)
            label(ax, 7.4, y + 0.35, "사전의 청바와 맞아요", fs=10.5, ha="left", color=RED if on else INK)
        else:
            cells(ax, 5.6, y, ["청", "청바"], w=1.5, h=0.7, gap=0.1, hot=(0,), fs=11)
            label(ax, 8.9, y + 0.35, "'청'이 청소기·청자켓과도\n맞아 다 걸려요", fs=10, ha="left", color=RED)


# ── 심화: 별칭 ─────────────────────────────────────────────────────
def alias(ax, step):
    box(ax, 0.3, 3.6, 2.8, 0.9, fc=PINK if step == 3 else PAPER, ec=RED if step == 3 else "#555")
    label(ax, 1.7, 4.05, "별칭: 게시판", fs=11, color=RED if step == 3 else "#222")
    label(ax, 1.7, 5.0, "검색은 늘 별칭으로", fs=10, color=INK)
    cell(ax, 4.6, 4.8, 3.2, 0.8, "옛 인덱스 (기본)", fs=10.5, dim=(step == 3))
    if step == 1:
        empty(ax, 4.6, 2.5, 3.2, 0.8)
    else:
        cell(ax, 4.6, 2.5, 3.2, 0.8, "새 인덱스 (nori)", hot=(step == 2), fs=10.5)
    if step < 3:
        arrow(ax, (3.2, 4.2), (4.5, 5.1), ms=13)
    else:
        arrow(ax, (3.2, 3.9), (4.5, 2.9), color=RED, ms=14)
    if step == 2:
        box(ax, 9.0, 1.2, 2.6, 0.8, fc=PAPER)
        label(ax, 10.3, 1.6, "원본 (_source)", fs=10)
        arrow(ax, (8.95, 1.7), (7.85, 2.6), color=RED, ms=13)
        label(ax, 9.0, 3.4, "새 인덱스를\n원본에서 채워요", fs=10.5, ha="left", color=RED)
    elif step == 3:
        moral(ax, 6.0, 0.9, "별칭이 가리키는 곳만 한 번에 옮겨요")


# ── 정리: 처음 장면으로 돌아가기 ───────────────────────────────────
def back(ax, step):
    if step == 1:
        board(ax, POSTS, miss=(9,))
        dictionary(ax, STD)
        bubble(ax, *SAY, "처음엔 9번 글이\n안 나왔어요", TAIL)
        return
    board(ax, POSTS, hot=(1, 3, 9) if step == 3 else (), dim=(2,) if step == 3 else ())
    dictionary(ax, NORI, hot_nums={("환불", 9)} if step == 2 else (), name="ES (nori로 자른 사전)", name_hot=(step == 2))
    if step == 2:
        bubble(ax, *SAY, "환불했어요에서 '환불'을\n꺼내 9를 달아 뒀어요", TAIL, hot=True)
    else:
        x, y, _, _ = CYL
        for r in (0, 2, 4):
            arrow(ax, (x - 0.05, y + 1.2), (6.8, BOARD_ROW_Y[r]), color=RED, ms=12)
        bubble(ax, *SAY, "1번, 3번, 9번이 나와요", TAIL, hot=True)
        moral(ax, 4.0, 0.2, "글과 검색어를 같은 방식으로 잘라 두면 찾아요")


# ── 정리: 낱말 카드 ────────────────────────────────────────────────
def cards():
    fig, ax = canvas(6.4, 13.0, 9.8, 20.3)
    W, H = 4.6, 3.8

    def card(i, name, line):
        col, row = i % 2, i // 2
        x, y = 0.2 + col * 4.9, 16.3 - row * 4.05
        box(ax, x, y, W, H, fc="white")
        label(ax, x + 0.25, y + H - 0.4, name, fs=12.5, ha="left", bold=True)
        label(ax, x + W / 2, y + 0.45, line, fs=10, color=INK)
        return x, y

    x, y = card(0, "분석기", "글을 잘라 사전에 올릴 낱말을 만드는 줄")
    for k, t in enumerate(["문자", "토크나이저", "토큰"]):
        cell(ax, x + 0.2 + k * 1.45, y + 1.9, 1.35, 0.6, t, fs=9, hot=(k == 1))
    x, y = card(1, "토큰", "분석기가 잘라 낸 조각 하나")
    cell(ax, x + 0.4, y + 2.4, 3.8, 0.55, "환불했어요 감사", fc=PAPER, fs=10)
    cells(ax, x + 1.0, y + 1.4, ["환불", "감사"], w=1.2, h=0.55, hot=(0, 1), fs=10.5)
    x, y = card(2, "형태소 분석", "뜻을 가진 가장 작은 단위로 자르기")
    cells(ax, x + 0.3, y + 1.9, ["환불", "하", "았", "어요"], w=0.92, h=0.6, gap=0.06, hot=(0,), fs=10.5)
    x, y = card(3, "사용자 사전", "형태소 사전에 덧붙이는 낱말 목록")
    box(ax, x + 0.5, y + 1.85, 1.6, 0.7, fc=NOTE, ec=RED, lw=1.4)
    label(ax, x + 1.3, y + 2.2, "킹받네", fs=11, color=RED)
    arrow(ax, (x + 2.2, y + 2.2), (x + 2.75, y + 2.2), ms=10, color=RED)
    cell(ax, x + 2.85, y + 1.9, 1.4, 0.6, "킹받네", hot=True, fs=10.5)
    x, y = card(4, "text 필드", "분석기로 잘라서 저장")
    cells(ax, x + 0.4, y + 1.9, ["ord", "2024", "00153"], w=1.2, h=0.6, gap=0.1, fs=10.5)
    x, y = card(5, "keyword 필드", "값 전체를 낱말 하나로 저장")
    cell(ax, x + 0.5, y + 1.9, 3.6, 0.6, "ORD-2024-00153", hot=True, fs=10.5)
    x, y = card(6, "소문자 손질", "자르지 않고 소문자로만 바꾸기")
    cell(ax, x + 0.5, y + 1.9, 3.6, 0.6, "ord-2024-00153", hot=True, fs=10.5)
    x, y = card(7, "ES 인덱스", "글과 역색인을 함께 담는 통")
    box(ax, x + 1.1, y + 1.4, 2.4, 1.6, fc=NOTE, lw=1.4)
    label(ax, x + 2.3, y + 2.55, "글", fs=10.5)
    label(ax, x + 2.3, y + 1.85, "역색인", fs=10.5)
    x, y = card(8, "재색인", "새 설정의 인덱스에 글을 다시 넣기")
    box(ax, x + 0.4, y + 1.7, 1.4, 1.0, fc=NOTE, lw=1.2)
    label(ax, x + 1.1, y + 2.2, "옛", fs=10.5, color=INK)
    arrow(ax, (x + 1.9, y + 2.2), (x + 2.7, y + 2.2), ms=11, color=RED)
    box(ax, x + 2.8, y + 1.7, 1.4, 1.0, fc=PINK, ec=RED, lw=1.4)
    label(ax, x + 3.5, y + 2.2, "새", fs=10.5, color=RED)
    save(fig, OUT, "es02-cards.svg")


if __name__ == "__main__":
    S, L = (7.2, 3.8), (12, 6.6)
    stage(miss, 3, OUT, "es02-miss", S, L)
    stage(pipeline, 5, OUT, "es02-pipeline", S, L)
    standard()
    stage(nori, 3, OUT, "es02-nori", S, L)
    stage(lattice, 2, OUT, "es02-lattice", S, L)
    stage(turn, 2, OUT, "es02-turn", S, L)
    stage(userdict, 2, OUT, "es02-userdict", S, L)
    stage(termmatch, 2, OUT, "es02-termmatch", S, L)
    stage(ngram, 3, OUT, "es02-ngram", S, L)
    stage(keyword, 3, OUT, "es02-keyword", S, L)
    stage(reindex, 3, OUT, "es02-reindex", S, L)
    stage(alias, 3, OUT, "es02-alias", S, L)
    decide()
    stage(back, 3, OUT, "es02-back", S, L)
    cards()
