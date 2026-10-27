"""길 안내 그림. 실행: python lab/fig_paths.py  → docs/img/paths.svg

단계 세 칸에 글 상자를 놓고 본문 링크로 이어진 글끼리 화살표를 긋는다. 길마다 색이 다르다.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "es"))
from figkit import BLUE, GREEN, INK, NOTE, RED, YEL, arrow, box, canvas, label, save  # noqa: E402

OUT = os.environ.get("FIG_OUT") or os.path.join(os.path.dirname(__file__), "..", "docs", "img")
os.makedirs(OUT, exist_ok=True)

COLX = {1: 0.4, 2: 7.4, 3: 14.4}
W, H = 5.6, 1.0
NODES = {   # 이름: (단계, 줄, 글자)
    "c1": (1, 0, "컴퓨터 1편\n컴퓨터는 무엇을 할 줄 아나요"),
    "c6": (1, 1, "컴퓨터 6편\n컴퓨터에게 일을 어떻게 시키나요"),
    "c12": (1, 3, "컴퓨터 12편\n검색하면 어떻게 바로 찾을까요"),
    "a1": (2, 0.5, "알고리즘 1편\n양말이 두 배면 일은 몇 배가 될까요"),
    "a3": (2, 2.5, "알고리즘 3편\n업다운 놀이는 왜 금방 맞힐까요"),
    "a11": (2, 3.5, "알고리즘 11편\n창고 속 카드는 어떻게 빨리 찾을까요"),
    "a10": (2, 5, "알고리즘 10편\n가장 급한 것을 어떻게 늘 빨리 꺼낼까요"),
    "a9": (2, 6.5, "알고리즘 9편\n이름으로 어떻게 바로 찾을까요"),
    "e1": (3, 2.5, "ES 1편\n검색 엔진은 왜 목록을 거꾸로 만들어 둘까요"),
    "e11": (3, 3.5, "ES 11편\n숫자·날짜 범위 검색은 왜 빠를까요"),
    "e7": (3, 4.5, "ES 7편\nAND 검색은 어떻게 빨리 겹치는 걸 찾을까요"),
    "e9": (3, 5.5, "ES 9편\n상위 10개만 필요하면 왜 다 계산하지 않아도 될까요"),
    "e12": (3, 6.5, "ES 12편\n샤드 여러 개의 결과를 어떻게 합칠까요"),
    "e3": (3, 7.5, "ES 3편\n샤드 수는 왜 나중에 못 바꿀까요"),
    "e13": (3, 8.5, "ES 13편\n고유 사용자 수는 왜 근삿값일까요"),
}
PATHS = [   # 색, 이름, 이어진 글
    (GREEN, "일이 얼마나 늘어날까", [("c1", "a1"), ("c6", "a1")]),
    (BLUE, "많은 것 중에서 빨리 찾기", [("c12", "a3"), ("c12", "a11"), ("a3", "e1"), ("a11", "e1"),
                                         ("a11", "e7"), ("a11", "e11")]),
    (RED, "급한 것부터 꺼내기", [("a10", "e7"), ("a10", "e9"), ("a10", "e12")]),
    (YEL, "이름으로 자리 정하기", [("a9", "e3"), ("a9", "e13")]),
]
ROWS = 9.5


def ypos(row):
    return (ROWS - row) * 1.25


def main():
    fig, ax = canvas(14, 10.4, 20.4, ypos(-1.4) + 0.4)
    for st, x in COLX.items():
        label(ax, x + W / 2, ypos(-1.0), ["", "1단계 · 누구나", "2단계 · 코드 입문", "3단계 · 실제 소프트웨어"][st],
              fs=13, bold=True)
    color_of = {}
    for c, _, edges in PATHS:
        for a, b in edges:
            color_of.setdefault(a, c); color_of.setdefault(b, c)
    for c, _, edges in PATHS:
        for a, b in edges:
            sa, ra, _ = NODES[a]; sb, rb, _ = NODES[b]
            arrow(ax, (COLX[sa] + W + 0.1, ypos(ra) + H / 2), (COLX[sb] - 0.1, ypos(rb) + H / 2),
                  color=c, lw=2, ms=14)
    for name, (st, row, text) in NODES.items():
        box(ax, COLX[st], ypos(row), W, H, fc=NOTE, ec=color_of.get(name, INK), lw=2.2)
        top, bottom = text.split("\n")
        label(ax, COLX[st] + 0.2, ypos(row) + 0.72, top, fs=10, bold=True, ha="left")
        label(ax, COLX[st] + 0.2, ypos(row) + 0.3, bottom, fs=9.5, ha="left")
    for k, (c, name, _) in enumerate(PATHS):
        x = 0.4 + k * 5.0
        ax.plot([x, x + 0.8], [ypos(ROWS - 0.2), ypos(ROWS - 0.2)], color=c, lw=4)
        label(ax, x + 1.0, ypos(ROWS - 0.2), name, fs=10.5, ha="left")
    save(fig, OUT, "paths.svg")


if __name__ == "__main__":
    main()
