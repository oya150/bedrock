"""Elasticsearch 6편 그림 만들기. 실행: python lab/fig_es06.py  → docs/elasticsearch/img/06/*.svg

그림 안 글씨는 낱말과 숫자만 둔다. 문장은 본문과 그림 설명에 둔다. 강조는 빨강 하나.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "es"))
from figkit import (GREY, INK, LIGHT, NOTE, PAPER, PINK, RED, arrow, bits, box, canvas, cell, cells,  # noqa: E402
                    label, letters, outdir, save)
from matplotlib.patches import Circle, Rectangle  # noqa: E402

OUT = outdir("06")
SIZE, LIM = (7.2, 3.8), (12, 6.6)


def one(draw, name):
    fig, ax = canvas(*SIZE, *LIM)
    ax.add_patch(Rectangle((0, 0), *LIM, fill=False, ec="none"))
    draw(ax)
    save(fig, OUT, name)


# ── 같은 앞부분은 한 번만 ──────────────────────────────────────────
WORDS = ["seal", "search", "searched", "searching", "season", "seat"]
REST = [w[3:] for w in WORDS]
X0 = 1.2


def sea_repeat(ax):
    label(ax, 0.3, 6.35, "정렬된 낱말 여섯", fs=12.5, ha="left", bold=True)
    for r, w in enumerate(WORDS):
        letters(ax, X0, 4.55 - r * 0.68, w, hot=(0, 1, 2))
    label(ax, 7.5, 3.4, "글자 칸 37개", fs=13, ha="left", bold=True)
    label(ax, 7.5, 2.6, "sea × 6 = 18칸", fs=13, ha="left", color=RED, bold=True)


def block(ax):
    label(ax, 0.3, 6.35, "정렬된 낱말 여섯", fs=12.5, ha="left", bold=True)
    for r, w in enumerate(WORDS):
        letters(ax, X0, 4.55 - r * 0.68, w, blank=(0, 1, 2))
    letters(ax, X0, 5.45, "sea", hot=(0, 1, 2))
    label(ax, 3.0, 5.75, "← 한 번만", fs=11.5, ha="left", color=RED)
    box(ax, X0 + 1.55, 0.95, 5.2, 4.3, fc="none", ec=INK, lw=1.4, round_=False)
    label(ax, X0 + 6.6, 5.05, "블록", fs=11, ha="right", color=INK)
    label(ax, 8.2, 3.0, "블록 안 19칸\n+ 앞부분 3칸", fs=13, ha="left", bold=True)
    label(ax, 8.2, 2.0, "37칸 → 22칸", fs=13, ha="left", color=RED, bold=True)


# ── 안내판 ────────────────────────────────────────────────────────
def node(ax, x, y, final=False, hot=False, dim=False):
    ec = RED if hot else (GREY if dim else INK)
    ax.add_patch(Circle((x, y), 0.28, fc=PINK if hot else "white", ec=ec, lw=2.2 if final else 1.3,
                        ls="--" if dim else "-"))
    if final:
        ax.add_patch(Circle((x, y), 0.19, fc="none", ec=ec, lw=1.0, ls="--" if dim else "-"))


def edge(ax, a, b, ch, hot=False, dim=False, rad=0.0, dy=0.25, at=None):
    color = RED if hot else (GREY if dim else INK)
    arrow(ax, a, b, color=color, lw=1.5, ms=10, rad=rad)
    x, y = at or ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2 + dy)
    ax.text(x, y, ch, ha="center", va="center", fontsize=12, color=color)


def index(ax):
    box(ax, 8.6, 5.55, 3.1, 0.75, fc=PAPER)
    label(ax, 10.15, 5.92, "찾기: search", fs=12.5)
    label(ax, 0.3, 4.1, "블록", fs=12, ha="left", bold=True)
    for k, n in enumerate(["…", "블록 41", "블록 42", "블록 43", "…"]):
        x = 0.3 + k * 2.35
        hot = k == 2
        if n == "…":
            label(ax, x + 1.0, 3.3, "…", fs=14, color=INK)
            continue
        box(ax, x, 2.9, 2.0, 0.8, fc=PINK if hot else NOTE, ec=RED if hot else INK, round_=False)
        label(ax, x + 1.0, 3.3, n, fs=11.5, color=RED if hot else "#222", bold=hot)
    label(ax, 0.3, 6.35, "안내판", fs=12, ha="left", bold=True)
    P = {"r": (0.7, 5.15), "s": (1.9, 5.15), "sa": (3.1, 5.85), "se": (3.1, 5.15), "sea": (4.3, 5.15), "sh": (3.1, 4.5)}
    for k, (x, y) in P.items():
        node(ax, x, y, hot=k in ("s", "se", "sea"))
    for a, b, ch, dy in (("r", "s", "s", 0.3), ("s", "sa", "a", 0.25), ("s", "se", "e", None), ("se", "sea", "a", 0.3),
                         ("s", "sh", "h", -0.42)):
        (x1, y1), (x2, y2) = P[a], P[b]
        hot = (a, b) in (("r", "s"), ("s", "se"), ("se", "sea"))
        edge(ax, (x1 + 0.28, y1), (x2 - 0.28, y2), ch, hot=hot, dy=dy or 0, at=None if dy else (2.65, 4.9))
    for k, (x, y, t) in {"sa": (3.45, 5.85, "블록 41"), "sea": (4.65, 5.15, "블록 42"), "sh": (3.45, 4.5, "블록 43")}.items():
        label(ax, x, y, "→ " + t, fs=11, ha="left", color=RED if k == "sea" else INK)
    arrow(ax, (6.0, 4.95), (6.0, 3.75), color=RED, ms=14)
    # 블록 42를 열어 훑는다
    ax.plot([5.0, 0.3], [2.9, 2.45], color=INK, lw=1, ls=":")
    ax.plot([7.0, 11.7], [2.9, 2.45], color=INK, lw=1, ls=":")
    box(ax, 0.3, 0.85, 11.4, 1.6, fc=NOTE, ec=INK, round_=False)
    label(ax, 0.5, 2.15, "블록 42 (앞부분 sea)", fs=11, ha="left", color=INK)
    label(ax, 11.5, 2.15, "sea + rch = search", fs=11.5, ha="right", color=RED, bold=True)
    x = 0.6
    for r in REST:
        w = 0.36 * len(r) + 0.45
        cell(ax, x, 1.05, w, 0.7, r, hot=r == "rch", fs=12)
        x += w + 0.15


# ── 트라이 → FST ─────────────────────────────────────────────────
P4 = {"r": (0.5, 3.5), "s": (1.8, 3.5), "se": (3.1, 3.5), "sea": (4.4, 3.5), "seal": (5.8, 4.7), "seat": (5.8, 2.3),
      "seals": (7.1, 4.7), "seats": (7.1, 2.3)}
R = 0.28


def stem(ax, hot=(), vals=None):
    """s, e, a 줄기. vals가 있으면 '글자 / 값'으로 적는다."""
    for a, b, ch in (("r", "s", "s"), ("s", "se", "e"), ("se", "sea", "a")):
        t = f"{ch} / {vals[ch + b]}" if vals else ch
        edge(ax, (P4[a][0] + R, 3.5), (P4[b][0] - R, 3.5), t, hot=b in hot)


def trie(ax, merged):
    label(ax, 0.3, 6.35, "seal, seals, seat, seats", fs=12.5, ha="left", bold=True)
    for k, (x, y) in P4.items():
        final = k in ("seal", "seals", "seat", "seats")
        if k in ("seat", "seats") and merged:
            continue
        node(ax, x, y, final=final, hot=not merged and final)
    stem(ax)
    edge(ax, (P4["sea"][0] + 0.2, 3.7), (P4["seal"][0] - 0.25, 4.6), "l", at=(4.9, 4.35))
    edge(ax, (P4["seal"][0] + R, 4.7), (P4["seals"][0] - R, 4.7), "s", hot=not merged)
    if not merged:
        edge(ax, (P4["sea"][0] + 0.2, 3.3), (P4["seat"][0] - 0.25, 2.4), "t", at=(4.9, 2.6))
        edge(ax, (P4["seat"][0] + R, 2.3), (P4["seats"][0] - R, 2.3), "s", hot=True)
        label(ax, 7.8, 4.7, "← 끝 · s · 끝", fs=11.5, ha="left", color=RED)
        label(ax, 7.8, 2.3, "← 끝 · s · 끝", fs=11.5, ha="left", color=RED)
        label(ax, 7.8, 3.5, "트라이: 칸 8개", fs=12.5, ha="left", bold=True)
        label(ax, 6.0, 0.9, "이중 원 = 낱말 끝", fs=11, color=INK)
    else:
        edge(ax, (P4["sea"][0] + R, 3.4), (P4["seal"][0] + 0.1, 4.43), "t", hot=True, rad=0.55, at=(6.1, 3.6))
        label(ax, 7.8, 3.5, "FST: 칸 6개", fs=12.5, ha="left", bold=True)
        label(ax, 7.8, 2.8, "칸 8개 → 6개", fs=12.5, ha="left", color=RED, bold=True)


def output(ax):
    label(ax, 0.3, 6.35, "글자 / 값", fs=12.5, ha="left", bold=True)
    for k in ("r", "s", "se", "sea", "seal", "seals"):
        node(ax, *P4[k], final=k in ("seal", "seals"))
    stem(ax, hot=("s", "se", "sea"), vals={"ss": 5, "ese": 0, "asea": 0})
    edge(ax, (P4["sea"][0] + 0.2, 3.7), (P4["seal"][0] - 0.25, 4.6), "l / 0", at=(4.6, 4.45))
    edge(ax, (P4["sea"][0] + R, 3.4), (P4["seal"][0] + 0.1, 4.43), "t / 4", hot=True, rad=0.55, at=(6.1, 3.6))
    edge(ax, (P4["seal"][0] + R, 4.7), (P4["seals"][0] - R, 4.7), "s / 1")
    label(ax, 7.8, 3.9, "seal = 5 + 0 + 0 + 0 = 5", fs=11.5, ha="left", color=INK)
    label(ax, 7.8, 3.1, "seat = 5 + 0 + 0 + 4 = 9", fs=11.5, ha="left", color=RED, bold=True)


# ── 포스팅 목록: 차이값 ──────────────────────────────────────────
IDS = [3, 7, 8, 15, 21, 22, 40]
DIFF = [IDS[0]] + [b - a for a, b in zip(IDS, IDS[1:])]


def postings(ax):
    label(ax, 0.3, 6.35, "환불이 든 문서 번호", fs=12.5, ha="left", bold=True)
    X = lambda n: 0.6 + n * 0.27  # noqa: E731
    ax.plot([X(0), X(41)], [4.0, 4.0], color=INK, lw=1.4)
    for n in range(0, 41, 5):
        ax.plot([X(n), X(n)], [3.9, 4.1], color=INK, lw=1)
    label(ax, X(0), 3.55, "0", fs=9.5, color=INK)
    prev = 0
    for n in IDS:
        ax.add_patch(Circle((X(n), 4.0), 0.15, fc=INK, ec="none"))
        sh = {7: -0.15, 8: 0.15, 21: -0.15, 22: 0.15}.get(n, 0)
        label(ax, X(n) + sh, 3.55, str(n), fs=12, color="#222")
        arrow(ax, (X(prev), 4.15), (X(n), 4.15), color=RED, lw=1.4, ms=9, rad=-0.6)
        label(ax, (X(prev) + X(n)) / 2, 4.95 + 0.03 * (n - prev) + (0.35 if n - prev == 1 else 0),
              f"+{n - prev}", fs=11.5, color=RED, bold=True)
        prev = n
    label(ax, 0.3, 2.45, "문서 번호", fs=11.5, ha="left", color=INK)
    cells(ax, 2.2, 2.1, IDS, w=0.9, h=0.65, fs=11.5)
    label(ax, 0.3, 1.55, "차이값", fs=11.5, ha="left", color=RED)
    cells(ax, 2.2, 1.2, DIFF, w=0.9, h=0.65, hot=range(len(DIFF)), fs=11.5)


# ── 비트 패킹 ────────────────────────────────────────────────────
def pack(ax):
    label(ax, 0.3, 6.35, "18을 32비트로", fs=12.5, ha="left", bold=True)
    bits(ax, 0.5, 5.25, format(18, "032b"), w=0.34, h=0.58, hot=range(27, 32), dim=range(27))
    label(ax, 5.2, 4.85, "0 × 27칸", fs=11, color=GREY)
    label(ax, 10.3, 4.85, "10010 = 5칸", fs=11.5, color=RED, bold=True)
    label(ax, 0.3, 3.95, "묶음 하나 = 차이값 128개, 5칸씩 (앞 7개)", fs=12, ha="left", bold=True)
    x = 0.6
    for d in DIFF:
        hot = d == 18
        bits(ax, x, 2.7, format(d, "05b"), w=0.28, hot=range(5) if hot else ())
        label(ax, x + 0.7, 3.45, str(d), fs=11.5, color=RED if hot else INK, bold=hot)
        x += 5 * 0.28 + 0.12
    label(ax, x + 0.1, 2.95, "…", fs=13, ha="left", color=INK)
    label(ax, 6.0, 1.75, "가장 큰 값 18 → 5칸     128 × 5 = 640비트 = 80바이트", fs=11.5, color=INK)
    label(ax, 6.0, 0.8, "32칸씩 512바이트 → 5칸씩 80바이트", fs=12.5, color=RED, bold=True)


# ── 페이지 캐시 ──────────────────────────────────────────────────
def cache(ax):
    heap = 8
    label(ax, 0.3, 6.35, "메모리 16칸", fs=12.5, ha="left", bold=True)
    w = 0.66
    for k in range(16):
        x = 0.5 + k * w
        if k < heap:
            ax.add_patch(Rectangle((x, 4.8), w, 0.9, fc=LIGHT, ec=GREY, lw=1))
        else:
            ax.add_patch(Rectangle((x, 4.8), w, 0.9, fc="white", ec=INK, lw=1))
    label(ax, 0.5 + heap * w / 2, 5.25, "자바 힙", fs=11.5, color=INK)
    label(ax, 0.5 + (heap + 16) * w / 2, 4.35, "남는 메모리 (페이지 캐시)", fs=11, color=RED)
    label(ax, 0.3, 1.2, "디스크: 역색인 파일", fs=11, ha="left", color=INK)
    for k in range(6):
        x = 0.5 + k * 1.2
        mx = 0.5 + (heap + k) * w
        ax.add_patch(Rectangle((mx + 0.08, 4.9), w - 0.16, 0.7, fc=PINK, ec=RED, lw=1.2))
        ax.add_patch(Rectangle((x, 1.6), 0.9, 0.8, fc=NOTE, ec=INK, lw=1.2))
    arrow(ax, (3.9, 2.55), (0.5 + (heap + 0.5) * w, 4.7), color=RED, lw=1.5, ms=12)
    label(ax, 8.0, 2.0, "6조각 모두 올라감", fs=12, ha="left", color=INK)


if __name__ == "__main__":
    one(sea_repeat, "es06-sea.svg")
    one(block, "es06-block.svg")
    one(index, "es06-index.svg")
    one(lambda ax: trie(ax, merged=False), "es06-trie.svg")
    one(lambda ax: trie(ax, merged=True), "es06-fst.svg")
    one(output, "es06-output.svg")
    one(postings, "es06-postings.svg")
    one(pack, "es06-pack.svg")
    one(cache, "es06-cache.svg")
