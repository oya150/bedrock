"""쿠버네티스 16편 그림 만들기. 실행: python lab/fig_k8s16.py  → docs/kubernetes/img/16/*.svg

한 절에 한두 장. 지금 볼 곳만 빨강, 그림 안 글씨는 낱말과 숫자만.
예시는 빵집 주문 앱의 주문 처리(자바). 새 파드는 주문 처리-3.
클래스 다섯: 주문접수, 메뉴판, 결제, 장부연결, 영수증. 자주 불리는 메서드는 주문받기. 난수 상태 예시 값은 42.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "es"))
from figkit import (GREY, INK, LIGHT, NOTE, PAPER, PINK, RED, arrow, box,  # noqa: E402
                    canvas, cylinder, label, outdir, save)
from matplotlib.patches import Rectangle  # noqa: E402

OUT = outdir("16", topic="kubernetes")
CLASSES = ["주문접수", "메뉴판", "결제", "장부연결", "영수증"]


def chip(ax, x, y, w, h, s, hot=False, dim=False, fs=10):
    box(ax, x, y, w, h, fc=PINK if hot else (LIGHT if dim else NOTE), ec=RED if hot else (GREY if dim else INK),
        lw=1.8 if hot else 1.3)
    label(ax, x + w / 2, y + h / 2, s, fs=fs, color=RED if hot else (GREY if dim else "#222"), bold=hot)


def bar(ax, x, y, name, length, hot=False, dim=False, note=None):
    label(ax, x - 0.1, y, name, fs=9.5, ha="right", color=RED if hot else (GREY if dim else INK))
    ax.add_patch(Rectangle((x, y - 0.17), length, 0.34, fc=PINK if hot else (LIGHT if not dim else "white"),
                           ec=RED if hot else (GREY if dim else INK), lw=1.6 if hot else 1.0))
    if note:
        label(ax, x + length + 0.15, y, note, fs=9, ha="left", color=RED if hot else INK)


# ── 공통 ───────────────────────────────────────────────────────────
S, L = (7.2, 3.8), (12, 6.6)


def one(draw, name):
    fig, ax = canvas(*S, *L)
    ax.add_patch(Rectangle((0, 0), *L, fill=False, ec="none"))
    draw(ax)
    save(fig, OUT, name)


# ── 그림 1: 파드 목록 + 처리한 주문 ─────────────────────────────────────────
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


def orders(ax, bars):
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


def opening(ax):
    podlist(ax, RUN)
    orders(ax, [("주문 1", 3.0, True), ("주문 2", 2.6, False), None, ("주문 30", 0.6, False),
                ("주문 31", 0.5, True)])


# ── 그림 2: 클래스 찾고 읽고 검사하기 ─────────────────────────────
JVM = (9.4, 0.9, 2.0, 1.15)
CARD_Y = [4.4 - k * 0.62 for k in range(5)]


def jar(ax):
    box(ax, 0.3, 0.9, 3.6, 4.9, fc=PAPER)
    label(ax, 2.1, 5.45, "주문 처리 묶음 (JAR)", fs=10.5, bold=True)
    for k, c in enumerate(CLASSES):
        chip(ax, 0.6, 4.4 - k * 0.62, 3.0, 0.5, c, fs=10)
    label(ax, 2.1, 1.2, "⋮", fs=12, color=INK)


def load(ax):
    cylinder(ax, *JVM, "JVM")
    jar(ax)
    label(ax, 6.5, 5.45, "찾기 · 읽기 · 검사", fs=10.5, color=RED, bold=True)
    arrow(ax, (4.0, 3.2), (4.9, 3.2), color=RED, ms=14)
    for k in range(5):
        chip(ax, 5.0, CARD_Y[k], 3.0, 0.5, CLASSES[k] + "  ✓", hot=True, fs=10)
    arrow(ax, (8.1, 2.0), (9.3, 1.6), color=INK, ms=12)


# ── 그림 3: JIT ────────────────────────────────────────────────────
def jit(ax):
    chip(ax, 0.3, 5.3, 3.0, 0.65, "주문받기", fs=10.5)
    box(ax, 0.3, 3.4, 3.6, 1.35, fc=PAPER)
    label(ax, 2.1, 4.07, "해석기\n(한 줄씩)", fs=10)
    arrow(ax, (1.8, 5.25), (1.8, 4.85), color=INK, ms=11)
    box(ax, 5.0, 3.4, 2.2, 1.35, fc=PINK, ec=RED)
    label(ax, 6.1, 4.07, "JIT", fs=12, color=RED, bold=True)
    chip(ax, 8.3, 3.4, 2.6, 1.35, "기계어", hot=True, fs=11.5)
    arrow(ax, (4.0, 4.07), (4.9, 4.07), color=RED, ms=13)
    arrow(ax, (7.3, 4.07), (8.2, 4.07), color=RED, ms=13)
    label(ax, 0.3, 2.75, "주문에 걸린 시간", fs=10, ha="left", color=INK, bold=True)
    bar(ax, 1.4, 2.2, "주문 1", 5.2)
    bar(ax, 1.4, 1.65, "주문 2", 4.8)
    bar(ax, 1.4, 1.1, "주문 31", 0.9, hot=True, note="기계어")


# ── 그림 4·5: AppCDS ──────────────────────────────────────────────
FILE = (5.0, 2.7, 2.1, 1.4)


def cds(ax, use):
    box(ax, 0.3, 1.0, 4.0, 4.9, fc="white", ec=GREY if use else INK)
    label(ax, 2.3, 5.55, "연습 실행 · JVM", fs=10.5, bold=True, color=GREY if use else "#222")
    for k, c in enumerate(CLASSES):
        chip(ax, 0.6, 4.6 - k * 0.65, 3.4, 0.5, c, dim=use, fs=10)
    chip(ax, *FILE, "클래스\n묶음 파일", hot=not use, fs=10.5)
    arrow(ax, (4.4, 3.4), (4.95, 3.4), color=GREY if use else RED, ms=12)
    box(ax, 7.8, 1.0, 4.0, 4.9, fc="white")
    label(ax, 9.8, 5.55, "새 파드 · JVM", fs=10.5, bold=True)
    if not use:
        return
    arrow(ax, (7.2, 3.4), (7.75, 3.4), color=RED, ms=12)
    label(ax, 9.8, 5.1, "찾기 · 읽기 · 검사", fs=9.5, color=GREY)
    ax.plot([8.65, 10.95], [5.1, 5.1], color=GREY, lw=1.5)
    for k, c in enumerate(CLASSES):
        r, col = k // 2, k % 2
        chip(ax, 8.05 + col * 1.8, 4.15 - r * 0.6, 1.65, 0.48, c, hot=True, fs=9.5)


# ── 그림 6·7: 체크포인트·복원 ─────────────────────────────────────
CPF = (5.0, 0.95, 2.3, 1.3)
INSIDE = ["클래스", "기계어", "장부 연결", "주문 자료"]


def proc(ax, x, title, items, hot=False, dim=False):
    box(ax, x, 2.6, 4.0, 3.3, fc="white", ec=GREY if dim else (RED if hot else INK))
    label(ax, x + 2.0, 5.55, title, fs=10.5, bold=True, color=GREY if dim else (RED if hot else "#222"))
    for k, s in enumerate(items):
        r, c = k // 2, k % 2
        chip(ax, x + 0.25 + c * 1.85, 4.35 - r * 0.85, 1.65, 0.6, s, hot=hot, dim=dim, fs=9.5)


def crac_save(ax):
    proc(ax, 0.3, "다 데워진 주문 처리", INSIDE)
    chip(ax, *CPF, "체크포인트\n파일", hot=True, fs=10.5)
    arrow(ax, (3.0, 2.55), (4.95, 1.75), color=RED, ms=14)
    box(ax, 7.8, 2.6, 4.0, 3.3, fc="white", ec=GREY)
    label(ax, 9.8, 5.55, "새 파드", fs=10.5, color=GREY)


def crac_restore(ax):
    proc(ax, 0.3, "다 데워진 주문 처리", INSIDE, dim=True)
    chip(ax, *CPF, "체크포인트\n파일", fs=10.5)
    arrow(ax, (7.35, 1.75), (9.2, 2.55), color=RED, ms=14)
    proc(ax, 7.8, "새 파드 · 실행 중", ["클래스", "기계어", "주문 자료"], hot=True)


# ── 그림 8·9: 통째로 저장할 때 걸리는 것 ──────────────────────────
CX = [0.75, 2.4, 4.05, 5.7]
DB = (9.4, 3.3, 2.0, 1.1)


def cpfile(ax, hot):
    box(ax, 0.5, 3.2, 7.0, 2.1, fc=PAPER)
    label(ax, 0.75, 4.95, "체크포인트 파일", fs=10.5, ha="left", bold=True)
    for k, s in enumerate(["클래스", "기계어", "장부 연결", "난수 42"]):
        chip(ax, CX[k], 3.5, 1.5, 1.0, s, hot=(k == hot), fs=10)


def catch_conn(ax):
    cpfile(ax, 2)
    label(ax, CX[2] + 0.75, 2.85, "✗", fs=16, color=RED, bold=True)
    cylinder(ax, *DB, "주문 장부")
    ax.plot([7.6, 9.3], [3.85, 3.85], color=RED, lw=1.6, ls=(0, (4, 3)))
    label(ax, 8.45, 3.85, "✗", fs=13, color=RED, bold=True)


def catch_rand(ax):
    cpfile(ax, 3)
    for k, x in enumerate([0.5, 4.3, 8.1]):
        box(ax, x, 0.75, 3.3, 1.2, fc="white")
        label(ax, x + 1.65, 1.65, f"주문 처리-{k + 3}", fs=10, bold=True)
        chip(ax, x + 0.85, 0.9, 1.6, 0.48, "난수 42", hot=True, fs=9.5)
        arrow(ax, (4.0, 3.15), (x + 1.65, 2.0), color=GREY, ms=11, lw=1.4)


# ── 그림 10: 고르기 ───────────────────────────────────────────────
def decide():
    fig, ax = canvas(10, 5.0, 15, 7.4)
    box(ax, 0.3, 6.0, 6.6, 1.0, fc=NOTE)
    label(ax, 3.6, 6.5, "새 파드 기다림이 문제?", fs=11, bold=True)
    arrow(ax, (7.0, 6.5), (8.4, 6.5)); label(ax, 7.7, 6.8, "아니요", fs=10, color=INK)
    box(ax, 8.5, 6.0, 6.2, 1.0, fc=PAPER)
    label(ax, 11.6, 6.5, "그대로", fs=11)
    arrow(ax, (3.6, 5.9), (3.6, 5.2)); label(ax, 3.9, 5.55, "예", fs=10, color=INK, ha="left")
    box(ax, 0.3, 4.15, 6.6, 1.0, fc=PAPER)
    label(ax, 3.6, 4.65, "AppCDS (코드 그대로)", fs=11)
    arrow(ax, (3.6, 4.05), (3.6, 3.35))
    box(ax, 0.3, 2.3, 6.6, 1.0, fc=NOTE)
    label(ax, 3.6, 2.8, "예열도 줄여야 함?", fs=11, bold=True)
    arrow(ax, (7.0, 2.8), (8.4, 2.8)); label(ax, 7.7, 3.1, "아니요", fs=10, color=INK)
    box(ax, 8.5, 2.3, 6.2, 1.0, fc=PAPER)
    label(ax, 11.6, 2.8, "AppCDS로 충분", fs=11)
    arrow(ax, (3.6, 2.2), (3.6, 1.5), color=RED); label(ax, 3.9, 1.85, "예", fs=10, color=RED, ha="left")
    box(ax, 0.3, 0.1, 6.6, 1.3, fc=PINK, ec=RED)
    label(ax, 3.6, 0.75, "체크포인트·복원 (CRaC)\n연결 · 난수 손질 + 권한", fs=10.5, color=RED, bold=True)
    save(fig, OUT, "k8s16-decide.svg")


if __name__ == "__main__":
    one(opening, "k8s16-open.svg")
    one(load, "k8s16-load.svg")
    one(jit, "k8s16-jit.svg")
    one(lambda ax: cds(ax, False), "k8s16-cds-record.svg")
    one(lambda ax: cds(ax, True), "k8s16-cds-use.svg")
    one(crac_save, "k8s16-crac-save.svg")
    one(crac_restore, "k8s16-crac-restore.svg")
    one(catch_conn, "k8s16-catch-conn.svg")
    one(catch_rand, "k8s16-catch-rand.svg")
    decide()
