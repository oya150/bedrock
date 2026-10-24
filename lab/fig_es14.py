"""Elasticsearch 14편 그림 만들기. 실행: python lab/fig_es14.py  → docs/elasticsearch/img/14/*.svg"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "es"))
from figkit import (BLUE, GREY, INK, LIGHT, NOTE, PAPER, PINK, RED, arrow, box, canvas, cell, cells,  # noqa: E402
                    label, outdir, plt, save)

OUT = outdir("14")


def open_():
    fig, ax = canvas(11, 3.2, 20, 5.6)
    steps = [("0초", "es03이 꺼짐\n(주 샤드·마스터)", True),
             ("5초 뒤", "es02가 주 샤드\nes01이 마스터", False),
             ("그동안", "쓰기 50건 계속\nprimary term 1→2", False),
             ("다시 켜면", "es03은 작업 기록으로\n따라잡아요", False)]
    for k, (t, s, hot) in enumerate(steps):
        x = 0.3 + k * 5.0
        label(ax, x + 2.0, 4.9, t, fs=11, color=RED if hot else INK, bold=True)
        box(ax, x, 1.8, 4.0, 2.6, fc=PINK if hot else NOTE, ec=RED if hot else INK)
        label(ax, x + 2.0, 3.1, s, fs=11, color=RED if hot else "#222")
        if k < 3:
            arrow(ax, (x + 4.1, 3.1), (x + 4.9, 3.1), ms=14)
    label(ax, 10.0, 0.8, "검색은 내내 답했고 문서는 한 건도 사라지지 않았어요", fs=11, color=INK)
    save(fig, OUT, "es14-open.svg")


def map_():
    steps = ["같은 샤드를\n여러 노드에", "쓰기마다\n시퀀스 번호", "체크포인트로\n어디까지 같은지", "주 샤드 교체와\n따라잡기", "마스터는\n과반으로 뽑기"]
    fig, ax = canvas(11, 2.2, 20, 3)
    for k, s in enumerate(steps):
        x = 0.2 + k * 4.0
        hot = k == 2
        box(ax, x, 0.6, 3.2, 1.8, fc=PINK if hot else NOTE, ec=RED if hot else INK)
        label(ax, x + 1.6, 1.5, s, fs=11, color=RED if hot else "#222")
        label(ax, x + 0.22, 2.15, str(k + 1), fs=10, color=INK, ha="left")
        if k < 4:
            arrow(ax, (x + 3.3, 1.5), (x + 3.9, 1.5), ms=14)
    save(fig, OUT, "es14-map.svg")


def copies():
    fig, ax = canvas(11, 4.6, 19, 8.0)
    label(ax, 0.3, 7.5, "쓰기 10건(시퀀스 번호 0~9)이 세 복사본에 닿은 모습", fs=12, ha="left", bold=True)
    rows = [("주 샤드 (노드 A)", set(range(10)), 9),
            ("복제본 1 (노드 B)", {0, 1, 2, 3, 4, 5, 6, 7, 9}, 7),
            ("복제본 2 (노드 C)", {0, 1, 2, 3, 4, 5}, 5)]
    for k, (name, got, lcp) in enumerate(rows):
        y = 5.9 - k * 1.6
        label(ax, 0.3, y + 0.35, name, fs=11, ha="left")
        for i in range(10):
            has = i in got
            cell(ax, 4.6 + i * 0.85, y, 0.78, 0.75, str(i) if has else "", hot=False, dim=not has, fs=11,
                 fc="white" if has else LIGHT)
        label(ax, 13.4, y + 0.35, f"로컬 체크포인트 {lcp}", fs=11, ha="left", color=RED if lcp == 5 else "#222",
              bold=lcp == 5)
    # 글로벌 체크포인트 선
    gx = 4.6 + 6 * 0.85 - 0.04
    ax.plot([gx, gx], [2.3, 7.0], color=RED, lw=2.2, ls="--")
    label(ax, gx, 1.85, "글로벌 체크포인트 5 = 세 복사본의 최솟값", fs=11, color=RED, bold=True)
    label(ax, gx, 1.05, "왼쪽(0~5)은 세 곳 모두에 있어요. 오른쪽만 복사본마다 다를 수 있어요", fs=10, color=INK)
    save(fig, OUT, "es14-checkpoints.svg")


def quorum():
    fig, ax = canvas(11, 3.4, 20, 6.0)
    label(ax, 0.3, 5.6, "마스터 후보 5개가 네트워크로 3 대 2로 갈라지면", fs=12, ha="left", bold=True)
    box(ax, 0.6, 0.9, 10.2, 4.0, fc=NOTE)
    box(ax, 11.6, 0.9, 7.8, 4.0, fc=PAPER)
    for k in range(3):
        box(ax, 1.4 + k * 3.1, 2.6, 2.3, 1.4, fc=PINK if k == 0 else "white", ec=RED if k == 0 else INK)
        label(ax, 2.55 + k * 3.1, 3.3, "마스터" if k == 0 else "후보", fs=11, color=RED if k == 0 else "#222")
    label(ax, 5.7, 1.5, "3표 = 과반(5의 절반보다 많음) → 마스터를 뽑아요", fs=11, color=RED, bold=True)
    for k in range(2):
        box(ax, 12.6 + k * 3.2, 2.6, 2.3, 1.4, fc="white", ec=GREY)
        label(ax, 13.75 + k * 3.2, 3.3, "후보", fs=11, color=GREY)
    label(ax, 15.5, 1.5, "2표 → 마스터 없음, 쓰기 막힘", fs=11, color=INK)
    ax.plot([11.2, 11.2], [0.6, 5.2], color=INK, lw=2, ls=(0, (4, 3)))
    save(fig, OUT, "es14-quorum.svg")


if __name__ == "__main__":
    open_(); map_(); copies(); quorum()
