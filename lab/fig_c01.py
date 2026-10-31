"""컴퓨터 1편 그림 만들기. 실행: python lab/fig_c01.py  → docs/computer/img/01/*.svg

장면 띠로 그린다: 무대(게임 화면이 켜진 컴퓨터와 그 말풍선)는 그대로 두고 장마다 바뀐 곳만 빨강으로 칠한다.
예시는 편 끝까지 같은 수를 쓴다: 별 하나 10점, 점수 60 → 70, 최고 기록 50 → 70.
검토용 PNG가 필요하면 FIG_FMT=png FIG_OUT=<폴더> 로 실행한다.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "es"))
from figkit import (GREY, INK, LIGHT, NOTE, PAPER, PINK, RED, arrow, box, bubble, canvas, cell, label,  # noqa: E402
                    moral, save, stage)
from matplotlib.patches import Circle, Rectangle  # noqa: E402

OUT = os.environ.get("FIG_OUT") or os.path.join(os.path.dirname(__file__), "..", "docs", "computer", "img", "01")
os.makedirs(OUT, exist_ok=True)

ORDERS = ["별 먹으면 점수에 10 더하기", "끝나면 두 수 비교하기", "점수가 크면 최고 기록 바꾸기", "바꿨으면 새 기록! 띄우기"]
SAY = (7.1, 4.35, 4.8, 1.45)          # 오른쪽 위 말풍선 자리
TAIL = (6.75, 4.0)


def star(ax, x, y, hot=False, size=30):
    ax.plot(x, y, marker="*", markersize=size, color=RED if hot else YEL_, mec=INK, mew=1.0)


YEL_ = "#f6c445"


def hud(ax, x, name, value, hot=False, strike=None):
    """화면 위쪽 점수판 칸. strike=지워지는 옛 값(회색 줄 긋기)."""
    label(ax, x + 1.05, 5.45, name, fs=11, color=RED if hot else INK)
    ax.add_patch(Rectangle((x, 4.25), 2.1, 0.95, fc=PINK if hot else "white", ec=RED if hot else INK, lw=2.0 if hot else 1.3))
    if strike is not None:
        label(ax, x + 1.05, 4.72, strike, fs=22, color=GREY, bold=True)
        ax.plot([x + 0.55, x + 1.55], [4.72, 4.72], color=GREY, lw=2.5)
    else:
        label(ax, x + 1.05, 4.72, value, fs=22, color=RED if hot else "#222", bold=True)


def computer(ax, score="60", best="50", hot_score=False, hot_best=False, strike_best=None):
    """무대: 게임 화면이 켜진 컴퓨터. 화면 위쪽에 점수판 두 칸."""
    box(ax, 0.4, 1.3, 6.2, 5.05, fc=LIGHT, ec=INK, lw=1.8)           # 테두리
    ax.add_patch(Rectangle((0.7, 1.6), 5.6, 4.45, fc="white", ec=INK, lw=1.2))  # 화면
    ax.add_patch(Rectangle((3.0, 0.75), 1.0, 0.55, fc=LIGHT, ec=INK, lw=1.2))   # 받침
    ax.add_patch(Rectangle((2.3, 0.55), 2.4, 0.22, fc=LIGHT, ec=INK, lw=1.2))
    hud(ax, 0.95, "점수", score, hot=hot_score)
    hud(ax, 3.95, "최고 기록", best, hot=hot_best, strike=strike_best)


def notes(ax, hot=(), order=False):
    """오른쪽 아래 쪽지 네 장(명령어)."""
    for i, what in enumerate(ORDERS):
        y = 3.15 - i * 0.68
        on = i in hot
        box(ax, 7.55, y, 4.3, 0.56, fc=PINK if on else NOTE, ec=RED if on else INK, lw=1.8 if on else 1.2)
        ax.add_patch(Circle((7.2, y + 0.28), 0.22, fc="white", ec=RED if on else INK, lw=1.3))
        label(ax, 7.2, y + 0.28, i + 1, fs=10.5, color=RED if on else INK, bold=True)
        label(ax, 7.7, y + 0.28, what, fs=10.5, ha="left", color=RED if on else "#222")


# ── 여는 장면 ──────────────────────────────────────────────────────
def game(ax, step):
    if step == 1:
        computer(ax, "60", "50")
        star(ax, 4.6, 3.0)
        ax.plot([1.4, 4.0], [3.0, 3.0], color=GREY, lw=2, ls=":")
        label(ax, 1.2, 3.0, "●", fs=20, color=INK)
        label(ax, 3.5, 2.05, "별 하나에 10점", fs=11, color=INK)
        bubble(ax, *SAY, "게임하는 중이에요", TAIL)
    else:
        computer(ax, "70", "70", hot_score=True, hot_best=True)
        label(ax, 3.5, 3.45, "게임 끝", fs=15, color=INK)
        label(ax, 3.5, 2.45, "새 기록!", fs=24, color=RED, bold=True)
        bubble(ax, *SAY, "새 기록이에요!", TAIL, hot=True)


# ── 세 가지 일 (한 장) ─────────────────────────────────────────────
def map_():
    fig, ax = canvas(9.0, 3.2, 13.5, 4.6)
    items = [("별을 먹으면", "더하기"), ("게임이 끝나면", "어느 쪽이 클까"), ("더 크면", "바꿔 적기")]
    for i, (when, what) in enumerate(items):
        x = 0.3 + i * 4.5
        box(ax, x, 0.9, 3.6, 2.7, fc="white")
        ax.add_patch(Rectangle((x + 0.25, 2.05), 3.1, 1.3, fc=PAPER, ec=INK, lw=1.0))
        if i == 0:
            star(ax, x + 1.8, 2.7, size=24)
        elif i == 1:
            label(ax, x + 1.8, 2.7, "70 ? 50", fs=15, bold=True)
        else:
            label(ax, x + 1.25, 2.7, "50", fs=15, color=GREY, bold=True)
            label(ax, x + 1.8, 2.7, "→", fs=15, color=INK)
            label(ax, x + 2.35, 2.7, "70", fs=15, color=RED, bold=True)
        label(ax, x + 0.3, 3.95, "①②③"[i], fs=14, color=RED, bold=True, ha="left")
        label(ax, x + 1.8, 1.65, what, fs=14, bold=True)
        label(ax, x + 1.8, 1.15, when, fs=11, color=INK)
        if i < 2:
            arrow(ax, (x + 3.7, 2.25), (x + 4.4, 2.25), ms=14)
    save(fig, OUT, "c01-map.svg")


# ── 더하기 ─────────────────────────────────────────────────────────
def add(ax, step):
    computer(ax, "70" if step == 3 else "60", "50", hot_score=(step == 3))
    if step == 1:
        star(ax, 3.5, 3.0, hot=True)
        label(ax, 3.5, 2.05, "별을 먹었어요", fs=12, color=RED)
        bubble(ax, *SAY, "별 하나는 10점이에요", TAIL, hot=True)
    elif step == 2:
        label(ax, 3.5, 2.9, "60 + 10", fs=24, color=RED, bold=True)
        bubble(ax, *SAY, "60에 10을 더해요", TAIL, hot=True)
    else:
        label(ax, 3.5, 2.9, "60 + 10 = 70", fs=20, color=INK, bold=True)
        arrow(ax, (4.6, 3.25), (2.6, 4.15), color=RED, ms=14, rad=0.2)
        bubble(ax, *SAY, "점수 칸에 70을 적어요", TAIL, hot=True)
        moral(ax, 6.0, 0.2, "별을 먹을 때마다 한 번씩 더해요")


# ── 비교 ───────────────────────────────────────────────────────────
def compare(ax, step):
    computer(ax, "70", "50", hot_score=(step == 2))
    label(ax, 3.5, 3.0, "게임 끝", fs=15, color=INK)
    if step == 1:
        bubble(ax, *SAY, "70과 50 중에\n어느 쪽이 클까요?", TAIL)
    else:
        label(ax, 3.5, 4.72, ">", fs=24, color=RED, bold=True)
        bubble(ax, *SAY, "70이 더 커요", TAIL, hot=True)
        moral(ax, 6.0, 0.2, "어느 쪽이 큰지 알아보는 일이 비교예요")


# ── 바꿔 적기 ──────────────────────────────────────────────────────
def write(ax, step):
    computer(ax, "70", "70" if step == 3 else "50", hot_best=(step == 3), strike_best="50" if step == 2 else None)
    label(ax, 3.5, 3.0, "게임 끝", fs=15, color=INK)
    if step == 1:
        bubble(ax, *SAY, "내 점수가 더 크니까\n최고 기록을 바꿔요", TAIL)
    elif step == 2:
        bubble(ax, *SAY, "있던 50을 지워요", TAIL, hot=True)
    else:
        bubble(ax, *SAY, "그 자리에 70을 적어요", TAIL, hot=True)
        moral(ax, 6.0, 0.2, "더 클 때만 바꿔 적어요")


# ── 쪽지(명령어) ───────────────────────────────────────────────────
def orders(ax, step):
    if step == 1:
        computer(ax, "60", "50")
        notes(ax)
        bubble(ax, *SAY, "게임을 만든 사람이\n적어 둔 쪽지예요", TAIL)
    elif step == 2:
        computer(ax, "70", "50", hot_score=True)
        star(ax, 3.5, 3.0)
        notes(ax, hot=(0,))
        arrow(ax, (6.95, 3.43), (3.1, 4.5), color=RED, ms=14, rad=0.15)
        bubble(ax, *SAY, "별! 1번 쪽지대로 더해요", TAIL, hot=True)
    else:
        computer(ax, "70", "70", hot_best=True)
        label(ax, 3.5, 3.45, "게임 끝", fs=15, color=INK)
        label(ax, 3.5, 2.45, "새 기록!", fs=24, color=RED, bold=True)
        notes(ax, hot=(1, 2, 3))
        bubble(ax, *SAY, "끝! 2번, 3번, 4번을\n차례로 해요", TAIL, hot=True)
        moral(ax, 6.0, 0.15, "쪽지에 없는 일은 하지 않아요")


# ── 빠르기 (한 장) ─────────────────────────────────────────────────
def speed():
    fig, ax = canvas(7.6, 4.8, 10.5, 7.6)
    label(ax, 4.0, 7.0, "같은 1초 동안", fs=15, color=INK)
    ax.add_patch(Circle((1.6, 3.6), 0.45, fc="white", ec=INK, lw=2))
    ax.plot([1.6, 1.6], [3.15, 1.9], color=INK, lw=2.5)
    ax.plot([1.0, 2.2], [2.8, 2.8], color=INK, lw=2.5)
    ax.plot([1.6, 1.1], [1.9, 1.0], color=INK, lw=2.5)
    ax.plot([1.6, 2.1], [1.9, 1.0], color=INK, lw=2.5)
    box(ax, 2.6, 1.6, 1.3, 0.5, fc=NOTE)
    label(ax, 3.25, 1.85, "더하기", fs=10)
    label(ax, 2.2, 0.3, "사람은 더하기 한 번", fs=13)
    box(ax, 5.3, 1.0, 2.6, 1.8, fc=PAPER)
    ax.add_patch(Rectangle((6.3, 0.55), 0.6, 0.45, color=INK))
    label(ax, 6.6, 1.9, "컴퓨터", fs=14)
    # 쪽지 더미는 그림 위쪽 끝을 넘어가서 몇 장인지 셀 수 없게 그린다
    for k in range(30):
        box(ax, 8.5, 1.0 + k * 0.4, 1.4, 0.3, fc=NOTE, ec=RED, lw=1.2)
        ax.text(9.2, 1.15 + k * 0.4, "더하기", ha="center", va="center", fontsize=8, clip_on=True)
    label(ax, 10.1, 6.2, "끝이\n안 보여요", fs=11, color=RED, ha="left")
    label(ax, 7.4, 0.0, "컴퓨터는 셀 수 없이 많이", fs=13, color=RED, bold=True)
    save(fig, OUT, "c01-speed.svg")


# ── 정리: 처음 장면으로 돌아가기 ───────────────────────────────────
def back(ax, step):
    computer(ax, "70", "70")
    label(ax, 3.5, 3.45, "게임 끝", fs=15, color=INK)
    label(ax, 3.5, 2.45, "새 기록!", fs=24, color=RED if step == 1 else INK, bold=True)
    if step == 1:
        bubble(ax, *SAY, "처음에 본 화면이에요\n새 기록은 어떻게 알았을까요?", TAIL)
        return
    tags = [(2.0, 3.95, "①"), (5.0, 3.95, "②③"), (5.5, 2.45, "④")]
    for x, y, t in tags:
        label(ax, x, y, t, fs=13, color=RED, bold=True)
    notes(ax, hot=(0, 1, 2, 3))
    bubble(ax, *SAY, "쪽지 네 장대로 했을 뿐이에요", TAIL, hot=True)
    moral(ax, 6.0, 0.15, "더하기, 비교, 바꿔 적기를 쪽지대로 아주 빨리 해요")


# ── 정리: 낱말 카드 ────────────────────────────────────────────────
def cards():
    fig, ax = canvas(6.4, 2.9, 9.8, 4.4)
    W, H = 4.6, 3.9
    for col, (name, line) in enumerate([("비교", "둘 중 어느 쪽이 큰지 알아보는 일"), ("명령어", "컴퓨터에게 시키는 일 하나를 적은 쪽지")]):
        x, y = 0.2 + col * 4.9, 0.25
        box(ax, x, y, W, H, fc="white")
        label(ax, x + 0.25, y + H - 0.4, name, fs=12.5, ha="left", bold=True)
        label(ax, x + W / 2, y + 0.45, line, fs=10, color=INK)
        if col == 0:
            cell(ax, x + 0.6, y + 1.5, 1.3, 1.0, "70", hot=True, fs=18)
            label(ax, x + 2.3, y + 2.0, ">", fs=20, color=RED, bold=True)
            cell(ax, x + 2.7, y + 1.5, 1.3, 1.0, "50", fs=18)
        else:
            box(ax, x + 0.5, y + 1.55, 3.6, 0.9, fc=NOTE, lw=1.4)
            label(ax, x + 2.3, y + 2.0, "점수에 10 더하기", fs=11.5)
    save(fig, OUT, "c01-cards.svg")


if __name__ == "__main__":
    S, L = (7.2, 3.8), (12, 6.6)
    stage(game, 2, OUT, "c01-game", S, L)
    map_()
    stage(add, 3, OUT, "c01-add", S, L)
    stage(compare, 2, OUT, "c01-compare", S, L)
    stage(write, 3, OUT, "c01-write", S, L)
    stage(orders, 3, OUT, "c01-orders", S, L)
    speed()
    stage(back, 2, OUT, "c01-back", S, L)
    cards()
