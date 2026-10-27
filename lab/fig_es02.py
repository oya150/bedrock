"""Elasticsearch 2편 그림 만들기. 실행: python lab/fig_es02.py  → docs/elasticsearch/img/02/*.svg"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "es"))
from figkit import (GREY, INK, NOTE, PAPER, PINK, RED, arrow, box, canvas, cell, cells,  # noqa: E402
                    label, outdir, save)

OUT = outdir("02")


def miss():
    """띄어쓰기로만 자르면 "환불"은 글 1만 찾고 "환불했어요"(글 2)와는 안 맞는다."""
    fig, ax = canvas(10, 3.8, 15, 5.6)
    label(ax, 0.3, 5.0, "글 1: 환불 요청합니다", fs=11, ha="left")
    label(ax, 0.3, 4.4, "글 2: 어제 환불했어요", fs=11, ha="left")
    label(ax, 0.3, 3.6, "띄어쓰기로 자르기", fs=10, ha="left", color=INK)
    arrow(ax, (3.2, 4.0), (4.6, 3.5))
    label(ax, 7.0, 5.0, "용어 사전", fs=12, bold=True)
    rows = [("환불", "글 1", True), ("요청합니다", "글 1", False), ("어제", "글 2", False), ("환불했어요", "글 2", False)]
    for k, (w, d, hot) in enumerate(rows):
        y = 4.05 - k * 0.85
        cell(ax, 4.8, y, 2.6, 0.72, w, hot=hot, fs=11)
        label(ax, 7.6, y + 0.36, f"→ {d}", fs=10.5, ha="left", color=RED if hot else INK)
    box(ax, 11.4, 3.7, 2.8, 1.0, fc=PINK, ec=RED)
    label(ax, 12.8, 4.2, "검색어: 환불", fs=12, color=RED, bold=True)
    arrow(ax, (11.3, 4.1), (9.0, 4.4), color=RED)
    label(ax, 11.4, 3.2, "글 1만 나와요", fs=11, color=RED, ha="left")
    label(ax, 8.8, 1.8, "← 글자가 달라 안 맞아요", fs=10.5, color=INK, ha="left")
    save(fig, OUT, "es02-miss.svg")


def map_():
    steps = ["글자가 똑같아야\n찾아요", "분석기\n세 단계", "한국어는\n형태소로", "검색어도\n같은 길로", "통째로\n둘 값", "바꾸려면\n재색인", "필드마다\n정하기"]
    fig, ax = canvas(13.9, 1.8, 28, 3)
    for k, s in enumerate(steps):
        x = 0.2 + k * 4.0
        hot = k == 1
        box(ax, x, 0.6, 3.2, 1.8, fc=PINK if hot else NOTE, ec=RED if hot else INK)
        label(ax, x + 1.6, 1.5, s, fs=11, color=RED if hot else "#222")
        label(ax, x + 0.22, 2.15, str(k + 1), fs=10, color=INK, ha="left")
        if k < len(steps) - 1:
            arrow(ax, (x + 3.3, 1.5), (x + 3.9, 1.5), ms=14)
    save(fig, OUT, "es02-map.svg")


def pipeline():
    fig, ax = canvas(11, 4.6, 20, 7.4)
    stages = ["문자 필터", "토크나이저", "토큰 필터"]
    xs = [3.6, 8.6, 13.6]
    for x, s in zip(xs, stages):
        box(ax, x, 5.3, 3.4, 1.1, fc=PAPER)
        label(ax, x + 1.7, 5.85, s, fs=12, bold=True)
    label(ax, 3.6 + 1.7, 4.8, "html_strip 필터:\n태그 지우기", fs=10, color=INK, va="top")
    label(ax, 8.6 + 1.7, 4.8, "standard 토크나이저:\n띄어쓰기·문장부호로 자르기", fs=10, color=INK, va="top")
    label(ax, 13.6 + 1.7, 4.8, "lowercase 필터:\n소문자로", fs=10, color=INK, va="top")
    for x in xs[:-1]:
        arrow(ax, (x + 3.5, 5.85), (x + 4.9, 5.85), ms=14)
    arrow(ax, (17.1, 5.85), (18.4, 5.85), ms=14)
    label(ax, 19.2, 5.85, "역색인", fs=12, bold=True)

    y = 2.4
    label(ax, 0.2, y + 1.15, "글", fs=12, ha="left", bold=True)
    cell(ax, 0.2, y, 3.0, 0.8, "<b>Refund</b> 요청", fs=10)
    cell(ax, 3.9, y, 2.6, 0.8, "Refund 요청", fs=11)
    cells(ax, 8.6, y, ["Refund", "요청"], w=1.5, h=0.8, fs=11)
    cells(ax, 13.6, y, ["refund", "요청"], w=1.5, h=0.8, fs=11, hot=(0,))
    y = 0.6
    label(ax, 0.2, y + 1.15, "검색어", fs=12, ha="left", bold=True)
    cell(ax, 0.2, y, 3.0, 0.8, "REFUND", fs=11)
    cell(ax, 3.9, y, 2.6, 0.8, "REFUND", fs=11)
    cells(ax, 8.6, y, ["REFUND"], w=1.5, h=0.8, fs=11)
    cells(ax, 13.6, y, ["refund"], w=1.5, h=0.8, fs=11, hot=(0,))
    label(ax, 17.4, 1.85, "같은 낱말이 돼서\n찾을 수 있어요", fs=11, color=RED, ha="left")
    save(fig, OUT, "es02-pipeline.svg")


def nori():
    fig, ax = canvas(10, 3.6, 15, 5.4)
    label(ax, 0.3, 4.85, "환불했어요", fs=13, ha="left", bold=True)
    parts = [("환불", "명사"), ("하", "접미사"), ("았", "어미"), ("어요", "어미")]
    x = 0.3
    for k, (m, pos) in enumerate(parts):
        hot = k == 0
        cell(ax, x, 3.2, 1.5, 0.85, m, hot=hot)
        label(ax, x + 0.75, 2.85, pos, fs=10, color=RED if hot else INK)
        x += 1.65
    label(ax, 3.6, 2.15, "① 형태소로 자르기 (했 = 하 + 았)", fs=11, color=INK)
    arrow(ax, (7.2, 3.6), (8.6, 3.6))
    cell(ax, 8.8, 3.2, 1.5, 0.85, "환불", hot=True)
    for k, m in enumerate(["하", "았", "어요"]):
        cell(ax, 10.5 + k * 1.05, 3.2, 0.95, 0.85, m, dim=True, fs=11)
        ax.plot([10.5 + k * 1.05, 11.45 + k * 1.05], [3.2, 4.05], color=GREY, lw=1.5)
    label(ax, 11.6, 2.15, "② 검색에 쓸모없는 품사 버리기", fs=11, color=INK)
    label(ax, 8.8, 1.2, "역색인에는 '환불'만 올라가요", fs=12, color=RED, ha="left", bold=True)
    save(fig, OUT, "es02-nori.svg")


def termmatch():
    fig, ax = canvas(10.5, 4.2, 16, 6.4)
    label(ax, 12.9, 5.95, "용어 사전", fs=12, bold=True)
    cell(ax, 11.6, 4.7, 2.6, 0.8, "refund", hot=False)
    cell(ax, 11.6, 3.8, 2.6, 0.8, "request")
    # match
    label(ax, 0.2, 4.95, "match", fs=12, ha="left", bold=True, color=RED)
    cell(ax, 1.8, 4.7, 1.8, 0.8, "Refund")
    arrow(ax, (3.7, 5.1), (4.6, 5.1), ms=14)
    box(ax, 4.7, 4.65, 2.6, 0.9, fc=PAPER)
    label(ax, 6.0, 5.1, "분석기", fs=11)
    arrow(ax, (7.4, 5.1), (8.3, 5.1), ms=14)
    cell(ax, 8.4, 4.7, 1.8, 0.8, "refund", hot=True)
    arrow(ax, (10.3, 5.1), (11.5, 5.1), color=RED, ms=14)
    label(ax, 14.5, 5.1, "1건", fs=12, color=RED, ha="left", bold=True)
    # term
    label(ax, 0.2, 2.15, "term", fs=12, ha="left", bold=True)
    cell(ax, 1.8, 1.9, 1.8, 0.8, "Refund")
    arrow(ax, (3.7, 2.3), (8.3, 2.3), ms=14)
    label(ax, 6.0, 2.75, "그대로", fs=11, color=INK)
    cell(ax, 8.4, 1.9, 1.8, 0.8, "Refund")
    arrow(ax, (10.3, 2.3), (11.4, 2.3), color=INK, ms=14)
    label(ax, 11.6, 2.3, "사전에 대문자\nRefund는 없어요\n→ 0건", fs=11, ha="left", color=INK)
    save(fig, OUT, "es02-termmatch.svg")


def standard():
    """기본 분석기: 한국어는 덩어리째, 영어는 하이픈에서 잘리고 소문자로."""
    fig, ax = canvas(10, 2.8, 15, 4.2)
    cell(ax, 0.3, 2.6, 4.8, 0.8, "환불했어요. Refund-Request!", fc=PAPER, fs=11)
    arrow(ax, (5.2, 3.0), (6.4, 3.0))
    label(ax, 5.8, 3.55, "기본 분석기", fs=10, color=INK)
    cells(ax, 6.5, 2.6, ["환불했어요", "refund", "request"], w=2.5, h=0.8, hot=(1, 2), fs=11)
    label(ax, 7.75, 2.1, "한국어는\n덩어리째", fs=10, color=INK)
    label(ax, 11.4, 2.1, "하이픈에서 잘리고 소문자로", fs=10, color=RED)
    save(fig, OUT, "es02-standard.svg")


def keyword():
    """주문번호: text는 잘려서 2024만 쳐도 걸리고 keyword는 통째로."""
    fig, ax = canvas(10, 3.4, 15, 5.0)
    label(ax, 0.3, 4.4, "text 필드", fs=12, ha="left", bold=True)
    cell(ax, 0.3, 3.4, 3.6, 0.8, "ORD-2024-00153", fc=PAPER, fs=11)
    arrow(ax, (4.0, 3.8), (5.0, 3.8))
    cells(ax, 5.1, 3.4, ["ord", "2024", "00153"], w=1.4, h=0.8, fs=11)
    label(ax, 9.7, 3.8, "\"2024\"만 쳐도 걸려요", fs=10.5, ha="left", color=INK)
    label(ax, 0.3, 2.0, "keyword 필드", fs=12, ha="left", bold=True, color=RED)
    cell(ax, 0.3, 1.0, 3.6, 0.8, "ORD-2024-00153", fc=PAPER, fs=11)
    arrow(ax, (4.0, 1.4), (5.0, 1.4), color=RED)
    cell(ax, 5.1, 1.0, 3.6, 0.8, "ORD-2024-00153", hot=True, fs=11)
    label(ax, 9.7, 1.4, "값 전체가 같을 때만 찾아요", fs=10.5, ha="left", color=RED)
    save(fig, OUT, "es02-keyword.svg")


def reindex():
    """분석기를 바꾸려면 원본에서 새 인덱스로 다시 넣는다."""
    fig, ax = canvas(10, 3.6, 15, 5.2)
    box(ax, 0.3, 1.6, 4.2, 2.8, fc=NOTE)
    label(ax, 2.4, 4.0, "옛 인덱스 (기본 분석기)", fs=11, bold=True)
    for k, t in enumerate(["환불했어요", "환불을"]):
        cell(ax, 0.8, 2.9 - k * 0.95, 3.2, 0.75, t, fs=11)
    box(ax, 5.4, 0.5, 4.0, 1.0, fc=PAPER)
    label(ax, 7.4, 1.0, "원본 (_source)", fs=10.5)
    box(ax, 10.4, 1.6, 4.3, 2.8, fc=PINK, ec=RED)
    label(ax, 12.55, 4.0, "새 인덱스 (nori)", fs=11, bold=True, color=RED)
    cell(ax, 11.0, 2.9, 3.0, 0.75, "환불", hot=True, fs=11)
    arrow(ax, (9.5, 1.0), (10.9, 2.0), color=RED)
    label(ax, 8.9, 2.2, "글을 다시 넣기\n(재색인)", fs=10.5, color=RED)
    label(ax, 2.4, 1.1, "사전은 저절로\n바뀌지 않아요", fs=10, color=INK)
    save(fig, OUT, "es02-reindex.svg")


def decide():
    """필드마다 자르는 방식 정하기."""
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


def lattice():
    """nori: 후보 길 중 비용 합이 가장 작은 길을 고른다(숫자는 설명용)."""
    fig, ax = canvas(10, 3.6, 15, 5.2)
    cell(ax, 0.3, 2.6, 1.9, 0.9, "아버지", fc=PAPER, fs=11)
    # 위 길: 가 + 방 + 에
    top = [("가", "조사", 2), ("방", "명사", 3), ("에", "조사", 1)]
    x = 3.2
    for k, (m, pos, c) in enumerate(top):
        cell(ax, x, 3.6, 1.4, 0.8, m, hot=True, fs=11)
        label(ax, x + 0.7, 4.65, f"{pos} {c}", fs=9.5, color=RED)
        if k < 2:
            arrow(ax, (x + 1.45, 4.0), (x + 1.95, 4.0), color=RED, ms=12)
        x += 2.0
    arrow(ax, (2.3, 3.2), (3.1, 3.9), color=RED, ms=12)
    label(ax, 9.3, 4.0, "합 6", fs=11, color=RED, ha="left", bold=True)
    # 아래 길: 가방 + 에
    cell(ax, 3.2, 1.3, 2.6, 0.8, "가방", fs=11, dim=True)
    label(ax, 4.5, 1.0, "명사 6", fs=9.5, color=INK)
    arrow(ax, (5.85, 1.7), (6.6, 1.7), ms=12)
    cell(ax, 6.7, 1.3, 1.4, 0.8, "에", fs=11, dim=True)
    label(ax, 7.4, 1.0, "조사 1", fs=9.5, color=INK)
    arrow(ax, (2.3, 2.9), (3.1, 2.0), ms=12)
    label(ax, 9.3, 1.7, "합 7", fs=11, color=INK, ha="left")
    label(ax, 7.5, 0.3, "비용 합이 가장 작은 길을 골라요 (숫자는 설명용)", fs=10.5, color=INK)
    save(fig, OUT, "es02-lattice.svg")


def alias():
    """별칭은 바로가기: 새 인덱스를 채운 뒤 가리키는 곳만 한 번에 옮긴다."""
    fig, ax = canvas(10, 4.4, 15, 6.6)
    rows = [("① 검색은 별칭으로", False, False), ("② 새 인덱스를 원본에서 채워요", True, False), ("③ 별칭을 한 번에 옮겨요", True, True)]
    for k, (title, has_new, moved) in enumerate(rows):
        y = 5.0 - k * 2.05
        label(ax, 0.3, y + 0.95, title, fs=10.5, ha="left", color=RED if moved else INK, bold=moved)
        box(ax, 0.3, y - 0.05, 2.6, 0.8, fc=PINK if moved else PAPER, ec=RED if moved else INK)
        label(ax, 1.6, y + 0.35, "별칭: 게시판", fs=10.5, color=RED if moved else "#222")
        if not moved:
            cell(ax, 5.2, y - 0.05, 3.6, 0.8, "옛 인덱스 (기본)", fs=10.5)
        if has_new:
            cell(ax, 10.2, y - 0.05, 3.6, 0.8, "새 인덱스 (nori)", hot=moved, fs=10.5)
        if moved:
            arrow(ax, (3.0, y + 0.35), (10.1, y + 0.35), color=RED, ms=14)
        else:
            arrow(ax, (3.0, y + 0.35), (5.1, y + 0.35), ms=14)
    save(fig, OUT, "es02-alias.svg")


def ngram():
    """자동완성: 저장은 edge_ngram, 검색어는 기본 분석기로만."""
    fig, ax = canvas(10, 4.0, 15, 6.0)
    label(ax, 0.3, 5.2, "저장", fs=11.5, ha="left", bold=True)
    cell(ax, 2.2, 4.8, 1.8, 0.8, "청바지", fc=PAPER, fs=11)
    arrow(ax, (4.1, 5.2), (5.4, 5.2), ms=12)
    label(ax, 4.75, 5.65, "edge_ngram", fs=9.5, color=INK)
    cells(ax, 5.5, 4.8, ["청", "청바", "청바지"], w=1.5, h=0.8, hot=(1,), fs=11)
    label(ax, 0.3, 3.4, "검색어", fs=11.5, ha="left", bold=True, color=RED)
    cell(ax, 2.2, 3.0, 1.8, 0.8, "청바", fc=PAPER, fs=11)
    arrow(ax, (4.1, 3.4), (6.85, 3.4), color=RED, ms=12)
    label(ax, 5.5, 3.85, "기본 분석기", fs=9.5, color=RED)
    cell(ax, 6.95, 3.0, 1.5, 0.8, "청바", hot=True, fs=11)
    label(ax, 10.3, 3.4, "사전의 청바와 맞아요", fs=10.5, ha="left", color=RED)
    label(ax, 0.3, 1.6, "검색어도\nedge_ngram", fs=10.5, ha="left", color=INK)
    cell(ax, 2.2, 1.2, 1.8, 0.8, "청바", fc=PAPER, fs=11)
    arrow(ax, (4.1, 1.6), (5.4, 1.6), ms=12)
    cells(ax, 5.5, 1.2, ["청", "청바"], w=1.5, h=0.8, fs=11)
    label(ax, 8.9, 1.6, "\"청\"이 청소기·청자켓과도 맞아\n다 걸려요", fs=10, ha="left", color=INK)
    save(fig, OUT, "es02-ngram.svg")


def normalizer():
    """keyword + 소문자 손질: 저장값과 검색어가 같은 손질을 거친다."""
    fig, ax = canvas(10, 2.8, 15, 4.2)
    for k, (who, hot) in enumerate([("저장", False), ("검색어 (match든 term이든)", True)]):
        y = 2.8 - k * 1.6
        label(ax, 0.3, y + 0.9, who, fs=11, ha="left", bold=True, color=RED if hot else "#222")
        cell(ax, 0.3, y, 3.6, 0.75, "ORD-2024-00153", fc=PAPER, fs=11)
        arrow(ax, (4.0, y + 0.37), (6.6, y + 0.37), color=RED if hot else INK, ms=12)
        label(ax, 5.3, y + 0.75, "소문자 손질", fs=9.5, color=RED if hot else INK)
        cell(ax, 6.7, y, 3.6, 0.75, "ord-2024-00153", hot=hot, fs=11)
    label(ax, 10.7, 2.05, "두 값이 같아\n찾아요", fs=11, ha="left", color=RED)
    save(fig, OUT, "es02-normalizer.svg")


if __name__ == "__main__":
    miss(); map_(); pipeline(); nori(); termmatch(); standard(); keyword(); reindex(); decide(); lattice(); alias(); ngram(); normalizer()
