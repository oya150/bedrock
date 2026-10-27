"""Elasticsearch 1편 그림 만들기. 실행: python lab/fig_es01.py  → docs/elasticsearch/img/01/*.svg"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "es"))
from figkit import (GREY, INK, LIGHT, NOTE, PAPER, PINK, RED, arrow, box, canvas, cell, cells,  # noqa: E402
                    label, outdir, save)

OUT = outdir("01")


def scan():
    rows = ["배송은 언제 오나요", "환불 요청합니다", "사이즈 교환 문의", "주문 취소했어요",
            "환불 언제 들어오나요", "색상이 달라요"]
    fig, ax = canvas(8.4, 4.6, 12, 6.6)
    label(ax, 0.3, 6.25, "posts 표", fs=12, ha="left", bold=True)
    cell(ax, 0.3, 5.45, 0.8, 0.6, "id", fc=PAPER); cell(ax, 1.1, 5.45, 5.0, 0.6, "body", fc=PAPER)
    for k, r in enumerate(rows):
        y = 4.75 - k * 0.7
        hot = "환불" in r
        cell(ax, 0.3, y, 0.8, 0.6, k + 1, hot=hot); cell(ax, 1.1, y, 5.0, 0.6, r, hot=hot)
    label(ax, 3.6, 0.55, "⋮  (글이 백만 개)", fs=12, color=INK)
    for k in range(5):
        y = 4.75 - k * 0.7 + 0.3
        arrow(ax, (6.4, y), (6.4, y - 0.62), color=RED, lw=1.6, ms=12)
    label(ax, 6.75, 4.0, "1번 글부터\n한 줄씩 다 읽어요", fs=12, ha="left", color=RED)
    box(ax, 6.7, 1.0, 5.1, 1.1, fc=NOTE)
    label(ax, 9.25, 1.55, "WHERE body LIKE '%환불%'", fs=12)
    save(fig, OUT, "es01-scan.svg")


def map_():
    steps = ["한 줄씩\n다 보기", "글마다\n낱말 목록", "뒤집기:\n낱말마다 글 목록", "목록 꺼내서\n합치기"]
    fig, ax = canvas(10, 2.3, 16, 3)
    for k, s in enumerate(steps):
        x = 0.3 + k * 4.0
        box(ax, x, 0.6, 3.1, 1.8, fc=PINK if k == 2 else NOTE, ec=RED if k == 2 else INK)
        label(ax, x + 1.55, 1.5, s, fs=12, color=RED if k == 2 else "#222")
        label(ax, x + 0.25, 2.15, str(k + 1), fs=10, color=INK, ha="left")
        if k < 3:
            arrow(ax, (x + 3.2, 1.5), (x + 3.9, 1.5))
    save(fig, OUT, "es01-map.svg")


DOCS = {1: ["주문", "환불", "요청"], 2: ["주문", "배송", "언제"], 3: ["환불", "완료", "감사"]}


def flip():
    fig, ax = canvas(10, 5.0, 15, 7.9)
    label(ax, 2.6, 6.8, "글마다 낱말 목록", fs=13, bold=True)
    for k, (d, ws) in enumerate(DOCS.items()):
        y = 5.4 - k * 1.3
        cell(ax, 0.3, y, 1.0, 0.8, f"글 {d}", fc=PAPER)
        cells(ax, 1.5, y, ws, w=1.1, hot=[i for i, w in enumerate(ws) if w == "환불"])
    arrow(ax, (5.3, 3.8), (6.9, 3.8), lw=3, ms=26, color=RED)
    label(ax, 6.1, 4.4, "뒤집기", fs=13, color=RED, bold=True)

    inv = {}
    for d, ws in DOCS.items():
        for w in ws:
            inv.setdefault(w, []).append(d)
    terms = sorted(inv)
    label(ax, 10.0, 7.55, "낱말마다 글 목록 (역색인)", fs=13, bold=True)
    for k, t in enumerate(terms):
        y = 6.05 - k * 0.78
        hot = t == "환불"
        cell(ax, 7.6, y, 1.3, 0.66, t, hot=hot)
        arrow(ax, (9.0, y + 0.33), (9.6, y + 0.33), lw=1.4, ms=10, color=RED if hot else INK)
        cells(ax, 9.7, y, inv[t], w=0.7, h=0.66, hot=range(len(inv[t])) if hot else ())
    label(ax, 8.25, 6.85, "용어 사전 (가나다순)", fs=10, color=INK)
    label(ax, 11.6, 6.85, "포스팅 목록 (글 번호순)", fs=10, color=INK)
    save(fig, OUT, "es01-flip.svg")


def lookup():
    terms = ["감사", "배송", "언제", "완료", "요청", "주문", "환불"]
    fig, ax = canvas(10, 3.6, 15, 5.2)
    cells(ax, 0.3, 3.2, terms, w=1.3, h=0.8, hot=(6,))
    # 이진 탐색: 가운데(완료) → 남은 반의 가운데(주문) → 환불
    for n, i in enumerate((3, 5, 6)):
        x = 0.3 + i * 1.38 + 0.65
        hot = i == 6
        arrow(ax, (x, 2.0), (x, 3.1), color=RED if hot else INK, lw=1.6, ms=12)
        label(ax, x, 1.55, f"{'①②③'[n]} {terms[i]}", fs=11, color=RED if hot else INK, bold=hot)
    label(ax, 0.3 + 3 * 1.38 + 0.65, 0.95, "가나다순이라 볼 때마다 반씩 버려요", fs=11, color=INK)
    x_end = 0.3 + 6 * 1.38 + 1.3
    arrow(ax, (x_end + 0.1, 3.6), (x_end + 1.0, 3.6), color=RED)
    cells(ax, x_end + 1.1, 3.2, [1, 3], w=0.8, h=0.8, hot=(0, 1))
    label(ax, x_end + 1.95, 2.7, "글 1, 3", fs=11, color=RED)
    save(fig, OUT, "es01-lookup.svg")


def and_():
    a = [2, 5, 9, 14, 20]
    b = [1, 5, 8, 14, 21, 30]
    fig, ax = canvas(10, 3.4, 15, 4.6)
    label(ax, 0.3, 3.55, "환불", fs=12, ha="left", bold=True)
    label(ax, 0.3, 1.55, "주문", fs=12, ha="left", bold=True)
    cells(ax, 1.6, 3.15, a, w=1.0, h=0.8, hot=(1, 3))
    cells(ax, 1.6, 1.15, b, w=1.0, h=0.8, hot=(1, 3))
    for x0 in (1.6 + 1 * 1.08 + 0.5, 1.6 + 3 * 1.08 + 0.5):
        ax.plot([x0, x0], [2.0, 3.1], color=RED, lw=2)
    label(ax, 8.4, 2.55, "둘 다 있는 글: 5, 14", fs=12, color=RED, ha="left", bold=True)
    label(ax, 8.4, 0.5, "작은 번호 쪽을 한 칸씩 앞으로.\n두 목록을 한 번씩만 훑어요.", fs=11, ha="left", color=INK)
    save(fig, OUT, "es01-and.svg")


def forward():
    """글마다 낱말 목록만 있으면 '환불이 든 글'을 찾으려고 카드를 다 열어 봐야 한다."""
    fig, ax = canvas(10, 3.6, 15, 5.0)
    box(ax, 0.3, 3.7, 3.6, 0.9, fc=PINK, ec=RED)
    label(ax, 2.1, 4.15, "환불이 든 글은?", fs=12, color=RED, bold=True)
    for k, (d, ws) in enumerate(DOCS.items()):
        y = 2.6 - k * 1.05
        cell(ax, 5.6, y, 1.0, 0.8, f"글 {d}", fc=PAPER)
        cells(ax, 6.8, y, ws, w=1.1, hot=[i for i, w in enumerate(ws) if w == "환불"])
        arrow(ax, (3.9, 4.0), (5.5, y + 0.4), color=RED, lw=1.6, ms=12)
        label(ax, 10.4, y + 0.4, ("첫째", "둘째", "셋째")[k] + "로 열어 봐요", fs=10.5, color=INK, ha="left")
    label(ax, 2.1, 1.3, "목록이 '글 → 낱말' 방향이라\n글을 하나씩 다 열어 봐야 해요", fs=11, color=INK)
    save(fig, OUT, "es01-forward.svg")


def speed():
    """실측 표를 막대로: 200 ms와 0.01 ms."""
    fig, ax = canvas(10, 2.6, 15, 3.4)
    label(ax, 0.3, 2.55, "글마다 하나씩 확인", fs=11.5, ha="left")
    ax.add_patch(__import__("matplotlib").patches.Rectangle((4.0, 2.25), 9.5, 0.6, fc=GREY, ec=INK))
    label(ax, 13.6, 2.55, "약 200 ms", fs=11, ha="left")
    label(ax, 0.3, 1.25, "역색인에서 찾기", fs=11.5, ha="left", color=RED, bold=True)
    ax.add_patch(__import__("matplotlib").patches.Rectangle((4.0, 0.95), 0.03, 0.6, fc=RED, ec=RED))
    label(ax, 4.2, 1.25, "약 0.01 ms  (막대가 안 보일 만큼 짧아요)", fs=11, ha="left", color=RED)
    save(fig, OUT, "es01-speed.svg")


def cost():
    """미리 만들기 1초 = 하나씩 검색 다섯 번. 그 뒤 검색은 거의 공짜."""
    fig, ax = canvas(10, 3.4, 15, 4.6)
    label(ax, 0.3, 3.9, "역색인 없이", fs=12, ha="left", bold=True)
    for k in range(5):
        cell(ax, 3.0 + k * 1.95, 3.5, 1.85, 0.75, f"검색 {k + 1}", fc=LIGHT, fs=11)
    label(ax, 13.0, 3.87, "…검색할 때마다\n0.2초씩", fs=10, ha="left", color=INK)
    label(ax, 0.3, 1.9, "역색인 있으면", fs=12, ha="left", bold=True, color=RED)
    cell(ax, 3.0, 1.5, 9.7, 0.75, "처음 한 번 만들기 (약 1초)", fc=PINK, fs=11)
    for k in range(6):
        ax.plot([12.85 + k * 0.28] * 2, [1.5, 2.25], color=RED, lw=2)
    label(ax, 13.0, 1.05, "그다음 검색은\n거의 0초", fs=10, ha="left", color=RED)
    label(ax, 7.8, 0.4, "검색을 다섯 번 넘게 하면 미리 만든 쪽이 이득이에요", fs=11, color=INK)
    save(fig, OUT, "es01-cost.svg")


def miss():
    """낱말을 띄어쓰기로만 자르면 '환불했어요'는 '환불'로 안 찾힌다."""
    fig, ax = canvas(10, 3.0, 15, 4.0)
    cell(ax, 0.3, 2.6, 4.2, 0.8, "글: 환불했어요 감사", fc=PAPER, fs=11)
    arrow(ax, (4.6, 3.0), (5.6, 3.0))
    label(ax, 5.1, 3.55, "띄어쓰기로 자르기", fs=9.5, color=INK)
    cells(ax, 5.7, 2.6, ["환불했어요", "감사"], w=2.0, h=0.8, fs=11)
    label(ax, 7.8, 2.2, "역색인에 올라간 낱말", fs=9.5, color=INK)
    box(ax, 10.6, 2.5, 4.1, 1.0, fc=PINK, ec=RED)
    label(ax, 12.65, 3.0, "\"환불\"로 찾으면\n사전에 없어요 ✗", fs=11, color=RED)
    box(ax, 0.3, 0.4, 14.4, 1.0, fc=NOTE)
    label(ax, 7.5, 0.9, "LIKE '%환불%'은 글 속 글자를 훑어서 이 글도 찾아요. 그래서 ES로 옮기면 찾히는 글이 달라져요(2편).",
          fs=10.5)
    save(fig, OUT, "es01-miss.svg")


def decide():
    """언제 역색인을 만들까: 자주 찾나 → 글 중간 낱말로 찾나."""
    fig, ax = canvas(10, 4.2, 15, 6.0)
    box(ax, 0.3, 4.4, 4.4, 1.2, fc=NOTE)
    label(ax, 2.5, 5.0, "자주 찾나요?", fs=12, bold=True)
    box(ax, 5.6, 4.4, 4.4, 1.2, fc=NOTE)
    label(ax, 7.8, 5.0, "글 중간의 낱말로\n찾나요?", fs=12, bold=True)
    box(ax, 10.9, 4.4, 3.8, 1.2, fc=PINK, ec=RED)
    label(ax, 12.8, 5.0, "역색인\n(ES)", fs=12, color=RED, bold=True)
    arrow(ax, (4.8, 5.0), (5.5, 5.0)); label(ax, 5.15, 5.45, "예", fs=10, color=INK)
    arrow(ax, (10.1, 5.0), (10.8, 5.0), color=RED); label(ax, 10.45, 5.45, "예", fs=10, color=RED)
    arrow(ax, (2.5, 4.3), (2.5, 2.9)); label(ax, 2.85, 3.6, "아니요", fs=10, color=INK, ha="left")
    arrow(ax, (7.8, 4.3), (7.8, 2.9)); label(ax, 8.15, 3.6, "아니요", fs=10, color=INK, ha="left")
    box(ax, 0.3, 0.6, 4.4, 2.2, fc=LIGHT, ec=GREY)
    label(ax, 2.5, 1.7, "그때그때 훑기\n예: 한 달에 몇 번\n로그에서 주문번호 찾기", fs=10.5)
    box(ax, 5.6, 0.6, 4.4, 2.2, fc=LIGHT, ec=GREY)
    label(ax, 7.8, 1.7, "데이터베이스 인덱스\n예: '청바'로 시작하는\n상품 이름 찾기", fs=10.5)
    save(fig, OUT, "es01-decide.svg")


def blocks():
    """심화: 사전 전체를 메모리에 두지 않고 '어느 블록에 있나'만 작게 둔다."""
    fig, ax = canvas(10, 3.6, 15, 4.8)
    box(ax, 0.3, 1.2, 3.4, 2.6, fc=PINK, ec=RED)
    label(ax, 2.0, 3.35, "메모리: 작은 안내판", fs=11, color=RED, bold=True)
    for k, t in enumerate(["ㄱ~ㅂ → 블록 1", "ㅅ~ㅇ → 블록 2", "ㅈ~ㅎ → 블록 3"]):
        label(ax, 2.0, 2.75 - k * 0.55, t, fs=10.5, color=RED if k == 2 else "#222")
    groups = [["감사", "배송", "…"], ["언제", "완료", "요청"], ["주문", "환불", "…"]]
    for k, g in enumerate(groups):
        y = 3.3 - k * 1.15
        label(ax, 10.0, y + 0.4, f"블록 {k + 1}", fs=10.5, color=INK, ha="left")
        cells(ax, 5.9, y, g, w=1.3, h=0.8, hot=(1,) if k == 2 else (), fs=11)
    arrow(ax, (3.8, 1.65), (5.8, 1.35), color=RED)
    label(ax, 7.8, 4.4, "디스크: 낱말을 정렬해 수십 개씩 묶은 블록", fs=10.5, color=INK)
    label(ax, 7.5, 0.35, "안내판으로 블록을 고르고 그 블록 하나만 읽어요", fs=11, color=INK)
    save(fig, OUT, "es01-blocks.svg")


def phrase():
    """심화: 낱말 위치가 있어야 '환불 요청'이 붙어 있는지 안다."""
    fig, ax = canvas(10, 3.0, 15, 4.2)
    label(ax, 0.3, 3.7, "글 1", fs=12, ha="left", bold=True)
    cells(ax, 1.3, 3.2, ["주문", "환불", "요청"], w=1.4, h=0.8, hot=(1, 2))
    for k in range(3):
        label(ax, 1.3 + k * 1.48 + 0.7, 2.9, f"자리 {k}", fs=9.5, color=INK)
    label(ax, 0.3, 1.75, "역색인", fs=12, ha="left", bold=True)
    label(ax, 1.3, 1.75, "환불 → 글 1 (자리 1)     요청 → 글 1 (자리 2)", fs=11, ha="left", color=RED)
    box(ax, 0.3, 0.2, 14.4, 0.9, fc=NOTE)
    label(ax, 7.5, 0.65, "자리 1 다음이 자리 2라서 \"환불 요청\"이 붙어 있다는 걸 알아요. 자리를 안 적어 두면 알 수 없어요.", fs=10.5)
    save(fig, OUT, "es01-phrase.svg")


def deleted():
    """심화: 지운 글은 목록에서 빼지 않고 '지움' 표시만 한다."""
    fig, ax = canvas(10, 3.2, 15, 4.4)
    label(ax, 0.3, 3.75, "환불 →", fs=12, ha="left", bold=True)
    cells(ax, 1.8, 3.35, [1, 3], w=0.9, h=0.8)
    label(ax, 4.6, 3.75, "목록은 그대로", fs=10.5, ha="left", color=INK)
    label(ax, 0.3, 2.25, "살아 있는 글", fs=12, ha="left", bold=True)
    for k, (d, alive) in enumerate([(1, True), (3, False)]):
        cell(ax, 3.0 + k * 1.6, 1.85, 1.5, 0.8, f"글 {d} {'○' if alive else '✗'}", hot=not alive, fs=11)
    label(ax, 6.4, 2.25, "글 3을 지우면 ✗ 표시만 해요", fs=10.5, ha="left", color=RED)
    box(ax, 0.3, 0.2, 14.4, 1.0, fc=NOTE)
    label(ax, 7.5, 0.7, "검색 결과에는 글 1만 나오지만 '환불이 든 글 수'는 합치기(5편) 전까지 2로 남아요.", fs=10.5)
    save(fig, OUT, "es01-deleted.svg")


if __name__ == "__main__":
    scan(); map_(); flip(); lookup(); and_()
    forward(); speed(); cost(); miss(); decide(); blocks(); phrase(); deleted()
