"""Elasticsearch 14편 그림 만들기. 실행: python lab/fig_es14.py  → docs/elasticsearch/img/14/*.svg

본문 절은 장면 띠로 그린다: 같은 무대를 여러 장 그리고 장마다 바뀐 곳만 빨강으로 칠한다.
예시는 주문 인덱스(샤드 1개, 복사본 3개)와 노드 es01·es02·es03을 편 끝까지 잇는다(.claude/writing/work/cal/units-es14.md).
처음 주 샤드·마스터는 es03. es03이 꺼지면 es02가 주 샤드, es01이 마스터.
설명용 쓰기 10건(시퀀스 번호 0~9): es03 0~9, es02 0~7·9, es01 0~5 → 로컬 체크포인트 9·7·5, 글로벌 5.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "es"))
from figkit import (GREY, INK, LIGHT, NOTE, PAPER, PINK, RED, arrow, box, bubble,  # noqa: E402
                    canvas, cell, cells, cylinder, label, moral, outdir, save, stage)
from matplotlib.patches import Rectangle  # noqa: E402

OUT = outdir("14")
NAMES = ["es01", "es02", "es03"]


def empty(ax, x, y, w, h, s="", fs=10, ec=GREY, lw=1.0):
    ax.add_patch(Rectangle((x, y), w, h, fc="white", ec=ec, lw=lw, ls="--"))
    if s:
        label(ax, x + w / 2, y + h / 2, s, fs=fs, color=GREY)


def cross(ax, x, y, w, h, color=RED, lw=2.4):
    ax.plot([x, x + w], [y, y + h], color=color, lw=lw)
    ax.plot([x, x + w], [y + h, y], color=color, lw=lw)


def strike(ax, x, y, w, h, color=GREY, lw=1.6):
    ax.plot([x, x + w], [y + h / 2, y + h / 2], color=color, lw=lw)


# ── 여는 장면과 돌아오는 장면: 주문 관리 화면 + 노드 원통 셋 ─────────
CX = [6.15, 8.05, 9.95]
CW, CY, CH = 1.6, 3.3, 1.5
SAY = (6.0, 0.35, 5.75, 1.45)


def screen(ax, found, saved):
    """주문 관리 화면. found/saved=(글, 모양 'hot'|'dim'|'') 또는 None(빈 답 칸)."""
    box(ax, 0.3, 1.3, 5.4, 4.95, fc="white", round_=False)
    ax.add_patch(Rectangle((0.3, 5.8), 5.4, 0.45, fc=LIGHT, ec=INK, lw=1.2))
    label(ax, 0.5, 6.02, "쇼핑몰 주문 관리", fs=11, ha="left", color=INK)
    for y, ask, btn, ans in ((4.85, "주문 검색", "검색", found), (3.0, "새 주문", "저장", saved)):
        ax.add_patch(Rectangle((0.55, y), 3.6, 0.55, fc="white", ec=INK, lw=1.2))
        label(ax, 0.7, y + 0.27, ask, fs=11, ha="left")
        ax.add_patch(Rectangle((4.25, y), 1.2, 0.55, fc=LIGHT, ec=INK, lw=1.2))
        label(ax, 4.85, y + 0.27, btn, fs=10.5)
        if ans is None:
            empty(ax, 0.55, y - 0.8, 4.9, 0.6)
            continue
        s, mode = ans
        hot, dim = mode == "hot", mode == "dim"
        ax.add_patch(Rectangle((0.55, y - 0.8), 4.9, 0.6, fc=PINK if hot else ("white" if dim else NOTE),
                               ec=RED if hot else (GREY if dim else INK), lw=1.8 if hot else 1.1))
        label(ax, 0.7, y - 0.5, s, fs=10.5, ha="left", color=RED if hot else (GREY if dim else "#222"), bold=hot)


def drum(ax, i, role, off=False, hot_off=False, hot_role=False, master=False, hot_master=False):
    """노드 원통 하나. role=안에 든 복사본 이름, master=위에 마스터 꼬리표."""
    x = CX[i]
    if off:
        cylinder(ax, x, CY, CW, CH, NAMES[i], fc=LIGHT, ec=GREY, color=RED if hot_off else GREY)
        cell(ax, x + 0.15, CY + 0.45, CW - 0.3, 0.6, role, dim=True, fs=9.5)
        cross(ax, x + 0.1, CY + 0.1, CW - 0.2, CH - 0.1, color=RED if hot_off else GREY)
        label(ax, x + CW / 2, CY - 0.45, "꺼짐", fs=10.5, color=RED if hot_off else GREY, bold=hot_off)
    else:
        cylinder(ax, x, CY, CW, CH, NAMES[i])
        cell(ax, x + 0.15, CY + 0.45, CW - 0.3, 0.6, role, hot=hot_role, fs=9.5)
    if master:
        ax.add_patch(Rectangle((x + 0.25, 5.75), CW - 0.5, 0.45, fc=PINK if hot_master else PAPER,
                               ec=RED if hot_master else INK, lw=1.6 if hot_master else 1.1))
        label(ax, x + CW / 2, 5.97, "마스터", fs=10, color=RED if hot_master else "#222", bold=hot_master)


def tail(i):
    return (CX[i] + CW / 2, CY - 0.25)


F152 = "주문 152건"


def opening(ax, step):
    if step == 1:
        screen(ax, (F152, ""), None)
        drum(ax, 0, "복제본")
        drum(ax, 1, "복제본")
        drum(ax, 2, "주 샤드", master=True)
        bubble(ax, *SAY, "주 샤드와 마스터를\n제가 맡았어요", tail(2), fs=11)
    elif step == 2:
        screen(ax, (F152, "dim"), None)
        drum(ax, 0, "복제본")
        drum(ax, 1, "복제본")
        drum(ax, 2, "주 샤드", off=True, hot_off=True)
        label(ax, 8.85, 1.6, "es03을 강제로 껐어요", fs=11.5, color=RED, bold=True)
    elif step == 3:
        screen(ax, (F152, "dim"), None)
        drum(ax, 0, "복제본", master=True, hot_master=True)
        drum(ax, 1, "주 샤드", hot_role=True)
        drum(ax, 2, "주 샤드", off=True)
        bubble(ax, *SAY, "5초 뒤 제가 주 샤드를\n넘겨받았어요", tail(1), hot=True, fs=11)
    else:
        screen(ax, ("주문 152건 그대로", "hot"), ("✓ 새 주문 50건 저장됐어요", "hot"))
        drum(ax, 0, "복제본", master=True)
        drum(ax, 1, "주 샤드")
        drum(ax, 2, "주 샤드", off=True)
        moral(ax, 6.0, 0.6, "노드가 꺼져도 검색도 저장도 됐어요")


def back(ax, step):
    screen(ax, ("주문 152건 그대로", "dim"), ("✓ 새 주문 50건 저장됐어요", "dim"))
    drum(ax, 0, "복제본", master=True)
    if step == 1:
        drum(ax, 1, "주 샤드")
        drum(ax, 2, "주 샤드", off=True)
        bubble(ax, *SAY, "es03이 꺼지자 5초 만에\n제가 넘겨받았어요", tail(1), fs=11)
    elif step == 2:
        drum(ax, 1, "주 샤드")
        drum(ax, 2, "주 샤드", off=True)
        bubble(ax, *SAY, "152건을 다 받은\nin-sync 복제본이었어요", tail(1), hot=True, fs=11)
    else:
        drum(ax, 1, "주 샤드")
        drum(ax, 2, "복제본", hot_role=True)
        bubble(ax, *SAY, "다시 켜져서 작업 기록을\n받아 따라잡았어요", tail(2), hot=True, fs=11)
        moral(ax, 3.0, 0.6, "복사본이 있어 문서가 그대로예요", fs=11.5)


# ── 본문 무대: 노드 상자 셋 ───────────────────────────────────────
NBX = [0.3, 4.2, 8.1]
NBW, NBY, NBH = 3.5, 1.25, 1.75


def node(ax, i, role, hot=False, off=False, hot_off=False, note=""):
    x = NBX[i]
    if off:
        box(ax, x, NBY, NBW, NBH, fc=LIGHT, ec=RED if hot_off else GREY, lw=2.0 if hot_off else 1.4)
        label(ax, x + 0.2, NBY + NBH - 0.3, NAMES[i], fs=11, ha="left", bold=True, color=RED if hot_off else GREY)
        label(ax, x + NBW - 0.2, NBY + NBH - 0.3, "꺼짐", fs=10.5, ha="right", color=RED if hot_off else GREY,
              bold=hot_off)
        cell(ax, x + 0.6, NBY + 0.3, 2.3, 0.65, role, dim=True, fs=10.5)
        cross(ax, x + 0.6, NBY + 0.3, 2.3, 0.65, color=RED if hot_off else GREY, lw=2.0)
        return
    box(ax, x, NBY, NBW, NBH, fc=NOTE)
    label(ax, x + 0.2, NBY + NBH - 0.3, NAMES[i], fs=11, ha="left", bold=True)
    if note:
        label(ax, x + NBW - 0.2, NBY + NBH - 0.3, note, fs=10.5, ha="right", color=RED if hot else INK, bold=hot)
    cell(ax, x + 0.6, NBY + 0.3, 2.3, 0.65, role, hot=hot, fs=10.5)


def top(i):
    return NBX[i] + NBW / 2, NBY + NBH + 0.05


# ── 같은 샤드를 여러 노드에 ────────────────────────────────────────
CLIENT = (8.1, 5.35, 3.5, 0.75)


def copies(ax, step):
    hot1 = step == 1
    node(ax, 0, "복제본", hot=hot1)
    node(ax, 1, "복제본", hot=hot1)
    node(ax, 2, "주 샤드", hot=hot1)
    if step == 1:
        label(ax, 0.3, 6.0, "number_of_replicas: 2", fs=11.5, ha="left", bold=True)
        label(ax, 0.3, 5.35, "같은 샤드의 복사본 3개를 노드마다 하나씩", fs=11, ha="left", color=RED)
        label(ax, 6.0, 0.6, "같은 샤드의 복사본 둘이 한 노드에 놓이는 일은 없어요", fs=11, color=INK)
        return
    w2, w3 = step == 2, step == 3
    box(ax, *CLIENT, fc=PAPER)
    label(ax, CLIENT[0] + CLIENT[2] / 2, CLIENT[1] + CLIENT[3] / 2, "새 주문 저장", fs=11)
    c2 = RED if w2 else GREY
    arrow(ax, (9.2, 5.3), (9.2, 3.1), color=c2, ms=14)
    label(ax, 9.05, 4.2, "①", fs=12, ha="right", color=c2, bold=w2)
    sx, sy = 8.6, 3.1
    arrow(ax, (sx, sy), (top(1)[0] + 0.4, sy), color=c2, ms=14, rad=0.5)
    arrow(ax, (sx, sy), (top(0)[0], sy), color=c2, ms=14, rad=0.38)
    label(ax, 5.6, 5.0, "② 복제본 둘에 동시에", fs=11, color=c2, bold=w2)
    if step == 2:
        return
    c3 = RED if w3 else GREY
    arrow(ax, (10.7, 3.1), (10.7, 5.3), color=c3, ms=14)
    label(ax, 10.85, 4.2, "③", fs=12, ha="left", color=c3, bold=w3)
    if step == 3:
        label(ax, 7.9, 6.25, "③ 성공: total 3, successful 3", fs=11, ha="right", color=RED, bold=True)
        return
    if step == 4:
        label(ax, 7.9, 6.25, "③ 성공 (세 곳 모두)", fs=10.5, ha="right", color=GREY)
        box(ax, 0.3, 5.35, 3.0, 0.75, fc=PINK, ec=RED)
        label(ax, 1.8, 5.72, "주문 검색", fs=11, color=RED, bold=True)
        arrow(ax, (1.2, 5.3), (1.2, 3.1), color=RED, ms=14)
        label(ax, 1.4, 4.2, "복사본 하나에", fs=10.5, ha="left", color=RED)
        moral(ax, 6.0, 0.55, "쓰기는 주 샤드가 먼저, 검색은 아무 복사본에서나", fs=11.5)


# ── 시퀀스 번호와 체크포인트: 번호 칸 줄 셋 ─────────────────────────
ROWY = {2: 4.45, 1: 3.35, 0: 2.25}
RX0, RW, RG, RH = 2.95, 0.6, 0.08, 0.7
LCPX = 10.6


def rx(k):
    return RX0 + k * (RW + RG)


def rowname(ax, i, role, color="#222", bold=False):
    label(ax, 0.3, ROWY[i] + RH / 2, f"{NAMES[i]} · {role}", fs=10.5, ha="left", color=color, bold=bold)


def row(ax, i, got, hot=(), dim=False, hot_gap=(), text=None):
    """번호 칸 열 개. got=받은 번호, text={번호: 칸 글자}."""
    y = ROWY[i]
    text = text or {}
    for k in range(10):
        if k in got:
            cell(ax, rx(k), y, RW, RH, text.get(k, str(k)), hot=k in hot, dim=dim, fs=10.5,
                 fc=None if (k in hot or dim) else "white")
        else:
            empty(ax, rx(k), y, RW, RH, ec=RED if k in hot_gap else GREY, lw=1.8 if k in hot_gap else 1.0)


def lcp(ax, i, v, hot=False, dim=False):
    label(ax, LCPX, ROWY[i] + RH / 2, str(v), fs=12.5, color=RED if hot else (GREY if dim else "#222"), bold=hot)


def seq(ax, step):
    label(ax, 0.3, 6.15, "새 주문 하나를 저장하면", fs=11, ha="left", color=INK)
    items = ["0", "1", "2", "⋯", "99"]
    for i, role in ((2, "주 샤드"), (1, "복제본"), (0, "복제본")):
        rowname(ax, i, role)
        for k, t in enumerate(items):
            cell(ax, rx(k), ROWY[i], RW, RH, t, fs=10.5, fc="white")
        nx = rx(5)
        if i == 2:
            cell(ax, nx, ROWY[i], RW + 0.25, RH, "100", hot=(step == 1), fs=10.5, fc=None if step == 1 else "white")
        elif step == 1:
            empty(ax, nx, ROWY[i], RW + 0.25, RH)
        else:
            cell(ax, nx, ROWY[i], RW + 0.25, RH, "100", hot=True, fs=10.5)
    if step == 1:
        label(ax, rx(6) + 0.4, ROWY[2] + RH / 2, "주 샤드가 100번을 매겨요", fs=11, ha="left", color=RED, bold=True)
        label(ax, 6.0, 1.3, "쓰기 응답에도 _seq_no: 100이 나와요", fs=10.5, color=INK)
        return
    label(ax, rx(6) + 0.4, ROWY[2] + RH / 2, "주 샤드가 100번을 매겨요", fs=11, ha="left", color=INK)
    label(ax, rx(6) + 0.4, (ROWY[1] + ROWY[0] + RH) / 2, "복제본은 같은 번호로\n받아 적어요", fs=11, ha="left",
          color=RED, bold=True)
    moral(ax, 6.0, 1.0, "번호는 주 샤드만 매겨요")


GOT = {2: set(range(10)), 1: {0, 1, 2, 3, 4, 5, 6, 7, 9}, 0: set(range(6))}
GCPX = rx(6) - RG / 2


def ledger(ax, step):
    """1~2 로컬 체크포인트, 3~5 글로벌 체크포인트, 6~8 새 주 샤드가 번호를 맞춤."""
    label(ax, 0.3, 6.2, "쓰기 10건 (시퀀스 번호 0~9)", fs=11, ha="left", color=INK)
    if step >= 2:
        label(ax, LCPX, 5.65, "로컬\n체크포인트", fs=10, color=INK)
    fix = step >= 6
    # es03
    rowname(ax, 2, "꺼짐" if fix else "주 샤드", color=GREY if fix else "#222")
    row(ax, 2, GOT[2], dim=fix)
    if step >= 2:
        lcp(ax, 2, 9, dim=fix)
    # es02
    if fix:
        rowname(ax, 1, "새 주 샤드", color=RED if step == 6 else "#222", bold=step == 6)
    else:
        rowname(ax, 1, "복제본")
    got1 = GOT[1] | ({8} if step >= 7 else set())
    row(ax, 1, got1, hot_gap=(8,) if step == 1 else (), hot=(8,) if step == 7 else (), text={8: "빈"})
    if step >= 2:
        lcp(ax, 1, 9 if step >= 7 else 7, hot=step in (2, 7))
    if step == 1:
        label(ax, rx(8) + RW / 2, ROWY[1] - 0.3, "8은 아직", fs=10, color=RED)
        label(ax, 6.0, 1.3, "9가 8보다 먼저 닿았어요", fs=11, color=RED, bold=True)
        return
    if step == 2:
        y = ROWY[1] - 0.15
        ax.plot([rx(0), rx(7) + RW], [y, y], color=RED, lw=2.4)
        label(ax, (rx(0) + rx(7) + RW) / 2, y - 0.35, "0부터 빈틈없이 받은 곳", fs=10.5, color=RED)
        moral(ax, 6.0, 0.9, "es02의 로컬 체크포인트는 7이에요")
        return
    # es01
    rowname(ax, 0, "복제본")
    got0 = GOT[0] | (set(range(6, 10)) if step == 8 else set())
    row(ax, 0, got0, hot=(set(range(6)) if step == 3 else (set(range(6, 10)) if step == 8 else set())),
        text={8: "빈"})
    lcp(ax, 0, 9 if step == 8 else 5, hot=step in (3, 8))
    if step == 3:
        label(ax, 6.0, 1.3, "es01은 아직 5번까지만 받았어요", fs=11, color=INK)
        return
    lc = RED if step == 4 else INK
    ax.plot([GCPX, GCPX], [ROWY[0] - 0.25, ROWY[2] + RH + 0.25], color=lc, lw=2.4 if step == 4 else 1.8, ls="--")
    if step == 4:
        label(ax, 6.0, 1.3, "글로벌 체크포인트 5 = 9, 7, 5 가운데 가장 작은 값", fs=11, color=RED, bold=True)
        return
    if step == 5:
        lo, hi = ROWY[0] - 0.12, ROWY[2] + RH + 0.12
        ax.add_patch(Rectangle((rx(0) - 0.1, lo), GCPX - rx(0) + 0.05, hi - lo, fill=False, ec=RED, lw=2.0))
        label(ax, (rx(0) + GCPX) / 2, 1.5, "세 곳 모두 같아요", fs=10.5, color=RED, bold=True)
        label(ax, (GCPX + rx(9) + RW) / 2, 1.5, "여기만 다를 수 있어요", fs=10.5, color=INK)
        moral(ax, 6.0, 0.6, "글로벌 체크포인트 뒤쪽만 맞추면 돼요")
        return
    if step == 6:
        label(ax, 6.0, 1.3, "맞출 곳은 글로벌 체크포인트 5 뒤의 6~9번이에요", fs=11, color=INK)
    elif step == 7:
        label(ax, 6.0, 1.3, "8번 빈자리를 빈 작업으로 채워요", fs=11, color=RED, bold=True)
    else:
        arrow(ax, (rx(9) + RW + 0.08, ROWY[1] + 0.35), (rx(9) + RW + 0.08, ROWY[0] + 0.35), color=RED, ms=13,
              rad=-0.6)
        label(ax, 6.0, 1.45, "es02가 6~9번을 es01에 보내요", fs=11, color=RED)
        moral(ax, 6.0, 0.6, "0~5번은 다시 보내지 않아요")


# ── 주 샤드 교체: 노드 상자 셋 + 마스터가 적어 둔 것 ─────────────────
CARD = (6.3, 4.1, 5.4, 2.25)
ISX = [8.3, 9.4, 10.5]


def card(ax, master, out3=False, hot_out=False, back3=False, term="1", hot_term=False):
    x, y, w, h = CARD
    box(ax, x, y, w, h, fc=PAPER)
    label(ax, x + 0.2, y + h - 0.32, f"마스터 {master}가 적어 둔 것", fs=10.5, ha="left", bold=True)
    label(ax, x + 0.2, y + 1.15, "in-sync 목록", fs=10, ha="left", color=INK)
    for k, n in enumerate(NAMES):
        cx, cy = ISX[k], y + 0.9
        if k == 2 and out3:
            cell(ax, cx, cy, 1.0, 0.5, n, hot=hot_out, dim=not hot_out, fs=10)
            strike(ax, cx, cy, 1.0, 0.5, color=RED if hot_out else GREY, lw=1.3)
        else:
            cell(ax, cx, cy, 1.0, 0.5, n, hot=(k == 2 and back3), fs=10, fc=None if (k == 2 and back3) else "white")
    label(ax, x + 0.2, y + 0.4, "primary term", fs=10, ha="left", color=INK)
    cell(ax, ISX[0], y + 0.15, 1.0, 0.5, term, hot=hot_term, fs=11, fc=None if hot_term else "white")
    if hot_term:
        label(ax, ISX[1] - 0.05, y + 0.4, "(1 → 2)", fs=10, ha="left", color=RED)


def takeover(ax, step):
    """1~4 주 샤드가 바뀜, 5~6 돌아온 es03이 따라잡음."""
    note = {1: ("es03이 꺼졌어요. 새 마스터는 es01", False),
            2: ("es02를 주 샤드로 올리고 term도 올려요", True),
            3: ("꺼진 뒤 첫 쓰기를 es03이 못 받았어요", True),
            4: ("만약 es03이 네트워크만 끊겼다 돌아왔다면", False),
            5: ("es03을 다시 켰어요", True),
            6: ("es02가 그 뒤의 작업을 보내요", True)}[step]
    label(ax, 0.3, 5.95, note[0], fs=11, ha="left", color=RED if note[1] else INK, bold=note[1])
    node(ax, 0, "복제본")
    node(ax, 1, "주 샤드" if step >= 2 else "복제본", hot=(step == 2))
    if step <= 3:
        node(ax, 2, "주 샤드", off=True, hot_off=(step == 1))
    elif step == 4:
        node(ax, 2, "옛 주 샤드", note="term 1")
    else:
        node(ax, 2, "복제본", hot=(step == 5), note="다시 켬" if step == 5 else "")
    card(ax, "es01", out3=(step >= 3 and step != 6), hot_out=(step == 3), back3=(step == 6),
         term="2" if step >= 2 else "1", hot_term=(step == 2))
    if step == 2:
        arrow(ax, (CARD[0] + 0.3, CARD[1] - 0.05), (top(1)[0] + 0.6, top(1)[1]), color=RED, ms=14)
        label(ax, 3.9, 3.6, "in-sync 목록에서 골라요", fs=10.5, color=RED, ha="right")
    elif step == 3:
        label(ax, 0.3, 5.35, "그 쓰기 응답 _primary_term: 2", fs=10.5, ha="left", color=INK)
    elif step == 4:
        arrow(ax, (top(2)[0] - 0.4, top(2)[1]), (top(0)[0] + 0.5, top(0)[1]), color=RED, ms=14, rad=0.22)
        label(ax, 0.3, 5.35, "es03이 term 1로 복제본에 쓰기를 보내요", fs=10.5, ha="left", color=INK)
        label(ax, 1.9, 3.55, "✗ 거절", fs=12, ha="right", color=RED, bold=True)
        moral(ax, 6.0, 0.55, "주 샤드는 언제나 하나예요")
    elif step == 6:
        sx = top(1)[0] + 0.4
        arrow(ax, (sx, top(1)[1]), (top(2)[0] - 0.3, top(2)[1]), color=RED, ms=14, rad=-0.5)
        label(ax, 0.3, 5.35, "다 따라잡으면 in-sync 목록에 다시 들어가요", fs=10.5, ha="left", color=RED)
        moral(ax, 6.0, 0.55, "파일을 통째로 다시 받지 않아요")


# ── 마스터 없는 클러스터 (실험: 노드 3개 중 둘을 끔) ─────────────────
def nomaster(ax, step):
    node(ax, 0, "복제본")
    node(ax, 1, "주 샤드", off=True, hot_off=(step == 1))
    node(ax, 2, "복제본", off=True, hot_off=(step == 1))
    x, y, w, h = CARD
    box(ax, x, y, w, h, fc=PAPER)
    label(ax, x + w / 2, y + h - 0.45, "마스터", fs=11, bold=True)
    empty(ax, x + 1.2, y + 0.4, w - 2.4, 0.8, "없음", fs=11)
    label(ax, 0.3, 5.95, "노드 둘을 껐어요. es01 혼자 1표", fs=11, ha="left", color=RED if step == 1 else INK,
          bold=step == 1)
    if step == 1:
        label(ax, 0.3, 5.35, "1표는 3표 중 과반(2표)이 안 돼요", fs=10.5, ha="left", color=INK)
        return
    cell(ax, 0.3, 4.95, 5.6, 0.55, "주문 검색 · 문서 수 세기 → ✓ 답해요", fs=10.5)
    cell(ax, 0.3, 4.2, 5.6, 0.55, "새 주문 저장 → ✗ no master", hot=True, fs=10.5)
    moral(ax, 6.0, 0.55, "마스터가 없으면 쓰기만 막혀요")


# ── 마스터는 과반이 뽑아요 ─────────────────────────────────────────
QX = [0.5, 2.4, 4.3, 7.4, 9.3]
QW, QY, QH = 1.55, 2.5, 1.1
SPLIT = 6.4


def cand(ax, k, s, hot=False, dim=False):
    box(ax, QX[k], QY, QW, QH, fc=PINK if hot else ("white" if dim else NOTE), ec=RED if hot else (GREY if dim else INK))
    label(ax, QX[k] + QW / 2, QY + QH / 2, s, fs=11, color=RED if hot else (GREY if dim else "#222"), bold=hot)


def quorum(ax, step):
    label(ax, 0.3, 6.15, "마스터 후보 5개 (과반 = 3표)", fs=11.5, ha="left", bold=True)
    right_dim = step == 4
    for k in range(5):
        if k == 0:
            cand(ax, k, "마스터", hot=False)
        elif k == 3 and step == 3:
            cand(ax, k, "마스터", hot=True)
        else:
            cand(ax, k, "후보", dim=(k >= 3 and right_dim))
    if step == 1:
        label(ax, 6.0, 1.5, "평소에는 다섯이 서로 연결돼 있어요", fs=11, color=INK)
        return
    ax.plot([SPLIT, SPLIT], [1.85, 5.2], color=RED if step == 2 else INK, lw=2.2, ls=(0, (4, 3)))
    label(ax, SPLIT, 5.5, "네트워크가 끊김", fs=10.5, color=RED if step == 2 else INK, bold=step == 2)
    label(ax, (QX[0] + QX[2] + QW) / 2, 4.15, "3개", fs=11, color=INK)
    label(ax, (QX[3] + QX[4] + QW) / 2, 4.15, "2개", fs=11, color=INK)
    if step == 2:
        label(ax, 6.0, 1.3, "양쪽은 서로에게 닿지 못해요", fs=11, color=INK)
    elif step == 3:
        label(ax, (QX[3] + QX[4] + QW) / 2, 1.95, "만약 2표로도 뽑으면", fs=10.5, color=RED)
        label(ax, 6.0, 1.2, "마스터가 둘: 스플릿 브레인", fs=11.5, color=RED, bold=True)
    else:
        ax.add_patch(Rectangle((QX[0] - 0.2, QY - 0.2), QX[2] + QW - QX[0] + 0.4, QH + 0.4, fill=False, ec=RED, lw=2.0))
        label(ax, (QX[0] + QX[2] + QW) / 2, 1.85, "3표 = 과반 → 마스터", fs=11, color=RED, bold=True)
        label(ax, (QX[3] + QX[4] + QW) / 2, 1.85, "2표 → 마스터 없음, 쓰기 막힘", fs=10.5, color=INK)
        moral(ax, 6.0, 0.8, "과반은 한쪽에만 있어서 마스터는 하나예요")


# ── 복제본 0은 언제 괜찮을까요 ─────────────────────────────────────
def decide():
    fig, ax = canvas(10, 3.6, 15, 5.4)
    box(ax, 0.3, 3.6, 6.0, 1.3, fc=NOTE)
    label(ax, 3.3, 4.25, "이 인덱스의 원본이 ES에만 있나요?", fs=10.5, bold=True)
    arrow(ax, (6.4, 4.25), (8.4, 4.25), color=RED)
    label(ax, 7.4, 4.55, "예", fs=10, color=RED)
    box(ax, 8.5, 3.6, 6.2, 1.3, fc=PINK, ec=RED)
    label(ax, 11.6, 4.25, "복제본을 0으로 내리지 말고\n디스크를 늘리거나 오래된 데이터를 줄여요", fs=10, color=RED, bold=True)
    arrow(ax, (3.3, 3.5), (3.3, 2.6))
    label(ax, 3.6, 3.05, "아니요", fs=10, color=INK, ha="left")
    box(ax, 0.3, 1.3, 6.0, 1.2, fc=PAPER)
    label(ax, 3.3, 1.9, "다시 색인할 수 있으니\n잠깐 0으로 둬도 돼요", fs=10)
    box(ax, 8.5, 1.3, 6.2, 1.2, fc=LIGHT, ec=GREY)
    label(ax, 11.6, 1.9, "복제본이 0이면 노드 하나만 꺼져도\n그 샤드는 빨간색이에요", fs=10, color=INK)
    save(fig, OUT, "es14-decide.svg")


# ── 정리: 낱말 카드 ────────────────────────────────────────────────
def cards():
    fig, ax = canvas(6.4, 13.0, 9.8, 20.45)
    W, H = 4.6, 3.8

    def card_(i, name, line):
        col, r = i % 2, i // 2
        x, y = 0.2 + col * 4.9, 16.45 - r * 4.05
        box(ax, x, y, W, H, fc="white")
        label(ax, x + 0.25, y + H - 0.4, name, fs=12.5, ha="left", bold=True)
        label(ax, x + W / 2, y + 0.6, line, fs=10, color=INK)
        return x, y

    x, y = card_(0, "주 샤드", "쓰기를 먼저 받는 복사본")
    label(ax, x + 1.0, y + 2.1, "쓰기", fs=10, color=INK)
    arrow(ax, (x + 1.4, y + 2.1), (x + 2.1, y + 2.1), color=RED, ms=11)
    cell(ax, x + 2.2, y + 1.8, 1.8, 0.6, "주 샤드", hot=True, fs=10)
    x, y = card_(1, "복제본", "주 샤드를 그대로 받아\n적는 복사본")
    cell(ax, x + 0.35, y + 1.85, 1.55, 0.6, "주 샤드", fs=9.5, fc="white")
    arrow(ax, (x + 2.0, y + 2.15), (x + 2.6, y + 2.15), color=RED, ms=11)
    cell(ax, x + 2.7, y + 1.85, 1.55, 0.6, "복제본", hot=True, fs=9.5)
    x, y = card_(2, "시퀀스 번호", "쓰기마다 0부터 하나씩\n매기는 번호")
    cells(ax, x + 0.4, y + 1.85, ["0", "1", "2", "⋯", "100"], w=0.7, h=0.55, gap=0.06, hot=(0, 1, 2, 4), fs=9.5)
    x, y = card_(3, "로컬 체크포인트", "0부터 빈틈없이 받은\n마지막 번호")
    for k, t in enumerate(["5", "6", "7", "", "9"]):
        if t:
            cell(ax, x + 0.4 + k * 0.72, y + 1.85, 0.65, 0.55, t, hot=(t == "7"), fs=9.5, fc=None if t == "7" else "white")
        else:
            empty(ax, x + 0.4 + k * 0.72, y + 1.85, 0.65, 0.55)
    x, y = card_(4, "글로벌 체크포인트", "세 복사본 로컬 체크포인트\n가운데 가장 작은 값")
    for r, n in enumerate([6, 5, 3]):
        for k in range(6):
            cx, cy = x + 0.8 + k * 0.5, y + 2.6 - r * 0.45
            if k < n:
                cell(ax, cx, cy, 0.42, 0.36, "", fs=8, fc="white")
            else:
                empty(ax, cx, cy, 0.42, 0.36)
    gx = x + 0.8 + 3 * 0.5 - 0.04
    ax.plot([gx, gx], [y + 1.6, y + 3.1], color=RED, lw=2.0, ls="--")
    x, y = card_(5, "in-sync 목록", "쓰기를 빠짐없이 받은\n복사본 목록")
    for k, n in enumerate(NAMES):
        cell(ax, x + 0.4 + k * 1.3, y + 1.85, 1.15, 0.55, n, hot=(k < 2), dim=(k == 2), fs=9.5)
    strike(ax, x + 0.4 + 2 * 1.3, y + 1.85, 1.15, 0.55)
    x, y = card_(6, "primary term", "주 샤드가 바뀔 때마다\n하나씩 커지는 번호")
    cell(ax, x + 1.0, y + 1.85, 0.8, 0.6, "1", fs=10.5, fc="white")
    arrow(ax, (x + 1.9, y + 2.15), (x + 2.6, y + 2.15), color=RED, ms=11)
    cell(ax, x + 2.7, y + 1.85, 0.8, 0.6, "2", hot=True, fs=10.5)
    x, y = card_(7, "마스터 후보", "투표해서 마스터를\n뽑는 노드들")
    for k in range(3):
        box(ax, x + 0.4 + k * 1.3, y + 1.8, 1.1, 0.6, fc=PINK if k == 0 else NOTE, ec=RED if k == 0 else INK, lw=1.3)
        label(ax, x + 0.95 + k * 1.3, y + 2.1, "마스터" if k == 0 else "후보", fs=9.5, color=RED if k == 0 else "#222")
    x, y = card_(8, "빈 작업 (no-op)", "빈 번호를 채우는\n아무 일도 안 하는 작업")
    cells(ax, x + 0.9, y + 1.85, ["7", "빈", "9"], w=0.8, h=0.55, gap=0.08, hot=(1,), fs=9.5)
    x, y = card_(9, "스플릿 브레인", "마스터가 둘 생기는 사고")
    for k in range(2):
        box(ax, x + 0.5 + k * 2.2, y + 1.8, 1.4, 0.6, fc=PINK, ec=RED, lw=1.3)
        label(ax, x + 1.2 + k * 2.2, y + 2.1, "마스터", fs=9.5, color=RED)
    ax.plot([x + 2.3, x + 2.3], [y + 1.6, y + 2.6], color=INK, lw=1.6, ls=(0, (3, 2)))
    save(fig, OUT, "es14-cards.svg")


if __name__ == "__main__":
    S, L = (7.2, 3.8), (12, 6.6)
    stage(opening, 4, OUT, "es14-open", S, L)
    stage(copies, 4, OUT, "es14-copies", S, L)
    stage(seq, 2, OUT, "es14-seq", S, L)
    stage(ledger, 2, OUT, "es14-local", S, L)
    stage(lambda ax, k: ledger(ax, k + 2), 3, OUT, "es14-checkpoints", S, L)
    stage(takeover, 4, OUT, "es14-takeover", S, L)
    stage(lambda ax, k: ledger(ax, k + 5), 3, OUT, "es14-fix", S, L)
    stage(lambda ax, k: takeover(ax, k + 4), 2, OUT, "es14-rejoin", S, L)
    stage(quorum, 4, OUT, "es14-quorum", S, L)
    stage(nomaster, 2, OUT, "es14-nomaster", S, L)
    decide()
    stage(back, 3, OUT, "es14-back", S, L)
    cards()
