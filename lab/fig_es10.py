"""Elasticsearch 10편 그림 만들기. 실행: python lab/fig_es10.py  → docs/elasticsearch/img/10/*.svg

본문 절은 장면 띠로 그린다: 같은 무대를 여러 장 그리고 장마다 바뀐 곳만 빨강으로 칠한다.
예시는 쇼핑몰 주문 목록 화면의 주문 다섯 개와 브랜드 문서 1~7을 편 끝까지 잇는다
(.claude/writing/work/cal/units-es10.md).
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "es"))
from figkit import (GREY, INK, LIGHT, NOTE, PAPER, PINK, RED, arrow, box, bubble, canvas, cell,  # noqa: E402
                    cells, cylinder, label, moral, outdir, save, stage)
from matplotlib.patches import Rectangle  # noqa: E402

OUT = outdir("10")

ORDERS = {3: "나이키 에어맥스", 9: "아디다스 운동화", 10: "푸마 클라우드", 25: "나이키 양말", 100: "아디다스 모자"}
PUT = [3, 9, 10, 25, 100]              # 넣은 순서 = 숫자 순서
KW = [10, 100, 25, 3, 9]               # keyword(글자) 정렬
TITLE = [25, 3, 100, 9, 10]            # 제목 가나다순
BRANDS = ["나이키", "아디다스", "푸마", "나이키", "아디다스", "푸마", "나이키"]
INV = [("나이키", [1, 4, 7]), ("아디다스", [2, 5]), ("푸마", [3, 6])]
DICT = ["나이키", "아디다스", "푸마"]

CYL = (8.3, 3.3, 3.2, 1.6)
SAY = (7.3, 0.55, 4.4, 1.4)
TAIL = (9.9, 3.05)


def empty(ax, x, y, w, h, s="", fs=10, color=GREY):
    ax.add_patch(Rectangle((x, y), w, h, fc="white", ec=GREY, lw=1.0, ls="--"))
    if s:
        label(ax, x + w / 2, y + h / 2, s, fs=fs, color=color)


# ── 무대: 쇼핑몰 주문 목록 화면 ─────────────────────────────────────
ROW_Y = [4.25 - k * 0.6 for k in range(5)]


def screen(ax, order, btn=None, hot=False, dim=False):
    """주문 목록 화면. order=주문번호 차례, btn='title'|'no'(빨간 버튼), hot=줄 빨강, dim=줄 회색."""
    box(ax, 0.4, 0.65, 6.5, 5.75, fc="white", round_=False)
    ax.add_patch(Rectangle((0.4, 5.95), 6.5, 0.45, fc=LIGHT, ec=INK, lw=1.2))
    label(ax, 0.6, 6.17, "쇼핑몰 주문 목록", fs=11, ha="left", color=INK)
    for key, x, w, s in (("title", 0.7, 1.6, "제목순"), ("no", 2.5, 2.0, "주문번호순")):
        on = btn == key
        ax.add_patch(Rectangle((x, 5.2), w, 0.5, fc=PINK if on else LIGHT, ec=RED if on else INK, lw=2.0 if on else 1.2))
        label(ax, x + w / 2, 5.45, s, fs=11, color=RED if on else "#222", bold=on)
    label(ax, 1.3, 4.85, "주문번호", fs=10, color=INK)
    label(ax, 3.9, 4.85, "상품 제목", fs=10, color=INK)
    ax.plot([0.65, 6.65], [4.62, 4.62], color=INK, lw=1.0)
    for y, n in zip(ROW_Y, order):
        if hot:
            ax.add_patch(Rectangle((0.65, y - 0.25), 6.0, 0.5, fc=PINK, ec=RED, lw=1.5))
        else:
            ax.plot([0.65, 6.65], [y - 0.28, y - 0.28], color=GREY, lw=0.8)
        c = RED if hot else (GREY if dim else "#222")
        label(ax, 1.3, y, n, fs=11.5, color=c, bold=hot)
        label(ax, 2.4, y, ORDERS[n], fs=11.5, ha="left", color=c)


def es(ax, say, hot=False):
    cylinder(ax, *CYL, "ES")
    bubble(ax, *SAY, say, TAIL, hot=hot, fs=11)


def error_window(ax):
    ax.add_patch(Rectangle((1.0, 1.35), 5.3, 2.75, fc="white", ec=RED, lw=2.2, zorder=5))
    ax.add_patch(Rectangle((1.0, 3.65), 5.3, 0.45, fc=PINK, ec=RED, lw=2.0, zorder=5))
    label(ax, 1.2, 3.87, "오류", fs=11, ha="left", color=RED, bold=True, zorder=6)
    label(ax, 3.65, 2.95, "Text fields are not\noptimised …", fs=11, color=RED, family="monospace", zorder=6)
    label(ax, 3.65, 1.85, "title(text)로는 줄 세울 수 없어요", fs=10.5, color=RED, zorder=6)


def opening(ax, step):
    if step == 1:
        screen(ax, PUT)
        es(ax, "주문 5개를 넣었어요\n검색은 잘 돼요")
    elif step == 2:
        screen(ax, PUT, btn="title")
        error_window(ax)
        es(ax, "title은 text 필드라\n정렬이 막혀 있어요", hot=True)
    else:
        screen(ax, KW, btn="no", hot=True)
        es(ax, "order_no_kw(keyword)로\n줄 세웠어요", hot=True)
        moral(ax, 3.65, 0.2, "3번 주문이 100번 주문보다 뒤에 있어요")


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
    label(ax, 0.3, 6.1, "역색인: 값 → 문서", fs=12, ha="left", bold=True)
    if step == 1:
        inverted(ax, x0=0.7, hot_row=0)
        label(ax, 8.6, 4.55, "나이키가 든 문서는?", fs=12, color=RED, bold=True)
        label(ax, 8.6, 3.75, "나이키 줄 하나만 읽어요", fs=11, color=RED)
        label(ax, 8.6, 2.7, "검색은 이 방향이라 빨라요", fs=10.5, color=INK)
        return
    inverted(ax, x0=0.7, hot_doc=7 if step == 2 else None, mark=(step == 2))
    if step == 2:
        label(ax, 8.6, 4.55, "문서 7의 브랜드는?", fs=12, color=RED, bold=True)
        label(ax, 8.6, 3.75, "①②③ 목록을 다 뒤져야 알아요", fs=11, color=RED)
        return
    label(ax, 8.6, 4.55, "문서 7의 브랜드는?", fs=11, color=INK)
    label(ax, 0.3, 2.25, "검색 결과를 브랜드순으로 줄 세우려면", fs=11, ha="left", color=RED)
    for d in range(1, 8):
        x = 0.3 + (d - 1) * 1.62
        cell(ax, x, 1.35, 1.5, 0.55, f"문서 {d}", fc=PAPER, fs=10)
        label(ax, x + 0.75, 1.0, "브랜드?", fs=10, color=RED, bold=True)
    moral(ax, 6.0, 0.3, "정렬은 문서마다 값을 묻는 반대 방향이에요")


# ── 뒤집어 쓰기는 비싸요 (fielddata) ──────────────────────────────
HX, HY, HW, HH = 6.7, 1.3, 4.9, 4.2
FD = [(1, "나이키"), (2, "아디다스"), (3, "푸마"), None, (7, "나이키")]


def flip(ax, step):
    label(ax, 0.3, 6.1, "역색인 (디스크)", fs=12, ha="left", bold=True)
    inverted(ax, x0=0.3, grey=(step == 3))
    label(ax, HX + HW / 2, 6.1, "JVM 힙 (ES의 메모리)", fs=12, bold=True)
    over = step == 3
    box(ax, HX, HY, HW, HH, fc=PINK if over else "white", ec=RED if over else INK, lw=2.2 if over else 1.6, round_=False)
    if step == 1:
        label(ax, HX + HW / 2, HY + HH / 2, "비어 있어요", fs=11, color=GREY)
        label(ax, 3.0, 1.8, "브랜드순 정렬이 처음 왔어요", fs=11, color=INK)
        return
    hot = step == 2
    for k, r in enumerate(FD):
        y = HY + HH - 0.75 - k * 0.68
        if r is None:
            label(ax, HX + HW / 2, y + 0.28, "⋮", fs=13, color=INK)
            continue
        cell(ax, HX + 0.4, y, 1.5, 0.55, f"문서 {r[0]}", fc=PAPER, fs=10)
        cell(ax, HX + 2.0, y, 2.4, 0.55, r[1], hot=hot, fs=10.5)
    if hot:
        arrow(ax, (5.4, 4.65), (HX - 0.1, 4.65), color=RED, ms=16)
        label(ax, 3.0, 2.2, "모든 목록을 훑어 뒤집어요", fs=11, color=RED, bold=True)
        label(ax, 3.0, 1.55, "문서 100만 개 · 79 ms", fs=11, color=RED)
        return
    label(ax, HX + HW / 2, 1.6, "⋮  수억 줄", fs=11, color=RED, bold=True)
    label(ax, 3.0, 2.2, "문서가 수억 개면", fs=11, color=RED, bold=True)
    label(ax, 3.0, 1.55, "뒤집은 표가 힙을 다 차지해요", fs=11, color=RED)
    moral(ax, 6.0, 0.45, "그래서 text 필드의 fielddata는 꺼 두었어요")


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
    label(ax, 1.7, 5.28, "역색인에 적어요 (1편)", fs=10, ha="left", color=INK)
    if step == 1:
        empty(ax, CX, 1.15, 3.6, 3.15, "?", fs=14)
        return
    hot = step == 2
    label(ax, CX + 1.8, 4.6, "doc values (열)", fs=10.5, color=RED if hot else INK, bold=hot)
    for d, (y, v) in enumerate(zip(COL_Y, BRANDS), start=1):
        cell(ax, CX, y, 1.3, 0.42, f"문서 {d}", fc=PAPER, fs=9)
        cell(ax, CX + 1.4, y, 2.2, 0.42, v, hot=hot or (step == 3 and d in RESULT), fs=9.5)
    if hot:
        arrow(ax, (4.6, 6.05), (CX + 2.5, 4.85), color=RED, ms=15, rad=-0.15)
        label(ax, 6.0, 5.35, "열에도 적어요", fs=11, color=RED, bold=True, ha="left")
        return
    arrow(ax, (4.6, 6.05), (CX + 2.5, 4.85), color=GREY, ms=13, rad=-0.15)
    for d in RESULT:
        y = COL_Y[d - 1] + 0.21
        arrow(ax, (CX - 0.75, y), (CX - 0.08, y), color=RED, ms=12, lw=1.6)
    label(ax, 3.5, 1.35, "결과 문서 칸만 바로 읽어요 · 1만 개 4 ms", fs=10.5, color=RED, bold=True)
    moral(ax, 6.0, 0.4, "doc values는 색인할 때 디스크에 적어 두는 문서 → 값 열이에요")


# ── text 필드는 열을 만들지 않아요 ─────────────────────────────────
def textf(ax, step):
    box(ax, 0.3, 5.45, 4.6, 0.75, fc=NOTE)
    label(ax, 2.6, 5.82, "넣는 제목 · 나이키 에어맥스", fs=11)
    label(ax, 0.3, 4.75, "title (text)", fs=11, ha="left", bold=True)
    arrow(ax, (2.9, 5.4), (2.9, 4.1), color=RED if step == 1 else GREY, ms=13)
    cells(ax, 0.3, 3.35, ["나이키", "에어맥스"], w=1.8, h=0.65, hot=(0, 1) if step == 1 else (), fs=11)
    label(ax, 2.2, 2.85, "분석기가 두 조각으로 잘라요 (2편)", fs=10.5, color=RED if step == 1 else INK)
    label(ax, 2.2, 2.3, "역색인에는 조각만 들어가요", fs=10.5, color=INK)
    label(ax, 8.6, 4.75, "title의 doc values", fs=11, bold=True)
    if step == 1:
        empty(ax, 6.6, 3.35, 4.0, 0.65, "?", fs=13)
        return
    empty(ax, 6.6, 3.35, 4.0, 0.65, "만들지 않아요", fs=11, color=RED if step == 2 else GREY)
    if step == 2:
        label(ax, 8.6, 2.85, "제목 전체는 값으로 남지 않아요", fs=10.5, color=RED, bold=True)
        label(ax, 8.6, 2.3, "조각으로 줄 세우면 제목순이 안 돼요", fs=10.5, color=INK)
        return
    label(ax, 8.6, 2.85, "제목 전체는 값으로 남지 않아요", fs=10.5, color=INK)
    label(ax, 3.4, 1.4, "title.raw\n(keyword 하위 필드)", fs=10.5, ha="right", color=RED)
    cell(ax, 3.6, 1.05, 3.6, 0.65, "나이키 에어맥스", hot=True, fs=11)
    arrow(ax, (5.4, 5.4), (5.4, 1.8), color=RED, ms=14)
    moral(ax, 6.0, 0.4, "제목 정렬은 keyword 하위 필드로 해요")


# ── 문자열은 순번으로 담아요 ───────────────────────────────────────
def ordinals(ax, step):
    label(ax, 0.3, 6.15, "브랜드 열 (doc values)", fs=12, ha="left", bold=True)
    for d in range(1, 8):
        x = 0.3 + (d - 1) * 1.6
        cell(ax, x, 5.0, 1.5, 0.5, f"문서 {d}", fc=PAPER, fs=10)
        if step < 3:
            cell(ax, x, 4.3, 1.5, 0.6, BRANDS[d - 1], hot=(step == 1 and BRANDS[d - 1] == "나이키"), fs=10.5)
        else:
            cell(ax, x, 4.3, 1.5, 0.6, DICT.index(BRANDS[d - 1]), hot=(step == 3), fs=12)
    if step == 1:
        label(ax, 6.0, 3.6, "나이키가 문서 수만큼 반복돼요", fs=11, color=RED, bold=True)
        return
    hot = step == 2
    label(ax, 0.3, 3.4, "값 사전 (글자 순서, 한 번씩)", fs=11, ha="left", bold=True, color=RED if hot else "#222")
    for k, v in enumerate(DICT):
        y = 2.55 - k * 0.7
        cell(ax, 0.3, y, 0.8, 0.6, k, fc=PAPER, fs=11)
        cell(ax, 1.2, y, 2.2, 0.6, v, hot=hot, fs=11)
    if step == 2:
        label(ax, 7.6, 2.3, "서로 다른 값만 적고\n0, 1, 2 번호를 붙여요", fs=11, color=RED)
        return
    if step == 3:
        label(ax, 7.6, 3.65, "열에는 순번만 적어요", fs=11, color=RED, bold=True)
        label(ax, 7.6, 2.3, "순번이 작을수록 이름도 앞이에요\n작은 정수끼리 비교하면 이름순", fs=10.5, color=INK)
        return
    label(ax, 7.6, 3.65, "브랜드별 건수", fs=11, bold=True, color=RED)
    for k, n in enumerate([3, 2, 2]):
        x = 5.0 + k * 2.25
        cell(ax, x, 2.35, 0.8, 0.6, k, fc=PAPER, fs=11)
        cell(ax, x + 0.85, 2.35, 1.0, 0.6, f"{n}건", hot=True, fs=11)
        label(ax, x + 0.9, 1.75, f"→ {DICT[k]}", fs=10, color=INK)
    label(ax, 8.4, 1.15, "다 센 다음 사전에서 이름으로 바꿔요", fs=10, color=INK)
    moral(ax, 6.0, 0.35, "정렬과 집계는 순번(작은 정수)으로 해요")


# ── 숫자는 숫자 필드에 담아요 ──────────────────────────────────────
def kwsort(ax, step):
    label(ax, 0.3, 5.6, "keyword (글자)로 정렬", fs=11.5, ha="left", bold=True)
    cells(ax, 4.0, 5.2, ['"10"', '"100"', '"25"', '"3"', '"9"'], w=1.45, h=0.75, fs=12)
    for k, ch in enumerate("11239"):
        label(ax, 4.0 + k * 1.53 + 0.72, 4.75, ch, fs=11.5, color=RED if step == 1 else INK, bold=step == 1)
    label(ax, 0.3, 4.75, "첫 글자", fs=10.5, ha="left", color=INK)
    if step == 1:
        label(ax, 7.6, 3.95, "첫 글자부터 비교해요  1 < 2 < 3 < 9", fs=11, color=RED, bold=True)
        label(ax, 0.3, 2.6, "long (숫자)으로 정렬", fs=11.5, ha="left", bold=True, color=GREY)
        empty(ax, 4.0, 2.2, 7.6, 0.75)
        return
    label(ax, 7.6, 3.95, "첫 글자부터 비교해요  1 < 2 < 3 < 9", fs=10.5, color=INK)
    label(ax, 0.3, 2.6, "long (숫자)으로 정렬", fs=11.5, ha="left", bold=True)
    cells(ax, 4.0, 2.2, [3, 9, 10, 25, 100], w=1.45, h=0.75, hot=range(5), fs=12)
    label(ax, 7.6, 1.6, "doc values에 숫자로 담겨요", fs=10.5, color=RED)
    moral(ax, 6.0, 0.6, "크기 순서로 줄 세우려면 숫자 필드에 담아요")


# ── 번호는 언제 숫자 필드에 ────────────────────────────────────────
def decide():
    fig, ax = canvas(10, 3.6, 15, 5.4)
    box(ax, 0.3, 3.6, 6.0, 1.3, fc=NOTE)
    label(ax, 3.3, 4.25, "이 번호로 줄 세우거나\n범위로 찾나요?", fs=10.5, bold=True)
    arrow(ax, (6.4, 4.25), (8.4, 4.25), color=RED)
    label(ax, 7.4, 4.55, "예", fs=10, color=RED)
    box(ax, 8.5, 3.6, 6.2, 1.3, fc=PINK, ec=RED)
    label(ax, 11.6, 4.25, "long 같은 숫자 필드에 담아요", fs=10.5, color=RED, bold=True)
    arrow(ax, (3.3, 3.5), (3.3, 2.6))
    label(ax, 3.6, 3.05, "아니요", fs=10, color=INK, ha="left")
    box(ax, 0.3, 1.3, 6.0, 1.2, fc=PAPER)
    label(ax, 3.3, 1.9, "정확히 같은 값으로만 찾으면\nkeyword에 담아요 (앞자리 0도 그대로)", fs=10)
    arrow(ax, (11.6, 3.5), (11.6, 2.6))
    label(ax, 11.9, 3.05, "앞자리 0을 지켜야 하면", fs=10, color=INK, ha="left")
    box(ax, 8.5, 1.3, 6.2, 1.2, fc=PAPER)
    label(ax, 11.6, 1.9, "keyword로 두고 정렬은 따로\nlong 필드나 주문 시각(date)으로", fs=10)
    save(fig, OUT, "es10-decide.svg")


# ── 정리: 처음 장면으로 돌아가기 ───────────────────────────────────
def back(ax, step):
    if step == 1:
        screen(ax, KW, dim=True)
        es(ax, "처음엔 제목순은 오류,\n주문번호순은 10이 먼저였어요")
    elif step == 2:
        screen(ax, TITLE, btn="title", hot=True)
        es(ax, "title.raw 열의 순번으로\n줄 세웠어요", hot=True)
    else:
        screen(ax, PUT, btn="no", hot=True)
        es(ax, "long 열로\n줄 세웠어요", hot=True)
        moral(ax, 3.65, 0.2, "정렬은 역색인 대신 doc values 열을 읽어요")


# ── 정리: 낱말 카드 ────────────────────────────────────────────────
def cards():
    fig, ax = canvas(6.4, 7.8, 9.8, 12.2)
    W, H = 4.6, 3.8

    def card(i, name, line):
        col, row = i % 2, i // 2
        x, y = 0.2 + col * 4.9, 8.2 - row * 4.05
        box(ax, x, y, W, H, fc="white")
        label(ax, x + 0.25, y + H - 0.4, name, fs=12.5, ha="left", bold=True)
        label(ax, x + W / 2, y + 0.6, line, fs=10, color=INK)
        return x, y

    x, y = card(0, "doc values", "색인할 때 디스크에 적는\n문서 → 값 열")
    for k, v in enumerate(["나이키", "아디다스"]):
        cell(ax, x + 0.6, y + 2.2 - k * 0.5, 1.2, 0.45, f"문서 {k + 1}", fc=PAPER, fs=9)
        cell(ax, x + 1.9, y + 2.2 - k * 0.5, 1.9, 0.45, v, hot=True, fs=9.5)
    x, y = card(1, "fielddata", "첫 정렬 때 역색인을 뒤집어\n힙에 만드는 문서 → 값 표")
    cell(ax, x + 0.4, y + 1.95, 1.4, 0.5, "나이키", fs=9.5)
    label(ax, x + 1.95, y + 2.2, "1 4 7", fs=9.5, ha="left", color=INK)
    arrow(ax, (x + 2.75, y + 2.2), (x + 3.25, y + 2.2), color=RED, ms=11)
    box(ax, x + 3.35, y + 1.9, 0.95, 0.6, fc=PINK, ec=RED, lw=1.4, round_=False)
    label(ax, x + 3.82, y + 2.2, "힙", fs=10, color=RED)
    x, y = card(2, "순번 (ordinal)", "값 사전에서 붙인 번호,\n열에는 이 번호만 적어요")
    cells(ax, x + 0.5, y + 1.95, [0, 1, 2, 0, 1, 2, 0], w=0.48, h=0.5, gap=0.04, hot=range(7), fs=10)
    x, y = card(3, "집계", "조건에 맞는 문서를\n묶어 세는 일")
    for k, (b, n) in enumerate([("나이키", 3), ("아디다스", 2)]):
        cell(ax, x + 0.5, y + 2.25 - k * 0.55, 1.9, 0.48, b, fs=9.5)
        cell(ax, x + 2.5, y + 2.25 - k * 0.55, 1.1, 0.48, f"{n}건", hot=True, fs=9.5)
    x, y = card(4, "keyword 하위 필드", "같은 글을 자르지 않고\n한 값으로 함께 담기")
    cell(ax, x + 0.4, y + 2.25, 3.8, 0.45, "title: 나이키 · 에어맥스", fs=9.5)
    cell(ax, x + 0.4, y + 1.7, 3.8, 0.45, "title.raw: 나이키 에어맥스", hot=True, fs=9.5)
    x, y = card(5, "JVM 힙", "ES가 객체를 담는 메모리,\n차면 노드가 느려지거나 멈춰요")
    box(ax, x + 0.6, y + 1.7, 3.4, 0.75, fc="white", round_=False)
    ax.add_patch(Rectangle((x + 0.6, y + 1.7), 2.9, 0.75, fc=PINK, ec=RED, lw=1.4))
    save(fig, OUT, "es10-cards.svg")


if __name__ == "__main__":
    S, L = (7.2, 3.8), (12, 6.6)
    stage(opening, 3, OUT, "es10-open", S, L)
    stage(direction, 3, OUT, "es10-direction", S, L)
    stage(flip, 3, OUT, "es10-flip", S, L)
    stage(docvalues, 3, OUT, "es10-docvalues", S, L)
    stage(textf, 3, OUT, "es10-text", S, L)
    stage(ordinals, 4, OUT, "es10-ordinals", S, L)
    stage(kwsort, 2, OUT, "es10-kwsort", S, L)
    decide()
    stage(back, 3, OUT, "es10-back", S, L)
    cards()
