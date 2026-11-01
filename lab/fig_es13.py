"""Elasticsearch 13편 그림 만들기. 실행: python lab/fig_es13.py  → docs/elasticsearch/img/13/*.svg

본문 절은 장면 띠로 그린다: 같은 무대를 여러 장 그리고 장마다 바뀐 곳만 빨강으로 칠한다.
예시는 방문 대시보드의 "오늘 방문자" 94,707명과 사용자 u-1~u-40을 편 끝까지 잇는다(.claude/writing/work/cal/units-es13.md).
해시 비트와 통 값은 lab/es/13_hll.py 와 같은 해시(blake2b 64비트)로 여기서 직접 계산한다.
"""
import hashlib
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "es"))
from figkit import (GREY, INK, LIGHT, NOTE, PAPER, PINK, RED, arrow, box, bubble, canvas,  # noqa: E402
                    cell, cells, cylinder, label, moral, outdir, save, stage)
from matplotlib.patches import Circle, FancyBboxPatch, Rectangle  # noqa: E402

OUT = outdir("13")


# ── 계산: 해시 비트, 앞 0 줄, 통 배열 ─────────────────────────────
def h64(x):
    return int.from_bytes(hashlib.blake2b(x.encode(), digest_size=8).digest(), "big")


def hbits(x):
    return format(h64(x), "064b")


def lead0(s):
    return len(s) - len(s.lstrip("0"))


def regs(ids, p=3):
    """앞 p비트로 통을 고르고 통마다 나머지 비트의 가장 긴 앞 0 줄을 적는다."""
    reg = [0] * (1 << p)
    for u in ids:
        b = hbits(u)
        i = int(b[:p], 2)
        reg[i] = max(reg[i], lead0(b[p:]))
    return reg


def estimate(reg):
    """lab/es/13_hll.py 와 같은 식. 통에는 0 줄 길이 + 1 을 넣어 계산한다."""
    m = len(reg)
    alpha = 0.7213 / (1 + 1.079 / m)
    return alpha * m * m / sum(2.0 ** -(z + 1) for z in reg)


USERS = [f"u-{i}" for i in range(1, 41)]
SHARD_A = USERS[:20]
SHARD_B = ["u-13"] + USERS[20:]
ALL, REG_A, REG_B = regs(USERS), regs(SHARD_A), regs(SHARD_B)
EST = estimate(ALL)
ZROWS = ["u-10", "u-11", "u-12", "u-13"]
assert [lead0(hbits(u)) for u in ZROWS + ["u-21"]] == [1, 0, 1, 3, 6]
assert hbits("u-34")[:10] == "0110000101" and lead0(hbits("u-34")[3:]) == 4
assert ALL == [3, 5, 2, 4, 1, 2, 4, 1] == [max(a, b) for a, b in zip(REG_A, REG_B)]
assert REG_A == [2, 5, 0, 1, 1, 2, 4, 1] and REG_B == [3, 4, 2, 4, 1, 2, 2, 0]
assert round(EST) == 46


def empty(ax, x, y, w, h, s="", fs=10):
    ax.add_patch(Rectangle((x, y), w, h, fc="white", ec=GREY, lw=1.0, ls="--"))
    if s:
        label(ax, x + w / 2, y + h / 2, s, fs=fs, color=GREY)


# ── 여는 장면·돌아오는 장면: 방문 대시보드 ──────────────────────────
CYL = (8.5, 4.0, 2.8, 1.3)
SAY = (6.9, 1.0, 4.9, 1.75)
TAIL = (9.9, 3.75)


def dash(ax, n, hot=False, note=None):
    box(ax, 0.4, 3.2, 6.2, 3.1, fc="white", round_=False)
    ax.add_patch(Rectangle((0.4, 5.85), 6.2, 0.45, fc=LIGHT, ec=INK, lw=1.2))
    label(ax, 0.6, 6.07, "방문 대시보드", fs=11, ha="left", color=INK)
    box(ax, 0.85, 3.5, 5.3, 2.05, fc=PAPER)
    label(ax, 1.1, 5.2, "오늘 방문자", fs=11.5, ha="left", color=INK)
    label(ax, 3.5, 4.4, f"{n}명", fs=22, bold=True, color=RED if hot else "#222")
    if note:
        label(ax, 3.5, 3.8, note, fs=10, color=RED if hot else INK)


def logpaper(ax, count=None, hot=False):
    box(ax, 0.4, 0.75, 6.2, 2.15, fc="white", round_=False)
    label(ax, 0.6, 2.6, "방문 기록 로그 (30만 줄)", fs=11, ha="left", color=INK)
    for k, t in enumerate(["u-10  방문", "u-13  방문", "u-10  방문", "⋮"]):
        label(ax, 0.8, 2.15 - k * 0.38, t, fs=10.5, ha="left", color="#222" if t != "⋮" else INK)
    if count:
        c = RED if hot else "#222"
        label(ax, 4.6, 1.95, "직접 세면", fs=11, color=c)
        label(ax, 4.6, 1.35, f"{count}명", fs=17, color=c, bold=True)


def es(ax):
    cylinder(ax, *CYL, "ES")


def opening(ax, step):
    es(ax)
    bubble(ax, *SAY, "방문 기록 30만 건에서\n서로 다른 사용자를\n셌어요", TAIL)
    if step == 1:
        dash(ax, "94,707", hot=True)
        logpaper(ax)
    else:
        dash(ax, "94,707")
        logpaper(ax, "95,062", hot=True)
        moral(ax, 6.0, 0.3, "집계가 로그보다 355명 적어요")


def back(ax, step):
    es(ax)
    logpaper(ax, "95,062")
    if step == 1:
        dash(ax, "94,707")
        bubble(ax, *SAY, "처음엔 로그보다\n355명 적었어요", TAIL)
    elif step == 2:
        dash(ax, "94,707")
        bubble(ax, *SAY, "통 16,384개(16 KB)에\n가장 긴 0 줄만 적어\n어림했어요", TAIL, hot=True)
    else:
        dash(ax, "95,086", hot=True, note="precision_threshold 40,000")
        bubble(ax, *SAY, "통을 262,144개로\n늘리니 24명 차이예요", TAIL, hot=True)
        moral(ax, 6.0, 0.3, "적은 메모리로 어림하고 통 수로 정확도를 골라요")


# ── 정확히 세기: 본 ID 목록 ────────────────────────────────────────
LX, LW = 2.9, 1.1
SEEN_TAIL = (9.4, 1.5)


def seen(ax, step):
    label(ax, 0.3, 6.15, "들어온 방문 기록", fs=11, ha="left", color=INK)
    label(ax, LX, 6.15, "ES가 기억하는 본 ID 목록", fs=11, ha="left", color=INK)
    cylinder(ax, 9.5, 0.8, 2.1, 1.0, "ES")
    ids = ["u-10", "u-11", "u-12"]
    if step == 1:
        cell(ax, 0.4, 5.0, 1.6, 0.7, "u-12", hot=True)
        cells(ax, LX, 5.0, ids, w=LW, h=0.7, hot=(2,), fs=11)
        arrow(ax, (1.2, 4.95), (LX + 2 * 1.18 + 0.5, 4.95), color=RED, rad=0.3, ms=14)
        bubble(ax, 3.4, 2.1, 5.6, 1.5, "u-12는 본 적 있어요.\n그대로 둬요", SEEN_TAIL, hot=True)
    elif step == 2:
        cell(ax, 0.4, 5.0, 1.6, 0.7, "u-13", hot=True)
        cells(ax, LX, 5.0, ids + ["u-13"], w=LW, h=0.7, hot=(3,), fs=11)
        arrow(ax, (1.2, 4.95), (LX + 3 * 1.18 + 0.5, 4.95), color=RED, rad=0.3, ms=14)
        bubble(ax, 3.4, 2.1, 5.6, 1.5, "u-13은 처음이에요.\n목록에 더해요", SEEN_TAIL, hot=True)
    else:
        label(ax, 1.2, 5.35, "⋮", fs=13, color=INK)
        end = cells(ax, LX, 5.0, ids + ["u-13", "⋯"], w=LW, h=0.7, fs=11)
        cell(ax, end + 0.1, 5.0, 1.6, 0.7, "100만 번째", hot=True, fs=10.5)
        label(ax, LX, 4.4, "칸 하나에 40바이트만 잡아도 100만 칸이면 40 MB", fs=11, ha="left", color=RED)
        bubble(ax, 3.4, 2.1, 5.6, 1.5, "사용자가 100만 명이면\n목록도 100만 칸이에요", SEEN_TAIL, hot=True)
        moral(ax, 6.0, 0.55, "정확히 세려면 본 ID를 모두 기억해야 해요")


# ── 정확히 세기: 샤드마다 목록을 보내요 ────────────────────────────
def shardbox(ax, x, name, items, hot, n):
    box(ax, x, 3.9, 5.4, 2.2, fc=NOTE)
    label(ax, x + 0.2, 5.75, name, fs=11.5, ha="left", bold=True)
    label(ax, x + 5.2, 5.75, f"{n}명", fs=11, ha="right", color=INK)
    cells(ax, x + 0.2, 4.2, items, w=0.95, h=0.7, gap=0.06, hot=hot, fs=10.5)


def ship(ax, step):
    hot = step == 1
    shardbox(ax, 0.3, "샤드 A", ["u-1", "⋯", "u-13", "⋯", "u-20"], (2,) if hot else (), 20)
    shardbox(ax, 6.2, "샤드 B", ["u-13", "u-21", "⋯", "u-39", "u-40"], (0,) if hot else (), 21)
    cylinder(ax, 4.9, 1.3, 2.2, 0.9, "조율 노드")
    if step == 1:
        bubble(ax, 7.6, 0.3, 4.1, 1.4, "센 수를 더하면 41명.\nu-13을 두 번 세요", (7.2, 2.0), hot=True)
    else:
        arrow(ax, (2.8, 3.85), (4.75, 2.7), color=RED, ms=14)
        arrow(ax, (9.2, 3.85), (7.25, 2.7), color=RED, ms=14)
        label(ax, 2.7, 3.15, "ID 목록 통째로", fs=10.5, color=RED)
        label(ax, 9.4, 3.15, "ID 목록 통째로", fs=10.5, color=RED)
        bubble(ax, 7.6, 0.3, 4.1, 1.4, "겹친 u-13을 지우니\n40명이에요", (7.2, 2.0), hot=True)
        moral(ax, 3.0, 0.45, "샤드마다 ID 목록을\n통째로 보내야 해요", fs=12)


# ── 해시 앞의 0 줄 ─────────────────────────────────────────────────
ZY = [5.45, 4.7, 3.95, 3.2, 2.45, 1.7]
BX, BW = 2.2, 0.5


def bitrow(ax, y, u, b, hot_zero=False, row_hot=False, note=True, whole=False):
    z = lead0(b)
    label(ax, 0.35, y + 0.3, u, fs=11, ha="left", color=RED if row_hot else "#222", bold=row_hot)
    arrow(ax, (1.25, y + 0.3), (BX - 0.1, y + 0.3), color=GREY, ms=10, lw=1.4)
    for i, ch in enumerate(b[:8]):
        cell(ax, BX + i * BW, y, BW - 0.04, 0.6, ch, hot=whole or ((hot_zero or row_hot) and i < z), fs=10.5)
    label(ax, BX + 8 * BW + 0.15, y + 0.3, "…", fs=11, color=INK)
    if note:
        label(ax, 7.0, y + 0.3, f"앞 0 {z}개" if z else "앞 0 없음", fs=10.5, ha="left", color=RED if row_hot else INK)


def memo(ax, n, est, hot=False, extra=None):
    box(ax, 8.6, 2.5, 3.1, 3.4, fc=PAPER, ec=RED if hot else INK)
    label(ax, 10.15, 5.5, "가장 긴 0 줄", fs=11, color=INK)
    label(ax, 10.15, 4.55, str(n), fs=26, bold=True, color=RED if hot else ("#222" if n != "?" else GREY))
    if est:
        label(ax, 10.15, 3.5, est, fs=10.5, color=RED if hot else INK)
    if extra:
        label(ax, 10.15, 2.9, extra, fs=10.5, color=RED if hot else INK)


def zeros(ax, step):
    label(ax, BX, 6.4, "ID를 해시한 비트", fs=11, ha="left", color=INK)
    for k, u in enumerate(ZROWS):
        bitrow(ax, ZY[k], u, hbits(u), hot_zero=step == 2, note=step >= 2)
    if step == 1:
        for k in range(4):
            arrow(ax, (1.25, ZY[k] + 0.3), (BX - 0.1, ZY[k] + 0.3), color=RED, ms=10, lw=1.6)
        memo(ax, "?", None)
    elif step == 2:
        memo(ax, 3, "1/8 → 대략 8명", hot=True)
    elif step == 3:
        bitrow(ax, ZY[4], "u-12", hbits("u-12"), row_hot=True, whole=True)
        label(ax, 7.0, ZY[4] - 0.15, "또 왔어요. 비트가 같아요", fs=10, ha="left", color=RED)
        memo(ax, 3, "1/8 → 대략 8명", extra="그대로")
    else:
        bitrow(ax, ZY[4], "u-12", hbits("u-12"))
        bitrow(ax, ZY[5], "u-21", hbits("u-21"), row_hot=True)
        memo(ax, 6, "1/64 → 대략 64명", hot=True, extra="실제는 5명")
        moral(ax, 6.0, 0.6, "가장 긴 줄 하나에 기대면 운이 크게 껴요")


# ── 통 여러 개 ─────────────────────────────────────────────────────
TX, TW = 1.6, 1.12


def tongs(ax, vals, hot=(), y=2.6):
    label(ax, 0.3, y + 0.35, "통 8개", fs=11, ha="left", bold=True)
    for i in range(8):
        x = TX + i * (TW + 0.1)
        label(ax, x + TW / 2, y - 0.3, f"{i}번", fs=10, color=RED if i in hot else INK)
        if vals[i] is None:
            empty(ax, x, y, TW, 0.7)
        else:
            cell(ax, x, y, TW, 0.7, vals[i], hot=i in hot, fs=12)


def buckets(ax, step):
    b = hbits("u-34")[:10]
    label(ax, 0.3, 5.6, "u-34", fs=11.5, ha="left", bold=True)
    x0 = 1.5
    hot1 = step == 1
    for i, ch in enumerate(b):
        x = x0 + i * 0.55 + (0.3 if i >= 3 else 0)
        cell(ax, x, 5.3, 0.5, 0.6, ch, hot=hot1 and (i < 3 or 3 <= i < 7), fs=11)
    label(ax, x0 + 10 * 0.55 + 0.45, 5.6, "…", fs=11, color=INK)
    label(ax, x0 + 0.8, 4.85, "앞 3비트 = 통 번호", fs=10, color=RED if hot1 else INK)
    label(ax, x0 + 3.95, 4.85, "나머지의 앞 0 줄", fs=10, color=RED if hot1 else INK)
    label(ax, x0 + 0.8, 4.45, "011 → 3번", fs=10, color=RED if hot1 else INK)
    label(ax, x0 + 3.95, 4.45, "0이 4개", fs=10, color=RED if hot1 else INK)
    if step == 1:
        tongs(ax, [None, None, None, 4, None, None, None, None], hot=(3,))
        arrow(ax, (x0 + 3.95, 4.2), (TX + 3 * (TW + 0.1) + TW / 2, 3.4), color=RED, ms=14)
    else:
        tongs(ax, ALL, hot=range(8) if step == 2 else ())
        label(ax, 11.7, 4.45, "u-1 ~ u-40, 40명", fs=10.5, ha="right", color=RED if step == 2 else INK)
    if step == 3:
        label(ax, 6.0, 1.55, f"통마다 어림해 조화평균으로 모으면 대략 {round(EST)}명 (실제 40명)", fs=11.5, color=RED, bold=True)
        moral(ax, 6.0, 0.75, "통 여러 개를 평균하면 운이 덜 껴요")


# ── 샤드끼리 합치기 ────────────────────────────────────────────────
MX, MW = 2.6, 1.0


def mrow(ax, y, name, vals, hot=False, dashed=False):
    label(ax, 0.3, y + 0.35, name, fs=11.5, ha="left", bold=True, color=RED if hot else "#222")
    for i in range(8):
        x = MX + i * (MW + 0.12)
        if dashed:
            empty(ax, x, y, MW, 0.7)
        else:
            cell(ax, x, y, MW, 0.7, vals[i], hot=hot, fs=12)


def merge(ax, step):
    for i in range(8):
        label(ax, MX + i * (MW + 0.12) + MW / 2, 6.05, f"{i}번", fs=10, color=INK)
    mrow(ax, 5.0, "샤드 A", REG_A)
    mrow(ax, 1.3, "샤드 B", REG_B)
    if step == 1:
        mrow(ax, 3.15, "조율 노드", None, dashed=True)
        label(ax, 0.3, 2.8, "통 배열만 받아요", fs=10, ha="left", color=INK)
    else:
        mrow(ax, 3.15, "조율 노드", ALL, hot=True)
        for i in range(8):
            x = MX + i * (MW + 0.12) + MW / 2
            if REG_A[i] >= REG_B[i]:
                arrow(ax, (x, 4.95), (x, 3.9), color=RED, ms=10, lw=1.5)
            if REG_B[i] >= REG_A[i]:
                arrow(ax, (x, 2.05), (x, 3.1), color=RED, ms=10, lw=1.5)
        label(ax, 0.3, 2.8, "칸마다 큰 값", fs=10, ha="left", color=RED)
        moral(ax, 6.0, 0.45, "칸마다 큰 값만 고르면 합쳐져요")


# ── 백분위: t-digest ───────────────────────────────────────────────
AX0, AX1, AY = 0.7, 11.3, 3.9
DELTA = 28
QB = [(1 - math.cos(math.pi * j / DELTA * 2)) / 2 for j in range(DELTA // 2 + 1)]


def qx(q):
    return AX0 + q * (AX1 - AX0)


def tdigest(ax, step):
    label(ax, 0.3, 5.65, "응답 시간 30만 건을 빠른 순으로 줄 세웠어요", fs=11.5, ha="left", bold=True)
    ax.plot([AX0, AX1], [AY, AY], color=INK, lw=1.4)
    for q, t in [(0, "0%"), (0.5, "50%\n54.5 ms"), (1, "100%")]:
        ax.plot([qx(q), qx(q)], [AY - 0.08, AY + 0.08], color=INK, lw=1.2)
        label(ax, qx(q), AY - 0.45, t, fs=10, color=INK)
    if step == 1:
        for k in range(141):
            ax.add_patch(Circle((qx(k / 140), 4.4), 0.045, fc=INK, ec="none"))
        label(ax, 6.0, 2.55, "점 하나가 요청 하나예요. 정확히 구하려면 30만 개를 다 들고 줄 세워요", fs=10.5, color=INK)
    else:
        hot = step == 2
        for a, b in zip(QB, QB[1:]):
            x, w = qx(a) + 0.025, qx(b) - qx(a) - 0.05
            ax.add_patch(FancyBboxPatch((x, 4.18), w, 0.44, boxstyle=f"round,pad=0,rounding_size={min(0.2, w / 2):.3f}",
                                        fc=PINK if hot else NOTE, ec=RED if hot else INK, lw=1.4))
        if hot:
            label(ax, 6.0, 2.55, "가운데는 큰 묶음, 양 끝은 작은 묶음. 묶음마다 평균값과 개수만 남겨요", fs=10.5, color=RED)
        else:
            ax.plot([qx(0.99), qx(0.99)], [4.85, AY - 0.15], color=RED, lw=2.2)
            label(ax, qx(0.99), 5.1, "99%", fs=10.5, color=RED, bold=True)
            label(ax, 11.7, 2.55, "99% 자리는 작은 묶음 안이라 350.9 ms 가까이 읽어요", fs=10.5, ha="right", color=RED)
            moral(ax, 6.0, 1.3, "꼬리는 작은 묶음으로 촘촘히 남겨요")


# ── 판단: 언제 쓸모 있을까요 ──────────────────────────────────────
def decide():
    fig, ax = canvas(10, 3.6, 15, 5.4)
    box(ax, 0.3, 3.6, 6.0, 1.3, fc=NOTE)
    label(ax, 3.3, 4.25, "한 명 차이가 돈 계산에 걸리나요?", fs=10.5, bold=True)
    arrow(ax, (6.4, 4.25), (8.4, 4.25), color=RED)
    label(ax, 7.4, 4.55, "예", fs=10, color=RED)
    box(ax, 8.5, 3.6, 6.2, 1.3, fc=PINK, ec=RED)
    label(ax, 11.6, 4.25, "정확히 센 값을 써요\n(composite 집계, 원본 로그 배치)", fs=10.5, color=RED, bold=True)
    arrow(ax, (3.3, 3.5), (3.3, 2.6))
    label(ax, 3.6, 3.05, "아니요", fs=10, color=INK, ha="left")
    box(ax, 0.3, 1.3, 6.0, 1.2, fc=PAPER)
    label(ax, 3.3, 1.9, "cardinality 근삿값을 써요\n(대시보드처럼 1% 안팎 오차가 괜찮은 곳)", fs=10)
    box(ax, 8.5, 1.3, 6.2, 1.2, fc=LIGHT, ec=GREY)
    label(ax, 11.6, 1.9, "percentiles로 경보를 걸면\n기준에 여유를 둬요", fs=10, color=INK)
    save(fig, OUT, "es13-decide.svg")


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

    x, y = card(0, "cardinality 집계", "서로 다른 값이 몇 개인지\n세는 집계")
    cells(ax, x + 0.3, y + 1.8, ["u-10", "u-13", "u-10"], w=0.85, h=0.55, gap=0.06, fs=9.5)
    arrow(ax, (x + 3.0, y + 2.07), (x + 3.55, y + 2.07), color=RED, ms=11)
    cell(ax, x + 3.65, y + 1.8, 0.65, 0.55, "2", hot=True, fs=10.5)
    x, y = card(1, "앞 0 줄", "해시 비트가 맨 앞부터\n0으로 이어진 길이")
    cells(ax, x + 0.5, y + 1.8, list(hbits("u-13")[:7]), w=0.45, h=0.55, gap=0.04, hot=(0, 1, 2), fs=9.5)
    x, y = card(2, "통", "앞 비트로 고른 칸.\n가장 긴 0 줄만 적어요")
    cells(ax, x + 0.35, y + 1.8, ALL, w=0.42, h=0.55, gap=0.06, hot=(3,), fs=9.5)
    x, y = card(3, "HyperLogLog", "통마다 어림해 조화평균으로\n모으는 방법")
    cells(ax, x + 0.3, y + 1.8, ALL[:4] + ["⋯"], w=0.42, h=0.55, gap=0.05, fs=9.5)
    arrow(ax, (x + 2.75, y + 2.07), (x + 3.3, y + 2.07), color=RED, ms=11)
    label(ax, x + 3.85, y + 2.07, f"≈{round(EST)}명", fs=10.5, color=RED, bold=True)
    x, y = card(4, "HyperLogLog++", "값이 적으면 해시를 그대로,\n많아지면 통 배열로")
    cells(ax, x + 0.3, y + 1.8, ["해시", "해시"], w=0.75, h=0.55, gap=0.06, fs=9.5)
    arrow(ax, (x + 1.95, y + 2.07), (x + 2.5, y + 2.07), color=RED, ms=11)
    cells(ax, x + 2.6, y + 1.8, ["", "", "", ""], w=0.4, h=0.55, gap=0.04, hot=range(4), fs=9)
    x, y = card(5, "precision_threshold", "통 수를 정하는 값\n기본 3,000이면 통 16,384개")
    for k, n in enumerate([2, 4, 8]):
        label(ax, x + 0.3, y + 2.6 - k * 0.42, ["100", "3,000", "40,000"][k], fs=9, ha="left", color=RED if k == 1 else INK)
        for j in range(n):
            ax.add_patch(Rectangle((x + 1.4 + j * 0.34, y + 2.45 - k * 0.42), 0.28, 0.3,
                                   fc=PINK if k == 1 else NOTE, ec=RED if k == 1 else INK, lw=1.0))
    x, y = card(6, "p99 (백분위)", "빠른 순으로 줄 세운\n99퍼센트 자리의 값")
    ax.plot([x + 0.4, x + 4.2], [y + 2.0, y + 2.0], color=INK, lw=1.3)
    for k in range(25):
        ax.add_patch(Circle((x + 0.4 + k * 3.8 / 24, y + 2.2), 0.035, fc=INK, ec="none"))
    xm = x + 0.4 + 0.99 * 3.8
    ax.plot([xm, xm], [y + 1.75, y + 2.55], color=RED, lw=2)
    label(ax, xm - 0.1, y + 2.8, "99%", fs=9.5, color=RED, ha="right")
    x, y = card(7, "t-digest", "값을 묶음으로 줄여 어림해요.\n꼬리는 촘촘히")
    qb = [(1 - math.cos(math.pi * j / 4)) / 2 for j in range(5)]
    for a, b in zip(qb, qb[1:]):
        ax.add_patch(FancyBboxPatch((x + 0.4 + a * 3.8 + 0.02, y + 1.85), (b - a) * 3.8 - 0.04, 0.4,
                                    boxstyle="round,pad=0,rounding_size=0.15", fc=PINK, ec=RED, lw=1.2))
    save(fig, OUT, "es13-cards.svg")


if __name__ == "__main__":
    S, L = (7.2, 3.8), (12, 6.6)
    stage(opening, 2, OUT, "es13-open", S, L)
    stage(seen, 3, OUT, "es13-seen", S, L)
    stage(ship, 2, OUT, "es13-ship", S, L)
    stage(zeros, 4, OUT, "es13-zeros", S, L)
    stage(buckets, 3, OUT, "es13-buckets", S, L)
    stage(merge, 2, OUT, "es13-merge", S, L)
    stage(tdigest, 3, OUT, "es13-tdigest", S, L)
    decide()
    stage(back, 3, OUT, "es13-back", S, L)
    cards()
