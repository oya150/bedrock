"""쿠버네티스 15편 그림 만들기. 실행: python lab/fig_k8s15.py  → docs/kubernetes/img/15/*.svg

한 절에 한두 장. 지금 볼 곳만 빨강, 그림 안 글씨는 낱말과 숫자만.
예시는 빵집 주문 앱의 주문 처리 이미지. 층 셋: 바탕(칸 3), 실행 도구(칸 4), 주문 처리(칸 2).
노드 A에는 이미지가 이미 있고 새 노드 C는 비어 있다. 지연 로딩 예시 파일은 a~e, 시작에 필요한 파일은 d.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "es"))
from figkit import (GREY, INK, LIGHT, NOTE, PAPER, PINK, RED, arrow, box,  # noqa: E402
                    canvas, cell, label, outdir, save)
from matplotlib.patches import Rectangle  # noqa: E402

OUT = outdir("15", topic="kubernetes")
LAYERS = [("바탕", 3), ("실행 도구", 4), ("주문 처리", 2)]  # 아래에서 위로


def empty(ax, x, y, w, h, ec=GREY):
    ax.add_patch(Rectangle((x, y), w, h, fc="white", ec=ec, lw=1.2, ls="--"))


def chip(ax, x, y, w, h, s, hot=False, dim=False, fs=10):
    box(ax, x, y, w, h, fc=PINK if hot else (LIGHT if dim else NOTE), ec=RED if hot else (GREY if dim else INK),
        lw=1.8 if hot else 1.3)
    label(ax, x + w / 2, y + h / 2, s, fs=fs, color=RED if hot else (GREY if dim else "#222"), bold=hot)


# ── 공통 ───────────────────────────────────────────────────────────
S, L = (7.2, 3.8), (12, 6.6)


def one(draw, name, ylim=None):
    """ylim=(아래, 위)를 주면 그 높이만 남기고 자른다."""
    fig, ax = canvas(*S, *L)
    ax.add_patch(Rectangle((0, 0), *L, fill=False, ec="none"))
    draw(ax)
    if ylim:
        ax.set_ylim(*ylim)
        fig.set_size_inches(S[0], S[1] * (ylim[1] - ylim[0]) / L[1])
    save(fig, OUT, name)


# ── 그림 1: 파드 목록 화면 + 노드 보관함 ────────────────────────────
ROW_Y = [4.75 - k * 0.85 for k in range(3)]
ROWS = [("주문 처리-1", "노드 A", "실행 중"), ("주문 처리-2", "노드 A", "실행 중"), ("주문 처리-3", "노드 C", "이미지 받는 중")]


def podlist(ax, rows, hot=()):
    box(ax, 0.3, 1.1, 6.7, 5.25, fc="white", round_=False)
    ax.add_patch(Rectangle((0.3, 5.9), 6.7, 0.45, fc=LIGHT, ec=INK, lw=1.2))
    label(ax, 0.5, 6.12, "빵집 주문 앱 · 파드 목록", fs=11, ha="left", color=INK)
    for x, h in ((0.55, "이름"), (2.75, "노드"), (3.95, "상태")):
        label(ax, x, 5.45, h, fs=10, ha="left", color=INK)
    ax.plot([0.5, 6.8], [5.2, 5.2], color=INK, lw=1.0)
    for k, (n, nd, s) in enumerate(rows):
        y = ROW_Y[k]
        on = k in hot
        if on:
            ax.add_patch(Rectangle((0.45, y - 0.3), 6.4, 0.6, fc=PINK, ec=RED, lw=1.8))
        else:
            ax.plot([0.5, 6.8], [y - 0.34, y - 0.34], color=GREY, lw=0.8)
        for x, t in ((0.55, n), (2.75, nd), (3.95, s)):
            label(ax, x, y, t, fs=10.5, ha="left", color=RED if on else "#222", bold=on)


def store(ax, name, y, content=None, hot=False):
    box(ax, 7.6, y, 4.2, 1.35, fc="white", ec=RED if hot else INK)
    label(ax, 7.8, y + 1.05, f"{name} 보관함", fs=10, ha="left", color=RED if hot else INK, bold=hot)
    if content == "img":
        chip(ax, 8.0, y + 0.2, 3.4, 0.55, "주문 처리 이미지")
    else:
        label(ax, 9.7, y + 0.47, "비어 있음", fs=10, color=RED if hot else GREY, bold=hot)


def opening(ax):
    podlist(ax, ROWS, hot=(2,))
    store(ax, "노드 A", 3.9, "img")
    store(ax, "노드 C", 1.9, hot=True)


# ── 그림 2: 층 묶음 받기 ───────────────────────────────────────────
LY = [1.5, 2.7, 3.9]  # 바탕, 실행 도구, 주문 처리
UW = 0.48


def bundle(ax, x, y, name, n, hot=(), part=None):
    """압축 묶음 한 줄: 이름 + 촘촘한 칸 n개. part=앞 몇 칸만 들어옴(나머지 점선)."""
    label(ax, x, y + 0.35, name, fs=10, ha="left", color=RED if hot else "#222", bold=bool(hot))
    for k in range(n):
        cx = x + 1.4 + k * (UW + 0.04)
        if part is not None and k >= part:
            empty(ax, cx, y + 0.05, UW, 0.6)
        else:
            on = hot is True or (hot and k in hot)
            ax.add_patch(Rectangle((cx, y + 0.05), UW, 0.6, fc=PINK if on else LIGHT,
                                   ec=RED if on else INK, lw=1.6 if on else 1.0))
    label(ax, x + 1.4 + n * (UW + 0.04) + 0.1, y + 0.35, "압축", fs=8.5, ha="left", color=GREY)


def pull(ax):
    box(ax, 0.3, 1.0, 4.6, 4.9, fc=PAPER)
    label(ax, 2.6, 5.5, "이미지 저장소", fs=11, bold=True)
    for (n, c), y in zip(LAYERS, LY):
        bundle(ax, 0.55, y, n, c)
    box(ax, 7.0, 1.0, 4.7, 4.9, fc="white")
    label(ax, 9.35, 5.5, "노드 C 보관함", fs=11, bold=True)
    bundle(ax, 7.25, LY[0], "바탕", 3, hot=True)
    bundle(ax, 7.25, LY[1], "실행 도구", 4, hot=True, part=2)
    arrow(ax, (5.0, 2.6), (6.9, 2.6), color=RED, ms=15)


# ── 그림 3: 압축 풀어 펼치기 ───────────────────────────────────────
FW = 0.85
FY = [1.0, 2.05, 3.1]


def files(ax, x, y, n, hot=False, dim=(), red=()):
    for k in range(n):
        cx = x + k * (FW + 0.08)
        if k in dim:
            ax.add_patch(Rectangle((cx, y), FW, 0.8, fc="white", ec=GREY, lw=1.0))
        else:
            cell(ax, cx, y, FW, 0.8, "파일", hot=hot or k in red, fs=9)


def unpack(ax):
    label(ax, 0.3, 4.4, "받은 묶음", fs=11, ha="left", bold=True)
    label(ax, 6.2, 4.4, "펼친 파일", fs=11, ha="left", bold=True)
    for k, ((n, c), y) in enumerate(zip(LAYERS, FY)):
        bundle(ax, 0.3, y + 0.05, n, c)
        files(ax, 6.2, y, c, hot=True)
        yk = y + 0.4
        arrow(ax, (4.6, yk), (6.1, yk), color=RED, ms=14)
        label(ax, 5.35, yk + 0.25, "①②③"[k], fs=11, color=RED, bold=True)
    chip(ax, 7.9, 4.95, 2.6, 0.7, "컨테이너 시작", hot=True, fs=11)
    arrow(ax, (9.2, 3.95), (9.2, 4.9), color=RED, ms=12)


# ── 그림 4: 시작에 필요한 파일 ─────────────────────────────────────
def need(ax):
    label(ax, 3.2, 5.6, "받고 펼친 파일 전부", fs=11.5, bold=True)
    for (n, c), y in zip(LAYERS, [1.6, 2.75, 3.9]):
        label(ax, 1.4, y + 0.4, n, fs=10, ha="right", color=INK)
        files(ax, 1.6, y, c, dim=range(1, c), red=(0,))
    label(ax, 2.0, 1.25, "↑ 읽음", fs=10.5, ha="left", color=RED, bold=True)
    label(ax, 5.5, 3.15, "← 안 읽음", fs=10.5, ha="left", color=INK)


# ── 그림 5·6: 지연 로딩 ───────────────────────────────────────────
NAMES = ["a", "b", "c", "d", "e"]
SX = [0.6 + k * 1.45 for k in range(5)]
SY, SH = 4.2, 0.9
TOC = (SX[4] + 1.45, 1.6)


def solid(ax):
    label(ax, 0.6, 5.55, "보통 층 · 한 덩어리 압축", fs=11, ha="left", bold=True)
    ax.add_patch(Rectangle((0.6, SY), SX[4] + 1.3 - 0.6, SH, fc=LIGHT, ec=INK, lw=1.4))
    for k, n in enumerate(NAMES):
        label(ax, SX[k] + 0.65, SY + SH / 2, n, fs=12, color=RED if n == "d" else INK, bold=(n == "d"))
    ax.annotate("", xy=(SX[3] + 0.9, 3.95), xytext=(0.6, 3.95),
                arrowprops=dict(arrowstyle="-|>", color=RED, lw=2))
    label(ax, 2.6, 3.6, "a부터 풀기", fs=10.5, color=RED, bold=True)


def lazy(ax):
    box(ax, 2.0, 0.95, 8.0, 1.75, fc="white")
    label(ax, 2.2, 2.4, "노드 C", fs=10.5, ha="left", color=INK, bold=True)
    label(ax, 0.6, 5.55, "eStargz 층 · 파일마다 압축", fs=11, ha="left", bold=True)
    for k, n in enumerate(NAMES):
        cell(ax, SX[k], SY, 1.3, SH, n, hot=(n == "d"), fs=12)
    cell(ax, TOC[0], SY, TOC[1], SH, "목차", hot=True, fs=11)
    arrow(ax, (TOC[0] + 0.8, SY - 0.05), (8.6, 2.0), color=RED, ms=13)
    label(ax, TOC[0] + 1.0, 3.5, "①", fs=11, color=RED, bold=True)
    arrow(ax, (SX[3] + 0.65, SY - 0.05), (SX[3] + 0.4, 2.0), color=RED, ms=13)
    label(ax, SX[3] + 0.95, 3.5, "②", fs=11, color=RED, bold=True)
    label(ax, (SX[0] + SX[2] + 1.3) / 2, 3.8, "나중에", fs=10, color=GREY)
    label(ax, SX[4] + 0.65, 3.8, "나중에", fs=10, color=GREY)
    chip(ax, 7.8, 1.2, 1.5, 0.6, "목차", hot=True)
    chip(ax, 4.7, 1.2, 0.8, 0.6, "d", hot=True)
    chip(ax, 2.3, 1.2, 1.9, 0.6, "컨테이너 시작", hot=True, fs=9.5)


# ── 그림 7·8: 사전 풀 ─────────────────────────────────────────────
NX = {"A": 0.3, "B": 3.2, "C": 6.1, "D": 9.0}


def nodebox(ax, n, has=True, hot_img=False, pre_hot=False, pulling=False, new=False):
    x = NX[n]
    box(ax, x, 1.0, 2.6, 3.9, fc="white", ec=RED if new else INK)
    label(ax, x + 1.3, 4.6, f"노드 {n}" + (" (새로)" if new else ""), fs=10.5, bold=True,
          color=RED if new else "#222")
    chip(ax, x + 0.25, 3.65, 2.1, 0.55, "미리 받기", hot=pre_hot, fs=9.5)
    ax.add_patch(Rectangle((x + 0.15, 1.2), 2.3, 1.3, fc=PAPER, ec=INK, lw=1.0))
    label(ax, x + 0.3, 2.25, "보관함", fs=9, color=INK, ha="left")
    if has:
        chip(ax, x + 0.3, 1.35, 2.0, 0.55, "주문 처리 이미지", hot=hot_img, fs=8.5)
    elif pulling:
        label(ax, x + 1.3, 1.62, "받는 중…", fs=9.5, color=RED, bold=True)


def prepull(ax):
    label(ax, 0.3, 5.8, "DaemonSet", fs=11.5, ha="left", bold=True)
    nodebox(ax, "A")
    nodebox(ax, "B")
    nodebox(ax, "C", hot_img=True, pre_hot=True)
    arrow(ax, (NX["C"] + 1.9, 3.6), (NX["C"] + 1.9, 1.95), color=RED, ms=12)


def newnode(ax):
    label(ax, 0.3, 5.8, "DaemonSet", fs=11.5, ha="left", bold=True)
    for n in "ABC":
        nodebox(ax, n)
    nodebox(ax, "D", has=False, pre_hot=True, pulling=True, new=True)


# ── 그림 9: 고르기 ────────────────────────────────────────────────
def decide():
    fig, ax = canvas(10, 5.6, 15, 8.4)
    rows = [(7.1, "이미지 없는 노드에서 늦게 뜸?", "아니요", "그대로"),
            (5.2, "안 쓰는 파일이 많음?", "예", "이미지 줄이기"),
            (3.3, "뜰 노드가 정해짐?", "예", "사전 풀")]
    downs = ["예", "아니요", None]
    for k, (y, q, side, ans) in enumerate(rows):
        box(ax, 0.3, y, 6.4, 1.0, fc=NOTE)
        label(ax, 3.5, y + 0.5, q, fs=11, bold=True)
        arrow(ax, (6.8, y + 0.5), (8.4, y + 0.5)); label(ax, 7.6, y + 0.8, side, fs=10, color=INK)
        box(ax, 8.5, y, 6.2, 1.0, fc=PAPER)
        label(ax, 11.6, y + 0.5, ans, fs=11)
        if downs[k]:
            arrow(ax, (3.5, y - 0.1), (3.5, y - 0.8)); label(ax, 3.8, y - 0.45, downs[k], fs=10, color=INK, ha="left")
    arrow(ax, (3.5, 3.2), (3.5, 2.4), color=RED)
    label(ax, 3.8, 2.8, "아니요 (노드가 자주 생김)", fs=10, color=RED, ha="left")
    box(ax, 0.3, 1.3, 6.4, 1.0, fc=PINK, ec=RED)
    label(ax, 3.5, 1.8, "지연 로딩", fs=11.5, color=RED, bold=True)
    save(fig, OUT, "k8s15-decide.svg")


if __name__ == "__main__":
    one(opening, "k8s15-open.svg")
    one(pull, "k8s15-pull.svg")
    one(unpack, "k8s15-unpack.svg")
    one(need, "k8s15-need.svg")
    one(solid, "k8s15-solid.svg", ylim=(3.2, 6.0))
    one(lazy, "k8s15-lazy.svg")
    one(prepull, "k8s15-prepull.svg")
    one(newnode, "k8s15-newnode.svg")
    decide()
