"""Elasticsearch 10편 그림 만들기. 실행: python lab/fig_es10.py  → docs/elasticsearch/img/10/*.svg

그림 9장. 예시는 브랜드 문서 1~7(나이키·아디다스·푸마)과 주문번호 3, 9, 10, 25, 100을 편 끝까지 잇는다.
그림 안 글씨는 낱말·숫자만 둔다. 빨강은 지금 볼 곳에만 칠한다.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "es"))
from figkit import (GREY, INK, NOTE, PAPER, PINK, RED, arrow, box, canvas, cell, cells, label, moral,  # noqa: E402
                    outdir, save, stage)
from matplotlib.patches import Rectangle  # noqa: E402

OUT = outdir("10")

BRANDS = ["나이키", "아디다스", "푸마", "나이키", "아디다스", "푸마", "나이키"]
INV = [("나이키", [1, 4, 7]), ("아디다스", [2, 5]), ("푸마", [3, 6])]
DICT = ["나이키", "아디다스", "푸마"]


# ── 역색인은 방향이 반대예요 ───────────────────────────────────────
INV_Y = [4.75, 3.85, 2.95]


def inverted(ax, x0=0.3, ys=INV_Y, hot_row=None, hot_doc=None, mark=False, grey=False, h=0.7, fs=11):
    for k, ((b, ds), y) in enumerate(zip(INV, ys)):
        on = hot_row == k
        cell(ax, x0, y, 1.8, h, b, hot=on, fs=fs)
        arrow(ax, (x0 + 1.9, y + h / 2), (x0 + 2.55, y + h / 2), color=RED if (on or mark) else (GREY if grey else INK),
              lw=1.4, ms=11)
        hot = [i for i, d in enumerate(ds) if on or d == hot_doc]
        cells(ax, x0 + 2.65, y, ds, w=0.7, h=h, hot=hot, fs=fs)
        if mark:
            label(ax, x0 - 0.1, y + h / 2, "①②③"[k], fs=11, color=RED, ha="right")


def direction(ax, step):
    """1: 문서 7의 브랜드를 찾으려고 세 줄을 다 읽어요. 2: 정렬은 문서마다 값을 물어요."""
    label(ax, 0.3, 6.1, "역색인: 값 → 문서", fs=12, ha="left", bold=True)
    inverted(ax, x0=0.7, hot_doc=7 if step == 1 else None, mark=(step == 1))
    if step == 1:
        label(ax, 8.6, 4.55, "문서 7의 브랜드?", fs=12, color=RED, bold=True)
        label(ax, 8.6, 3.75, "①②③ 모두 읽기", fs=11, color=RED)
        return
    label(ax, 0.3, 2.25, "브랜드순 정렬", fs=11, ha="left", color=RED, bold=True)
    for d in range(1, 8):
        x = 0.3 + (d - 1) * 1.62
        cell(ax, x, 1.35, 1.5, 0.55, f"문서 {d}", fc=PAPER, fs=10)
        label(ax, x + 0.75, 1.0, "브랜드?", fs=10, color=RED, bold=True)
    moral(ax, 6.0, 0.3, "문서마다 값 묻기")


# ── 뒤집어 쓰기는 비싸요 (fielddata) ──────────────────────────────
HX, HY, HW, HH = 6.7, 1.3, 4.9, 4.2
FD = [(1, "나이키"), (2, "아디다스"), (3, "푸마"), None, (7, "나이키")]


def flip():
    """뒤집은 표(fielddata)가 힙을 다 차지해요."""
    fig, ax = canvas(7.2, 3.8, 12, 6.6)
    label(ax, 0.3, 6.1, "역색인 (디스크)", fs=12, ha="left", bold=True)
    inverted(ax, x0=0.3, grey=True)
    label(ax, HX + HW / 2, 6.1, "자바 힙", fs=12, bold=True)
    box(ax, HX, HY, HW, HH, fc=PINK, ec=RED, lw=2.2, round_=False)
    for k, r in enumerate(FD):
        y = HY + HH - 0.75 - k * 0.68
        if r is None:
            label(ax, HX + HW / 2, y + 0.28, "⋮", fs=13, color=INK)
            continue
        cell(ax, HX + 0.4, y, 1.5, 0.55, f"문서 {r[0]}", fc=PAPER, fs=10)
        cell(ax, HX + 2.0, y, 2.4, 0.55, r[1], fs=10.5)
    arrow(ax, (5.4, 4.65), (HX - 0.1, 4.65), color=GREY, ms=14)
    label(ax, HX + HW / 2, 1.6, "⋮  수억 줄", fs=11, color=RED, bold=True)
    label(ax, 3.0, 2.2, "문서 수억 개", fs=11, color=RED, bold=True)
    label(ax, 3.0, 1.55, "힙 가득", fs=11, color=RED)
    moral(ax, 6.0, 0.45, "text 필드: fielddata 꺼짐")
    save(fig, OUT, "es10-flip.svg")


# ── 그래서 미리 열로 적어 둬요 (doc values) ───────────────────────
CX = 7.6
COL_Y = [3.9 - k * 0.46 for k in range(7)]
RESULT = (2, 4, 7)                     # 검색 결과 문서(예)


def docvalues(ax, step):
    box(ax, 0.3, 5.7, 4.2, 0.7, fc=NOTE)
    label(ax, 2.4, 6.05, "넣는 문서 7 · 브랜드 나이키", fs=11)
    box(ax, 0.3, 0.95, 11.3, 3.95, fc="white", round_=False)
    label(ax, 0.5, 4.6, "세그먼트 (디스크)", fs=10.5, ha="left", bold=True, color=INK)
    inverted(ax, x0=0.6, ys=[3.55, 2.7, 1.85], h=0.6, fs=10.5)
    arrow(ax, (1.5, 5.62), (1.5, 4.95), color=GREY, ms=13)
    label(ax, 1.7, 5.28, "역색인 (1편)", fs=10, ha="left", color=INK)
    hot = step == 1
    label(ax, CX + 1.8, 4.6, "doc values (열)", fs=10.5, color=RED if hot else INK, bold=hot)
    for d, (y, v) in enumerate(zip(COL_Y, BRANDS), start=1):
        cell(ax, CX, y, 1.3, 0.42, f"문서 {d}", fc=PAPER, fs=9)
        cell(ax, CX + 1.4, y, 2.2, 0.42, v, hot=hot or (step == 2 and d in RESULT), fs=9.5)
    if hot:
        arrow(ax, (4.6, 6.05), (CX + 2.5, 4.85), color=RED, ms=15, rad=-0.15)
        label(ax, 6.0, 5.35, "열에도", fs=11, color=RED, bold=True, ha="left")
        return
    arrow(ax, (4.6, 6.05), (CX + 2.5, 4.85), color=GREY, ms=13, rad=-0.15)
    for d in RESULT:
        y = COL_Y[d - 1] + 0.21
        arrow(ax, (CX - 0.75, y), (CX - 0.08, y), color=RED, ms=12, lw=1.6)
    label(ax, 3.5, 1.35, "결과 2 4 7만 읽기", fs=10.5, color=RED, bold=True)
    moral(ax, 6.0, 0.4, "doc values: 문서 → 값 열 (디스크)")


# ── text 필드는 열을 만들지 않아요 ─────────────────────────────────
def textf():
    """title은 두 조각으로 잘려 열이 없고 title.raw는 제목 전체를 값 하나로 담아요."""
    fig, ax = canvas(7.2, 3.8, 12, 6.6)
    box(ax, 0.3, 5.45, 4.6, 0.75, fc=NOTE)
    label(ax, 2.6, 5.82, "넣는 제목 · 나이키 에어맥스", fs=11)
    label(ax, 0.3, 4.75, "title (text)", fs=11, ha="left", bold=True)
    arrow(ax, (2.9, 5.4), (2.9, 4.1), color=GREY, ms=13)
    cells(ax, 0.3, 3.35, ["나이키", "에어맥스"], w=1.8, h=0.65, fs=11)
    label(ax, 2.2, 2.85, "분석기: 두 조각 (2편)", fs=10.5, color=INK)
    label(ax, 2.2, 2.3, "역색인: 조각만", fs=10.5, color=INK)
    label(ax, 8.6, 4.75, "title의 doc values", fs=11, bold=True)
    ax.add_patch(Rectangle((6.6, 3.35), 4.0, 0.65, fc="white", ec=RED, lw=1.4, ls="--"))
    label(ax, 8.6, 3.67, "없음", fs=11.5, color=RED, bold=True)
    label(ax, 3.4, 1.4, "title.raw\n(keyword 하위 필드)", fs=10.5, ha="right", color=RED)
    cell(ax, 3.6, 1.05, 3.6, 0.65, "나이키 에어맥스", hot=True, fs=11)
    arrow(ax, (5.4, 5.4), (5.4, 1.8), color=RED, ms=14)
    moral(ax, 6.0, 0.4, "제목 정렬: title.raw")
    save(fig, OUT, "es10-text.svg")


# ── 문자열은 순번으로 담아요 ───────────────────────────────────────
def ordinals(ax, step):
    """1: 열에는 순번만 적어요. 2: 집계는 순번마다 칸 하나를 두고 세요."""
    label(ax, 0.3, 6.15, "브랜드 열 (doc values)", fs=12, ha="left", bold=True)
    for d in range(1, 8):
        x = 0.3 + (d - 1) * 1.6
        cell(ax, x, 5.0, 1.5, 0.5, f"문서 {d}", fc=PAPER, fs=10)
        cell(ax, x, 4.3, 1.5, 0.6, DICT.index(BRANDS[d - 1]), hot=(step == 1), fs=12)
    label(ax, 0.3, 3.4, "값 사전 (글자 순서)", fs=11, ha="left", bold=True)
    for k, v in enumerate(DICT):
        y = 2.55 - k * 0.7
        cell(ax, 0.3, y, 0.8, 0.6, k, fc=PAPER, fs=11)
        cell(ax, 1.2, y, 2.2, 0.6, v, fs=11)
    if step == 1:
        label(ax, 7.6, 3.65, "열: 순번만", fs=11, color=RED, bold=True)
        label(ax, 7.6, 2.3, "순번 순서 = 이름 순서", fs=10.5, color=INK)
        return
    label(ax, 7.6, 3.65, "브랜드별 건수", fs=11, bold=True, color=RED)
    for k, n in enumerate([3, 2, 2]):
        x = 5.0 + k * 2.25
        cell(ax, x, 2.35, 0.8, 0.6, k, fc=PAPER, fs=11)
        cell(ax, x + 0.85, 2.35, 1.0, 0.6, f"{n}건", hot=True, fs=11)
        label(ax, x + 0.9, 1.75, f"→ {DICT[k]}", fs=10, color=INK)
    moral(ax, 6.0, 0.35, "정렬·집계: 순번으로")


# ── 숫자는 숫자 필드에 담아요 ──────────────────────────────────────
def kwsort():
    """글자로 담으면 첫 글자 순서, long에 담으면 크기 순서."""
    fig, ax = canvas(7.2, 3.8, 12, 6.6)
    label(ax, 0.3, 5.6, "keyword (글자)", fs=11.5, ha="left", bold=True)
    cells(ax, 4.0, 5.2, ['"10"', '"100"', '"25"', '"3"', '"9"'], w=1.45, h=0.75, fs=12)
    for k, ch in enumerate("11239"):
        label(ax, 4.0 + k * 1.53 + 0.72, 4.75, ch, fs=11.5, color=INK)
    label(ax, 0.3, 4.75, "첫 글자", fs=10.5, ha="left", color=INK)
    label(ax, 7.6, 3.95, "첫 글자 비교  1 < 2 < 3 < 9", fs=10.5, color=INK)
    label(ax, 0.3, 2.6, "long (숫자)", fs=11.5, ha="left", bold=True)
    cells(ax, 4.0, 2.2, [3, 9, 10, 25, 100], w=1.45, h=0.75, hot=range(5), fs=12)
    label(ax, 7.6, 1.6, "숫자 크기 비교", fs=10.5, color=RED)
    moral(ax, 6.0, 0.6, "크기순 정렬: 숫자 필드")
    save(fig, OUT, "es10-kwsort.svg")


if __name__ == "__main__":
    S, L = (7.2, 3.8), (12, 6.6)
    stage(direction, 2, OUT, "es10-direction", S, L)
    flip()
    stage(docvalues, 2, OUT, "es10-docvalues", S, L)
    textf()
    stage(ordinals, 2, OUT, "es10-ordinals", S, L)
    kwsort()
