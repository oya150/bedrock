"""Elasticsearch 5편 그림 만들기. 실행: python lab/fig_es05.py  → docs/elasticsearch/img/05/*.svg"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "es"))
from figkit import (GREY, INK, LIGHT, NOTE, PAPER, PINK, RED, arrow, box, canvas, cell, cells,  # noqa: E402
                    label, outdir, save, story)
from matplotlib.patches import Rectangle  # noqa: E402

OUT = outdir("05")


def open_():
    fig, ax = canvas(9, 3.4, 13, 5.0)
    for k, (t, n, kb, h) in enumerate((("지우기 전", "문서 300개", "20.7 kb", 2.4), ("100개 지운 뒤", "문서 200개", "25.9 kb", 3.0))):
        x = 1.5 + k * 5.0
        ax.add_patch(Rectangle((x, 0.8), 1.6, h, fc=NOTE if k == 0 else PINK, ec=RED if k else INK, lw=1.6))
        label(ax, x + 0.8, 0.4, t, fs=11)
        label(ax, x + 0.8, h + 1.1, n, fs=11, color=RED if k else "#222")
        label(ax, x + 0.8, 0.8 + h / 2, kb, fs=10, color=RED if k else INK)
    arrow(ax, (3.4, 2.0), (6.2, 2.0))
    label(ax, 9.6, 2.3, "지웠는데\n오히려 커졌어요", fs=12, color=RED, ha="left", bold=True)
    save(fig, OUT, "es05-open.svg")


def map_():
    """정리 절: 이 편이 한 말을 결론 문장으로."""
    story(["문서를 지우면 세그먼트는 그대로 두고 삭제 표시만 해요",
           "지운 문서는 검색에 안 나오지만 자리와 통계는 그대로 차지해요",
           "문서를 고치면 옛 문서에 삭제 표시를 하고 새 문서를 넣어요",
           "병합이 살아 있는 문서만 옮겨 적을 때 지운 문서가 실제로 빠져요",
           "보존 표시가 붙든 작업 기록은 병합해도 잠시 남아요"], 3, OUT, "es05-map.svg")


def livedocs():
    fig, ax = canvas(10, 3.6, 15, 5.4)
    label(ax, 0.3, 5.0, "세그먼트 _0", fs=12, ha="left", bold=True)
    label(ax, 0.3, 4.05, "문서", fs=11, ha="left", color=INK)
    label(ax, 0.3, 2.85, "살아 있나", fs=11, ha="left", color=INK)
    dead = {2, 4}
    for i in range(6):
        x = 2.4 + i * 1.3
        cell(ax, x, 3.7, 1.1, 0.75, f"문서 {i+1}", fs=10, dim=i in dead)
        if i in dead:
            ax.plot([x, x + 1.1], [3.7, 4.45], color=GREY, lw=1.5)
        cell(ax, x, 2.5, 1.1, 0.75, 0 if i in dead else 1, hot=i in dead, fs=12)
    label(ax, 10.5, 2.85, "← 지우면 이 칸만 0으로", fs=11, color=RED, ha="left")
    label(ax, 7.5, 1.4, "역색인과 문서는 그대로 두고, 검색할 때 0인 문서를 건너뛰어요", fs=11, color=INK)
    label(ax, 7.5, 0.6, "자리도 차지하고 낱말이 든 문서 수에도 그대로 세어져요", fs=11, color=INK)
    save(fig, OUT, "es05-livedocs.svg")


def update():
    fig, ax = canvas(10, 3.2, 15, 4.8)
    box(ax, 0.3, 1.6, 6.2, 2.4, fc=NOTE)
    label(ax, 0.6, 3.6, "세그먼트 _1 (옛것)", fs=11, ha="left")
    cell(ax, 0.8, 2.2, 2.5, 0.9, "101: 환불 문의", dim=True, fs=10)
    ax.plot([0.8, 3.3], [2.2, 3.1], color=GREY, lw=1.5)
    label(ax, 4.9, 2.65, "지웠다고\n표시", fs=10, color=RED)
    box(ax, 8.3, 1.6, 6.2, 2.4, fc=PINK, ec=RED)
    label(ax, 8.6, 3.6, "새 세그먼트", fs=11, ha="left", color=RED)
    cell(ax, 8.8, 2.2, 3.4, 0.9, "101: 환불 문의 수정", hot=True, fs=10)
    arrow(ax, (6.7, 2.65), (8.1, 2.65), color=RED)
    label(ax, 7.4, 0.8, "고치기 = 옛 문서에 삭제 표시 + 새 문서를 새 세그먼트에", fs=11, color=INK)
    save(fig, OUT, "es05-update.svg")


def merge():
    fig, ax = canvas(10.5, 4.2, 16, 6.4)
    segs = [("가", 6, {1, 3, 4}), ("나", 6, {0}), ("다", 6, set())]
    for k, (n, c, dead) in enumerate(segs):
        x = 0.3 + k * 3.4
        box(ax, x, 3.7, 3.1, 2.0, fc=NOTE)
        label(ax, x + 1.55, 5.35, f"세그먼트 {n}", fs=11)
        for i in range(c):
            xx = x + 0.2 + (i % 3) * 0.95
            yy = 4.55 - (i // 3) * 0.7
            cell(ax, xx, yy, 0.8, 0.55, "", dim=i in dead, fc=None if i in dead else "white")
            if i in dead:
                ax.plot([xx, xx + 0.8], [yy, yy + 0.55], color=GREY, lw=1.2)
    for k in range(3):
        arrow(ax, (1.85 + k * 3.4, 3.6), (5.35, 2.35), lw=1.4, ms=12)
    label(ax, 7.9, 3.1, "병합", fs=12, color=RED, bold=True, ha="left")
    box(ax, 2.3, 0.3, 6.1, 1.9, fc=PINK, ec=RED)
    label(ax, 5.35, 1.9, "새 세그먼트 (살아 있는 문서만 새로 씀)", fs=11, color=RED)
    for i in range(14):
        cell(ax, 2.55 + (i % 7) * 0.8, 0.95 - (i // 7) * 0.55, 0.7, 0.45, "", fc="white")
    label(ax, 10.6, 4.6, "지운 문서 4개는\n새 세그먼트에\n옮겨 적지 않아요", fs=11, color=RED, ha="left")
    label(ax, 10.6, 1.4, "옛 세그먼트 셋은\n다 쓰고 나면 지워요", fs=11, color=INK, ha="left")
    save(fig, OUT, "es05-merge.svg")


def cost():
    """병합 중에는 옛 세그먼트와 새 세그먼트가 함께 있다."""
    fig, ax = canvas(10, 3.0, 15, 4.6)
    label(ax, 0.3, 4.2, "병합 중", fs=12, ha="left", bold=True)
    for k in range(3):
        cell(ax, 0.3 + k * 1.5, 2.6, 1.3, 1.0, "가나다"[k], fs=10.5)
    box(ax, 0.3, 1.1, 4.3, 1.1, fc=PINK, ec=RED)
    label(ax, 2.45, 1.65, "새 세그먼트 (만드는 중)", fs=10.5, color=RED)
    arrow(ax, (5.2, 2.4), (8.2, 2.4))
    label(ax, 8.8, 4.2, "병합 뒤", fs=12, ha="left", bold=True)
    box(ax, 8.8, 1.1, 4.3, 1.1, fc=NOTE)
    label(ax, 10.95, 1.65, "새 세그먼트", fs=10.5)
    label(ax, 7.5, 0.35, "합치는 동안은 옛 것과 새것이 함께 있어 디스크를 잠시 더 써요", fs=10.5, color=INK)
    save(fig, OUT, "es05-cost.svg")


def lease():
    """작업 번호 줄과 보존 표시(실험에서 지운 직후)."""
    fig, ax = canvas(10.5, 3.4, 16, 5.2)
    label(ax, 15.6, 4.8, "시퀀스 번호 →", fs=11, ha="right", bold=True)
    groups = [("1~100 넣기\n(지운 원래 글)", True), ("101~200\n넣기", False), ("201~300\n넣기", False), ("301~400 지우기\n(빈 문서)", True)]
    for k, (t, dead) in enumerate(groups):
        x = 0.6 + k * 3.7
        cell(ax, x, 2.6, 3.3, 1.2, t, dim=dead, fs=9.5)
    xf = 0.6 + 3 * 3.7 - 0.2
    ax.plot([xf, xf], [2.3, 4.3], color=RED, lw=2.5)
    ax.add_patch(Rectangle((xf, 3.9), 0.8, 0.4, fc=RED, ec=RED))
    label(ax, xf - 0.2, 4.55, "보존 표시", fs=10.5, color=RED, ha="right", bold=True)
    label(ax, 2.25, 1.9, "커밋 전이라 남음", fs=10, color=INK)
    label(ax, 13.4, 1.9, "보존 표시가 붙듦", fs=10, color=RED)
    label(ax, 8.0, 0.8, "보존 표시보다 뒤 번호를 단 지운 문서는 병합해도 남겨 둬요", fs=11, color=INK, bold=True)
    save(fig, OUT, "es05-lease.svg")


def retain():
    """지운 직후 강제 병합과 70초 뒤 병합."""
    fig, ax = canvas(10.5, 3.2, 16, 4.8)
    steps = [("100개 지우기", False), ("바로 강제 병합\n지운 문서 200 그대로", True), ("70초 뒤 다시 병합\n지운 문서 0", False)]
    for k, (t, hot) in enumerate(steps):
        x = 0.3 + k * 5.3
        box(ax, x, 2.6, 4.6, 1.5, fc=PINK if hot else NOTE, ec=RED if hot else INK)
        label(ax, x + 2.3, 3.35, t, fs=10.5, color=RED if hot else "#222")
        if k < 2:
            arrow(ax, (x + 4.65, 3.35), (x + 5.25, 3.35), ms=12)
    label(ax, 8.0, 1.75, "지운 문서를 버리려면 두 가지가 필요해요", fs=11, color=INK, bold=True)
    label(ax, 8.0, 1.05, "보존 표시가 옮겨 가고(30초마다), 그 기록까지 담은 커밋이 있어야 해요", fs=10.5, color=INK)
    save(fig, OUT, "es05-retain.svg")


def tomb():
    """지우기는 빈 문서를 남긴다."""
    fig, ax = canvas(10.5, 3.2, 16, 4.8)
    box(ax, 0.3, 1.9, 6.6, 2.2, fc=NOTE)
    label(ax, 0.6, 3.75, "세그먼트 _0 (원래 글)", fs=11, ha="left")
    cells(ax, 0.6, 2.3, ["글 1", "글 2", "…", "글 100"], w=1.4, h=0.8, fs=10, dim=(0, 1, 2, 3))
    label(ax, 3.6, 1.55, "지운 글 100 (삭제 표시)", fs=10.5, color=INK)
    box(ax, 8.3, 1.9, 7.4, 2.2, fc=PINK, ec=RED)
    label(ax, 8.6, 3.75, "새 세그먼트 _3", fs=11, ha="left", color=RED)
    cells(ax, 8.6, 2.3, ["1번 지움", "2번 지움", "…", "100번 지움"], w=1.6, h=0.8, fs=9.5, dim=(0, 1, 2, 3))
    label(ax, 12.0, 1.55, "빈 문서 100 (처음부터 지운 상태)", fs=10.5, color=RED)
    label(ax, 8.0, 0.6, "지운 글 100 + 빈 문서 100 = 지운 문서 수 200", fs=11, color=INK, bold=True)
    save(fig, OUT, "es05-tomb.svg")


def decide():
    fig, ax = canvas(10, 3.6, 15, 5.4)
    box(ax, 0.3, 3.6, 6.0, 1.3, fc=NOTE)
    label(ax, 3.3, 4.25, "이 인덱스에 앞으로 더 쓰나요?", fs=10.5, bold=True)
    arrow(ax, (6.4, 4.25), (8.4, 4.25), color=RED); label(ax, 7.4, 4.55, "예", fs=10, color=RED)
    box(ax, 8.5, 3.6, 6.2, 1.3, fc=PINK, ec=RED)
    label(ax, 11.6, 4.25, "강제 병합하지 말고 ES에 맡겨요", fs=10.5, color=RED, bold=True)
    arrow(ax, (3.3, 3.5), (3.3, 2.6)); label(ax, 3.6, 3.05, "아니요", fs=10, color=INK, ha="left")
    box(ax, 0.3, 1.3, 6.0, 1.2, fc=PAPER)
    label(ax, 3.3, 1.9, "세그먼트 하나로 강제 병합해도 좋아요\n(검색이 빨라지고 디스크가 줄어요)", fs=10)
    box(ax, 8.5, 1.3, 6.2, 1.2, fc=LIGHT, ec=GREY)
    label(ax, 11.6, 1.9, "기간 지난 데이터를 지우려면\n기간별 인덱스를 통째로 지워요", fs=10, color=INK)
    save(fig, OUT, "es05-decide.svg")


def recover():
    """복제본을 맞추는 두 길과 각각 필요한 기록."""
    fig, ax = canvas(10.5, 3.6, 16, 5.4)
    rows = ((3.2, "잠깐 끊겼다 돌아온 복제본", ["빠진 작업만 다시 보내요"], "보존 표시가 붙들어요", False),
            (0.7, "새로 붙는 복제본", ["① 커밋 하나의 파일을 복사해 줘요", "② 커밋 뒤의 작업을 따로 보내요"], "커밋 조건", True))
    for y, title, steps, need, hot in rows:
        label(ax, 0.3, y + 1.5, title, fs=11, ha="left", bold=True)
        box(ax, 0.3, y, 2.4, 1.1, fc=NOTE); label(ax, 1.5, y + 0.55, "주 샤드", fs=10.5)
        x = 3.2
        for k, st in enumerate(steps):
            w = 4.6 if len(steps) > 1 else 6.0
            arrow(ax, (x - 0.4, y + 0.55), (x, y + 0.55), ms=10)
            box(ax, x, y, w, 1.1, fc=PAPER); label(ax, x + w / 2, y + 0.55, st, fs=9.5)
            x += w + 0.5
        arrow(ax, (x - 0.4, y + 0.55), (x, y + 0.55), ms=10)
        box(ax, x, y, 15.7 - x, 1.1, fc=PINK if hot else NOTE, ec=RED if hot else INK)
        label(ax, x + (15.7 - x) / 2, y + 0.55, "그 작업 기록이 필요\n(" + need + ")", fs=9.5, color=RED if hot else "#222")
    save(fig, OUT, "es05-recover.svg")


def bigseg():
    """계속 쓰는 인덱스를 강제 병합했을 때."""
    fig, ax = canvas(10.5, 3.2, 16, 4.8)
    titles = ["강제 병합 직후", "계속 쓰는 동안", "지운 문서가 많이 쌓인 뒤"]
    deads = [0, 6, 14]
    for k in range(3):
        x = 0.3 + k * 5.3
        hot = k == 2
        label(ax, x + 2.3, 4.4, titles[k], fs=11, bold=True, color=RED if hot else "#222")
        box(ax, x, 1.4, 4.6, 2.5, fc=PINK if hot else NOTE, ec=RED if hot else INK)
        for i in range(20):
            cx = x + 0.25 + (i % 5) * 0.85
            cy = 3.25 - (i // 5) * 0.5
            cell(ax, cx, cy, 0.7, 0.38, "", dim=i < deads[k], fc=None if i < deads[k] else "white")
        if k < 2:
            arrow(ax, (x + 4.65, 2.65), (x + 5.25, 2.65), ms=12)
    label(ax, 2.6, 0.9, "5 GB를 넘는 세그먼트 하나", fs=10, color=INK)
    label(ax, 7.9, 0.9, "옛 판이 쌓여도 평소 병합은 손대지 않아요", fs=10, color=INK)
    label(ax, 13.2, 0.9, "큰 세그먼트 전체를 한꺼번에 다시 써요", fs=10, color=RED)
    save(fig, OUT, "es05-bigseg.svg")


if __name__ == "__main__":
    open_(); map_(); livedocs(); update(); merge(); cost(); lease(); retain(); tomb(); decide(); recover(); bigseg()
