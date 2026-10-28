"""Elasticsearch 1편 그림 만들기. 실행: python lab/fig_es01.py  → docs/elasticsearch/img/01/*.svg"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "es"))
from figkit import (story, GREY, INK, LIGHT, NOTE, PAPER, PINK, RED, YEL, arrow, box, canvas, cell, cells,  # noqa: E402
                    label, outdir, save)

OUT = outdir("01")


def scan():
    rows = ["주문 환불 요청", "주문 배송 언제", "환불 완료 감사", "사이즈 교환 문의",
            "주문 취소했어요", "색상이 달라요"]
    fig, ax = canvas(8.4, 4.6, 12, 6.6)
    label(ax, 0.3, 6.25, "데이터베이스 속 글 표", fs=12, ha="left", bold=True)
    cell(ax, 0.3, 5.45, 0.8, 0.6, "번호", fc=PAPER); cell(ax, 1.1, 5.45, 5.0, 0.6, "글", fc=PAPER)
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
    label(ax, 9.25, 1.55, "'환불'이 든 글 찾기", fs=12)
    save(fig, OUT, "es01-scan.svg")


def map_():
    """정리 절: 이 편이 한 말을 결론 문장으로."""
    story(['글을 하나씩 다 훑으면 글이 늘수록 찾는 시간도 늘어나요', '그래서 낱말마다 그 낱말이 든 글 번호를 미리 적어 둬요(역색인)', '낱말을 정렬해 둔 사전이라 글이 늘어도 낱말 하나를 찾는 걸음은 거의 그대로예요', '두 낱말이 다 든 글은 번호 줄 둘을 한 번씩 훑어 겹쳐 찾아요', '대신 미리 만드는 시간과 공간이 들고 잘라 둔 낱말로만 찾을 수 있어요', '넣은 글은 모았다가 한꺼번에 올려서 잠시 뒤에야 검색돼요'], 1, OUT, "es01-map.svg")


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
    label(ax, 11.6, 6.85, "글 번호 (번호순)", fs=10, color=INK)
    save(fig, OUT, "es01-flip.svg")


def lookup():
    terms = ["감사", "배송", "언제", "완료", "요청", "주문", "환불"]
    fig, ax = canvas(10, 3.6, 15, 5.2)
    cells(ax, 0.3, 3.2, terms, w=1.3, h=0.8, hot=(6,), dim=(0, 1, 2, 3, 4, 5))
    # 이진 탐색: 가운데(완료) → 남은 반의 가운데(주문) → 환불
    for n, i in enumerate((3, 5, 6)):
        x = 0.3 + i * 1.38 + 0.65
        hot = i == 6
        arrow(ax, (x, 2.0), (x, 3.1), color=RED if hot else INK, lw=1.6, ms=12)
        label(ax, x, 1.55, f"{'①②③'[n]} {terms[i]}", fs=11, color=RED if hot else INK, bold=hot)
    label(ax, 0.3 + 3 * 1.38 + 0.65, 0.95, "가나다순이라 볼 때마다 반씩 버려요 (버린 칸은 흐리게)", fs=11, color=INK)
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
    label(ax, 8.4, 0.5, "두 목록을 한 번씩만 훑어요", fs=11, ha="left", color=INK)
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
    label(ax, 0.3, 2.55, "전체 훑기", fs=11.5, ha="left")
    ax.add_patch(__import__("matplotlib").patches.Rectangle((4.0, 2.25), 9.5, 0.6, fc=GREY, ec=INK))
    label(ax, 13.6, 2.55, "약 200 ms\n(0.2초)", fs=11, ha="left")
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
    label(ax, 7.8, 0.4, "이 실험에서는 검색을 다섯 번 넘게 하면 미리 만든 쪽이 이득이었어요", fs=11, color=INK)
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
    label(ax, 7.5, 0.9, "글자를 훑는 '%환불%'은 이 글도 찾아요", fs=10.5)
    save(fig, OUT, "es01-miss.svg")


def decide():
    """언제 역색인을 만들까: 자주 찾나 → 글 중간 낱말로 찾나."""
    fig, ax = canvas(10, 4.2, 15, 6.0)
    box(ax, 0.3, 4.4, 4.4, 1.2, fc=NOTE)
    label(ax, 2.5, 5.0, "자주 찾나요?", fs=12, bold=True)
    box(ax, 5.6, 4.4, 4.4, 1.2, fc=NOTE)
    label(ax, 7.8, 5.0, "글 중간에 든\n낱말로 찾나요?", fs=11.5, bold=True)
    box(ax, 10.9, 4.4, 3.8, 1.2, fc=PINK, ec=RED)
    label(ax, 12.8, 5.0, "역색인\n(ES)", fs=12, color=RED, bold=True)
    arrow(ax, (4.8, 5.0), (5.5, 5.0)); label(ax, 5.15, 5.45, "예", fs=10, color=INK)
    arrow(ax, (10.1, 5.0), (10.8, 5.0), color=RED); label(ax, 10.45, 5.45, "예", fs=10, color=RED)
    arrow(ax, (2.5, 4.3), (2.5, 2.9)); label(ax, 2.85, 3.6, "아니요", fs=10, color=INK, ha="left")
    arrow(ax, (7.8, 4.3), (7.8, 2.9)); label(ax, 8.15, 3.6, "아니요", fs=10, color=INK, ha="left")
    box(ax, 0.3, 0.6, 4.4, 2.2, fc=LIGHT, ec=GREY)
    label(ax, 2.5, 1.7, "그때그때 전체 훑기\n예: 몇 년 치 가계부에서\n가끔 가게 이름 찾기", fs=10.5)
    box(ax, 5.6, 0.6, 4.4, 2.2, fc=LIGHT, ec=GREY)
    label(ax, 7.8, 1.7, "데이터베이스 인덱스\n예: '청바'로 시작하는\n상품 이름 찾기", fs=10.5)
    save(fig, OUT, "es01-decide.svg")


def fingers():
    """손가락 두 개가 움직이는 단계."""
    a = [2, 5, 9, 14, 20]
    b = [1, 5, 8, 14, 21, 30]
    steps = [(0, 0, "다르니 작은 쪽(주문 1)을 앞으로"), (0, 1, "다르니 작은 쪽(환불 2)을 앞으로"),
             (1, 1, "같다! 5를 결과에 넣고 둘 다 앞으로"), (2, 2, "다르니 작은 쪽(주문 8)을 앞으로")]
    fig, ax = canvas(11, 6.2, 17, 9.4)
    for k, (i, j, msg) in enumerate(steps):
        y0 = 8.4 - k * 2.25
        label(ax, 0.2, y0 + 0.1, "①②③④"[k], fs=13, color=RED, ha="left", bold=True)
        label(ax, 0.9, y0 + 0.1, "환불", fs=10.5, ha="left")
        label(ax, 0.9, y0 - 0.85, "주문", fs=10.5, ha="left")
        cells(ax, 2.0, y0 - 0.25, a, w=0.8, h=0.65, hot=(i,), fs=11)
        cells(ax, 2.0, y0 - 1.2, b, w=0.8, h=0.65, hot=(j,), fs=11)
        label(ax, 8.2, y0 - 0.4, msg, fs=11, ha="left", color=RED if "같다" in msg else "#222")
    save(fig, OUT, "es01-fingers.svg")


def scale():
    """글 수가 늘 때 걸음 수: 하나씩 보기는 글 수만큼, 사전 찾기는 낱말 종류 5,000개에서 이진 탐색 13걸음."""
    sizes = ["글 10만", "글 20만", "글 40만"]
    scan = [100_000, 200_000, 400_000]
    fig, ax = canvas(10, 3.8, 15, 5.2)
    label(ax, 0.3, 4.85, "낱말 하나 찾는 걸음 수", fs=12, ha="left", bold=True)
    for k, (name, n) in enumerate(zip(sizes, scan)):
        y = 3.8 - k * 1.25
        label(ax, 0.3, y + 0.25, name, fs=11, ha="left")
        w = 9.0 * n / scan[-1]
        ax.add_patch(__import__("matplotlib").patches.Rectangle((2.2, y + 0.05), w, 0.4, fc=GREY, ec=INK))
        label(ax, 2.3 + w, y + 0.25, f"하나씩: {n:,}번", fs=10, ha="left")
        ax.add_patch(__import__("matplotlib").patches.Rectangle((2.2, y - 0.45), 0.08, 0.4, fc=RED, ec=RED))
        label(ax, 2.45, y - 0.25, "사전에서 찾기: 13번", fs=10, ha="left", color=RED)
    label(ax, 7.5, 0.25, "낱말 종류가 5,000개로 같으면 글이 늘어도 사전에서 찾는 걸음은 그대로예요", fs=10.5, color=INK)
    save(fig, OUT, "es01-scale.svg")


def prefix():
    """정렬된 목록에서 '환불%'는 한 덩어리, '%환불%'는 흩어져 있다."""
    rows = ["교환 문의", "반품 문의", "빠른 환불 부탁", "사이즈 교환", "주문 취소", "주문 환불 요청",
            "쿠폰 문의", "환불 언제 돼요", "환불 완료 감사", "환불 요청합니다", "회원 탈퇴"]
    fig, ax = canvas(10, 6.0, 15, 9.4)
    label(ax, 4.0, 9.0, "데이터베이스 인덱스 (가나다순)", fs=12, bold=True)
    top = 8.0
    for k, r in enumerate(rows):
        y = top - k * 0.7
        start = r.startswith("환불")
        inside = "환불" in r and not start
        cell(ax, 1.8, y, 4.4, 0.6, r, hot=start, fc=None if start else ("#fff3cf" if inside else NOTE), fs=11)
        if inside or start:
            label(ax, 6.7, y + 0.3, "●", fs=12, color=YEL)
    first = top - 7 * 0.7
    arrow(ax, (0.2, first + 0.3), (1.7, first + 0.3), color=RED, lw=2.2)
    label(ax, 0.2, first + 0.75, "'환불%'", fs=11.5, color=RED, ha="left", bold=True)
    ax.plot([6.4, 6.4], [top - 9 * 0.7, first + 0.6], color=RED, lw=3)
    label(ax, 7.2, top - 8 * 0.7 + 0.3, "← '환불%' (환불로 시작)\n    한 덩어리라 바로 찾아가요", fs=11, color=RED, ha="left")
    label(ax, 7.2, top - 2 * 0.7 + 0.3, "← ● '%환불%' (어디든 환불)\n    ㅃ, ㅈ, ㅎ에 흩어져\n    다 읽어야 해요", fs=11, color="#9a7000", ha="left")
    label(ax, 7.5, 0.25, "%는 '아무 글자나 와도 된다'는 표시예요", fs=10.5, color=INK)
    save(fig, OUT, "es01-prefix.svg")


def blocks():
    """심화: 사전은 디스크에 블록으로 두고 '어느 블록에 있나'만 작은 안내판으로 먼저 읽는다."""
    fig, ax = canvas(10, 3.6, 15, 4.8)
    box(ax, 0.3, 1.2, 3.4, 2.6, fc=PINK, ec=RED)
    label(ax, 2.0, 3.35, "먼저 읽는 작은 안내판", fs=11, color=RED, bold=True)
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
        label(ax, 1.3 + k * 1.48 + 0.7, 2.9, f"위치 {k}", fs=9.5, color=INK)
    label(ax, 0.3, 1.75, "역색인", fs=12, ha="left", bold=True)
    label(ax, 1.3, 1.75, "환불 → 글 1 (위치 1)     요청 → 글 1 (위치 2)", fs=11, ha="left", color=RED)
    box(ax, 0.3, 0.2, 14.4, 0.9, fc=NOTE)
    label(ax, 7.5, 0.65, "위치 1 다음이 위치 2라서 \"환불 요청\"이 붙어 있다는 걸 알아요. 위치를 안 적어 두면 알 수 없어요.", fs=10.5)
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
    label(ax, 7.5, 0.7, "새로 고침 뒤 검색에는 글 1번만 나와요. 디스크 공간은 병합(5편) 때 대개 줄어요", fs=10.5)
    save(fig, OUT, "es01-deleted.svg")


def segs():
    """새로 고침마다 작은 역색인(세그먼트)이 하나씩 생기고 검색은 모두를 본다."""
    fig, ax = canvas(10, 3.6, 15, 4.8)
    label(ax, 7.5, 4.45, "1초마다 그동안 들어온 글로 세그먼트를 하나씩 만들어요", fs=11, color=INK)
    for k, t in enumerate(["0~1초에 온 글", "1~2초에 온 글", "2~3초에 온 글"]):
        x = 1.2 + k * 4.6
        box(ax, x, 2.5, 3.8, 1.4, fc=NOTE)
        label(ax, x + 1.9, 3.45, f"세그먼트 {k + 1}", fs=11.5, bold=True)
        label(ax, x + 1.9, 2.9, t, fs=10, color=INK)
    box(ax, 5.8, 0.3, 3.4, 0.9, fc=PINK, ec=RED)
    label(ax, 7.5, 0.75, "검색", fs=12, color=RED, bold=True)
    for k in range(3):
        arrow(ax, (7.5, 1.25), (1.2 + k * 4.6 + 1.9, 2.45), color=RED, lw=1.6, ms=12)
    label(ax, 9.6, 0.75, "셋 다 찾아보고 결과를 합쳐요", fs=10.5, ha="left", color=RED)
    save(fig, OUT, "es01-segs.svg")


def merge():
    """작은 역색인이 많아지면 몇 개씩 하나로 합친다."""
    fig, ax = canvas(10, 2.8, 15, 3.8)
    for k in range(3):
        box(ax, 0.4, 2.6 - k * 1.0, 2.6, 0.8, fc=NOTE)
        label(ax, 1.7, 3.0 - k * 1.0, f"세그먼트 {k + 1}", fs=10.5)
    arrow(ax, (3.3, 2.0), (6.6, 2.0), lw=3, ms=22, color=RED)
    label(ax, 4.95, 2.45, "병합", fs=12, color=RED, bold=True)
    box(ax, 6.9, 0.9, 4.0, 2.2, fc=PINK, ec=RED)
    label(ax, 8.9, 2.0, "합친 세그먼트 1개", fs=12, color=RED, bold=True)
    label(ax, 11.3, 2.0, "찾아볼 곳이\n하나로 줄어요", fs=10.5, ha="left", color=INK)
    save(fig, OUT, "es01-merge.svg")


def heap():
    """심화: 7.7부터 안내판은 힙 밖. 디스크 파일에서 필요한 부분만 운영체제 메모리로."""
    fig, ax = canvas(10, 3.4, 15, 4.6)
    box(ax, 0.3, 1.3, 4.0, 2.6, fc=NOTE)
    label(ax, 2.3, 3.4, "ES 전용 메모리", fs=11.5, bold=True)
    label(ax, 2.3, 2.9, "(자바 힙)", fs=10.5, color=INK)
    label(ax, 2.3, 2.1, "크기를 미리\n정해 둬요", fs=10, color=INK)
    box(ax, 5.3, 1.3, 4.2, 2.6, fc=PINK, ec=RED)
    label(ax, 7.4, 3.4, "운영체제가 쓰는", fs=11.5, bold=True, color=RED)
    label(ax, 7.4, 2.9, "남는 메모리", fs=11.5, bold=True, color=RED)
    label(ax, 7.4, 2.1, "안내판 중\n필요한 부분", fs=10, color=RED)
    box(ax, 10.6, 1.3, 4.1, 2.6, fc=PAPER)
    label(ax, 12.65, 3.4, "디스크", fs=11.5, bold=True)
    label(ax, 12.65, 2.4, "안내판 파일", fs=10.5)
    arrow(ax, (10.5, 2.3), (9.6, 2.3), color=RED)
    label(ax, 10.05, 1.0, "필요한 부분만 읽어 와요", fs=9.5, color=RED)
    label(ax, 7.5, 0.35, "ES 7.7부터는 안내판이 힙 밖에 있어서 낱말이 늘어도 힙은 그대로예요", fs=10.5, color=INK)
    save(fig, OUT, "es01-heap.svg")


if __name__ == "__main__":
    scan(); map_(); flip(); lookup(); and_()
    prefix(); forward(); speed(); scale(); fingers(); cost(); miss(); decide(); blocks(); phrase(); deleted(); segs(); merge(); heap()
