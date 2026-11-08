"""쿠버네티스 10편 그림 만들기. 실행: python lab/fig_k8s10.py  → docs/kubernetes/img/10/*.svg

본문 절은 장면 띠로 그린다: 같은 무대를 여러 장 그리고 장마다 바뀐 곳만 빨강으로 칠한다.
예시는 빵집 주문 앱의 주문 처리 파드. 매니페스트는 requests cpu 2 · memory 2Gi, limits cpu 3 · memory 3Gi.
노드 A·B는 CPU 4개씩. 노드 A에는 주문 장부(예약 2), 노드 B에는 주문 화면(1)과 다른 앱(2).
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "es"))
from figkit import (GREY, INK, LIGHT, NOTE, PAPER, PINK, RED, arrow, box, bubble,  # noqa: E402
                    canvas, cell, cylinder, label, moral, outdir, save, stage)
from matplotlib.patches import Rectangle  # noqa: E402

OUT = outdir("10", topic="kubernetes")


def empty(ax, x, y, w, h, ec=GREY):
    ax.add_patch(Rectangle((x, y), w, h, fc="white", ec=ec, lw=1.2, ls="--"))


def cross(ax, x0, y0, x1, y1, color=RED, lw=3):
    ax.plot([x0, x1], [y0, y1], color=color, lw=lw)
    ax.plot([x0, x1], [y1, y0], color=color, lw=lw)


def vline(ax, x, y0, y1, color=RED):
    ax.plot([x, x], [y0, y1], color=color, lw=2.2, ls="--")


# ── 파드 목록 화면 ─────────────────────────────────────────────────
ROW_Y = [4.75 - k * 0.85 for k in range(4)]


def podlist(ax, rows, hot=(), dim=(), corner=None):
    box(ax, 0.3, 0.95, 6.7, 5.4, fc="white", round_=False)
    ax.add_patch(Rectangle((0.3, 5.9), 6.7, 0.45, fc=LIGHT, ec=INK, lw=1.2))
    label(ax, 0.5, 6.12, "빵집 주문 앱 · 파드 목록", fs=11, ha="left", color=INK)
    label(ax, 0.55, 5.45, "이름", fs=10, ha="left", color=INK)
    label(ax, 2.75, 5.45, "상태", fs=10, ha="left", color=INK)
    ax.plot([0.5, 6.8], [5.2, 5.2], color=INK, lw=1.0)
    for k, (n, s) in enumerate(rows):
        y = ROW_Y[k]
        on, off = k in hot, k in dim
        if on:
            ax.add_patch(Rectangle((0.45, y - 0.3), 6.4, 0.6, fc=PINK, ec=RED, lw=1.8))
        else:
            ax.plot([0.5, 6.8], [y - 0.34, y - 0.34], color=GREY, lw=0.8)
        c = RED if on else (GREY if off else "#222")
        label(ax, 0.55, y, n, fs=11, ha="left", color=c, bold=on)
        label(ax, 2.75, y, s, fs=10.5, ha="left", color=c, bold=on)
    if corner:
        label(ax, 9.6, 6.15, corner, fs=12.5, color=INK, bold=True)


ROWS = [("주문 화면", "실행 중"), ("주문 장부", "실행 중"), ("주문 처리-1", "실행 중"), ("주문 처리-2", "자리 없음 (Pending)")]
OOM = "다시 시작 2번 · OOMKilled"


def gauge(ax, title, n, fill, hot=(), limit=None, limit_label="", over=False, note=None, unit_w=0.85):
    """오른쪽 사용량 칸 줄. fill=채운 칸 수, hot=빨강 칸, limit=몇 칸 뒤에 한도 점선."""
    label(ax, 9.6, 5.25, title, fs=11, bold=True)
    x0 = 7.75
    for k in range(n):
        x = x0 + k * (unit_w + 0.1)
        if k < fill:
            cell(ax, x, 3.9, unit_w, 0.8, "", hot=(k in hot), fc=None if k in hot else LIGHT)
        elif over and k == fill:
            empty(ax, x, 3.9, unit_w, 0.8, ec=RED)
            cross(ax, x + 0.15, 4.05, x + unit_w - 0.15, 4.55, lw=2.2)
        else:
            empty(ax, x, 3.9, unit_w, 0.8)
    if limit is not None:
        lx = x0 + limit * (unit_w + 0.1) - 0.05
        vline(ax, lx, 3.7, 4.95)
        label(ax, lx + 0.1, 3.45, limit_label, fs=10, color=RED, bold=True, ha="left")
    if note:
        label(ax, 9.6, 3.0, note, fs=10, color=INK)


def opening(ax, step):
    if step == 1:
        podlist(ax, ROWS, hot=(3,))
        gauge(ax, "노드 A · CPU 4개", 4, 1, note="지금 쓰는 CPU는 1개")
        moral(ax, 6.0, 0.35, "노드는 한가한데 자리가 없대요")
    elif step == 2:
        rows = ROWS[:2] + [("주문 처리-1", "느려요"), ROWS[3]]
        podlist(ax, rows, hot=(2,), dim=(3,))
        gauge(ax, "주문 처리-1 · CPU", 4, 3, hot=(0, 1, 2), limit=3, limit_label="한도 3")
        moral(ax, 6.0, 0.35, "CPU가 남는데 3개에서 더 못 올라가요")
    else:
        rows = ROWS[:2] + [("주문 처리-1", OOM), ROWS[3]]
        podlist(ax, rows, hot=(2,), dim=(3,))
        gauge(ax, "주문 처리-1 · 메모리", 4, 3, limit=3, limit_label="한도 3Gi", over=True)
        moral(ax, 6.0, 0.35, "메모리를 더 쓰려다 다시 시작했어요")


# ── 스케줄러: 예약의 합으로 노드 고르기 ────────────────────────────
CW, CG = 0.85, 0.1
NODES = {"A": 0.3, "B": 4.6}
SCH = (9.6, 1.0, 2.0, 1.3)
SSAY = (7.0, 4.75, 4.8, 1.2)
STAIL = (10.6, 3.15)


def node(ax, name, pods, use=None):
    """pods=[(이름, 칸 수, hot)], 남는 칸은 점선. use=실제 사용 칸 수."""
    x = NODES[name]
    box(ax, x, 0.95, 4.0, 2.85, fc="white")
    label(ax, x + 0.2, 3.5, f"노드 {name} · CPU 4개", fs=10.5, ha="left", bold=True)
    cx = x + 0.15
    used = 0
    for n, w, hot in pods:
        ww = w * CW + (w - 1) * CG
        cell(ax, cx, 2.25, ww, 0.8, n, hot=hot, fs=9.5)
        cx += ww + CG
        used += w
    for _ in range(4 - used):
        empty(ax, cx, 2.25, CW, 0.8)
        cx += CW + CG
    if use is not None:
        label(ax, x + 0.2, 1.85, "실제 사용", fs=9, ha="left", color=INK)
        for k in range(4):
            xx = x + 1.3 + k * 0.62
            if k < use:
                ax.add_patch(Rectangle((xx, 1.1), 0.55, 0.45, fc=LIGHT, ec=INK, lw=1.0))
            else:
                ax.add_patch(Rectangle((xx, 1.1), 0.55, 0.45, fc="white", ec=GREY, lw=1.0, ls="--"))


def mark(ax, name, ok, text, hot=True):
    x = NODES[name] + 2.0
    c = RED if hot else INK
    label(ax, x, 4.15, ("✓ " if ok else "✗ ") + text, fs=10.5, color=c, bold=hot)


def podcard(ax, s):
    box(ax, 0.3, 5.0, 4.6, 0.85, fc=PINK, ec=RED)
    label(ax, 2.6, 5.42, s, fs=11, color=RED, bold=True)


def sched(ax, step):
    cylinder(ax, *SCH, "스케줄러")
    if step == 1:
        node(ax, "A", [("주문 장부", 2, False)])
        node(ax, "B", [("화면", 1, False), ("다른 앱", 2, False)])
        podcard(ax, "주문 처리-1 · 예약 CPU 2")
        bubble(ax, *SSAY, "어느 노드에\n놓을까요?", STAIL, hot=True)
    elif step == 2:
        node(ax, "A", [("주문 장부", 2, False), ("주문 처리-1", 2, True)])
        node(ax, "B", [("화면", 1, False), ("다른 앱", 2, False)])
        box(ax, 0.3, 5.0, 4.6, 0.85, fc=LIGHT, ec=GREY)
        label(ax, 2.6, 5.42, "주문 처리-1 · 예약 CPU 2", fs=11, color=GREY)
        mark(ax, "A", True, "남은 칸 2")
        mark(ax, "B", False, "남은 칸 1", hot=False)
        bubble(ax, *SSAY, "맡아 둔 칸을 더해서\n남은 칸을 세요", STAIL, hot=True)
    else:
        node(ax, "A", [("주문 장부", 2, False), ("주문 처리-1", 2, False)], use=1)
        node(ax, "B", [("화면", 1, False), ("다른 앱", 2, False)])
        podcard(ax, "주문 처리-2 · 예약 CPU 2")
        mark(ax, "A", False, "남은 칸 0")
        mark(ax, "B", False, "남은 칸 1")
        bubble(ax, *SSAY, "놓을 곳이 없어요\n기다려요 (Pending)", STAIL, hot=True)
        moral(ax, 6.0, 0.35, "스케줄러는 실제 사용량 대신 예약의 합을 봐요")


# ── 예약보다 더 쓰기 ───────────────────────────────────────────────
OW = 1.55
OX = [0.7 + k * (OW + 0.15) for k in range(4)]


def over(ax, step):
    box(ax, 0.3, 0.95, 7.4, 4.6, fc="white")
    label(ax, 0.55, 5.2, "노드 A · CPU 4개", fs=11, ha="left", bold=True)
    label(ax, 0.7, 4.65, "예약", fs=10, ha="left", color=INK)
    cell(ax, OX[0], 3.6, 2 * OW + 0.15, 0.8, "주문 장부", fs=10.5)
    cell(ax, OX[2], 3.6, 2 * OW + 0.15, 0.8, "주문 처리-1", fs=10.5)
    label(ax, 0.7, 2.75, "실제 사용", fs=10, ha="left", color=INK)
    if step == 1:
        use = ["장부", None, "처리-1", "처리-1"]
        hot = ()
    elif step == 2:
        use = ["장부", "처리-1", "처리-1", "처리-1"]
        hot = (1,)
    else:
        use = ["장부", "장부", "처리-1", "처리-1"]
        hot = (0, 1, 2, 3)
    for k, u in enumerate(use):
        if u is None:
            empty(ax, OX[k], 1.7, OW, 0.8)
        else:
            cell(ax, OX[k], 1.7, OW, 0.8, u, hot=(k in hot), fs=10.5)
    if step == 1:
        bubble(ax, 3.7, 5.75, 5.3, 0.8, "점심이라 CPU 3개만큼 일하고 싶어요", (5.9, 4.45), hot=True, fs=10.5)
    elif step == 2:
        label(ax, 9.75, 2.1, "남는 칸이 있으면\n예약보다 더 써도 돼요", fs=11, color=RED, bold=True)
    else:
        bubble(ax, 3.4, 5.75, 3.2, 0.75, "나도 바빠졌어요", (2.2, 4.45), hot=True, fs=10.5)
        label(ax, 9.75, 2.1, "둘 다 바쁘면\n예약한 크기에 맞춰\n나눠요", fs=11, color=RED, bold=True)


# ── CPU 한도: 시간 조각 ────────────────────────────────────────────
COLX = [3.0, 5.25]
ROWY = [4.55, 3.75, 2.95, 2.15]
GW, GH = 2.05, 0.65


def cpu(ax, step):
    top = "한도가 없으면" if step == 1 else "한도 CPU 3"
    label(ax, 0.4, 6.1, top, fs=12.5, ha="left", bold=True, color=RED if step == 2 else "#222")
    for c, x in enumerate(COLX):
        label(ax, x + GW / 2, 5.45, f"조각 {c + 1}", fs=10.5, color=INK)
    for r, y in enumerate(ROWY):
        label(ax, 2.75, y + GH / 2, f"주문 {r + 1}", fs=10.5, ha="right", color=INK)
    ax.annotate("", xy=(7.6, 1.6), xytext=(3.0, 1.6), arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.4))
    label(ax, 7.75, 1.6, "시간", fs=10, ha="left", color=INK)
    for r, y in enumerate(ROWY):
        for c, x in enumerate(COLX):
            if c == 0 and (step == 1 or r < 3):
                cell(ax, x, y, GW, GH, "처리", fs=10)
            elif step == 3 and c == 1 and r == 3:
                cell(ax, x, y, GW, GH, "처리", hot=True, fs=10)
            elif step >= 2 and c == 0 and r == 3:
                empty(ax, x, y, GW, GH, ec=RED if step == 2 else GREY)
            else:
                empty(ax, x, y, GW, GH)
    if step == 1:
        label(ax, 9.8, 4.0, "한 조각에\n넷 다 끝나요", fs=11.5, color=RED, bold=True)
    else:
        ax.plot([2.85, 5.2], [2.88, 2.88], color=RED, lw=2.2, ls="--")
        label(ax, 7.55, 3.15, "한도 3", fs=10.5, ha="left", color=RED, bold=(step == 2))
        if step == 2:
            label(ax, 7.55, 2.47, "주문 4는 기다려요", fs=11, ha="left", color=RED, bold=True)
        else:
            label(ax, 7.55, 2.47, "한 조각 늦게 끝나요", fs=11, ha="left", color=RED, bold=True)
            moral(ax, 6.0, 0.7, "CPU 한도를 넘으면 기다리느라 느려져요")


# ── 메모리 한도: OOM 킬 ────────────────────────────────────────────
MW = 1.6
MX = [0.6 + k * (MW + 0.15) for k in range(4)]
KER = (9.4, 1.0, 2.2, 1.25)


def mem(ax, step):
    cylinder(ax, *KER, "커널")
    label(ax, 0.6, 4.45, "주문 처리-1의 메모리", fs=10.5, ha="left", bold=True)
    for k in range(4):
        if k < 3 and step < 3:
            cell(ax, MX[k], 3.0, MW, 1.0, "주문 자료", fs=10.5)
        elif k == 3 and step == 1:
            empty(ax, MX[k], 3.0, MW, 1.0, ec=RED)
            label(ax, MX[k] + MW / 2, 3.5, "하나 더", fs=10.5, color=RED)
        else:
            empty(ax, MX[k], 3.0, MW, 1.0)
    lx = MX[3] - 0.075
    vline(ax, lx, 2.8, 4.3)
    label(ax, lx - 0.1, 4.45, "한도 3Gi", fs=10, ha="right", color=RED, bold=True)
    if step == 1:
        bubble(ax, 4.2, 5.0, 4.6, 1.15, "주문 처리-1: 주문 자료를\n하나 더 올려야 해요", (MX[3] + MW / 2, 4.1), hot=True, fs=10.5)
    elif step == 2:
        cross(ax, MX[0] + 0.1, 3.05, MX[2] + MW - 0.1, 3.95, lw=4)
        label(ax, 3.2, 2.45, "OOM 킬", fs=13, color=RED, bold=True)
        bubble(ax, 6.7, 4.75, 5.1, 1.2, "한도를 넘었으니\n이 프로세스를 끝내요", (10.5, 2.95), hot=True, fs=10.5)
    else:
        label(ax, 3.2, 5.1, "다시 시작 1번", fs=12.5, color=RED, bold=True)
        label(ax, 3.2, 2.45, "들고 있던 주문 자료는 사라졌어요", fs=10.5, color=INK)
        moral(ax, 5.5, 0.55, "메모리 한도를 넘으면 프로세스가 죽어요")


# ── 판단 (한 장) ───────────────────────────────────────────────────
def decide():
    fig, ax = canvas(10, 4.8, 15, 7.2)
    box(ax, 0.3, 5.8, 6.4, 1.1, fc=NOTE)
    label(ax, 3.5, 6.35, "이 파드가 바쁠 때 쓰는 양을 알고 있나요?", fs=10.5, bold=True)
    arrow(ax, (6.8, 6.35), (8.4, 6.35)); label(ax, 7.6, 6.65, "아니요", fs=10, color=INK)
    box(ax, 8.5, 5.8, 6.2, 1.1, fc=PAPER)
    label(ax, 11.6, 6.35, "먼저 실제 사용량을 지켜봐요", fs=10.5)
    arrow(ax, (3.5, 5.7), (3.5, 5.0)); label(ax, 3.8, 5.35, "예", fs=10, color=INK, ha="left")
    box(ax, 0.3, 3.85, 6.4, 1.05, fc=PAPER)
    label(ax, 3.5, 4.37, "그 양을 requests에 적어요\n(노드를 고를 때 자리를 맡아요)", fs=10.5)
    arrow(ax, (3.5, 3.75), (3.5, 3.05))
    box(ax, 0.3, 2.0, 6.4, 0.95, fc=NOTE)
    label(ax, 3.5, 2.47, "한도를 넘으면 어떻게 되면 좋을까요?", fs=10.5, bold=True)
    arrow(ax, (6.8, 2.47), (8.4, 2.47)); label(ax, 7.6, 2.8, "느려져도 돼요", fs=10, color=INK)
    box(ax, 8.5, 2.0, 6.2, 0.95, fc=PAPER)
    label(ax, 11.6, 2.47, "limits.cpu (넘으면 느려져요)", fs=10.5)
    arrow(ax, (3.5, 1.9), (3.5, 1.25), color=RED); label(ax, 3.8, 1.57, "죽으면 안 돼요", fs=10, color=RED, ha="left")
    box(ax, 0.3, 0.1, 6.4, 1.05, fc=PINK, ec=RED)
    label(ax, 3.5, 0.62, "limits.memory를 넉넉히\n프로그램도 그 안에서 쓰게", fs=10.5, color=RED, bold=True)
    save(fig, OUT, "k8s10-decide.svg")


# ── 정리: 처음 장면으로 돌아가기 ───────────────────────────────────
def tag(ax, y, s):
    label(ax, 7.25, y, s, fs=9, ha="left", color=RED, bold=True,
          bbox=dict(boxstyle="round,pad=0.25", fc=PINK, ec=RED, lw=1.3))


def back(ax, step):
    rows = ROWS[:2] + [("주문 처리-1", OOM), ROWS[3]]
    if step == 1:
        podlist(ax, rows, dim=(0, 1, 2, 3), corner="처음")
    else:
        podlist(ax, rows, hot=(2, 3))
        tag(ax, ROW_Y[3], "예약 합이 꽉 찼어요 (requests)")
        tag(ax, ROW_Y[2] + 0.22, "CPU 한도에서 기다려요 (limits.cpu)")
        tag(ax, ROW_Y[2] - 0.3, "메모리 한도를 넘어 죽었어요 (limits.memory)")
        moral(ax, 6.0, 0.35, "예약은 노드를 고르고 한도는 넘을 때 벌어질 일을 정해요")


# ── 정리: 낱말 카드 ────────────────────────────────────────────────
def cards():
    fig, ax = canvas(6.4, 5.4, 9.8, 8.3)
    W, H = 4.6, 3.8

    def card(i, name, line):
        col, row = i % 2, i // 2
        x, y = 0.2 + col * 4.9, 4.25 - row * 4.05
        box(ax, x, y, W, H, fc="white")
        label(ax, x + 0.25, y + H - 0.4, name, fs=12.5, ha="left", bold=True)
        label(ax, x + W / 2, y + 0.6, line, fs=9.5, color=INK)
        return x, y

    x, y = card(0, "requests", "노드를 고를 때 더하는 예약\n이만큼 쓸 수 있게 자리를 맡아요")
    for k in range(4):
        cell(ax, x + 0.4 + k * 0.97, y + 1.55, 0.85, 0.75, "", hot=k < 2)
    label(ax, x + 1.32, y + 2.6, "예약", fs=10, color=RED, bold=True)
    x, y = card(1, "limits", "넘으면 막히는 한도\nCPU는 느려지고 메모리는 죽어요")
    for k in range(4):
        if k < 3:
            cell(ax, x + 0.4 + k * 0.97, y + 1.55, 0.85, 0.75, "")
        else:
            empty(ax, x + 0.4 + k * 0.97, y + 1.55, 0.85, 0.75)
    vline(ax, x + 0.4 + 3 * 0.97 - 0.06, y + 1.35, y + 2.55)
    x, y = card(2, "스로틀", "CPU 한도를 넘으면\n다음 조각까지 기다리게 하는 일")
    label(ax, x + 1.35, y + 2.95, "조각 1", fs=9, color=INK)
    label(ax, x + 3.05, y + 2.95, "조각 2", fs=9, color=INK)
    for r in range(3):
        cell(ax, x + 0.6, y + 2.35 - r * 0.42, 1.5, 0.36, "", fs=8)
    empty(ax, x + 0.6, y + 2.35 - 3 * 0.42, 1.5, 0.36, ec=RED)
    cell(ax, x + 2.3, y + 2.35 - 3 * 0.42, 1.5, 0.36, "", hot=True)
    x, y = card(3, "OOM 킬", "메모리 한도를 넘은 프로세스를\n커널이 끝내는 일")
    for k in range(3):
        cell(ax, x + 0.4 + k * 1.0, y + 1.55, 0.9, 0.75, "")
    cross(ax, x + 0.5, y + 1.6, x + 3.2, y + 2.25, lw=3)
    save(fig, OUT, "k8s10-cards.svg")


if __name__ == "__main__":
    S, L = (7.2, 3.8), (12, 6.6)
    stage(opening, 3, OUT, "k8s10-open", S, L)
    stage(sched, 3, OUT, "k8s10-sched", S, L)
    stage(over, 3, OUT, "k8s10-over", S, L)
    stage(cpu, 3, OUT, "k8s10-cpu", S, L)
    stage(mem, 3, OUT, "k8s10-mem", S, L)
    decide()
    stage(back, 2, OUT, "k8s10-back", S, L)
    cards()
