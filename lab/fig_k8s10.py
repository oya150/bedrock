"""쿠버네티스 10편 그림 만들기. 실행: python lab/fig_k8s10.py  → docs/kubernetes/img/10/*.svg

그림 안 글씨는 낱말과 숫자만 둔다. 절마다 한두 장.
예시는 빵집 주문 앱의 주문 처리 파드. 매니페스트는 requests cpu 2 · memory 2Gi, limits cpu 3 · memory 3Gi.
노드 A·B는 CPU 4개씩. 노드 A에는 주문 장부(예약 2), 노드 B에는 주문 화면(1)과 다른 앱(2).
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "es"))
from figkit import (GREY, INK, LIGHT, PINK, RED, arrow, box,  # noqa: E402
                    canvas, cell, cylinder, label, outdir, save)
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


def opening():
    fig, ax = canvas(7.2, 3.8, 12, 6.6)
    rows = ROWS[:2] + [("주문 처리-1", OOM), ROWS[3]]
    podlist(ax, rows, hot=(2, 3))
    gauge(ax, "노드 A · CPU 4개", 4, 1, note="사용 중 1개")
    save(fig, OUT, "k8s10-open.svg")


# ── 스케줄러: 예약의 합으로 노드 고르기 ────────────────────────────
CW, CG = 0.85, 0.1
NODES = {"A": 0.3, "B": 4.6}
SCH = (9.6, 1.0, 2.0, 1.3)


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
    if step == 2:
        node(ax, "A", [("주문 장부", 2, False), ("주문 처리-1", 2, True)])
        node(ax, "B", [("화면", 1, False), ("다른 앱", 2, False)])
        box(ax, 0.3, 5.0, 4.6, 0.85, fc=LIGHT, ec=GREY)
        label(ax, 2.6, 5.42, "주문 처리-1 · 예약 CPU 2", fs=11, color=GREY)
        mark(ax, "A", True, "남은 칸 2")
        mark(ax, "B", False, "남은 칸 1", hot=False)
    else:
        node(ax, "A", [("주문 장부", 2, False), ("주문 처리-1", 2, False)], use=1)
        node(ax, "B", [("화면", 1, False), ("다른 앱", 2, False)])
        podcard(ax, "주문 처리-2 · 예약 CPU 2")
        mark(ax, "A", False, "남은 칸 0")
        mark(ax, "B", False, "남은 칸 1")
        label(ax, 2.6, 4.75, "Pending", fs=11, color=RED, bold=True)


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
    if step == 2:
        use = ["장부", "처리-1", "처리-1", "처리-1"]
        hot = (1,)
    else:
        use = ["장부", "장부", "처리-1", "처리-1"]
        hot = (0, 1, 2, 3)
    for k, u in enumerate(use):
        cell(ax, OX[k], 1.7, OW, 0.8, u, hot=(k in hot), fs=10.5)
    if step == 2:
        label(ax, 9.75, 2.1, "주문 처리-1\n예약 2 · 사용 3", fs=11, color=RED, bold=True)
    else:
        label(ax, 9.75, 2.1, "장부 2 · 처리 2", fs=11, color=RED, bold=True)


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
        label(ax, 9.8, 4.0, "끝: 조각 1", fs=11.5, color=RED, bold=True)
    else:
        ax.plot([2.85, 5.2], [2.88, 2.88], color=RED, lw=2.2, ls="--")
        label(ax, 7.55, 3.15, "한도 3", fs=10.5, ha="left", color=RED, bold=(step == 2))
        if step == 2:
            label(ax, 7.55, 2.47, "주문 4는 기다려요", fs=11, ha="left", color=RED, bold=True)
        else:
            label(ax, 7.55, 2.47, "끝: 조각 2", fs=11, ha="left", color=RED, bold=True)


# ── 메모리 한도: OOM 킬 ────────────────────────────────────────────
MW = 1.6
MX = [0.6 + k * (MW + 0.15) for k in range(4)]
KER = (9.4, 1.0, 2.2, 1.25)


def mem(ax, step):
    cylinder(ax, *KER, "커널")
    label(ax, 0.6, 4.45, "주문 처리-1의 메모리", fs=10.5, ha="left", bold=True)
    for k in range(4):
        if k < 3:
            cell(ax, MX[k], 3.0, MW, 1.0, "주문 자료", fs=10.5)
        elif k == 3 and step == 1:
            empty(ax, MX[k], 3.0, MW, 1.0, ec=RED)
            label(ax, MX[k] + MW / 2, 3.5, "하나 더", fs=10.5, color=RED)
        else:
            empty(ax, MX[k], 3.0, MW, 1.0)
    lx = MX[3] - 0.075
    vline(ax, lx, 2.8, 4.3)
    label(ax, lx - 0.1, 4.45, "한도 3Gi", fs=10, ha="right", color=RED, bold=True)
    if step == 2:
        cross(ax, MX[0] + 0.1, 3.05, MX[2] + MW - 0.1, 3.95, lw=4)
        label(ax, 3.2, 2.45, "OOM 킬", fs=13, color=RED, bold=True)
        arrow(ax, (9.35, 1.9), (5.0, 2.95), color=RED, ms=14)


def one(draw, step, name, size=(7.2, 3.8), lim=(12, 6.6)):
    fig, ax = canvas(*size, *lim)
    ax.add_patch(Rectangle((0, 0), *lim, fill=False, ec="none"))
    draw(ax, step)
    save(fig, OUT, name)


if __name__ == "__main__":
    opening()
    one(sched, 2, "k8s10-sched-1.svg")
    one(sched, 3, "k8s10-sched-2.svg")
    one(over, 2, "k8s10-over-1.svg")
    one(over, 3, "k8s10-over-2.svg")
    one(cpu, 1, "k8s10-cpu-1.svg")
    one(cpu, 3, "k8s10-cpu-2.svg")
    one(mem, 1, "k8s10-mem-1.svg")
    one(mem, 2, "k8s10-mem-2.svg")
