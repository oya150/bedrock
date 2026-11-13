"""쿠버네티스 12편 그림 만들기. 실행: python lab/fig_k8s12.py  → docs/kubernetes/img/12/*.svg

예시는 11편의 빵집 주문 장부를 잇는다. 주문 1~3이 이미 있고 주문 4, 5가 새로 들어온다.
노드 A(주문 장부 파드와 엔진), B, C(볼륨 레플리카), D(비어 있다가 재구축 자리).
그림 안 글씨는 낱말과 숫자만 둔다. 지금 볼 곳만 빨강.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "es"))
from figkit import (GREY, INK, LIGHT, NOTE, PAPER, PINK, RED, arrow, box, canvas, cell,  # noqa: E402
                    cylinder, label, outdir, save, stage)
from matplotlib.patches import Rectangle  # noqa: E402

OUT = outdir("12", topic="kubernetes")
NX = {"A": 0.25, "B": 3.2, "C": 6.15, "D": 9.1}
NW, NY, NH = 2.65, 0.4, 3.0


def cross(ax, x, y, s=0.5, color=RED):
    ax.plot([x - s, x + s], [y - s, y + s], color=color, lw=3)
    ax.plot([x - s, x + s], [y + s, y - s], color=color, lw=3)


def node(ax, n, dead=False):
    x = NX[n]
    box(ax, x, NY, NW, NH, fc=LIGHT if dead else "white", ec=GREY if dead else INK, lw=1.5)
    label(ax, x + 0.15, NY + NH - 0.25, f"노드 {n}", fs=10, ha="left", bold=True, color=GREY if dead else INK)


def podbox(ax, n, s="주문 장부 파드", hot=False, dim=False):
    x = NX[n] + 0.15
    c = RED if hot else (GREY if dim else "#222")
    box(ax, x, 2.35, NW - 0.3, 0.6, fc=PINK if hot else ("white" if dim else NOTE),
        ec=RED if hot else (GREY if dim else INK), lw=1.8 if hot else 1.3)
    label(ax, x + (NW - 0.3) / 2, 2.65, s, fs=9.5, color=c)


def engine(ax, n, hot=False, dim=False):
    x = NX[n] + 0.15
    c = RED if hot else (GREY if dim else "#222")
    box(ax, x, 1.75, NW - 0.3, 0.4, fc=PINK if hot else (LIGHT if dim else PAPER),
        ec=RED if hot else (GREY if dim else INK), lw=1.8 if hot else 1.3)
    label(ax, x + (NW - 0.3) / 2, 1.95, "엔진", fs=10, color=c, bold=hot)


def replica(ax, n, k=3, hot=(), dim=False, err=False, title="레플리카", hotbox=False):
    """노드 아래쪽 볼륨 레플리카. k=든 주문 수(1부터), hot=빨간 칸 번호."""
    x, y = NX[n] + 0.12, 0.55
    ec = RED if (hotbox or err) else (GREY if dim else INK)
    box(ax, x, y, NW - 0.24, 0.9, fc=PINK if hotbox else ("white" if not dim else LIGHT), ec=ec,
        lw=1.8 if (hotbox or err) else 1.2)
    label(ax, x + 0.1, y + 0.72, title, fs=8.5, ha="left", color=RED if (hotbox or err) else (GREY if dim else INK))
    for j in range(k):
        cell(ax, x + 0.12 + j * 0.47, y + 0.08, 0.42, 0.45, str(j + 1), hot=(j + 1) in hot, dim=dim, fs=9)
    if err:
        label(ax, x + NW - 0.45, y + 0.72, "오류", fs=9, color=RED, bold=True)


def localdisk(ax, n, rows, hot=False, dim=False, name="디스크"):
    x = NX[n] + 0.35
    c = RED if hot else (GREY if dim else INK)
    cylinder(ax, x, 0.75, NW - 0.7, 0.85, "", fc=PINK if hot else (LIGHT if dim else NOTE), ec=c)
    label(ax, x + (NW - 0.7) / 2, 1.17, rows, fs=9, color=c)
    if not dim:
        label(ax, x + (NW - 0.7) / 2, 2.0, name, fs=9.5, color=c)


def fanout(ax, targets, src="A", color=RED):
    """src 노드의 엔진에서 레플리카들로 가는 화살표. 같은 노드 레플리카는 짧은 아래 화살표."""
    for n in targets:
        if n == src:
            arrow(ax, (NX[n] + 1.32, 1.73), (NX[n] + 1.32, 1.47), color=color, ms=10, lw=1.8)
        else:
            arrow(ax, (NX[src] + 2.5, 1.95), (NX[n] + 2.1, 1.48), color=color, ms=11, lw=1.8, rad=-0.12)


# ── 그림 1: 디스크가 한 노드에만 있으면 그 노드와 함께 멈춰요 ─────────────
def opening():
    fig, ax = canvas(6.6, 2.75, 9.1, 3.8)
    for n in "ABC":
        node(ax, n, dead=(n == "A"))
    podbox(ax, "A", dim=True)
    localdisk(ax, "A", "주문 1, 2, 3", dim=True)
    cross(ax, NX["A"] + NW / 2, NY + NH / 2, s=1.0)
    podbox(ax, "B", s="새 주문 장부 파드", hot=True)
    label(ax, NX["B"] + NW / 2, 1.4, "디스크 없음", fs=11, color=RED, bold=True)
    save(fig, OUT, "k8s12-open.svg")


# ── 그림 2: 가끔 떠 둔 복사본에는 마지막 주문이 없어요 ─────────────────
def copy():
    fig, ax = canvas(7.2, 2.3, 12, 3.8)
    node(ax, "A", dead=True)
    node(ax, "B")
    podbox(ax, "A", dim=True)
    localdisk(ax, "A", "주문 1, 2, 3", dim=True)
    cross(ax, NX["A"] + NW / 2, NY + NH / 2, s=1.0)
    localdisk(ax, "B", "주문 1, 2", hot=True, name="어젯밤 복사본")
    box(ax, 6.4, 0.4, 5.3, 3.0, fc=PAPER)
    label(ax, 9.05, 3.05, "복사본의 주문", fs=10, color=INK, bold=True)
    for j in range(3):
        if j < 2:
            cell(ax, 7.3 + j * 1.2, 1.9, 1.0, 0.7, f"주문 {j + 1}", fs=10)
        else:
            ax.add_patch(Rectangle((7.3 + j * 1.2, 1.9), 1.0, 0.7, fc="white", ec=RED, lw=1.5, ls="--"))
    label(ax, 9.7, 1.4, "주문 3 없음", fs=10.5, color=RED, bold=True)
    save(fig, OUT, "k8s12-copy.svg")


# ── 그림 3: 엔진 하나가 받아 레플리카 모두에 보내요 ─────────────────────
def engine_fig():
    fig, ax = canvas(6.6, 2.75, 9.1, 3.8)
    for n in "ABC":
        node(ax, n)
    podbox(ax, "A")
    engine(ax, "A", hot=True)
    arrow(ax, (NX["A"] + 1.32, 2.33), (NX["A"] + 1.32, 2.17), color=RED, ms=10)
    for n in "ABC":
        replica(ax, n, k=4, hot=(4,))
    fanout(ax, "ABC")
    save(fig, OUT, "k8s12-engine.svg")


# ── 그림 4: 엔진은 파일을 모르고 번호 붙은 칸만 다뤄요 ──────────────────
def block():
    fig, ax = canvas(7.2, 1.9, 12, 3.2)
    box(ax, 0.3, 0.3, 4.6, 2.6, fc="white")
    label(ax, 2.6, 2.55, "데이터베이스가 보는 것", fs=10.5, bold=True, color=INK)
    box(ax, 0.8, 0.65, 3.6, 1.45, fc=NOTE, round_=False)
    label(ax, 2.6, 1.75, "주문 장부 파일", fs=10.5)
    label(ax, 2.6, 1.1, "… 주문 4 크루아상 1개", fs=10, color=RED)
    arrow(ax, (5.0, 1.4), (6.1, 1.4), color=RED, ms=14)
    label(ax, 5.55, 1.85, "운영체제", fs=9.5, color=INK)
    box(ax, 6.2, 0.3, 5.5, 2.6, fc="white")
    label(ax, 8.95, 2.55, "엔진이 보는 것", fs=10.5, bold=True, color=INK)
    for j in range(8):
        cell(ax, 6.5 + j * 0.62, 1.1, 0.55, 0.65, str(j), hot=(j == 5), fs=10)
    label(ax, 8.95, 0.65, "번호 붙은 칸", fs=9.5, color=INK)
    save(fig, OUT, "k8s12-block.svg")


# ── 그림 5~7: 레플리카가 있는 노드가 죽으면 (장면 띠 3장) ────────────────
def fail(ax, step):
    for n in "ABCD":
        node(ax, n, dead=(n == "C"))
    podbox(ax, "A")
    engine(ax, "A")
    replica(ax, "A", k=5, hot=(5,) if step == 1 else ())
    replica(ax, "B", k=5, hot=(5,) if step == 1 else ())
    replica(ax, "C", k=4, dim=step > 1, err=(step == 1))
    cross(ax, NX["C"] + NW / 2, NY + NH / 2 + 0.3, s=0.6, color=RED if step == 1 else GREY)
    if step == 1:
        fanout(ax, "AB")
    elif step == 2:
        replica(ax, "D", k=0, hotbox=True, title="새 레플리카")
        arrow(ax, (NX["B"] + 1.3, 1.55), (NX["D"] + 1.3, 1.55), color=RED, ms=13, rad=-0.3)
    else:
        replica(ax, "D", k=5, hot=(1, 2, 3, 4, 5))


# ── 그림 8: 파드가 있던 노드가 죽으면 새 엔진이 이어 가요 ────────────────
def back():
    fig, ax = canvas(6.6, 2.75, 9.1, 3.8)
    for n in "ABC":
        node(ax, n, dead=(n == "A"))
    podbox(ax, "A", dim=True)
    engine(ax, "A", dim=True)
    replica(ax, "A", k=3, dim=True)
    cross(ax, NX["A"] + NW / 2, NY + NH / 2, s=1.0, color=GREY)
    podbox(ax, "B", s="새 주문 장부 파드", hot=True)
    engine(ax, "B", hot=True)
    replica(ax, "B")
    replica(ax, "C")
    fanout(ax, "BC", src="B")
    save(fig, OUT, "k8s12-back.svg")


# ── 그림 9: 판단 ───────────────────────────────────────────────────
def decide():
    fig, ax = canvas(10, 4.2, 15, 6.4)
    box(ax, 0.3, 4.6, 6.0, 1.3, fc=NOTE)
    label(ax, 3.3, 5.25, "노드가 고장 나도 남아야 하나요?", fs=10.5, bold=True)
    arrow(ax, (6.4, 5.25), (8.4, 5.25))
    label(ax, 7.4, 5.55, "아니요", fs=10, color=INK)
    box(ax, 8.5, 4.6, 6.2, 1.3, fc=PAPER)
    label(ax, 11.6, 5.25, "노드 자기 디스크", fs=10.5)
    arrow(ax, (3.3, 4.5), (3.3, 3.5))
    label(ax, 3.6, 4.0, "예", fs=10, color=INK, ha="left")
    box(ax, 0.3, 2.2, 6.0, 1.2, fc=NOTE)
    label(ax, 3.3, 2.8, "저장 장치가 복사본을 두나요?", fs=10.5, bold=True)
    arrow(ax, (6.4, 2.8), (8.4, 2.8))
    label(ax, 7.4, 3.1, "예", fs=10, color=INK)
    box(ax, 8.5, 2.2, 6.2, 1.2, fc=PAPER)
    label(ax, 11.6, 2.8, "그 저장 장치의 CSI 드라이버", fs=10.5)
    arrow(ax, (3.3, 2.1), (3.3, 1.3), color=RED)
    label(ax, 3.6, 1.7, "아니요 (노드 디스크뿐)", fs=10, color=RED, ha="left")
    box(ax, 0.3, 0.1, 6.0, 1.1, fc=PINK, ec=RED)
    label(ax, 3.3, 0.65, "Longhorn", fs=11.5, color=RED, bold=True)
    save(fig, OUT, "k8s12-decide.svg")


if __name__ == "__main__":
    opening()
    copy()
    engine_fig()
    block()
    stage(fail, 3, OUT, "k8s12-fail", (7.2, 2.3), (12, 3.8))
    back()
    decide()
