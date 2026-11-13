"""AI 1편 그림 만들기. 실행: python lab/fig_ai01.py  → docs/ai/img/01/*.svg

예시는 보낸 메시지 다섯 개와 그 횟수표를 편 끝까지 잇는다.
그림 안 글씨는 낱말과 숫자만 둔다. 문장은 본문과 그림 설명에 둔다(쉬운글-정책 5장).
숫자는 모두 이 다섯 메시지로 직접 센 것이다.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "es"))
from figkit import GREY, INK, PAPER, RED, arrow, box, canvas, cell, label, outdir, save  # noqa: E402
from matplotlib.patches import Rectangle  # noqa: E402

OUT = outdir("01", "ai")

MSGS = [["오늘", "점심", "뭐", "먹지"], ["오늘", "날씨", "좋다"], ["내일", "점심", "같이", "먹자"],
        ["오늘", "저녁", "뭐", "먹을까"], ["날씨", "뭐", "이래"]]
TABLE = [("오늘", [("점심", 1), ("날씨", 1), ("저녁", 1)]),
         ("내일", [("점심", 1)]),
         ("날씨", [("좋다", 1), ("뭐", 1)]),
         ("점심", [("뭐", 1), ("같이", 1)]),
         ("저녁", [("뭐", 1)]),
         ("같이", [("먹자", 1)]),
         ("뭐", [("먹지", 1), ("먹을까", 1), ("이래", 1)])]
ENDS = [(w, [("(끝)", 1)]) for w in ["먹지", "좋다", "먹자", "먹을까", "이래"]]  # 메시지 마지막 낱말
WORDS = ["오늘", "점심", "뭐", "먹지", "날씨", "좋다", "내일", "같이", "먹자", "저녁", "먹을까", "이래"]
PAIRS = {(m[i], m[i + 1]) for m in MSGS for i in range(len(m) - 1)}  # 메시지 안에서 이웃한 두 낱말, 13가지



def make(draw, name, y0, y1):
    """가로 0~12, 세로 y0~y1 만 남겨 그린다. 빈 아래쪽이 남지 않게."""
    fig, ax = canvas(7.2, 0.6 * (y1 - y0), 12, y1)
    ax.set_ylim(y0, y1)
    ax.add_patch(Rectangle((0, y0), 12, y1 - y0, fill=False, ec="none"))
    draw(ax, 1)
    save(fig, OUT, name)


# ── 챗봇: 낱말 하나를 맞혀 붙이고 또 맞혀요 ───────────────────────
ANSWER = ["따뜻한", "국수", "어때요?"]


def chat(ax, step):
    label(ax, 0.6 + 1.3, 6.1, "물음", fs=10.5, color=INK)
    label(ax, 3.7 + 2.3, 6.1, "챗봇의 답", fs=10.5, color=INK)
    for r in range(3):
        y = 4.8 - r * 1.2
        label(ax, 0.3, y + 0.3, str(r + 1), fs=11, color=INK)
        cell(ax, 0.6, y, 2.6, 0.6, "점심 뭐 먹지?", fs=11.5)
        for k in range(r + 1):
            cell(ax, 3.7 + k * 1.6, y, 1.45, 0.6, ANSWER[k], hot=k == r, fs=11.5)


# ── 횟수표: 보낸 메시지 → 앞 낱말마다 다음 낱말 횟수 ──────────────
TX, TY0, TDY = 5.5, 6.15, 0.56


def msg_rows(ax, hot_words=(), dim_words=(), x0=0.75, y0=6.15, dy=0.65, w=0.95):
    """보낸 메시지 다섯 줄을 낱말 칸으로. hot_words={(줄, 칸)}."""
    for r, m in enumerate(MSGS):
        y = y0 - r * dy
        label(ax, x0 - 0.3, y + 0.25, str(r + 1), fs=10, color=INK)
        for k, wd in enumerate(m):
            cell(ax, x0 + k * (w + 0.06), y, w, 0.5, wd, hot=(r, k) in hot_words, dim=(r, k) in dim_words, fs=10.5)


def word_xy(r, k, x0=0.75, y0=6.15, dy=0.65, w=0.95):
    """msg_rows 기본 배치에서 (줄, 칸) 칸의 왼쪽 아래."""
    return x0 + k * (w + 0.06), y0 - r * dy


def table_row(ax, x, y, front, items, hot=False, fw=1.05, iw=1.2, gap=0.12, fs=10):
    cell(ax, x, y, fw, 0.46, front, hot=hot, fs=10.5)
    arrow(ax, (x + fw + 0.05, y + 0.23), (x + fw + 0.42, y + 0.23), color=GREY, ms=9, lw=1.2)
    for k, (wd, n) in enumerate(items):
        cell(ax, x + fw + 0.5 + k * (iw + gap), y, iw, 0.46, f"{wd} {n}", hot=hot, fs=fs)


def tally(ax, step):
    label(ax, 0.3, 6.95, "보낸 메시지", fs=11.5, ha="left", bold=True)
    label(ax, TX, 6.95, "횟수표", fs=11.5, ha="left", bold=True)
    msg_rows(ax, {(0, 1), (1, 1), (3, 1)})
    for k, (front, items) in enumerate(TABLE + ENDS):
        table_row(ax, TX, TY0 - k * 0.5, front, items, hot=front == "오늘")


# ── 뽑기와 이어 붙이기: 같은 무대 ─────────────────────────────────
OX, OY, OW = 0.5, 5.0, 1.15


def ticket_box(ax, x, y, words, tw=1.05):
    w = len(words) * (tw + 0.15) + 0.35
    box(ax, x, y, w, 1.05, fc=PAPER)
    for k, wd in enumerate(words):
        cell(ax, x + 0.25 + k * (tw + 0.15), y + 0.25, tw, 0.55, wd, fs=11)


def chain_stage(ax, out, hot_out, front, tickets, pick):
    label(ax, 0.3, 6.2, "뽑은 문장", fs=11.5, ha="left", bold=True)
    for k, wd in enumerate(out):
        cell(ax, OX + k * (OW + 0.1), OY, OW, 0.6, wd, hot=k == hot_out, fs=12)
    label(ax, 0.3, 4.05, "앞 낱말", fs=10.5, ha="left", color=INK)
    cell(ax, 0.5, 2.9, 1.15, 0.6, front, fs=12)
    arrow(ax, (1.75, 3.2), (2.35, 3.2), color=GREY, ms=11, lw=1.3)
    label(ax, 2.5, 2.35, "제비 통", fs=10.5, ha="left", color=INK)
    ticket_box(ax, 2.45, 2.65, tickets)
    px = 2.45 + 0.25 + pick * 1.2
    cell(ax, px, 2.9, 1.05, 0.55, tickets[pick], hot=True, fs=11)
    tx = OX + hot_out * (OW + 0.1) + OW / 2
    arrow(ax, (px + 0.52, 3.55), (tx, OY - 0.08), color=RED, ms=13)


def draw(ax, step):
    chain_stage(ax, ["오늘", "점심"], 1, "오늘", ["점심", "날씨", "저녁"], 0)


def chain(ax, step):
    chain_stage(ax, ["오늘", "점심", "같이", "먹자"], 3, "같이", ["먹자"], 0)


def tangle(ax, step):
    chain_stage(ax, ["내일", "점심", "뭐", "이래"], 3, "뭐", ["먹지", "먹을까", "이래"], 2)


# ── 엉킴의 원인: 세 메시지의 "뭐"가 한 줄로 모여요 ─────────────────
MWO = [(0, 2), (3, 2), (4, 1)]  # "뭐"가 있는 (줄, 칸)
RX, RW = 6.6, 0.9


def mo_arrow(ax, r, k, to_y, color):
    x, y = word_xy(r, k + 1)
    arrow(ax, (x + 0.95 + 0.05, y + 0.25), (RX - 0.08, to_y + 0.23), color=color, ms=11, lw=1.5)


def merge(ax, step):
    label(ax, 0.3, 6.95, "보낸 메시지", fs=11.5, ha="left", bold=True)
    label(ax, RX, 6.95, "\"뭐\" 줄", fs=11.5, ha="left", bold=True)
    ry = 4.6
    msg_rows(ax, dim_words={(r, k - 1) for r, k in MWO})
    for r, k in MWO:
        mo_arrow(ax, r, k, ry, RED)
    table_row(ax, RX, ry, "뭐", TABLE[6][1], fw=RW, iw=1.1, gap=0.1, hot=True)


# ── "뭐" 줄을 앞 낱말 둘로 나눠요 ──────────────────────────────────
SPLIT = [((0, 2), "점심 뭐", "먹지", 5.5), ((3, 2), "저녁 뭐", "먹을까", 4.6), ((4, 1), "날씨 뭐", "이래", 3.7)]


def split(ax, step):
    label(ax, 0.3, 6.95, "보낸 메시지", fs=11.5, ha="left", bold=True)
    label(ax, RX, 6.95, "앞 낱말 둘", fs=11.5, ha="left", bold=True)
    msg_rows(ax)
    for (r, k), front, nxt, y in SPLIT:
        mo_arrow(ax, r, k, y, RED)
        cell(ax, RX, y, 1.5, 0.46, front, fs=10.5, hot=True)
        arrow(ax, (RX + 1.55, y + 0.23), (RX + 1.95, y + 0.23), color=GREY, ms=9, lw=1.2)
        cell(ax, RX + 2.05, y, 1.4, 0.46, f"{nxt} 1", fs=10, hot=True)


# ── 막힘의 원인: 12 × 12 칸 ────────────────────────────────────────
GX, GTOP, GC = 1.35, 7.0, 0.48


def grid(ax, step):
    label(ax, GX + 6 * GC, 8.2, "둘째 낱말 →", fs=9.5, color=INK)
    label(ax, GX - 0.08, 7.25, "첫 낱말 ↓", fs=9.5, ha="right", color=INK)
    for i, wd in enumerate(WORDS):
        label(ax, GX - 0.08, GTOP - (i + 1) * GC + GC / 2, wd, fs=9, ha="right")
    for j, wd in enumerate(WORDS):
        label(ax, GX + j * GC + GC / 2, GTOP + 0.06, wd, fs=8.5, rotation=90, va="bottom")
    for i, a in enumerate(WORDS):
        for j, b in enumerate(WORDS):
            seen = (a, b) in PAIRS
            ax.add_patch(Rectangle((GX + j * GC, GTOP - (i + 1) * GC), GC, GC, fc=RED if seen else "white",
                                   ec=RED if seen else GREY, lw=1.0 if seen else 0.8))
    i, j = WORDS.index("내일"), WORDS.index("저녁")
    x, y = GX + j * GC, GTOP - (i + 1) * GC
    ax.add_patch(Rectangle((x - 0.04, y - 0.04), GC + 0.08, GC + 0.08, fill=False, ec=RED, lw=2.4))
    label(ax, x + GC / 2, y + GC / 2, "?", fs=11, color=RED, bold=True)
    label(ax, 7.6, 5.4, "12 × 12 = 144", fs=12, ha="left", color=INK)
    ax.add_patch(Rectangle((7.6, 4.35), 0.4, 0.4, fc=RED, ec=RED))
    label(ax, 8.15, 4.55, "13", fs=12, ha="left", color=RED, bold=True)


if __name__ == "__main__":
    make(chat, "ai01-chat-1.svg", 2.1, 6.5)
    make(tally, "ai01-tally-1.svg", 0.5, 7.3)
    make(draw, "ai01-draw-1.svg", 2.0, 6.5)
    make(chain, "ai01-chain-1.svg", 2.0, 6.5)
    make(tangle, "ai01-tangle-1.svg", 2.0, 6.5)
    make(merge, "ai01-merge-1.svg", 3.3, 7.3)
    make(split, "ai01-split-1.svg", 3.3, 7.3)
    make(grid, "ai01-grid-1.svg", 1.0, 8.7)
