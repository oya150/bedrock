"""Elasticsearch 3편 그림 만들기. 실행: python lab/fig_es03.py  → docs/elasticsearch/img/03/*.svg"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "es"))
from figkit import (story, BLUE, GREEN, GREY, INK, NOTE, PAPER, PINK, RED, YEL, arrow, box, canvas, cell,  # noqa: E402
                    label, outdir, save)

OUT = outdir("03")
SC = [BLUE, GREEN, YEL, "#c6a0d8"]
SC6 = [BLUE, GREEN, YEL, "#c6a0d8", "#e8a87c", "#9fd3c7"]


def open_():
    """샤드 3개 인덱스: 4개로 늘리기는 거절, 6개로 쪼개기는 된다."""
    fig, ax = canvas(10, 3.6, 15, 5.4)
    label(ax, 0.3, 5.0, "주문 기록 (조각 3개)", fs=12, ha="left", bold=True)
    for k in range(3):
        box(ax, 0.3 + k * 1.7, 2.6, 1.45, 1.6, fc=SC[k])
        label(ax, 1.02 + k * 1.7, 3.4, f"조각 {k}", fs=11)
    arrow(ax, (5.4, 3.9), (8.3, 4.3), color=RED)
    box(ax, 8.4, 3.75, 6.2, 1.0, fc=PINK, ec=RED)
    label(ax, 11.5, 4.25, "4개로 늘리기 → 거절", fs=12, color=RED, bold=True)
    arrow(ax, (5.4, 3.0), (8.3, 2.5))
    box(ax, 8.4, 1.95, 6.2, 1.0, fc=PAPER)
    label(ax, 11.5, 2.45, "6개로 쪼개기 → 돼요", fs=12)
    label(ax, 2.8, 1.6, "처음 만들 때 3개로 정했어요", fs=11, color=INK)
    label(ax, 7.5, 0.5, "4개는 안 되고 6개는 되는 까닭은?", fs=11.5, color=INK)
    save(fig, OUT, "es03-open.svg")


def shards():
    """인덱스 하나를 샤드 셋으로 나눠 노드 세 대에 둔다. 샤드마다 용어 사전이 따로 있다."""
    fig, ax = canvas(10, 4.0, 15, 6.0)
    box(ax, 4.6, 4.7, 5.8, 1.0, fc=PAPER)
    label(ax, 7.5, 5.2, "주문 인덱스 (문서 수억 개)", fs=12, bold=True)
    for k in range(3):
        x = 0.4 + k * 5.0
        arrow(ax, (7.5, 4.6), (x + 2.1, 3.85), ms=14)
        box(ax, x, 0.5, 4.2, 3.2, fc="white", ec=GREY)
        label(ax, x + 2.1, 3.35, f"노드 {k + 1} (컴퓨터)", fs=10.5, color=INK)
        box(ax, x + 0.3, 0.8, 3.6, 2.2, fc=SC[k])
        label(ax, x + 2.1, 2.55, f"샤드 {k}", fs=12, bold=True)
        cell(ax, x + 0.6, 1.05, 3.0, 0.9, "용어 사전 · 포스팅 목록", fs=9.5, fc=NOTE)
    save(fig, OUT, "es03-shards.svg")


def route():
    """_id → 해시값 → 샤드 수로 나눈 나머지 → 샤드 (해시값은 설명용으로 작게)."""
    fig, ax = canvas(10.5, 3.8, 16, 5.8)
    rows = [("order-8", 30, 0), ("order-4", 25, 1), ("order-1", 41, 2)]
    label(ax, 6.25, 5.3, "해시값", fs=10.5, color=INK)
    label(ax, 9.6, 5.3, "÷ 3 의 나머지", fs=10.5, color=INK)
    for k, (i, h, sh) in enumerate(rows):
        y = 3.9 - k * 1.3
        hot = k == 2
        cell(ax, 0.2, y, 1.9, 0.8, i, hot=hot, fs=11)
        arrow(ax, (2.2, y + 0.4), (2.9, y + 0.4), ms=12)
        box(ax, 3.0, y, 2.0, 0.8, fc=PAPER)
        label(ax, 4.0, y + 0.4, "해시 함수", fs=10)
        arrow(ax, (5.1, y + 0.4), (5.7, y + 0.4), ms=12)
        cell(ax, 5.8, y, 0.9, 0.8, h, fs=11, hot=hot)
        arrow(ax, (6.8, y + 0.4), (8.9, y + 0.4), ms=12)
        cell(ax, 9.0, y, 1.2, 0.8, h % 3, fs=11, hot=hot)
        arrow(ax, (10.3, y + 0.4), (11.4, y + 0.4), ms=12)
        box(ax, 11.5, y - 0.05, 2.0, 0.9, fc=SC[sh])
        label(ax, 12.5, y + 0.4, f"샤드 {sh}", fs=11, bold=hot, color=RED if hot else "#222")
    label(ax, 8.0, 0.35, "어느 노드든 _id만 알면 같은 샤드를 계산해요 (해시값은 설명용으로 작게)", fs=10.5, color=INK)
    save(fig, OUT, "es03-route.svg")


def reshuffle():
    fig, ax = canvas(10.5, 4.0, 16, 6.0)
    label(ax, 0.3, 5.6, "해시값 0~11을 나머지로 샤드 3개, 4개에 나눠 담으면", fs=12, ha="left", bold=True)
    for n, y0 in ((3, 3.4), (4, 0.6)):
        label(ax, 0.3, y0 + 0.6, f"샤드 {n}개", fs=11, ha="left", color=INK)
        for s in range(n):
            x = 1.6 + s * (14.0 / n)
            w = 14.0 / n - 0.25
            box(ax, x, y0, w, 1.15, fc=SC[s] if n == 3 else "white", ec=INK, lw=1.2)
            label(ax, x + w - 0.1, y0 + 1.4, f"샤드 {s}", fs=9.5, color=INK, ha="right")
            hs = [h for h in range(12) if h % n == s]
            for j, h in enumerate(hs):
                moved = n == 4 and (h % 3 != h % 4)
                cell(ax, x + 0.15 + j * 0.85, y0 + 0.2, 0.75, 0.75, h, hot=moved, fs=10,
                     fc=None if moved else SC[h % 3])
    label(ax, 15.6, 0.1, "빨강: 샤드가 바뀌는 문서 12개 중 9개", fs=11, color=RED, ha="right")
    save(fig, OUT, "es03-reshuffle.svg")


def lost():
    """샤드 수만 바꾸면: 꺼낼 때 없다고 하고, 다시 쓰면 두 개가 된다."""
    fig, ax = canvas(10.5, 5.0, 16, 7.6)
    label(ax, 0.3, 7.2, "샤드 수만 3개에서 4개로 바꾸고 문서는 그대로 둔다면", fs=12, ha="left", bold=True)
    for k, (title, dup) in enumerate([("① 번호로 꺼내면", False), ("② 같은 번호로 다시 쓰면", True)]):
        y = 4.0 - k * 3.4
        label(ax, 0.3, y + 2.2, title, fs=11.5, ha="left", bold=True)
        for s in range(4):
            x = 0.3 + s * 2.6
            box(ax, x, y, 2.3, 1.5, fc=SC[s] if s < 3 else "white", ec=INK, lw=1.2)
            label(ax, x + 1.15, y + 1.2, f"샤드 {s}", fs=10, color=INK)
        cell(ax, 5.55, y + 0.2, 1.8, 0.65, "order-1", fs=10)
        if dup:
            cell(ax, 2.95, y + 0.2, 1.8, 0.65, "order-1", hot=True, fs=10)
            label(ax, 10.9, y + 0.75, "샤드 1에 새로 생기고\n샤드 2의 옛것도 남아\n같은 번호가 두 개", fs=10.5, color=RED, ha="left")
        else:
            arrow(ax, (11.0, y + 1.9), (4.0, y + 1.55), color=RED, ms=14, rad=0.15)
            label(ax, 11.1, y + 1.9, "새 계산은 샤드 1", fs=10.5, color=RED, ha="left")
            label(ax, 10.9, y + 0.6, "샤드 1에는 order-1이 없어서\n'없는 문서'라고 답해요", fs=10.5, color=RED, ha="left")
    save(fig, OUT, "es03-lost.svg")


def relocate():
    """노드를 늘리면 문서를 다시 계산하지 않고 샤드를 통째로 옮긴다."""
    fig, ax = canvas(10.5, 3.6, 16, 5.4)
    for k, (title, nodes) in enumerate([("노드 3대", [[0, 1], [2, 3], [4, 5]]), ("노드 4대", [[0], [2, 3], [4, 5], [1]])]):
        y = 3.1 - k * 2.7
        label(ax, 0.3, y + 0.8, title, fs=11, ha="left", bold=True)
        for n, shs in enumerate(nodes):
            x = 2.4 + n * 3.4
            box(ax, x, y, 3.0, 1.6, fc="white", ec=GREY)
            label(ax, x + 1.5, y + 1.35, f"노드 {n + 1}", fs=9.5, color=INK)
            for j, s in enumerate(shs):
                hot = k == 1 and s == 1
                cell(ax, x + 0.2 + j * 1.35, y + 0.2, 1.2, 0.75, f"샤드 {s}", hot=hot, fs=9.5, fc=None if hot else SC6[s])
    arrow(ax, (4.4, 3.0), (13.6, 1.4), color=RED, ms=14, rad=-0.15)
    label(ax, 9.0, 2.55, "샤드 1을 통째로 옮겨요", fs=10.5, color=RED)
    save(fig, OUT, "es03-relocate.svg")


def slots():
    """ES 7.0~9.3: 샤드가 이어진 칸을 맡고, 쪼개면 칸을 반씩 나눠 맡는다."""
    fig, ax = canvas(10.5, 4.4, 16, 6.4)
    label(ax, 0.3, 6.0, "ES 7.0~9.3, 칸을 6개로 줄여 그리면: 샤드 3개가 칸을 2개씩 맡다가 쪼개면 1개씩", fs=12, ha="left", bold=True)
    W = 2.3
    label(ax, 0.3, 4.75, "칸", fs=11, ha="left", color=INK)
    for slot in range(6):
        cell(ax, 1.4 + slot * W, 4.4, W - 0.1, 0.7, f"칸 {slot}", fs=10, fc=SC[slot // 2])
    label(ax, 0.3, 3.25, "샤드 3개", fs=11, ha="left", color=INK)
    label(ax, 0.3, 1.25, "샤드 6개", fs=11, ha="left", color=INK)
    for p in range(3):
        x = 1.4 + p * 2 * W
        box(ax, x, 2.9, 2 * W - 0.1, 0.75, fc=SC[p], round_=False)
        label(ax, x + W - 0.05, 3.27, f"샤드 {p} (칸 {2*p}, {2*p+1})", fs=10)
        for c in range(2):
            t = 2 * p + c
            xx = 1.4 + t * W
            hot = p == 2
            arrow(ax, (x + W - 0.05, 2.85), (xx + (W - 0.1) / 2, 1.75), color=RED if hot else INK, lw=1.4, ms=12)
            box(ax, xx, 0.9, W - 0.1, 0.75, fc=SC[p], ec=RED if hot else INK, lw=2 if hot else 1.2, round_=False)
            label(ax, xx + (W - 0.1) / 2, 1.27, f"샤드 {t} (칸 {t})", fs=10, color=RED if hot else "#222")
    label(ax, 8.0, 0.3, "쪼갤 때 문서는 자기 샤드에서 갈라진 두 샤드 중 하나로만 가요", fs=11, color=RED)
    save(fig, OUT, "es03-slots.svg")


def split():
    """옛 샤드 0의 문서(해시값 0, 3, 6, 9)를 6으로 나누면 두 샤드로만, 4로 나누면 네 샤드로 흩어진다."""
    fig, ax = canvas(10.5, 4.6, 16, 7.0)
    label(ax, 0.3, 6.6, "옛 샤드 0 (해시값을 3으로 나눈 나머지가 0)", fs=12, ha="left", bold=True)
    for j, h in enumerate([0, 3, 6, 9]):
        cell(ax, 0.3 + j * 0.9, 5.4, 0.8, 0.8, h, fs=11, fc=BLUE)
    for k, (n, hot) in enumerate([(6, False), (4, True)]):
        y = 3.2 - k * 2.7
        label(ax, 0.3, y + 1.45, f"{n}으로 나눈 나머지로 샤드 {n}개에 담으면", fs=11, ha="left", color=RED if hot else INK, bold=True)
        W = 14.2 / n
        for t in range(n):
            x = 1.6 + t * W
            hs = [h for h in (0, 3, 6, 9) if h % n == t]
            got = bool(hs)
            box(ax, x, y, W - 0.2, 1.0, fc=(PINK if hot else BLUE) if got else "white", ec=RED if (hot and got) else INK, lw=1.2, round_=False)
            label(ax, x + (W - 0.2) / 2, y + 0.72, f"샤드 {t}", fs=9.5, color=INK)
            label(ax, x + (W - 0.2) / 2, y + 0.3, " ".join(map(str, hs)), fs=11, color=RED if hot else "#222", bold=got)
    label(ax, 15.6, 2.95, "두 샤드로만 가요", fs=11, ha="right", color=INK)
    label(ax, 15.6, 0.05, "네 샤드로 다 흩어져요", fs=11, ha="right", color=RED)
    save(fig, OUT, "es03-split.svg")


def cuts():
    """라우팅 칸 768개를 칼자국으로: 3조각·6조각은 칼자국에서 잘리고 9조각은 칼자국 사이를 지난다."""
    fig, ax = canvas(10.5, 4.2, 16, 6.0)
    label(ax, 0.3, 5.6, "칸 768개를 24칸으로 줄여 그리면", fs=12, ha="left", bold=True)
    X0, W = 2.4, 13.2
    for k, (n, hot) in enumerate([(3, False), (6, False), (9, True)]):
        y = 4.0 - k * 1.6
        label(ax, 0.3, y + 0.35, f"{n}조각", fs=11, ha="left", color=RED if hot else INK, bold=hot)
        box(ax, X0, y, W, 0.7, fc=YEL if not hot else PINK, ec=RED if hot else INK, lw=1.2, round_=False)
        for t in range(1, 24):
            x = X0 + W * t / 24
            ax.plot([x, x], [y + 0.45, y + 0.7], color=INK, lw=0.8)
        for c in range(1, n):
            x = X0 + W * c / n
            on = (24 * c) % n == 0
            ax.plot([x, x], [y - 0.12, y + 0.82], color=RED if not on else "#222", lw=2.4)
        label(ax, X0 + W + 0.1, y + 0.35, "칸 경계에서 잘려요" if not hot else "칸 한가운데를 지나요", fs=10, ha="left",
              color=RED if hot else INK)
    label(ax, X0, -0.25, "검정 선: 칸 경계에서 잘라요   빨간 선: 칸 한가운데를 지나요", fs=10, ha="left", color=INK)
    save(fig, OUT, "es03-cuts.svg")


def routing():
    """라우팅 값 user-7: 사진 9장이 한 샤드에. 라우팅 값 없이 번호로 꺼내면 다른 샤드를 본다."""
    fig, ax = canvas(10.5, 4.2, 16, 6.2)
    label(ax, 0.3, 5.7, "사진 m1~m9를 routing=user-7로 넣으면", fs=11.5, ha="left", bold=True)
    for k in range(3):
        x = 7.2 + k * 2.9
        box(ax, x, 2.4, 2.6, 2.6, fc=SC[k] if k == 0 else "white", ec=INK, lw=1.2)
        label(ax, x + 1.3, 4.7, f"샤드 {k}", fs=10.5, color=INK)
    for j in range(9):
        cell(ax, 7.4 + (j % 3) * 0.75, 3.7 - (j // 3) * 0.6, 0.68, 0.5, f"m{j+1}", fs=8.5, fc=NOTE)
    cell(ax, 0.3, 4.2, 2.6, 0.8, "user-7", fs=11)
    arrow(ax, (3.0, 4.6), (3.7, 4.6), ms=12)
    box(ax, 3.8, 4.2, 1.9, 0.8, fc=PAPER)
    label(ax, 4.75, 4.6, "해시 함수", fs=10)
    arrow(ax, (5.8, 4.6), (7.1, 4.3), ms=12)
    label(ax, 0.3, 1.7, "m1을 라우팅 값 없이 번호로 꺼내면", fs=11.5, ha="left", bold=True, color=RED)
    cell(ax, 0.3, 0.4, 2.6, 0.8, "m1 (_id)", hot=True, fs=11)
    arrow(ax, (3.0, 0.8), (3.7, 0.8), color=RED, ms=12)
    box(ax, 3.8, 0.4, 1.9, 0.8, fc=PAPER)
    label(ax, 4.75, 0.8, "해시 함수", fs=10)
    arrow(ax, (5.8, 0.8), (14.0, 2.35), color=RED, ms=14)
    label(ax, 15.6, 0.9, "샤드 2를 봐서\n'없음'(404)", fs=10.5, color=RED, ha="right")
    save(fig, OUT, "es03-routing.svg")


def decide():
    """샤드 수 정하기."""
    fig, ax = canvas(10, 3.2, 15, 4.8)
    box(ax, 0.3, 3.0, 5.6, 1.4, fc=NOTE)
    label(ax, 3.1, 3.7, "시간이 지나며 계속 쌓이기만 하나요?\n(가계부·주문 기록)", fs=10.5, bold=True)
    arrow(ax, (6.0, 3.7), (7.4, 3.7), color=RED)
    label(ax, 6.7, 4.0, "예", fs=10, color=RED)
    box(ax, 7.5, 3.0, 7.2, 1.4, fc=PINK, ec=RED)
    label(ax, 11.1, 3.7, "기간마다 새 인덱스\n만들 때마다 샤드 수를 다시 정해요", fs=10.5, color=RED)
    arrow(ax, (3.1, 2.9), (3.1, 1.7))
    label(ax, 3.6, 2.3, "아니요", fs=10, color=INK, ha="left")
    box(ax, 0.3, 0.3, 5.6, 1.3, fc=NOTE)
    label(ax, 3.1, 0.95, "앞으로 클 크기 ÷ 샤드 하나 크기\n(10~50 GB 정도)", fs=10.5, bold=True)
    arrow(ax, (6.0, 0.95), (7.4, 0.95))
    box(ax, 7.5, 0.3, 7.2, 1.3, fc=PAPER)
    label(ax, 11.1, 0.95, "그 수로 정하고\n예상보다 커지면 2배로 쪼개요", fs=10.5)
    save(fig, OUT, "es03-decide.svg")


def map_():
    """정리 절: 이 편이 한 말을 결론 문장으로."""
    story(['문서가 많으면 인덱스를 샤드 여러 개로 나눠 여러 노드에 담아요', '문서가 갈 샤드는 해시값과 샤드 수로 계산해요(라우팅 값을 따로 줄 수도 있어요)', '샤드 수를 바꾸면 계산이 달라져 문서 대부분이 자리를 옮겨야 해요', '그래서 샤드 수는 못 바꾸고 2배, 4배로 쪼개는 것만 돼요', '샤드 수는 앞으로 클 크기로 정하고 계속 쌓이는 데이터는 기간마다 새 인덱스를 만들어요'], 2, OUT, "es03-map.svg")


if __name__ == "__main__":
    open_(); shards(); route(); reshuffle(); lost(); relocate(); split(); slots(); cuts(); routing(); decide(); map_()
