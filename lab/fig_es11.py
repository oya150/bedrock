"""Elasticsearch 11편 그림 만들기. 실행: python lab/fig_es11.py  → docs/elasticsearch/img/11/*.svg

그림마다 한 장. 그림 안 글씨는 낱말과 숫자만 두고 지금 볼 곳만 빨강으로 칠한다.
예시는 쇼핑몰 가격 필터 10~25원과 상품 넷(스티커 10원, 연필 25원, 지우개 100원, 공책 2000원).
상품이 100만 개로 늘면 가격대 1만~5만 원.
"""
import os
import random
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "es"))
from figkit import (GREY, INK, LIGHT, NOTE, PAPER, PINK, RED, arrow, box, bubble,  # noqa: E402
                    canvas, cell, cells, cylinder, label, outdir, save)
from matplotlib.patches import Circle, Rectangle  # noqa: E402

OUT = outdir("11")
GOODS = [("스티커", 10), ("연필", 25), ("지우개", 100), ("공책", 2000)]
CYL = (8.0, 3.0, 3.6, 1.7)
ROW_Y = [3.95, 3.35, 2.75, 2.15]


def empty(ax, x, y, w, h, s="", fs=10):
    ax.add_patch(Rectangle((x, y), w, h, fc="white", ec=GREY, lw=1.0, ls="--"))
    if s:
        label(ax, x + w / 2, y + h / 2, s, fs=fs, color=GREY)


def field(ax, x, y, w, s, fs=12):
    ax.add_patch(Rectangle((x, y), w, 0.5, fc="white", ec=INK, lw=1.2))
    label(ax, x + w / 2, y + 0.25, s, fs=fs)


def shop(ax, hot=(), dim=(), checks=(), footer="상품 4개", fhot=False):
    """처음 장면과 돌아오는 장면의 무대: 쇼핑몰 상품 목록 화면과 가격 필터. hot/dim/checks=상품 가격."""
    box(ax, 0.6, 0.65, 6.4, 5.75, fc="white", round_=False)
    ax.add_patch(Rectangle((0.6, 5.95), 6.4, 0.45, fc=LIGHT, ec=INK, lw=1.2))
    label(ax, 0.8, 6.17, "쇼핑몰 상품 목록", fs=11, ha="left", color=INK)
    label(ax, 0.9, 5.45, "가격", fs=11.5, ha="left", color=INK)
    field(ax, 1.75, 5.2, 1.0, "10")
    label(ax, 3.1, 5.45, "원 ~", fs=11, color=INK)
    field(ax, 3.45, 5.2, 1.0, "25")
    label(ax, 4.75, 5.45, "원", fs=11, color=INK)
    ax.add_patch(Rectangle((5.55, 5.2), 1.2, 0.5, fc=LIGHT, ec=INK, lw=1.2))
    label(ax, 6.15, 5.45, "적용", fs=11.5)
    label(ax, 1.9, 4.65, "상품", fs=10, color=INK)
    label(ax, 4.6, 4.65, "가격", fs=10, color=INK)
    ax.plot([0.85, 6.75], [4.45, 4.45], color=INK, lw=1.0)
    for (name, p), y in zip(GOODS, ROW_Y):
        on, off = p in hot, p in dim
        if on:
            ax.add_patch(Rectangle((0.85, y - 0.24), 5.9, 0.48, fc=PINK, ec=RED, lw=1.8))
        else:
            ax.plot([0.85, 6.75], [y - 0.27, y - 0.27], color=GREY, lw=0.8)
        c = RED if on else (GREY if off else "#222")
        label(ax, 1.9, y, name, fs=11.5, color=c, bold=on)
        label(ax, 4.6, y, f"{p}원", fs=11.5, color=c, bold=on)
        if p in checks:
            label(ax, 6.45, y, "✓", fs=12, color=GREY if off else RED)
    if footer:
        label(ax, 3.8, 1.2, footer, fs=11.5, color=RED if fhot else INK, bold=fhot)


def es(ax, kind, hot=False):
    x, y, w, h = CYL
    cylinder(ax, *CYL, "ES")
    c = RED if hot else "#222"
    label(ax, x + w / 2, y + 1.1, "가격 필드", fs=11, color=INK)
    label(ax, x + w / 2, y + 0.5, kind, fs=12, color=c, bold=hot)


# ── 여는 장면: keyword 가격으로 10~25원을 찾으면 넷 다 나와요 ──────
def opening(ax):
    shop(ax, hot=(100, 2000), checks=(10, 25, 100, 2000), footer="4개", fhot=True)
    es(ax, "keyword")


# ── 글자 순서와 숫자 순서 ──────────────────────────────────────────
def order(ax):
    W, G = 2.0, 0.15
    X0 = 3.2
    label(ax, 0.3, 4.97, "keyword\n(글자 순서)", fs=11, ha="left", color=RED)
    cells(ax, X0, 4.6, ['"10"', '"100"', '"2000"', '"25"'], w=W, h=0.75, gap=G, hot=(1, 2), fs=12)
    xa, xb = X0, X0 + 4 * W + 3 * G
    ax.plot([xa, xa, xb, xb], [5.55, 5.75, 5.75, 5.55], color=RED, lw=2)
    label(ax, (xa + xb) / 2, 6.1, '"10" ~ "25": 4개', fs=11.5, color=RED, bold=True)
    label(ax, 0.3, 2.37, "long\n(숫자 순서)", fs=11, ha="left", color=INK)
    cells(ax, X0, 2.0, ["10", "25", "100", "2000"], w=W, h=0.75, gap=G, fs=12)
    xb2 = X0 + 2 * W + G
    ax.plot([xa, xa, xb2, xb2], [2.95, 3.15, 3.15, 2.95], color=INK, lw=2)
    label(ax, (xa + xb2) / 2, 3.5, "10 ~ 25: 2개", fs=11.5, color=INK, bold=True)


# ── 값마다 목록은 범위에 약해요 ────────────────────────────────────
def inverted(ax):
    label(ax, 0.3, 6.2, "상품 100만 개 · 가격은 100원 단위", fs=11, ha="left", color=INK)
    rows = ["10,000원", "10,100원", "⋯", "49,900원", "50,000원"]
    docs = [["3", "81", "⋯"], ["12", "40", "⋯"], None, ["7", "66", "⋯"], ["25", "93", "⋯"]]
    label(ax, 0.3, 5.6, "역색인: 값 → 문서 목록", fs=10.5, ha="left", color=INK)
    for k, (v, d) in enumerate(zip(rows, docs)):
        y = 4.75 - k * 0.8
        if d is None:
            label(ax, 1.6, y + 0.3, "⋮", fs=13, color=RED)
            continue
        cell(ax, 0.3, y, 2.6, 0.6, v, hot=True, fs=10.5)
        arrow(ax, (3.0, y + 0.3), (3.5, y + 0.3), color=RED, ms=11, lw=1.5)
        cells(ax, 3.6, y, d, w=0.75, h=0.6, gap=0.06, fs=10)
    field(ax, 7.3, 5.5, 4.3, "가격 10,000 ~ 50,000원", fs=11)
    label(ax, 9.45, 4.3, "서로 다른 값 401개", fs=11.5, color=RED, bold=True)
    label(ax, 9.45, 3.6, "→ 목록 401개 합치기", fs=11, color=RED)


# ── 잎 칸 ──────────────────────────────────────────────────────────
BOUNDS = [(100, 9_800), (9_900, 19_800), (19_900, 30_100), (30_200, 40_000),
          (40_100, 50_300), (50_400, 61_000), (61_100, 70_500), (70_600, 80_000)]
LO, HI = 10_000, 50_000
LW, LX0 = 1.42, 0.3


def kind(a, b):
    if b < LO or a > HI:
        return "out"
    if LO <= a and b <= HI:
        return "in"
    return "cut"


assert [kind(a, b) for a, b in BOUNDS] == ["out", "cut", "in", "in", "cut", "out", "out", "out"]


def leaf(ax, k, y, h, state="", hot=False, fs=9.5, title=True):
    """잎 칸 하나. state: ''(보통) out(건너뜀, 언제나 회색). hot=이번 장에 바뀜(빨강, 밖은 회색 그대로)."""
    a, b = BOUNDS[k]
    x = LX0 + k * LW
    w = LW - 0.14
    if state == "out":
        fc, ec, col = LIGHT, GREY, GREY
    elif hot:
        fc, ec, col = PINK, RED, RED
    else:
        fc, ec, col = NOTE, INK, "#222"
    hot = hot and state != "out"
    ax.add_patch(Rectangle((x, y), w, h, fc=fc, ec=ec, lw=2.0 if hot else 1.2))
    if title:
        label(ax, x + w / 2, y + h - 0.3, f"잎 칸 {k + 1}", fs=9.5, color=col, bold=hot)
    label(ax, x + w / 2, y + h / 2 - (0.2 if title else 0), f"{a:,}\n~{b:,}", fs=fs, color=col)
    return x, w


def leaves(ax, step):
    label(ax, 0.3, 6.2, "잎 칸: 가격순 512개씩 (상품 100만 개)", fs=11, ha="left", color=INK)
    tags = {"out": "건너뜀", "in": "통째로\n담기", "cut": "하나씩\n확인"}
    when = {"out": 3, "in": 4, "cut": 5}
    for k, (a, b) in enumerate(BOUNDS):
        s = kind(a, b)
        shown = step >= when[s]
        hot = step == when[s]
        x, w = leaf(ax, k, 3.5, 1.9, s if shown else "", hot=hot)
        if shown:
            label(ax, x + w / 2, 2.95, tags[s], fs=10, color=RED if hot else (GREY if s == "out" else INK), bold=hot)
    if step >= 2:
        x1 = LX0 + 1 * LW + 0.1
        x2 = LX0 + 4 * LW + LW - 0.3
        c = RED if step == 2 else INK
        ax.plot([x1, x2], [2.2, 2.2], color=c, lw=3)
        ax.plot([x1, x1], [2.05, 2.35], color=c, lw=2)
        ax.plot([x2, x2], [2.05, 2.35], color=c, lw=2)
        label(ax, (x1 + x2) / 2, 1.7, "찾는 범위: 10,000 ~ 50,000원", fs=11, color=c, bold=step == 2)


# ── 칸을 둘씩 묶은 나무 ────────────────────────────────────────────
def node(ax, x, y, w, h, s, state="", hot=False, fs=9.5, tag="", tagcol=RED):
    """마디. 밖(out)은 언제나 회색. tag=판정 글씨(아랫줄), 이번 장에 바뀐 판정만 빨강."""
    if state == "out":
        fc, ec, col = LIGHT, GREY, GREY
    elif hot:
        fc, ec, col = PINK, RED, RED
    else:
        fc, ec, col = PAPER, INK, "#222"
    box(ax, x, y, w, h, fc=fc, ec=ec, lw=2.0 if (hot and state != "out") else 1.3)
    if tag:
        label(ax, x + w / 2, y + h * 0.7, s, fs=fs, color=col, bold=hot and state != "out")
        label(ax, x + w / 2, y + h * 0.3, tag, fs=fs, color=tagcol, bold=tagcol == RED)
    else:
        label(ax, x + w / 2, y + h / 2, s, fs=fs, color=col, bold=hot)


def tree(ax, step):
    label(ax, 0.3, 6.25, "찾는 범위: 10,000 ~ 50,000원", fs=10.5, ha="left", color=INK)
    ly, lh = 0.95, 0.95
    l1y, l2y, ry, nh, n1 = 2.45, 3.95, 5.2, 0.6, 0.85
    centers = [LX0 + k * LW + (LW - 0.14) / 2 for k in range(8)]
    for k in range(8):
        st = "out" if ((step >= 2 and k >= 6) or (step >= 4 and k in (0, 5))) else ""
        hot = (step == 3 and k in (2, 3)) or (step == 4 and k in (1, 4))
        x, w = leaf(ax, k, ly, lh, st, hot=hot, fs=8.5, title=False)
        if step == 4 and k in (0, 1, 4, 5):
            t, c = ("하나씩 확인", RED) if k in (1, 4) else ("건너뜀", GREY)
            label(ax, x + w / 2, ly - 0.22, t, fs=9, color=c, bold=c == RED)
    l1 = [(0, 1), (2, 3), (4, 5), (6, 7)]
    for i, (a, b) in enumerate(l1):
        cx = (centers[a] + centers[b]) / 2
        w = 2.5
        for j in (a, b):
            ax.plot([centers[j], cx], [ly + lh, l1y], color=GREY, lw=1.0)
        s = f"{BOUNDS[a][0]:,}~{BOUNDS[b][1]:,}"
        st = "out" if (i == 3 and step >= 2) else ""
        hot = (i == 3 and step == 2) or (i == 1 and step == 3)
        tag, tc = "", RED
        if i == 3 and step >= 2:
            tag, tc = "통째로 건너뜀", RED if step == 2 else GREY
        if i == 1 and step >= 3:
            tag, tc = "통째로 담기", RED if step == 3 else INK
        node(ax, cx - w / 2, l1y, w, n1, s, st, hot=hot, tag=tag, tagcol=tc)
    for i, (a, b) in enumerate([(0, 3), (4, 7)]):
        cx = (centers[a] + centers[b]) / 2
        for j in (i * 2, i * 2 + 1):
            p, q = l1[j]
            ax.plot([(centers[p] + centers[q]) / 2, cx], [l1y + n1, l2y], color=GREY, lw=1.0)
        node(ax, cx - 1.4, l2y, 2.8, nh, f"{BOUNDS[a][0]:,}~{BOUNDS[b][1]:,}")
    rc = (centers[0] + centers[7]) / 2
    for a, b in [(0, 3), (4, 7)]:
        ax.plot([(centers[a] + centers[b]) / 2, rc], [l2y + nh, ry], color=GREY, lw=1.0)
    node(ax, rc - 1.4, ry, 2.8, nh, "100~80,000")
    if step == 1:
        label(ax, 11.7, 6.25, "마디 범위 = 아래 칸 범위 합", fs=10.5, ha="right", color=INK)


# ── 숫자 필드와 keyword 필드의 저장소 ─────────────────────────────
def disk():
    fig, ax = canvas(7.2, 3.6, 12, 6.0)
    parts = ["역색인", "BKD (points)", "doc values"]
    for x, name, have in ((0.3, "가격 (long)", (False, True, True)), (6.2, "가격 (keyword)", (True, False, True))):
        box(ax, x, 1.3, 5.5, 4.0, fc=NOTE)
        label(ax, x + 2.75, 4.85, name, fs=12, bold=True)
        for k, (p, h) in enumerate(zip(parts, have)):
            y = 3.65 - k * 1.0
            if h:
                cell(ax, x + 0.3, y, 4.9, 0.75, p, hot=(x < 1 and k == 1), fs=11)
            else:
                empty(ax, x + 0.3, y, 4.9, 0.75, f"{p}  0", fs=11)
    save(fig, OUT, "es11-disk.svg")


# ── 여러 차원: 지도 위 가게 80곳 ──────────────────────────────────
PX0, PY0, PW, PH = 0.8, 0.9, 7.6, 5.0
random.seed(11)
PTS = [(PX0 + 0.1 + random.random() * (PW - 0.2), PY0 + 0.1 + random.random() * (PH - 0.2)) for _ in range(80)]


def split(pts):
    """가장 넓게 퍼진 쪽을 가운데(중앙값)에서 반으로 자른다. (축, 자르는 값, 왼/아래 점, 오른/위 점)."""
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    a = 0 if (max(xs) - min(xs)) >= (max(ys) - min(ys)) else 1
    s = sorted(p[a] for p in pts)
    m = (s[len(s) // 2 - 1] + s[len(s) // 2]) / 2
    lo = [p for p in pts if p[a] < m]
    hi = [p for p in pts if p[a] > m]
    assert len(lo) == len(hi) == len(pts) // 2
    return a, m, lo, hi


def kd_cuts():
    """세 번 반으로 잘라 칸 여덟 개(칸마다 10곳)를 만든다. [(층, 축, 값, 칸 네모)]."""
    cuts, cur = [], [(PTS, (PX0, PY0, PX0 + PW, PY0 + PH))]
    for depth in range(3):
        nxt = []
        for pts, (x0, y0, x1, y1) in cur:
            a, m, lo, hi = split(pts)
            cuts.append((depth, a, m, (x0, y0, x1, y1)))
            if a == 0:
                nxt += [(lo, (x0, y0, m, y1)), (hi, (m, y0, x1, y1))]
            else:
                nxt += [(lo, (x0, y0, x1, m)), (hi, (x0, m, x1, y1))]
        cur = nxt
    assert all(len(p) == 10 for p, _ in cur)
    for p, (x0, y0, x1, y1) in cur:  # 점이 제 칸 안에 있는지
        assert all(x0 < x < x1 and y0 < y < y1 for x, y in p)
    return cuts, [r for _, r in cur]


CUTS, KCELLS = kd_cuts()
assert CUTS[0][1] == 0  # 첫 칼질은 경도(가로로 넓게 퍼짐)
XM = CUTS[0][2]


def rel(c, r):
    """칸 c(x0, y0, x1, y1)와 네모 r(x, y, w, h)의 관계: out(안 겹침) in(통째로 안) cut(걸침)."""
    x0, y0, x1, y1 = c
    rx0, ry0, rx1, ry1 = r[0], r[1], r[0] + r[2], r[1] + r[3]
    if x1 <= rx0 or x0 >= rx1 or y1 <= ry0 or y0 >= ry1:
        return "out"
    if rx0 <= x0 and x1 <= rx1 and ry0 <= y0 and y1 <= ry1:
        return "in"
    return "cut"


def pick_rect():
    """오른쪽 절반의 칸 하나를 통째로 품고 이웃 칸에 걸치는 네모(지도 밖으로는 안 나감)."""
    for c in KCELLS:
        x0, y0, x1, y1 = c
        if x0 < XM + 0.1:
            continue
        for m in (0.3, 0.25, 0.35, 0.2, 0.4):
            rx0, ry0 = max(x0 - m, XM + 0.05), max(y0 - m, PY0)
            rx1, ry1 = min(x1 + m, PX0 + PW), min(y1 + m, PY0 + PH)
            r = (rx0, ry0, rx1 - rx0, ry1 - ry0)
            kinds = [rel(k, r) for k in KCELLS]
            if kinds.count("in") == 1 and "cut" in kinds:
                return r
    raise SystemExit(f"네모 자리를 못 찾음 {KCELLS} XM={XM}")


RECT = pick_rect()
KIND = [rel(c, RECT) for c in KCELLS]
assert all(k == "out" for c, k in zip(KCELLS, KIND) if c[2] <= XM + 1e-9)  # 왼쪽 절반은 다 밖
assert sum(1 for x, _ in PTS if x < XM) == 40


def cutline(ax, a, m, rect, color, lw, ls="-"):
    x0, y0, x1, y1 = rect
    if a == 0:
        ax.plot([m, m], [y0, y1], color=color, lw=lw, ls=ls, zorder=2)
    else:
        ax.plot([x0, x1], [m, m], color=color, lw=lw, ls=ls, zorder=2)


def kd(ax, step):
    ax.add_patch(Rectangle((PX0, PY0), PW, PH, fc="white", ec=INK, lw=1.4))
    label(ax, PX0, 6.25, "지도 위 가게 80곳", fs=11, ha="left", color=INK)
    label(ax, PX0 + PW / 2, 0.55, "경도 →", fs=10, color=INK)
    label(ax, 0.35, PY0 + PH / 2, "위\n도\n↑", fs=10, color=INK)
    off = step == 5
    for x, y in PTS:
        dead = off and any(k == "out" and c[0] < x < c[2] and c[1] < y < c[3] for c, k in zip(KCELLS, KIND))
        ax.add_patch(Circle((x, y), 0.06, fc=GREY if dead else INK, ec="none", zorder=3))
    if off:
        for (x0, y0, x1, y1), k in zip(KCELLS, KIND):
            if k == "out":
                ax.add_patch(Rectangle((x0, y0), x1 - x0, y1 - y0, fc=LIGHT, ec="none", alpha=0.7, zorder=1))
    for depth, a, m, rect in CUTS:
        if step < 2 or (depth > 0 and step < 3):
            continue
        hot = (depth == 0 and step == 2) or (depth > 0 and step == 3)
        lw = {0: 2.4, 1: 1.7, 2: 1.2}[depth]
        cutline(ax, a, m, rect, RED if hot else "#222", lw, ls="--" if depth == 2 else "-")
    if step >= 4:
        x, y, w, h = RECT
        hot = step == 4
        ax.add_patch(Rectangle((x, y), w, h, fc=PINK, ec=RED, lw=2.2 if hot else 1.6, alpha=0.55, zorder=2))
        ly_ = y + h + 0.25 if y + h < PY0 + PH - 0.1 else y - 0.25
        label(ax, x + w / 2, ly_, "찾는 네모", fs=10.5, color=RED, bold=hot, zorder=4,
              bbox=dict(fc="white", ec="none", pad=0.5, alpha=0.8))
    NX = 8.7
    if step == 3:
        label(ax, NX, 4.6, "① 경도로 반\n(40곳 / 40곳)", fs=10.5, ha="left", color="#222")
        label(ax, NX, 3.3, "② 나뉜 쪽마다\n또 반\n(칸마다 10곳)", fs=10.5, ha="left", color=RED)
    elif step == 5:
        label(ax, PX0 + (XM - PX0) / 2, PY0 + PH / 2, "왼쪽 절반\n통째로 건너뜀", fs=11.5, color=GREY, bold=True, zorder=4,
              bbox=dict(fc=LIGHT, ec="none", pad=1))
        for (x0, y0, x1, y1), k in zip(KCELLS, KIND):
            if x1 <= XM + 1e-9:
                continue
            t, c = {"out": ("건너뜀", GREY), "in": ("통째로\n담기", RED), "cut": ("하나씩\n확인", RED)}[k]
            if k == "cut":
                ax.add_patch(Rectangle((x0, y0), x1 - x0, y1 - y0, fill=False, ec=RED, lw=1.6, ls="--", zorder=2))
            ty = (y0 + y1) / 2
            if k == "cut":  # 네모 밖 쪽에 글씨를 둔다
                ty = y1 - 0.4 if y1 - (RECT[1] + RECT[3]) > RECT[1] - y0 else y0 + 0.4
            label(ax, (x0 + x1) / 2, ty, t, fs=10.5, color=c, bold=c == RED, zorder=5,
                  bbox=dict(fc="white" if k != "out" else LIGHT, ec="none", pad=1, alpha=0.85))


# ── 넓은 범위와 드문 조건 ──────────────────────────────────────────
def wide(ax):
    label(ax, 0.3, 6.2, "최근 1년 주문 중 고객 12345의 주문", fs=11, ha="left", color=INK)
    label(ax, 0.3, 5.35, "최근 1년", fs=11, ha="left", color=INK)
    ax.add_patch(Rectangle((2.0, 5.05), 5.2, 0.6, fc=LIGHT, ec=GREY, lw=1.6))
    label(ax, 4.6, 5.35, "전체 주문의 절반", fs=11, color=INK)
    label(ax, 0.3, 4.3, "고객 12345", fs=11, ha="left", color=RED, bold=True)
    for k in range(10):
        cell(ax, 2.0 + k * 0.42, 4.0, 0.36, 0.6, "", hot=True)
    label(ax, 6.3, 4.3, "⋯ 30건", fs=11, ha="left", color=RED, bold=True)
    cylinder(ax, 8.4, 3.9, 3.0, 1.4, "ES")
    bubble(ax, 3.4, 0.9, 8.2, 2.0, "① 고객 12345의 30건 꺼내기\n② 30건의 날짜만 doc values로 확인", (9.2, 3.6), hot=True)


def one(draw, name, size=(7.2, 3.8), lim=(12, 6.6)):
    """장면 하나만 그린다."""
    fig, ax = canvas(*size, *lim)
    ax.add_patch(Rectangle((0, 0), *lim, fill=False, ec="none"))
    draw(ax)
    save(fig, OUT, name)


if __name__ == "__main__":
    one(opening, "es11-open.svg")
    one(order, "es11-order.svg")
    one(inverted, "es11-inv.svg")
    one(lambda ax: leaves(ax, 5), "es11-leaves.svg")
    one(lambda ax: tree(ax, 1), "es11-tree-1.svg")
    one(lambda ax: tree(ax, 4), "es11-tree-2.svg")
    disk()
    one(lambda ax: kd(ax, 3), "es11-kd-1.svg")
    one(lambda ax: kd(ax, 5), "es11-kd-2.svg")
    one(wide, "es11-wide.svg")
