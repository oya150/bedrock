"""Elasticsearch 9편 그림 만들기. 실행: python lab/fig_es09.py  → docs/elasticsearch/img/09/*.svg

본문 절은 장면 띠로 그린다: 같은 무대를 여러 장 그리고 장마다 바뀐 곳만 빨강으로 칠한다.
예시는 검색어 rare common, 맞는 문서 20만 개를 편 끝까지 잇는다(.claude/writing/work/cal/units-es09.md).
WAND·묶음 그림의 점수(문턱 4.2, common 1.2, rare 8.5)는 설명용이고 건수·계산 횟수는 본문 표의 실측이다.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "es"))
from figkit import (GREY, INK, LIGHT, NOTE, PAPER, PINK, RED, arrow, box, bubble,  # noqa: E402
                    canvas, cell, cells, cylinder, label, magnifier, moral, outdir, save, stage)
from matplotlib.patches import Rectangle  # noqa: E402

OUT = outdir("09")
CYL = (8.0, 3.0, 3.6, 1.7)
SAY = (7.2, 0.45, 4.55, 1.35)
TAIL = (9.8, 2.75)
ROWS = ["1위 문서", "2위 문서", "⋮", "10위 문서"]
GTE = '"value": 10000, "relation": "gte"'


# ── 공통 무대: 검색 화면과 ES ──────────────────────────────────────
def screen(ax, count, hot=False, dim_count=False):
    """처음 장면과 돌아오는 장면의 무대. count=None이면 '?건' 빈칸, 문자열이면 그 값을 건수 칸에 쓴다."""
    box(ax, 0.3, 1.55, 6.7, 4.85, fc="white", round_=False)
    ax.add_patch(Rectangle((0.3, 5.95), 6.7, 0.45, fc=LIGHT, ec=INK, lw=1.2))
    label(ax, 0.5, 6.17, "검색 화면", fs=11, ha="left", color=INK)
    ax.add_patch(Rectangle((0.55, 5.2), 4.8, 0.5, fc="white", ec=INK, lw=1.2))
    magnifier(ax, 0.8, 5.47)
    label(ax, 1.1, 5.45, "rare common", fs=12, ha="left")
    ax.add_patch(Rectangle((5.45, 5.2), 1.3, 0.5, fc=LIGHT, ec=INK, lw=1.2))
    label(ax, 6.1, 5.45, "검색", fs=11.5)
    label(ax, 0.6, 4.72, "검색 결과", fs=11, ha="left", color=INK)
    if count is None:
        ax.add_patch(Rectangle((1.95, 4.47), 1.1, 0.5, fc="white", ec=GREY, lw=1.0, ls="--"))
        label(ax, 2.5, 4.72, "?", fs=12, color=GREY)
        label(ax, 3.15, 4.72, "건", fs=11, ha="left", color=INK)
    else:
        if hot:
            ax.add_patch(Rectangle((1.95, 4.45), 4.95, 0.55, fc=PINK, ec=RED, lw=1.6))
        label(ax, 2.05, 4.72, count, fs=10.5, ha="left", color=RED if hot else (GREY if dim_count else "#222"), bold=hot)
    ax.plot([0.55, 6.75], [4.3, 4.3], color=INK, lw=1.0)
    for k, t in enumerate(ROWS):
        y = 3.95 - k * 0.55
        if t == "⋮":
            label(ax, 3.65, y, t, fs=12, color=INK)
            continue
        label(ax, 0.75, y, t, fs=11.5, ha="left")
        ax.plot([0.55, 6.75], [y - 0.27, y - 0.27], color=GREY, lw=0.8)


def es(ax, lines, hot=False):
    x, y, w, h = CYL
    cylinder(ax, *CYL, "ES")
    c = RED if hot else "#222"
    for k, t in enumerate(lines):
        label(ax, x + w / 2, y + 1.15 - k * 0.65, t, fs=11, color=c, bold=hot)


# ── 여는 장면: 건수가 1만 개 이상으로 나와요 ───────────────────────
def opening(ax, step):
    if step == 1:
        screen(ax, None)
        es(ax, ["맞는 문서", "200,000개"])
        bubble(ax, *SAY, "위 10개를\n보냈어요", TAIL)
    else:
        screen(ax, GTE, hot=True)
        es(ax, ["맞는 문서", "200,000개"])
        bubble(ax, *SAY, "건수는 1만 개까지만\n셌어요", TAIL, hot=True)
        moral(ax, 3.65, 0.85, "맞는 문서는 20만 개인데 1만 개 이상이래요")


# ── 위 10개는 힙으로 골라요 (그림은 위 3개로 줄임) ────────────────
TOP, KIDS = (2.6, 4.3), [(1.1, 2.75), (4.1, 2.75)]
NW, NH = 1.2, 0.75


def heap(ax, step):
    label(ax, 0.3, 6.2, "지금까지 본 점수 중 위 3개 (힙, 가장 작은 점수가 맨 위)", fs=11.5, ha="left", bold=True)
    tx, ty = TOP
    for kx, ky in KIDS:
        ax.plot([tx + NW / 2, kx + NW / 2], [ty, ky + NH], color=INK, lw=1.2)
    top = "5.1" if step == 3 else "4.2"
    on = step in (1, 3)
    cell(ax, tx, ty, NW, NH, top, hot=on, fs=12)
    cell(ax, *KIDS[0], NW, NH, "6.0", fs=12)
    cell(ax, *KIDS[1], NW, NH, "7.5", fs=12)
    label(ax, tx - 0.15, ty + NH / 2, f"문턱 {top}", fs=11, ha="right", color=RED if on else INK, bold=on)
    if step >= 2:
        hot2 = step == 2
        box(ax, 8.4, 4.4, 3.0, 0.8, fc=PINK if hot2 else LIGHT, ec=RED if hot2 else GREY)
        label(ax, 9.9, 4.8, "새 문서 3.1", fs=11, color=RED if hot2 else GREY)
        arrow(ax, (8.3, 4.8), (tx + NW + 0.1, ty + 0.5), color=RED if hot2 else GREY, ms=14)
        label(ax, 9.9, 3.95, "4.2보다 작아서 버려요", fs=10.5, color=RED if hot2 else INK)
    if step == 3:
        box(ax, 8.4, 2.4, 3.0, 0.8, fc=PINK, ec=RED)
        label(ax, 9.9, 2.8, "새 문서 5.1", fs=11, color=RED)
        arrow(ax, (8.3, 2.8), (tx + NW + 0.1, ty + 0.2), color=RED, ms=14)
        label(ax, 9.9, 1.95, "4.2를 밀어내고 들어가요", fs=10.5, color=RED)
        moral(ax, 6.0, 0.8, "문턱은 올라가기만 해요")
    elif step == 1:
        label(ax, 6.0, 1.5, "이 점수를 넘어야 위 3개에 들 수 있어요", fs=11, color=INK)


# ── 목록 두 줄: common과 rare ──────────────────────────────────────
LX, LW, LS = 2.3, 0.9, 1.0
CY, RY = 4.3, 2.9


def cx(d):
    return LX + (d - 1) * LS


def lists(ax, skip_dim=False, rare_hot=False):
    label(ax, 0.3, CY + 0.5, "common", fs=11, ha="left", bold=True)
    label(ax, 0.3, CY + 0.1, "최고 1.2", fs=10, ha="left", color=INK)
    label(ax, 0.3, RY + 0.5, "rare", fs=11, ha="left", bold=True)
    label(ax, 0.3, RY + 0.1, "최고 8.5", fs=10, ha="left", color=INK)
    for d in range(1, 8):
        both = d in (3, 6)
        cell(ax, cx(d), CY, LW, 0.7, d, hot=both and rare_hot, dim=skip_dim and not both, fs=12)
        if both:
            cell(ax, cx(d), RY, LW, 0.7, d, hot=rare_hot, fs=12)


# ── 문턱을 넘을 수 없는 문서는 계산하지 않아요 (WAND) ──────────────
def wand(ax, step):
    label(ax, 0.3, 6.2, "검색어 rare common · 지금 문턱 4.2", fs=11.5, ha="left", bold=True)
    lists(ax, skip_dim=step >= 2, rare_hot=step == 3)
    if step == 1:
        label(ax, 6.0, 1.6, "문서마다 낼 수 있는 최고 점수를 더해 봐요", fs=11, color=INK)
        label(ax, 6.0, 0.95, "common만 있으면 1.2, 둘 다 있으면 1.2 + 8.5 = 9.7", fs=10.5, color=INK)
    elif step == 2:
        for d in (1, 2, 4, 5, 7):
            label(ax, cx(d) + LW / 2, CY - 0.3, "건너뜀", fs=9.5, color=RED)
        label(ax, 6.0, 1.6, "common만 든 문서: 최고 1.2 ≤ 문턱 4.2", fs=11, color=RED, bold=True)
        label(ax, 6.0, 0.95, "아무리 잘 받아도 문턱을 못 넘어요", fs=10.5, color=INK)
    elif step == 3:
        for d in (3, 6):
            label(ax, cx(d) + LW / 2, RY - 0.3, "계산", fs=10, color=RED, bold=True)
        label(ax, 6.0, 1.6, "rare가 든 문서: 최고 9.7 > 문턱 4.2", fs=11, color=RED, bold=True)
        label(ax, 6.0, 0.95, "이 문서만 점수를 계산해요", fs=10.5, color=INK)
    else:
        s0 = LX - 0.25
        a3, b3, a6 = cx(3) + 0.3, cx(3) + 0.6, cx(6) + 0.3
        # rare 목록이 앞장서요(①③, 아래), common은 그 번호로 건너뛰어요(②④, 위)
        arrow(ax, (s0, RY - 0.1), (a3, RY - 0.1), color=RED, rad=0.35, ms=13, lw=1.6)
        label(ax, (s0 + a3) / 2, RY - 0.85, "①", fs=11, color=RED, bold=True)
        arrow(ax, (b3, RY - 0.1), (a6, RY - 0.1), color=RED, rad=0.35, ms=13, lw=1.6)
        label(ax, (b3 + a6) / 2, RY - 0.85, "③", fs=11, color=RED, bold=True)
        arrow(ax, (s0, CY + 0.8), (a3, CY + 0.8), color=RED, rad=-0.35, ms=13, lw=1.6)
        label(ax, (s0 + a3) / 2, CY + 1.5, "② advance(3)", fs=10, color=RED)
        arrow(ax, (b3, CY + 0.8), (a6, CY + 0.8), color=RED, rad=-0.35, ms=13, lw=1.6)
        label(ax, (b3 + a6) / 2, CY + 1.5, "④ advance(6)", fs=10, color=RED)
        label(ax, 10.7, CY + 0.35, "1 2 4 5 7은\n밟지 않아요", fs=10, color=INK)
        moral(ax, 6.0, 0.95, "드문 rare 목록이 앞장서고 common은 건너뛰어요")


# ── 묶음마다 최고 점수 (block-max) ─────────────────────────────────
BX = [0.3, 4.2, 8.1]
BW = 3.6
BLOCKS = [("0.6", "3.0", "3.6", False), ("1.2", "8.5", "9.7", True), ("0.7", "2.9", "3.6", False)]


def blockmax(ax, step):
    label(ax, 0.3, 6.2, "문턱 4.2 · 128개씩 묶음", fs=11.5, ha="left", bold=True)
    label(ax, 11.7, 6.2, "c: common만 든 문서, r: rare도 든 문서", fs=10, ha="right", color=INK)
    for k, (x, (c, r, s, opn)) in enumerate(zip(BX, BLOCKS)):
        skipped = step == 3 and not opn
        box(ax, x, 3.4, BW, 1.9, fc=LIGHT if skipped else NOTE, ec=GREY if skipped else INK)
        label(ax, x + 0.15, 5.0, f"묶음 {k + 1}", fs=10.5, ha="left", bold=True, color=GREY if skipped else "#222")
        for j in range(5):
            cell(ax, x + 0.2 + j * 0.65, 3.65, 0.58, 0.7, "r" if j == 2 else "c", dim=skipped, fs=10.5)
        if step == 1:
            label(ax, x + BW / 2, 2.85, "1.2 + 8.5 = 9.7", fs=10.5, color=INK)
            label(ax, x + BW / 2, 2.3, "열어 봐요", fs=10.5, color=INK)
        else:
            hot2 = step == 2
            label(ax, x + BW / 2, 2.85, f"{c} + {r} = {s}", fs=10.5, color=RED if hot2 else INK, bold=hot2)
            if step == 3:
                label(ax, x + BW / 2, 2.3, "열어 봐요" if opn else "통째로 건너뜀", fs=10.5,
                      color=INK if opn else RED, bold=not opn)
    if step == 1:
        label(ax, 6.0, 1.45, "목록 전체의 최고 점수로 보면", fs=11, color=RED)
        label(ax, 6.0, 0.85, "rare가 든 묶음은 모두 열어 봐야 해요", fs=11, color=RED, bold=True)
    elif step == 2:
        label(ax, 6.0, 1.45, "묶음마다 그 안의 최고 점수를 적어 둬요", fs=11, color=RED, bold=True)
    else:
        moral(ax, 6.0, 1.2, "문턱을 못 넘는 묶음은 통째로 건너뛰어요")


# ── 전환: 건너뛰는 대신 치르는 값 ──────────────────────────────────
def turn(ax, step):
    screen(ax, GTE, dim_count=step == 2)
    es(ax, ["맞는 문서", "200,000개"])
    if step == 1:
        bubble(ax, *SAY, "문턱을 못 넘는 문서는\n계산하지 않았어요", TAIL)
        return
    bubble(ax, 7.3, 0.15, 4.45, 2.4, "", TAIL, hot=True)
    label(ax, 9.52, 2.1, "대신 치르는 값이 있어요", fs=11.5, color=RED, bold=True)
    for k, t in enumerate(["① 건너뛴 문서는 안 세요", "② 다 봐야 하면 못 건너뛰어요"]):
        label(ax, 7.55, 1.45 - k * 0.6, t, fs=10.5, ha="left", color=RED)


# ── 첫째 값: 건너뛴 문서는 세지 않아요 ─────────────────────────────
def tally(ax, step):
    label(ax, 0.3, 6.2, "검색어 rare common · 맞는 문서 7개", fs=11.5, ha="left", bold=True)
    lists(ax, skip_dim=step == 1)
    box(ax, 9.6, 3.3, 2.1, 1.6, fc=PINK, ec=RED)
    label(ax, 10.65, 4.5, "건수", fs=11, color=RED)
    if step == 1:
        label(ax, 10.65, 3.8, "2", fs=16, color=RED, bold=True)
        label(ax, 6.0, 1.6, "건너뛴 1 2 4 5 7은 세지도 않았어요", fs=11, color=RED, bold=True)
        label(ax, 6.0, 0.95, "계산한 3과 6만 셌어요", fs=10.5, color=INK)
    else:
        label(ax, 10.65, 3.8, "7 (eq)", fs=15, color=RED, bold=True)
        arrow(ax, (LX - 0.25, CY + 0.95), (cx(7) + LW + 0.1, CY + 0.95), color=RED, ms=14, lw=1.8)
        label(ax, 5.3, CY + 1.3, "맞는 문서를 하나씩 다 지나가요", fs=10.5, color=RED)
        label(ax, 6.0, 1.6, "정확한 건수를 내려면 7개를 모두 봐야 해요", fs=11, color=INK)
        moral(ax, 6.0, 0.9, "다 세려면 건너뛸 수 없어요")


# ── 실측: track_total_hits 세 가지 ─────────────────────────────────
PHASES = ["true", "기본값 (1만)", "false"]
ROWS3 = {1: ("점수 계산 200,000번 (두 버전 같음)", "건수 200,000 (eq)"),
         2: ("점수 계산 10,022번 (7.17은 11,635번)", "건수 10,000 (gte)"),
         3: ("점수 계산 604번 (7.17은 2,446번)", "건수는 세지 않아요")}


def counts(ax, step):
    label(ax, 0.3, 6.2, "track_total_hits를 바꿔 가며 위 10개 찾기", fs=11.5, ha="left", bold=True)
    for k, t in enumerate(PHASES):
        x = 0.3 + k * 3.9
        on = k + 1 == step
        label(ax, x + 1.6, 5.5, t, fs=11, color=RED if on else INK, bold=on)
        if k < 2:
            arrow(ax, (x + 3.0, 5.5), (x + 3.7, 5.5), color=GREY, ms=10, lw=1.2)
    label(ax, 0.3, 4.75, "맞는 문서 20만 개 (한 칸 = 1만 개, 빨강 = 점수 계산)", fs=10.5, ha="left", color=INK)
    for i in range(20):
        x = 0.3 + i * 0.57
        if step == 1 or (step == 2 and i == 0):
            cell(ax, x, 3.75, 0.5, 0.7, "", hot=True)
        else:
            cell(ax, x, 3.75, 0.5, 0.7, "", fc="white")
    if step == 3:
        ax.add_patch(Rectangle((0.3, 3.75), 0.07, 0.7, fc=RED, ec=RED))
    a, b = ROWS3[step]
    label(ax, 6.0, 2.95, a, fs=11.5, color=RED, bold=True)
    label(ax, 6.0, 2.3, b, fs=11, color=RED)
    label(ax, 6.0, 1.55, "1위 점수는 세 경우 모두 같았어요", fs=10.5, color=INK)
    if step == 3:
        moral(ax, 6.0, 0.8, "덜 셀수록 덜 계산해요")


# ── 둘째 값: 다 봐야 하는 요청 ─────────────────────────────────────
def request_card(ax, extra):
    box(ax, 0.3, 2.3, 6.4, 3.8, fc=PAPER)
    label(ax, 0.55, 5.75, "검색 요청", fs=11, ha="left", bold=True)
    for k, t in enumerate(["query: rare common", "size: 10", "track_total_hits: false"]):
        label(ax, 0.6, 5.1 - k * 0.6, t, fs=10.5, ha="left", family="monospace")
    if extra is None:
        ax.add_patch(Rectangle((0.55, 2.55), 5.9, 0.6, fc="white", ec=GREY, lw=1.0, ls="--"))
        label(ax, 3.5, 2.85, "덧붙인 것 없음", fs=10, color=GREY)
    else:
        ax.add_patch(Rectangle((0.55, 2.55), 5.9, 0.6, fc=PINK, ec=RED, lw=1.5))
        label(ax, 0.7, 2.85, extra, fs=10.5, ha="left", color=RED, bold=True)


def fullscan(ax, step):
    if step == 1:
        request_card(ax, None)
        es(ax, ["건너뛰기 켜짐", "604번 계산"])
        bubble(ax, *SAY, "문턱으로\n건너뛰었어요", TAIL)
    elif step == 2:
        request_card(ax, "+ 집계: 카테고리별 건수")
        es(ax, ["건너뛰기 꺼짐", "다 지나가요"], hot=True)
        bubble(ax, *SAY, "건수를 내려면\n다 봐야 해요", TAIL, hot=True)
    else:
        request_card(ax, "+ function_score: weight")
        es(ax, ["건너뛰기 꺼짐", "200,000번 계산"], hot=True)
        bubble(ax, *SAY, "점수에 값을 섞으면\n건너뛰기가 꺼져요", TAIL, hot=True)
        moral(ax, 3.5, 1.5, "다 봐야 하는 요청은 못 건너뛰어요")


# ── 언제 쓸모 있을까: 갈림길 ───────────────────────────────────────
def decide():
    fig, ax = canvas(10, 4.2, 15, 6.0)
    box(ax, 0.3, 4.4, 4.6, 1.2, fc=NOTE)
    label(ax, 2.6, 5.0, "총 건수를 정확히\n보여 줘야 하나요?", fs=11.5, bold=True)
    box(ax, 7.0, 4.4, 7.7, 1.2, fc=LIGHT, ec=GREY)
    label(ax, 10.85, 5.0, "기본값 그대로 두고\n\"1만 건 이상\"으로 보여 줘요", fs=10.5)
    arrow(ax, (5.0, 5.0), (6.9, 5.0))
    label(ax, 5.95, 5.35, "아니요", fs=10, color=INK)
    arrow(ax, (2.6, 4.3), (2.6, 3.0))
    label(ax, 2.9, 3.65, "예", fs=10, color=INK, ha="left")
    box(ax, 0.3, 0.8, 4.6, 2.1, fc=NOTE)
    label(ax, 2.6, 1.85, "몇 건까지\n정확하면 되나요?", fs=11.5, bold=True)
    arrow(ax, (5.0, 2.2), (6.9, 2.75))
    label(ax, 5.9, 2.9, "10만 건까지", fs=10, color=INK)
    box(ax, 7.0, 2.25, 7.7, 1.0, fc=LIGHT, ec=GREY)
    label(ax, 10.85, 2.75, "track_total_hits: 100000\n그 안에서만 정확히 세요", fs=10.5)
    arrow(ax, (5.0, 1.5), (6.9, 1.05), color=RED)
    label(ax, 5.9, 0.95, "끝까지", fs=10, color=RED)
    box(ax, 7.0, 0.55, 7.7, 1.0, fc=PINK, ec=RED)
    label(ax, 10.85, 1.05, "꼭 필요한 화면에서만 true\n지연이 얼마나 느는지 재 보고 정해요", fs=10.5, color=RED)
    save(fig, OUT, "es09-decide.svg")


# ── 정리: 처음 장면으로 돌아가기 ───────────────────────────────────
def back(ax, step):
    if step == 1:
        screen(ax, GTE)
        es(ax, ["맞는 문서", "200,000개"])
        bubble(ax, *SAY, "처음엔 1만 개 이상\n이라고만 했어요", TAIL)
    elif step == 2:
        screen(ax, GTE)
        es(ax, ["점수 계산", "10,022번"], hot=True)
        bubble(ax, *SAY, "1만 개째까지 세고\n그 뒤로는 건너뛰었어요", TAIL, hot=True)
    else:
        screen(ax, "1만 건 이상", hot=True)
        es(ax, ["점수 계산", "10,022번"])
        bubble(ax, *SAY, "위 10개는 다 셀 때와\n똑같아요", TAIL)
        moral(ax, 3.65, 0.85, "다 세지 않아서 덜 계산했어요")


# ── 정리: 낱말 카드 ────────────────────────────────────────────────
def cards():
    """이 편 본문에서 이름 붙인 말 여섯. 카드마다 본문 그림을 작게 다시 그리고 한 줄 뜻. 휴대폰 폭에 맞게 두 장씩."""
    fig, ax = canvas(6.4, 7.9, 9.8, 12.2)
    W, H = 4.6, 3.8

    def card(i, name, line):
        col, row = i % 2, i // 2
        x, y = 0.2 + col * 4.9, 8.2 - row * 4.05
        box(ax, x, y, W, H, fc="white")
        label(ax, x + 0.25, y + H - 0.4, name, fs=12.5, ha="left", bold=True)
        label(ax, x + W / 2, y + 0.6, line, fs=10, color=INK)
        return x, y

    x, y = card(0, "힙", "위 몇 개만 들고 가장 작은\n점수를 맨 위에 두는 칸")
    for kx in (0.95, 2.75):
        ax.plot([x + 2.3, x + kx + 0.45], [y + 2.15, y + 1.95], color=INK, lw=1.0)
    cell(ax, x + 1.85, y + 2.15, 0.9, 0.55, "4.2", hot=True, fs=10)
    cell(ax, x + 0.95, y + 1.4, 0.9, 0.55, "6.0", fs=10)
    cell(ax, x + 2.75, y + 1.4, 0.9, 0.55, "7.5", fs=10)
    x, y = card(1, "문턱", "힙 맨 위 점수, 넘어야\n위 10개에 들어요")
    cell(ax, x + 0.5, y + 1.75, 1.0, 0.6, "4.2", dim=True, fs=10.5)
    arrow(ax, (x + 1.65, y + 2.05), (x + 2.75, y + 2.05), color=RED, ms=11)
    cell(ax, x + 2.9, y + 1.75, 1.0, 0.6, "5.1", hot=True, fs=10.5)
    x, y = card(2, "WAND", "낱말별 최고 점수를 더해\n못 넘는 문서는 건너뛰기")
    cells(ax, x + 0.5, y + 2.2, [1, 2, 3, 4], w=0.8, h=0.5, gap=0.1, dim=(0, 1, 3), hot=(2,), fs=10)
    cell(ax, x + 0.5 + 2 * 0.9, y + 1.6, 0.8, 0.5, 3, hot=True, fs=10)
    x, y = card(3, "block-max WAND", "128개 묶음마다 최고 점수로\n묶음째 건너뛰기")
    for k in range(3):
        skip = k != 1
        box(ax, x + 0.4 + k * 1.35, y + 1.65, 1.1, 0.75, fc=LIGHT if skip else PINK, ec=GREY if skip else RED, lw=1.2)
        label(ax, x + 0.95 + k * 1.35, y + 2.02, "3.6" if skip else "9.7", fs=10, color=GREY if skip else RED)
    x, y = card(4, "impacts", "묶음 최고 점수의 재료\n(횟수와 문서 길이)")
    cell(ax, x + 0.6, y + 1.75, 3.4, 0.6, "(횟수 2, 길이 3) ⋯", hot=True, fs=10)
    x, y = card(5, "track_total_hits", "건수를 몇 개까지\n정확히 셀지 정하는 값")
    for i in range(8):
        cell(ax, x + 0.4 + i * 0.48, y + 1.75, 0.42, 0.55, "", hot=(i == 0), fc=None if i == 0 else "white")
    label(ax, x + 0.61, y + 2.55, "1만", fs=9.5, color=RED)
    save(fig, OUT, "es09-cards.svg")


if __name__ == "__main__":
    S, L = (7.2, 3.8), (12, 6.6)
    stage(opening, 2, OUT, "es09-open", S, L)
    stage(heap, 3, OUT, "es09-heap", S, L)
    stage(wand, 4, OUT, "es09-wand", S, L)
    stage(blockmax, 3, OUT, "es09-block", S, L)
    stage(turn, 2, OUT, "es09-turn", S, L)
    stage(tally, 2, OUT, "es09-tally", S, L)
    stage(counts, 3, OUT, "es09-counts", S, L)
    stage(fullscan, 3, OUT, "es09-full", S, L)
    decide()
    stage(back, 3, OUT, "es09-back", S, L)
    cards()
