"""Elasticsearch 13편 그림 만들기. 실행: python lab/fig_es13.py  → docs/elasticsearch/img/13/*.svg

그림 9장. 예시는 방문 대시보드의 사용자 u-1~u-40을 편 끝까지 잇는다. 그림 안 글씨는 낱말과 숫자만 둔다.
해시 비트와 통 값은 lab/es/13_hll.py 와 같은 해시(blake2b 64비트)로 여기서 직접 계산한다.
"""
import hashlib
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "es"))
from figkit import (GREY, INK, LIGHT, NOTE, PAPER, PINK, RED, arrow, box, canvas,  # noqa: E402
                    cell, cells, cylinder, label, outdir, save, stage)
from matplotlib.patches import FancyBboxPatch, Rectangle  # noqa: E402

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
# 통에는 앞 0 줄 + 1 을 적는다(빈 통 0 과 구별). 그림과 본문은 이 값을 보여 준다.
SHOW, SHOW_A, SHOW_B = ([z + 1 for z in r] for r in (ALL, REG_A, REG_B))
assert SHOW == [4, 6, 3, 5, 2, 3, 5, 2]
assert round(sum(2.0 ** -v for v in SHOW) ** -1 * 8) == 9 and round(9 * 8 * 0.64) == 46


def empty(ax, x, y, w, h, s="", fs=10):
    ax.add_patch(Rectangle((x, y), w, h, fc="white", ec=GREY, lw=1.0, ls="--"))
    if s:
        label(ax, x + w / 2, y + h / 2, s, fs=fs, color=GREY)


# ── 정확히 세기: 본 ID 목록 ────────────────────────────────────────
LX, LW, LS = 3.4, 1.1, 1.18


def seen(ax):
    label(ax, 0.3, 6.3, "들어온 기록", fs=11, ha="left", color=INK)
    cell(ax, 0.3, 5.2, 1.4, 0.7, "u-12", fs=11)
    cell(ax, 0.3, 2.6, 1.4, 0.7, "u-13", hot=True, fs=11)
    end = cells(ax, LX, 4.0, ["u-10", "u-11", "u-12", "u-13", "⋯"], w=LW, h=0.7, gap=LS - LW, hot=(3,), fs=11)
    cell(ax, end + 0.1, 4.0, 1.7, 0.7, "100만 번째", fs=10.5)
    label(ax, LX, 3.55, "본 ID 목록", fs=11, ha="left", color=INK)
    arrow(ax, (1.75, 5.55), (LX + 2 * LS + LW / 2, 4.75), color=GREY, rad=-0.2, ms=13)
    label(ax, 4.6, 5.95, "있음 → 그대로", fs=10.5, color=INK)
    arrow(ax, (1.75, 2.95), (LX + 3 * LS + LW / 2, 3.95), color=RED, rad=0.2, ms=13)
    label(ax, 5.2, 2.55, "없음 → 더함", fs=10.5, color=RED)
    label(ax, 6.0, 1.2, "사용자 100만 명 → 100만 칸 → 칸마다 40바이트면 40 MB", fs=11.5, color=RED, bold=True)


# ── 정확히 세기: 샤드마다 목록을 보내요 ────────────────────────────
def shardbox(ax, x, name, items, hot, n):
    box(ax, x, 3.9, 5.4, 2.2, fc=NOTE)
    label(ax, x + 0.2, 5.75, name, fs=11.5, ha="left", bold=True)
    label(ax, x + 5.2, 5.75, f"{n}명", fs=11, ha="right", color=INK)
    cells(ax, x + 0.2, 4.2, items, w=0.95, h=0.7, gap=0.06, hot=hot, fs=10.5)


def ship(ax):
    shardbox(ax, 0.3, "샤드 A", ["u-1", "⋯", "u-13", "⋯", "u-20"], (2,), 20)
    shardbox(ax, 6.2, "샤드 B", ["u-13", "u-21", "⋯", "u-39", "u-40"], (0,), 21)
    cylinder(ax, 4.9, 1.3, 2.2, 0.9, "조율 노드")
    arrow(ax, (2.8, 3.85), (4.75, 2.4), color=RED, ms=14)
    arrow(ax, (9.2, 3.85), (7.25, 2.4), color=RED, ms=14)
    label(ax, 2.5, 3.0, "ID 목록 통째로", fs=10.5, color=RED)
    label(ax, 9.5, 3.0, "ID 목록 통째로", fs=10.5, color=RED)
    label(ax, 0.3, 0.75, "센 수 더하기: 20 + 21 = 41 ✗", fs=11, ha="left", color=INK)
    label(ax, 11.7, 0.75, "목록 합쳐 겹침 지우기: 40 ✓", fs=11, ha="right", color=RED, bold=True)


# ── 해시 앞의 0 줄 ─────────────────────────────────────────────────
ZY = [5.45, 4.7, 3.95, 3.2, 2.45, 1.7]
BX, BW = 2.2, 0.5


def bitrow(ax, y, u, b, hot_zero=False, row_hot=False, note=True):
    z = lead0(b)
    label(ax, 0.35, y + 0.3, u, fs=11, ha="left", color=RED if row_hot else "#222", bold=row_hot)
    arrow(ax, (1.25, y + 0.3), (BX - 0.1, y + 0.3), color=GREY, ms=10, lw=1.4)
    for i, ch in enumerate(b[:8]):
        cell(ax, BX + i * BW, y, BW - 0.04, 0.6, ch, hot=(hot_zero or row_hot) and i < z, fs=10.5)
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
        bitrow(ax, ZY[k], u, hbits(u), hot_zero=step == 1)
    if step == 1:
        memo(ax, 3, "1/8 → 대략 8명", hot=True)
    else:
        bitrow(ax, ZY[4], "u-12", hbits("u-12"), note=False)
        label(ax, 7.0, ZY[4] + 0.3, "다시 옴", fs=10.5, ha="left", color=INK)
        bitrow(ax, ZY[5], "u-21", hbits("u-21"), row_hot=True)
        memo(ax, 6, "1/64 → 대략 64명", hot=True, extra="실제 5명")


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
    label(ax, x0 + 3.95, 4.45, "0이 4개 → 4 + 1 = 5", fs=10, color=RED if hot1 else INK)
    if step == 1:
        tongs(ax, [None, None, None, 5, None, None, None, None], hot=(3,))
        arrow(ax, (x0 + 3.95, 4.2), (TX + 3 * (TW + 0.1) + TW / 2, 3.4), color=RED, ms=14)
    else:
        tongs(ax, SHOW, hot=range(8))
        label(ax, 11.7, 4.45, "u-1 ~ u-40, 40명", fs=10.5, ha="right", color=RED)
        label(ax, 0.3, 1.85, "통마다 어림", fs=10, ha="left", color=INK)
        for i, v in enumerate(SHOW):
            label(ax, TX + i * (TW + 0.1) + TW / 2, 1.85, str(2 ** v), fs=10.5, color=INK)
        label(ax, 6.0, 1.0, f"조화평균 9 × 통 8 × 0.64 → 대략 {round(EST)}명 (실제 40명)", fs=11.5, color=RED, bold=True)


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
    mrow(ax, 5.0, "샤드 A", SHOW_A)
    mrow(ax, 1.3, "샤드 B", SHOW_B)
    if step == 1:
        mrow(ax, 3.15, "조율 노드", None, dashed=True)
        label(ax, 0.3, 2.8, "통 배열만 받아요", fs=10, ha="left", color=INK)
    else:
        mrow(ax, 3.15, "조율 노드", SHOW, hot=True)
        for i in range(8):
            x = MX + i * (MW + 0.12) + MW / 2
            if REG_A[i] >= REG_B[i]:
                arrow(ax, (x, 4.95), (x, 3.9), color=RED, ms=10, lw=1.5)
            if REG_B[i] >= REG_A[i]:
                arrow(ax, (x, 2.05), (x, 3.1), color=RED, ms=10, lw=1.5)
        label(ax, 0.3, 2.8, "칸마다 큰 값", fs=10, ha="left", color=RED)


# ── 백분위: t-digest ───────────────────────────────────────────────
AX0, AX1, AY = 0.7, 11.3, 3.9
DELTA = 28
QB = [(1 - math.cos(math.pi * j / DELTA * 2)) / 2 for j in range(DELTA // 2 + 1)]


def qx(q):
    return AX0 + q * (AX1 - AX0)


def tdigest(ax):
    label(ax, 0.3, 5.65, "응답 시간을 빠른 순으로 줄 세움", fs=11.5, ha="left", bold=True)
    ax.plot([AX0, AX1], [AY, AY], color=INK, lw=1.4)
    for q, t in [(0, "0%"), (0.5, "50%"), (1, "100%")]:
        ax.plot([qx(q), qx(q)], [AY - 0.08, AY + 0.08], color=INK, lw=1.2)
        label(ax, qx(q), AY - 0.4, t, fs=10, color=INK)
    for a, b in zip(QB, QB[1:]):
        x, w = qx(a) + 0.025, qx(b) - qx(a) - 0.05
        tail = a > 0.9 or b < 0.1
        ax.add_patch(FancyBboxPatch((x, 4.18), w, 0.44, boxstyle=f"round,pad=0,rounding_size={min(0.2, w / 2):.3f}",
                                    fc=PINK if tail else NOTE, ec=RED if tail else INK, lw=1.4))
    ax.plot([qx(0.99), qx(0.99)], [4.85, AY - 0.15], color=RED, lw=2.2)
    label(ax, qx(0.99), 5.1, "99%", fs=10.5, color=RED, bold=True)
    label(ax, qx(0.5), 2.7, "가운데: 큰 묶음", fs=11, color=INK)
    label(ax, qx(0.92), 2.7, "꼬리: 작은 묶음", fs=11, color=RED)
    label(ax, qx(0.08), 2.7, "꼬리: 작은 묶음", fs=11, color=RED)
    label(ax, 6.0, 1.7, "묶음마다 평균값 + 개수", fs=11, color=INK)


# ── 판단: 언제 쓸모 있을까요 ──────────────────────────────────────
def decide():
    fig, ax = canvas(10, 3.6, 15, 5.4)
    box(ax, 0.3, 3.6, 6.0, 1.3, fc=NOTE)
    label(ax, 3.3, 4.25, "한 명 차이가 돈 계산에 걸림", fs=10.5, bold=True)
    arrow(ax, (6.4, 4.25), (8.4, 4.25), color=RED)
    label(ax, 7.4, 4.55, "예", fs=10, color=RED)
    box(ax, 8.5, 3.6, 6.2, 1.3, fc=PINK, ec=RED)
    label(ax, 11.6, 4.25, "정확히 세기\n(composite 집계, 원본 로그 세기)", fs=10.5, color=RED, bold=True)
    arrow(ax, (3.3, 3.5), (3.3, 2.6))
    label(ax, 3.6, 3.05, "아니요", fs=10, color=INK, ha="left")
    box(ax, 0.3, 1.3, 6.0, 1.2, fc=PAPER)
    label(ax, 3.3, 1.9, "cardinality 근삿값\n(흐름을 보는 대시보드)", fs=10)
    box(ax, 8.5, 1.3, 6.2, 1.2, fc=LIGHT, ec=GREY)
    label(ax, 11.6, 1.9, "percentiles 경보\n→ 기준에 여유", fs=10, color=INK)
    save(fig, OUT, "es13-decide.svg")


def single(draw, name, size=(7.2, 3.8), lim=(12, 6.6)):
    fig, ax = canvas(*size, *lim)
    ax.add_patch(Rectangle((0, 0), *lim, fill=False, ec="none"))
    draw(ax)
    save(fig, OUT, name)


if __name__ == "__main__":
    S, L = (7.2, 3.8), (12, 6.6)
    single(seen, "es13-seen.svg")
    single(ship, "es13-ship.svg")
    stage(zeros, 2, OUT, "es13-zeros", S, L)
    stage(buckets, 2, OUT, "es13-buckets", S, L)
    single(lambda ax: merge(ax, 2), "es13-merge.svg")
    single(tdigest, "es13-tdigest.svg")
    decide()
