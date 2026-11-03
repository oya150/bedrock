"""AI 1편 그림 만들기. 실행: python lab/fig_ai01.py  → docs/ai/img/01/*.svg

본문 절은 장면 띠로 그린다: 같은 무대를 여러 장 그리고 장마다 바뀐 곳만 빨강으로 칠한다.
예시는 보낸 메시지 다섯 개와 그 횟수표를 편 끝까지 잇는다(.claude/writing/work/cal/units-ai01.md).
숫자는 모두 이 다섯 메시지로 직접 센 것이다.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "es"))
from figkit import (GREY, INK, LIGHT, NOTE, PAPER, PINK, RED, arrow, box, bubble, canvas, cell,  # noqa: E402
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


def phone(ax, typed, sugg, typed_hot=False, hot=(), dim=False, hot_words=()):
    """sugg=None이면 후보 칸 셋이 빈 점선, 빈 목록이면 빈칸에 빨간 물음표. hot=빨간 후보 번호, hot_words={(줄, 칸)}."""
    box(ax, 0.4, 0.9, 4.8, 5.55, fc="white")
    label(ax, 0.65, 6.15, "보낸 메시지", fs=10, ha="left", color=INK)
    for r, m in enumerate(MSGS):
        y = 5.45 - r * 0.52
        for k, wd in enumerate(m):
            cell(ax, 0.65 + k * 1.05, y, 0.98, 0.42, wd, hot=(r, k) in hot_words, fs=9.5)
    ax.add_patch(Rectangle((0.6, 2.75), 4.4, 0.5, fc=PINK if typed_hot else "white", ec=RED if typed_hot else INK, lw=1.4))
    label(ax, 0.8, 3.0, typed + " |", fs=12, ha="left", color=RED if typed_hot else "#222", bold=typed_hot)
    for k in range(3):
        x = 0.6 + k * 1.5
        if sugg is None:
            empty(ax, x, 2.05, 1.4, 0.5)
        elif not sugg:
            empty(ax, x, 2.05, 1.4, 0.5, "?" if k == 1 else "", color=RED)
        elif k < len(sugg):
            cell(ax, x, 2.05, 1.4, 0.5, sugg[k], hot=k in hot, dim=dim, fs=11.5)
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
    if step == 1:
        phone(ax, "오늘", None, typed_hot=True)
        bubble(ax, *SAY, "\"오늘\" 다음에 올 낱말을\n골라야 해요", TAIL)
    elif step == 2:
        phone(ax, "오늘", ["점심", "날씨", "저녁"], hot=(0, 1, 2))
        bubble(ax, *SAY, "이 셋을 띄웠어요", TAIL, hot=True)
    else:
        phone(ax, "오늘", ["점심", "날씨", "저녁"], hot_words={(0, 1), (1, 1), (3, 1)})
        bubble(ax, *SAY, "이 셋을 띄웠어요", TAIL)
        moral(ax, 6.0, 0.4, "셋 다 보낸 메시지에서 \"오늘\" 바로 다음에 있었어요")


# ── 횟수표: 보낸 메시지 → 앞 낱말마다 다음 낱말 횟수 ──────────────
TX, TY0, TDY = 5.5, 6.15, 0.56


def msg_rows(ax, hot_words=(), dim_words=(), x0=0.75, y0=6.15, dy=0.65, w=0.95, hot_rows=()):
    """보낸 메시지 다섯 줄을 낱말 칸으로. hot_words={(줄, 칸)}, hot_rows=줄 번호(0부터)."""
    for r, m in enumerate(MSGS):
        y = y0 - r * dy
        label(ax, x0 - 0.3, y + 0.25, str(r + 1), fs=10, color=RED if r in hot_rows else INK, bold=r in hot_rows)
        for k, wd in enumerate(m):
            cell(ax, x0 + k * (w + 0.06), y, w, 0.5, wd, hot=(r, k) in hot_words or r in hot_rows,
                 dim=(r, k) in dim_words, fs=10.5)


def word_xy(r, k, x0=0.75, y0=6.15, dy=0.65, w=0.95):
    """msg_rows 기본 배치에서 (줄, 칸) 칸의 왼쪽 아래."""
    return x0 + k * (w + 0.06), y0 - r * dy


def table_row(ax, x, y, front, items, hot=False, fw=1.05, iw=1.2, gap=0.12, hot_items=(), fs=10):
    cell(ax, x, y, fw, 0.46, front, fs=10.5)
    arrow(ax, (x + fw + 0.05, y + 0.23), (x + fw + 0.42, y + 0.23), color=GREY, ms=9, lw=1.2)
    for k, (wd, n) in enumerate(items):
        cell(ax, x + fw + 0.5 + k * (iw + gap), y, iw, 0.46, f"{wd} {n}", hot=hot or k in hot_items, fs=fs)


def table1(ax, x, y0, dy=TDY, start=False, ends=False, hot_rows=(), hot_cells=(), start_hot=False, ends_hot=False):
    """앞 낱말 1개 표. start=(처음) 줄을 그릴지, ends=(끝) 줄을 그릴지. hot_cells={(앞 낱말, 다음 낱말)}."""
    for k, (front, items) in enumerate(TABLE):
        if front == ST and not start:
            continue
        hot = front in hot_rows or (front == ST and start_hot)
        picks = tuple(j for j, (wd, _) in enumerate(items) if (front, wd) in hot_cells)
        table_row(ax, x, y0 - k * dy, front, items, hot=hot, hot_items=picks)
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
    if step == 1:
        phone(ax, "오늘", ["점심", "날씨", "저녁"], hot=(0,))
        bubble(ax, *SAY, "\"점심\"을 눌렀어요", TAIL, hot=True)
    elif step == 2:
        phone(ax, "오늘 점심", ["뭐", "같이"], typed_hot=True, hot=(0, 1))
        bubble(ax, *SAY, "이제 앞 낱말은 \"점심\"이에요\n\"점심\" 줄을 띄워요", TAIL, hot=True)
    else:
        phone(ax, "오늘 점심 뭐", ["먹지", "먹을까", "이래"], typed_hot=True, hot=(0, 1, 2))
        bubble(ax, *SAY, "\"뭐\"를 눌렀으니\n\"뭐\" 줄을 띄워요", TAIL, hot=True)
        moral(ax, 6.0, 0.4, "누른 낱말이 새 앞 낱말이 돼요")


# ── 처음과 끝도 표에 적어요 ────────────────────────────────────────
def edge(ax, step):
    label(ax, 0.3, 6.95, "보낸 메시지", fs=11.5, ha="left", bold=True)
    label(ax, TX, 6.95, "횟수표 (앞 낱말 → 다음 낱말 횟수)", fs=11.5, ha="left", bold=True)
    if step == 1:
        msg_rows(ax, {(r, 0) for r in range(5)})
        table1(ax, TX, TY0, start=True, start_hot=True)
        label(ax, 2.6, 2.5, "메시지의 첫 낱말을 세요", fs=11, color=RED)
    else:
        msg_rows(ax, {(r, len(m) - 1) for r, m in enumerate(MSGS)})
        table1(ax, TX, TY0, start=True, ends=True, ends_hot=True)
        label(ax, 2.6, 2.5, "메시지의 끝 낱말을 세요", fs=11, color=RED)
        moral(ax, 6.0, 0.75, "메시지의 처음과 끝도 표에 적어요")


# ── 늘 1등만 누르면 ────────────────────────────────────────────────
def sentence(ax, words, hot=(), dim=(), x0=6.9, y=5.55, title="누른 문장"):
    label(ax, x0, y + 0.95, title, fs=11.5, ha="left", bold=True)
    for k, wd in enumerate(words):
        cell(ax, x0 + k * 1.15, y, 1.05, 0.55, wd, hot=k in hot, dim=k in dim, fs=11.5)


def best(ax, step):
    label(ax, 0.3, 6.95, "횟수표", fs=11.5, ha="left", bold=True)
    if step == 1:
        table1(ax, 0.5, TY0, start=True, ends=True, hot_cells={(ST, "오늘")})
        sentence(ax, ["오늘"], hot=(0,))
        label(ax, 6.9, 4.4, "(처음) 줄의 1등은 \"오늘\" 3번", fs=11, ha="left", color=RED)
    elif step == 2:
        table1(ax, 0.5, TY0, start=True, ends=True, hot_rows=("오늘",))
        sentence(ax, ["오늘"])
        label(ax, 6.9, 4.4, "\"오늘\" 줄은 셋 다 1번이에요\n1등이 없어요", fs=11, ha="left", color=RED, va="top")
    else:
        table1(ax, 0.5, TY0, start=True, ends=True, hot_cells={("오늘", "점심"), ("점심", "뭐"), ("뭐", "먹지")})
        sentence(ax, ["오늘", "점심", "뭐", "먹지"], hot=(1, 2, 3))
        label(ax, 6.9, 4.4, "같으면 맨 앞 것을 눌러요", fs=11, ha="left", color=RED)
        moral(ax, 6.0, 0.9, "1등만 누르면 늘 \"오늘 점심 뭐 먹지\"가 나와요")


# ── 뽑기: 제비 통 ──────────────────────────────────────────────────
TICKETS = ["오늘", "오늘", "오늘", "내일", "날씨"]


def ticket_box(ax, x, y, words, hot=False, taken=None, tw=1.05):
    w = len(words) * (tw + 0.15) + 0.35
    box(ax, x, y, w, 1.05, fc=PAPER)
    for k, wd in enumerate(words):
        tx = x + 0.25 + k * (tw + 0.15)
        if k == taken:
            empty(ax, tx, y + 0.25, tw, 0.55)
        else:
            cell(ax, tx, y + 0.25, tw, 0.55, wd, hot=hot, fs=11)
    return x + w


def draw(ax, step):
    label(ax, 0.3, 6.2, "(처음) 줄에서 첫 낱말 뽑기", fs=11.5, ha="left", bold=True)
    table_row(ax, 0.5, 5.0, ST, TABLE[0][1])
    label(ax, 0.5, 3.75, "횟수만큼 제비를 넣은 통", fs=10.5, ha="left", color=INK)
    end = ticket_box(ax, 0.5, 2.35, TICKETS, hot=step == 1, taken=3 if step == 2 else None)
    if step == 1:
        label(ax, 0.5 + (end - 0.5) / 2, 1.85, "오늘 3장, 내일 1장, 날씨 1장", fs=10.5, color=RED)
    else:
        arrow(ax, (end + 0.1, 2.9), (end + 1.3, 2.9), color=RED, ms=14)
        cell(ax, end + 1.45, 2.6, 1.15, 0.6, "내일", hot=True, fs=12)
        label(ax, 0.5 + (end - 0.5) / 2, 1.85, "5번 뽑으면 3번쯤은 오늘, 2번쯤은 다른 낱말", fs=10.5, color=INK)
        moral(ax, 6.0, 0.9, "많이 나온 낱말일수록 자주 뽑혀요")


# ── 이어 붙이기와 엉킴: 같은 무대 ─────────────────────────────────
OX, OY, OW = 0.5, 5.0, 1.15


def chain_stage(ax, out, hot_out, front, tickets, pick, dim_out=(), note=None, end_moral=None, pick_hot=True):
    label(ax, 0.3, 6.2, "뽑은 문장", fs=11.5, ha="left", bold=True)
    for k, wd in enumerate(out):
        cell(ax, OX + k * (OW + 0.1), OY, OW, 0.6, wd, hot=k == hot_out, dim=k in dim_out, fs=12)
    label(ax, 0.3, 4.05, "앞 낱말", fs=10.5, ha="left", color=INK)
    cell(ax, 0.5, 2.9, 1.15, 0.6, front, fs=12)
    arrow(ax, (1.75, 3.2), (2.35, 3.2), color=GREY, ms=11, lw=1.3)
    label(ax, 2.5, 2.35, "그 줄의 제비", fs=10.5, ha="left", color=INK)
    ticket_box(ax, 2.45, 2.65, tickets)
    px = 2.45 + 0.25 + pick * 1.2
    cell(ax, px, 2.9, 1.05, 0.55, tickets[pick], hot=pick_hot, fs=11)
    tx = OX + hot_out * (OW + 0.1) + OW / 2
    arrow(ax, (px + 0.52, 3.55), (tx, OY - 0.08), color=RED if pick_hot else GREY, ms=13)
    if note:
        label(ax, 6.0, 1.75, note, fs=11, color=RED, bold=True)
    if end_moral:
        moral(ax, 6.0, 1.0, end_moral)


CHAIN = [(["내일", "점심"], 1, "내일", ["점심"], 0),
         (["내일", "점심", "뭐"], 2, "점심", ["뭐", "같이"], 0),
         (["내일", "점심", "뭐", "먹지"], 3, "뭐", ["먹지", "먹을까", "이래"], 0),
         (["내일", "점심", "뭐", "먹지", EN], 4, "먹지", [EN], 0)]


def chain(ax, step):
    out, h, front, tk, pick = CHAIN[step - 1]
    chain_stage(ax, out, h, front, tk, pick, end_moral="보낸 적 없는 문장이 나왔어요" if step == 4 else None)


def tangle(ax, step):
    out = ["내일", "점심", "뭐", "이래"]
    if step == 1:
        chain_stage(ax, out, 3, "뭐", ["먹지", "먹을까", "이래"], 2)
    else:
        chain_stage(ax, out, 3, "뭐", ["먹지", "먹을까", "이래"], 2, dim_out=(0, 1),
                    note="표는 \"뭐\" 줄만 봐요. \"점심\"은 안 봐요",
                    end_moral="날씨 메시지의 \"이래\"가 섞여 나왔어요", pick_hot=False)


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
    if step == 1:
        msg_rows(ax, hot_words=set(MWO))
        cell(ax, RX, ry, RW, 0.46, "뭐", fs=10.5)
        empty(ax, RX + 1.35, ry, 3.6, 0.46)
        label(ax, RX, 3.6, "\"뭐\"는 1번, 4번, 5번에 있어요\n앞 낱말은 점심, 저녁, 날씨예요", fs=10.5, ha="left",
              color=RED, va="top")
        return
    dim = {(r, k - 1) for r, k in MWO} if step == 2 else set()
    msg_rows(ax, dim_words=dim)
    for r, k in MWO:
        mo_arrow(ax, r, k, ry, RED if step == 2 else GREY)
    table_row(ax, RX, ry, "뭐", TABLE[7][1], fw=RW, iw=1.1, gap=0.1, hot=step == 2)
    if step == 2:
        label(ax, RX, 3.6, "세 메시지가 한 줄로 모여요\n점심, 저녁, 날씨는 표에 안 적혀요", fs=10.5, ha="left",
              color=RED, va="top")
    else:
        for j in range(3):
            label(ax, RX + 1.4 + j * 1.2 + 0.55, ry + 0.75, "?", fs=13, color=RED, bold=True)
        label(ax, RX, 3.6, "줄에 적힌 낱말은\n어느 메시지에서 왔는지 몰라요", fs=10.5, ha="left", color=RED, va="top")
        moral(ax, 6.0, 0.75, "\"뭐\" 줄에는 세 메시지의 다음 낱말이 섞여 있어요")


def human(ax, step):
    label(ax, 0.3, 6.95, "보낸 메시지", fs=11.5, ha="left", bold=True)
    msg_rows(ax)
    spans = {1: [(0, 1), (3, 1)], 2: [(4, 0)]}
    for st, rows in spans.items():
        if st > step:
            continue
        for r, k in rows:
            x, y = word_xy(r, k)
            on = st == step
            ax.add_patch(Rectangle((x - 0.07, y - 0.07), 3 * 1.01 + 0.08, 0.64, fill=False,
                                   ec=RED if on else INK, lw=2.2 if on else 1.4))
    label(ax, RX - 0.6, 5.3, "밥 이야기: \"점심 뭐\", \"저녁 뭐\"\n→ 다음은 먹지, 먹을까", fs=10.5, ha="left",
          color=RED if step == 1 else "#222")
    if step == 2:
        label(ax, RX - 0.6, 3.8, "날씨 이야기: \"날씨 뭐\"\n→ 다음은 이래", fs=10.5, ha="left", color=RED)
        moral(ax, 6.0, 1.75, "무슨 이야기인지는 \"뭐\" 앞 낱말에 남아 있어요")


# ── "뭐" 줄을 앞 낱말로 나눠요 ─────────────────────────────────────
SPLIT = [((0, 2), "점심 뭐", "먹지", 5.5), ((3, 2), "저녁 뭐", "먹을까", 4.6), ((4, 1), "날씨 뭐", "이래", 3.7)]


def split(ax, step):
    label(ax, 0.3, 6.95, "보낸 메시지", fs=11.5, ha="left", bold=True)
    label(ax, RX, 6.95, "앞 낱말 2개 표", fs=11.5, ha="left", bold=True)
    msg_rows(ax)
    for (r, k), front, nxt, y in SPLIT:
        mo_arrow(ax, r, k, y, RED if step == 1 else GREY)
        hot = step == 1 or (step == 2 and front == "점심 뭐")
        cell(ax, RX, y, 1.5, 0.46, front, fs=10.5, hot=hot)
        arrow(ax, (RX + 1.55, y + 0.23), (RX + 1.95, y + 0.23), color=GREY, ms=9, lw=1.2)
        cell(ax, RX + 2.05, y, 1.4, 0.46, f"{nxt} 1", fs=10, hot=hot)
    if step == 1:
        label(ax, RX, 2.9, "\"뭐\" 한 줄이 세 줄로 갈라져요", fs=10.5, ha="left", color=RED)
    else:
        label(ax, RX, 2.9, "\"내일 점심 뭐\" 다음은\n\"점심 뭐\" 줄에서 골라요 → 먹지", fs=10.5, ha="left",
              color=RED, va="top")
        moral(ax, 6.0, 0.75, "갈라진 세 줄은 다음 낱말이 하나씩이에요")


# ── 앞 낱말 2개 표 전체와 따라가기 ─────────────────────────────────
TABLE2 = [((ST, ST), [("오늘", 3), ("내일", 1), ("날씨", 1)]), ((ST, "오늘"), [("점심", 1), ("날씨", 1), ("저녁", 1)]),
          ((ST, "내일"), [("점심", 1)]), ((ST, "날씨"), [("뭐", 1)]), (("오늘", "점심"), [("뭐", 1)]),
          (("오늘", "날씨"), [("좋다", 1)]), (("오늘", "저녁"), [("뭐", 1)]), (("내일", "점심"), [("같이", 1)]),
          (("날씨", "뭐"), [("이래", 1)]), (("점심", "뭐"), [("먹지", 1)]), (("점심", "같이"), [("먹자", 1)]),
          (("저녁", "뭐"), [("먹을까", 1)]), (("뭐", "먹지"), [(EN, 1)]), (("날씨", "좋다"), [(EN, 1)]),
          (("같이", "먹자"), [(EN, 1)]), (("뭐", "먹을까"), [(EN, 1)]), (("뭐", "이래"), [(EN, 1)])]
PATH = {(ST, ST): ("①", "오늘"), (ST, "오늘"): ("②", "저녁"), ("오늘", "저녁"): ("③", "뭐"),
        ("저녁", "뭐"): ("④", "먹을까"), ("뭐", "먹을까"): ("⑤", EN)}


def table2_draw(ax, on_rows=(), numbers=False):
    label(ax, 0.3, 7.0, "앞 낱말 2개 표 (앞 낱말 둘 → 다음 낱말 횟수)", fs=11.5, ha="left", bold=True)
    for k, (front, items) in enumerate(TABLE2):
        col, row = (0, k) if k < 9 else (1, k - 9)
        x, y = (0.6 if col == 0 else 6.7), 6.2 - row * 0.56
        on = front in on_rows
        if front in PATH and numbers:
            label(ax, x - 0.3, y + 0.23, PATH[front][0], fs=10.5, color=RED if on else INK, bold=on)
        cell(ax, x, y, 2.0, 0.46, " ".join(front), hot=on, fs=10)
        arrow(ax, (x + 2.05, y + 0.23), (x + 2.4, y + 0.23), color=GREY, ms=9, lw=1.2)
        for j, (wd, n) in enumerate(items):
            cell(ax, x + 2.5 + j * 1.15, y, 1.05, 0.46, f"{wd} {n}", hot=on and PATH[front][1] == wd, fs=9.5)


def table2(ax, step):
    table2_draw(ax)
    label(ax, 6.7, 1.0, "문장 맨 앞은 (처음)으로 채워요", fs=10.5, ha="left", color=INK)


def path(ax, step):
    if step == 1:
        table2_draw(ax, on_rows=[(ST, ST), (ST, "오늘")], numbers=True)
        label(ax, 6.7, 1.0, "첫 두 낱말은 제비로 뽑아요", fs=10.5, ha="left", color=RED)
    else:
        table2_draw(ax, on_rows=[("오늘", "저녁"), ("저녁", "뭐"), ("뭐", "먹을까")], numbers=True)
        label(ax, 6.7, 1.0, "③ ~ ⑤ 줄은 다음 낱말이 하나뿐이에요", fs=10.5, ha="left", color=RED)
        moral(ax, 6.0, 0.35, "4번 메시지 \"오늘 저녁 뭐 먹을까\"와 똑같아요")


# ── 둘째 값: 베낌 ──────────────────────────────────────────────────
def copy(ax, step):
    label(ax, 0.3, 6.2, "보낸 메시지", fs=11.5, ha="left", bold=True)
    label(ax, 5.6, 6.2, "앞 낱말 2개 표로 뽑은 문장", fs=11.5, ha="left", bold=True)
    msg_rows(ax, hot_rows={1: (3,), 2: (2,)}[step], y0=5.3, dy=0.75)
    got = [("오늘 저녁 뭐 먹을까", "4번과 똑같아요")]
    if step == 2:
        got.append(("내일 점심 같이 먹자", "3번과 똑같아요"))
    for k, (s, why) in enumerate(got):
        y = 5.3 - k * 0.95
        hot = k == step - 1
        cell(ax, 5.6, y, 3.4, 0.5, s, hot=hot, fs=11)
        label(ax, 9.15, y + 0.25, why, fs=10, ha="left", color=RED if hot else INK)
    if step == 2:
        y = 3.3
        empty(ax, 5.6, y, 3.4, 0.5, color=RED)
        label(ax, 7.3, y + 0.25, "내일 점심 뭐 먹지", fs=11, color=RED)
        ax.plot([5.7, 8.9], [y + 0.25, y + 0.25], color=RED, lw=1.6)
        label(ax, 9.15, y + 0.25, "이제 못 만들어요", fs=10, ha="left", color=RED)
        label(ax, 7.3, y - 0.4, "\"내일 점심\" 다음은 \"같이\"뿐이에요", fs=10, color=INK)
        moral(ax, 6.0, 0.75, "보낸 문장만 그대로 나와요")


# ── 베낌의 원인: 갈림길 ────────────────────────────────────────────
NODE = {ST: (0.9, 3.4), "오늘": (2.75, 5.3), "내일": (2.75, 1.8),
        "날씨": (4.75, 5.4), "저녁": (4.75, 4.0), "점심": (4.75, 2.5),
        "좋다": (6.75, 5.9), "뭐": (6.75, 4.0), "같이": (6.75, 1.8),
        "먹지": (8.75, 5.0), "먹을까": (8.75, 4.0), "이래": (8.75, 3.0), "먹자": (8.75, 1.8)}
EDGES = [(f, wd) for f, items in TABLE for wd, _ in items]
FORKS = [f for f, items in TABLE if len(items) > 1]  # (처음), 오늘, 날씨, 점심, 뭐
ROUTE = [("내일", "점심"), ("점심", "뭐"), ("뭐", "먹지")]


def fork(ax, step):
    label(ax, 0.3, 6.35, "앞 낱말 1개 표를 길로 그리면", fs=11.5, ha="left", bold=True)
    for a, b in EDGES:
        (x1, y1), (x2, y2) = NODE[a], NODE[b]
        on = step == 1 and (a, b) in ROUTE
        arrow(ax, (x1 + 0.5, y1), (x2 - 0.5, y2), color=RED if on else GREY, ms=10, lw=2.0 if on else 1.2)
    on_route = {w for e in ROUTE for w in e}
    for wd, (x, y) in NODE.items():
        hot = (step == 1 and wd in on_route) or (step == 2 and wd in FORKS)
        cell(ax, x - 0.5, y - 0.25, 1.0, 0.5, wd, hot=hot, fs=10.5)
    if step == 1:
        label(ax, 4.75, 1.75, "3번 길에서\n1번 길로 갈아탔어요", fs=10, color=RED, va="top")
        label(ax, 10.0, 6.35, "\"내일 점심 뭐 먹지\"", fs=11, color=RED, bold=True)
    else:
        label(ax, 6.0, 1.1, "다음 낱말이 둘 이상인 줄 = 갈림길 다섯", fs=10.5, color=RED)
        moral(ax, 6.0, 0.5, "갈림길에서 길을 갈아타면 새 문장이 생겨요")


def roads(ax, step):
    label(ax, 0.3, 6.35, "앞 낱말 2개 표를 길로 그리면", fs=11.5, ha="left", bold=True)
    y0, dy, w = 5.0, 0.9, 1.15
    zone_on = step == 1
    ax.add_patch(Rectangle((0.95, y0 - 4 * dy - 0.15), 2 * (w + 0.45) - 0.3, 4 * dy + 0.8, fill=False,
                           ec=RED if zone_on else GREY, lw=2.0 if zone_on else 1.2, ls="--"))
    label(ax, 2.35, y0 + 0.88, "제비로 고르는 곳", fs=10, color=RED if zone_on else INK, bold=zone_on)
    for r, m in enumerate(MSGS):
        y = y0 - r * dy
        label(ax, 0.55, y + 0.25, str(r + 1), fs=10, color=INK)
        for k, wd in enumerate(m):
            x = 1.05 + k * (w + 0.45)
            hot = step == 2 and r in (0, 2) and k == 1
            cell(ax, x, y, w, 0.5, wd, hot=hot, fs=10.5)
            if k < len(m) - 1:
                arrow(ax, (x + w + 0.03, y + 0.25), (x + w + 0.42, y + 0.25), color=GREY, ms=9, lw=1.2)
    if step == 1:
        label(ax, 8.4, 3.4, "셋째 낱말부터는\n줄마다 다음 낱말이 하나뿐", fs=10.5, ha="left", color=RED, va="center")
    else:
        label(ax, 8.4, 5.25, "\"오늘 점심\" 다음은 뭐뿐", fs=10.5, ha="left", color=RED)
        label(ax, 8.4, 3.4, "\"내일 점심\" 다음은 같이뿐", fs=10.5, ha="left", color=RED)
        moral(ax, 6.0, 0.55, "갈아탈 갈림길이 없어서 출발한 메시지 그대로 가요")


# ── 막힘의 원인: 12 × 12 칸 ────────────────────────────────────────
GX, GTOP, GC = 1.35, 7.0, 0.48


def grid(ax, step):
    label(ax, 0.3, 8.75, "낱말 12개로 만들 수 있는 두 낱말 짝", fs=11.5, ha="left", bold=True)
    label(ax, GX + 6 * GC, 8.2, "둘째 낱말 →", fs=9.5, color=INK)
    label(ax, GX - 0.08, 7.25, "첫 낱말 ↓", fs=9.5, ha="right", color=INK)
    for i, wd in enumerate(WORDS):
        y = GTOP - (i + 1) * GC
        label(ax, GX - 0.08, y + GC / 2, wd, fs=9, ha="right", color=RED if step == 1 else "#222", bold=step == 1)
    if step == 1:
        label(ax, 7.6, 5.6, "앞 낱말 1개 표의 낱말 줄은\n낱말마다 하나예요\n→ 12줄 안쪽\n(처음) 줄은 따로 하나", fs=10.5, ha="left", color=RED,
              va="top")
        return
    for j, wd in enumerate(WORDS):
        label(ax, GX + j * GC + GC / 2, GTOP + 0.06, wd, fs=8.5, rotation=90, va="bottom",
              color=RED if step == 2 else "#222")
    for i, a in enumerate(WORDS):
        for j, b in enumerate(WORDS):
            x, y = GX + j * GC, GTOP - (i + 1) * GC
            seen = (a, b) in PAIRS
            if step == 3 and seen:
                fc, ec, lw = RED, RED, 1.0
            elif step == 4 and seen:
                fc, ec, lw = PINK, INK, 0.8
            else:
                fc, ec, lw = "white", RED if step == 2 else GREY, 0.8
            ax.add_patch(Rectangle((x, y), GC, GC, fc=fc, ec=ec, lw=lw))
    if step == 2:
        label(ax, 7.6, 5.6, "앞 낱말 2개 표의 줄은\n짝마다 하나예요\n12 × 12 = 144가지", fs=10.5, ha="left", color=RED,
              va="top")
    elif step == 3:
        label(ax, 7.6, 5.6, "메시지에 나온 짝은\n13가지뿐이에요\n144칸 가운데 13칸", fs=10.5, ha="left", color=RED,
              va="top")
    else:
        i, j = WORDS.index("내일"), WORDS.index("저녁")
        x, y = GX + j * GC, GTOP - (i + 1) * GC
        ax.add_patch(Rectangle((x - 0.04, y - 0.04), GC + 0.08, GC + 0.08, fill=False, ec=RED, lw=2.4))
        label(ax, x + GC / 2, y + GC / 2, "?", fs=11, color=RED, bold=True)
        label(ax, 7.6, 5.6, "\"내일 저녁\" 칸은 비어 있어요\n그래서 줄이 없어요", fs=10.5, ha="left", color=RED, va="top")
        moral(ax, 6.0, 0.45, "아는 낱말끼리도 처음 보는 짝이면 막혀요")


# ── 전환: 줄을 나눈 대신 치르는 값 ────────────────────────────────
def turn(ax, step):
    if step == 1:
        phone(ax, "오늘 저녁", ["뭐"])
        program(ax, "언어 모델", ["앞 낱말 2개 표"])
        bubble(ax, *SAY, "앞 낱말 둘을 보고\n다음 낱말을 띄워요", TAIL)
        return
    phone(ax, "오늘 저녁", ["뭐"], dim=True)
    program(ax, "언어 모델", ["앞 낱말 2개 표"])
    bubble(ax, 6.3, 0.35, 5.5, 2.2, "", TAIL, hot=True)
    label(ax, 9.05, 2.1, "줄을 나눴더니 무엇이 달라졌을까요?", fs=11.5, color=RED, bold=True)
    for k, t in enumerate(["①", "②"]):
        y = 1.2 - k * 0.6
        label(ax, 6.75, y + 0.2, t, fs=11, color=RED, bold=True)
        empty(ax, 7.1, y, 4.3, 0.42, "?", color=RED)


# ── 첫째 값: 막힘 ──────────────────────────────────────────────────
def stuck(ax, step):
    program(ax, "언어 모델", ["표에서 내일로 시작하는 줄", "내일 점심 → 같이 1"])
    if step == 1:
        phone(ax, "내일 저녁", None, typed_hot=True)
        bubble(ax, *SAY, "\"내일 저녁\" 줄을\n찾아요", TAIL)
    else:
        phone(ax, "내일 저녁", [])
        bubble(ax, *SAY, "\"내일 저녁\" 줄이\n표에 없어요", TAIL, hot=True)
        moral(ax, 6.0, 0.4, "처음 보는 짝 앞에서는 아무것도 못 띄워요")


# ── 언제 쓸모 있을까: 갈림길 ───────────────────────────────────────
def decide():
    fig, ax = canvas(9.4, 3.6, 14, 5.4)
    box(ax, 0.3, 3.3, 5.0, 1.5, fc=NOTE)
    label(ax, 2.8, 4.05, "앞의 한두 낱말만 보고\n맞혀도 되나요?", fs=11.5, bold=True)
    arrow(ax, (5.4, 4.05), (6.9, 4.05), color=RED)
    label(ax, 6.15, 4.4, "예", fs=10.5, color=RED)
    box(ax, 7.0, 3.1, 6.7, 1.9, fc=PINK, ec=RED)
    label(ax, 10.35, 4.05, "세기 모델을 쓸 수 있어요\n검색어 추천,\n어느 나라 말인지 알아맞히기", fs=10.5, color=RED)
    arrow(ax, (2.8, 3.2), (2.8, 2.0))
    label(ax, 3.05, 2.6, "아니요", fs=10.5, color=INK, ha="left")
    box(ax, 0.3, 0.5, 5.0, 1.4, fc=LIGHT, ec=GREY)
    label(ax, 2.8, 1.2, "더 앞을 보고 처음 보는\n짝도 다뤄야 해요", fs=10.5)
    arrow(ax, (5.4, 1.2), (6.9, 1.2))
    box(ax, 7.0, 0.5, 6.7, 1.4, fc=LIGHT, ec=GREY)
    label(ax, 10.35, 1.2, "세기 대신 다른 방법이 필요해요\n(이어지는 편들)", fs=10.5)
    save(fig, OUT, "ai01-decide.svg")


# ── 정리: 처음 장면으로 돌아가기 ───────────────────────────────────
def back(ax, step):
    row = ["횟수표 \"오늘\" 줄", "점심 1 · 날씨 1 · 저녁 1"]
    if step == 1:
        phone(ax, "오늘", None)
        program(ax, "언어 모델")
        bubble(ax, *SAY, "\"오늘\" 다음에 올 낱말을\n골라야 해요", TAIL)
    elif step == 2:
        phone(ax, "오늘", None)
        program(ax, "언어 모델", row, hot=True)
        bubble(ax, *SAY, "횟수표에서 \"오늘\" 줄을 펼쳐요", TAIL, hot=True)
    else:
        phone(ax, "오늘", ["점심", "날씨", "저녁"], hot=(0, 1, 2))
        program(ax, "언어 모델", row)
        bubble(ax, *SAY, "그 줄의 낱말을 띄워요", TAIL)
        moral(ax, 6.0, 0.4, "\"오늘\" 다음에 왔던 낱말을 세어서 띄웠어요")


# ── 정리: 낱말 카드 ────────────────────────────────────────────────
def cards():
    """이 편 본문에서 이름 붙인 말 둘. 카드마다 본문 그림을 작게 다시 그리고 한 줄 뜻."""
    fig, ax = canvas(6.4, 4.2, 9.8, 6.45)
    W, H = 9.4, 2.9

    def card(i, name, line):
        x, y = 0.2, 3.35 - i * 3.15
        box(ax, x, y, W, H, fc="white")
        label(ax, x + 0.3, y + H - 0.45, name, fs=12.5, ha="left", bold=True)
        label(ax, x + 6.9, y + 1.1, line, fs=10, color=INK)
        return x, y

    x, y = card(0, "언어 모델", "앞 낱말을 보고\n다음 낱말을 맞히는 프로그램")
    cylinder(ax, x + 0.5, y + 0.55, 1.6, 0.8, "")
    bubble(ax, x + 2.5, y + 1.45, 1.9, 0.7, "점심?", (x + 2.1, y + 1.0), hot=True, fs=10.5)
    x, y = card(1, "말뭉치", "횟수를 세는 재료로\n모아 둔 글")
    for k, s in enumerate(["오늘 점심 뭐 먹지", "오늘 날씨 좋다", "⋮"]):
        if s == "⋮":
            label(ax, x + 2.3, y + 0.45, s, fs=11, color=INK)
            continue
        cell(ax, x + 0.5, y + 1.55 - k * 0.6, 3.6, 0.48, s, hot=k == 0, fs=10)
    save(fig, OUT, "ai01-cards.svg")


if __name__ == "__main__":
    T = ((7.2, 4.3), (12, 7.4))
    stage(opening, 3, OUT, "ai01-open", S, L)
    stage(tally, 2, OUT, "ai01-tally", *T)
    stage(press, 3, OUT, "ai01-press", S, L)
    stage(edge, 2, OUT, "ai01-edge", *T)
    stage(best, 3, OUT, "ai01-best", *T)
    stage(draw, 2, OUT, "ai01-draw", S, L)
    stage(chain, 4, OUT, "ai01-chain", S, L)
    stage(tangle, 2, OUT, "ai01-tangle", S, L)
    stage(merge, 3, OUT, "ai01-merge", *T)
    stage(human, 2, OUT, "ai01-human", *T)
    stage(split, 2, OUT, "ai01-split", *T)
    stage(table2, 1, OUT, "ai01-table2", *T)
    stage(turn, 2, OUT, "ai01-turn", S, L)
    stage(stuck, 2, OUT, "ai01-stuck", S, L)
    stage(grid, 4, OUT, "ai01-grid", (7.2, 5.4), (12, 9.0))
    stage(path, 2, OUT, "ai01-path", *T)
    stage(copy, 2, OUT, "ai01-copy", S, L)
    stage(fork, 2, OUT, "ai01-fork", S, L)
    stage(roads, 2, OUT, "ai01-roads", S, L)
    decide()
    stage(back, 3, OUT, "ai01-back", S, L)
    cards()
