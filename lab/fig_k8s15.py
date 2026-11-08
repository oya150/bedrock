"""쿠버네티스 15편 그림 만들기. 실행: python lab/fig_k8s15.py  → docs/kubernetes/img/15/*.svg

본문 절은 장면 띠로 그린다: 같은 무대를 여러 장 그리고 장마다 바뀐 곳만 빨강으로 칠한다.
예시는 빵집 주문 앱의 주문 처리 이미지. 층 셋: 바탕(칸 3), 실행 도구(칸 4), 주문 처리(칸 2).
노드 A에는 이미지가 이미 있고 새 노드 C는 비어 있다. 지연 로딩 예시 파일은 a~e, 시작에 필요한 파일은 d.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "es"))
from figkit import (GREY, INK, LIGHT, NOTE, PAPER, PINK, RED, arrow, box,  # noqa: E402
                    canvas, cell, label, moral, outdir, save, stage)
from matplotlib.patches import Rectangle  # noqa: E402

OUT = outdir("15", topic="kubernetes")
LAYERS = [("바탕", 3), ("실행 도구", 4), ("주문 처리", 2)]  # 아래에서 위로


def empty(ax, x, y, w, h, ec=GREY):
    ax.add_patch(Rectangle((x, y), w, h, fc="white", ec=ec, lw=1.2, ls="--"))


def chip(ax, x, y, w, h, s, hot=False, dim=False, fs=10):
    box(ax, x, y, w, h, fc=PINK if hot else (LIGHT if dim else NOTE), ec=RED if hot else (GREY if dim else INK),
        lw=1.8 if hot else 1.3)
    label(ax, x + w / 2, y + h / 2, s, fs=fs, color=RED if hot else (GREY if dim else "#222"), bold=hot)


# ── 파드 목록 화면 + 노드 보관함 ────────────────────────────────────
ROW_Y = [4.75 - k * 0.85 for k in range(3)]
ROWS = [("주문 처리-1", "노드 A", "실행 중"), ("주문 처리-2", "노드 A", "실행 중"), ("주문 처리-3", "노드 C", "이미지 받는 중")]


def podlist(ax, rows, hot=(), dim=()):
    box(ax, 0.3, 1.1, 6.7, 5.25, fc="white", round_=False)
    ax.add_patch(Rectangle((0.3, 5.9), 6.7, 0.45, fc=LIGHT, ec=INK, lw=1.2))
    label(ax, 0.5, 6.12, "빵집 주문 앱 · 파드 목록", fs=11, ha="left", color=INK)
    for x, h in ((0.55, "이름"), (2.75, "노드"), (3.95, "상태")):
        label(ax, x, 5.45, h, fs=10, ha="left", color=INK)
    ax.plot([0.5, 6.8], [5.2, 5.2], color=INK, lw=1.0)
    for k, (n, nd, s) in enumerate(rows):
        y = ROW_Y[k]
        on, off = k in hot, k in dim
        if on:
            ax.add_patch(Rectangle((0.45, y - 0.3), 6.4, 0.6, fc=PINK, ec=RED, lw=1.8))
        else:
            ax.plot([0.5, 6.8], [y - 0.34, y - 0.34], color=GREY, lw=0.8)
        c = RED if on else (GREY if off else "#222")
        for x, t in ((0.55, n), (2.75, nd), (3.95, s)):
            label(ax, x, y, t, fs=10.5, ha="left", color=c, bold=on)


def store(ax, name, y, content=None, hot=False):
    """오른쪽 노드 보관함. content=None(비어 있음) | 'img' | 'lazy'."""
    box(ax, 7.6, y, 4.2, 1.35, fc="white")
    label(ax, 7.8, y + 1.05, f"{name} 보관함", fs=10, ha="left", color=INK)
    if content == "img":
        chip(ax, 8.0, y + 0.2, 3.4, 0.55, "주문 처리 이미지", hot=hot)
    elif content == "lazy":
        chip(ax, 8.0, y + 0.2, 1.5, 0.55, "목차", hot=hot)
        chip(ax, 9.7, y + 0.2, 0.8, 0.55, "d", hot=hot)
    else:
        label(ax, 9.7, y + 0.47, "비어 있음", fs=10, color=GREY)


def corner(ax, s):
    label(ax, 9.7, 6.1, s, fs=12, color=INK, bold=True)


def opening(ax, step):
    store(ax, "노드 A", 3.9, "img")
    if step == 1:
        podlist(ax, ROWS, hot=(1,))
        corner(ax, "막 띄웠을 때")
        store(ax, "노드 C", 1.9)
    elif step == 2:
        podlist(ax, ROWS, hot=(2,))
        corner(ax, "한참 뒤")
        store(ax, "노드 C", 1.9)
    else:
        rows = ROWS[:2] + [("주문 처리-3", "노드 C", "실행 중")]
        podlist(ax, rows, hot=(2,))
        corner(ax, "더 한참 뒤")
        store(ax, "노드 C", 1.9, "img", hot=True)
        moral(ax, 6.0, 0.4, "이미지가 없는 노드에서만 오래 걸려요")


# ── 층 묶음 받기 ───────────────────────────────────────────────────
LY = [1.5, 2.7, 3.9]  # 바탕, 실행 도구, 주문 처리
UW = 0.48


def bundle(ax, x, y, name, n, hot=(), dim=False, part=None):
    """압축 묶음 한 줄: 이름 + 촘촘한 칸 n개. part=앞 몇 칸만 들어옴(나머지 점선)."""
    label(ax, x, y + 0.35, name, fs=10, ha="left", color=RED if hot else (GREY if dim else "#222"), bold=bool(hot))
    for k in range(n):
        cx = x + 1.4 + k * (UW + 0.04)
        if part is not None and k >= part:
            empty(ax, cx, y + 0.05, UW, 0.6)
        else:
            on = hot is True or (hot and k in hot)
            ax.add_patch(Rectangle((cx, y + 0.05), UW, 0.6, fc=PINK if on else (LIGHT if not dim else "white"),
                                   ec=RED if on else (GREY if dim else INK), lw=1.6 if on else 1.0))
    label(ax, x + 1.4 + n * (UW + 0.04) + 0.1, y + 0.35, "압축", fs=8.5, ha="left", color=GREY)


def pull(ax, step):
    box(ax, 0.3, 1.0, 4.6, 4.9, fc=PAPER)
    label(ax, 2.6, 5.5, "이미지 저장소", fs=11, bold=True)
    for (n, c), y in zip(LAYERS, LY):
        bundle(ax, 0.55, y, n, c)
    box(ax, 7.0, 1.0, 4.7, 4.9, fc="white")
    label(ax, 9.35, 5.5, "노드 C 보관함", fs=11, bold=True)
    if step == 1:
        label(ax, 9.35, 3.0, "비어 있음", fs=11, color=GREY)
    elif step == 2:
        bundle(ax, 7.25, LY[0], "바탕", 3, hot=True)
        bundle(ax, 7.25, LY[1], "실행 도구", 4, hot=True, part=2)
        arrow(ax, (5.0, 2.6), (6.9, 2.6), color=RED, ms=15)
        label(ax, 6.0, 0.45, "층마다 압축한 묶음째 받아요", fs=11, color=RED, bold=True)
    else:
        bundle(ax, 7.25, LY[0], "바탕", 3)
        bundle(ax, 7.25, LY[1], "실행 도구", 4)
        bundle(ax, 7.25, LY[2], "주문 처리", 2, hot=True)
        moral(ax, 6.0, 0.45, "세 층을 다 받았어요 · 아직 압축된 채예요")


# ── 압축 풀어 펼치기 ───────────────────────────────────────────────
FW = 0.85
FY = [1.5, 2.55, 3.6]


def files(ax, x, y, n, hot=False, dim=(), red=()):
    for k in range(n):
        cx = x + k * (FW + 0.08)
        if k in dim:
            ax.add_patch(Rectangle((cx, y), FW, 0.8, fc="white", ec=GREY, lw=1.0))
        else:
            on = hot or k in red
            cell(ax, cx, y, FW, 0.8, "파일", hot=on, fs=9)


def unpack(ax, step):
    label(ax, 0.3, 5.6, "받은 묶음", fs=11, ha="left", bold=True)
    for k, ((n, c), y) in enumerate(zip(LAYERS, FY)):
        bundle(ax, 0.3, y + 0.05, n, c, hot=(True if k == step - 1 else ()))
    label(ax, 6.2, 5.6, "펼친 파일", fs=11, ha="left", bold=True)
    for k, ((n, c), y) in enumerate(zip(LAYERS, FY)):
        x = 6.2
        if k < step:
            files(ax, x, y, c, hot=(k == step - 1))
        else:
            empty(ax, x, y, c * (FW + 0.08) - 0.08, 0.8)
    yk = FY[step - 1] + 0.4
    arrow(ax, (4.6, yk), (6.1, yk), color=RED, ms=14)
    if step == 1:
        label(ax, 6.0, 0.6, "압축을 풀어 파일로 펼쳐요", fs=11, color=RED, bold=True)
    elif step == 2:
        label(ax, 6.0, 0.6, "아래층 위에 겹쳐 펼쳐요", fs=11, color=RED, bold=True)
    else:
        chip(ax, 8.4, 4.75, 2.6, 0.7, "컨테이너 시작", hot=True, fs=11)
        moral(ax, 6.0, 0.6, "다 받고 다 펼쳐야 컨테이너가 시작해요")


# ── 시작에 필요한 파일 ─────────────────────────────────────────────
def need(ax, step):
    label(ax, 3.2, 5.6, "받고 펼친 파일 전부", fs=11.5, bold=True)
    for k, ((n, c), y) in enumerate(zip(LAYERS, [1.6, 2.75, 3.9])):
        label(ax, 1.4, y + 0.4, n, fs=10, ha="right", color=INK)
        if step == 1:
            files(ax, 1.6, y, c)
        else:
            files(ax, 1.6, y, c, dim=range(1, c), red=(0,))
    if step == 2:
        label(ax, 2.0, 1.25, "↑ 시작할 때 읽은 파일", fs=10.5, ha="left", color=RED, bold=True)
        label(ax, 5.5, 3.15, "← 아직 안 읽은 파일", fs=10.5, ha="left", color=INK)
        moral(ax, 6.0, 0.7, "다 받았지만 시작에 쓰는 건 일부예요")


# ── 지연 로딩 ──────────────────────────────────────────────────────
NAMES = ["a", "b", "c", "d", "e"]
SX = [0.6 + k * 1.45 for k in range(5)]
SY, SH = 4.2, 0.9
TOC = (SX[4] + 1.45, 1.6)


def lazy(ax, step):
    box(ax, 2.0, 0.95, 8.0, 1.75, fc="white")
    label(ax, 2.2, 2.4, "노드 C", fs=10.5, ha="left", color=INK, bold=True)
    if step == 1:
        label(ax, 0.6, 5.55, "보통 층 · 한 덩어리로 압축", fs=11, ha="left", bold=True)
        ax.add_patch(Rectangle((0.6, SY), SX[4] + 1.3 - 0.6, SH, fc=LIGHT, ec=INK, lw=1.4))
        for k, n in enumerate(NAMES):
            label(ax, SX[k] + 0.65, SY + SH / 2, n, fs=12, color=RED if n == "d" else INK, bold=(n == "d"))
        arrow(ax, (SX[3] + 0.65, 5.75), (SX[3] + 0.65, SY + SH + 0.05), color=RED, ms=13)
        label(ax, SX[3] + 0.9, 5.55, "d만 필요해요", fs=10.5, ha="left", color=RED, bold=True)
        ax.annotate("", xy=(SX[3] + 0.4, 3.95), xytext=(0.6, 3.95),
                    arrowprops=dict(arrowstyle="-|>", color=RED, lw=2))
        label(ax, 2.6, 3.6, "앞에서부터 풀어 가야 d에 닿아요", fs=10.5, color=RED, bold=True)
        return
    label(ax, 0.6, 5.55, "eStargz 층 · 파일마다 따로 압축", fs=11, ha="left", bold=True)
    for k, n in enumerate(NAMES):
        on = step == 3 and n == "d"
        cell(ax, SX[k], SY, 1.3, SH, n, hot=on, fs=12)
    cell(ax, TOC[0], SY, TOC[1], SH, "목차", hot=(step == 2), fs=11)
    if step == 2:
        label(ax, TOC[0] + TOC[1] / 2, 3.75, "파일마다 어디 있는지\n적어 둬요", fs=10, color=RED, bold=True)
    else:
        arrow(ax, (TOC[0] + 0.8, SY - 0.05), (8.6, 2.0), color=RED, ms=13)
        label(ax, TOC[0] + 1.0, 3.5, "①", fs=11, color=RED, bold=True)
        arrow(ax, (SX[3] + 0.65, SY - 0.05), (SX[3] + 0.4, 2.0), color=RED, ms=13)
        label(ax, SX[3] + 0.95, 3.5, "②", fs=11, color=RED, bold=True)
        label(ax, (SX[0] + SX[2] + 1.3) / 2, 3.8, "쓸 때 받아요", fs=10, color=GREY)
        chip(ax, 7.8, 1.2, 1.5, 0.6, "목차", hot=True)
        chip(ax, 4.7, 1.2, 0.8, 0.6, "d", hot=True)
        chip(ax, 2.3, 1.2, 1.9, 0.6, "컨테이너 시작", hot=True, fs=9.5)
        moral(ax, 6.0, 0.45, "목차를 먼저 받고 필요한 파일만 받아서 시작해요")


# ── 사전 풀 ────────────────────────────────────────────────────────
NX = {"A": 0.3, "B": 3.2, "C": 6.1, "D": 9.0}


def nodebox(ax, n, has=True, hot_img=False, pre_hot=False, extra=None, pulling=False):
    x = NX[n]
    box(ax, x, 1.0, 2.6, 3.9, fc="white")
    label(ax, x + 1.3, 4.6, f"노드 {n}", fs=10.5, bold=True)
    chip(ax, x + 0.25, 3.65, 2.1, 0.55, "미리 받기", hot=pre_hot, fs=9.5)
    if extra:
        chip(ax, x + 0.25, 2.85, 2.1, 0.55, extra, hot=True, fs=9.5)
    ax.add_patch(Rectangle((x + 0.15, 1.2), 2.3, 1.3, fc=PAPER, ec=INK, lw=1.0))
    label(ax, x + 0.3, 2.25, "보관함", fs=9, color=INK, ha="left")
    if has:
        chip(ax, x + 0.3, 1.35, 2.0, 0.55, "주문 처리 이미지", hot=hot_img, fs=8.5)
    elif pulling:
        label(ax, x + 1.3, 1.62, "받는 중…", fs=9.5, color=RED, bold=True)
    return x


def prepull(ax, step):
    label(ax, 0.3, 5.8, "DaemonSet: 노드마다 하나씩", fs=11.5, ha="left", bold=True)
    nodebox(ax, "A")
    nodebox(ax, "B")
    if step == 1:
        nodebox(ax, "C", hot_img=True, pre_hot=True)
        arrow(ax, (NX["C"] + 1.9, 3.6), (NX["C"] + 1.9, 1.95), color=RED, ms=12)
    elif step == 2:
        nodebox(ax, "C", extra="주문 처리-3")
        label(ax, 10.35, 3.0, "이미 있으니\n바로 시작해요", fs=11, color=RED, bold=True)
    else:
        nodebox(ax, "C", extra="주문 처리-3")
        nodebox(ax, "D", has=False, pre_hot=True, pulling=True)
        label(ax, 10.3, 5.35, "이 파드도 이미지를\n받는 중이에요", fs=10, color=RED, bold=True)
        moral(ax, 6.0, 0.45, "새로 들어온 노드는 미리 받기도 처음부터 해요")


# ── 판단 (한 장) ───────────────────────────────────────────────────
def decide():
    fig, ax = canvas(10, 5.6, 15, 8.4)
    rows = [(7.1, "이미지가 없는 노드에서 받느라 시작이 늦나요?", "아니요", "그대로 둬요"),
            (5.2, "이미지에 안 쓰는 파일이 많나요?", "예", "먼저 이미지를 줄여요"),
            (3.3, "파드가 뜰 노드가 미리 정해져 있나요?", "예", "사전 풀\n(DaemonSet으로 미리 받아 둬요)")]
    downs = ["예", "아니요", None]
    for k, (y, q, side, ans) in enumerate(rows):
        box(ax, 0.3, y, 6.4, 1.0, fc=NOTE)
        label(ax, 3.5, y + 0.5, q, fs=10.5, bold=True)
        arrow(ax, (6.8, y + 0.5), (8.4, y + 0.5)); label(ax, 7.6, y + 0.8, side, fs=10, color=INK)
        box(ax, 8.5, y, 6.2, 1.0, fc=PAPER)
        label(ax, 11.6, y + 0.5, ans, fs=10.5)
        if downs[k]:
            arrow(ax, (3.5, y - 0.1), (3.5, y - 0.8)); label(ax, 3.8, y - 0.45, downs[k], fs=10, color=INK, ha="left")
    arrow(ax, (3.5, 3.2), (3.5, 2.4), color=RED)
    label(ax, 3.8, 2.8, "아니요, 노드가 수시로 새로 생겨요", fs=10, color=RED, ha="left")
    box(ax, 0.3, 1.3, 6.4, 1.0, fc=PINK, ec=RED)
    label(ax, 3.5, 1.8, "지연 로딩\n(필요한 파일만 먼저 받아요)", fs=10.5, color=RED, bold=True)
    save(fig, OUT, "k8s15-decide.svg")


# ── 정리: 처음 장면으로 돌아가기 ───────────────────────────────────
def back(ax, step):
    store(ax, "노드 A", 3.9, "img")
    if step == 1:
        podlist(ax, ROWS, dim=(0, 1, 2))
        corner(ax, "처음")
        store(ax, "노드 C", 1.9)
        return
    rows = ROWS[:2] + [("주문 처리-3", "노드 C", "실행 중")]
    podlist(ax, rows, hot=(2,))
    if step == 2:
        corner(ax, "사전 풀")
        store(ax, "노드 C", 1.9, "img", hot=True)
    else:
        corner(ax, "지연 로딩")
        store(ax, "노드 C", 1.9, "lazy", hot=True)
        moral(ax, 6.0, 0.4, "미리 받아 두거나 필요한 파일만 받으면 바로 떠요")


# ── 정리: 낱말 카드 ────────────────────────────────────────────────
def cards():
    fig, ax = canvas(6.4, 5.4, 9.8, 8.3)
    W, H = 4.6, 3.8

    def card(i, name, line):
        col, row = i % 2, i // 2
        x, y = 0.2 + col * 4.9, 4.25 - row * 4.05
        box(ax, x, y, W, H, fc="white")
        label(ax, x + 0.25, y + H - 0.4, name, fs=12, ha="left", bold=True)
        label(ax, x + W / 2, y + 0.6, line, fs=9.5, color=INK)
        return x, y

    x, y = card(0, "이미지 저장소 (레지스트리)", "이미지를 올려 두고\n내려받게 해 주는 서버")
    chip(ax, x + 0.3, y + 1.55, 1.5, 0.8, "저장소", fs=10)
    arrow(ax, (x + 1.9, y + 1.95), (x + 2.7, y + 1.95), color=RED, ms=11)
    chip(ax, x + 2.8, y + 1.55, 1.5, 0.8, "보관함", hot=True, fs=10)
    x, y = card(1, "압축 풀기", "받은 층 묶음을 파일로 펼치는 일\n아래층부터 차례로")
    ax.add_patch(Rectangle((x + 0.3, y + 1.65), 1.3, 0.6, fc=LIGHT, ec=INK, lw=1.0))
    label(ax, x + 0.95, y + 1.95, "압축", fs=9, color=INK)
    arrow(ax, (x + 1.7, y + 1.95), (x + 2.3, y + 1.95), color=RED, ms=11)
    for k in range(3):
        cell(ax, x + 2.4 + k * 0.68, y + 1.65, 0.6, 0.6, "", hot=True)
    x, y = card(2, "지연 로딩", "다 받기 전에 시작하고\n파일은 쓸 때 받아요")
    for k, n in enumerate(NAMES):
        cell(ax, x + 0.3 + k * 0.62, y + 1.65, 0.56, 0.6, n, hot=(n == "d"), dim=(n != "d"), fs=9.5)
    cell(ax, x + 0.3 + 5 * 0.62, y + 1.65, 0.95, 0.6, "목차", hot=True, fs=9)
    x, y = card(3, "사전 풀", "쓸 이미지를 노드에\n미리 받아 두는 일")
    for k in range(3):
        ax.add_patch(Rectangle((x + 0.3 + k * 1.38, y + 1.5), 1.25, 1.0, fc="white", ec=INK, lw=1.0))
        cell(ax, x + 0.42 + k * 1.38, y + 1.65, 1.0, 0.5, "이미지", hot=True, fs=8.5)
    save(fig, OUT, "k8s15-cards.svg")


if __name__ == "__main__":
    S, L = (7.2, 3.8), (12, 6.6)
    stage(opening, 3, OUT, "k8s15-open", S, L)
    stage(pull, 3, OUT, "k8s15-pull", S, L)
    stage(unpack, 3, OUT, "k8s15-unpack", S, L)
    stage(need, 2, OUT, "k8s15-need", S, L)
    stage(lazy, 3, OUT, "k8s15-lazy", S, L)
    stage(prepull, 3, OUT, "k8s15-prepull", S, L)
    decide()
    stage(back, 3, OUT, "k8s15-back", S, L)
    cards()
