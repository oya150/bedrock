"""Elasticsearch 5편 그림 만들기. 실행: python lab/fig_es05.py  → docs/elasticsearch/img/05/*.svg

본문 절은 장면 띠로 그린다: 같은 무대를 여러 장 그리고 장마다 바뀐 곳만 빨강으로 칠한다.
예시는 쇼핑몰 문의 게시판의 환불 문의 글 300개를 편 끝까지 잇는다(.claude/writing/work/cal/units-es05.md).
세그먼트 _0 = 글 1~100, _1 = 글 101~200, _2 = 글 201~300, 지운 뒤 생긴 _3 = 빈 문서 100.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "es"))
from figkit import (GREY, INK, LIGHT, NOTE, PAPER, PINK, RED, arrow, board, box, bubble,  # noqa: E402
                    canvas, cell, cells, cylinder, label, moral, outdir, save, stage)
from matplotlib.patches import Rectangle  # noqa: E402

OUT = outdir("05")
POSTS = [(1, "환불 문의"), (2, "환불 언제 돼요"), None, (101, "환불 문의"), None, (300, "환불 요청")]
CYL = (8.0, 3.0, 3.6, 1.7)
SAY = (7.2, 0.55, 4.5, 1.3)
TAIL = (9.8, 2.75)
SEGX = [0.2, 3.05, 5.9, 8.75]
SEGW = 2.7


def empty(ax, x, y, w, h, s="", fs=10):
    ax.add_patch(Rectangle((x, y), w, h, fc="white", ec=GREY, lw=1.0, ls="--"))
    if s:
        label(ax, x + w / 2, y + h / 2, s, fs=fs, color=GREY)


def strike(ax, x, y, w, h):
    ax.plot([x, x + w], [y, y + h], color=GREY, lw=1.4)


def seg(ax, x, y, w, name, items, dead=(), hot=False, hotcell=(), h=1.5, fs=10):
    """세그먼트 상자. items=칸 글자, dead=지운 문서 칸(회색 줄), hot=상자 빨강."""
    box(ax, x, y, w, h, fc=PINK if hot else NOTE, ec=RED if hot else INK)
    label(ax, x + 0.15, y + h - 0.3, name, fs=10, ha="left", bold=True, color=RED if hot else "#222")
    n = len(items)
    cw = (w - 0.3 - (n - 1) * 0.1) / n
    for k, t in enumerate(items):
        cx, cy = x + 0.15 + k * (cw + 0.1), y + 0.15
        cell(ax, cx, cy, cw, 0.7, t, hot=k in hotcell, dim=k in dead, fs=fs)
        if k in dead:
            strike(ax, cx, cy, cw, 0.7)


def shard4(ax, y=3.9, gone=False):
    """실험의 세그먼트 넷: _0(지운 글), _1, _2, _3(빈 문서)."""
    rows = [("_0", "글 1~100", True), ("_1", "글 101~200", False), ("_2", "글 201~300", False), ("_3", "빈 문서 100", True)]
    for x, (n, t, dead) in zip(SEGX, rows):
        if gone:
            empty(ax, x, y, SEGW, 1.5, f"{n} (지움)")
        else:
            seg(ax, x, y, SEGW, f"세그먼트 {n}", [t], dead=(0,) if dead else ())


def disk(ax, kb, dele, hot=False):
    x, y, w, h = CYL
    cylinder(ax, *CYL, "ES")
    c = RED if hot else "#222"
    label(ax, x + w / 2, y + 1.15, f"디스크 {kb}", fs=11.5, color=c, bold=hot)
    label(ax, x + w / 2, y + 0.45, f"지운 문서 {dele}", fs=11, color=c, bold=hot)


def footer(ax, s, hot=False):
    label(ax, 3.8, 0.88, s, fs=11.5, color=RED if hot else INK, bold=hot)


# ── 여는 장면: 지웠는데 디스크가 늘었어요 ──────────────────────────
def opening(ax, step):
    if step == 1:
        board(ax, POSTS, footer=None)
        footer(ax, "글 300개")
        disk(ax, "20.7 kb", 0)
        bubble(ax, *SAY, "환불 문의 글 300개를\n넣었어요", TAIL)
    elif step == 2:
        board(ax, POSTS, miss=(1, 2), footer=None)
        footer(ax, "글 200개", hot=True)
        disk(ax, "20.7 kb", 0)
        bubble(ax, *SAY, "오래된 1~100번 글을\n지웠어요", TAIL, hot=True)
    else:
        board(ax, POSTS, dim=(1, 2), footer=None)
        footer(ax, "글 200개")
        disk(ax, "25.9 kb", 200, hot=True)
        bubble(ax, *SAY, "디스크가 25.9 kb로\n늘었어요", TAIL, hot=True)
        moral(ax, 4.0, 0.2, "지웠는데 오히려 커졌어요")


# ── 지우기는 표시만 해요 ───────────────────────────────────────────
def mark(ax, step):
    label(ax, 0.2, 4.92, "글", fs=11, ha="left", color=INK)
    label(ax, 0.2, 3.87, "살아\n있나", fs=10.5, ha="left", color=INK)
    for x, name, nums in ((1.4, "세그먼트 _0", ["1", "2", "⋯", "100"]), (6.6, "세그먼트 _1", ["101", "102", "⋯", "200"])):
        box(ax, x, 3.35, 5.0, 2.75, fc=NOTE)
        label(ax, x + 0.15, 5.8, name, fs=10.5, ha="left", bold=True)
        gone = step > 1 and x < 2
        for k, t in enumerate(nums):
            cx = x + 0.2 + k * 1.17
            cell(ax, cx, 4.6, 1.07, 0.65, t, dim=gone, fs=10.5)
            if gone:
                strike(ax, cx, 4.6, 1.07, 0.65)
            alive = "⋯" if t == "⋯" else ("0" if gone else "1")
            cell(ax, cx, 3.55, 1.07, 0.65, alive, hot=(gone and step == 2), fs=11)
    if step == 1:
        label(ax, 6.0, 2.3, "세그먼트는 한 번 만들면 고치지 않아요 (4편)", fs=11, color=INK)
        label(ax, 6.0, 1.55, "_2 (글 201~300)도 같은 모양이에요", fs=10.5, color=INK)
    elif step == 2:
        label(ax, 6.0, 2.3, "1~100번을 지우면 표에만 0을 적어요", fs=11.5, color=RED, bold=True)
        label(ax, 6.0, 1.55, "글과 역색인은 그대로 남아요", fs=10.5, color=INK)
    else:
        ax.add_patch(Rectangle((0.3, 1.85), 1.6, 0.6, fc="white", ec=INK, lw=1.2))
        label(ax, 1.2, 2.15, "환불", fs=11)
        label(ax, 2.1, 2.15, "→", fs=12, color=INK)
        nums = ["1", "⋯", "100", "101", "⋯", "300"]
        cells(ax, 2.5, 1.85, nums, w=0.85, h=0.6, gap=0.08, dim=(0, 1, 2), hot=(3, 4, 5), fs=10)
        label(ax, 8.2, 2.15, "200건", fs=12, color=RED, bold=True, ha="left")
        label(ax, 6.0, 1.15, "'환불'이 든 문서 수는 300 그대로", fs=10.5, color=INK)
        moral(ax, 6.0, 0.35, "지운 글은 건너뛰지만 자리와 통계는 그대로예요")


# ── 지우기도 문서를 하나 남겨요 ────────────────────────────────────
def tomb(ax, step):
    label(ax, 11.6, 6.2, "지운 문서 수 200", fs=11, ha="right", bold=True)
    rows = [("_0", "글 1~100", True), ("_1", "글 101~200", False), ("_2", "글 201~300", False)]
    for x, (n, t, dead) in zip(SEGX, rows):
        seg(ax, x, 3.9, SEGW, f"세그먼트 {n}", [t], dead=(0,) if dead else ())
    label(ax, SEGX[0] + SEGW / 2, 3.55, "지운 글 100", fs=10, color=INK)
    if step == 1:
        empty(ax, SEGX[3], 3.9, SEGW, 1.5, "?", fs=14)
        label(ax, 6.0, 2.2, "지운 글은 100개인데 지운 문서 수는 200이에요", fs=11, color=INK)
        return
    seg(ax, SEGX[3], 3.9, SEGW, "세그먼트 _3", ["빈 문서 100"], dead=(0,), hot=(step == 2))
    label(ax, SEGX[3] + SEGW / 2, 3.55, "1번 지움 ⋯ 100번 지움", fs=10, color=RED if step == 2 else INK)
    if step == 2:
        label(ax, 6.0, 2.2, "지운 글 100 + 빈 문서 100 = 200", fs=12, color=RED, bold=True)
        label(ax, 6.0, 1.45, "빈 문서는 처음부터 지운 상태로 들어가요", fs=10.5, color=INK)
    else:
        box(ax, 8.6, 1.3, 3.0, 0.9, fc=PINK, ec=RED)
        label(ax, 10.1, 1.75, "복제본 (다른 노드)", fs=10.5, color=RED)
        arrow(ax, (10.1, 3.3), (10.1, 2.3), color=RED, ms=14)
        label(ax, 8.3, 2.55, "끊겼다 돌아온 복제본에\n'1번 지움'을 다시 보내요", fs=10.5, color=RED, ha="right")
        moral(ax, 5.0, 0.4, "빈 문서는 복제본에 다시 보낼 지우기 기록이에요")


# ── 고치기는 지우고 새로 넣기 ──────────────────────────────────────
def update(ax, step):
    label(ax, 0.3, 6.15, "101번 글 고치기:  환불 문의 → 환불 문의 수정", fs=11, ha="left", color=INK)
    box(ax, 0.3, 3.3, 5.4, 2.0, fc=NOTE)
    label(ax, 0.45, 5.0, "세그먼트 _1", fs=10.5, ha="left", bold=True)
    gone = step > 1
    cell(ax, 0.5, 3.6, 2.7, 0.8, "101 환불 문의", dim=gone, fs=10.5)
    if gone:
        strike(ax, 0.5, 3.6, 2.7, 0.8)
    cell(ax, 3.35, 3.6, 2.15, 0.8, "102 ⋯ 200", fs=10.5)
    if step == 2:
        label(ax, 1.85, 2.85, "삭제 표시 (지운 문서 1)", fs=11, color=RED, bold=True)
    elif step == 3:
        label(ax, 1.85, 2.85, "삭제 표시 (지운 문서 1)", fs=10.5, color=INK)
    if step < 3:
        empty(ax, 6.4, 3.3, 5.2, 2.0, "새 세그먼트", fs=10.5)
        return
    box(ax, 6.4, 3.3, 5.2, 2.0, fc=PINK, ec=RED)
    label(ax, 6.55, 5.0, "새 세그먼트", fs=10.5, ha="left", bold=True, color=RED)
    cell(ax, 6.7, 3.6, 4.6, 0.8, "101 환불 문의 수정", hot=True, fs=10.5)
    label(ax, 9.0, 2.85, "고친 글 전체를 새 문서로", fs=10.5, color=RED)
    moral(ax, 6.0, 1.4, "고치기 = 옛 글에 삭제 표시 + 고친 글을 새로 넣기")


# ── 병합 ───────────────────────────────────────────────────────────
NEW = (2.2, 1.0, 7.6, 1.6)


def merged(ax, hot=False):
    seg(ax, NEW[0], NEW[1], NEW[2], "새 세그먼트", ["글 101~200", "글 201~300"], hot=hot, h=NEW[3])


def merge(ax, step):
    if step == 1:
        shard4(ax)
        label(ax, 11.6, 6.2, "세그먼트 4개 · 지운 문서 200", fs=11, ha="right", bold=True)
        empty(ax, *NEW, "새 세그먼트", fs=10.5)
        return
    if step == 2:
        shard4(ax)
        label(ax, 11.6, 6.2, "세그먼트 4개 · 지운 문서 200", fs=11, ha="right", bold=True)
        for x in (SEGX[1], SEGX[2]):
            arrow(ax, (x + SEGW / 2, 3.85), (x + SEGW / 2 + (0.6 if x < 5 else -0.6), 2.65), color=RED, ms=14)
        for x in (SEGX[0], SEGX[3]):
            label(ax, x + SEGW / 2, 3.35, "✗ 옮기지 않아요", fs=10.5, color=RED, bold=True)
        merged(ax, hot=True)
        return
    shard4(ax, gone=True)
    label(ax, 11.6, 6.2, "세그먼트 4개 → 1개 · 지운 문서 0", fs=11, ha="right", bold=True, color=RED)
    merged(ax)
    moral(ax, 6.0, 0.35, "병합할 때 지운 문서가 실제로 빠져요")


# ── 전환: 병합도 공짜는 아니에요 ───────────────────────────────────
def turn(ax, step):
    seg(ax, 0.3, 4.3, 5.8, "세그먼트 (병합 뒤)", ["글 101~200", "글 201~300"])
    label(ax, 3.2, 3.85, "지운 문서 0 · 세그먼트 4개 → 1개", fs=10.5, color=INK)
    cylinder(ax, 8.2, 3.9, 3.0, 1.4, "ES")
    if step == 1:
        bubble(ax, 3.0, 1.0, 6.4, 1.4, "지운 문서를 치우고\n세그먼트 수도 줄였어요", (9.7, 3.6))
    else:
        bubble(ax, 0.5, 0.15, 11.1, 3.1, "", (9.7, 3.6), hot=True)
        label(ax, 6.0, 2.8, "그런데 병합에는 따라오는 것이 있어요", fs=12, color=RED, bold=True)
        for k, t in enumerate(["① 다 읽고 다시 쓰느라 디스크를 잠시 더 써요", "② 그래서 큰 세그먼트는 늦게 합쳐요",
                               "③ 복제본에 보낼 기록은 합쳐도 남겨요"]):
            label(ax, 1.1, 2.15 - k * 0.6, t, fs=11, ha="left", color=RED)


# ── 첫째 값: 합치는 동안 디스크를 더 써요 ──────────────────────────
GX, GW = 9.8, 1.6


def cost(ax, step):
    label(ax, 0.3, 6.2, "병합 중" if step == 1 else "병합 뒤", fs=12, ha="left", bold=True)
    for k, (n, t, dead) in enumerate([("_0", "1~100", True), ("_1", "101~200", False), ("_2", "201~300", False),
                                      ("_3", "빈 문서", True)]):
        x = 0.3 + k * 2.05
        if step == 1:
            seg(ax, x, 4.0, 1.9, n, [t], dead=(0,) if dead else (), fs=9.5, h=1.4)
        else:
            empty(ax, x, 4.0, 1.9, 1.4, f"{n} (지움)", fs=9.5)
    seg(ax, 1.3, 1.6, 6.0, "새 세그먼트" + (" (만드는 중)" if step == 1 else ""), ["글 101~200", "글 201~300"],
        hot=(step == 1), h=1.4)
    if step == 1:
        arrow(ax, (4.3, 3.95), (4.3, 3.05), color=RED, ms=14)
        label(ax, 4.6, 3.5, "다 읽고 새로 써요", fs=10.5, color=RED, ha="left")
    label(ax, GX + GW / 2, 5.6, "디스크", fs=11, bold=True)
    ax.add_patch(Rectangle((GX, 1.0), GW, 4.2, fc="white", ec=INK, lw=1.4))
    if step == 1:
        ax.add_patch(Rectangle((GX, 1.0), GW, 2.0, fc=LIGHT, ec=INK, lw=1.0))
        label(ax, GX + GW / 2, 2.0, "옛 4개", fs=10, color=INK)
        ax.add_patch(Rectangle((GX, 3.0), GW, 1.2, fc=PINK, ec=RED, lw=1.6))
        label(ax, GX + GW / 2, 3.6, "새 1개", fs=10, color=RED, bold=True)
    else:
        ax.add_patch(Rectangle((GX, 1.0), GW, 1.2, fc=PINK, ec=RED, lw=1.6))
        label(ax, GX + GW / 2, 1.6, "새 1개", fs=10, color=RED, bold=True)
        moral(ax, 4.6, 0.6, "합치는 동안만 디스크를 더 써요")


# ── 둘째 값: 큰 세그먼트는 늦게 합쳐요 ─────────────────────────────
BIG_DEAD = {2, 7, 11, 13, 18}


def cap(ax, step):
    box(ax, 0.3, 1.9, 5.6, 3.2, fc=NOTE)
    label(ax, 0.45, 4.8, "큰 세그먼트", fs=10.5, ha="left", bold=True)
    for i in range(20):
        cx, cy = 0.55 + (i % 5) * 1.05, 3.9 - (i // 5) * 0.6
        if i in BIG_DEAD:
            cell(ax, cx, cy, 0.9, 0.45, "", dim=True)
            strike(ax, cx, cy, 0.9, 0.45)
            if step == 2:
                ax.add_patch(Rectangle((cx, cy), 0.9, 0.45, fill=False, ec=RED, lw=2.0))
        else:
            cell(ax, cx, cy, 0.9, 0.45, "", fc="white")
    label(ax, 3.1, 1.5, "상한 5 GB에 가까워요", fs=10.5, color=INK)
    hot1 = step == 1
    label(ax, 9.0, 6.15, "작은 세그먼트들", fs=10.5, color=INK)
    for k in range(3):
        box(ax, 7.0 + k * 1.45, 4.85, 1.1, 0.8, fc=NOTE)
        arrow(ax, (7.55 + k * 1.45, 4.75), (9.0, 3.9), color=RED if hot1 else GREY, ms=12, lw=1.5)
    box(ax, 7.6, 2.9, 2.8, 0.9, fc=PINK if hot1 else NOTE, ec=RED if hot1 else INK)
    label(ax, 9.0, 3.35, "합친 세그먼트", fs=10.5, color=RED if hot1 else "#222")
    if hot1:
        label(ax, 9.0, 2.4, "비슷한 크기끼리 합쳐요", fs=11, color=RED, bold=True)
    else:
        label(ax, 6.0, 0.95, "지운 문서가 꽤 쌓일 때까지 큰 세그먼트는 그대로 둬요", fs=10.5, color=INK)
        moral(ax, 6.0, 0.3, "큰 인덱스에는 지운 문서가 늘 조금 남아요")


# ── 셋째 값: 복제본에 보낼 기록은 합쳐도 남겨요 ────────────────────
PHASES = ["지운 직후", "바로 강제 병합", "70초 뒤 다시 병합"]


def timeline(ax, step, phases):
    for k, t in enumerate(phases):
        x = 0.3 + k * 3.9
        on = k + 1 == step
        label(ax, x + 1.6, 6.1, t, fs=11, color=RED if on else INK, bold=on)
        if k < len(phases) - 1:
            arrow(ax, (x + 3.25, 6.1), (x + 3.85, 6.1), color=GREY, ms=10, lw=1.2)


def retain(ax, step):
    timeline(ax, step, PHASES)
    if step == 1:
        shard4(ax, y=3.3)
        label(ax, 6.0, 2.2, "25.9 kb · 지운 문서 200", fs=12, color=INK)
        return
    if step == 2:
        seg(ax, 0.3, 3.3, 11.3, "세그먼트 (하나로 합침)", ["글 1~100", "글 101~200", "글 201~300", "빈 문서 100"],
            dead=(0, 3), hot=True)
        label(ax, 6.0, 2.2, "17.0 kb · 지운 문서 200 그대로", fs=12, color=RED, bold=True)
        return
    seg(ax, 0.3, 3.3, 11.3, "세그먼트 (다시 합침)", ["글 101~200", "글 201~300"], hot=True)
    label(ax, 6.0, 2.2, "10.1 kb · 지운 문서 0", fs=12, color=RED, bold=True)
    moral(ax, 6.0, 0.9, "기록을 붙들 일이 끝나야 지운 문서가 빠져요")


def recover(ax, step):
    top, bot = step == 1, step == 2
    label(ax, 0.3, 6.15, "잠깐 끊겼다 돌아온 복제본", fs=11, ha="left", bold=True, color=RED if top else "#222")
    box(ax, 0.3, 4.75, 2.0, 0.9, fc=NOTE)
    label(ax, 1.3, 5.2, "주 샤드", fs=10.5)
    arrow(ax, (2.45, 5.2), (8.55, 5.2), color=RED if top else GREY, ms=14)
    label(ax, 5.5, 5.5, "빠진 작업만 다시 보내요", fs=10.5, color=RED if top else INK)
    box(ax, 8.7, 4.75, 2.8, 0.9, fc=PINK if top else NOTE, ec=RED if top else INK)
    label(ax, 10.1, 5.2, "복제본", fs=10.5, color=RED if top else "#222")
    label(ax, 6.0, 4.3, "그 작업 기록이 있어야 해요 (보존 표시가 붙들어요)", fs=10.5, color=RED if top else INK)
    label(ax, 0.3, 3.45, "새로 붙는 복제본", fs=11, ha="left", bold=True, color=RED if bot else "#222")
    if top:
        empty(ax, 0.3, 1.5, 11.2, 1.5)
        return
    box(ax, 0.3, 1.6, 2.0, 1.3, fc=NOTE)
    label(ax, 1.3, 2.25, "주 샤드", fs=10.5)
    arrow(ax, (2.45, 2.55), (8.55, 2.55), color=RED, ms=13)
    label(ax, 5.5, 2.8, "① 커밋 하나의 파일을 복사해 줘요", fs=10, color=RED)
    arrow(ax, (2.45, 1.85), (8.55, 1.85), color=RED, ms=13)
    label(ax, 5.5, 2.1, "② 커밋 뒤의 작업을 따로 보내요", fs=10, color=RED)
    box(ax, 8.7, 1.6, 2.8, 1.3, fc=PINK, ec=RED)
    label(ax, 10.1, 2.25, "새 복제본", fs=10.5, color=RED)
    moral(ax, 6.0, 0.7, "커밋 뒤의 작업 기록도 남겨 둬요")


# ── 심화: 보존 표시와 시퀀스 번호 ──────────────────────────────────
GROUPS = [("1~100 넣기", "지운 원래 글"), ("101~200 넣기", ""), ("201~300 넣기", ""), ("301~400 지우기", "빈 문서")]


def flag(ax, xf, hot=True):
    c = RED if hot else INK
    ax.plot([xf, xf], [3.3, 5.0], color=c, lw=2.5)
    ax.add_patch(Rectangle((xf - 0.6, 4.6), 0.6, 0.4, fc=c, ec=c))
    label(ax, xf, 5.3, "보존 표시", fs=10.5, color=c, ha="right", bold=True)


GX0, GSTEP, GWID = 0.3, 2.7, 2.55
CX = GX0 + 3 * GSTEP + GWID + 0.2


def lease(ax, step):
    label(ax, 11.6, 6.15, "시퀀스 번호 →", fs=11, ha="right", bold=True)
    for k, (t, sub) in enumerate(GROUPS):
        x = GX0 + k * GSTEP
        dropped = (k == 0 and step >= 2) or (k == 3 and step == 3)
        if dropped:
            empty(ax, x, 3.3, GWID, 1.2, "빠짐", fs=11)
            ax.add_patch(Rectangle((x, 3.3), GWID, 1.2, fill=False, ec=RED, lw=1.6, ls="--"))
        else:
            cell(ax, x, 3.3, GWID, 1.2, t + ("\n(" + sub + ")" if sub else ""), dim=bool(sub), fs=9.5)
    xf = GX0 + 3 * GSTEP - 0.075 if step < 3 else 11.55
    flag(ax, xf, hot=(step != 2))
    g4 = GX0 + 3 * GSTEP + GWID / 2
    if step == 1:
        label(ax, GX0 + GWID / 2, 2.9, "커밋이 없어 남음", fs=10, color=INK)
        label(ax, g4, 2.9, "보존 표시가 붙듦", fs=10, color=RED)
        label(ax, 6.0, 1.6, "강제 병합 직후: 지운 문서 200개가 남았어요", fs=11, color=INK)
        return
    ax.plot([CX, CX], [2.3, 4.5], color=INK, lw=2.0)
    label(ax, CX, 1.95, "강제 병합이 남긴 커밋", fs=10, ha="right", color=RED if step == 2 else INK)
    if step == 2:
        label(ax, g4, 2.9, "보존 표시가 붙듦", fs=10, color=INK)
        label(ax, 5.5, 1.1, "한 번 더 합치면 원래 글만 빠져요 (지운 문서 100)", fs=11, color=RED, bold=True)
    else:
        label(ax, 5.5, 1.1, "보존 표시가 400번 뒤로 옮겨 갔어요", fs=11, color=INK)
        moral(ax, 5.5, 0.35, "다시 합치자 지운 문서 0개")


# ── 강제 병합은 언제 ───────────────────────────────────────────────
BIG_PHASES = ["강제 병합 직후", "계속 쓰는 동안", "지운 문서가 쌓인 뒤"]
OLD = {3, 8, 12, 15, 21, 26, 29, 33, 36}


def bigseg(ax, step):
    timeline(ax, step, BIG_PHASES)
    hot = step == 3
    box(ax, 1.3, 1.95, 9.4, 3.3, fc=PINK if hot else NOTE, ec=RED if hot else INK)
    label(ax, 1.45, 4.95, "5 GB를 넘는 세그먼트 하나", fs=10.5, ha="left", bold=True, color=RED if hot else "#222")
    for i in range(40):
        cx, cy = 1.55 + (i % 10) * 0.9, 4.1 - (i // 10) * 0.6
        if step > 1 and i in OLD:
            cell(ax, cx, cy, 0.78, 0.45, "", hot=(step == 2), dim=(step == 3))
            strike(ax, cx, cy, 0.78, 0.45)
        else:
            cell(ax, cx, cy, 0.78, 0.45, "", fc="white")
    if step == 1:
        label(ax, 6.0, 1.3, "계속 쓰는 인덱스를 세그먼트 하나로 합쳤어요", fs=11, color=INK)
    elif step == 2:
        label(ax, 6.0, 1.3, "고친 글의 옛 판이 쌓여도 평소 병합은 손대지 않아요", fs=11, color=RED)
    else:
        label(ax, 6.0, 1.3, "큰 세그먼트 전체를 한꺼번에 다시 써요", fs=11, color=RED, bold=True)
        moral(ax, 6.0, 0.45, "계속 쓰는 인덱스는 강제 병합하지 않아요")


def decide():
    fig, ax = canvas(10, 3.6, 15, 5.4)
    box(ax, 0.3, 3.6, 6.0, 1.3, fc=NOTE)
    label(ax, 3.3, 4.25, "이 인덱스에 앞으로 더 쓰나요?", fs=10.5, bold=True)
    arrow(ax, (6.4, 4.25), (8.4, 4.25), color=RED)
    label(ax, 7.4, 4.55, "예", fs=10, color=RED)
    box(ax, 8.5, 3.6, 6.2, 1.3, fc=PINK, ec=RED)
    label(ax, 11.6, 4.25, "강제 병합하지 말고 ES에 맡겨요", fs=10.5, color=RED, bold=True)
    arrow(ax, (3.3, 3.5), (3.3, 2.6))
    label(ax, 3.6, 3.05, "아니요", fs=10, color=INK, ha="left")
    box(ax, 0.3, 1.3, 6.0, 1.2, fc=PAPER)
    label(ax, 3.3, 1.9, "세그먼트 하나로 강제 병합해도 좋아요\n(검색이 빨라지고 디스크가 줄어요)", fs=10)
    box(ax, 8.5, 1.3, 6.2, 1.2, fc=LIGHT, ec=GREY)
    label(ax, 11.6, 1.9, "기간 지난 데이터를 지우려면\n기간별 인덱스를 통째로 지워요", fs=10, color=INK)
    save(fig, OUT, "es05-decide.svg")


def monthly(ax, step):
    label(ax, 0.3, 6.15, "가계부 기록을 달마다 다른 인덱스에", fs=11, ha="left", color=INK)
    names = ["budget-2025-09", None, "budget-2026-09", "budget-2026-10"]
    for x, n in zip(SEGX, names):
        if n is None:
            label(ax, x + SEGW / 2, 4.0, "⋯", fs=16, color=INK)
            continue
        hot = step == 2 and n.endswith("2025-09")
        box(ax, x, 3.3, SEGW, 1.4, fc=PINK if hot else NOTE, ec=RED if hot else INK)
        label(ax, x + SEGW / 2, 4.2, n, fs=10, color=RED if hot else "#222", bold=hot)
        label(ax, x + SEGW / 2, 3.65, "한 달 치 기록", fs=9.5, color=RED if hot else INK)
    if step == 1:
        label(ax, 6.0, 2.2, "1년 지난 기록을 지울 때가 됐어요", fs=11, color=INK)
        return
    ax.plot([SEGX[0], SEGX[0] + SEGW], [3.3, 4.7], color=RED, lw=2.2)
    ax.plot([SEGX[0], SEGX[0] + SEGW], [4.7, 3.3], color=RED, lw=2.2)
    label(ax, SEGX[0] + SEGW / 2, 2.85, "인덱스를 통째로 지워요", fs=11, color=RED, bold=True)
    label(ax, 6.0, 1.7, "삭제 표시도 병합도 빈 문서도 없어요", fs=11, color=INK)
    moral(ax, 6.0, 0.8, "인덱스를 지우면 파일이 바로 지워져요")


# ── 정리: 처음 장면으로 돌아가기 ───────────────────────────────────
def back(ax, step):
    board(ax, POSTS, dim=(1, 2), footer=None)
    footer(ax, "글 200개")
    if step == 1:
        disk(ax, "25.9 kb", 200)
        bubble(ax, *SAY, "처음엔 지운 뒤에도\n25.9 kb였어요", TAIL)
    else:
        disk(ax, "10.1 kb", 0, hot=True)
        bubble(ax, *SAY, "기록을 붙들 일이 끝난 뒤\n다시 합쳤어요", TAIL, hot=True)
        moral(ax, 4.0, 0.2, "지운 글은 병합 때 실제로 사라져요")


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

    x, y = card(0, "삭제 표시", "세그먼트는 두고\n살아 있나 표에 0을 적기")
    for k, t in enumerate(["1", "2"]):
        cell(ax, x + 1.2 + k * 1.1, y + 2.2, 1.0, 0.5, t, dim=True, fs=10)
        strike(ax, x + 1.2 + k * 1.1, y + 2.2, 1.0, 0.5)
        cell(ax, x + 1.2 + k * 1.1, y + 1.6, 1.0, 0.5, "0", hot=True, fs=10)
    x, y = card(1, "빈 문서 (tombstone)", "지우기 요청이 남기는\n'몇 번 지움' 문서")
    cell(ax, x + 1.2, y + 1.8, 2.2, 0.6, "1번 지움", hot=True, fs=10.5)
    x, y = card(2, "soft delete", "지운 문서는 숨은 값으로,\n지우기는 빈 문서로")
    cell(ax, x + 0.4, y + 1.8, 1.7, 0.6, "글 1", dim=True, fs=10)
    strike(ax, x + 0.4, y + 1.8, 1.7, 0.6)
    cell(ax, x + 2.3, y + 1.8, 1.9, 0.6, "1번 지움", hot=True, fs=10)
    x, y = card(3, "병합", "살아 있는 문서만\n새 세그먼트에 옮겨 적기")
    cell(ax, x + 0.4, y + 2.15, 1.0, 0.45, "", dim=True)
    strike(ax, x + 0.4, y + 2.15, 1.0, 0.45)
    cell(ax, x + 0.4, y + 1.6, 1.0, 0.45, "", fc="white")
    arrow(ax, (x + 1.55, y + 1.85), (x + 2.6, y + 1.85), color=RED, ms=11)
    box(ax, x + 2.75, y + 1.55, 1.4, 0.65, fc=PINK, ec=RED, lw=1.4)
    x, y = card(4, "강제 병합", "병합을 직접 시키는 요청\n(_forcemerge)")
    for k in range(4):
        box(ax, x + 0.35 + k * 0.5, y + 1.8, 0.38, 0.55, fc=NOTE, lw=1.0)
    arrow(ax, (x + 2.4, y + 2.07), (x + 3.0, y + 2.07), color=RED, ms=11)
    box(ax, x + 3.15, y + 1.75, 1.0, 0.65, fc=PINK, ec=RED, lw=1.4)
    x, y = card(5, "복제본", "샤드를 통째로 복사해\n다른 노드에 둔 것")
    box(ax, x + 0.35, y + 1.75, 1.55, 0.65, fc=NOTE, lw=1.2)
    label(ax, x + 1.12, y + 2.07, "주 샤드", fs=9.5)
    arrow(ax, (x + 2.0, y + 2.07), (x + 2.6, y + 2.07), color=RED, ms=11)
    box(ax, x + 2.7, y + 1.75, 1.55, 0.65, fc=PINK, ec=RED, lw=1.4)
    label(ax, x + 3.47, y + 2.07, "복제본", fs=9.5, color=RED)
    x, y = card(6, "보존 표시", "복제본이 받아 간 곳에 꽂는\n책갈피, 뒤 기록은 남겨요")
    cells(ax, x + 0.4, y + 1.75, ["⋯", "300", "301", "⋯"], w=0.85, h=0.55, gap=0.08, fs=9.5)
    xf = x + 0.4 + 2 * 0.93 - 0.04
    ax.plot([xf, xf], [y + 1.6, y + 2.75], color=RED, lw=2.2)
    ax.add_patch(Rectangle((xf - 0.45, y + 2.45), 0.45, 0.3, fc=RED, ec=RED))
    x, y = card(7, "시퀀스 번호", "샤드에 들어온 작업마다\n붙는 차례 번호")
    cells(ax, x + 0.4, y + 1.8, ["1", "2", "3", "⋯", "400"], w=0.7, h=0.55, gap=0.06, hot=(0, 1, 2), fs=9.5)
    save(fig, OUT, "es05-cards.svg")


if __name__ == "__main__":
    S, L = (7.2, 3.8), (12, 6.6)
    stage(opening, 3, OUT, "es05-open", S, L)
    stage(mark, 3, OUT, "es05-mark", S, L)
    stage(tomb, 3, OUT, "es05-tomb", S, L)
    stage(update, 3, OUT, "es05-update", S, L)
    stage(merge, 3, OUT, "es05-merge", S, L)
    stage(turn, 2, OUT, "es05-turn", S, L)
    stage(cost, 2, OUT, "es05-cost", S, L)
    stage(cap, 2, OUT, "es05-cap", S, L)
    stage(retain, 3, OUT, "es05-retain", S, L)
    stage(recover, 2, OUT, "es05-recover", S, L)
    stage(lease, 3, OUT, "es05-lease", S, L)
    stage(bigseg, 3, OUT, "es05-bigseg", S, L)
    decide()
    stage(monthly, 2, OUT, "es05-monthly", S, L)
    stage(back, 2, OUT, "es05-back", S, L)
    cards()
