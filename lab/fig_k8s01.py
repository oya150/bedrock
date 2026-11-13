"""쿠버네티스 1편 그림 만들기. 실행: python lab/fig_k8s01.py  → docs/kubernetes/img/01/*.svg

갈래 공통 무대(4·5편도 이 모양을 그대로 쓴다):
- 건물 = 컴퓨터 한 대. 사각 몸체 + 위에 검은 지붕 띠, 맨 아래 칸이 "관리실 · 커널"(회색 띠).
- 칸막이 사무실 = 컨테이너. 관리실 위 층을 굵은 세로 벽으로 나눈 칸. 칸 안에 프로그램 이름.
- 따로 지은 집 = VM(5편 microVM은 같은 집을 작게). 세모 지붕 + 몸체, 집마다 아래에 자기 관리실.
- 땅 = 실제 컴퓨터(집을 지을 때만 그린다).
예시는 빵집 주문 앱 세 부품: 주문 화면, 주문 처리, 주문 장부. 프로세스 번호 230·231·232.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "es"))
from figkit import (GREY, INK, LIGHT, NOTE, PAPER, PINK, RED, arrow, box,  # noqa: E402
                    canvas, cell, label, outdir, save, stage)
from matplotlib.patches import Circle, Polygon, Rectangle  # noqa: E402

OUT = outdir("01", topic="kubernetes")
PARTS = ["주문 화면", "주문 처리", "주문 장부"]


# ── 공통 무대 ─────────────────────────────────────────────────────
def window(ax, x, y, w, h, title, hot=False):
    """실제 화면 모양 창: 제목 띠와 동그라미 셋."""
    ec = RED if hot else INK
    ax.add_patch(Rectangle((x, y), w, h, fc="white", ec=ec, lw=1.8 if hot else 1.4))
    ax.add_patch(Rectangle((x, y + h - 0.45), w, 0.45, fc=LIGHT, ec=ec, lw=1.2))
    for k in range(3):
        ax.add_patch(Circle((x + 0.22 + k * 0.22, y + h - 0.225), 0.06, fc=GREY, ec="none"))
    label(ax, x + 0.95, y + h - 0.225, title, fs=10, ha="left", color=RED if hot else INK, bold=hot)


def rows(ax, x, y, w, items, hot=(), dim=(), dy=0.5, fs=10.5):
    """창 안의 줄들. items=[(왼쪽 칸, 오른쪽 칸)]. hot/dim=줄 번호(0부터)."""
    for k, (a, b) in enumerate(items):
        yy = y - k * dy
        on, off = k in hot, k in dim
        if on:
            ax.add_patch(Rectangle((x, yy - dy / 2 + 0.04), w, dy - 0.08, fc=PINK, ec=RED, lw=1.5))
        c = RED if on else (GREY if off else "#222")
        label(ax, x + 0.2, yy, a, fs=fs, ha="left", color=c, bold=on)
        label(ax, x + 1.15, yy, b, fs=fs, ha="left", color=c, bold=on)


def building(ax, x, y, w, h, rooms, walls=True, wall_hot=False, kern_hot=False, room_hot=(), room_dim=(),
             title="건물 = 컴퓨터 한 대", kern="관리실 · 커널", fs=10.5):
    """건물 한 채. rooms=칸 이름 목록. walls=False면 칸막이 없이 한 층에 섞여 있다. 칸 가운데 (x, y) 목록을 돌려준다."""
    ax.add_patch(Rectangle((x, y), w, h, fc="white", ec=INK, lw=2.2))
    ax.add_patch(Rectangle((x - 0.15, y + h), w + 0.3, 0.2, fc=INK, ec=INK))
    if title:
        label(ax, x + w / 2, y + h + 0.48, title, fs=10.5, color=INK, bold=True)
    kc = RED if kern_hot else INK
    ax.add_patch(Rectangle((x + 0.15, y + 0.15), w - 0.3, 0.6, fc=PINK if kern_hot else LIGHT, ec=kc,
                           lw=1.8 if kern_hot else 1.2))
    label(ax, x + w / 2, y + 0.45, kern, fs=10.5, color=kc, bold=kern_hot)
    n = len(rooms)
    top, bot = y + h - 0.15, y + 0.9
    rw = (w - 0.3) / max(n, 1)
    centers = []
    for k, r in enumerate(rooms):
        rx = x + 0.15 + k * rw
        cx, cy = rx + rw / 2, (top + bot) / 2
        centers.append((cx, cy))
        on, off = k in room_hot, k in room_dim
        if walls:
            ax.add_patch(Rectangle((rx + 0.05, bot), rw - 0.1, top - bot, fc=PINK if on else NOTE,
                                   ec=RED if on else INK, lw=1.2))
        cw = min(1.6, rw - 0.25)
        if r:
            cell(ax, cx - cw / 2, cy - 0.28, cw, 0.56, r, hot=on, dim=off, fs=fs)
    if walls:
        for k in range(1, n):
            wx = x + 0.15 + k * rw
            ax.plot([wx, wx], [bot - 0.05, top], color=RED if wall_hot else INK, lw=4 if wall_hot else 3.2,
                    solid_capstyle="butt")
    return centers


def house(ax, x, y, w, h, prog, kern_hot=False, dim=False, hide=False, kern="관리실 · 커널"):
    """땅 위에 따로 지은 집(VM). 집마다 아래에 자기 관리실. hide=안을 가린다(밖에서 본 모습)."""
    ec = GREY if dim else INK
    ax.add_patch(Rectangle((x, y), w, h, fc="white", ec=ec, lw=2.0))
    ax.add_patch(Polygon([(x - 0.15, y + h), (x + w + 0.15, y + h), (x + w / 2, y + h + 0.7)], closed=True,
                         fc=LIGHT, ec=ec, lw=2.0))
    if hide:
        ax.add_patch(Rectangle((x + 0.1, y + 0.1), w - 0.2, h - 0.2, fc=LIGHT, ec="none"))
        label(ax, x + w / 2, y + h / 2, "안은\n안 보여요", fs=10, color=RED)
        return
    kc = RED if kern_hot else ec
    ax.add_patch(Rectangle((x + 0.12, y + 0.12), w - 0.24, 0.6, fc=PINK if kern_hot else LIGHT, ec=kc,
                           lw=1.8 if kern_hot else 1.1))
    label(ax, x + w / 2, y + 0.42, kern, fs=9.5, color=kc, bold=kern_hot)
    if prog:
        cell(ax, x + w / 2 - 0.8, y + h - 0.85, 1.6, 0.56, prog, dim=dim, fs=10.5)


def ground(ax, x0, x1, y, name="땅 = 실제 컴퓨터"):
    ax.add_patch(Rectangle((x0, y - 0.35), x1 - x0, 0.35, fc=LIGHT, ec=INK, lw=1.2))
    label(ax, (x0 + x1) / 2, y - 0.6, name, fs=10.5, color=INK, bold=True)


# ── 여는 장면: 컨테이너 목록과 이 컴퓨터의 프로그램 목록 ─────────
PS = [("1", "시작 프로그램"), ("57", "접속 관리"), ("230", "주문 화면"), ("231", "주문 처리"), ("232", "주문 장부")]


def ctr_list(ax, hot=None, dim=False):
    window(ax, 0.3, 3.3, 5.0, 2.9, "컨테이너 목록")
    label(ax, 0.5, 5.35, "이름", fs=9.5, ha="left", color=INK)
    label(ax, 3.8, 5.35, "상태", fs=9.5, ha="left", color=INK)
    ax.plot([0.45, 5.15], [5.12, 5.12], color=INK, lw=0.8)
    for k, p in enumerate(PARTS):
        yy = 4.75 - k * 0.5
        on = hot is True or (hot is not None and hot is not False and hot == k)
        if on:
            ax.add_patch(Rectangle((0.4, yy - 0.21), 4.8, 0.42, fc=PINK, ec=RED, lw=1.5))
        c = RED if on else (GREY if dim else "#222")
        label(ax, 0.6, yy, p, fs=10.5, ha="left", color=c, bold=on)
        label(ax, 3.8, yy, "실행 중", fs=10.5, ha="left", color=c)


def ps_list(ax, hot=(), y0=6.2):
    window(ax, 6.0, y0 - 4.3, 5.7, 4.3, "이 컴퓨터에서 돌아가는 프로그램", hot=False)
    label(ax, 6.2, y0 - 0.85, "번호", fs=9.5, ha="left", color=INK)
    label(ax, 7.15, y0 - 0.85, "프로그램", fs=9.5, ha="left", color=INK)
    ax.plot([6.15, 11.55], [y0 - 1.07, y0 - 1.07], color=INK, lw=0.8)
    rows(ax, 6.1, y0 - 1.45, 5.5, PS, hot=hot)


def opening(ax):
    ctr_list(ax, hot=1)
    ps_list(ax, hot=(3,))
    arrow(ax, (5.25, 4.25), (6.05, 3.3), color=RED, ms=14, rad=-0.2)
    label(ax, 3.3, 2.75, "같은 프로그램", fs=11, color=RED, bold=True)


# ── 가상 머신: 땅 위에 집을 따로 지어요 ───────────────────────────
HX = [0.6, 4.4, 8.2]


def vm(ax):
    ground(ax, 0.3, 11.7, 1.3)
    for k, p in enumerate(PARTS):
        house(ax, HX[k], 1.3, 3.2, 3.0, p, kern_hot=True)
    label(ax, 6.0, 6.25, "가상 머신 셋 = 집 세 채 = 커널 셋", fs=11.5, color=RED, bold=True)


# ── 컨테이너 프로그램은 같은 커널에 부탁해요 ─────────────────────
BX, BY, BW, BH = 1.5, 1.0, 9.0, 3.8


def shared(ax):
    cs = building(ax, BX, BY, BW, BH, PARTS, walls=False, kern_hot=True)
    for k, (cx, cy) in enumerate(cs):
        arrow(ax, (cx, cy - 0.35), (cx, BY + 0.8), color=RED, ms=13)
        label(ax, cx, cy + 0.6, f"{230 + k}번", fs=11, color=RED, bold=True)


# ── 칸막이: 리눅스 네임스페이스 ───────────────────────────────────
def ns(ax, step):
    if step == 1:
        cs = building(ax, 0.4, 1.0, 7.4, 3.8, PARTS, walls=False, room_hot=(1,))
        for k in (0, 2):
            ax.annotate("", xy=(cs[k][0], cs[k][1] + 0.35), xytext=(cs[1][0], cs[1][1] + 0.35),
                        arrowprops=dict(arrowstyle="-|>", color=RED, lw=1.6, ls="--"))
        label(ax, 8.3, 4.4, "주문 처리 눈에\n보이는 것", fs=10.5, ha="left", color=RED, bold=True)
        label(ax, 8.3, 3.1, "· 다른 프로그램 목록\n· 다른 프로그램 파일\n· 같은 네트워크 문", fs=10.5,
              ha="left", color=RED)
    else:
        building(ax, 0.4, 1.0, 7.4, 3.8, PARTS, walls=True, wall_hot=True, room_hot=(1,))
        window(ax, 8.2, 1.6, 3.6, 3.6, "주문 처리 칸 안", hot=True)
        label(ax, 8.4, 4.4, "번호", fs=9.5, ha="left", color=INK)
        label(ax, 9.35, 4.4, "프로그램", fs=9.5, ha="left", color=INK)
        ax.plot([8.35, 11.65], [4.2, 4.2], color=INK, lw=0.8)
        rows(ax, 8.3, 3.85, 3.4, [("1", "주문 처리")], hot=(0,))
        label(ax, 10.0, 2.6, "다른 칸: 안 보임", fs=10, color=RED)


# ── 사용량 한도: cgroup ───────────────────────────────────────────
def memrow(ax, use, hot=(), x=0.5, y=5.5):
    """건물 메모리 12칸. use=[(이름, 칸 수)]. hot=빨강 칠할 부품 번호."""
    label(ax, x, y + 0.85, "건물 메모리 12칸", fs=10.5, ha="left", bold=True)
    k = 0
    for i, (name, n) in enumerate(use):
        for j in range(n):
            cell(ax, x + k * 0.9, y, 0.85, 0.6, name[3:] if j == 0 else "", hot=(i in hot), fs=9.5)
            k += 1
    while k < 12:
        ax.add_patch(Rectangle((x + k * 0.9, y), 0.85, 0.6, fc="white", ec=GREY, lw=1.0, ls="--"))
        k += 1


def cg(ax, step):
    if step == 1:
        memrow(ax, [("주문 화면", 2), ("주문 처리", 2), ("주문 장부", 8)], hot=(2,))
        building(ax, 1.5, 0.8, 9.0, 3.5, PARTS, room_hot=(2,), title=None)
        label(ax, 6.0, 4.85, "장부 8칸 · 빈칸 0", fs=10.5, color=RED, bold=True)
    else:
        memrow(ax, [("주문 화면", 2), ("주문 처리", 2), ("주문 장부", 4)])
        for x0, n in ((0.5, 2), (2.3, 2), (4.1, 4)):
            ax.plot([x0 + n * 0.9 - 0.025] * 2, [5.35, 6.25], color=RED, lw=2.4)
        label(ax, 7.85, 6.35, "빨간 선 = 한도", fs=10, ha="left", color=RED, bold=True)
        building(ax, 1.5, 1.0, 9.0, 3.3, ["화면 ≤ 2칸", "처리 ≤ 2칸", "장부 ≤ 4칸"], room_hot=(0, 1, 2), title=None)


# ── 가볍지만 커널을 같이 써요 ─────────────────────────────────────
def compare(ax):
    ground(ax, 0.2, 6.0, 1.5, name="가상 머신")
    for k in range(3):
        house(ax, 0.4 + k * 1.9, 1.5, 1.6, 2.6, "", kern="커널", kern_hot=True)
    for k, p in enumerate(PARTS):
        label(ax, 1.2 + k * 1.9, 3.45, p, fs=9, color="#222")
    building(ax, 6.6, 1.2, 5.1, 3.0, PARTS, title="컨테이너", kern_hot=True, kern="커널", fs=9)
    label(ax, 3.1, 5.5, "커널 3개", fs=11.5, color=RED, bold=True)
    label(ax, 9.15, 5.5, "커널 1개", fs=11.5, color=RED, bold=True)


# ── 판단 (한 장) ──────────────────────────────────────────────────
def decide():
    fig, ax = canvas(10, 4.2, 15, 6.4)
    box(ax, 0.3, 4.6, 6.2, 1.3, fc=NOTE)
    label(ax, 3.4, 5.25, "프로그램 여럿을\n서로 떼어 돌리나요?", fs=10.5, bold=True)
    arrow(ax, (6.6, 5.25), (8.4, 5.25))
    label(ax, 7.5, 5.55, "아니요", fs=10, color=INK)
    box(ax, 8.5, 4.6, 6.2, 1.3, fc=PAPER)
    label(ax, 11.6, 5.25, "그냥 프로그램으로", fs=10.5)
    arrow(ax, (3.4, 4.5), (3.4, 3.5)); label(ax, 3.7, 4.0, "예", fs=10, color=INK, ha="left")
    box(ax, 0.3, 2.1, 6.2, 1.3, fc=NOTE)
    label(ax, 3.4, 2.75, "다른 커널이 필요하거나\n믿을 수 없는 코드인가요?", fs=10.5, bold=True)
    arrow(ax, (6.6, 2.75), (8.4, 2.75)); label(ax, 7.5, 3.05, "예", fs=10, color=INK)
    box(ax, 8.5, 2.1, 6.2, 1.3, fc=PAPER)
    label(ax, 11.6, 2.75, "커널을 따로 주는 방법\n(5·6편)", fs=10.5)
    arrow(ax, (3.4, 2.0), (3.4, 1.3), color=RED); label(ax, 3.7, 1.65, "아니요", fs=10, color=RED, ha="left")
    box(ax, 0.3, 0.1, 6.2, 1.1, fc=PINK, ec=RED)
    label(ax, 3.4, 0.65, "컨테이너", fs=11, color=RED, bold=True)
    save(fig, OUT, "k8s01-decide.svg")


def one(draw, name, size=(7.2, 3.8), lim=(12, 6.6)):
    """한 장 그림."""
    fig, ax = canvas(*size, *lim)
    draw(ax)
    save(fig, OUT, name)


if __name__ == "__main__":
    S, L = (7.2, 3.8), (12, 6.6)
    one(opening, "k8s01-open.svg")
    one(vm, "k8s01-vm.svg")
    one(shared, "k8s01-shared.svg")
    stage(ns, 2, OUT, "k8s01-ns", S, L)
    stage(cg, 2, OUT, "k8s01-cg", S, L)
    one(compare, "k8s01-compare.svg")
    decide()
