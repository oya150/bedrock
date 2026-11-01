"""Elasticsearch 11편 그림 만들기. 실행: python lab/fig_es11.py  → docs/elasticsearch/img/11/*.svg

본문 절은 장면 띠로 그린다: 같은 무대를 여러 장 그리고 장마다 바뀐 곳만 빨강으로 칠한다.
예시는 쇼핑몰 가격 필터 10~25원과 상품 넷(스티커 10원, 연필 25원, 지우개 100원, 공책 2000원)을 편 끝까지 잇는다.
상품이 100만 개로 늘면 가격대 1만~5만 원(.claude/writing/work/cal/units-es11.md).
"""
import os
import random
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "es"))
from figkit import (BLUE, GREY, INK, LIGHT, NOTE, PAPER, PINK, RED, arrow, box, bubble,  # noqa: E402
                    canvas, cell, cells, cylinder, label, moral, outdir, save, stage)
from matplotlib.patches import Circle, Rectangle  # noqa: E402

OUT = outdir("11")
GOODS = [("스티커", 10), ("연필", 25), ("지우개", 100), ("공책", 2000)]
CYL = (8.0, 3.0, 3.6, 1.7)
SAY = (7.2, 0.55, 4.5, 1.3)
TAIL = (9.8, 2.75)
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


# ── 여는 장면: 가격 10~25원을 찾았는데 100원이 섞여요 ─────────────
def opening(ax, step):
    if step == 1:
        shop(ax)
        es(ax, "keyword")
        bubble(ax, *SAY, "가격을 keyword 필드에\n담았어요", TAIL)
    elif step == 2:
        shop(ax, hot=(100, 2000), checks=(10, 25, 100, 2000), footer="4개가 나왔어요", fhot=True)
        es(ax, "keyword")
        bubble(ax, *SAY, "10~25원을 찾았더니\n100원, 2000원도 나왔어요", TAIL, hot=True)
    else:
        shop(ax, dim=(100, 2000), checks=(10, 25), footer="2개가 나왔어요")
        es(ax, "long", hot=True)
        bubble(ax, *SAY, "long 필드에 담으니\n10원, 25원만 나와요", TAIL, hot=True)
        moral(ax, 4.0, 0.2, "같은 가격인데 필드 타입에 따라 결과가 달라요")


# ── 글자 순서와 숫자 순서 ──────────────────────────────────────────
def order(ax, step):
    W, G = 2.0, 0.15
    X0 = 3.2
    label(ax, 0.3, 4.97, "keyword\n(글자 순서)", fs=11, ha="left", color=INK)
    cells(ax, X0, 4.6, ['"10"', '"100"', '"2000"', '"25"'], w=W, h=0.75, gap=G, fs=12)
    xa, xb = X0, X0 + 4 * W + 3 * G
    c1 = RED if step == 1 else GREY
    ax.plot([xa, xa, xb, xb], [5.55, 5.75, 5.75, 5.55], color=c1, lw=2)
    label(ax, (xa + xb) / 2, 6.1, '"10" ~ "25" 사이: 넷 다', fs=11.5, color=c1, bold=step == 1)
    if step == 1:
        label(ax, 6.0, 3.6, '"100"은 "10" 바로 뒤, "2000"은 "25" 앞에 와요', fs=11, color=INK)
        return
    label(ax, 0.3, 2.37, "long\n(숫자 순서)", fs=11, ha="left", color=RED)
    cells(ax, X0, 2.0, ["10", "25", "100", "2000"], w=W, h=0.75, gap=G, hot=(0, 1), fs=12)
    xb2 = X0 + 2 * W + G
    ax.plot([xa, xa, xb2, xb2], [2.95, 3.15, 3.15, 2.95], color=RED, lw=2)
    label(ax, (xa + xb2) / 2, 3.5, "10 ~ 25 사이: 둘", fs=11.5, color=RED, bold=True)
    moral(ax, 6.0, 0.9, "숫자는 숫자 순서로 담아야 범위가 맞아요")


# ── 값마다 목록은 범위에 약해요 ────────────────────────────────────
def inverted(ax, step):
    if step < 3:
        label(ax, 0.3, 6.2, "상품 100만 개 · 가격은 100원 단위", fs=11, ha="left", color=INK)
        rows = ["10,000원", "10,100원", "⋯", "49,900원", "50,000원"]
        docs = [["3", "81", "⋯"], ["12", "40", "⋯"], None, ["7", "66", "⋯"], ["25", "93", "⋯"]]
    else:
        label(ax, 0.3, 6.2, "주문 시각 (값이 거의 다 달라요)", fs=11, ha="left", color=RED)
        rows = ["09:00:00.001", "09:00:00.004", "⋯", "15:59:59.990", "15:59:59.997"]
        docs = [["17"], ["52"], None, ["8"], ["31"]]
    label(ax, 0.3, 5.6, "역색인: 값 → 문서 목록", fs=10.5, ha="left", color=INK)
    for k, (v, d) in enumerate(zip(rows, docs)):
        y = 4.75 - k * 0.8
        if d is None:
            label(ax, 1.6, y + 0.3, "⋮", fs=13, color=RED if step > 1 else INK)
            continue
        on = (step == 1 and k == 0) or step > 1
        cell(ax, 0.3, y, 2.6, 0.6, v, hot=on, fs=10.5)
        arrow(ax, (3.0, y + 0.3), (3.5, y + 0.3), color=RED if on else INK, ms=11, lw=1.5)
        cells(ax, 3.6, y, d, w=0.75, h=0.6, gap=0.06, fs=10)
    if step == 1:
        field(ax, 7.3, 5.5, 4.3, "가격 = 10,000원", fs=11)
        label(ax, 9.45, 4.3, "목록 하나만 꺼내요", fs=11.5, color=RED, bold=True)
    elif step == 2:
        field(ax, 7.3, 5.5, 4.3, "가격 10,000 ~ 50,000원", fs=11)
        label(ax, 9.45, 4.3, "서로 다른 값 401개", fs=11.5, color=RED, bold=True)
        label(ax, 9.45, 3.6, "목록 401개를 꺼내 합쳐요", fs=11, color=RED)
    else:
        field(ax, 7.3, 5.5, 4.3, "주문 시각 범위", fs=11)
        label(ax, 9.45, 4.3, "서로 다른 값 20만 개", fs=11.5, color=RED, bold=True)
        label(ax, 9.45, 3.6, "목록 20만 개를 꺼내 합쳐요", fs=11, color=RED)
        moral(ax, 6.0, 0.45, "값 종류가 많을수록 꺼낼 목록이 늘어요")


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
    label(ax, 0.3, 6.2, "가격순으로 줄 세워 512개씩 담은 잎 칸 (상품 100만 개)", fs=11, ha="left", color=INK)
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
    if step == 1:
        label(ax, 6.0, 2.2, "칸마다 든 값의 범위를 알아 둬요", fs=11, color=INK)
    if step == 5:
        moral(ax, 6.0, 0.75, "하나씩 확인하는 칸은 양 끝 둘뿐이에요")


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
        label(ax, 11.7, 6.25, "마디 범위 = 아래 칸 범위를 합친 것", fs=10.5, ha="right", color=INK)
    if step == 4:
        moral(ax, 6.0, 0.3, "하나씩 확인하는 칸은 이번에도 양 끝 둘이에요")


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
    moral(ax, 6.0, 0.6, "숫자 필드는 역색인 대신 BKD에 담겨요")
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
        cutline(ax, a, m, rect, RED if hot else BLUE, lw, ls="--" if depth == 2 else "-")
    if step >= 4:
        x, y, w, h = RECT
        hot = step == 4
        ax.add_patch(Rectangle((x, y), w, h, fc=PINK, ec=RED, lw=2.2 if hot else 1.6, alpha=0.55, zorder=2))
        ly_ = y + h + 0.25 if y + h < PY0 + PH - 0.1 else y - 0.25
        label(ax, x + w / 2, ly_, "찾는 네모", fs=10.5, color=RED, bold=hot, zorder=4,
              bbox=dict(fc="white", ec="none", pad=0.5, alpha=0.8))
    NX = 8.7
    if step == 1:
        label(ax, NX, 4.2, "값이 둘이라\n줄 세울 순서가\n하나로 안 정해져요", fs=10.5, ha="left", color=INK)
    elif step == 2:
        label(ax, NX, 4.2, "① 넓게 퍼진\n경도 쪽을 반으로\n(40곳 / 40곳)", fs=10.5, ha="left", color=RED)
    elif step == 3:
        label(ax, NX, 4.2, "② 나뉜 쪽마다\n넓은 쪽을 또 반으로\n칸마다 10곳이\n될 때까지", fs=10.5, ha="left", color=RED)
    elif step == 4:
        label(ax, NX, 4.2, "가게를 찾을\n네모가 왔어요", fs=10.5, ha="left", color=RED)
    else:
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
        moral(ax, 10.15, 3.4, "겹치는 칸만\n들어가 봐요", fs=12)


# ── 넓은 범위와 드문 조건 ──────────────────────────────────────────
def wide(ax, step):
    label(ax, 0.3, 6.2, "최근 1년 주문 중 고객 12345의 주문", fs=11, ha="left", color=INK)
    label(ax, 0.3, 5.35, "최근 1년", fs=11, ha="left", color=INK)
    h1 = step == 1
    ax.add_patch(Rectangle((2.0, 5.05), 5.2, 0.6, fc=PINK if h1 else LIGHT, ec=RED if h1 else GREY, lw=1.6))
    label(ax, 4.6, 5.35, "전체 주문의 절반", fs=11, color=RED if h1 else INK, bold=h1)
    label(ax, 0.3, 4.3, "고객 12345", fs=11, ha="left", color=INK)
    for k in range(10):
        cell(ax, 2.0 + k * 0.42, 4.0, 0.36, 0.6, "", hot=not h1)
    label(ax, 6.3, 4.3, "⋯ 30건", fs=11, ha="left", color=INK if h1 else RED, bold=not h1)
    cylinder(ax, 8.4, 3.9, 3.0, 1.4, "ES")
    if h1:
        bubble(ax, 3.4, 0.9, 8.2, 2.0, "날짜 범위를 BKD로 먼저 찾으면\n주문 절반의 문서 번호를 다 모아야 해요", (9.2, 3.6), hot=True)
    else:
        bubble(ax, 3.4, 0.9, 8.2, 2.0, "30건을 먼저 꺼내고\n그 30건의 날짜만 doc values로 확인해요", (9.2, 3.6), hot=True)
        moral(ax, 6.0, 0.35, "ES가 조건마다 문서 수를 어림해 길을 골라요")


def decide():
    fig, ax = canvas(10, 3.6, 15, 5.4)
    box(ax, 0.3, 3.6, 6.0, 1.3, fc=NOTE)
    label(ax, 3.3, 4.25, "가격대·기간처럼 범위로 찾나요?", fs=10.5, bold=True)
    arrow(ax, (6.4, 4.25), (8.4, 4.25), color=RED)
    label(ax, 7.4, 4.55, "예", fs=10, color=RED)
    box(ax, 8.5, 3.6, 6.2, 1.3, fc=PINK, ec=RED)
    label(ax, 11.6, 4.25, "숫자·날짜 필드에 담아요 (BKD)", fs=10.5, color=RED, bold=True)
    arrow(ax, (3.3, 3.5), (3.3, 2.6))
    label(ax, 3.6, 3.05, "아니요", fs=10, color=INK, ha="left")
    box(ax, 0.3, 1.3, 6.0, 1.2, fc=PAPER)
    label(ax, 3.3, 1.9, "범위도 정렬도 없이 같은 값만 찾는다면\nkeyword여도 결과는 맞아요", fs=10)
    arrow(ax, (11.6, 3.5), (11.6, 2.6))
    label(ax, 11.9, 3.05, "범위가 아주 넓으면", fs=10, color=INK, ha="left")
    box(ax, 8.5, 1.3, 6.2, 1.2, fc=LIGHT, ec=GREY)
    label(ax, 11.6, 1.9, "다른 조건이 드물 때 ES가\ndoc values로 확인하는 길을 골라요", fs=10, color=INK)
    save(fig, OUT, "es11-decide.svg")


# ── 정리: 처음 장면으로 돌아가기 ───────────────────────────────────
def back(ax, step):
    if step == 1:
        shop(ax, hot=(100, 2000), checks=(10, 25, 100, 2000), footer="처음엔 4개가 나왔어요")
        es(ax, "keyword")
        bubble(ax, *SAY, "처음엔 글자 순서로 찾아서\n100원, 2000원이 섞였어요", TAIL)
    else:
        shop(ax, hot=(10, 25), dim=(100, 2000), checks=(10, 25), footer="2개가 나왔어요")
        es(ax, "long (BKD)", hot=True)
        bubble(ax, *SAY, "값 순서로 담은 칸에서\n10~25원만 꺼냈어요", TAIL, hot=True)
        moral(ax, 4.0, 0.2, "숫자는 숫자 필드에 담아야 범위가 맞고 빨라요")


# ── 정리: 낱말 카드 ────────────────────────────────────────────────
def cards():
    fig, ax = canvas(6.4, 7.9, 9.8, 12.25)
    W, H = 4.6, 3.8

    def card(i, name, line):
        col, row = i % 2, i // 2
        x, y = 0.2 + col * 4.9, 8.25 - row * 4.05
        box(ax, x, y, W, H, fc="white")
        label(ax, x + 0.25, y + H - 0.4, name, fs=12.5, ha="left", bold=True)
        label(ax, x + W / 2, y + 0.6, line, fs=10, color=INK)
        return x, y

    x, y = card(0, "잎 칸 (leaf block)", "값 512개 안팎을\n값 순서로 담은 칸")
    ax.add_patch(Rectangle((x + 1.3, y + 1.45), 2.0, 1.35, fc=PINK, ec=RED, lw=1.6))
    label(ax, x + 2.3, y + 2.12, "19,900\n~30,100", fs=10, color=RED)
    x, y = card(1, "마디", "잎 칸 둘을 묶은 윗단 칸,\n범위는 둘을 합친 것")
    box(ax, x + 1.25, y + 2.35, 2.1, 0.5, fc=PINK, ec=RED, lw=1.4)
    for dx in (0.75, 2.65):
        ax.add_patch(Rectangle((x + dx, y + 1.4), 1.2, 0.5, fc=NOTE, ec=INK, lw=1.0))
        ax.plot([x + dx + 0.6, x + 2.3], [y + 1.9, y + 2.3], color=GREY, lw=1.0)
    x, y = card(2, "BKD 트리", "잎 칸을 둘씩 층층이\n묶은 나무")
    pos = [(2.3, 2.6), (1.5, 2.0), (3.1, 2.0), (1.1, 1.4), (1.9, 1.4), (2.7, 1.4), (3.5, 1.4)]
    for k, (px, py) in enumerate(pos):
        if k:
            par = pos[(k - 1) // 2]
            ax.plot([x + px, x + par[0]], [y + py + 0.15, y + par[1] - 0.15], color=GREY, lw=1.0)
        hot = k == 0
        ax.add_patch(Rectangle((x + px - 0.3, y + py - 0.15), 0.6, 0.3, fc=PINK if hot else NOTE,
                               ec=RED if hot else INK, lw=1.2))
    x, y = card(3, "points", "Lucene이 숫자·날짜·IP·위치를\nBKD로 담는 저장소")
    empty(ax, x + 0.4, y + 2.15, 3.8, 0.5, "역색인  0", fs=9.5)
    cell(ax, x + 0.4, y + 1.5, 3.8, 0.5, "BKD (points)", hot=True, fs=10)
    x, y = card(4, "밖 · 안 · 걸침", "칸 범위만 보고 건너뛰기,\n통째로 담기, 하나씩 확인")
    cell(ax, x + 0.4, y + 1.6, 1.1, 0.8, "밖", dim=True, fs=10.5)
    cell(ax, x + 1.75, y + 1.6, 1.1, 0.8, "안", hot=True, fs=10.5)
    cell(ax, x + 3.1, y + 1.6, 1.1, 0.8, "걸침", fs=10.5)
    x, y = card(5, "k-d 트리", "가장 넓게 퍼진 쪽부터\n반씩 잘라 만든 나무")
    ax.add_patch(Rectangle((x + 1.1, y + 1.35), 2.4, 1.5, fc="white", ec=INK, lw=1.2))
    ax.plot([x + 2.3, x + 2.3], [y + 1.35, y + 2.85], color=RED, lw=2.0)
    ax.plot([x + 1.1, x + 2.3], [y + 2.05, y + 2.05], color=BLUE, lw=1.5)
    ax.plot([x + 2.3, x + 3.5], [y + 2.25, y + 2.25], color=BLUE, lw=1.5)
    save(fig, OUT, "es11-cards.svg")


if __name__ == "__main__":
    S, L = (7.2, 3.8), (12, 6.6)
    stage(opening, 3, OUT, "es11-open", S, L)
    stage(order, 2, OUT, "es11-order", S, L)
    stage(inverted, 3, OUT, "es11-inv", S, L)
    stage(leaves, 5, OUT, "es11-leaves", S, L)
    stage(tree, 4, OUT, "es11-tree", S, L)
    disk()
    stage(kd, 5, OUT, "es11-kd", S, L)
    stage(wide, 2, OUT, "es11-wide", S, L)
    decide()
    stage(back, 2, OUT, "es11-back", S, L)
    cards()
