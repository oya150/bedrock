"""AI 1편 그림 만들기. 실행: python lab/fig_ai01.py  → docs/ai/img/01/*.svg

본문 절은 장면 띠로 그린다: 같은 무대를 여러 장 그리고 장마다 바뀐 곳만 빨강으로 칠한다.
예시는 보낸 메시지 다섯 개와 그 횟수표를 편 끝까지 잇는다(.claude/writing/work/cal/units-ai01-v3.md).
숫자는 모두 이 다섯 메시지로 직접 센 것이다.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "es"))
from figkit import (GREY, INK, LIGHT, PAPER, PINK, RED, arrow, box, bubble, canvas, cell,  # noqa: E402
                    cylinder, label, moral, outdir, save, stage)
from matplotlib.patches import Rectangle  # noqa: E402

OUT = outdir("01", "ai")

MSGS = [["오늘", "점심", "뭐", "먹지"], ["오늘", "날씨", "좋다"], ["내일", "점심", "같이", "먹자"],
        ["오늘", "저녁", "뭐", "먹을까"], ["날씨", "뭐", "이래"]]
ST, EN = "(처음)", "(끝)"
TABLE = [(ST, [("오늘", 3), ("내일", 1), ("날씨", 1)]),
         ("오늘", [("점심", 1), ("날씨", 1), ("저녁", 1)]),
         ("내일", [("점심", 1)]),
         ("날씨", [("좋다", 1), ("뭐", 1)]),
         ("점심", [("뭐", 1), ("같이", 1)]),
         ("저녁", [("뭐", 1)]),
         ("같이", [("먹자", 1)]),
         ("뭐", [("먹지", 1), ("먹을까", 1), ("이래", 1)])]
ENDS = "먹지 · 좋다 · 먹자 · 먹을까 · 이래 → (끝) 1"
WORDS = ["오늘", "점심", "뭐", "먹지", "날씨", "좋다", "내일", "같이", "먹자", "저녁", "먹을까", "이래"]
PAIRS = {(m[i], m[i + 1]) for m in MSGS for i in range(len(m) - 1)}  # 메시지 안에서 이웃한 두 낱말, 13가지


def empty(ax, x, y, w, h, s="", color=GREY):
    ax.add_patch(Rectangle((x, y), w, h, fc="white", ec=color, lw=1.2, ls="--"))
    if s:
        label(ax, x + w / 2, y + h / 2, s, fs=12, color=color, bold=color == RED)


# ── 무대: 휴대폰 메시지 자판과 자판 속 프로그램 ────────────────────
CYL = (7.2, 3.35, 4.0, 1.45)
SAY = (6.3, 0.95, 5.5, 1.55)
TAIL = (9.2, 3.1)
S, L = (7.2, 3.8), (12, 6.6)
T = ((7.2, 4.3), (12, 7.4))


def phone(ax, typed, sugg, typed_hot=False, hot=()):
    """sugg=None이면 후보 칸 셋이 빈 점선, 빈 목록이면 빈칸에 빨간 물음표. hot=빨간 후보 번호."""
    box(ax, 0.4, 0.9, 4.8, 5.55, fc="white")
    label(ax, 0.65, 6.15, "보낸 메시지", fs=10, ha="left", color=INK)
    for r, m in enumerate(MSGS):
        y = 5.45 - r * 0.52
        for k, wd in enumerate(m):
            cell(ax, 0.65 + k * 1.05, y, 0.98, 0.42, wd, fs=9.5)
    ax.add_patch(Rectangle((0.6, 2.75), 4.4, 0.5, fc=PINK if typed_hot else "white", ec=RED if typed_hot else INK, lw=1.4))
    label(ax, 0.8, 3.0, typed + " |", fs=12, ha="left", color=RED if typed_hot else "#222", bold=typed_hot)
    for k in range(3):
        x = 0.6 + k * 1.5
        if sugg is None:
            empty(ax, x, 2.05, 1.4, 0.5)
        elif not sugg:
            empty(ax, x, 2.05, 1.4, 0.5, "?" if k == 1 else "", color=RED)
        elif k < len(sugg):
            cell(ax, x, 2.05, 1.4, 0.5, sugg[k], hot=k in hot, fs=11.5)
        else:
            empty(ax, x, 2.05, 1.4, 0.5)
    for r in range(2):
        for k in range(8):
            ax.add_patch(Rectangle((0.65 + k * 0.54 + r * 0.27, 1.45 - r * 0.42), 0.44, 0.33, fc=LIGHT, ec="none"))


def program(ax, name, lines=(), hot=False):
    x, y, w, h = CYL
    cylinder(ax, *CYL, name)
    for k, t in enumerate(lines):
        label(ax, x + w / 2, y + 1.0 - k * 0.55, t, fs=10.5, color=RED if hot else "#222", bold=hot)


def opening(ax, step):
    program(ax, "자판 속 프로그램")
    phone(ax, "오늘", ["점심", "날씨", "저녁"], typed_hot=True, hot=(0, 1, 2))
    bubble(ax, *SAY, "아직 안 친 낱말을\n미리 맞혀서 띄웠어요", TAIL, hot=True)
    moral(ax, 6.0, 0.4, "자판은 다음 낱말을 맞혀서 띄워요")


# ── 챗봇: 다음 낱말 하나를 맞히고 붙이기를 되풀이 ──────────────────
ANSWER = ["따뜻한", "국수", "어때요?"]


def chat(ax, step):
    program(ax, "챗봇 속 프로그램")
    box(ax, 0.4, 0.9, 4.8, 5.55, fc="white")
    label(ax, 0.65, 6.15, "챗봇과 나눈 이야기", fs=10, ha="left", color=INK)
    ax.add_patch(Rectangle((2.1, 4.95), 2.85, 0.6, fc=LIGHT, ec=INK, lw=1.2))
    label(ax, 3.52, 5.25, "점심 뭐 먹지?", fs=11.5)
    label(ax, 4.95, 4.7, "내 질문", fs=9, ha="right", color=INK)
    label(ax, 0.65, 4.2, "챗봇의 답", fs=9, ha="left", color=INK)
    for k in range(2):
        cell(ax, 0.65 + k * 1.45, 3.35, 1.35, 0.6, ANSWER[k], hot=k == 1, fs=11.5)
    empty(ax, 0.65 + 2 * 1.45, 3.35, 1.35, 0.6, "?", color=RED)
    bubble(ax, *SAY, "\"국수\"를 붙이고\n또 다음 낱말을 맞혀요", TAIL, hot=True)
    moral(ax, 6.0, 0.4, "맞히고 붙이기를 되풀이해서 긴 답을 써요")


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


def table_row(ax, x, y, front, items, hot=False, fw=1.05, iw=1.2, gap=0.12, hot_items=(), fs=10):
    cell(ax, x, y, fw, 0.46, front, hot=hot, fs=10.5)
    arrow(ax, (x + fw + 0.05, y + 0.23), (x + fw + 0.42, y + 0.23), color=GREY, ms=9, lw=1.2)
    for k, (wd, n) in enumerate(items):
        cell(ax, x + fw + 0.5 + k * (iw + gap), y, iw, 0.46, f"{wd} {n}", hot=hot or k in hot_items, fs=fs)


def table1(ax, x, y0, dy=TDY, start=False, ends=False, hot_rows=(), start_hot=False, ends_hot=False):
    """앞 낱말 1개 표. start=(처음) 줄을 그릴지, ends=(끝) 줄을 그릴지."""
    for k, (front, items) in enumerate(TABLE):
        if front == ST and not start:
            continue
        hot = front in hot_rows or (front == ST and start_hot)
        table_row(ax, x, y0 - k * dy, front, items, hot=hot)
    if ends:
        label(ax, x, y0 - 8 * dy + 0.23, ENDS, fs=10, ha="left", color=RED if ends_hot else "#222", bold=ends_hot)


def tally(ax, step):
    label(ax, 0.3, 6.95, "보낸 메시지", fs=11.5, ha="left", bold=True)
    label(ax, TX, 6.95, "횟수표 (앞 낱말 → 다음 낱말 횟수)", fs=11.5, ha="left", bold=True)
    if step == 1:
        msg_rows(ax, {(0, 1), (1, 1), (3, 1)})
        for k, (front, items) in enumerate(TABLE):
            if front == ST:
                continue
            y = TY0 - k * TDY
            if front == "오늘":
                table_row(ax, TX, y, front, items, hot=True)
            else:
                cell(ax, TX, y, 1.05, 0.46, front, fs=10.5)
                empty(ax, TX + 1.55, y, 3.84, 0.46)
        label(ax, 2.6, 2.5, "\"오늘\" 바로 다음 낱말을 세요", fs=11, color=RED)
    else:
        msg_rows(ax)
        table1(ax, TX, TY0, hot_rows=[f for f, _ in TABLE if f not in (ST, "오늘")])
        moral(ax, 6.0, 0.75, "앞 낱말마다 다음에 온 낱말을 셌어요")


# ── 후보를 누르면: 누른 낱말이 새 앞 낱말 ──────────────────────────
def press(ax, step):
    program(ax, "언어 모델")
    phone(ax, "오늘 점심", ["뭐", "같이"], typed_hot=True, hot=(0, 1))
    bubble(ax, *SAY, "누른 \"점심\"이 새 앞 낱말이에요\n\"점심\" 줄을 띄워요", TAIL, hot=True)
    moral(ax, 6.0, 0.4, "누를 때마다 앞 낱말이 바뀌어요")


# ── 처음과 끝도 표에 적어요 ────────────────────────────────────────
def edge(ax, step):
    label(ax, 0.3, 6.95, "보낸 메시지", fs=11.5, ha="left", bold=True)
    label(ax, TX, 6.95, "횟수표 (앞 낱말 → 다음 낱말 횟수)", fs=11.5, ha="left", bold=True)
    msg_rows(ax, {(r, 0) for r in range(5)} | {(r, len(m) - 1) for r, m in enumerate(MSGS)})
    table1(ax, TX, TY0, start=True, ends=True, start_hot=True, ends_hot=True)
    label(ax, 2.6, 2.5, "메시지의 첫 낱말과 끝 낱말을 세요", fs=11, color=RED)
    moral(ax, 6.0, 0.75, "메시지의 처음과 끝도 표에 적어요")


# ── 뽑기: 제비 통 ──────────────────────────────────────────────────
TICKETS = ["오늘", "오늘", "오늘", "내일", "날씨"]


def ticket_box(ax, x, y, words, taken=None, tw=1.05):
    w = len(words) * (tw + 0.15) + 0.35
    box(ax, x, y, w, 1.05, fc=PAPER)
    for k, wd in enumerate(words):
        tx = x + 0.25 + k * (tw + 0.15)
        if k == taken:
            empty(ax, tx, y + 0.25, tw, 0.55)
        else:
            cell(ax, tx, y + 0.25, tw, 0.55, wd, fs=11)
    return x + w


def draw(ax, step):
    label(ax, 0.3, 6.2, "(처음) 줄에서 첫 낱말 뽑기", fs=11.5, ha="left", bold=True)
    table_row(ax, 0.5, 5.0, ST, TABLE[0][1])
    label(ax, 0.5, 3.75, "제비뽑기 쪽지를 넣은 통", fs=10.5, ha="left", color=INK)
    end = ticket_box(ax, 0.5, 2.35, TICKETS, taken=3)
    arrow(ax, (end + 0.1, 2.9), (end + 1.3, 2.9), color=RED, ms=14)
    cell(ax, end + 1.45, 2.6, 1.15, 0.6, "내일", hot=True, fs=12)
    label(ax, 0.5 + (end - 0.5) / 2, 1.85, "오늘 3장, 내일 1장, 날씨 1장", fs=10.5, color=INK)
    moral(ax, 6.0, 0.9, "많이 나온 낱말일수록 자주 뽑혀요")


# ── 이어 붙이기와 엉킴: 같은 무대 ─────────────────────────────────
OX, OY, OW = 0.5, 5.0, 1.15


def chain_stage(ax, out, hot_out, front, tickets, pick, end_moral=None):
    label(ax, 0.3, 6.2, "뽑은 문장", fs=11.5, ha="left", bold=True)
    for k, wd in enumerate(out):
        cell(ax, OX + k * (OW + 0.1), OY, OW, 0.6, wd, hot=k == hot_out, fs=12)
    label(ax, 0.3, 4.05, "앞 낱말", fs=10.5, ha="left", color=INK)
    cell(ax, 0.5, 2.9, 1.15, 0.6, front, fs=12)
    arrow(ax, (1.75, 3.2), (2.35, 3.2), color=GREY, ms=11, lw=1.3)
    label(ax, 2.5, 2.35, "그 줄의 제비", fs=10.5, ha="left", color=INK)
    ticket_box(ax, 2.45, 2.65, tickets)
    px = 2.45 + 0.25 + pick * 1.2
    cell(ax, px, 2.9, 1.05, 0.55, tickets[pick], hot=True, fs=11)
    tx = OX + hot_out * (OW + 0.1) + OW / 2
    arrow(ax, (px + 0.52, 3.55), (tx, OY - 0.08), color=RED, ms=13)
    if end_moral:
        moral(ax, 6.0, 1.0, end_moral)


def chain(ax, step):
    chain_stage(ax, ["내일", "점심", "뭐", "먹지", EN], 3, "뭐", ["먹지", "먹을까", "이래"], 0,
                end_moral="보낸 적 없는 문장이 나왔어요")


def tangle(ax, step):
    chain_stage(ax, ["내일", "점심", "뭐", "이래"], 3, "뭐", ["먹지", "먹을까", "이래"], 2,
                end_moral="말이 안 되는 문장이 나왔어요")


# ── 엉킴의 원인: 세 메시지의 "뭐"가 한 줄로 모여요 ─────────────────
MWO = [(0, 2), (3, 2), (4, 1)]  # "뭐"가 있는 (줄, 칸)
RX, RW = 6.6, 0.9


def mo_arrow(ax, r, k, to_y, color):
    x, y = word_xy(r, k + 1)
    arrow(ax, (x + 0.95 + 0.05, y + 0.25), (RX - 0.08, to_y + 0.23), color=color, ms=11, lw=1.5)


def merge(ax, step):
    label(ax, 0.3, 6.95, "보낸 메시지", fs=11.5, ha="left", bold=True)
    label(ax, RX, 6.95, "앞 낱말 1개 표의 \"뭐\" 줄", fs=11.5, ha="left", bold=True)
    ry = 4.6
    msg_rows(ax, dim_words={(r, k - 1) for r, k in MWO})
    for r, k in MWO:
        mo_arrow(ax, r, k, ry, RED)
    table_row(ax, RX, ry, "뭐", TABLE[7][1], fw=RW, iw=1.1, gap=0.1, hot=True)
    label(ax, RX, 3.6, "세 메시지가 한 줄로 모여요\n\"뭐\" 줄에는 앞 낱말이 적히지 않아요", fs=10.5, ha="left",
          color=RED, va="top")
    moral(ax, 6.0, 0.75, "\"뭐\" 줄만 봐서는 어느 메시지에서 왔는지 몰라요")


# ── "뭐" 줄을 앞 낱말로 나눠요 ─────────────────────────────────────
SPLIT = [((0, 2), "점심 뭐", "먹지", 5.5), ((3, 2), "저녁 뭐", "먹을까", 4.6), ((4, 1), "날씨 뭐", "이래", 3.7)]


def split(ax, step):
    label(ax, 0.3, 6.95, "보낸 메시지", fs=11.5, ha="left", bold=True)
    label(ax, RX, 6.95, "앞 낱말 2개 표", fs=11.5, ha="left", bold=True)
    msg_rows(ax)
    for (r, k), front, nxt, y in SPLIT:
        mo_arrow(ax, r, k, y, RED)
        cell(ax, RX, y, 1.5, 0.46, front, fs=10.5, hot=True)
        arrow(ax, (RX + 1.55, y + 0.23), (RX + 1.95, y + 0.23), color=GREY, ms=9, lw=1.2)
        cell(ax, RX + 2.05, y, 1.4, 0.46, f"{nxt} 1", fs=10, hot=True)
    label(ax, RX, 2.9, "\"뭐\" 한 줄이 세 줄로 갈라져요", fs=10.5, ha="left", color=RED)
    moral(ax, 6.0, 0.75, "\"내일 점심 뭐\" 다음은 \"점심 뭐\" 줄의 먹지뿐이에요")


# ── 막힘: 처음 보는 짝 ─────────────────────────────────────────────
def stuck(ax, step):
    program(ax, "언어 모델", ["앞 낱말 2개 표의 \"내일\" 줄", "내일 점심 → 같이 1"])
    phone(ax, "내일 저녁", [], typed_hot=True)
    bubble(ax, *SAY, "\"내일 저녁\" 줄이\n표에 없어요", TAIL, hot=True)
    moral(ax, 6.0, 0.4, "처음 보는 짝 앞에서는 아무것도 못 띄워요")


# ── 막힘의 원인: 12 × 12 칸 ────────────────────────────────────────
GX, GTOP, GC = 1.35, 7.0, 0.48


def grid(ax, step):
    label(ax, 0.3, 8.75, "낱말 12개로 만들 수 있는 두 낱말 짝", fs=11.5, ha="left", bold=True)
    label(ax, GX + 6 * GC, 8.2, "둘째 낱말 →", fs=9.5, color=INK)
    label(ax, GX - 0.08, 7.25, "첫 낱말 ↓", fs=9.5, ha="right", color=INK)
    for i, wd in enumerate(WORDS):
        y = GTOP - (i + 1) * GC
        label(ax, GX - 0.08, y + GC / 2, wd, fs=9, ha="right")
    for j, wd in enumerate(WORDS):
        label(ax, GX + j * GC + GC / 2, GTOP + 0.06, wd, fs=8.5, rotation=90, va="bottom")
    for i, a in enumerate(WORDS):
        for j, b in enumerate(WORDS):
            x, y = GX + j * GC, GTOP - (i + 1) * GC
            seen = (a, b) in PAIRS
            if seen:
                fc, ec, lw = RED, RED, 1.0
            else:
                fc, ec, lw = "white", GREY, 0.8
            ax.add_patch(Rectangle((x, y), GC, GC, fc=fc, ec=ec, lw=lw))
    label(ax, 7.6, 5.6, "짝은 12 × 12 = 144가지\n메시지에 나온 짝은\n13가지뿐이에요", fs=10.5, ha="left", color=RED,
          va="top")
    i, j = WORDS.index("내일"), WORDS.index("저녁")
    x, y = GX + j * GC, GTOP - (i + 1) * GC
    ax.add_patch(Rectangle((x - 0.04, y - 0.04), GC + 0.08, GC + 0.08, fill=False, ec=RED, lw=2.4))
    label(ax, x + GC / 2, y + GC / 2, "?", fs=11, color=RED, bold=True)
    label(ax, 7.6, 4.2, "\"내일 저녁\" 칸은 비어 있어요\n그래서 줄이 없어요", fs=10.5, ha="left", color=RED, va="top")
    moral(ax, 6.0, 0.45, "아는 낱말끼리도 처음 보는 짝이면 막혀요")


# ── 세기의 벽: 짧게 보면 엉키고 길게 보면 막혀요 ───────────────────
def wall(ax, step):
    for x0, title, verdict in [(0.3, "앞 낱말 하나를 보면", "엉켜요"), (6.1, "앞 낱말 둘을 보면", "막혀요")]:
        box(ax, x0, 1.55, 5.6, 4.75, fc="white")
        label(ax, x0 + 2.8, 5.85, title, fs=11.5, bold=True)
        label(ax, x0 + 2.8, 2.05, verdict, fs=14, color=RED, bold=True)
    for k, wd in enumerate(["내일", "점심", "뭐", "이래"]):
        cell(ax, 0.6 + k * 1.27, 4.35, 1.17, 0.6, wd, hot=k == 3, fs=12)
    label(ax, 3.1, 3.3, "\"뭐\" 줄에 세 메시지가\n섞여 있어서", fs=10.5, color=INK)
    for k, wd in enumerate(["내일", "저녁"]):
        cell(ax, 6.5 + k * 1.27, 4.35, 1.17, 0.6, wd, fs=12)
    arrow(ax, (9.05, 4.65), (9.65, 4.65), color=GREY, ms=11, lw=1.3)
    empty(ax, 9.75, 4.35, 1.17, 0.6, "?", color=RED)
    label(ax, 8.9, 3.3, "\"내일 저녁\" 줄이\n표에 없어서", fs=10.5, color=INK)
    moral(ax, 6.0, 0.8, "세기로는 엉킴과 막힘을 같이 풀 수 없어요")


# ── 정리: 처음 장면으로 돌아가기 ───────────────────────────────────
def back(ax, step):
    phone(ax, "오늘", ["점심", "날씨", "저녁"], hot=(0, 1, 2))
    program(ax, "언어 모델", ["횟수표 \"오늘\" 줄", "점심 1 · 날씨 1 · 저녁 1"])
    bubble(ax, *SAY, "앞 낱말 하나만 보면 돼요", TAIL, hot=True)
    moral(ax, 6.0, 0.4, "후보 몇 개 띄우기는 세기로 충분해요")


# ── 정리: 낱말 카드 ────────────────────────────────────────────────
def cards():
    """이 편 본문에서 이름 붙인 말 하나. 본문 그림을 작게 다시 그리고 한 줄 뜻."""
    fig, ax = canvas(6.4, 2.1, 9.8, 3.25)
    W, H = 9.4, 2.9
    x, y = 0.2, 0.2
    box(ax, x, y, W, H, fc="white")
    label(ax, x + 0.3, y + H - 0.45, "언어 모델", fs=12.5, ha="left", bold=True)
    label(ax, x + 6.9, y + 1.1, "앞 낱말을 보고\n다음 낱말을 맞히는 프로그램", fs=10, color=INK)
    cylinder(ax, x + 0.5, y + 0.55, 1.6, 0.8, "")
    bubble(ax, x + 2.5, y + 1.45, 1.9, 0.7, "점심?", (x + 2.1, y + 1.0), hot=True, fs=10.5)
    save(fig, OUT, "ai01-cards.svg")


if __name__ == "__main__":
    stage(opening, 1, OUT, "ai01-open", S, L)
    stage(chat, 1, OUT, "ai01-chat", S, L)
    stage(tally, 2, OUT, "ai01-tally", *T)
    stage(press, 1, OUT, "ai01-press", S, L)
    stage(edge, 1, OUT, "ai01-edge", *T)
    stage(draw, 1, OUT, "ai01-draw", S, L)
    stage(chain, 1, OUT, "ai01-chain", S, L)
    stage(tangle, 1, OUT, "ai01-tangle", S, L)
    stage(merge, 1, OUT, "ai01-merge", *T)
    stage(split, 1, OUT, "ai01-split", *T)
    stage(stuck, 1, OUT, "ai01-stuck", S, L)
    stage(grid, 1, OUT, "ai01-grid", (7.2, 5.4), (12, 9.0))
    stage(wall, 1, OUT, "ai01-wall", S, L)
    stage(back, 1, OUT, "ai01-back", S, L)
    cards()
