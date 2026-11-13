"""Elasticsearch 14편 그림 만들기. 실행: python lab/fig_es14.py  → docs/elasticsearch/img/14/*.svg

예시는 주문 인덱스(샤드 1개, 복사본 3개)와 노드 es01·es02·es03을 편 끝까지 잇는다.
처음 주 샤드·마스터는 es03. es03이 꺼지면 es02가 주 샤드, es01이 마스터.
설명용 쓰기 10건(시퀀스 번호 0~9): es03 0~9, es02 0~7·9, es01 0~5 → 로컬 체크포인트 9·7·5, 글로벌 5.
그림 안 글씨는 낱말과 숫자만 둔다. 문장은 본문과 그림 설명에 둔다.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "es"))
from figkit import (GREY, INK, LIGHT, NOTE, PAPER, PINK, RED, arrow, box,  # noqa: E402
                    canvas, cell, cylinder, label, outdir, save)
from matplotlib.patches import Rectangle  # noqa: E402

OUT = outdir("14")
NAMES = ["es01", "es02", "es03"]
SIZE, LIM = (7.2, 3.8), (12, 6.6)


def one(draw, name):
    fig, ax = canvas(*SIZE, *LIM)
    ax.add_patch(Rectangle((0, 0), *LIM, fill=False, ec="none"))  # 그림마다 잘리는 테두리를 같게
    draw(ax)
    save(fig, OUT, name)


def empty(ax, x, y, w, h, s="", fs=10, ec=GREY, lw=1.0):
    ax.add_patch(Rectangle((x, y), w, h, fc="white", ec=ec, lw=lw, ls="--"))
    if s:
        label(ax, x + w / 2, y + h / 2, s, fs=fs, color=GREY)


def cross(ax, x, y, w, h, color=RED, lw=2.4):
    ax.plot([x, x + w], [y, y + h], color=color, lw=lw)
    ax.plot([x, x + w], [y + h, y], color=color, lw=lw)


def strike(ax, x, y, w, h, color=GREY, lw=1.6):
    ax.plot([x, x + w], [y + h / 2, y + h / 2], color=color, lw=lw)


# ── 여는 장면: 주문 관리 화면 + 노드 원통 셋 ─────────────────────────
CX = [6.15, 8.05, 9.95]
CW, CY, CH = 1.6, 3.3, 1.5


def screen(ax, found, saved):
    """주문 관리 화면. found/saved=(글, 강조 여부) 또는 None(빈 답 칸)."""
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
        s, hot = ans
        ax.add_patch(Rectangle((0.55, y - 0.8), 4.9, 0.6, fc=PINK if hot else NOTE, ec=RED if hot else INK,
                               lw=1.8 if hot else 1.1))
        label(ax, 0.7, y - 0.5, s, fs=10.5, ha="left", color=RED if hot else "#222", bold=hot)


def drum(ax, i, role, off=False, hot=False, master=False):
    """노드 원통 하나. role=안에 든 복사본 이름, master=위에 마스터 꼬리표. hot=이 그림에서 바뀐 곳."""
    x = CX[i]
    if off:
        cylinder(ax, x, CY, CW, CH, NAMES[i], fc=LIGHT, ec=GREY, color=RED if hot else GREY)
        cell(ax, x + 0.15, CY + 0.45, CW - 0.3, 0.6, role, dim=True, fs=9.5)
        cross(ax, x + 0.1, CY + 0.1, CW - 0.2, CH - 0.1, color=RED if hot else GREY)
        label(ax, x + CW / 2, CY - 0.45, "꺼짐", fs=10.5, color=RED if hot else GREY, bold=hot)
    else:
        cylinder(ax, x, CY, CW, CH, NAMES[i])
        cell(ax, x + 0.15, CY + 0.45, CW - 0.3, 0.6, role, hot=hot and not master, fs=9.5)
    if master:
        ax.add_patch(Rectangle((x + 0.25, 5.75), CW - 0.5, 0.45, fc=PINK if hot else PAPER,
                               ec=RED if hot else INK, lw=1.6 if hot else 1.1))
        label(ax, x + CW / 2, 5.97, "마스터", fs=10, color=RED if hot else "#222", bold=hot)


def open_before(ax):
    screen(ax, ("주문 100건", False), None)
    drum(ax, 0, "복제본")
    drum(ax, 1, "복제본")
    drum(ax, 2, "주 샤드", master=True)


def open_after(ax):
    screen(ax, ("주문 100건", True), ("✓ 저장", True))
    drum(ax, 0, "복제본", master=True, hot=True)
    drum(ax, 1, "주 샤드", hot=True)
    drum(ax, 2, "주 샤드", off=True, hot=True)


# ── 본문 무대: 노드 상자 셋 ───────────────────────────────────────
NBX = [0.3, 4.2, 8.1]
NBW, NBY, NBH = 3.5, 1.25, 1.75


def node(ax, i, role, hot=False, off=False, note=""):
    x = NBX[i]
    if off:
        box(ax, x, NBY, NBW, NBH, fc=LIGHT, ec=GREY, lw=1.4)
        label(ax, x + 0.2, NBY + NBH - 0.3, NAMES[i], fs=11, ha="left", bold=True, color=GREY)
        label(ax, x + NBW - 0.2, NBY + NBH - 0.3, "꺼짐", fs=10.5, ha="right", color=GREY)
        cell(ax, x + 0.6, NBY + 0.3, 2.3, 0.65, role, dim=True, fs=10.5)
        cross(ax, x + 0.6, NBY + 0.3, 2.3, 0.65, color=GREY, lw=2.0)
        return
    box(ax, x, NBY, NBW, NBH, fc=NOTE)
    label(ax, x + 0.2, NBY + NBH - 0.3, NAMES[i], fs=11, ha="left", bold=True)
    if note:
        label(ax, x + NBW - 0.2, NBY + NBH - 0.3, note, fs=10.5, ha="right", color=INK)
    cell(ax, x + 0.6, NBY + 0.3, 2.3, 0.65, role, hot=hot, fs=10.5)


def top(i):
    return NBX[i] + NBW / 2, NBY + NBH + 0.05


def write(ax):
    """쓰기: ① 주 샤드가 받고 ② 복제본 둘에 보내고 ③ 성공."""
    node(ax, 0, "복제본")
    node(ax, 1, "복제본")
    node(ax, 2, "주 샤드")
    x, y, w, h = 8.1, 5.35, 3.5, 0.75
    box(ax, x, y, w, h, fc=PAPER)
    label(ax, x + w / 2, y + h / 2, "새 주문 저장", fs=11)
    arrow(ax, (9.2, 5.3), (9.2, 3.1), color=RED, ms=14)
    label(ax, 9.05, 4.2, "①", fs=12, ha="right", color=RED, bold=True)
    sx, sy = 8.6, 3.1
    arrow(ax, (sx, sy), (top(1)[0] + 0.4, sy), color=RED, ms=14, rad=0.5)
    arrow(ax, (sx, sy), (top(0)[0], sy), color=RED, ms=14, rad=0.38)
    label(ax, 5.6, 5.0, "② 복제본 둘에", fs=11, color=RED, bold=True)
    arrow(ax, (10.7, 3.1), (10.7, 5.3), color=RED, ms=14)
    label(ax, 10.85, 4.2, "③", fs=12, ha="left", color=RED, bold=True)
    label(ax, 7.9, 6.25, "③ 성공: total 3, successful 3", fs=11, ha="right", color=INK)


# ── 시퀀스 번호와 체크포인트: 번호 칸 줄 셋 ─────────────────────────
ROWY = {2: 4.45, 1: 3.35, 0: 2.25}
RX0, RW, RG, RH = 2.95, 0.6, 0.08, 0.7
LCPX = 10.6
GCPX = RX0 + 6 * (RW + RG) - RG / 2


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


def ledger_head(ax):
    label(ax, 0.3, 6.2, "쓰기 10건 (번호 0~9)", fs=11, ha="left", color=INK)
    label(ax, LCPX, 5.65, "로컬\n체크포인트", fs=10, color=INK)


ES02 = {0, 1, 2, 3, 4, 5, 6, 7, 9}


def local(ax):
    ledger_head(ax)
    rowname(ax, 2, "주 샤드")
    row(ax, 2, set(range(10)))
    lcp(ax, 2, 9)
    rowname(ax, 1, "복제본")
    row(ax, 1, ES02, hot_gap=(8,))
    lcp(ax, 1, 7, hot=True)
    label(ax, rx(8) + RW / 2, ROWY[1] - 0.3, "8 아직", fs=10, color=RED)
    y = ROWY[1] - 0.15
    ax.plot([rx(0), rx(7) + RW], [y, y], color=RED, lw=2.4)
    label(ax, (rx(0) + rx(7) + RW) / 2, y - 0.35, "0~7 빈틈없음", fs=10.5, color=RED)


def global_cp(ax):
    ledger_head(ax)
    rowname(ax, 2, "주 샤드")
    row(ax, 2, set(range(10)))
    lcp(ax, 2, 9)
    rowname(ax, 1, "복제본")
    row(ax, 1, ES02)
    lcp(ax, 1, 7)
    rowname(ax, 0, "복제본")
    row(ax, 0, set(range(6)))
    lcp(ax, 0, 5, hot=True)
    ax.plot([GCPX, GCPX], [ROWY[0] - 0.25, ROWY[2] + RH + 0.25], color=RED, lw=2.4, ls="--")
    lo, hi = ROWY[0] - 0.12, ROWY[2] + RH + 0.12
    ax.add_patch(Rectangle((rx(0) - 0.1, lo), GCPX - rx(0) + 0.05, hi - lo, fill=False, ec=RED, lw=2.0))
    label(ax, (rx(0) + GCPX) / 2, 1.5, "셋 다 같음", fs=10.5, color=RED, bold=True)
    label(ax, (GCPX + rx(9) + RW) / 2, 1.5, "다를 수 있음", fs=10.5, color=INK)
    label(ax, 6.0, 0.7, "글로벌 체크포인트 5", fs=11.5, color=RED, bold=True)


def fix(ax):
    ledger_head(ax)
    rowname(ax, 2, "꺼짐", color=GREY)
    row(ax, 2, set(range(10)), dim=True)
    lcp(ax, 2, 9, dim=True)
    rowname(ax, 1, "새 주 샤드")
    row(ax, 1, set(range(10)), hot=(8,), text={8: "빈"})
    lcp(ax, 1, 9, hot=True)
    rowname(ax, 0, "복제본")
    row(ax, 0, set(range(10)), hot=set(range(6, 10)), text={8: "빈"})
    lcp(ax, 0, 9, hot=True)
    ax.plot([GCPX, GCPX], [ROWY[0] - 0.25, ROWY[2] + RH + 0.25], color=INK, lw=1.8, ls="--")
    arrow(ax, (rx(9) + RW + 0.08, ROWY[1] + 0.35), (rx(9) + RW + 0.08, ROWY[0] + 0.35), color=RED, ms=13, rad=-0.6)
    label(ax, (rx(0) + GCPX) / 2, 1.5, "0~5 그대로", fs=10.5, color=INK)
    label(ax, (GCPX + rx(9) + RW) / 2, 1.5, "6~9 보냄", fs=10.5, color=RED, bold=True)


# ── 주 샤드 교체: 노드 상자 셋 + 마스터가 적어 둔 것 ─────────────────
CARD = (6.3, 4.1, 5.4, 2.25)
ISX = [8.3, 9.4, 10.5]


def card(ax, term="2", hot_term=False, out3=True):
    x, y, w, h = CARD
    box(ax, x, y, w, h, fc=PAPER)
    label(ax, x + 0.2, y + h - 0.32, "마스터 es01이 적어 둔 것", fs=10.5, ha="left", bold=True)
    label(ax, x + 0.2, y + 1.15, "in-sync 목록", fs=10, ha="left", color=INK)
    for k, n in enumerate(NAMES):
        cx, cy = ISX[k], y + 0.9
        if k == 2 and out3:
            cell(ax, cx, cy, 1.0, 0.5, n, dim=True, fs=10)
            strike(ax, cx, cy, 1.0, 0.5, lw=1.3)
        else:
            cell(ax, cx, cy, 1.0, 0.5, n, fs=10, fc="white")
    label(ax, x + 0.2, y + 0.4, "primary term", fs=10, ha="left", color=INK)
    cell(ax, ISX[0], y + 0.15, 1.0, 0.5, term, hot=hot_term, fs=11, fc=None if hot_term else "white")
    if hot_term:
        label(ax, ISX[1] - 0.05, y + 0.4, "(1 → 2)", fs=10, ha="left", color=RED)


def takeover(ax):
    label(ax, 0.3, 5.95, "es03 꺼짐", fs=11, ha="left", color=INK)
    node(ax, 0, "복제본")
    node(ax, 1, "주 샤드", hot=True)
    node(ax, 2, "주 샤드", off=True)
    card(ax, hot_term=True, out3=False)
    arrow(ax, (CARD[0] + 0.3, CARD[1] - 0.05), (top(1)[0] + 0.6, top(1)[1]), color=RED, ms=14)
    label(ax, 3.9, 3.6, "in-sync 목록에서", fs=10.5, color=RED, ha="right")


def reject(ax):
    label(ax, 0.3, 5.95, "es03 돌아옴", fs=11, ha="left", color=INK)
    node(ax, 0, "복제본")
    node(ax, 1, "주 샤드")
    node(ax, 2, "옛 주 샤드", note="term 1")
    card(ax)
    arrow(ax, (top(2)[0] - 0.4, top(2)[1]), (top(0)[0] + 0.5, top(0)[1]), color=RED, ms=14, rad=0.22)
    label(ax, 0.3, 5.35, "term 1 쓰기", fs=10.5, ha="left", color=RED)
    label(ax, 1.9, 3.55, "✗ 거절", fs=12, ha="right", color=RED, bold=True)


# ── 마스터는 과반이 뽑아요 ─────────────────────────────────────────
QX = [0.5, 2.4, 4.3, 7.4, 9.3]
QW, QY, QH = 1.55, 2.5, 1.1
SPLIT = 6.4


def cand(ax, k, s, dim=False):
    box(ax, QX[k], QY, QW, QH, fc="white" if dim else NOTE, ec=GREY if dim else INK)
    label(ax, QX[k] + QW / 2, QY + QH / 2, s, fs=11, color=GREY if dim else "#222")


def quorum(ax):
    label(ax, 0.3, 6.15, "마스터 후보 5개 (과반 3표)", fs=11.5, ha="left", bold=True)
    for k in range(5):
        cand(ax, k, "마스터" if k == 0 else "후보", dim=k >= 3)
    ax.plot([SPLIT, SPLIT], [1.85, 5.2], color=INK, lw=2.2, ls=(0, (4, 3)))
    label(ax, SPLIT, 5.5, "네트워크 끊김", fs=10.5, color=INK)
    label(ax, (QX[0] + QX[2] + QW) / 2, 4.15, "3개", fs=11, color=INK)
    label(ax, (QX[3] + QX[4] + QW) / 2, 4.15, "2개", fs=11, color=INK)
    ax.add_patch(Rectangle((QX[0] - 0.2, QY - 0.2), QX[2] + QW - QX[0] + 0.4, QH + 0.4, fill=False, ec=RED, lw=2.0))
    label(ax, (QX[0] + QX[2] + QW) / 2, 1.85, "3표 → 마스터", fs=11, color=RED, bold=True)
    label(ax, (QX[3] + QX[4] + QW) / 2, 1.85, "2표 → 마스터 없음", fs=10.5, color=INK)


if __name__ == "__main__":
    one(open_before, "es14-open-1.svg")
    one(open_after, "es14-open-2.svg")
    one(write, "es14-write.svg")
    one(local, "es14-local.svg")
    one(global_cp, "es14-global.svg")
    one(takeover, "es14-takeover.svg")
    one(reject, "es14-reject.svg")
    one(fix, "es14-fix.svg")
    one(quorum, "es14-quorum.svg")
