"""쿠버네티스 4편 그림 만들기. 실행: python lab/fig_k8s04.py  → docs/kubernetes/img/04/*.svg

그림 안 글씨는 낱말과 숫자만 둔다. 문장은 본문과 그림 설명에 둔다(쉬운글-정책 5장).
예시는 동네 빵집 주문 앱. 컴퓨터 한 대(건물)에 컨테이너 셋(칸막이 사무실): 주문 화면, 주문 처리, 주문 장부.
아래층 공용 관리실이 커널이다.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "es"))
from figkit import (INK, LIGHT, NOTE, PAPER, PINK, RED, arrow, box, bubble,  # noqa: E402
                    canvas, cell, label, outdir, save)
from matplotlib.patches import Rectangle  # noqa: E402

OUT = outdir("04", topic="kubernetes")
ROOMS = ["주문 화면", "주문 처리", "주문 장부"]
RX = [0.7, 3.15, 5.6]          # 사무실 왼쪽 x
RW, RY, RH = 2.3, 3.2, 1.9     # 사무실 폭, 아래 y, 높이
KX, KY, KW, KH = 0.7, 0.9, 7.2, 1.35  # 관리실(커널)
WIN = (4.4, 2.25)             # 관리실 창구(시스템 호출 받는 곳) 위쪽 가운데


def make(draw, name, y0, y1):
    """가로 0~12, 세로 y0~y1 만 남겨 그린다. 그림마다 글씨 크기가 같게 가로 폭을 고정한다."""
    fig, ax = canvas(7.2, 0.6 * (y1 - y0), 12, y1)
    ax.set_ylim(y0, y1)
    ax.add_patch(Rectangle((0, y0), 12, y1 - y0, fill=False, ec="none"))
    draw(ax)
    save(fig, OUT, name)


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


# ── 그림 1. 컨테이너 목록과 기록 ───────────────────────────────────
LINES = [("주문 화면", "실행 중"), ("주문 처리", "실행 중"), ("주문 장부", "실행 중")]


def fig_open(ax):
    box(ax, 0.4, 1.3, 11.2, 5.05, fc="#1f2329", ec=INK, round_=False)
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
    label(ax, 0.8, 2.45, "주문 화면: 수상한 접속", fs=11, ha="left", color="#ff8a66", bold=True)
    label(ax, 0.8, 1.85, "주문 장부: 장부 파일 읽음 ← 주문 화면 쪽 프로세스", fs=11, ha="left",
          color="#ff8a66", bold=True)


# ── 그림 2. 칸막이 사무실과 공용 관리실 ─────────────────────────────
def fig_office(ax):
    building(ax, kernel_hot=True)
    for k in range(3):
        arrow(ax, (room_mid(k), RY - 0.05), (WIN[0] + (k - 1) * 0.4, KY + KH + 0.12), color=RED, ms=11, lw=1.6)


# ── 그림 3. 시스템 호출 ──────────────────────────────────────────────
def fig_syscall(ax):
    building(ax, note=False, room_hot=(2,))
    disk(ax, hot=True)
    note_paper(ax, 8.6, 4.6, "열기: 장부 파일", w=2.8)
    arrow(ax, (6.0, RY - 0.05), (WIN[0] + 0.4, KY + KH + 0.14), color=RED, ms=12)
    label(ax, 4.6, 2.85, "① 부탁", fs=10, color=RED, bold=True)
    arrow(ax, (KX + KW + 0.05, KY + 0.6), (8.95, 1.4), color=RED, ms=12)
    label(ax, 10.2, 2.3, "② 꺼내기", fs=10, color=RED, bold=True)
    arrow(ax, (7.4, KY + KH + 0.02), (7.4, RY - 0.05), color=RED, ms=12)
    label(ax, 7.55, 2.75, "③ 건네기", fs=10, color=RED, bold=True, ha="left")


# ── 그림 4. 관리실이 칸막이를 지켜요 ─────────────────────────────────
def fig_guard(ax):
    building(ax, note=False, room_hot=(0,))
    disk(ax)
    note_paper(ax, 8.6, 4.6, "열기: 장부 파일", w=2.8)
    arrow(ax, (room_mid(0), RY - 0.05), (WIN[0] - 0.5, KY + KH + 0.12), color=RED, ms=12)
    bubble(ax, 8.6, 2.9, 2.8, 0.9, "이 칸엔 없음", (KX + KW - 0.3, KY + KH - 0.2), hot=True, fs=10.5)
    label(ax, room_mid(0) - 0.7, RY - 0.35, "✗", fs=16, color=RED, bold=True)


# ── 그림 5·6. 관리실에 구멍이 나면 ───────────────────────────────────
def fig_escape1(ax):
    building(ax, note=False, kernel_broken=True, intruder=0)
    disk(ax)
    note_paper(ax, 8.6, 4.6, "이상하게 꾸민 부탁", w=2.8)
    arrow(ax, (room_mid(0), RY - 0.05), (WIN[0] - 0.5, KY + KH + 0.12), color=RED, ms=12)


def fig_escape2(ax):
    building(ax, note=False, kernel_broken=True, wall_broken=True, intruder=0, room_hot=(2,))
    disk(ax, hot=True)
    arrow(ax, (room_mid(0) + 0.5, RY + 0.3), (KX + 4.4, KY + 0.6), color=RED, ms=12, rad=0.2)
    arrow(ax, (KX + 5.1, KY + 0.6), (room_mid(2), RY + 0.3), color=RED, ms=12, rad=0.3)
    arrow(ax, (KX + KW + 0.05, KY + 0.6), (8.95, 1.4), color=RED, ms=12)
    label(ax, 10.2, 3.6, "모든 칸 열림", fs=11, color=RED, bold=True)


# ── 그림 7. 창구 좁히기: seccomp ─────────────────────────────────────
KINDS = ["열기", "읽기", "쓰기", "보내기", "시계", "모듈", "재부팅", "…"]


def fig_seccomp(ax):
    building(ax, note=False)
    label(ax, 8.6, 5.7, "seccomp 목록", fs=10, ha="left", bold=True, color=RED)
    for k, s in enumerate(KINDS):
        col, row = k % 2, k // 2
        x, y = 8.6 + col * 1.6, 4.85 - row * 0.75
        closed = s in ("모듈", "재부팅", "시계", "…")
        cell(ax, x, y, 1.45, 0.6, s, hot=not closed, dim=closed, fs=10)


# ── 그림 8. 고르는 길 ────────────────────────────────────────────────
def fig_decide(ax):
    box(ax, 0.3, 4.0, 5.0, 1.0, fc=NOTE)
    label(ax, 2.8, 4.5, "남이 만든 코드나 낯선 요청?", fs=10, bold=True)
    arrow(ax, (5.4, 4.5), (6.9, 4.5))
    label(ax, 6.15, 4.8, "아니요", fs=10, color=INK)
    box(ax, 7.0, 4.0, 4.7, 1.0, fc=PAPER)
    label(ax, 9.35, 4.5, "컨테이너 + seccomp", fs=10.5)
    arrow(ax, (2.8, 3.9), (2.8, 3.1), color=RED)
    label(ax, 3.0, 3.5, "예", fs=10, color=RED, ha="left")
    box(ax, 0.3, 2.0, 5.0, 1.0, fc=NOTE)
    label(ax, 2.8, 2.5, "커널 공격까지 막기?", fs=10.5, bold=True)
    arrow(ax, (5.4, 2.5), (6.9, 2.5))
    label(ax, 6.15, 2.8, "아니요", fs=10, color=INK)
    box(ax, 7.0, 2.0, 4.7, 1.0, fc=PAPER)
    label(ax, 9.35, 2.5, "컨테이너 + seccomp", fs=10.5)
    arrow(ax, (2.8, 1.9), (2.8, 1.3), color=RED)
    label(ax, 3.0, 1.6, "예", fs=10, color=RED, ha="left")
    box(ax, 0.3, 0.25, 5.0, 1.0, fc=PINK, ec=RED)
    label(ax, 2.8, 0.75, "칸마다 커널 따로 (5편·6편)", fs=10.5, color=RED, bold=True)


if __name__ == "__main__":
    make(fig_open, "k8s04-open-1.svg", 1.1, 6.5)
    make(fig_office, "k8s04-office-1.svg", 0.4, 6.7)
    make(fig_syscall, "k8s04-syscall-1.svg", 0.4, 6.7)
    make(fig_guard, "k8s04-guard-1.svg", 0.4, 6.7)
    make(fig_escape1, "k8s04-escape-1.svg", 0.4, 6.7)
    make(fig_escape2, "k8s04-escape-2.svg", 0.4, 6.7)
    make(fig_seccomp, "k8s04-seccomp-1.svg", 0.4, 6.7)
    make(fig_decide, "k8s04-decide.svg", 0, 5.2)
