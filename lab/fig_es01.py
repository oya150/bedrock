"""Elasticsearch 1편 그림 만들기. 실행: python lab/fig_es01.py  → docs/elasticsearch/img/01/*.svg

본문 절은 장면 띠로 그린다: 같은 무대를 여러 장 그리고 장마다 바뀐 곳만 빨강으로 칠한다.
예시는 편 끝까지 같은 글(1~6, 9)과 같은 번호를 쓴다.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "es"))
from figkit import (GREY, INK, LIGHT, NOTE, PAPER, PINK, RED, YEL, arrow, box, bubble, canvas, cell, cells,  # noqa: E402
                    cylinder, label, moral, outdir, save, stage)
from figkit import board as fk_board  # noqa: E402
from matplotlib.patches import Rectangle  # noqa: E402

OUT = outdir("01")

POSTS = ["주문 환불 요청", "주문 배송 언제", "환불 완료 감사", "사이즈 교환 문의", "주문 취소했어요", "색상이 달라요"]
DOCS = {1: ["주문", "환불", "요청"], 2: ["주문", "배송", "언제"], 3: ["환불", "완료", "감사"]}
TERMS = ["감사", "배송", "언제", "완료", "요청", "주문", "환불"]
REFUND = [1, 3, 7, 12, 20]
ORDER = [1, 2, 5, 7, 15, 20]


def ask(ax, s, x=8.4, y=5.6, w=3.4):
    """찾는 것 상자. 장면 띠마다 같은 자리에 둔다."""
    box(ax, x, y, w, 0.72, fc=PAPER)
    label(ax, x + w / 2, y + 0.36, s, fs=12.5)


def empty(ax, x, y, w, h):
    ax.add_patch(Rectangle((x, y), w, h, fc="white", ec=GREY, lw=1.0, ls="--"))


# ── 1번 글부터 다 읽기 ─────────────────────────────────────────────
ROW_Y = [4.15 - k * 0.55 for k in range(6)]
CYL = (8.6, 3.2, 2.6, 1.3)           # 오른쪽 위 저장소 원통 자리
SAY = (7.5, 0.95, 4.3, 1.25)         # 그 아래 말풍선 자리
SAY_TAIL = (9.9, 2.95)


def board(ax, hot=(), dim=(), checks=False):
    """처음 장면과 돌아오는 장면의 무대: 쇼핑몰 문의 게시판 화면."""
    fk_board(ax, list(enumerate(POSTS, 1)), hot=hot, dim=dim, checks=checks)


def scan(ax, step):
    board(ax, hot={2: (1,), 3: (1, 3)}.get(step, ()), checks=(step == 3))
    cylinder(ax, *CYL, "데이터베이스")
    if step == 1:
        bubble(ax, *SAY, "'환불'이 어느 글에\n들었는지 몰라요", SAY_TAIL)
    elif step == 2:
        arrow(ax, (0.05, ROW_Y[0]), (0.55, ROW_Y[0]), color=RED, ms=14)
        bubble(ax, *SAY, "1번 글부터 읽어요\n환불이 있으니 골라요", SAY_TAIL, hot=True)
    else:
        arrow(ax, (0.3, ROW_Y[0]), (0.3, 0.75), color=RED, ms=14)
        bubble(ax, *SAY, "끝까지 한 줄씩 다 읽어요\n글이 열 배면 시간도 열 배", SAY_TAIL, hot=True)
        moral(ax, 6.0, 0.2, "환불이 든 글을 다 찾으려면 백만 줄을 다 읽어요")


# ── 정렬해 둔 데이터베이스 인덱스 ──────────────────────────────────
INDEX = sorted(POSTS + ["교환 문의", "빠른 환불 부탁", "쿠폰 문의", "환불 언제 돼요", "환불 요청합니다"])


def prefix(ax, step):
    label(ax, 0.3, 6.3, "데이터베이스 인덱스 (제목 가나다순)", fs=12.5, ha="left", bold=True)
    for k, r in enumerate(INDEX):
        y = 5.55 - k * 0.47
        start, inside = r.startswith("환불"), "환불" in r
        hot = (step == 2 and start) or (step == 3 and inside)
        cell(ax, 1.3, y, 3.8, 0.42, r, hot=hot, fs=10.5)
        if step == 3 and inside:
            label(ax, 5.4, y + 0.21, "●", fs=11, color=RED)
    first = 5.55 - 8 * 0.47
    cylinder(ax, 9.8, 4.6, 1.8, 0.8, "데이터베이스")
    say, tail = (6.0, 2.55, 5.8, 1.3), (10.7, 4.35)
    if step == 1:
        bubble(ax, *say, "국어사전처럼 제목을\n가나다순으로 늘어놨어요", tail)
    elif step == 2:
        arrow(ax, (0.2, first + 0.21), (1.2, first + 0.21), color=RED, ms=14)
        bubble(ax, *say, "'환불%'는 한곳에 모여 있어서\n그 자리로 바로 가요", tail, hot=True)
        label(ax, 6.0, 1.75, "'환불%'는 환불로 시작하는 제목,\n%는 아무 글자나 와도 된다는 표시", fs=10.5, ha="left", color=INK)
    else:
        bubble(ax, *say, "'%환불%'는 ㅃ, ㅈ, ㅎ에 흩어져서\n처음부터 다 읽어요", tail, hot=True)
        label(ax, 6.0, 1.85, "'%환불%'는 어디든 환불이 든 제목", fs=10.5, ha="left", color=INK)
        moral(ax, 6.0, 0.25, "정렬해 둬도 중간에 든 낱말은 못 찾아가요")


# ── 글마다 낱말 목록 ───────────────────────────────────────────────
def doc_rows(ax, x0, y0, dy, hot_rows=(), hot_term=None, w=1.1, fs=11.5):
    for k, (d, ws) in enumerate(DOCS.items()):
        y = y0 - k * dy
        row_hot = d in hot_rows
        cell(ax, x0, y, 0.85, 0.7, f"글 {d}", hot=row_hot, fc=None if row_hot else PAPER, fs=fs)
        hot = range(3) if row_hot else [i for i, t in enumerate(ws) if t == hot_term]
        cells(ax, x0 + 0.95, y, ws, w=w, h=0.7, hot=hot, fs=fs)


def forward(ax, step):
    label(ax, 0.3, 6.3, "글마다 낱말 목록  (글 → 낱말)", fs=12.5, ha="left", bold=True)
    ask(ax, "3번 글에 무슨 낱말?" if step == 1 else "환불이 든 글은?", x=7.9, w=3.9)
    doc_rows(ax, 2.1, 4.6, 1.1, hot_rows=(3,) if step == 1 else (), hot_term="환불" if step == 2 else None)
    label(ax, 3.9, 1.6, "⋮  글이 백만 개", fs=12, color=INK)
    if step == 1:
        arrow(ax, (9.0, 5.5), (6.6, 2.75), color=RED, ms=14)
        label(ax, 8.6, 3.6, "글 3 줄만 보면\n바로 답이 나와요", fs=12, ha="left", color=RED)
    else:
        for k in range(3):
            y = 4.6 - k * 1.1 + 0.35
            arrow(ax, (1.25, y), (2.0, y), color=RED, ms=12)
            label(ax, 0.75, y, "①②③"[k], fs=12, color=RED)
        label(ax, 8.0, 3.6, "글을 하나씩\n열어 봐야 알아요", fs=12, ha="left", color=RED)
        moral(ax, 6.0, 0.4, "방향이 반대라 글 백만 개를 다 열어 봐요")


# ── 뒤집기 ─────────────────────────────────────────────────────────
INV = {}
for _d, _ws in DOCS.items():
    for _t in _ws:
        INV.setdefault(_t, []).append(_d)


def flip(ax, step):
    label(ax, 0.3, 6.3, "글마다 낱말 목록", fs=12.5, ha="left", bold=True)
    doc_rows(ax, 0.3, 5.0, 1.0, hot_rows=(1,) if step == 1 else (), w=0.95, fs=11)
    arrow(ax, (4.5, 3.85), (5.6, 3.85), lw=3, ms=24, color=RED if step == 1 else INK)
    label(ax, 5.05, 4.4, "뒤집기", fs=12, color=RED if step == 1 else INK, bold=True)
    label(ax, 8.9, 6.3, "낱말마다 글 번호 (역색인)", fs=12.5, bold=True)
    label(ax, 6.65, 5.85, "낱말 (가나다순)", fs=10.5, color=INK)
    label(ax, 9.45, 5.85, "글 번호 (번호순)", fs=10.5, color=INK)
    for k, t in enumerate(TERMS):
        y = 5.0 - k * 0.66
        ds = INV[t] if step > 1 else [d for d in INV[t] if d == 1]
        if not ds:
            empty(ax, 6.0, y, 1.3, 0.56)
            continue
        on = (step == 1) or (step == 3 and t == "환불")
        cell(ax, 6.0, y, 1.3, 0.56, t, hot=on, fs=11)
        arrow(ax, (7.4, y + 0.28), (8.0, y + 0.28), lw=1.3, ms=10, color=RED if on else INK)
        for j, d in enumerate(ds):
            new = step == 1 or (step == 2 and d != 1) or (step == 3 and t == "환불")
            cell(ax, 8.1 + j * 0.65, y, 0.58, 0.56, d, hot=new, fs=11)
    if step == 1:
        label(ax, 10.1, 3.0, "글 1의 낱말\n칸마다 1을\n적어요", fs=11.5, ha="left", color=RED)
    elif step == 2:
        label(ax, 10.1, 3.0, "글 2, 3도\n같이 적어요", fs=11.5, ha="left", color=RED)
    else:
        label(ax, 10.1, 1.25, "← 환불이 든 글", fs=11.5, ha="left", color=RED)
        moral(ax, 6.0, 0.25, "환불 줄 하나만 보면 1번과 3번 글이 나와요")


# ── 사전에서 낱말 하나 찾기 ─────────────────────────────────────────
def lookup(ax, step):
    label(ax, 0.3, 6.3, "가나다순으로 정렬한 낱말 일곱", fs=12.5, ha="left", bold=True)
    ask(ax, "찾기: 환불", x=9.0, y=5.55, w=2.8)
    seen = {2: (3,), 3: (3, 5), 4: (3, 5, 6)}.get(step, ())
    gone = {2: range(0, 3), 3: range(0, 5), 4: range(0, 6)}.get(step, ())
    X = [0.3 + k * 1.6 for k in range(7)]
    for k, t in enumerate(TERMS):
        cur = seen and k == seen[-1]
        cell(ax, X[k], 3.7, 1.45, 0.8, t, hot=cur, dim=(k in gone and not cur), fs=12)
    for n, i in enumerate(seen):
        cur = n == len(seen) - 1
        x = X[i] + 0.72
        arrow(ax, (x, 2.95), (x, 3.6), color=RED if cur else INK, lw=1.6, ms=12)
        label(ax, x, 2.65, "①②③"[n], fs=12.5, color=RED if cur else INK, bold=cur)
    if step == 1:
        label(ax, 6.0, 1.9, "가운데 낱말부터 봐요", fs=12.5, color=INK)
    elif step == 2:
        label(ax, 6.0, 1.6, "환불은 완료보다 뒤 → 앞 절반을 버려요", fs=12.5, color=RED)
    elif step == 3:
        label(ax, 6.0, 1.6, "환불은 주문보다 뒤 → 또 앞을 버려요", fs=12.5, color=RED)
    else:
        cells(ax, X[6] + 0.1, 1.35, [1, 3], w=0.6, h=0.6, hot=(0, 1), fs=11.5)
        label(ax, X[6] - 0.2, 1.65, "글", fs=11.5, ha="right", color=RED)
        label(ax, 4.6, 1.65, "닿았어요. 달린 글 번호를 꺼내요", fs=12.5, color=RED)
        moral(ax, 6.0, 0.4, "볼 때마다 반씩 버려서 세 번 만에 환불에 닿아요")


# ── 심화: 사전은 디스크에 블록으로 ─────────────────────────────────
def blocks(ax, step):
    ask(ax, "찾기: 환불", x=0.3, y=5.6, w=3.4)
    label(ax, 8.3, 6.3, "디스크: 정렬한 낱말을 수십 개씩 묶은 블록", fs=11.5, color=INK)
    groups = [["감사", "배송", "…"], ["언제", "완료", "요청"], ["주문", "환불", "…"]]
    for k, g in enumerate(groups):
        y = 4.9 - k * 1.25
        hot = step == 2 and k == 2
        cells(ax, 6.0, y, g, w=1.3, h=0.8, hot=(1,) if hot else (), fs=11.5)
        label(ax, 10.3, y + 0.4, f"블록 {k + 1}", fs=11.5, color=RED if hot else INK, ha="left", bold=hot)
    label(ax, 8.0, 1.15, "⋮  블록이 아주 많아요", fs=11.5, color=INK)
    if step == 1:
        label(ax, 0.3, 3.4, "어느 블록에\n있을까요?", fs=12.5, ha="left", color=INK)
        label(ax, 0.3, 2.1, "블록을 다 읽으면\n느려요", fs=12, ha="left", color=INK)
    else:
        box(ax, 0.3, 1.7, 3.6, 3.2, fc=PINK, ec=RED)
        label(ax, 2.1, 4.45, "작은 안내판", fs=12, color=RED, bold=True)
        for k, t in enumerate(["ㄱ~ㅂ → 블록 1", "ㅅ~ㅇ → 블록 2", "ㅈ~ㅎ → 블록 3"]):
            label(ax, 2.1, 3.75 - k * 0.6, t, fs=11.5, color=RED if k == 2 else "#222")
        arrow(ax, (4.0, 2.55), (5.9, 2.55), color=RED)
        moral(ax, 6.0, 0.35, "안내판으로 블록을 고르고 그 블록 하나만 읽어요")


# ── 손가락 두 개로 겹치기 ──────────────────────────────────────────
def fingers(ax, step):
    W, G = 0.85, 0.08
    xa = lambda i: 1.6 + i * (W + G)  # noqa: E731
    pos = {1: (0, 0), 2: (0, 0), 3: (1, 1)}.get(step)
    both = [1, 7, 20]
    label(ax, 0.3, 6.3, "게시판 글이 더 쌓여 두 줄이 길어졌어요", fs=12, ha="left", color=INK)
    label(ax, 0.3, 4.65, "환불", fs=12.5, ha="left", bold=True)
    label(ax, 0.3, 2.65, "주문", fs=12.5, ha="left", bold=True)
    hot_a = (0,) if step == 2 else ((1,) if step == 3 else ())
    hot_b = (0,) if step == 2 else ((1,) if step == 3 else ())
    if step == 4:
        hot_a = [REFUND.index(v) for v in both]
        hot_b = [ORDER.index(v) for v in both]
    cells(ax, 1.6, 4.25, REFUND, w=W, h=0.8, gap=G, hot=hot_a, fs=12)
    cells(ax, 1.6, 2.25, ORDER, w=W, h=0.8, gap=G, hot=hot_b, fs=12)
    if pos:
        i, j = pos
        ax.plot([xa(i) + W / 2], [5.35], marker="v", ms=13, color=RED)
        ax.plot([xa(j) + W / 2], [1.95], marker="^", ms=13, color=RED)
    # 결과 칸
    label(ax, 9.9, 5.5, "둘 다 있는 글", fs=12, color=INK)
    res = {1: [], 2: [1], 3: [1], 4: both}[step]
    for k in range(3):
        x = 8.75 + k * 0.8
        if k < len(res):
            cell(ax, x, 4.55, 0.7, 0.7, res[k], hot=(step == 2) or step == 4, fs=12)
        else:
            empty(ax, x, 4.55, 0.7, 0.7)
    if step == 1:
        label(ax, 6.0, 1.0, "두 목록 맨 앞에 손가락을 하나씩 올려요", fs=12.5, color=RED)
    elif step == 2:
        label(ax, 6.0, 1.0, "둘 다 1이에요. 결과에 넣고 둘 다 한 칸 앞으로", fs=12.5, color=RED)
    elif step == 3:
        arrow(ax, (xa(1) + W / 2, 2.15), (xa(2) + W / 2, 2.15), color=RED, rad=0.5, ms=12)
        label(ax, 6.0, 1.0, "3과 2가 달라요. 작은 쪽(주문 2)만 한 칸 앞으로", fs=12.5, color=RED)
    else:
        for v in both:
            x = xa(REFUND.index(v)) + W / 2
            x2 = xa(ORDER.index(v)) + W / 2
            ax.plot([x, x2], [4.2, 3.1], color=RED, lw=2)
        label(ax, 9.9, 3.4, "손가락은\n뒤로 가지 않아요", fs=11.5, color=INK)
        moral(ax, 6.0, 0.6, "두 목록을 한 번씩만 훑으면 끝나요")


# ── 잘라 둔 낱말로만 찾기 ──────────────────────────────────────────
def miss(ax, step):
    cell(ax, 0.3, 5.45, 3.6, 0.7, "글 9: 환불했어요 감사", fc=PAPER, fs=11.5)
    arrow(ax, (4.0, 5.8), (5.0, 5.8))
    label(ax, 4.5, 6.35, "띄어쓰기로 자르기", fs=10.5, color=INK)
    cells(ax, 5.1, 5.45, ["환불했어요", "감사"], w=1.9, h=0.7, hot=(0, 1) if step == 1 else (), fs=11.5)
    if step == 2:
        ask(ax, "찾기: 환불", x=9.2, y=5.45, w=2.6)
    label(ax, 0.3, 4.55, "용어 사전", fs=12, ha="left", bold=True)
    rows = [("감사", [3, 9]), ("⋮", None), ("환불", REFUND), ("환불했어요", [9])]
    for k, (t, ds) in enumerate(rows):
        y = 3.6 - k * 0.8
        if ds is None:
            label(ax, 1.4, y + 0.3, "⋮", fs=13, color=INK)
            continue
        on = step == 2 and t == "환불"
        cell(ax, 0.3, y, 2.2, 0.62, t, hot=on, fs=11.5)
        arrow(ax, (2.6, y + 0.31), (3.2, y + 0.31), lw=1.3, ms=10, color=RED if on else INK)
        for j, d in enumerate(ds):
            new = (step == 1 and d == 9) or on
            cell(ax, 3.3 + j * 0.65, y, 0.58, 0.62, d, hot=new, fs=11)
    if step == 1:
        label(ax, 7.6, 2.7, "낱말 칸에\n'환불했어요'가\n통째로 올라가요", fs=12, ha="left", color=RED)
    else:
        arrow(ax, (10.5, 5.35), (6.6, 1.55 + 0.31), color=RED, ms=14)
        label(ax, 8.0, 2.4, "환불 줄만 꺼내요", fs=12, ha="left", color=RED)
        label(ax, 5.0, 0.95, "← 글 9는 안 나와요", fs=12, ha="left", color=RED)
        moral(ax, 6.0, 0.3, "사전에 올라간 낱말과 똑같아야 찾아요")


# ── 넣은 글은 잠시 뒤에 ────────────────────────────────────────────
def segs(ax, step):
    box(ax, 0.3, 3.0, 2.8, 2.6, fc=NOTE)
    label(ax, 1.7, 5.15, "들어온 글을\n모으는 곳", fs=11.5, color=INK)
    new = {1: [1, 2, 3], 2: [4, 5], 3: []}[step]
    for k, d in enumerate(new):
        cell(ax, 0.55 + k * 0.85, 3.4, 0.75, 0.6, f"글{d}", hot=(step == 1), fs=10.5)
    segdocs = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    have = {1: 0, 2: 1, 3: 3}[step]
    for k in range(3):
        x = 3.8 + k * 2.75
        if k >= have:
            empty(ax, x, 3.0, 2.5, 2.6)
            label(ax, x + 1.25, 4.3, f"{k}~{k + 1}초에\n온 글", fs=10.5, color=GREY)
            continue
        on = step == 2 and k == 0
        box(ax, x, 3.0, 2.5, 2.6, fc=PINK if on else NOTE, ec=RED if on else INK)
        label(ax, x + 1.25, 5.1, f"세그먼트 {k + 1}", fs=12, bold=True, color=RED if on else "#222")
        for j, d in enumerate(segdocs[k]):
            cell(ax, x + 0.15 + j * 0.75, 3.6, 0.7, 0.6, f"글{d}", fs=10.5)
        label(ax, x + 1.25, 4.5, f"{k}~{k + 1}초에 온 글", fs=10.5, color=INK)
    if step == 1:
        label(ax, 1.7, 2.4, "아직 검색이\n안 돼요", fs=12, color=RED)
        label(ax, 8.0, 1.8, "1초 동안 들어온 글을 모아요", fs=12.5, color=INK)
    elif step == 2:
        arrow(ax, (3.15, 4.3), (3.75, 4.3), color=RED, ms=14)
        label(ax, 8.0, 1.8, "1초가 되면 모인 글로 작은 역색인을 만들어요", fs=12, color=RED)
        label(ax, 8.0, 1.15, "이제부터 글 1, 2, 3이 검색돼요", fs=12, color=INK)
    else:
        box(ax, 5.6, 0.95, 2.8, 0.75, fc=PINK, ec=RED)
        label(ax, 7.0, 1.32, "검색: 환불", fs=12, color=RED, bold=True)
        for k in range(3):
            arrow(ax, (7.0, 1.75), (3.8 + k * 2.75 + 1.25, 2.95), color=RED, lw=1.6, ms=12)
        moral(ax, 6.0, 0.35, "세그먼트를 모두 찾아보고 결과를 합쳐요")


# ── 심화: 지운 글 ──────────────────────────────────────────────────
def deleted(ax, step):
    label(ax, 0.3, 5.0, "환불 →", fs=12.5, ha="left", bold=True)
    cells(ax, 2.6, 4.6, REFUND, w=0.75, h=0.75, fs=12)
    label(ax, 7.0, 4.97, "목록은 그대로 둬요", fs=11.5, ha="left", color=INK)
    label(ax, 0.3, 3.0, "글 살아 있나", fs=12.5, ha="left", bold=True)
    for k, d in enumerate(REFUND):
        dead = step == 2 and d == 3
        cell(ax, 2.6 + k * 0.83, 2.6, 0.75, 0.75, "✗" if dead else "○", hot=dead, fs=12)
    if step == 1:
        label(ax, 7.0, 2.97, "글 3을 지워요", fs=12.5, ha="left", color=INK)
    else:
        label(ax, 7.0, 2.97, "글 3 칸에 ✗ 표시만 해요", fs=12.5, ha="left", color=RED)
        label(ax, 6.0, 1.4, "새로 고침 뒤 검색에는 1, 7, 12, 20만 나와요", fs=12, color=INK)
        moral(ax, 6.0, 0.45, "지운 글은 표시를 보고 걸러 내요")


def merge(ax, step):
    segdocs = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    for k, ds in enumerate(segdocs):
        y = 4.6 - k * 1.25
        box(ax, 0.3, y, 3.6, 1.0, fc=NOTE)
        label(ax, 0.55, y + 0.5, f"{k + 1}", fs=11, color=INK, ha="left")
        for j, d in enumerate(ds):
            dead = d == 3
            cell(ax, 0.95 + j * 0.95, y + 0.17, 0.85, 0.66, "✗" if dead else f"글{d}", dim=dead, fs=10.5)
    label(ax, 2.1, 5.95, "세그먼트 셋", fs=12, bold=True)
    if step == 1:
        label(ax, 7.6, 3.5, "세그먼트가 많으면\n찾아볼 곳이 늘어요", fs=12.5, ha="left", color=INK)
        return
    arrow(ax, (4.1, 3.4), (5.3, 3.4), lw=3, ms=22, color=RED)
    label(ax, 4.7, 3.9, "병합", fs=12, color=RED, bold=True)
    box(ax, 5.5, 2.4, 6.3, 2.0, fc=PINK, ec=RED)
    label(ax, 8.65, 4.0, "합친 세그먼트 1개", fs=12, color=RED, bold=True)
    for j, d in enumerate([1, 2, 4, 5, 6, 7, 8, 9]):
        cell(ax, 5.7 + j * 0.75, 2.75, 0.7, 0.66, f"글{d}", fs=10)
    label(ax, 8.65, 1.75, "지운 글 3은 옮기지 않아요", fs=12, color=RED)
    moral(ax, 6.0, 0.6, "병합할 때 지운 글의 번호와 공간이 치워져요")


# ── 정리: 처음 장면으로 돌아가기 ────────────────────────────────────
def back(ax, step):
    """scan과 같은 무대. 처음엔 데이터베이스가 다 읽었던 글을 이번엔 ES가 역색인으로 찾는다."""
    board(ax, hot=(1, 3) if step == 3 else (), dim=(2, 4, 5, 6) if step == 3 else ())
    if step == 1:
        arrow(ax, (0.3, ROW_Y[0]), (0.3, 0.75), color=GREY, ms=14)
        cylinder(ax, *CYL, "데이터베이스")
        bubble(ax, *SAY, "처음엔 1번 글부터\n백만 줄을 다 읽었어요", SAY_TAIL)
        return
    x, y, w, h = CYL
    cylinder(ax, *CYL, "ES (역색인)", ec=RED if step == 2 else INK, color=RED if step == 2 else "#222")
    cell(ax, x + 0.15, y + 0.35, 0.9, 0.5, "환불", hot=(step == 2), fs=10.5)
    cells(ax, x + 1.15, y + 0.35, [1, 3, "⋯"], w=0.42, h=0.5, gap=0.04, hot=(0, 1) if step == 2 else (), fs=10)
    if step == 2:
        bubble(ax, *SAY, "사전에서 환불 줄을 꺼내요\n1번과 3번이 달려 있어요", SAY_TAIL, hot=True)
    else:
        arrow(ax, (x - 0.05, y + 0.6), (6.8, ROW_Y[0]), color=RED, ms=14)
        arrow(ax, (x - 0.05, y + 0.6), (6.8, ROW_Y[2]), color=RED, ms=14)
        bubble(ax, *SAY, "1번과 3번 글만 열어요", SAY_TAIL, hot=True)
        moral(ax, 6.0, 0.2, "글이 백만 개여도 환불 줄 하나만 봐요")


# ── 전환: 빨라진 대신 치르는 값 ─────────────────────────────────────
def turn(ax, step):
    """돌아오는 장면과 같은 무대. 빨라진 결과를 보여 준 뒤 그 대가 세 가지로 넘어간다."""
    board(ax, hot=(1, 3) if step == 1 else (), dim=(2, 4, 5, 6) if step == 1 else (1, 2, 3, 4, 5, 6))
    x, y, w, h = CYL
    cylinder(ax, *CYL, "ES (역색인)")
    cell(ax, x + 0.15, y + 0.35, 0.9, 0.5, "환불", fs=10.5)
    cells(ax, x + 1.15, y + 0.35, [1, 3, "⋯"], w=0.42, h=0.5, gap=0.04, fs=10)
    if step == 1:
        bubble(ax, *SAY, "환불이 든 글을\n단번에 찾았어요", SAY_TAIL)
        return
    bubble(ax, 7.2, 0.25, 4.7, 2.45, "", SAY_TAIL, hot=True)
    label(ax, 9.55, 2.25, "대신 치르는 값이 있어요", fs=11.5, color=RED, bold=True)
    for k, t in enumerate(["① 미리 만드는 시간과 공간", "② 잘라 둔 낱말로만 찾기", "③ 넣은 글은 잠시 뒤에 검색"]):
        label(ax, 7.55, 1.7 - k * 0.5, t, fs=11, ha="left", color=RED)


# ── 정리: 낱말 카드 ────────────────────────────────────────────────
def cards():
    """이 편 본문에서 이름 붙인 말 여덟. 카드마다 본문 그림을 작게 다시 그리고 한 줄 뜻을 단다. 휴대폰 폭에 맞게 두 장씩."""
    fig, ax = canvas(6.4, 10.6, 9.8, 16.4)
    W, H = 4.6, 3.8

    def card(col, row, name, line):
        x, y = 0.2 + col * 4.9, 12.4 - row * 4.05
        box(ax, x, y, W, H, fc="white")
        label(ax, x + 0.25, y + H - 0.4, name, fs=12.5, ha="left", bold=True)
        label(ax, x + W / 2, y + 0.45, line, fs=10, color=INK)
        return x, y

    x, y = card(0, 0, "전체 훑기", "처음부터 끝까지 다 읽기")
    for k in range(4):
        cell(ax, x + 1.0, y + 2.65 - k * 0.42, 2.6, 0.38, "", fs=9)
    arrow(ax, (x + 0.7, y + 2.95), (x + 0.7, y + 1.0), color=RED, ms=12)
    x, y = card(1, 0, "색인", "찾으려고 미리 만들어 둔 목록")
    for k, (t, n) in enumerate([("광합성", "34, 112"), ("나무", "8"), ("뿌리", "21, 40")]):
        on = k == 0
        label(ax, x + 0.6, y + 2.75 - k * 0.5, t, fs=10.5, ha="left", color=RED if on else "#222", bold=on)
        label(ax, x + 3.9, y + 2.75 - k * 0.5, n, fs=10.5, ha="right", color=RED if on else "#222", bold=on)
    x, y = card(0, 1, "용어", "잘라 낸 낱말 하나")
    label(ax, x + W / 2, y + 2.75, "주문 환불 요청", fs=10.5, color=INK)
    arrow(ax, (x + W / 2, y + 2.5), (x + W / 2, y + 2.05), lw=1.3, ms=10)
    cells(ax, x + 0.85, y + 1.35, ["주문", "환불", "요청"], w=0.9, h=0.5, hot=(1,), fs=10)
    x, y = card(1, 1, "역색인", "낱말에서 글 번호로 가는 목록")
    for k, (t, ds) in enumerate([("주문", [1, 2, "⋯"]), ("환불", [1, 3, "⋯"])]):
        yy = y + 2.45 - k * 0.6
        cell(ax, x + 0.4, yy, 1.1, 0.48, t, hot=(t == "환불"), fs=10.5)
        arrow(ax, (x + 1.6, yy + 0.24), (x + 2.05, yy + 0.24), lw=1.2, ms=9)
        cells(ax, x + 2.15, yy, ds, w=0.5, h=0.48, hot=(0, 1) if t == "환불" else (), fs=10)
    x, y = card(0, 2, "용어 사전", "가나다순으로 늘어놓은 낱말 칸")
    for k, t in enumerate(["⋯"] + TERMS[3:]):
        cell(ax, x + 0.3 + k * 0.82, y + 1.9, 0.78, 0.55, t, hot=(t == "환불"), fs=10)
    x, y = card(1, 2, "포스팅 목록", "낱말 하나에 달린 글 번호 줄 (번호순)")
    label(ax, x + 0.3, y + 2.15, "환불", fs=10.5, ha="left", color=RED, bold=True)
    cells(ax, x + 1.15, y + 1.9, REFUND, w=0.6, h=0.48, hot=range(5), fs=10)
    x, y = card(0, 3, "세그먼트", "1초쯤 모은 글로 만든 작은 역색인")
    for k in range(3):
        box(ax, x + 0.4 + k * 1.3, y + 1.6, 1.1, 1.2, fc=NOTE, lw=1.4)
        label(ax, x + 0.95 + k * 1.3, y + 2.2, f"글{3 * k + 1}~{3 * k + 3}", fs=9.5, color=INK)
    x, y = card(1, 3, "새로 고침", "모은 글로 세그먼트를 만드는 일")
    box(ax, x + 0.4, y + 1.6, 1.4, 1.2, fc=NOTE, lw=1.4)
    label(ax, x + 1.1, y + 2.2, "모은 글", fs=9.5, color=INK)
    arrow(ax, (x + 1.9, y + 2.2), (x + 2.6, y + 2.2), color=RED, ms=12)
    box(ax, x + 2.7, y + 1.6, 1.5, 1.2, fc=PINK, ec=RED, lw=1.4)
    label(ax, x + 3.45, y + 2.2, "세그먼트", fs=9.5, color=RED)
    save(fig, OUT, "es01-cards.svg")


DOCS = {1: ["주문", "환불", "요청"], 2: ["주문", "배송", "언제"], 3: ["환불", "완료", "감사"]}


def speed():
    """실측 표를 막대로: 200 ms와 0.01 ms."""
    fig, ax = canvas(10, 2.6, 15, 3.4)
    label(ax, 0.3, 2.55, "전체 훑기", fs=11.5, ha="left")
    ax.add_patch(__import__("matplotlib").patches.Rectangle((4.0, 2.25), 9.5, 0.6, fc=GREY, ec=INK))
    label(ax, 13.6, 2.55, "약 200 ms\n(0.2초)", fs=11, ha="left")
    label(ax, 0.3, 1.25, "역색인에서 찾기", fs=11.5, ha="left", color=RED, bold=True)
    ax.add_patch(__import__("matplotlib").patches.Rectangle((4.0, 0.95), 0.03, 0.6, fc=RED, ec=RED))
    label(ax, 4.2, 1.25, "약 0.01 ms  (막대가 안 보일 만큼 짧아요)", fs=11, ha="left", color=RED)
    save(fig, OUT, "es01-speed.svg")


def cost():
    """미리 만들기 1초 = 하나씩 검색 다섯 번. 그 뒤 검색은 거의 공짜."""
    fig, ax = canvas(10, 3.4, 15, 4.6)
    label(ax, 0.3, 3.9, "역색인 없이", fs=12, ha="left", bold=True)
    for k in range(5):
        cell(ax, 3.0 + k * 1.95, 3.5, 1.85, 0.75, f"검색 {k + 1}", fc=LIGHT, fs=11)
    label(ax, 13.0, 3.87, "…검색할 때마다\n0.2초씩", fs=10, ha="left", color=INK)
    label(ax, 0.3, 1.9, "역색인 있으면", fs=12, ha="left", bold=True, color=RED)
    cell(ax, 3.0, 1.5, 9.7, 0.75, "처음 한 번 만들기 (약 1초)", fc=PINK, fs=11)
    for k in range(6):
        ax.plot([12.85 + k * 0.28] * 2, [1.5, 2.25], color=RED, lw=2)
    label(ax, 13.0, 1.05, "그다음 검색은\n거의 0초", fs=10, ha="left", color=RED)
    label(ax, 7.8, 0.4, "이 실험에서는 검색을 다섯 번 넘게 하면 미리 만든 쪽이 이득이었어요", fs=11, color=INK)
    save(fig, OUT, "es01-cost.svg")


def decide():
    """언제 역색인을 만들까: 자주 찾나 → 글 중간 낱말로 찾나."""
    fig, ax = canvas(10, 4.2, 15, 6.0)
    box(ax, 0.3, 4.4, 4.4, 1.2, fc=NOTE)
    label(ax, 2.5, 5.0, "자주 찾나요?", fs=12, bold=True)
    box(ax, 5.6, 4.4, 4.4, 1.2, fc=NOTE)
    label(ax, 7.8, 5.0, "글 중간에 든\n낱말로 찾나요?", fs=11.5, bold=True)
    box(ax, 10.9, 4.4, 3.8, 1.2, fc=PINK, ec=RED)
    label(ax, 12.8, 5.0, "역색인\n(ES)", fs=12, color=RED, bold=True)
    arrow(ax, (4.8, 5.0), (5.5, 5.0)); label(ax, 5.15, 5.45, "예", fs=10, color=INK)
    arrow(ax, (10.1, 5.0), (10.8, 5.0), color=RED); label(ax, 10.45, 5.45, "예", fs=10, color=RED)
    arrow(ax, (2.5, 4.3), (2.5, 2.9)); label(ax, 2.85, 3.6, "아니요", fs=10, color=INK, ha="left")
    arrow(ax, (7.8, 4.3), (7.8, 2.9)); label(ax, 8.15, 3.6, "아니요", fs=10, color=INK, ha="left")
    box(ax, 0.3, 0.6, 4.4, 2.2, fc=LIGHT, ec=GREY)
    label(ax, 2.5, 1.7, "그때그때 전체 훑기\n예: 몇 년 치 가계부에서\n가끔 가게 이름 찾기", fs=10.5)
    box(ax, 5.6, 0.6, 4.4, 2.2, fc=LIGHT, ec=GREY)
    label(ax, 7.8, 1.7, "데이터베이스 인덱스\n예: '청바'로 시작하는\n상품 이름 찾기", fs=10.5)
    save(fig, OUT, "es01-decide.svg")


def scale():
    """글 수가 늘 때 걸음 수: 하나씩 보기는 글 수만큼, 사전 찾기는 낱말 종류 5,000개에서 이진 탐색 13걸음."""
    sizes = ["글 10만", "글 20만", "글 40만"]
    scan = [100_000, 200_000, 400_000]
    fig, ax = canvas(10, 3.8, 15, 5.2)
    label(ax, 0.3, 4.85, "낱말 하나 찾는 걸음 수", fs=12, ha="left", bold=True)
    for k, (name, n) in enumerate(zip(sizes, scan)):
        y = 3.8 - k * 1.25
        label(ax, 0.3, y + 0.25, name, fs=11, ha="left")
        w = 9.0 * n / scan[-1]
        ax.add_patch(__import__("matplotlib").patches.Rectangle((2.2, y + 0.05), w, 0.4, fc=GREY, ec=INK))
        label(ax, 2.3 + w, y + 0.25, f"전체 훑기: {n:,}번", fs=10, ha="left")
        ax.add_patch(__import__("matplotlib").patches.Rectangle((2.2, y - 0.45), 0.08, 0.4, fc=RED, ec=RED))
        label(ax, 2.45, y - 0.25, "사전에서 찾기: 13번", fs=10, ha="left", color=RED)
    label(ax, 7.5, 0.25, "낱말 종류가 5,000개로 같으면 글이 늘어도 사전에서 찾는 걸음은 그대로예요", fs=10.5, color=INK)
    save(fig, OUT, "es01-scale.svg")


def phrase():
    """심화: 낱말 위치가 있어야 '환불 요청'이 붙어 있는지 안다."""
    fig, ax = canvas(10, 3.0, 15, 4.2)
    label(ax, 0.3, 3.7, "글 1", fs=12, ha="left", bold=True)
    cells(ax, 1.3, 3.2, ["주문", "환불", "요청"], w=1.4, h=0.8, hot=(1, 2))
    for k in range(3):
        label(ax, 1.3 + k * 1.48 + 0.7, 2.9, f"위치 {k}", fs=9.5, color=INK)
    label(ax, 0.3, 1.75, "역색인", fs=12, ha="left", bold=True)
    label(ax, 1.3, 1.75, "환불 → 글 1 (위치 1)     요청 → 글 1 (위치 2)", fs=11, ha="left", color=RED)
    box(ax, 0.3, 0.2, 14.4, 0.9, fc=NOTE)
    label(ax, 7.5, 0.65, "위치 1 다음이 위치 2라서 \"환불 요청\"이 붙어 있다는 걸 알아요. 위치를 안 적어 두면 알 수 없어요.", fs=10.5)
    save(fig, OUT, "es01-phrase.svg")


def heap():
    """심화: 7.7부터 안내판은 힙 밖. 디스크 파일에서 필요한 부분만 운영체제 메모리로."""
    fig, ax = canvas(10, 3.4, 15, 4.6)
    box(ax, 0.3, 1.3, 4.0, 2.6, fc=NOTE)
    label(ax, 2.3, 3.4, "ES 전용 메모리", fs=11.5, bold=True)
    label(ax, 2.3, 2.9, "(자바 힙)", fs=10.5, color=INK)
    label(ax, 2.3, 2.1, "크기를 미리\n정해 둬요", fs=10, color=INK)
    box(ax, 5.3, 1.3, 4.2, 2.6, fc=PINK, ec=RED)
    label(ax, 7.4, 3.4, "운영체제가 쓰는", fs=11.5, bold=True, color=RED)
    label(ax, 7.4, 2.9, "남는 메모리", fs=11.5, bold=True, color=RED)
    label(ax, 7.4, 2.1, "안내판 중\n필요한 부분", fs=10, color=RED)
    box(ax, 10.6, 1.3, 4.1, 2.6, fc=PAPER)
    label(ax, 12.65, 3.4, "디스크", fs=11.5, bold=True)
    label(ax, 12.65, 2.4, "안내판 파일", fs=10.5)
    arrow(ax, (10.5, 2.3), (9.6, 2.3), color=RED)
    label(ax, 10.05, 1.0, "필요한 부분만 읽어 와요", fs=9.5, color=RED)
    label(ax, 7.5, 0.35, "ES 7.7부터는 안내판이 힙 밖에 있어서 낱말이 늘어도 힙은 그대로예요", fs=10.5, color=INK)
    save(fig, OUT, "es01-heap.svg")


if __name__ == "__main__":
    S, L = (7.2, 3.8), (12, 6.6)
    stage(scan, 3, OUT, "es01-scan", S, L)
    stage(prefix, 3, OUT, "es01-prefix", S, L)
    stage(forward, 2, OUT, "es01-forward", S, L)
    stage(flip, 3, OUT, "es01-flip", S, L)
    stage(lookup, 4, OUT, "es01-lookup", S, L)
    speed(); scale()
    stage(blocks, 2, OUT, "es01-blocks", S, L)
    heap()
    stage(fingers, 4, OUT, "es01-fingers", S, L)
    phrase(); cost()
    stage(miss, 2, OUT, "es01-miss", S, L)
    stage(segs, 3, OUT, "es01-segs", S, L)
    stage(deleted, 2, OUT, "es01-deleted", S, L)
    stage(merge, 2, OUT, "es01-merge", S, L)
    decide()
    stage(turn, 2, OUT, "es01-turn", S, L)
    stage(back, 3, OUT, "es01-back", S, L)
    cards()
