"""쿠버네티스 16편 그림 만들기. 실행: python lab/fig_k8s16.py  → docs/kubernetes/img/16/*.svg

본문 절은 장면 띠로 그린다: 같은 무대를 여러 장 그리고 장마다 바뀐 곳만 빨강으로 칠한다.
예시는 빵집 주문 앱의 주문 처리(자바). 새 파드는 주문 처리-3.
클래스 다섯: 주문접수, 메뉴판, 결제, 장부연결, 영수증. 자주 불리는 메서드는 주문받기. 난수 상태 예시 값은 42.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "es"))
from figkit import (GREY, INK, LIGHT, NOTE, PAPER, PINK, RED, arrow, box, bubble,  # noqa: E402
                    canvas, cylinder, label, moral, outdir, save, stage)
from matplotlib.patches import Rectangle  # noqa: E402

OUT = outdir("16", topic="kubernetes")
CLASSES = ["주문접수", "메뉴판", "결제", "장부연결", "영수증"]


def empty(ax, x, y, w, h, ec=GREY):
    ax.add_patch(Rectangle((x, y), w, h, fc="white", ec=ec, lw=1.2, ls="--"))


def chip(ax, x, y, w, h, s, hot=False, dim=False, fs=10):
    box(ax, x, y, w, h, fc=PINK if hot else (LIGHT if dim else NOTE), ec=RED if hot else (GREY if dim else INK),
        lw=1.8 if hot else 1.3)
    label(ax, x + w / 2, y + h / 2, s, fs=fs, color=RED if hot else (GREY if dim else "#222"), bold=hot)


def cross(ax, x0, y0, x1, y1, color=RED, lw=2.5):
    ax.plot([x0, x1], [y0, y1], color=color, lw=lw)
    ax.plot([x0, x1], [y1, y0], color=color, lw=lw)


def bar(ax, x, y, name, length, hot=False, dim=False, note=None):
    label(ax, x - 0.1, y, name, fs=9.5, ha="right", color=RED if hot else (GREY if dim else INK))
    ax.add_patch(Rectangle((x, y - 0.17), length, 0.34, fc=PINK if hot else (LIGHT if not dim else "white"),
                           ec=RED if hot else (GREY if dim else INK), lw=1.6 if hot else 1.0))
    if note:
        label(ax, x + length + 0.15, y, note, fs=9, ha="left", color=RED if hot else INK)


# ── 파드 목록 + 처리한 주문 ─────────────────────────────────────────
ROW_Y = [4.75 - k * 0.85 for k in range(3)]
ROWS = [("주문 처리-1", "실행 중"), ("주문 처리-2", "실행 중"), ("주문 처리-3", "준비 중")]
RUN = ROWS[:2] + [("주문 처리-3", "실행 중")]


def podlist(ax, rows, hot=(), dim=()):
    box(ax, 0.3, 1.1, 6.4, 5.25, fc="white", round_=False)
    ax.add_patch(Rectangle((0.3, 5.9), 6.4, 0.45, fc=LIGHT, ec=INK, lw=1.2))
    label(ax, 0.5, 6.12, "빵집 주문 앱 · 파드 목록", fs=11, ha="left", color=INK)
    label(ax, 0.55, 5.45, "이름", fs=10, ha="left", color=INK)
    label(ax, 3.0, 5.45, "상태", fs=10, ha="left", color=INK)
    ax.plot([0.5, 6.5], [5.2, 5.2], color=INK, lw=1.0)
    for k, (n, s) in enumerate(rows):
        y = ROW_Y[k]
        on, off = k in hot, k in dim
        if on:
            ax.add_patch(Rectangle((0.45, y - 0.3), 6.1, 0.6, fc=PINK, ec=RED, lw=1.8))
        else:
            ax.plot([0.5, 6.5], [y - 0.34, y - 0.34], color=GREY, lw=0.8)
        c = RED if on else (GREY if off else "#222")
        label(ax, 0.55, y, n, fs=10.5, ha="left", color=c, bold=on)
        label(ax, 3.0, y, s, fs=10.5, ha="left", color=c, bold=on)


def orders(ax, bars, corner=None, msg=None):
    box(ax, 7.1, 1.1, 4.7, 4.15, fc="white")
    label(ax, 7.3, 4.95, "주문 처리-3이 처리한 주문", fs=10, ha="left", color=INK)
    label(ax, 7.3, 4.55, "막대 = 걸린 시간", fs=8.5, ha="left", color=GREY)
    for k, b in enumerate(bars):
        y = 3.95 - k * 0.6
        if b is None:
            label(ax, 8.0, y, "⋮", fs=11, color=INK)
            continue
        n, ln, hot = b
        bar(ax, 8.4, y, n, ln, hot=hot)
    if msg:
        label(ax, 9.45, 3.0, msg, fs=10.5, color=RED, bold=True)
    if corner:
        label(ax, 9.45, 6.05, corner, fs=12, color=INK, bold=True)


def opening(ax, step):
    if step == 1:
        podlist(ax, ROWS, hot=(2,))
        orders(ax, [], "막 띄웠을 때", msg="아직 주문을 못 받아요")
    elif step == 2:
        podlist(ax, RUN, hot=(2,))
        orders(ax, [("주문 1", 3.0, True), ("주문 2", 2.6, False)], "한참 뒤")
    else:
        podlist(ax, RUN)
        orders(ax, [("주문 1", 3.0, False), ("주문 2", 2.6, False), None, ("주문 30", 0.6, False),
                    ("주문 31", 0.5, True)], "더 뒤")
        moral(ax, 6.0, 0.45, "떠도 한동안 느리다가 빨라져요")


# ── 클래스 찾고 읽고 검사하기 ──────────────────────────────────────
JVM = (9.7, 0.9, 2.0, 1.15)
SAY = (6.2, 4.75, 5.6, 1.2)
TAIL = (10.7, 2.75)
CARD_Y = [3.75 - k * 0.62 for k in range(5)]


def jar(ax, hot=()):
    box(ax, 0.3, 0.9, 3.6, 4.9, fc=PAPER)
    label(ax, 2.1, 5.45, "주문 처리 묶음 (JAR)", fs=10.5, bold=True)
    for k, c in enumerate(CLASSES):
        chip(ax, 0.6, 4.4 - k * 0.62, 3.0, 0.5, c, hot=(k in hot), fs=10)
    label(ax, 2.1, 1.2, "⋮", fs=12, color=INK)


def card(ax, k, hot=False, check=True):
    chip(ax, 5.0, CARD_Y[k], 3.0, 0.5, CLASSES[k] + ("  ✓" if check else ""), hot=hot, fs=10)


def load(ax, step):
    cylinder(ax, *JVM, "JVM")
    if step == 1:
        jar(ax, hot=(0,))
        bubble(ax, *SAY, "주문접수 클래스가 필요해요\n묶음에서 찾아요", TAIL, hot=True, fs=10.5)
    elif step == 2:
        jar(ax)
        arrow(ax, (3.7, 4.65), (4.9, CARD_Y[0] + 0.25), color=RED, ms=13)
        card(ax, 0, hot=True)
        label(ax, 6.5, CARD_Y[0] - 0.3, "✓ 규칙 검사", fs=9.5, color=RED)
        bubble(ax, *SAY, "읽어서 규칙을 지키는지\n검사해요", TAIL, hot=True, fs=10.5)
    else:
        jar(ax)
        for k in range(5):
            card(ax, k, hot=(k > 0))
        bubble(ax, *SAY, "클래스마다\n찾고 읽고 검사해요", TAIL, hot=True, fs=10.5)
        moral(ax, 6.0, 0.35, "시작할 때는 이 일을 클래스 수만큼 되풀이해요")


# ── JIT 워밍업 ─────────────────────────────────────────────────────
def jit(ax, step):
    chip(ax, 0.3, 5.3, 3.0, 0.65, "주문받기", hot=(step == 2), fs=10.5)
    box(ax, 0.3, 3.4, 3.6, 1.35, fc=PAPER)
    label(ax, 2.1, 4.07, "해석기\n한 줄씩 풀어 실행", fs=10)
    arrow(ax, (1.8, 5.25), (1.8, 4.85), color=INK, ms=11)
    box(ax, 5.0, 3.4, 2.2, 1.35, fc=PINK if step == 2 else NOTE, ec=RED if step == 2 else INK)
    label(ax, 6.1, 4.07, "JIT", fs=12, color=RED if step == 2 else "#222", bold=True)
    if step >= 2:
        chip(ax, 8.3, 3.4, 2.6, 1.35, "기계어", hot=(step == 2), fs=11.5)
        c = RED if step == 2 else GREY
        arrow(ax, (4.0, 4.07), (4.9, 4.07), color=c, ms=13)
        arrow(ax, (7.3, 4.07), (8.2, 4.07), color=c, ms=13)
    else:
        empty(ax, 8.3, 3.4, 2.6, 1.35)
    label(ax, 0.3, 2.75, "주문에 걸린 시간", fs=10, ha="left", color=INK, bold=True)
    bar(ax, 1.4, 2.2, "주문 1", 5.2, hot=(step == 1))
    bar(ax, 1.4, 1.65, "주문 2", 4.8)
    if step == 1:
        label(ax, 9.6, 1.95, "처음에는 한 줄씩\n풀어서 실행해요", fs=10.5, color=RED, bold=True)
    elif step == 2:
        label(ax, 3.5, 5.62, "자주 불려요", fs=10.5, ha="left", color=RED, bold=True)
        label(ax, 9.6, 5.5, "자주 쓰는 것만\nCPU 말로 번역해 둬요", fs=10.5, color=RED, bold=True)
    else:
        bar(ax, 1.4, 1.1, "주문 31", 0.9, hot=True, note="기계어로 바로 실행")
        moral(ax, 6.0, 0.4, "번역이 끝나면 같은 주문이 금방 끝나요")


# ── AppCDS ─────────────────────────────────────────────────────────
FILE = (5.0, 2.7, 2.1, 1.4)


def cds(ax, step):
    tdim = step >= 2
    box(ax, 0.3, 1.0, 4.0, 4.9, fc="white", ec=GREY if tdim else INK)
    label(ax, 2.3, 5.55, "연습 실행 · JVM", fs=10.5, bold=True, color=GREY if tdim else "#222")
    for k, c in enumerate(CLASSES):
        chip(ax, 0.6, 4.6 - k * 0.65, 3.4, 0.5, c, dim=tdim, fs=10)
    chip(ax, *FILE, "클래스\n묶음 파일", hot=(step == 1), fs=10.5)
    arrow(ax, (4.4, 3.4), (4.95, 3.4), color=RED if step == 1 else GREY, ms=12)
    box(ax, 7.8, 1.0, 4.0, 4.9, fc="white")
    label(ax, 9.8, 5.55, "새 파드 · JVM", fs=10.5, bold=True)
    if step == 1:
        label(ax, 6.0, 0.45, "끝날 때 읽고 검사한 클래스를 파일로 적어요", fs=11, color=RED, bold=True)
        return
    arrow(ax, (7.2, 3.4), (7.75, 3.4), color=RED if step == 2 else GREY, ms=12)
    label(ax, 9.8, 5.1, "찾기 · 읽기 · 검사", fs=9.5, color=GREY)
    ax.plot([8.65, 10.95], [5.1, 5.1], color=GREY, lw=1.5)
    for k, c in enumerate(CLASSES):
        r, col = k // 2, k % 2
        chip(ax, 8.05 + col * 1.8, 4.15 - r * 0.6, 1.65, 0.48, c, hot=(step == 2), fs=9.5)
    if step == 2:
        label(ax, 6.0, 0.45, "찾고 읽고 검사하는 일을 건너뛰어요", fs=11, color=RED, bold=True)
    else:
        bar(ax, 8.9, 2.1, "주문 1", 2.6, hot=True)
        bar(ax, 8.9, 1.5, "주문 2", 2.3)
        moral(ax, 6.0, 0.45, "읽고 검사하는 시간은 줄지만 예열은 남아요")


# ── 체크포인트·복원 ────────────────────────────────────────────────
CPF = (5.0, 0.95, 2.3, 1.3)
INSIDE = ["클래스", "기계어", "장부 연결", "주문 자료"]


def proc(ax, x, title, items, hot=False, dim=False, extra=None):
    box(ax, x, 2.6, 4.0, 3.3, fc="white", ec=GREY if dim else (RED if hot else INK))
    label(ax, x + 2.0, 5.55, title, fs=10.5, bold=True, color=GREY if dim else (RED if hot else "#222"))
    for k, s in enumerate(items):
        r, c = k // 2, k % 2
        chip(ax, x + 0.25 + c * 1.85, 4.35 - r * 0.85, 1.65, 0.6, s, hot=hot, dim=dim, fs=9.5)
    if extra:
        label(ax, x + 2.0, 2.95, extra, fs=10, color=RED, bold=True)


def crac(ax, step):
    if step == 1:
        proc(ax, 0.3, "다 데워진 주문 처리", INSIDE)
        chip(ax, *CPF, "체크포인트\n파일", hot=True, fs=10.5)
        arrow(ax, (3.0, 2.55), (4.95, 1.75), color=RED, ms=14)
        box(ax, 7.8, 2.6, 4.0, 3.3, fc="white", ec=GREY)
        label(ax, 9.8, 5.55, "새 파드", fs=10.5, color=GREY)
        label(ax, 9.6, 1.5, "그 순간의 메모리를\n통째로 파일에 적어요", fs=10.5, color=RED, bold=True)
    else:
        proc(ax, 0.3, "다 데워진 주문 처리", INSIDE, dim=True)
        chip(ax, *CPF, "체크포인트\n파일", fs=10.5)
        arrow(ax, (7.35, 1.75), (9.2, 2.55), color=RED, ms=14)
        proc(ax, 7.8, "새 파드 · 실행 중", ["클래스", "기계어", "주문 자료"], hot=True)
        moral(ax, 6.0, 0.4, "읽기 · 검사 · 예열을 건너뛰고 이어서 달려요")


# ── 통째로 저장할 때 걸리는 것 ─────────────────────────────────────
CX = [0.75, 2.4, 4.05, 5.7]
DB = (9.4, 3.3, 2.0, 1.1)


def catch(ax, step):
    box(ax, 0.5, 3.2, 7.0, 2.1, fc=PAPER)
    label(ax, 0.75, 4.95, "체크포인트 파일", fs=10.5, ha="left", bold=True)
    for k, s in enumerate(["클래스", "기계어", "장부 연결", "난수 42"]):
        if k == 2 and step == 2:
            empty(ax, CX[k], 3.5, 1.5, 1.0)
            continue
        chip(ax, CX[k], 3.5, 1.5, 1.0, s, hot=(k == 2 and step == 1) or (k == 3 and step == 3), fs=10)
    if step == 1:
        label(ax, CX[2] + 0.75, 2.95, "✗ 되살릴 수 없어요", fs=9.5, color=RED, bold=True)
    cylinder(ax, *DB, "주문 장부")
    if step == 1:
        bubble(ax, 7.6, 5.45, 4.2, 1.0, "그 연결은 벌써 잊었어요", (10.4, 5.15), hot=True, fs=10.5)
        moral(ax, 4.0, 2.35, "열린 연결은 저장해도 되살릴 수 없어요")
    elif step == 2:
        label(ax, 0.5, 2.55, "① 저장 전에 연결을 닫아요", fs=11, ha="left", color=RED, bold=True)
        label(ax, 5.0, 2.55, "② 복원 뒤에 다시 열어요", fs=11, ha="left", color=RED, bold=True)
    else:
        for k, x in enumerate([0.5, 4.3, 8.1]):
            box(ax, x, 0.75, 3.3, 1.2, fc="white")
            label(ax, x + 1.65, 1.65, f"주문 처리-{k + 3}", fs=10, bold=True)
            chip(ax, x + 0.85, 0.9, 1.6, 0.48, "난수 42", hot=True, fs=9.5)
            arrow(ax, (4.0, 3.15), (x + 1.65, 2.0), color=GREY, ms=11, lw=1.4)
        moral(ax, 6.0, 0.3, "같은 파일에서 되살리면 난수도 다 같아요")


# ── 판단 (한 장) ───────────────────────────────────────────────────
def decide():
    fig, ax = canvas(10, 5.0, 15, 7.4)
    box(ax, 0.3, 6.0, 6.6, 1.0, fc=NOTE)
    label(ax, 3.6, 6.5, "파드가 자주 새로 뜨고 그때마다\n기다림이 문제인가요?", fs=10.5, bold=True)
    arrow(ax, (7.0, 6.5), (8.4, 6.5)); label(ax, 7.7, 6.8, "아니요", fs=10, color=INK)
    box(ax, 8.5, 6.0, 6.2, 1.0, fc=PAPER)
    label(ax, 11.6, 6.5, "그대로 둬요", fs=10.5)
    arrow(ax, (3.6, 5.9), (3.6, 5.2)); label(ax, 3.9, 5.55, "예", fs=10, color=INK, ha="left")
    box(ax, 0.3, 4.15, 6.6, 1.0, fc=PAPER)
    label(ax, 3.6, 4.65, "AppCDS부터 써요\n(프로그램 코드는 그대로)", fs=10.5)
    arrow(ax, (3.6, 4.05), (3.6, 3.35))
    box(ax, 0.3, 2.3, 6.6, 1.0, fc=NOTE)
    label(ax, 3.6, 2.8, "예열까지 건너뛰어야 하나요?", fs=10.5, bold=True)
    arrow(ax, (7.0, 2.8), (8.4, 2.8)); label(ax, 7.7, 3.1, "아니요", fs=10, color=INK)
    box(ax, 8.5, 2.3, 6.2, 1.0, fc=PAPER)
    label(ax, 11.6, 2.8, "AppCDS로 충분해요", fs=10.5)
    arrow(ax, (3.6, 2.2), (3.6, 1.5), color=RED); label(ax, 3.9, 1.85, "예", fs=10, color=RED, ha="left")
    box(ax, 0.3, 0.1, 6.6, 1.3, fc=PINK, ec=RED)
    label(ax, 3.6, 0.75, "체크포인트·복원 (CRaC)\n연결 · 난수 손질과 권한이 필요해요", fs=10.5, color=RED, bold=True)
    save(fig, OUT, "k8s16-decide.svg")


# ── 정리: 처음 장면으로 돌아가기 ───────────────────────────────────
def back(ax, step):
    if step == 1:
        podlist(ax, ROWS, dim=(0, 1, 2))
        orders(ax, [], "처음")
    elif step == 2:
        podlist(ax, RUN, hot=(2,))
        orders(ax, [("주문 1", 3.0, False), ("주문 2", 2.6, False)], "AppCDS")
    else:
        podlist(ax, RUN, hot=(2,))
        orders(ax, [("주문 1", 0.6, True), ("주문 2", 0.5, True)], "체크포인트·복원")
        moral(ax, 6.0, 0.45, "저장해 둔 상태에서 이어 가면 처음부터 빨라요")


# ── 정리: 낱말 카드 ────────────────────────────────────────────────
def cards():
    fig, ax = canvas(6.4, 5.4, 9.8, 8.3)
    W, H = 4.6, 3.8

    def cardbox(i, name, line):
        col, row = i % 2, i // 2
        x, y = 0.2 + col * 4.9, 4.25 - row * 4.05
        box(ax, x, y, W, H, fc="white")
        label(ax, x + 0.25, y + H - 0.4, name, fs=12, ha="left", bold=True)
        label(ax, x + W / 2, y + 0.6, line, fs=9, color=INK)
        return x, y

    x, y = cardbox(0, "클래스 읽기", "클래스를 묶음에서 찾고 읽고\n규칙을 검사하는 일")
    chip(ax, x + 0.3, y + 1.6, 1.4, 0.75, "JAR", fs=10)
    arrow(ax, (x + 1.8, y + 1.97), (x + 2.4, y + 1.97), color=RED, ms=11)
    chip(ax, x + 2.5, y + 1.6, 1.8, 0.75, "주문접수 ✓", hot=True, fs=9.5)
    x, y = cardbox(1, "JIT", "자주 쓰는 부분을 실행 도중에\n기계어로 번역하는 부품")
    chip(ax, x + 0.3, y + 1.6, 1.6, 0.75, "주문받기", fs=9.5)
    arrow(ax, (x + 2.0, y + 1.97), (x + 2.6, y + 1.97), color=RED, ms=11)
    chip(ax, x + 2.7, y + 1.6, 1.6, 0.75, "기계어", hot=True, fs=10)
    x, y = cardbox(2, "AppCDS", "읽고 검사한 클래스를 파일로 저장해\n다음 시작 때 바로 불러오는 기능")
    chip(ax, x + 0.3, y + 1.55, 1.5, 0.9, "묶음\n파일", hot=True, fs=9.5)
    for k in range(5):
        chip(ax, x + 2.1 + (k % 3) * 0.75, y + 2.05 - (k // 3) * 0.5, 0.65, 0.4, "", fs=8)
    x, y = cardbox(3, "체크포인트·복원", "돌고 있는 상태를 저장하고\n거기서 이어 가는 일")
    chip(ax, x + 0.25, y + 1.6, 1.15, 0.75, "프로세스", fs=8.5)
    arrow(ax, (x + 1.45, y + 1.97), (x + 1.75, y + 1.97), color=RED, ms=10)
    chip(ax, x + 1.8, y + 1.6, 1.0, 0.75, "파일", hot=True, fs=9)
    arrow(ax, (x + 2.85, y + 1.97), (x + 3.15, y + 1.97), color=RED, ms=10)
    chip(ax, x + 3.2, y + 1.6, 1.15, 0.75, "새 파드", hot=True, fs=8.5)
    save(fig, OUT, "k8s16-cards.svg")


if __name__ == "__main__":
    S, L = (7.2, 3.8), (12, 6.6)
    stage(opening, 3, OUT, "k8s16-open", S, L)
    stage(load, 3, OUT, "k8s16-load", S, L)
    stage(jit, 3, OUT, "k8s16-jit", S, L)
    stage(cds, 3, OUT, "k8s16-cds", S, L)
    stage(crac, 2, OUT, "k8s16-crac", S, L)
    stage(catch, 3, OUT, "k8s16-catch", S, L)
    decide()
    stage(back, 3, OUT, "k8s16-back", S, L)
    cards()
