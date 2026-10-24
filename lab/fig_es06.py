"""Elasticsearch 6편 그림 만들기. 실행: python lab/fig_es06.py  → docs/elasticsearch/img/06/*.svg"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "es"))
from figkit import (GREY, INK, LIGHT, NOTE, PAPER, PINK, RED, arrow, box, canvas, cell, cells,  # noqa: E402
                    label, outdir, save)
from matplotlib.patches import Circle  # noqa: E402

OUT = outdir("06")


def open_():
    fig, ax = canvas(9, 3.4, 13, 5.0)
    box(ax, 0.4, 0.6, 4.0, 3.9, fc=NOTE)
    label(ax, 2.4, 4.0, "용어 사전", fs=12, bold=True)
    for k, t in enumerate(["aardvark", "abacus", "abandon", "⋮", "zymurgy"]):
        label(ax, 2.4, 3.4 - k * 0.55, t, fs=10, color=INK)
    label(ax, 2.4, 0.2, "낱말 수억 개", fs=11, color=RED)
    arrow(ax, (4.6, 2.5), (7.4, 2.5), color=RED)
    label(ax, 6.0, 3.0, "다 올릴까?", fs=11, color=RED)
    box(ax, 7.6, 1.6, 4.6, 1.8, fc=PINK, ec=RED)
    label(ax, 9.9, 2.5, "JVM 힙 (수 GB)", fs=12, color=RED, bold=True)
    label(ax, 9.9, 1.0, "다른 일에도 써야 해요", fs=10, color=INK)
    save(fig, OUT, "es06-open.svg")


def map_():
    steps = ["앞부분 나눠 쓰기\n(트라이)", "뒷부분도\n나눠 쓰기(FST)", "사전은 디스크,\n색인만 메모리", "번호 목록은\n차이값으로", "차이값을\n비트로 꽉 채우기"]
    fig, ax = canvas(11, 2.2, 20, 3)
    for k, s in enumerate(steps):
        x = 0.2 + k * 4.0
        hot = k == 1
        box(ax, x, 0.6, 3.2, 1.8, fc=PINK if hot else NOTE, ec=RED if hot else INK)
        label(ax, x + 1.6, 1.5, s, fs=11, color=RED if hot else "#222")
        label(ax, x + 0.22, 2.15, str(k + 1), fs=10, color=INK, ha="left")
        if k < 4:
            arrow(ax, (x + 3.3, 1.5), (x + 3.9, 1.5), ms=14)
    save(fig, OUT, "es06-map.svg")


def node(ax, x, y, final=False, hot=False):
    ax.add_patch(Circle((x, y), 0.28, fc=PINK if hot else "white", ec=RED if hot else INK, lw=2.2 if final else 1.3))
    if final:
        ax.add_patch(Circle((x, y), 0.19, fc="none", ec=RED if hot else INK, lw=1.0))


def edge(ax, a, b, ch, hot=False):
    arrow(ax, a, b, color=RED if hot else INK, lw=1.5, ms=10)
    ax.text((a[0] + b[0]) / 2, (a[1] + b[1]) / 2 + 0.22, ch, ha="center", fontsize=11, color=RED if hot else "#222")


def trie():
    fig, ax = canvas(11, 4.4, 18, 7.2)
    label(ax, 0.3, 6.8, "낱말 넷: tap, taps, top, tops", fs=12, ha="left", bold=True)
    # 트라이
    label(ax, 4.2, 6.0, "트라이: 앞부분만 나눠 써요 (칸 8개)", fs=11, color=INK)
    P = {"r": (0.6, 3.2), "t": (1.9, 3.2), "ta": (3.2, 4.5), "to": (3.2, 1.9), "tap": (4.5, 4.5), "top": (4.5, 1.9),
         "taps": (5.8, 4.5), "tops": (5.8, 1.9)}
    for k, (x, y) in P.items():
        node(ax, x, y, final=k in ("tap", "taps", "top", "tops"))
    for a, b, ch in (("r", "t", "t"), ("t", "ta", "a"), ("t", "to", "o"), ("ta", "tap", "p"), ("to", "top", "p"),
                     ("tap", "taps", "s"), ("top", "tops", "s")):
        (x1, y1), (x2, y2) = P[a], P[b]
        edge(ax, (x1 + 0.28, y1), (x2 - 0.28, y2), ch)
    label(ax, 3.2, 0.9, "p, s 칸이 두 번씩 있어요", fs=10, color=INK)
    # 최소 자동자
    label(ax, 13.3, 6.0, "FST: 뒷부분도 나눠 써요 (칸 5개)", fs=11, color=RED)
    Q = {"r": (9.8, 3.2), "t": (11.1, 3.2), "m": (12.6, 3.2), "p": (14.1, 3.2), "s": (15.6, 3.2)}
    for k, (x, y) in Q.items():
        node(ax, x, y, final=k in ("p", "s"), hot=k in ("m", "p", "s"))
    edge(ax, (10.08, 3.2), (10.82, 3.2), "t")
    arrow(ax, (11.35, 3.35), (12.35, 3.35), color=RED, lw=1.5, ms=10, rad=-0.5)
    ax.text(11.85, 4.05, "a", ha="center", fontsize=11, color=RED)
    arrow(ax, (11.35, 3.05), (12.35, 3.05), color=RED, lw=1.5, ms=10, rad=0.5)
    ax.text(11.85, 2.2, "o", ha="center", fontsize=11, color=RED)
    edge(ax, (12.88, 3.2), (13.82, 3.2), "p", hot=True)
    edge(ax, (14.38, 3.2), (15.32, 3.2), "s", hot=True)
    label(ax, 12.9, 0.9, "ta-와 to-가 같은 꼬리 p, ps를 함께 써요", fs=10, color=RED)
    label(ax, 9.0, 0.2, "이중 원 = 여기서 끝나는 낱말이 있어요", fs=10, color=INK)
    save(fig, OUT, "es06-trie.svg")


def blocktree():
    fig, ax = canvas(11, 4.6, 18, 7.4)
    label(ax, 0.3, 7.0, "메모리(또는 mmap)", fs=12, ha="left", bold=True)
    box(ax, 0.3, 4.6, 6.0, 2.0, fc=PINK, ec=RED)
    label(ax, 3.3, 6.15, "블록 색인 (.tip)", fs=12, color=RED, bold=True)
    for k, t in enumerate(["sa…  → 블록 41", "se…  → 블록 42", "sh…  → 블록 43"]):
        label(ax, 0.8, 5.6 - k * 0.42, t, fs=10, ha="left", color=INK)
    ax.plot([0.2, 17.8], [4.1, 4.1], color=GREY, lw=1.5, ls="--")
    label(ax, 0.3, 3.65, "디스크", fs=12, ha="left", bold=True)
    for k, (name, ts) in enumerate((("블록 41", "sable … sawyer"), ("블록 42", "seal … sewer"), ("블록 43", "shack … shy"))):
        x = 0.3 + k * 4.4
        hot = k == 1
        box(ax, x, 1.2, 4.0, 1.9, fc=PINK if hot else NOTE, ec=RED if hot else INK, round_=False)
        label(ax, x + 2.0, 2.65, name, fs=11, color=RED if hot else "#222", bold=hot)
        label(ax, x + 2.0, 1.85, ts, fs=10, color=INK)
    label(ax, 7.0, 0.5, "용어 블록 (.tim): 낱말 수십 개씩 정렬해서 묶음", fs=11, color=INK)
    box(ax, 13.4, 5.0, 4.2, 1.2, fc=PAPER)
    label(ax, 15.5, 5.6, "찾기: search", fs=12)
    arrow(ax, (13.3, 5.6), (6.4, 5.45), color=RED)
    label(ax, 9.8, 5.95, "① 접두사로 블록 고르기", fs=10, color=RED)
    arrow(ax, (3.3, 4.5), (6.7, 3.2), color=RED)
    label(ax, 6.3, 3.75, "② 블록 하나만 읽어 훑기", fs=10, color=RED, ha="left")
    save(fig, OUT, "es06-blocktree.svg")


def postings():
    fig, ax = canvas(11, 4.4, 18, 7.0)
    ids = [3, 7, 8, 15, 21, 22, 40]
    d = [ids[0]] + [b - a for a, b in zip(ids, ids[1:])]
    label(ax, 0.3, 6.5, "환불의 포스팅 목록", fs=12, ha="left", bold=True)
    label(ax, 0.3, 5.45, "문서 번호", fs=11, ha="left", color=INK)
    cells(ax, 3.0, 5.05, ids, w=1.1, h=0.8)
    label(ax, 11.6, 5.45, "번호가 커질수록 자리도 커져요", fs=10, color=INK, ha="left")
    label(ax, 0.3, 3.75, "차이값", fs=11, ha="left", color=RED)
    cells(ax, 3.0, 3.35, d, w=1.1, h=0.8, hot=range(len(d)))
    label(ax, 11.6, 3.75, "앞 번호와의 차이만 적어요", fs=10, color=RED, ha="left")
    for k in range(1, len(ids)):
        ax.annotate("", xy=(3.55 + k * 1.18, 4.2), xytext=(3.55 + k * 1.18, 5.0), arrowprops=dict(arrowstyle="->", color=GREY))
    label(ax, 0.3, 1.95, "비트로", fs=11, ha="left", color=INK)
    bits = [format(x, "05b") for x in d]
    cells(ax, 3.0, 1.55, bits, w=1.1, h=0.8, fs=10)
    label(ax, 11.6, 1.95, "가장 큰 차이 18 → 5비트면 충분", fs=10, color=INK, ha="left")
    label(ax, 8.0, 0.5, "실제로는 128개씩 묶어 묶음마다 비트 수를 따로 정해요", fs=11, color=INK)
    save(fig, OUT, "es06-postings.svg")


if __name__ == "__main__":
    open_(); map_(); trie(); blocktree(); postings()
