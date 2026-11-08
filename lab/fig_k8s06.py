"""쿠버네티스 6편 그림 만들기. 실행: python lab/fig_k8s06.py  → docs/kubernetes/img/06/*.svg

본문 절은 장면 띠로 그린다: 같은 무대를 여러 장 그리고 장마다 바뀐 곳만 빨강으로 칠한다.
갈래 공통 무대(건물·창)는 1편 생성기(fig_k8s01)의 모양을 그대로 쓴다.
대표 비유는 민원 창구 대리인: 컨테이너와 관리실(커널) 사이에 gVisor가 서서 부탁을 대신 받는다.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "es"))
sys.path.insert(0, os.path.dirname(__file__))
from figkit import (GREY, INK, LIGHT, NOTE, PAPER, PINK, RED, arrow, box, bubble,  # noqa: E402
                    canvas, cell, label, moral, outdir, save, stage)
from fig_k8s01 import building, window  # noqa: E402
from matplotlib.patches import Rectangle  # noqa: E402

OUT = outdir("06", topic="kubernetes")
PARTS = ["주문 화면", "주문 처리", "주문 장부"]


def crack(ax, x, y):
    ax.plot([x, x + 0.25, x + 0.05, x + 0.3], [y - 0.25, y, y + 0.1, y + 0.35], color=RED, lw=2.2)


# ── 여는 장면: 파드 목록 창 ─────────────────────────────────────────
def podlist(ax, kinds, hot=(), title="파드 목록"):
    window(ax, 0.6, 1.3, 10.8, 4.9, title)
    label(ax, 1.0, 5.25, "이름", fs=10, ha="left", color=INK)
    label(ax, 5.0, 5.25, "띄우는 방식", fs=10, ha="left", color=INK)
    ax.plot([0.85, 11.15], [5.0, 5.0], color=INK, lw=0.8)
    for k, (p, kind) in enumerate(zip(PARTS, kinds)):
        y = 4.4 - k * 0.9
        on = k in hot
        if on:
            ax.add_patch(Rectangle((0.8, y - 0.32), 10.4, 0.64, fc=PINK, ec=RED, lw=1.5))
        c = RED if on else "#222"
        label(ax, 1.0, y, p, fs=11.5, ha="left", color=c, bold=on)
        label(ax, 5.0, y, kind, fs=11.5, ha="left", color=c, bold=on)


def opening(ax, step):
    if step == 1:
        podlist(ax, ["컨테이너 (기본)"] * 3)
        label(ax, 6.0, 0.7, "세 파드 모두 같은 방식으로 떠요", fs=11, color=INK)
    elif step == 2:
        podlist(ax, ["microVM?", "컨테이너 (기본)", "컨테이너 (기본)"], hot=(0,))
        label(ax, 6.0, 0.7, "주문 화면만 더 단단하게, 그런데 microVM은 파드마다 커널이 하나 더", fs=10.5, color=RED)
    else:
        podlist(ax, ["?", "컨테이너 (기본)", "컨테이너 (기본)"], hot=(0,))
        moral(ax, 6.0, 0.7, "그 사이 방법은 없을까요? 파드마다 어떻게 고를까요?", fs=11.5)


# ── 대리인: 부탁을 대신 받아요 ───────────────────────────────────────
BX, BY, BW, BH = 1.0, 0.8, 7.2, 4.6


def proxy_box(ax, hot=False, broken=False):
    x, y = BX + 0.3, BY + 1.05
    box(ax, x, y, 2.0, 0.65, fc=PINK if hot else NOTE, ec=RED if (hot or broken) else INK, lw=1.8 if hot else 1.3)
    label(ax, x + 1.0, y + 0.33, "대리인 gVisor", fs=9.5, color=RED if (hot or broken) else "#222", bold=hot)
    return x + 1.0, y


def proxy(ax, step):
    cs = building(ax, BX, BY, BW, BH, PARTS, kern="공용 관리실 · 커널", kern_hot=(step == 1))
    cx, cy = cs[0]
    if step == 1:
        arrow(ax, (cx, cy - 0.35), (cx, BY + 0.8), color=RED, ms=13)
        label(ax, 10.0, 3.6, "부탁이 곧장\n커널로 가요 (4편)", fs=10.5, color=RED)
        return
    px, py = proxy_box(ax, hot=(step == 2))
    arrow(ax, (cx, cy - 0.35), (px, py + 0.7), color=RED if step == 2 else GREY, ms=12)
    if step == 2:
        label(ax, 10.0, 3.0, "대리인이 부탁을\n받아서 직접 처리해요", fs=10.5, color=RED, bold=True)
    else:
        arrow(ax, (px, py - 0.05), (px, BY + 0.8), color=RED, ms=11, lw=1.4)
        label(ax, 10.0, 3.0, "커널에는\n꼭 필요한 몇 가지만", fs=10.5, color=RED, bold=True)
        moral(ax, 4.6, 0.2, "커널에 닿는 부탁이 줄어요")


# ── 사용자 공간 커널 ───────────────────────────────────────────────
def layers(ax, gv_hot=False, broken=False, block=False):
    ax.add_patch(Rectangle((0.4, 3.3), 11.2, 2.8, fc="white", ec=INK, lw=1.4))
    label(ax, 0.6, 5.8, "사용자 공간 · 보통 프로그램이 도는 자리", fs=10.5, ha="left", bold=True, color=INK)
    ax.add_patch(Rectangle((0.4, 0.9), 11.2, 2.2, fc=LIGHT, ec=INK, lw=1.4))
    label(ax, 0.6, 2.8, "커널 공간 · 컴퓨터 전체를 다루는 자리", fs=10.5, ha="left", bold=True, color=INK)
    cell(ax, 4.6, 1.3, 3.0, 0.8, "커널", fs=11)
    cell(ax, 0.8, 4.6, 2.2, 0.7, "주문 화면", fc=NOTE, fs=10.5)
    ec = RED if (gv_hot or broken) else INK
    box(ax, 3.7, 3.65, 3.6, 1.0, fc=PINK if gv_hot else NOTE, ec=ec, lw=1.8 if gv_hot else 1.3)
    label(ax, 5.65, 4.15, "gVisor (커널 일을 해요)", fs=10.5, color=ec, bold=gv_hot)
    arrow(ax, (3.0, 4.8), (3.65, 4.3), color=GREY, ms=11)
    cell(ax, 8.4, 4.6, 2.6, 0.7, "다른 프로그램", fc=NOTE, fs=10.5)
    if broken:
        crack(ax, 3.78, 4.05)


def userspace(ax, step):
    layers(ax, gv_hot=(step == 1), broken=(step == 2))
    if step == 1:
        label(ax, 9.7, 3.85, "커널 일을 하지만\n보통 프로그램 자리에서", fs=9.5, color=RED, bold=True)
    else:
        arrow(ax, (5.5, 3.6), (6.1, 2.15), color=RED, ms=12)
        label(ax, 6.35, 2.75, "✗", fs=16, color=RED, bold=True)
        arrow(ax, (7.35, 4.15), (8.35, 4.8), color=RED, ms=12)
        label(ax, 7.95, 4.75, "✗", fs=14, color=RED, bold=True)
        label(ax, 9.7, 3.85, "뚫려도 보통\n프로그램 권한뿐", fs=9.5, color=RED, bold=True)
        moral(ax, 6.0, 0.4, "침입자는 아직 진짜 커널 밖에 있어요")


# ── 치르는 값: 느려지고, 못 알아듣는 부탁이 있어요 ─────────────────
def cost(ax, step):
    if step == 1:
        label(ax, 0.4, 6.0, "파일 하나 읽기", fs=11, ha="left", bold=True)
        label(ax, 0.4, 5.2, "컨테이너", fs=10.5, ha="left", color=INK)
        cell(ax, 2.6, 4.9, 2.0, 0.6, "주문 화면", fc=NOTE, fs=10)
        arrow(ax, (4.7, 5.2), (5.6, 5.2), color=GREY, ms=11)
        cell(ax, 5.7, 4.9, 1.6, 0.6, "커널", fc=LIGHT, fs=10)
        label(ax, 0.4, 3.6, "gVisor", fs=10.5, ha="left", color=RED, bold=True)
        cell(ax, 2.6, 3.3, 2.0, 0.6, "주문 화면", fc=NOTE, fs=10)
        arrow(ax, (4.7, 3.6), (5.6, 3.6), color=RED, ms=11)
        cell(ax, 5.7, 3.3, 1.8, 0.6, "gVisor", hot=True, fs=10)
        arrow(ax, (7.6, 3.6), (8.5, 3.6), color=RED, ms=11)
        cell(ax, 8.6, 3.3, 1.6, 0.6, "커널", fc=LIGHT, fs=10)
        label(ax, 6.0, 2.4, "부탁마다 한 번 더 거쳐요", fs=11, color=RED, bold=True)
    else:
        cell(ax, 0.6, 3.8, 2.4, 0.7, "주문 화면", fc=NOTE, fs=10.5)
        cell(ax, 3.4, 3.9, 3.0, 0.5, "드물게 쓰는 부탁", hot=True, fs=9.5)
        arrow(ax, (3.1, 4.15), (3.35, 4.15), color=RED, ms=10)
        arrow(ax, (6.5, 4.15), (7.3, 4.15), color=RED, ms=11)
        cell(ax, 7.4, 3.8, 1.8, 0.7, "gVisor", fc=NOTE, fs=10.5)
        bubble(ax, 7.0, 5.0, 4.4, 1.0, "그 부탁은 아직\n흉내 내지 못해요", (8.3, 4.55), hot=True, fs=10.5)
        label(ax, 8.3, 3.3, "✗", fs=16, color=RED, bold=True)
        moral(ax, 6.0, 1.8, "어떤 프로그램은 그대로는 돌지 않아요")


def table():
    fig, ax = canvas(7.4, 3.6, 15, 7.2)
    cols = ["", "컨테이너", "gVisor", "microVM"]
    rows = [("커널", ["모두 같이 써요", "대리인이 앞을 막아요", "집마다 따로"]),
            ("부탁마다 드는 시간", ["짧아요", "길어져요", "집 안에서는 짧아요"]),
            ("그대로 도는 프로그램", ["거의 다", "일부는 안 돌아요", "거의 다\n(특별 장치 빼고)"]),
            ("더 드는 메모리", ["거의 없어요", "조금", "커널 하나만큼"])]
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


# ── RuntimeClass: 파드마다 고르기 ───────────────────────────────────
def paper(ax, x, y, w, h, title, lines, hot=(), ec_hot=False):
    box(ax, x, y, w, h, fc="white", ec=RED if ec_hot else INK, lw=1.8 if ec_hot else 1.3, round_=False)
    label(ax, x + 0.2, y + h - 0.35, title, fs=10.5, ha="left", bold=True, color=RED if ec_hot else "#222")
    for k, s in enumerate(lines):
        on = k in hot
        label(ax, x + 0.3, y + h - 0.95 - k * 0.5, s, fs=10.5, ha="left", color=RED if on else "#222", bold=on,
              family="monospace")


def node_box(ax, hot=None):
    box(ax, 7.6, 0.6, 4.1, 5.1, fc="white", round_=False)
    label(ax, 9.65, 5.35, "노드 (컴퓨터 한 대)", fs=10.5, bold=True, color=INK)
    label(ax, 9.65, 4.8, "kubelet", fs=10.5, color=RED if hot else INK, bold=bool(hot))
    for k, (h, d) in enumerate([("runc", "기본 컨테이너"), ("runsc", "gVisor"), ("kata", "microVM")]):
        y = 3.6 - k * 0.95
        on = hot == h
        cell(ax, 7.9, y, 1.5, 0.7, h, hot=on, fs=10)
        label(ax, 9.6, y + 0.35, d, fs=10, ha="left", color=RED if on else INK)


def rc(ax, step):
    paper(ax, 0.3, 3.4, 3.4, 2.6, "RuntimeClass", ["name: gvisor", "handler: runsc"],
          hot=(0, 1) if step == 1 else (), ec_hot=(step == 1))
    node_box(ax, hot="runsc" if step == 3 else None)
    if step == 1:
        arrow(ax, (3.8, 4.2), (7.85, 2.98), color=RED, ms=12, rad=-0.1)
        label(ax, 5.6, 4.5, "노드의 runsc를\n gvisor라고 불러요", fs=10, color=RED)
        return
    paper(ax, 0.3, 0.6, 3.9, 2.5, "주문 화면 파드", ["runtimeClassName:", "  gvisor"], hot=(0, 1) if step == 2 else (),
          ec_hot=(step == 2))
    if step == 2:
        arrow(ax, (2.0, 3.15), (2.0, 3.35), color=RED, ms=11)
        label(ax, 5.9, 2.0, "이 파드는\ngvisor로\n띄워 주세요", fs=10, color=RED)
    else:
        arrow(ax, (4.3, 1.8), (7.85, 2.98), color=RED, ms=12, rad=0.1)
        label(ax, 6.0, 1.3, "runsc로 띄워요", fs=10, color=RED)
        moral(ax, 6.0, 0.15, "파드마다 띄우는 방식을 골라요")


# ── 언제 쓸모 있을까요: 갈림길 ──────────────────────────────────────
def decide():
    fig, ax = canvas(7.4, 4.4, 15, 9)
    box(ax, 2.5, 7.4, 10.0, 1.1, fc=NOTE)
    label(ax, 7.5, 7.95, "이 파드에 커널 앞 벽이 더 필요한가요?", fs=11, bold=True)
    arrow(ax, (4.5, 7.3), (2.8, 6.0)); label(ax, 3.2, 6.8, "아니요", fs=10, color=INK)
    box(ax, 0.3, 4.4, 5.4, 1.5, fc=PAPER)
    label(ax, 3.0, 5.15, "RuntimeClass 없이\n기본 컨테이너", fs=10.5)
    arrow(ax, (10.5, 7.3), (11.6, 6.0), color=RED); label(ax, 11.6, 6.8, "예", fs=10, color=RED)
    box(ax, 8.6, 4.4, 6.1, 1.5, fc=NOTE)
    label(ax, 11.65, 5.15, "프로그램이 gVisor에서\n그대로 잘 도나요?", fs=10.5, bold=True)
    arrow(ax, (10.3, 4.3), (8.6, 3.0), color=RED); label(ax, 8.9, 3.8, "예", fs=10, color=RED)
    box(ax, 4.4, 1.2, 5.2, 1.7, fc=PINK, ec=RED)
    label(ax, 7.0, 2.05, "gVisor\n(메모리를 덜 써요)", fs=10.5, color=RED, bold=True)
    arrow(ax, (13.0, 4.3), (13.0, 3.0)); label(ax, 13.3, 3.65, "아니요, 느리거나 안 돌아요", fs=9.5, color=INK, ha="left")
    box(ax, 10.2, 1.2, 4.5, 1.7, fc=PAPER)
    label(ax, 12.45, 2.05, "microVM\n(5편 Kata Containers)", fs=10.5)
    label(ax, 7.5, 0.4, "어느 쪽이든 파드에 runtimeClassName 한 줄로 골라요", fs=10.5, color=INK)
    save(fig, OUT, "k8s06-decide.svg")


# ── 정리: 처음 장면으로 돌아가기 ───────────────────────────────────
def back(ax, step):
    if step == 1:
        podlist(ax, ["?", "컨테이너 (기본)", "컨테이너 (기본)"])
        label(ax, 6.0, 0.7, "처음 장면: 주문 화면만 더 단단하게 하고 싶었어요", fs=11, color=INK)
    else:
        podlist(ax, ["gVisor (runtimeClassName: gvisor)", "컨테이너 (기본)", "컨테이너 (기본)"], hot=(0,))
        moral(ax, 6.0, 0.7, "한 줄로 주문 화면만 대리인 뒤에 세웠어요")


# ── 정리: 낱말 카드 ────────────────────────────────────────────────
def cards():
    fig, ax = canvas(6.4, 5.4, 9.8, 8.3)
    W, H = 4.6, 3.8

    def card(i, name, line):
        col, row = i % 2, i // 2
        x, y = 0.2 + col * 4.9, 4.3 - row * 4.05
        box(ax, x, y, W, H, fc="white")
        label(ax, x + 0.25, y + H - 0.4, name, fs=12.5, ha="left", bold=True)
        label(ax, x + W / 2, y + 0.6, line, fs=10, color=INK)
        return x, y

    x, y = card(0, "gVisor", "시스템 호출을 중간에서\n대신 받아 처리하는 대리인")
    cell(ax, x + 0.3, y + 1.8, 1.3, 0.6, "화면", fc=NOTE, fs=10)
    arrow(ax, (x + 1.65, y + 2.1), (x + 1.95, y + 2.1), color=RED, ms=10)
    cell(ax, x + 2.0, y + 1.8, 1.3, 0.6, "gVisor", hot=True, fs=9.5)
    arrow(ax, (x + 3.35, y + 2.1), (x + 3.6, y + 2.1), color=GREY, ms=9)
    cell(ax, x + 3.65, y + 1.8, 0.8, 0.6, "커널", fc=LIGHT, fs=8.5)
    x, y = card(1, "사용자 공간 커널", "보통 프로그램 자리에서\n커널 일을 하는 프로그램")
    cell(ax, x + 0.4, y + 2.15, 3.8, 0.55, "사용자 공간: gVisor", hot=True, fs=9.5)
    cell(ax, x + 0.4, y + 1.45, 3.8, 0.55, "커널 공간: 커널", fc=LIGHT, fs=9.5)
    x, y = card(2, "RuntimeClass", "노드의 실행 방식에\n이름을 붙인 문서")
    cell(ax, x + 0.4, y + 1.8, 1.7, 0.6, "gvisor", hot=True, fs=10)
    arrow(ax, (x + 2.2, y + 2.1), (x + 2.7, y + 2.1), color=RED, ms=10)
    cell(ax, x + 2.8, y + 1.8, 1.4, 0.6, "runsc", fc=NOTE, fs=10)
    x, y = card(3, "runtimeClassName", "파드가 띄우는 방식을\n고르는 한 줄")
    cell(ax, x + 0.3, y + 1.8, 4.0, 0.6, "runtimeClassName: gvisor", hot=True, fs=9)
    save(fig, OUT, "k8s06-cards.svg")


if __name__ == "__main__":
    S, L = (7.2, 3.8), (12, 6.6)
    stage(opening, 3, OUT, "k8s06-open", S, L)
    stage(proxy, 3, OUT, "k8s06-proxy", S, L)
    stage(userspace, 2, OUT, "k8s06-user", S, L)
    stage(cost, 2, OUT, "k8s06-cost", S, L)
    table()
    stage(rc, 3, OUT, "k8s06-rc", S, L)
    decide()
    stage(back, 2, OUT, "k8s06-back", S, L)
    cards()
