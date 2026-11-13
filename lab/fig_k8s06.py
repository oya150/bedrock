"""쿠버네티스 6편 그림 만들기. 실행: python lab/fig_k8s06.py  → docs/kubernetes/img/06/*.svg

갈래 공통 무대(건물·창)는 1편 그림의 모양과 같다. 1편 생성기가 바뀌어도 이 편 그림이 흔들리지 않게
필요한 도우미(window·building)를 이 파일에 옮겨 두었다.
대표 비유는 민원 창구 대리인: 컨테이너와 관리실(커널) 사이에 gVisor가 서서 부탁을 대신 받는다.
그림 안 글씨는 낱말과 숫자만 둔다. 문장은 본문과 그림 설명에 있다.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "es"))
from figkit import (GREY, INK, LIGHT, NOTE, PAPER, PINK, RED, arrow, box,  # noqa: E402
                    canvas, cell, label, outdir, save)
from matplotlib.patches import Circle, Rectangle  # noqa: E402

OUT = outdir("06", topic="kubernetes")
PARTS = ["주문 화면", "주문 처리", "주문 장부"]
S, L = (7.2, 3.8), (12, 6.6)


# ── 공통 무대 (1편과 같은 모양) ───────────────────────────────────
def window(ax, x, y, w, h, title):
    ax.add_patch(Rectangle((x, y), w, h, fc="white", ec=INK, lw=1.4))
    ax.add_patch(Rectangle((x, y + h - 0.45), w, 0.45, fc=LIGHT, ec=INK, lw=1.2))
    for k in range(3):
        ax.add_patch(Circle((x + 0.22 + k * 0.22, y + h - 0.225), 0.06, fc=GREY, ec="none"))
    label(ax, x + 0.95, y + h - 0.225, title, fs=10, ha="left", color=INK)


def building(ax, x, y, w, h, rooms, kern_hot=False, kern="공용 관리실 · 커널"):
    """건물 한 채. 칸 가운데 (x, y) 목록을 돌려준다."""
    ax.add_patch(Rectangle((x, y), w, h, fc="white", ec=INK, lw=2.2))
    ax.add_patch(Rectangle((x - 0.15, y + h), w + 0.3, 0.2, fc=INK, ec=INK))
    label(ax, x + w / 2, y + h + 0.48, "건물 = 컴퓨터 한 대", fs=10.5, color=INK, bold=True)
    kc = RED if kern_hot else INK
    ax.add_patch(Rectangle((x + 0.15, y + 0.15), w - 0.3, 0.6, fc=PINK if kern_hot else LIGHT, ec=kc,
                           lw=1.8 if kern_hot else 1.2))
    label(ax, x + w / 2, y + 0.45, kern, fs=10.5, color=kc, bold=kern_hot)
    n = len(rooms)
    top, bot = y + h - 0.15, y + 0.9
    rw = (w - 0.3) / n
    centers = []
    for k, r in enumerate(rooms):
        rx = x + 0.15 + k * rw
        cx, cy = rx + rw / 2, (top + bot) / 2 + 0.6
        centers.append((cx, cy))
        ax.add_patch(Rectangle((rx + 0.05, bot), rw - 0.1, top - bot, fc=NOTE, ec=INK, lw=1.2))
        cw = min(1.6, rw - 0.25)
        cell(ax, cx - cw / 2, cy - 0.28, cw, 0.56, r, fs=10.5)
    for k in range(1, n):
        wx = x + 0.15 + k * rw
        ax.plot([wx, wx], [bot - 0.05, top], color=INK, lw=3.2, solid_capstyle="butt")
    return centers


def crack(ax, x, y):
    ax.plot([x, x + 0.25, x + 0.05, x + 0.3], [y - 0.25, y, y + 0.1, y + 0.35], color=RED, lw=2.2)


def one(draw, name, size=S, lim=L):
    fig, ax = canvas(*size, *lim)
    draw(ax)
    save(fig, OUT, name)


# ── 1. 파드 목록 창 ──────────────────────────────────────────────
def opening(ax):
    window(ax, 0.6, 1.3, 10.8, 4.2, "파드 목록")
    label(ax, 1.0, 4.55, "이름", fs=10, ha="left", color=INK)
    label(ax, 5.0, 4.55, "띄우는 방식", fs=10, ha="left", color=INK)
    ax.plot([0.85, 11.15], [4.3, 4.3], color=INK, lw=0.8)
    kinds = ["?", "컨테이너 (기본)", "컨테이너 (기본)"]
    for k, (p, kind) in enumerate(zip(PARTS, kinds)):
        y = 3.7 - k * 0.9
        on = k == 0
        if on:
            ax.add_patch(Rectangle((0.8, y - 0.32), 10.4, 0.64, fc=PINK, ec=RED, lw=1.5))
        c = RED if on else "#222"
        label(ax, 1.0, y, p, fs=11.5, ha="left", color=c, bold=on)
        label(ax, 5.0, y, kind, fs=11.5 if not on else 14, ha="left", color=c, bold=on)


# ── 2·3. 부탁이 곧장 커널로 / 대리인을 거쳐서 ─────────────────────
BX, BY, BW, BH = 1.0, 0.8, 7.2, 4.6


def proxy_direct(ax):
    cs = building(ax, BX, BY, BW, BH, PARTS, kern_hot=True)
    cx, cy = cs[0]
    arrow(ax, (cx, cy - 0.35), (cx, BY + 0.8), color=RED, ms=13)
    label(ax, cx + 0.2, BY + 2.1, "시스템\n호출", fs=10, ha="left", color=RED, bold=True)


def proxy_gvisor(ax):
    cs = building(ax, BX, BY, BW, BH, PARTS)
    cx, cy = cs[0]
    x, y = BX + 0.3, BY + 1.35
    box(ax, x, y, 2.0, 0.65, fc=PINK, ec=RED, lw=1.8)
    label(ax, x + 1.0, y + 0.33, "gVisor", fs=10.5, color=RED, bold=True)
    arrow(ax, (cx, cy - 0.35), (x + 1.0, y + 0.72), color=RED, ms=12)
    label(ax, cx + 0.2, cy - 0.8, "시스템\n호출", fs=9.5, ha="left", color=RED)
    arrow(ax, (x + 1.0, y - 0.03), (x + 1.0, BY + 0.78), color=INK, ms=10, lw=1.3)


# ── 4. 사용자 공간 커널 ───────────────────────────────────────────
def userspace(ax):
    ax.add_patch(Rectangle((0.4, 3.3), 11.2, 2.8, fc="white", ec=INK, lw=1.4))
    label(ax, 0.6, 5.8, "사용자 공간 · 보통 프로그램 자리", fs=10.5, ha="left", bold=True, color=INK)
    ax.add_patch(Rectangle((0.4, 0.9), 11.2, 2.2, fc=LIGHT, ec=INK, lw=1.4))
    label(ax, 0.6, 2.8, "커널 공간 · 컴퓨터 전체를 다루는 자리", fs=10.5, ha="left", bold=True, color=INK)
    cell(ax, 4.6, 1.3, 3.0, 0.8, "커널", fs=11)
    cell(ax, 0.8, 4.6, 2.2, 0.7, "주문 화면", fc=NOTE, fs=10.5)
    box(ax, 3.7, 3.65, 3.6, 1.0, fc=PINK, ec=RED, lw=1.8)
    label(ax, 5.65, 4.15, "gVisor", fs=11, color=RED, bold=True)
    arrow(ax, (3.0, 4.8), (3.65, 4.3), color=GREY, ms=11)
    cell(ax, 8.4, 4.6, 2.6, 0.7, "다른 프로그램", fc=NOTE, fs=10.5)
    crack(ax, 3.85, 4.05)
    arrow(ax, (5.5, 3.6), (6.1, 2.15), color=RED, ms=12)
    label(ax, 6.35, 2.75, "✗", fs=16, color=RED, bold=True)
    arrow(ax, (7.35, 4.15), (8.35, 4.8), color=RED, ms=12)
    label(ax, 7.95, 4.75, "✗", fs=14, color=RED, bold=True)


# ── 5. 부탁 하나에 한 번 더 ───────────────────────────────────────
def cost(ax):
    label(ax, 0.4, 6.0, "파일 하나 읽기", fs=11, ha="left", bold=True)
    label(ax, 0.4, 5.0, "컨테이너", fs=10.5, ha="left", color=INK)
    cell(ax, 2.6, 4.7, 2.0, 0.6, "주문 화면", fc=NOTE, fs=10)
    arrow(ax, (4.7, 5.0), (5.6, 5.0), color=GREY, ms=11)
    cell(ax, 5.7, 4.7, 1.6, 0.6, "커널", fc=LIGHT, fs=10)
    label(ax, 0.4, 3.2, "gVisor", fs=10.5, ha="left", color=RED, bold=True)
    cell(ax, 2.6, 2.9, 2.0, 0.6, "주문 화면", fc=NOTE, fs=10)
    arrow(ax, (4.7, 3.2), (5.6, 3.2), color=RED, ms=11)
    cell(ax, 5.7, 2.9, 1.8, 0.6, "gVisor", hot=True, fs=10)
    arrow(ax, (7.6, 3.2), (8.5, 3.2), color=RED, ms=11)
    cell(ax, 8.6, 2.9, 1.6, 0.6, "커널", fc=LIGHT, fs=10)
    label(ax, 6.6, 2.4, "+1번", fs=11, color=RED, bold=True)


# ── 6. 세 방법 표 ────────────────────────────────────────────────
def table():
    fig, ax = canvas(7.4, 3.6, 15, 7.2)
    cols = ["", "컨테이너", "gVisor", "microVM"]
    rows = [("커널", ["같이 씀", "대리인이 막음", "집마다 따로"]),
            ("부탁마다 드는 시간", ["짧음", "길어짐", "집 안에선 짧음"]),
            ("그대로 도는 프로그램", ["거의 다", "일부 안 됨", "거의 다\n(특별 장치 빼고)"]),
            ("더 드는 메모리", ["거의 없음", "조금", "커널 하나만큼"])]
    weak = {(0, 0), (1, 1), (2, 1), (3, 2)}
    xs = [0.2, 4.0, 7.6, 11.2]
    ws = [3.7, 3.5, 3.5, 3.6]
    for j, c in enumerate(cols):
        if c:
            label(ax, xs[j] + ws[j] / 2, 6.9, c, fs=11.5, bold=True)
    for i, (name, vals) in enumerate(rows):
        y = 5.2 - i * 1.4
        cell(ax, xs[0], y, ws[0], 1.2, name, fc=LIGHT, fs=10.5)
        for j, v in enumerate(vals):
            cell(ax, xs[j + 1], y, ws[j + 1] - 0.1, 1.2, v, hot=(i, j) in weak, fs=10)
    save(fig, OUT, "k8s06-table.svg")


# ── 7·8. RuntimeClass ────────────────────────────────────────────
def paper(ax, x, y, w, h, title, lines, hot=False):
    box(ax, x, y, w, h, fc="white", ec=RED if hot else INK, lw=1.8 if hot else 1.3, round_=False)
    label(ax, x + 0.2, y + h - 0.35, title, fs=10.5, ha="left", bold=True, color=RED if hot else "#222")
    for k, s in enumerate(lines):
        label(ax, x + 0.3, y + h - 0.95 - k * 0.5, s, fs=10.5, ha="left", color=RED if hot else "#222",
              bold=hot, family="monospace")


def node_box(ax, hot=None, kubelet=False):
    box(ax, 7.6, 0.6, 4.1, 5.1, fc="white", round_=False)
    label(ax, 9.65, 6.1, "노드", fs=10.5, bold=True, color=INK)
    label(ax, 9.65, 4.8, "kubelet", fs=10.5, color=RED if kubelet else INK, bold=kubelet)
    for k, (h, d) in enumerate([("runc", "기본 컨테이너"), ("runsc", "gVisor"), ("kata", "microVM")]):
        y = 3.6 - k * 0.95
        on = hot == h
        cell(ax, 7.9, y, 1.5, 0.7, h, hot=on, fs=10)
        label(ax, 9.6, y + 0.35, d, fs=10, ha="left", color=RED if on else INK)


def rc_class(ax):
    paper(ax, 0.3, 3.4, 3.4, 2.6, "RuntimeClass", ["name: gvisor", "handler: runsc"], hot=True)
    node_box(ax, hot="runsc")
    arrow(ax, (3.8, 4.2), (7.85, 2.98), color=RED, ms=12, rad=-0.1)


def rc_pod(ax):
    paper(ax, 0.3, 3.4, 3.4, 2.6, "RuntimeClass", ["name: gvisor", "handler: runsc"])
    paper(ax, 0.3, 0.6, 3.9, 2.5, "주문 화면 파드", ["runtimeClassName:", "  gvisor"], hot=True)
    node_box(ax, hot="runsc", kubelet=True)
    arrow(ax, (2.0, 3.15), (2.0, 3.35), color=RED, ms=11)
    arrow(ax, (4.3, 1.8), (7.85, 2.98), color=RED, ms=12, rad=0.1)


# ── 9. 갈림길 ────────────────────────────────────────────────────
def decide():
    fig, ax = canvas(7.4, 4.4, 15, 9)
    box(ax, 3.5, 7.4, 8.0, 1.1, fc=NOTE)
    label(ax, 7.5, 7.95, "커널 앞 벽이 더 필요?", fs=11.5, bold=True)
    arrow(ax, (4.5, 7.3), (2.8, 6.0)); label(ax, 3.2, 6.8, "아니요", fs=10, color=INK)
    box(ax, 0.6, 4.6, 4.4, 1.3, fc=PAPER)
    label(ax, 2.8, 5.25, "기본 컨테이너", fs=11)
    arrow(ax, (10.5, 7.3), (11.6, 6.0), color=RED); label(ax, 11.6, 6.8, "예", fs=10, color=RED)
    box(ax, 9.0, 4.6, 5.4, 1.3, fc=NOTE)
    label(ax, 11.7, 5.25, "gVisor에서 잘 돌까?", fs=11, bold=True)
    arrow(ax, (10.3, 4.5), (8.6, 3.0), color=RED); label(ax, 8.9, 3.9, "예", fs=10, color=RED)
    box(ax, 5.0, 1.4, 4.2, 1.4, fc=PINK, ec=RED)
    label(ax, 7.1, 2.1, "gVisor", fs=11.5, color=RED, bold=True)
    arrow(ax, (13.0, 4.5), (13.0, 2.9)); label(ax, 13.3, 3.7, "아니요", fs=10, color=INK, ha="left")
    box(ax, 10.6, 1.4, 4.1, 1.4, fc=PAPER)
    label(ax, 12.65, 2.1, "microVM", fs=11.5)
    save(fig, OUT, "k8s06-decide.svg")


if __name__ == "__main__":
    one(opening, "k8s06-open-1.svg", lim=(12, 5.8))
    one(proxy_direct, "k8s06-proxy-1.svg")
    one(proxy_gvisor, "k8s06-proxy-2.svg")
    one(userspace, "k8s06-user-1.svg")
    one(cost, "k8s06-cost-1.svg")
    table()
    one(rc_class, "k8s06-rc-1.svg")
    one(rc_pod, "k8s06-rc-2.svg")
    decide()
