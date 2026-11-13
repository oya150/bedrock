"""Elasticsearch 8편 그림 만들기. 실행: python lab/fig_es08.py  → docs/elasticsearch/img/08/*.svg

새 정책(2026-11-13): 그림 8장, 그림 안에는 낱말·숫자만 둔다. 지금 볼 곳만 빨강.
예시는 검색어 "환불 배송"과 두 문서 "환불 환불 문의", "배송 지연 문의"를 편 끝까지 잇는다
(.claude/writing/work/cal/units-es08.md). 개발 서버와 다른 서버 모두 문서 52개.
"""
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "es"))
from figkit import (GREY, INK, NOTE, PINK, RED, arrow, box, canvas, cell, cells, label, magnifier,  # noqa: E402
                    outdir, save)
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


# ── 여는 그림: 두 서버를 나란히 ───────────────────────────────────
SERVERS = [("개발 서버", [A_DOC, B_DOC], "배송 언제 와요"), ("다른 서버", [B_DOC, A_DOC], "환불 언제 돼요")]


def opening():
    fig, ax = canvas(7.2, 3.9, 12, 6.5)
    for k, (name, rows, filler) in enumerate(SERVERS):
        x = 0.2 + k * 6.0
        hot = k == 1
        box(ax, x, 0.3, 5.6, 5.9, fc="white")
        label(ax, x + 2.8, 5.8, name, fs=12.5, bold=True)
        ax.add_patch(Rectangle((x + 0.3, 4.75), 5.0, 0.55, fc="white", ec=INK, lw=1.2))
        magnifier(ax, x + 0.55, 5.03)
        label(ax, x + 0.85, 5.02, "환불 배송", fs=11.5, ha="left")
        for j, t in enumerate(rows):
            y = 4.05 - j * 0.65
            c = RED if hot else "#222"
            label(ax, x + 0.6, y, f"{j + 1}위", fs=11, color=c, bold=hot)
            label(ax, x + 1.2, y, t, fs=11.5, ha="left", color=c, bold=hot)
        ax.plot([x + 0.3, x + 5.3], [2.95, 2.95], color=GREY, lw=1.0)
        label(ax, x + 2.8, 2.6, "함께 든 문서", fs=10, color=INK)
        cell(ax, x + 0.4, 1.55, 4.8, 0.6, f"{filler} ×30", hot=hot, fs=11)
        cell(ax, x + 0.4, 0.75, 4.8, 0.6, "상품 문의 ×20", fs=11)
    save(fig, OUT, "es08-open.svg")


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
    for x, t in ((2.9, "고정값"), (5.0, "드문 정도\n(IDF)"), (7.3, "횟수 몫\n(tf)"), (9.5, "'환불' 점수")):
        label(ax, x, 3.4, t, fs=9.5, color=c)
    if step == 2:
        empty(ax, 2.4, 2.2, 9.2, 0.7, "?", fs=13)
        return
    label(ax, 2.5, 2.55, "없음  →  0", fs=12.5, ha="left", color=RED, bold=True)
    ax.plot([0.3, 11.6], [1.75, 1.75], color=INK, lw=1.0)
    label(ax, 0.3, 1.25, "문서 점수", fs=11, ha="left", bold=True)
    label(ax, 2.5, 1.25, "0.6870  +  0  =  0.6870", fs=12.5, ha="left", color=RED, bold=True)


# ── 많이 나올수록 높지만 금방 배불러요 ─────────────────────────────
FS = [1, 2, 5, 10, 20]
BX = [1.6 + k * 2.0 for k in range(5)]
Y0, TOP = 1.5, 3.8


def tfbars(ax, step):
    label(ax, 0.3, 6.2, "\"환불\"이 나온 횟수 · 문서 길이 평균", fs=11, ha="left", color=INK)
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
    label(ax, 3.0, 5.65, "횟수 몫", fs=11.5, color=RED, bold=True)


# ── 드문 낱말일수록 무거워요 ───────────────────────────────────────
GCOLS, GW, GH = 13, 0.56, 0.5


def grid(ax, step):
    server = "개발 서버" if step == 1 else "다른 서버"
    label(ax, 0.3, 6.2, f"{server} · 문서 52개", fs=11, ha="left", color=INK)
    n = 1 if step == 1 else 31
    for i in range(52):
        cx = 0.3 + (i % GCOLS) * (GW + 0.08)
        cy = 4.9 - (i // GCOLS) * (GH + 0.1)
        on = i < n
        ax.add_patch(Rectangle((cx, cy), GW, GH, fc=PINK if on else NOTE, ec=RED if on else INK, lw=1.6 if on else 0.8))
    label(ax, 4.45, 2.35, "빨간 칸: \"환불\"이 든 문서", fs=10.5, color=RED)
    x = 10.2
    label(ax, x, 5.2, "\"환불\"이 든 문서", fs=11, color=INK)
    label(ax, x, 4.5, f"{n}개 / 52개", fs=13, color=RED, bold=True)
    label(ax, x, 3.6, "드문 정도 (IDF)", fs=11, color=INK)
    label(ax, x, 2.9, f"{idf(52, n):.2f}", fs=17, color=RED, bold=True)


# ── 짧은 문서가 유리해요 ───────────────────────────────────────────
DOCS = [("평균 길이", ["환불", "문의", "드려요", "급해요"], "0.45"),
        ("평균의 절반", ["환불", "문의"], "0.57"),
        ("평균의 두 배", ["배송", "교환", "환불", "기간", "안내", "꼭", "읽어", "주세요"], "0.32")]
WW = 0.98


def length(ax, step):
    label(ax, 0.3, 6.2, "\"환불\" 한 번 · 평균 4낱말", fs=11, ha="left", color=INK)
    label(ax, 10.8, 5.45, "횟수 몫", fs=10.5, color=INK)
    xa = 1.95 + 4 * (WW + 0.06) - 0.03
    ax.plot([xa, xa], [1.5, 5.25], color=GREY, lw=1.4, ls="--")
    label(ax, xa, 5.45, "평균 길이", fs=10, color=INK)
    for k, (name, words, v) in enumerate(DOCS):
        y = 4.35 - k * 1.25
        label(ax, 0.3, y + 0.3, name, fs=10, ha="left", color=INK)
        cells(ax, 1.95, y, words, w=WW, h=0.6, gap=0.06, fs=10)
        on = (k + 1 == step) or (step == 4 and k != 0)
        if k + 1 <= step:
            label(ax, 10.8, y + 0.3, v, fs=14, color=RED if on else "#222", bold=on)
        else:
            empty(ax, 10.25, y, 1.1, 0.6, "?", fs=12)


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
        label(ax, x + 1.45, 2.8, "⋯ 40개", fs=10, color=INK)
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
    if step == 3:
        box(ax, 3.2, 0.95, 5.6, 0.95, fc=PINK, ec=RED, lw=1.6)
        label(ax, 6.0, 1.42, "① 통계 합치기: \"환불\" 42개 / 82개", fs=11, color=RED, bold=True)
        arrow(ax, (3.0, 2.4), (4.3, 1.95), color=RED, ms=13)
        arrow(ax, (9.0, 2.4), (7.7, 1.95), color=RED, ms=13)
        label(ax, 6.0, 0.4, "dfs_query_then_fetch", fs=12, color=RED, bold=True)


def one(draw, step, name, ylo=0.0):
    """장면 하나만 그린다. ylo 아래 빈 곳은 잘라 낸다."""
    w, h, xmax, ymax = 7.2, 3.8, 12, 6.6
    fig, ax = canvas(w, h * (ymax - ylo) / ymax, xmax, ymax)
    ax.set_ylim(ylo, ymax)
    draw(ax, step)
    save(fig, OUT, name)


if __name__ == "__main__":
    opening()
    one(sum_, 3, "es08-sum.svg", ylo=0.8)
    one(tfbars, 2, "es08-tf.svg", ylo=0.9)
    one(length, 4, "es08-len.svg", ylo=1.4)
    one(grid, 1, "es08-idf-1.svg", ylo=2.0)
    one(grid, 2, "es08-idf-2.svg", ylo=2.0)
    one(shards, 2, "es08-shards-1.svg", ylo=2.2)
    one(shards, 3, "es08-shards-2.svg")
