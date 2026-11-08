"""쿠버네티스 4편 그림 만들기. 실행: python lab/fig_k8s04.py  → docs/kubernetes/img/04/*.svg

본문 절은 장면 띠로 그린다: 같은 무대를 여러 장 그리고 장마다 바뀐 곳만 빨강으로 칠한다.
예시는 동네 빵집 주문 앱. 컴퓨터 한 대(건물)에 컨테이너 셋(칸막이 사무실): 주문 화면, 주문 처리, 주문 장부.
아래층 공용 관리실이 커널이다.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "es"))
from figkit import (GREY, INK, LIGHT, NOTE, PAPER, PINK, RED, arrow, box, bubble,  # noqa: E402
                    canvas, cell, label, moral, outdir, save, stage)
from matplotlib.patches import Rectangle  # noqa: E402

OUT = outdir("04", topic="kubernetes")
ROOMS = ["주문 화면", "주문 처리", "주문 장부"]
RX = [0.7, 3.15, 5.6]          # 사무실 왼쪽 x
RW, RY, RH = 2.3, 3.2, 1.9     # 사무실 폭, 아래 y, 높이
KX, KY, KW, KH = 0.7, 0.9, 7.2, 1.35  # 관리실(커널)
WIN = (4.4, 2.25)             # 관리실 창구(시스템 호출 받는 곳) 위쪽 가운데


def room_mid(k):
    return RX[k] + RW / 2


# ── 무대: 건물 한 채 = 컴퓨터 한 대 ───────────────────────────────
def building(ax, wall_hot=False, wall_broken=False, kernel_hot=False, kernel_broken=False,
             room_hot=(), intruder=None, note=True):
    ax.add_patch(Rectangle((0.4, 0.55), 7.8, 5.3, fc="white", ec=INK, lw=2.2))
    ax.add_patch(Rectangle((0.25, 5.85), 8.1, 0.2, fc=INK, ec=INK))
    label(ax, 4.3, 6.35, "건물 = 컴퓨터 한 대 (노드)", fs=10.5, bold=True, color=INK)
    for k, name in enumerate(ROOMS):
        on = k in room_hot
        box(ax, RX[k], RY, RW, RH, fc=PINK if on else NOTE, ec=RED if on else INK, lw=1.5, round_=False)
        label(ax, room_mid(k), RY + RH - 0.35, name, fs=11, bold=True, color=RED if on else "#222")
        label(ax, room_mid(k), RY + RH - 0.75, "컨테이너", fs=9, color=RED if on else INK)
    # 칸막이: 사무실 사이 굵은 벽
    for x in (RX[0] + RW + 0.07, RX[1] + RW + 0.07):
        ec = RED if (wall_hot or wall_broken) else INK
        ax.plot([x, x], [RY - 0.05, RY + RH + 0.05], color=ec, lw=4.5 if not wall_broken else 3,
                ls="--" if wall_broken else "-")
    if note:
        label(ax, 8.35, RY + RH - 0.3, "칸막이", fs=10, ha="left", color=RED if wall_hot else INK, bold=wall_hot)
        label(ax, 8.35, RY + RH - 0.7, "리눅스 네임스페이스\n· cgroup", fs=8.5, ha="left", va="top",
              color=RED if wall_hot else INK)
    kc = RED if (kernel_hot or kernel_broken) else INK
    box(ax, KX, KY, KW, KH, fc=PINK if kernel_hot else LIGHT, ec=kc, lw=2.0 if kernel_hot else 1.5, round_=False)
    label(ax, KX + 0.2, KY + KH - 0.3, "공용 관리실 · 커널", fs=11, ha="left", bold=True, color=kc)
    ax.add_patch(Rectangle((WIN[0] - 0.7, KY + KH - 0.05), 1.4, 0.12, fc="white", ec=kc, lw=1.4))
    label(ax, WIN[0], KY + KH - 0.3, "창구", fs=9, color=kc)
    if kernel_broken:
        label(ax, KX + 6.1, KY + 0.45, "✗ 버그", fs=13, color=RED, bold=True)
        ax.plot([KX + 4.5, KX + 4.9, KX + 4.6, KX + 5.0], [KY + 0.1, KY + 0.45, KY + 0.65, KY + 1.0], color=RED, lw=2.2)
    if intruder is not None:
        x = room_mid(intruder)
        label(ax, x, RY + 0.55, "침입자", fs=9.5, color="white", bold=True,
              bbox=dict(boxstyle="round,pad=0.25", fc=RED, ec=RED))


def note_paper(ax, x, y, s, hot=True, w=2.6):
    cell(ax, x, y, w, 0.55, s, hot=hot, fs=9.5, fc=PINK if hot else PAPER)


def disk(ax, hot=False):
    cell(ax, 9.0, 0.95, 2.4, 1.0, "디스크\n장부 파일", hot=hot, fs=10)


# ── 여는 장면: 컨테이너 목록 화면 ───────────────────────────────────
LINES = [("주문 화면", "실행 중"), ("주문 처리", "실행 중"), ("주문 장부", "실행 중")]


def terminal(ax, logs=(), log_hot=()):
    box(ax, 0.4, 0.75, 11.2, 5.6, fc="#1f2329", ec=INK, round_=False)
    ax.add_patch(Rectangle((0.4, 5.95), 11.2, 0.4, fc="#3a3f47", ec=INK, lw=1.2))
    for k, c in enumerate(("#e4572e", "#f6c445", "#8fb58f")):
        ax.add_patch(Rectangle((0.6 + k * 0.35, 6.07), 0.18, 0.18, fc=c, ec="none"))
    label(ax, 6.0, 6.15, "노드 1 · 컨테이너 목록", fs=10, color="#ddd")
    label(ax, 0.8, 5.55, "이름", fs=10.5, ha="left", color="#9aa")
    label(ax, 3.6, 5.55, "상태", fs=10.5, ha="left", color="#9aa")
    for k, (n, s) in enumerate(LINES):
        y = 5.0 - k * 0.5
        label(ax, 0.8, y, n, fs=11.5, ha="left", color="#eee")
        label(ax, 3.6, y, s, fs=11.5, ha="left", color="#8fb58f")
    ax.plot([0.7, 11.3], [3.3, 3.3], color="#555", lw=1)
    label(ax, 0.8, 3.0, "기록", fs=10.5, ha="left", color="#9aa")
    for k, s in enumerate(logs):
        on = k in log_hot
        label(ax, 0.8, 2.5 - k * 0.55, s, fs=11, ha="left", color="#ff8a66" if on else "#bbb", bold=on)


def opening(ax, step):
    if step == 1:
        terminal(ax)
        moral(ax, 6.0, 0.3, "컴퓨터 한 대에서 컨테이너 셋이 돌아요", fs=11.5)
    elif step == 2:
        terminal(ax, ["주문 화면: 수상한 접속이 들어왔어요"], log_hot=(0,))
    else:
        terminal(ax, ["주문 화면: 수상한 접속이 들어왔어요",
                      "주문 장부: 주문 화면 쪽 프로세스가 장부 파일을 읽었어요"], log_hot=(1,))
        moral(ax, 6.0, 0.3, "칸막이가 있는데 침입자가 장부까지 갔어요", fs=11.5)


# ── 칸막이 사무실과 공용 관리실 ────────────────────────────────────
def office(ax, step):
    building(ax, wall_hot=(step == 1), kernel_hot=(step == 2))
    if step == 1:
        label(ax, 10.1, 2.4, "칸마다 보이는 것과\n쓸 수 있는 양을\n나눠요", fs=10, color=RED)
    else:
        for k in range(3):
            arrow(ax, (room_mid(k), RY - 0.05), (WIN[0] + (k - 1) * 0.4, KY + KH + 0.12), color=RED, ms=11, lw=1.6)
        label(ax, 10.1, 1.55, "셋 다 같은\n관리실을 써요", fs=10.5, color=RED, bold=True)
        moral(ax, 4.3, 0.2, "칸막이는 나눠도 관리실은 하나예요")


# ── 시스템 호출: 무엇을 하든 관리실 창구에 부탁해요 ─────────────────
def syscall(ax, step):
    building(ax, note=False, room_hot=(2,) if step == 1 else ())
    disk(ax, hot=(step == 2))
    if step == 1:
        note_paper(ax, 8.5, 4.6, "장부 파일 열어 주세요", w=3.1)
        arrow(ax, (room_mid(2), RY - 0.05), (WIN[0] + 0.5, KY + KH + 0.12), color=RED, ms=12)
        label(ax, 8.5, 4.0, "주문 장부가 창구에 부탁", fs=9.5, ha="left", color=RED)
    elif step == 2:
        arrow(ax, (KX + KW + 0.05, KY + 0.6), (8.95, 1.4), color=RED, ms=12)
        arrow(ax, (WIN[0] + 0.7, KY + KH + 0.15), (room_mid(2) + 0.4, RY - 0.05), color=RED, ms=12, rad=-0.2)
        label(ax, 10.2, 2.35, "관리실이 꺼내 줘요", fs=10, color=RED)
    else:
        for k in range(3):
            arrow(ax, (room_mid(k), RY - 0.05), (WIN[0] + (k - 1) * 0.4, KY + KH + 0.12), color=RED, ms=11, lw=1.6)
        label(ax, 10.2, 4.6, "파일 읽기\n네트워크 보내기\n메모리 받기", fs=10, color=RED)
        label(ax, 10.2, 3.4, "모두 창구로", fs=10.5, color=RED, bold=True)
        moral(ax, 4.3, 0.2, "프로그램은 무엇을 하든 커널에 부탁해요")


# ── 관리실이 칸막이를 지켜요 ─────────────────────────────────────────
def guard(ax, step):
    building(ax, note=False, room_hot=(0,) if step == 1 else ())
    disk(ax)
    if step == 1:
        note_paper(ax, 8.5, 4.6, "장부 파일 열어 주세요", w=3.1)
        arrow(ax, (room_mid(0), RY - 0.05), (WIN[0] - 0.5, KY + KH + 0.12), color=RED, ms=12)
        label(ax, 8.5, 4.0, "주문 화면이 같은 부탁", fs=9.5, ha="left", color=RED)
    else:
        bubble(ax, 8.4, 3.4, 3.4, 1.1, "그 파일은 당신 칸에\n없어요", (KX + KW - 0.3, KY + KH - 0.2), hot=True, fs=10.5)
        label(ax, room_mid(0), RY - 0.35, "✗", fs=16, color=RED, bold=True)
        moral(ax, 4.3, 0.2, "칸막이는 관리실이 지키는 규칙이에요")


# ── 관리실에 구멍이 나면: 컨테이너 탈출 ─────────────────────────────
def escape(ax, step):
    building(ax, note=False, kernel_broken=(step >= 2), wall_broken=(step == 3), intruder=0)
    disk(ax, hot=(step == 3))
    if step == 1:
        note_paper(ax, 8.5, 4.6, "이상하게 꾸민 부탁", w=3.1)
        arrow(ax, (room_mid(0), RY - 0.05), (WIN[0] - 0.5, KY + KH + 0.12), color=RED, ms=12)
        label(ax, 8.5, 4.0, "버그를 건드리는 쪽지", fs=9.5, ha="left", color=RED)
    elif step == 2:
        bubble(ax, 8.4, 3.4, 3.4, 1.1, "어? 규칙을\n지킬 수가 없어요", (KX + KW - 0.3, KY + KH - 0.2), hot=True, fs=10.5)
    else:
        arrow(ax, (room_mid(0) + 0.5, RY + 0.3), (KX + 4.4, KY + 0.6), color=RED, ms=12, rad=0.2)
        arrow(ax, (KX + 5.1, KY + 0.6), (room_mid(2), RY + 0.3), color=RED, ms=12, rad=0.3)
        arrow(ax, (KX + KW + 0.05, KY + 0.6), (8.95, 1.4), color=RED, ms=12)
        label(ax, 10.2, 3.4, "모든 칸이\n열렸어요", fs=11, color=RED, bold=True)
        moral(ax, 4.3, 0.2, "관리실이 뚫리면 칸막이 전체가 뚫려요")


# ── 창구 좁히기: seccomp ─────────────────────────────────────────────
KINDS = ["열기", "읽기", "쓰기", "보내기", "시계", "모듈", "재부팅", "…"]


def seccomp(ax, step):
    building(ax, note=False)
    label(ax, 8.6, 5.7, "창구가 받는 부탁 종류", fs=10, ha="left", bold=True)
    for k, s in enumerate(KINDS):
        col, row = k % 2, k // 2
        x, y = 8.6 + col * 1.6, 4.85 - row * 0.75
        closed = step == 2 and s in ("모듈", "재부팅", "시계", "…")
        cell(ax, x, y, 1.45, 0.6, s, hot=(step == 2 and not closed), dim=closed, fs=10)
        if closed:
            label(ax, x + 1.25, y + 0.3, "✗", fs=11, color=GREY)
    if step == 2:
        label(ax, 10.2, 1.6, "쓰는 것만 열어 둬요\n(seccomp)", fs=10, color=RED, bold=True)
        moral(ax, 4.3, 0.2, "창구는 좁혀도 관리실은 여전히 하나예요")


# ── 언제 쓸모 있을까요: 갈림길 ──────────────────────────────────────
def decide():
    fig, ax = canvas(7.4, 4.4, 15, 9)
    box(ax, 3.0, 7.4, 9.0, 1.1, fc=NOTE)
    label(ax, 7.5, 7.95, "이 컴퓨터에서 남이 만든 코드도 돌리나요?", fs=11, bold=True)
    arrow(ax, (4.5, 7.3), (2.8, 6.0)); label(ax, 3.2, 6.8, "아니요", fs=10, color=INK)
    box(ax, 0.3, 4.3, 5.4, 1.6, fc=PAPER)
    label(ax, 3.0, 5.1, "컨테이너 칸막이로 충분해요\n창구는 좁혀 둬요(seccomp)", fs=10.5)
    arrow(ax, (10.5, 7.3), (11.6, 6.0), color=RED); label(ax, 11.6, 6.8, "예", fs=10, color=RED)
    box(ax, 8.6, 4.3, 6.1, 1.6, fc=NOTE)
    label(ax, 11.65, 5.1, "그 코드가 커널 버그를 노려도\n괜찮나요?", fs=10.5, bold=True)
    arrow(ax, (10.3, 4.2), (8.6, 2.9)); label(ax, 8.6, 3.7, "괜찮아요", fs=10, color=INK)
    box(ax, 5.2, 1.3, 4.3, 1.5, fc=PAPER)
    label(ax, 7.35, 2.05, "컨테이너로 돌려요", fs=10.5)
    arrow(ax, (13.0, 4.2), (13.0, 2.9), color=RED); label(ax, 13.3, 3.55, "안 돼요", fs=10, color=RED, ha="left")
    box(ax, 10.0, 0.4, 4.8, 2.4, fc=PINK, ec=RED)
    label(ax, 12.4, 1.6, "커널을 따로 주는\n방법을 써요\n(5편 microVM, 6편)", fs=10.5, color=RED, bold=True)
    save(fig, OUT, "k8s04-decide.svg")


# ── 정리: 처음 장면으로 돌아가기 ───────────────────────────────────
def back(ax, step):
    if step == 1:
        building(ax, note=False, intruder=0)
        disk(ax)
        label(ax, 10.2, 4.3, "처음 장면:\n침입자가\n장부까지 갔어요", fs=10.5, color=INK)
    else:
        building(ax, note=False, kernel_broken=True, intruder=0)
        disk(ax, hot=True)
        arrow(ax, (room_mid(0) + 0.5, RY + 0.3), (KX + 4.4, KY + 0.6), color=RED, ms=12, rad=0.2)
        arrow(ax, (KX + KW + 0.05, KY + 0.6), (8.95, 1.4), color=RED, ms=12)
        label(ax, 10.2, 4.3, "벽을 넘은 게\n아니에요\n아래 관리실로\n돌아갔어요", fs=10.5, color=RED, bold=True)
        moral(ax, 4.3, 0.2, "칸막이 아래에 커널 하나가 있었어요")


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

    x, y = card(0, "커널", "하드웨어를 나눠 주는\n운영체제의 중심 (관리실)")
    for k in range(3):
        cell(ax, x + 0.4 + k * 1.3, y + 2.25, 1.15, 0.55, ROOMS[k][-2:], fs=9.5)
    cell(ax, x + 0.4, y + 1.4, 3.75, 0.6, "커널 하나", hot=True, fs=10)
    x, y = card(1, "시스템 호출", "프로그램이 커널에\n일을 부탁하는 창구")
    cell(ax, x + 0.4, y + 1.8, 1.7, 0.7, "주문 장부", fc=NOTE, fs=10)
    arrow(ax, (x + 2.2, y + 2.15), (x + 2.8, y + 2.15), color=RED, ms=11)
    cell(ax, x + 2.9, y + 1.8, 1.3, 0.7, "커널", hot=True, fs=10)
    x, y = card(2, "컨테이너 탈출", "커널 버그로 칸막이 밖\n다른 칸·컴퓨터에 닿는 일")
    for k in range(3):
        cell(ax, x + 0.4 + k * 1.3, y + 2.25, 1.15, 0.55, ROOMS[k][-2:], hot=(k != 1), fs=9.5)
    cell(ax, x + 0.4, y + 1.4, 3.75, 0.6, "✗ 버그", hot=True, fs=10)
    x, y = card(3, "seccomp", "쓸 수 있는 시스템 호출\n종류를 줄이는 장치")
    for k, s in enumerate(["열기", "읽기", "모듈", "재부팅"]):
        cell(ax, x + 0.3 + k * 1.02, y + 1.8, 0.95, 0.6, s, hot=k < 2, dim=k >= 2, fs=9)
    save(fig, OUT, "k8s04-cards.svg")


if __name__ == "__main__":
    S, L = (7.2, 3.8), (12, 6.6)
    stage(opening, 3, OUT, "k8s04-open", S, L)
    stage(office, 2, OUT, "k8s04-office", S, L)
    stage(syscall, 3, OUT, "k8s04-syscall", S, L)
    stage(guard, 2, OUT, "k8s04-guard", S, L)
    stage(escape, 3, OUT, "k8s04-escape", S, L)
    stage(seccomp, 2, OUT, "k8s04-seccomp", S, L)
    decide()
    stage(back, 2, OUT, "k8s04-back", S, L)
    cards()
