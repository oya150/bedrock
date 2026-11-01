"""Elasticsearch 8편 그림 만들기. 실행: python lab/fig_es08.py  → docs/elasticsearch/img/08/*.svg

본문 절은 장면 띠로 그린다: 같은 무대를 여러 장 그리고 장마다 바뀐 곳만 빨강으로 칠한다.
예시는 검색어 "환불 배송"과 두 문서 "환불 환불 문의", "배송 지연 문의"를 편 끝까지 잇는다
(.claude/writing/work/cal/units-es08.md). 개발 서버와 다른 서버 모두 문서 52개.
"""
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "es"))
from figkit import (GREY, INK, LIGHT, NOTE, PAPER, PINK, RED, arrow, box, bubble, canvas, cell, cells,  # noqa: E402
                    cylinder, label, magnifier, moral, outdir, save, stage)
from matplotlib.patches import Rectangle  # noqa: E402

OUT = outdir("08")
K1, B = 1.2, 0.75
A_DOC, B_DOC = "환불 환불 문의", "배송 지연 문의"
CYL = (8.1, 3.2, 3.4, 1.7)
SAY = (7.1, 0.75, 4.7, 1.3)
TAIL = (9.8, 2.95)


def idf(N, n):
    return math.log(1 + (N - n + 0.5) / (n + 0.5))


def tf(f, dl, avgdl):
    return f / (f + K1 * (1 - B + B * dl / avgdl))


# 그림 숫자는 여기서 계산해 본문 숫자와 맞는지 확인한다
AVG = 136 / 52
assert f"{2.2 * idf(52, 1) * tf(2, 3, AVG):.3f}" == "4.707"
assert f"{2.2 * idf(52, 31) * tf(2, 3, AVG):.3f}" == "0.687"
assert f"{2.2 * idf(52, 1) * tf(1, 3, AVG):.3f}" == "3.363"
assert f"{2.2 * idf(52, 31) * tf(1, 3, AVG):.3f}" == "0.491"
assert f"{idf(52, 31):.4f}" == "0.5203" and f"{tf(2, 3, AVG):.4f}" == "0.6002"
SH = 122 / 41
assert f"{2.2 * idf(41, 41) * tf(1, 2, SH):.3f}" == "0.014"
assert f"{2.2 * idf(41, 1) * tf(1, 2, SH):.3f}" == "3.848"
assert f"{2.2 * idf(82, 42) * tf(1, 2, SH):.3f}" == "0.773"
assert [f"{tf(1, r * 4, 4):.2f}" for r in (1, 0.5, 2)] == ["0.45", "0.57", "0.32"]


def empty(ax, x, y, w, h, s="", fs=10):
    ax.add_patch(Rectangle((x, y), w, h, fc="white", ec=GREY, lw=1.0, ls="--"))
    if s:
        label(ax, x + w / 2, y + h / 2, s, fs=fs, color=GREY)


# ── 무대: 검색 화면 + ES 원통 (여는 장면과 돌아오는 장면) ──────────
ROW_Y = (3.85, 3.2)


def screen(ax, server, rows, hot_rows=False, scores=None, hot_scores=False, test=None, test_hot=False, test_dim=False):
    """검색 화면. rows=[1위 제목, 2위 제목], scores=[점수, 점수], test=(글, ✓/✗)."""
    box(ax, 0.3, 0.95, 6.5, 5.45, fc="white", round_=False)
    ax.add_patch(Rectangle((0.3, 5.95), 6.5, 0.45, fc=LIGHT, ec=INK, lw=1.2))
    label(ax, 0.5, 6.17, f"고객 문의 검색 · {server}", fs=11, ha="left", color=INK)
    ax.add_patch(Rectangle((0.55, 5.2), 4.7, 0.5, fc="white", ec=INK, lw=1.2))
    magnifier(ax, 0.8, 5.47)
    label(ax, 1.1, 5.45, "환불 배송", fs=12, ha="left")
    ax.add_patch(Rectangle((5.35, 5.2), 1.2, 0.5, fc=LIGHT, ec=INK, lw=1.2))
    label(ax, 5.95, 5.45, "검색", fs=11.5)
    label(ax, 0.95, 4.65, "순위", fs=10, color=INK)
    label(ax, 3.2, 4.65, "제목", fs=10, color=INK)
    label(ax, 5.9, 4.65, "점수", fs=10, color=INK)
    ax.plot([0.55, 6.55], [4.42, 4.42], color=INK, lw=1.0)
    for k, (t, y) in enumerate(zip(rows, ROW_Y)):
        if hot_rows:
            ax.add_patch(Rectangle((0.55, y - 0.26), 6.0, 0.52, fc=PINK, ec=RED, lw=1.8))
        else:
            ax.plot([0.55, 6.55], [y - 0.3, y - 0.3], color=GREY, lw=0.8)
        c = RED if hot_rows else "#222"
        label(ax, 0.95, y, f"{k + 1}위", fs=11, color=c, bold=hot_rows)
        label(ax, 1.6, y, t, fs=11.5, ha="left", color=c, bold=hot_rows)
        if scores:
            label(ax, 5.9, y, scores[k], fs=11.5, color=RED if hot_scores else "#222", bold=hot_scores)
    if test:
        s, mark = test
        c = RED if test_hot else (GREY if test_dim else "#222")
        ax.add_patch(Rectangle((0.55, 1.25), 6.0, 0.95, fc=PINK if test_hot else PAPER, ec=RED if test_hot else INK,
                               lw=1.5 if test_hot else 1.0))
        label(ax, 0.75, 1.92, "테스트", fs=10, ha="left", color=c, bold=True)
        label(ax, 0.75, 1.5, s, fs=11, ha="left", color=c)
        label(ax, 6.15, 1.72, mark, fs=17, color=c, bold=True)


def es(ax, lines, hot=False):
    x, y, w, h = CYL
    cylinder(ax, *CYL, "ES (문서 52개)")
    c = RED if hot else "#222"
    for k, t in enumerate(lines):
        label(ax, x + w / 2, y + 1.15 - k * 0.6, t, fs=11, color=c, bold=hot)


OTHER = ["환불 언제 돼요 ×30", "상품 문의 ×20"]


def opening(ax, step):
    if step == 1:
        screen(ax, "개발 서버", [A_DOC, B_DOC], test=("1위는 환불 환불 문의", "✓"))
        es(ax, ["두 문서 +", "다른 글 50개"])
        bubble(ax, *SAY, "개발 서버에서는\n환불 환불 문의가 1위예요", TAIL)
    elif step == 2:
        screen(ax, "다른 서버", [B_DOC, A_DOC], hot_rows=True, test=("1위는 환불 환불 문의", "✗"), test_hot=True)
        es(ax, ["두 문서 +", "다른 글 50개"])
        bubble(ax, *SAY, "같은 두 문서인데\n순위가 거꾸로예요", TAIL, hot=True)
    else:
        screen(ax, "다른 서버", [B_DOC, A_DOC], test=("1위는 환불 환불 문의", "✗"), test_dim=True)
        es(ax, OTHER, hot=True)
        bubble(ax, *SAY, "개발 서버에선 이 30개가\n'배송 언제 와요'였어요", TAIL, hot=True)
        moral(ax, 6.0, 0.3, "다른 글만 바뀌었는데 순위가 뒤집혔어요")


def back(ax, step):
    if step == 1:
        screen(ax, "다른 서버", [B_DOC, A_DOC], test=("1위는 환불 환불 문의", "✗"), test_dim=True)
        es(ax, OTHER)
        bubble(ax, *SAY, "처음엔 다른 글만 바뀌었는데\n순위가 뒤집혔어요", TAIL)
    else:
        screen(ax, "다른 서버", [B_DOC, A_DOC], scores=["3.363", "0.687"], hot_scores=True,
               test=("1위는 환불 환불 문의", "✗"), test_dim=True)
        es(ax, OTHER)
        bubble(ax, *SAY, "환불은 31개 문서에 있어 가볍고\n배송은 1개에만 있어 무거워요", TAIL, hot=True, fs=11)
        moral(ax, 6.0, 0.3, "순위는 함께 든 다른 문서들 속에서 정해져요")


# ── 점수는 낱말마다 곱해서 더해요 ──────────────────────────────────
def sum_(ax, step):
    ax.add_patch(Rectangle((0.3, 5.3), 3.6, 0.6, fc="white", ec=INK, lw=1.2))
    magnifier(ax, 0.6, 5.6)
    label(ax, 0.9, 5.58, "환불 배송", fs=12, ha="left")
    label(ax, 4.5, 5.6, "문서", fs=10.5, color=INK, ha="left")
    cell(ax, 5.3, 5.3, 3.0, 0.6, A_DOC, fs=11.5)
    label(ax, 8.5, 5.6, "(다른 서버)", fs=10, color=INK, ha="left")
    for w, y in (("환불", 3.9), ("배송", 2.2)):
        cell(ax, 0.3, y, 1.4, 0.7, w, hot=(step == 1), fs=12)
        label(ax, 2.0, y + 0.35, "→", fs=13, color=INK)
    if step == 1:
        for y in (3.9, 2.2):
            empty(ax, 2.4, y, 9.2, 0.7, "?", fs=13)
        label(ax, 6.0, 1.2, "검색어를 낱말로 나눠 낱말마다 점수를 내요", fs=11, color=RED, bold=True)
        return
    hot2 = step == 2
    c = RED if hot2 else "#222"
    for x, t in ((2.9, "2.2"), (3.85, "×"), (5.0, "0.5203"), (6.15, "×"), (7.3, "0.6002"), (8.4, "="), (9.5, "0.6870")):
        label(ax, x, 4.25, t, fs=12.5, color=c, bold=hot2)
    for x, t in ((2.9, "모든 낱말에\n똑같이"), (5.0, "드문 정도\n(IDF)"), (7.3, "횟수 몫\n(tf)"), (9.5, "'환불' 점수")):
        label(ax, x, 3.4, t, fs=9.5, color=c)
    if step == 2:
        empty(ax, 2.4, 2.2, 9.2, 0.7, "?", fs=13)
        return
    label(ax, 2.5, 2.55, "이 문서에 없어요  →  0", fs=12.5, ha="left", color=RED, bold=True)
    ax.plot([0.3, 11.6], [1.75, 1.75], color=INK, lw=1.0)
    label(ax, 0.3, 1.25, "문서 점수", fs=11, ha="left", bold=True)
    label(ax, 2.5, 1.25, "0.6870  +  0  =  0.6870", fs=12.5, ha="left", color=RED, bold=True)
    moral(ax, 6.0, 0.4, "낱말마다 낸 점수를 더하면 문서 점수예요")


# ── 많이 나올수록 높지만 금방 배불러요 ─────────────────────────────
FS = [1, 2, 5, 10, 20]
BX = [1.6 + k * 2.0 for k in range(5)]
Y0, TOP = 1.5, 3.8


def tfbars(ax, step):
    label(ax, 0.3, 6.2, "문서 안에서 \"환불\"이 나온 횟수 (문서 길이는 평균)", fs=11, ha="left", color=INK)
    ax.plot([0.9, 11.6], [Y0, Y0], color=INK, lw=1.2)
    for x, f in zip(BX, FS):
        label(ax, x, Y0 - 0.35, f"{f}번", fs=11)
    if step == 1:
        for x, f in zip(BX, FS):
            h = TOP * f / 20
            ax.add_patch(Rectangle((x - 0.4, Y0), 0.8, h, fc=PINK, ec=RED, lw=1.6))
            label(ax, x, Y0 + h + 0.3, f"{f}배", fs=11, color=RED, bold=True)
        label(ax, 4.6, 4.6, "횟수를 그대로 쓰면", fs=11.5, color=RED, bold=True)
        return
    ax.plot([0.9, 11.6], [Y0 + TOP, Y0 + TOP], color=GREY, lw=1.4, ls="--")
    label(ax, 0.75, Y0 + TOP, "1", fs=11, color=INK, ha="right")
    for x, f in zip(BX, FS):
        v = f / (f + K1)
        h = TOP * v
        ax.add_patch(Rectangle((x - 0.4, Y0), 0.8, h, fc=PINK, ec=RED, lw=1.6))
        label(ax, x, Y0 + h - 0.3, f"{v:.2f}", fs=10.5, color=RED, bold=True)
    label(ax, 3.0, 5.65, "BM25의 횟수 몫", fs=11.5, color=RED, bold=True)
    moral(ax, 6.0, 0.35, "많이 나올수록 오르지만 1을 넘지 않아요")


# ── 드문 낱말일수록 무거워요 ───────────────────────────────────────
GCOLS, GW, GH = 13, 0.56, 0.5


def grid(ax, step):
    server = "개발 서버" if step == 1 else "다른 서버"
    label(ax, 0.3, 6.2, f"{server} · 문서 52개 (한 칸이 문서 하나)", fs=11, ha="left", color=INK)
    n = 1 if step == 1 else 31
    for i in range(52):
        cx = 0.3 + (i % GCOLS) * (GW + 0.08)
        cy = 4.9 - (i // GCOLS) * (GH + 0.1)
        on = i < n
        ax.add_patch(Rectangle((cx, cy), GW, GH, fc=PINK if on else NOTE, ec=RED if on else INK, lw=1.6 if on else 0.8))
    label(ax, 4.45, 2.35, "빨간 칸 = \"환불\"이 든 문서", fs=10.5, color=RED)
    x = 10.2
    label(ax, x, 5.2, "\"환불\"이 든 문서", fs=11, color=INK)
    label(ax, x, 4.5, f"{n}개 / 52개", fs=13, color=RED, bold=True)
    label(ax, x, 3.6, "드문 정도 (IDF)", fs=11, color=INK)
    label(ax, x, 2.9, f"{idf(52, n):.2f}", fs=17, color=RED, bold=True)
    if step == 2:
        moral(ax, 6.0, 1.2, "같은 \"환불\"이라도 흔해지면 무게가 줄어요")
        label(ax, 6.0, 0.5, "드물 때 3.56 → 흔할 때 0.52", fs=11, color=INK)


# ── 짧은 문서가 유리해요 ───────────────────────────────────────────
DOCS = [("평균 길이", ["환불", "문의", "드려요", "급해요"], "0.45"),
        ("평균의 절반", ["환불", "문의"], "0.57"),
        ("평균의 두 배", ["배송", "교환", "환불", "기간", "안내", "꼭", "읽어", "주세요"], "0.32")]
WW = 0.98


def length(ax, step):
    label(ax, 0.3, 6.2, "\"환불\"이 한 번 나온 문서 셋 (평균이 네 낱말이라고 할게요)", fs=11, ha="left", color=INK)
    label(ax, 10.8, 5.45, "횟수 몫", fs=10.5, color=INK)
    xa = 1.95 + 4 * (WW + 0.06) - 0.03
    ax.plot([xa, xa], [1.5, 5.25], color=GREY, lw=1.4, ls="--")
    label(ax, xa, 5.45, "평균 길이", fs=10, color=INK)
    for k, (name, words, v) in enumerate(DOCS):
        y = 4.35 - k * 1.25
        label(ax, 0.3, y + 0.3, name, fs=10, ha="left", color=INK)
        cells(ax, 1.95, y, words, w=WW, h=0.6, gap=0.06, fs=10)
        on = k + 1 == step
        if k + 1 <= step:
            label(ax, 10.8, y + 0.3, v, fs=14, color=RED if on else "#222", bold=on)
        else:
            empty(ax, 10.25, y, 1.1, 0.6, "?", fs=12)
    if step == 3:
        moral(ax, 6.0, 0.6, "같은 한 번이라도 짧은 문서의 몫이 커요")


# ── 통계는 샤드마다 따로예요 ───────────────────────────────────────
SHARDS = [("샤드 A", "환불 언제 돼요", "0.014", "41개 중 41개"), ("샤드 B", "상품 문의 드려요", "3.848", "41개 중 1개")]


def shards(ax, step):
    for k, (name, filler, score, n) in enumerate(SHARDS):
        x = 0.3 + k * 5.9
        box(ax, x, 2.45, 5.4, 3.85, fc=NOTE)
        label(ax, x + 0.2, 5.95, name, fs=11, ha="left", bold=True)
        cell(ax, x + 0.25, 4.85, 2.4, 0.65, "환불 문의", fs=11.5)
        for j in range(2):
            cell(ax, x + 0.25, 3.95 - j * 0.6, 2.4, 0.5, filler, fs=9.5)
        label(ax, x + 1.45, 2.8, "⋯ 모두 40개", fs=10, color=INK)
        if step == 1:
            empty(ax, x + 3.1, 4.85, 2.05, 0.65, "점수 ?", fs=11)
        elif step == 2:
            box(ax, x + 3.1, 4.85, 2.05, 0.65, fc=PINK, ec=RED, lw=1.6)
            label(ax, x + 4.12, 5.17, score, fs=14, color=RED, bold=True)
            label(ax, x + 4.12, 4.15, "\"환불\"이 든 문서", fs=9.5, color=RED)
            label(ax, x + 4.12, 3.7, n, fs=10.5, color=RED, bold=True)
        else:
            box(ax, x + 3.1, 4.85, 2.05, 0.65, fc=PINK, ec=RED, lw=1.6)
            label(ax, x + 4.12, 5.17, "② 0.773", fs=14, color=RED, bold=True)
    if step == 1:
        label(ax, 6.0, 1.6, "똑같은 글 \"환불 문의\"를 샤드마다 하나씩 넣었어요", fs=11, color=INK)
        label(ax, 6.0, 0.95, "\"환불\"로 검색하면 두 글의 점수는?", fs=11, color=INK)
    elif step == 2:
        moral(ax, 6.0, 1.3, "똑같은 글인데 샤드마다 점수가 달라요")
        label(ax, 6.0, 0.6, "샤드마다 자기 문서로만 '환불이 드문가'를 세요", fs=10.5, color=INK)
    else:
        box(ax, 3.2, 0.95, 5.6, 0.95, fc=PINK, ec=RED, lw=1.6)
        label(ax, 6.0, 1.42, "① 통계를 먼저 모아요: \"환불\" 42개 / 82개", fs=11, color=RED, bold=True)
        arrow(ax, (3.0, 2.4), (4.3, 1.95), color=RED, ms=13)
        arrow(ax, (9.0, 2.4), (7.7, 1.95), color=RED, ms=13)
        moral(ax, 6.0, 0.35, "dfs_query_then_fetch: 두 글이 같은 점수를 받아요", fs=12)


# ── 정확한 순위 테스트는 언제 ──────────────────────────────────────
def decide():
    fig, ax = canvas(10, 3.6, 15, 5.4)
    box(ax, 0.3, 3.6, 6.0, 1.3, fc=NOTE)
    label(ax, 3.3, 4.25, "테스트가 정확한 1위를\n확인해야 하나요?", fs=10.5, bold=True)
    arrow(ax, (6.4, 4.25), (8.4, 4.25), color=RED)
    label(ax, 7.4, 4.55, "아니요", fs=10, color=RED)
    box(ax, 8.5, 3.6, 6.2, 1.3, fc=PINK, ec=RED)
    label(ax, 11.6, 4.25, "꼭 나올 문서는 상위 몇 개 안에,\n나오면 안 될 문서는 없는지로 판정해요", fs=10, color=RED, bold=True)
    arrow(ax, (3.3, 3.5), (3.3, 2.6))
    label(ax, 3.6, 3.05, "예", fs=10, color=INK, ha="left")
    box(ax, 0.3, 1.3, 6.0, 1.2, fc=PAPER)
    label(ax, 3.3, 1.9, "운영과 비슷한 크기의 문서 모음에서\n샤드 1개나 dfs_query_then_fetch로", fs=10)
    save(fig, OUT, "es08-decide.svg")


# ── 정리: 낱말 카드 ────────────────────────────────────────────────
def cards():
    fig, ax = canvas(6.4, 7.9, 9.8, 12.2)
    W, H = 4.6, 3.8

    def card(i, name, line):
        col, row = i % 2, i // 2
        x, y = 0.2 + col * 4.9, 8.2 - row * 4.05
        box(ax, x, y, W, H, fc="white")
        label(ax, x + 0.25, y + H - 0.4, name, fs=12.5, ha="left", bold=True)
        label(ax, x + W / 2, y + 0.6, line, fs=10, color=INK)
        return x, y

    x, y = card(0, "BM25", "ES의 기본 점수 공식,\n낱말마다 곱해서 더해요")
    cell(ax, x + 0.3, y + 1.85, 1.55, 0.55, "환불 0.687", hot=True, fs=9.5)
    label(ax, x + 2.05, y + 2.12, "+", fs=12, color=RED, bold=True)
    cell(ax, x + 2.3, y + 1.85, 1.1, 0.55, "배송 0", hot=True, fs=9.5)
    label(ax, x + 3.6, y + 2.12, "=", fs=12, color=INK)
    label(ax, x + 4.1, y + 2.12, "0.687", fs=9.5, color=RED, bold=True)
    x, y = card(1, "횟수 몫 (tf)", "많이 나올수록 오르지만\n1을 넘지 않는 몫")
    ax.plot([x + 0.4, x + 4.2], [y + 2.7, y + 2.7], color=GREY, lw=1.0, ls="--")
    for k, f in enumerate(FS):
        h = 1.3 * f / (f + K1)
        ax.add_patch(Rectangle((x + 0.55 + k * 0.75, y + 1.4), 0.5, h, fc=PINK, ec=RED, lw=1.2))
    x, y = card(2, "IDF", "낱말이 든 문서가 적을수록\n커지는 무게")
    for i in range(16):
        cx, cy = x + 0.55 + (i % 8) * 0.45, y + 2.25 - (i // 8) * 0.45
        ax.add_patch(Rectangle((cx, cy), 0.35, 0.35, fc=PINK if i == 0 else NOTE, ec=RED if i == 0 else INK,
                               lw=1.4 if i == 0 else 0.7))
    x, y = card(3, "k1 (기본 1.2)", "횟수가 늘 때 몫이 얼마나\n더 오를지 정하는 값")
    label(ax, x + 4.4, y + 3.4, "한 번일 때를 1로", fs=8.5, color=INK, ha="right")
    for k, f in enumerate(FS):
        for kk, kv in enumerate((K1, 3.0)):
            h = 0.4 * (f / (f + kv)) / (1 / (1 + kv))
            ax.add_patch(Rectangle((x + 0.5 + k * 0.75 + kk * 0.3, y + 1.4), 0.28, h,
                                   fc=PINK if kk == 0 else LIGHT, ec=RED if kk == 0 else GREY, lw=1.0))
    xl = x + 0.5 + 4 * 0.75
    label(ax, xl + 0.29, y + 1.4 + 0.4 * 2.075 + 0.15, "2.1배", fs=7.5, color=RED, ha="right")
    label(ax, xl + 0.44, y + 1.4 + 0.4 * 3.478 + 0.15, "3.5배", fs=8, color=INK)
    label(ax, x + 0.64, y + 1.22, "1.2", fs=8, color=RED)
    label(ax, x + 0.94, y + 1.22, "3", fs=8, color=INK)
    x, y = card(4, "b (기본 0.75)", "문서 길이를 얼마나\n반영할지 정하는 값")
    cells(ax, x + 0.4, y + 2.25, ["환불", "문의"], w=0.7, h=0.45, gap=0.05, hot=(0,), fs=9)
    label(ax, x + 3.9, y + 2.47, "0.57", fs=10, color=RED, bold=True)
    cells(ax, x + 0.4, y + 1.6, [""] * 8, w=0.33, h=0.45, gap=0.04, hot=(2,), fs=8)
    label(ax, x + 3.9, y + 1.82, "0.32", fs=10, color=RED, bold=True)
    x, y = card(5, "dfs_query_then_fetch", "샤드 통계를 먼저 모아\n점수를 매기는 검색")
    for k in range(2):
        box(ax, x + 0.4 + k * 2.6, y + 2.3, 1.2, 0.5, fc=NOTE, lw=1.0)
        label(ax, x + 1.0 + k * 2.6, y + 2.55, "샤드 " + "AB"[k], fs=9)
    arrow(ax, (x + 1.2, y + 2.2), (x + 1.9, y + 1.85), color=RED, ms=9, lw=1.3)
    arrow(ax, (x + 3.4, y + 2.2), (x + 2.7, y + 1.85), color=RED, ms=9, lw=1.3)
    box(ax, x + 1.6, y + 1.35, 1.4, 0.45, fc=PINK, ec=RED, lw=1.3)
    label(ax, x + 2.3, y + 1.57, "통계", fs=9, color=RED)
    save(fig, OUT, "es08-cards.svg")


if __name__ == "__main__":
    S, L = (7.2, 3.8), (12, 6.6)
    stage(opening, 3, OUT, "es08-open", S, L)
    stage(sum_, 3, OUT, "es08-sum", S, L)
    stage(tfbars, 2, OUT, "es08-tf", S, L)
    stage(grid, 2, OUT, "es08-idf", S, L)
    stage(length, 3, OUT, "es08-len", S, L)
    stage(shards, 3, OUT, "es08-shards", S, L)
    decide()
    stage(back, 2, OUT, "es08-back", S, L)
    cards()
