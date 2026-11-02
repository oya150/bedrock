"""AI 1편 그림 만들기. 실행: python lab/fig_ai01.py  → docs/ai/img/01/*.svg

본문 절은 장면 띠로 그린다: 같은 무대를 여러 장 그리고 장마다 바뀐 곳만 빨강으로 칠한다.
예시는 보낸 메시지 다섯 개와 그 횟수표를 편 끝까지 잇는다(.claude/writing/work/cal/units-ai01.md).
처음 보는 묶음 비율은 lab/ai/01_ngram.py 실측(이 사이트 본문 문장 7,537개)이다.
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
TABLE = [("(처음)", [("오늘", 3), ("내일", 1), ("날씨", 1)]),
         ("오늘", [("점심", 1), ("날씨", 1), ("저녁", 1)]),
         ("내일", [("점심", 1)]),
         ("날씨", [("좋다", 1), ("뭐", 1)]),
         ("점심", [("뭐", 1), ("같이", 1)]),
         ("저녁", [("뭐", 1)]),
         ("같이", [("먹자", 1)]),
         ("뭐", [("먹지", 1), ("먹을까", 1), ("이래", 1)])]
ENDS = "먹지 · 좋다 · 먹자 · 먹을까 · 이래 → (끝)"


def empty(ax, x, y, w, h, s="", color=GREY):
    ax.add_patch(Rectangle((x, y), w, h, fc="white", ec=color, lw=1.2, ls="--"))
    if s:
        label(ax, x + w / 2, y + h / 2, s, fs=12, color=color, bold=color == RED)


# ── 무대: 휴대폰 메시지 자판과 자판 속 프로그램 ────────────────────
CYL = (7.2, 3.35, 4.0, 1.45)
SAY = (6.3, 0.95, 5.5, 1.55)
TAIL = (9.2, 3.1)


def phone(ax, typed, sugg, typed_hot=False, sugg_hot=False, sugg_dim=False):
    """sugg=None이면 후보 칸 셋이 빈 점선, 빈 목록이면 빈칸에 빨간 물음표."""
    box(ax, 0.4, 0.9, 4.8, 5.55, fc="white")
    label(ax, 0.65, 6.15, "보낸 메시지", fs=10, ha="left", color=INK)
    for k, m in enumerate(MSGS):
        s = " ".join(m)
        w = 0.24 * len(s.replace(" ", "")) + 0.12 * (len(m) - 1) + 0.4
        y = 5.5 - k * 0.52
        ax.add_patch(Rectangle((5.0 - w, y), w, 0.42, fc=NOTE, ec=GREY, lw=1.0))
        label(ax, 5.0 - w / 2, y + 0.21, s, fs=10)
    ax.add_patch(Rectangle((0.6, 2.75), 4.4, 0.5, fc=PINK if typed_hot else "white", ec=RED if typed_hot else INK, lw=1.4))
    label(ax, 0.8, 3.0, typed + " |", fs=12, ha="left", color=RED if typed_hot else "#222", bold=typed_hot)
    for k in range(3):
        x = 0.6 + k * 1.5
        if sugg is None:
            empty(ax, x, 2.05, 1.4, 0.5)
        elif not sugg:
            empty(ax, x, 2.05, 1.4, 0.5, "?" if k == 1 else "", color=RED)
        elif k < len(sugg):
            if sugg_hot:
                cell(ax, x, 2.05, 1.4, 0.5, sugg[k], hot=True, fs=11.5)
            else:
                cell(ax, x, 2.05, 1.4, 0.5, sugg[k], dim=sugg_dim, fs=11.5)
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
    if step == 1:
        phone(ax, "오늘", None, typed_hot=True)
        program(ax, "자판 속 프로그램")
        bubble(ax, *SAY, "\"오늘\" 다음에 올 낱말을\n골라야 해요", TAIL)
    else:
        phone(ax, "오늘", ["점심", "날씨", "저녁"], sugg_hot=True)
        program(ax, "자판 속 프로그램")
        bubble(ax, *SAY, "이 셋을 띄웠어요", TAIL, hot=True)
        moral(ax, 6.0, 0.4, "셋 다 보낸 메시지에 있던 낱말이에요")


# ── 횟수표 세기 ────────────────────────────────────────────────────
TX, TY0, TDY = 5.5, 6.15, 0.56


def msg_rows(ax, hot_words=(), x0=0.75, y0=6.15, dy=0.65, w=0.95, hot_rows=()):
    """보낸 메시지 다섯 줄을 낱말 칸으로. hot_words={(줄, 칸)}, hot_rows=줄 번호(0부터)."""
    for r, m in enumerate(MSGS):
        y = y0 - r * dy
        label(ax, x0 - 0.3, y + 0.25, str(r + 1), fs=10, color=RED if r in hot_rows else INK, bold=r in hot_rows)
        for k, wd in enumerate(m):
            cell(ax, x0 + k * (w + 0.06), y, w, 0.5, wd, hot=(r, k) in hot_words or r in hot_rows, fs=10.5)


def table_row(ax, x, y, front, items, hot=False, fw=1.05, iw=1.2, gap=0.12, hot_items=()):
    cell(ax, x, y, fw, 0.46, front, fs=10.5)
    arrow(ax, (x + fw + 0.05, y + 0.23), (x + fw + 0.42, y + 0.23), color=GREY, ms=9, lw=1.2)
    for k, (wd, n) in enumerate(items):
        cell(ax, x + fw + 0.5 + k * (iw + gap), y, iw, 0.46, f"{wd} {n}", hot=hot or k in hot_items, fs=10)


def tally(ax, step):
    label(ax, 0.3, 6.95, "보낸 메시지", fs=11.5, ha="left", bold=True)
    label(ax, TX, 6.95, "횟수표 (앞 낱말 → 다음 낱말 횟수)", fs=11.5, ha="left", bold=True)
    hot_words = {(0, 1), (1, 1), (3, 1)} if step == 1 else set()
    msg_rows(ax, hot_words)
    for k, (front, items) in enumerate(TABLE):
        y = TY0 - k * TDY
        if step == 1 and front != "오늘":
            cell(ax, TX, y, 1.05, 0.46, front, fs=10.5)
            empty(ax, TX + 1.55, y, 3.84, 0.46)
            continue
        table_row(ax, TX, y, front, items, hot=(step == 1) == (front == "오늘"))
    label(ax, TX, TY0 - 8 * TDY + 0.23, ENDS, fs=10, ha="left", color=RED if step == 2 else GREY)
    if step == 1:
        label(ax, 2.6, 2.5, "\"오늘\" 바로 다음 낱말을 세요", fs=11, color=RED)
    else:
        moral(ax, 6.0, 0.75, "앞 낱말마다 다음에 온 낱말을 셌어요")


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
    label(ax, 0.3, 6.2, "(처음) 줄에서 첫 낱말 고르기", fs=11.5, ha="left", bold=True)
    table_row(ax, 0.5, 5.0, "(처음)", TABLE[0][1], hot_items=(0,) if step == 1 else ())
    if step == 1:
        label(ax, 5.9, 4.35, "늘 1등만 고르면 언제나 \"오늘\"", fs=11, color=RED, bold=True)
        return
    label(ax, 0.5, 3.75, "횟수만큼 제비를 넣은 통", fs=10.5, ha="left", color=INK)
    end = ticket_box(ax, 0.5, 2.35, TICKETS, hot=step == 2, taken=3 if step == 3 else None)
    if step == 2:
        label(ax, 0.5 + (end - 0.5) / 2, 1.85, "오늘 3장, 내일 1장, 날씨 1장", fs=10.5, color=RED)
    else:
        arrow(ax, (end + 0.1, 2.9), (end + 1.3, 2.9), color=RED, ms=14)
        cell(ax, end + 1.45, 2.6, 1.15, 0.6, "내일", hot=True, fs=12)
        label(ax, 0.5 + (end - 0.5) / 2, 1.85, "5번 뽑으면 3번쯤은 오늘, 2번쯤은 다른 낱말", fs=10.5, color=INK)
        moral(ax, 6.0, 0.9, "많이 나온 낱말일수록 자주 뽑혀요")


# ── 이어 붙이기와 엉킴: 같은 무대 ─────────────────────────────────
OX, OY, OW = 0.5, 5.0, 1.15


def chain_stage(ax, out, hot_out, front, tickets, pick, dim_out=(), note=None, end_moral=None):
    label(ax, 0.3, 6.2, "뽑은 문장", fs=11.5, ha="left", bold=True)
    for k, wd in enumerate(out):
        cell(ax, OX + k * (OW + 0.1), OY, OW, 0.6, wd, hot=k == hot_out, dim=k in dim_out, fs=12)
    label(ax, 0.3, 4.05, "앞 낱말", fs=10.5, ha="left", color=INK)
    cell(ax, 0.5, 2.9, 1.15, 0.6, front, fs=12)
    arrow(ax, (1.75, 3.2), (2.35, 3.2), color=GREY, ms=11, lw=1.3)
    label(ax, 2.5, 2.35, "그 줄의 제비", fs=10.5, ha="left", color=INK)
    end = ticket_box(ax, 2.45, 2.65, tickets)
    k = pick
    px = 2.45 + 0.25 + k * 1.2
    cell(ax, px, 2.9, 1.05, 0.55, tickets[k], hot=True, fs=11)
    tx = OX + hot_out * (OW + 0.1) + OW / 2
    arrow(ax, (px + 0.52, 3.55), (tx, OY - 0.08), color=RED, ms=13, rad=0.0)
    if note:
        label(ax, 6.0, 1.75, note[0], fs=11, color=note[1], bold=note[1] == RED)
    if end_moral:
        moral(ax, 6.0, 1.0, end_moral)
    return end


CHAIN = [(["내일", "점심"], 1, "내일", ["점심"], 0),
         (["내일", "점심", "뭐"], 2, "점심", ["뭐", "같이"], 0),
         (["내일", "점심", "뭐", "먹지"], 3, "뭐", ["먹지", "먹을까", "이래"], 0),
         (["내일", "점심", "뭐", "먹지", "(끝)"], 4, "먹지", ["(끝)"], 0)]


def chain(ax, step):
    out, h, front, tk, pick = CHAIN[step - 1]
    m = "보낸 적 없는 문장이 나왔어요" if step == 4 else None
    chain_stage(ax, out, h, front, tk, pick, end_moral=m)


def tangle(ax, step):
    out = ["내일", "점심", "뭐", "이래"]
    if step == 1:
        chain_stage(ax, out, 3, "뭐", ["먹지", "먹을까", "이래"], 2)
    else:
        chain_stage(ax, out, 3, "뭐", ["먹지", "먹을까", "이래"], 2, dim_out=(0, 1),
                    note=("\"뭐\" 하나만 보고 골랐어요. \"점심\"은 안 봤어요", RED),
                    end_moral="앞쪽을 잊어서 문장이 엉켜요")


# ── 앞 낱말 둘 ─────────────────────────────────────────────────────
TWO = [("점심 뭐", "먹지"), ("날씨 뭐", "이래"), ("저녁 뭐", "먹을까")]


def two(ax, step):
    label(ax, 0.3, 6.2, "앞 낱말 1개", fs=11.5, ha="left", bold=True)
    table_row(ax, 0.5, 5.25, "뭐", TABLE[7][1])
    label(ax, 6.6, 5.48, "\"뭐\" 다음이 셋으로 갈려요", fs=10.5, ha="left", color=INK)
    if step == 1:
        return
    hot = step == 2
    label(ax, 0.3, 4.4, "앞 낱말 2개", fs=11.5, ha="left", bold=True, color=RED if hot else "#222")
    for k, (front, nxt) in enumerate(TWO):
        y = 3.55 - k * 0.62
        cell(ax, 0.5, y, 1.8, 0.46, front, fs=10.5, hot=hot)
        arrow(ax, (2.35, y + 0.23), (2.75, y + 0.23), color=GREY, ms=9, lw=1.2)
        cell(ax, 2.85, y, 1.4, 0.46, f"{nxt} 1", fs=10, hot=hot)
    if step == 2:
        moral(ax, 6.0, 1.0, "앞 낱말 둘을 보면 \"뭐\" 다음이 하나로 정해져요")
    else:
        y = 3.55 - 0.62
        ax.add_patch(Rectangle((0.38, y - 0.1), 4.0, 0.66, fill=False, ec=RED, lw=2.0))
        label(ax, 4.55, y + 0.23, "날씨 뭐 이래 = 낱말 3개 묶음 = 3-그램", fs=11, ha="left", color=RED, bold=True)
        label(ax, 0.3, 1.0, "앞 낱말 1개를 보는 표는 낱말 2개 묶음(2-그램)을 센 표예요", fs=10.5, ha="left", color=INK)


# ── 전환: 늘린 대신 치르는 값 ─────────────────────────────────────
def turn(ax, step):
    if step == 1:
        phone(ax, "오늘 저녁", ["뭐"])
        program(ax, "언어 모델", ["앞 낱말 2개 표"])
        bubble(ax, *SAY, "앞 낱말 둘을 보니\n엉킨 문장이 사라졌어요", TAIL)
        return
    phone(ax, "오늘 저녁", ["뭐"], sugg_dim=True)
    program(ax, "언어 모델", ["앞 낱말 2개 표"])
    bubble(ax, 6.3, 0.35, 5.5, 2.2, "", TAIL, hot=True)
    label(ax, 9.05, 2.1, "대신 치르는 값이 있어요", fs=11.5, color=RED, bold=True)
    for k, t in enumerate(["① 처음 보는 묶음에서 막혀요", "② 보낸 문장만 베껴요"]):
        label(ax, 6.6, 1.45 - k * 0.6, t, fs=10.5, ha="left", color=RED)


# ── 첫째 값: 막힘 ──────────────────────────────────────────────────
def stuck(ax, step):
    if step == 1:
        phone(ax, "내일 저녁", None, typed_hot=True)
        program(ax, "언어 모델", ["표에서 내일로 시작하는 줄", "내일 점심 → 같이 1"])
        bubble(ax, *SAY, "\"내일 저녁\" 줄을\n찾아요", TAIL)
    else:
        phone(ax, "내일 저녁", [])
        program(ax, "언어 모델", ["표에서 내일로 시작하는 줄", "내일 점심 → 같이 1"])
        bubble(ax, *SAY, "\"내일 저녁\" 줄이\n표에 없어요", TAIL, hot=True)
        moral(ax, 6.0, 0.4, "처음 보는 묶음 앞에서는 아무것도 못 띄워요")


# ── 실측: 처음 보는 묶음 ───────────────────────────────────────────
UNSEEN = [(1, 136), (2, 596), (3, 713), (4, 735)]


def unseen(ax, step):
    label(ax, 0.3, 6.2, "시험 글의 앞 묶음 1,000개 가운데 표에 없던 것", fs=11.5, ha="left", bold=True)
    label(ax, 0.3, 5.6, "한 칸 = 100개, 빨강 = 처음 본 묶음", fs=10, ha="left", color=INK)
    for k, (n, v) in enumerate(UNSEEN):
        y = 4.6 - k * 0.9
        if step == 1 and n > 2:
            continue
        hot = (step == 1 and n == 2) or (step == 2 and n > 2)
        label(ax, 0.3, y + 0.28, f"앞 낱말 {n}개", fs=10.5, ha="left", color=RED if hot else "#222", bold=hot)
        for i in range(10):
            x = 2.1 + i * 0.62
            ax.add_patch(Rectangle((x, y), 0.56, 0.56, fc="white", ec=INK, lw=1.0))
            fill = min(max(v / 100 - i, 0), 1)
            if fill > 0:
                ax.add_patch(Rectangle((x, y), 0.56 * fill, 0.56, fc=RED if hot else PINK, ec="none"))
        label(ax, 8.5, y + 0.28, f"{v}개", fs=11, ha="left", color=RED if hot else "#222", bold=hot)
    if step == 2:
        moral(ax, 6.0, 0.75, "앞 낱말을 늘릴수록 처음 보는 묶음이 많아졌어요")


# ── 실측: 글을 늘리면 (앞 낱말 2개, 같은 시험 글) ──────────────────
MORE = [("5,477개", 775), ("13,598개", 713), ("27,247개", 658), ("54,055개", 596)]


def bars(ax, y, name, v, hot, x0=2.6):
    label(ax, 0.3, y + 0.28, name, fs=10.5, ha="left", color=RED if hot else "#222", bold=hot)
    for i in range(10):
        x = x0 + i * 0.62
        ax.add_patch(Rectangle((x, y), 0.56, 0.56, fc="white", ec=INK, lw=1.0))
        fill = min(max(v / 100 - i, 0), 1)
        if fill > 0:
            ax.add_patch(Rectangle((x, y), 0.56 * fill, 0.56, fc=RED if hot else PINK, ec="none"))
    label(ax, x0 + 6.4, y + 0.28, f"{v}개", fs=11, ha="left", color=RED if hot else "#222", bold=hot)


def more(ax, step):
    label(ax, 0.3, 6.2, "앞 낱말 2개 · 배운 글의 낱말 수를 바꿔 가며", fs=11.5, ha="left", bold=True)
    label(ax, 0.3, 5.6, "시험 글의 앞 묶음 1,000개 가운데 표에 없던 것 (한 칸 = 100개)", fs=10, ha="left", color=INK)
    for k, (name, v) in enumerate(MORE):
        if step == 1 and k > 0:
            continue
        hot = (k == 0) if step == 1 else k > 0
        bars(ax, 4.6 - k * 0.9, "낱말 " + name, v, hot)
    if step == 2:
        moral(ax, 6.0, 0.75, "글을 두 배쯤 늘려도 60개쯤씩만 줄어요")


# ── 앞 낱말 2개 표 전체 ────────────────────────────────────────────
ST = "(처음)"
TABLE2 = [((ST, ST), [("오늘", 3), ("내일", 1), ("날씨", 1)]), ((ST, "오늘"), [("점심", 1), ("날씨", 1), ("저녁", 1)]),
          ((ST, "내일"), [("점심", 1)]), ((ST, "날씨"), [("뭐", 1)]), (("오늘", "점심"), [("뭐", 1)]),
          (("오늘", "날씨"), [("좋다", 1)]), (("오늘", "저녁"), [("뭐", 1)]), (("내일", "점심"), [("같이", 1)]),
          (("날씨", "뭐"), [("이래", 1)]), (("점심", "뭐"), [("먹지", 1)]), (("점심", "같이"), [("먹자", 1)]),
          (("저녁", "뭐"), [("먹을까", 1)]), (("뭐", "먹지"), [("(끝)", 1)]), (("날씨", "좋다"), [("(끝)", 1)]),
          (("같이", "먹자"), [("(끝)", 1)]), (("뭐", "먹을까"), [("(끝)", 1)]), (("뭐", "이래"), [("(끝)", 1)])]
PATH = {(ST, ST): ("①", "오늘"), (ST, "오늘"): ("②", "저녁"), ("오늘", "저녁"): ("③", "뭐"),
        ("저녁", "뭐"): ("④", "먹을까"), ("뭐", "먹을까"): ("⑤", "(끝)")}


def table2(ax, step):
    label(ax, 0.3, 7.0, "앞 낱말 2개 표 (앞 낱말 둘 → 다음 낱말 횟수)", fs=11.5, ha="left", bold=True)
    for k, (front, items) in enumerate(TABLE2):
        col, row = (0, k) if k < 9 else (1, k - 9)
        x, y = (0.6 if col == 0 else 6.7), 6.2 - row * 0.56
        on = step == 2 and front in PATH
        if on:
            label(ax, x - 0.3, y + 0.23, PATH[front][0], fs=10.5, color=RED, bold=True)
        cell(ax, x, y, 2.0, 0.46, " ".join(front), hot=on, fs=10)
        arrow(ax, (x + 2.05, y + 0.23), (x + 2.4, y + 0.23), color=GREY, ms=9, lw=1.2)
        for j, (wd, n) in enumerate(items):
            pick = on and PATH[front][1] == wd
            cell(ax, x + 2.5 + j * 1.15, y, 1.05, 0.46, f"{wd} {n}", hot=pick, fs=9.5)
    if step == 2:
        moral(ax, 6.0, 0.8, "① ~ ⑤를 따라가면 4번 메시지 \"오늘 저녁 뭐 먹을까\"예요")


# ── 둘째 값: 베낌 ──────────────────────────────────────────────────
def copy(ax, step):
    label(ax, 0.3, 6.2, "보낸 메시지", fs=11.5, ha="left", bold=True)
    label(ax, 5.6, 6.2, "앞 낱말 2개 표로 뽑은 문장", fs=11.5, ha="left", bold=True)
    rows = {1: (3,), 2: (2,)}[step]
    msg_rows(ax, hot_rows=rows, y0=5.3, dy=0.75)
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


# ── 언제 쓸모 있을까: 갈림길 ───────────────────────────────────────
def decide():
    fig, ax = canvas(9.4, 3.6, 14, 5.4)
    box(ax, 0.3, 3.3, 5.0, 1.5, fc=NOTE)
    label(ax, 2.8, 4.05, "앞의 한두 낱말만 보고\n맞혀도 되나요?", fs=11.5, bold=True)
    arrow(ax, (5.4, 4.05), (6.9, 4.05), color=RED)
    label(ax, 6.15, 4.4, "예", fs=10.5, color=RED)
    box(ax, 7.0, 3.1, 6.7, 1.9, fc=PINK, ec=RED)
    label(ax, 10.35, 4.05, "세기 모델을 쓸 수 있어요\n검색어 추천, 어느 나라 말인지\n알아맞히기, 맞춤법 후보 고르기", fs=10.5, color=RED)
    arrow(ax, (2.8, 3.2), (2.8, 2.0))
    label(ax, 3.05, 2.6, "아니요", fs=10.5, color=INK, ha="left")
    box(ax, 0.3, 0.5, 5.0, 1.4, fc=LIGHT, ec=GREY)
    label(ax, 2.8, 1.2, "더 앞을 보고 처음 보는\n묶음도 다뤄야 해요", fs=10.5)
    arrow(ax, (5.4, 1.2), (6.9, 1.2))
    box(ax, 7.0, 0.5, 6.7, 1.4, fc=LIGHT, ec=GREY)
    label(ax, 10.35, 1.2, "세기 대신 다른 방법이 필요해요\n(이어지는 편들)", fs=10.5)
    save(fig, OUT, "ai01-decide.svg")


# ── 정리: 처음 장면으로 돌아가기 ───────────────────────────────────
def back(ax, step):
    if step == 1:
        phone(ax, "오늘", None)
        program(ax, "언어 모델")
        bubble(ax, *SAY, "처음엔 이 셋을 왜 골랐는지\n몰랐어요", TAIL)
    elif step == 2:
        phone(ax, "오늘", None)
        program(ax, "언어 모델", ["횟수표 \"오늘\" 줄", "점심 1 · 날씨 1 · 저녁 1"], hot=True)
        bubble(ax, *SAY, "\"오늘\" 줄을 펼쳐요", TAIL, hot=True)
    else:
        phone(ax, "오늘", ["점심", "날씨", "저녁"], sugg_hot=True)
        program(ax, "언어 모델", ["횟수표 \"오늘\" 줄", "점심 1 · 날씨 1 · 저녁 1"])
        bubble(ax, *SAY, "그 줄의 낱말을 띄워요", TAIL)
        moral(ax, 6.0, 0.4, "\"오늘\" 다음에 왔던 낱말을 세어서 띄웠어요")


# ── 정리: 낱말 카드 ────────────────────────────────────────────────
def cards():
    """이 편 본문에서 이름 붙인 말 셋. 카드마다 본문 그림을 작게 다시 그리고 한 줄 뜻."""
    fig, ax = canvas(6.4, 6.3, 9.8, 9.6)
    W, H = 9.4, 2.9

    def card(i, name, line):
        x, y = 0.2, 6.5 - i * 3.15
        box(ax, x, y, W, H, fc="white")
        label(ax, x + 0.3, y + H - 0.45, name, fs=12.5, ha="left", bold=True)
        label(ax, x + 6.9, y + 1.1, line, fs=10, color=INK)
        return x, y

    x, y = card(0, "언어 모델", "앞 낱말을 보고\n다음 낱말을 맞히는 프로그램")
    cylinder(ax, x + 0.5, y + 0.55, 1.6, 0.8, "")
    bubble(ax, x + 2.5, y + 1.45, 1.9, 0.7, "점심?", (x + 2.1, y + 1.0), hot=True, fs=10.5)
    x, y = card(1, "말뭉치", "맞히는 재료로\n모아 둔 글")
    for k, s in enumerate(["오늘 점심 뭐 먹지", "오늘 날씨 좋다", "⋮"]):
        if s == "⋮":
            label(ax, x + 2.3, y + 0.45, s, fs=11, color=INK)
            continue
        cell(ax, x + 0.5, y + 1.55 - k * 0.6, 3.6, 0.48, s, hot=k == 0, fs=10)
    x, y = card(2, "n-그램", "낱말 n개가\n이어진 묶음")
    for k, s in enumerate(["날씨", "뭐", "이래"]):
        cell(ax, x + 0.5 + k * 1.15, y + 0.8, 1.05, 0.5, s, hot=True, fs=10.5)
    ax.plot([x + 0.5, x + 0.5, x + 3.85, x + 3.85], [y + 1.35, y + 1.45, y + 1.45, y + 1.35], color=RED, lw=1.6)
    label(ax, x + 2.2, y + 1.7, "3-그램", fs=10.5, color=RED, bold=True)
    save(fig, OUT, "ai01-cards.svg")


if __name__ == "__main__":
    S, L = (7.2, 3.8), (12, 6.6)
    stage(opening, 2, OUT, "ai01-open", S, L)
    stage(tally, 2, OUT, "ai01-tally", (7.2, 4.3), (12, 7.4))
    stage(draw, 3, OUT, "ai01-draw", S, L)
    stage(chain, 4, OUT, "ai01-chain", S, L)
    stage(tangle, 2, OUT, "ai01-tangle", S, L)
    stage(two, 3, OUT, "ai01-two", S, L)
    stage(turn, 2, OUT, "ai01-turn", S, L)
    stage(stuck, 2, OUT, "ai01-stuck", S, L)
    stage(unseen, 2, OUT, "ai01-unseen", S, L)
    stage(more, 2, OUT, "ai01-more", S, L)
    stage(table2, 2, OUT, "ai01-table2", (7.2, 4.3), (12, 7.4))
    stage(copy, 2, OUT, "ai01-copy", S, L)
    decide()
    stage(back, 3, OUT, "ai01-back", S, L)
    cards()
