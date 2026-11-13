"""쿠버네티스 11편 그림 만들기. 실행: python lab/fig_k8s11.py  → docs/kubernetes/img/11/*.svg

예시는 빵집 주문 앱의 주문 장부(데이터베이스). 주문 3건: 크루아상 2개, 식빵 1개, 단팥빵 3개.
신청서(PVC)는 주문 장부 · 10Gi · 한 노드에서 읽고 쓰기.
그림 안 글씨는 낱말과 숫자만 둔다. 지금 볼 곳만 빨강.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "es"))
from figkit import (GREY, INK, NOTE, PAPER, PINK, RED, arrow, box, canvas, cell,  # noqa: E402
                    cylinder, label, outdir, save, stage)
from matplotlib.patches import Rectangle  # noqa: E402

OUT = outdir("11", topic="kubernetes")
ORDERS = ["크루아상 2", "식빵 1", "단팥빵 3"]


def cross(ax, x, y, s=0.5, color=RED):
    ax.plot([x - s, x + s], [y - s, y + s], color=color, lw=3)
    ax.plot([x - s, x + s], [y + s, y - s], color=color, lw=3)


def pod(ax, x, y, w, h, name="주문 장부 파드", hot=False, dim=False):
    ec = RED if hot else (GREY if dim else INK)
    box(ax, x, y, w, h, fc=PINK if hot else ("white" if dim else NOTE), ec=ec, lw=2.0 if hot else 1.5)
    label(ax, x + w / 2, y + h - 0.3, name, fs=10.5, color=RED if hot else (GREY if dim else "#222"), bold=True)


def disk(ax, x, y, name, hot=False, dim=False, w=2.6, h=1.3):
    c = RED if hot else (GREY if dim else INK)
    cylinder(ax, x, y, w, h, name, fc=PINK if hot else NOTE, ec=c, color=c)
    label(ax, x + w / 2, y + h / 2, "주문 1, 2, 3", fs=10.5, color=c)


# ── 그림 1: 컨테이너 안에 적은 주문은 파드와 함께 사라져요 ───────────────
def lost():
    fig, ax = canvas(7.2, 3.4, 12, 5.6)

    def side(x, name, full):
        pod(ax, x, 0.4, 4.6, 4.8, name=name, hot=not full)
        box(ax, x + 0.4, 0.8, 3.8, 3.6, fc="white", lw=1.2)
        label(ax, x + 2.3, 4.05, "컨테이너", fs=10, color=INK)
        for k, s in enumerate(ORDERS):
            y = 3.0 - k * 0.95
            if full:
                cell(ax, x + 0.8, y, 3.0, 0.75, s, fs=10.5)
            else:
                ax.add_patch(Rectangle((x + 0.8, y), 3.0, 0.75, fc="white", ec=RED, lw=1.4, ls="--"))

    side(0.3, "주문 장부 파드", True)
    side(7.1, "새 파드", False)
    arrow(ax, (5.1, 2.8), (6.9, 2.8), color=RED, ms=16)
    label(ax, 6.0, 3.3, "다시 뜸", fs=10.5, color=RED, bold=True)
    save(fig, OUT, "k8s11-lost.svg")


# ── 그림 2: 파드 바깥의 디스크는 남아요 ────────────────────────────────
def outside():
    fig, ax = canvas(7.2, 3.8, 12, 6.6)
    pod(ax, 0.4, 3.9, 4.4, 2.2, name="지워진 파드", dim=True)
    cross(ax, 2.6, 4.75, s=0.55)
    pod(ax, 7.2, 3.9, 4.4, 2.2, name="새 파드", hot=True)
    label(ax, 9.4, 4.75, "컨테이너", fs=10, color=RED)
    disk(ax, 4.7, 0.6, "디스크 (파드 바깥)", hot=True)
    ax.plot([2.6, 4.65], [3.85, 1.4], color=GREY, lw=2, ls="--")
    ax.plot([9.4, 7.35], [3.85, 1.4], color=RED, lw=3.5)
    label(ax, 9.6, 2.3, "다시 붙임", fs=10.5, color=RED, bold=True)
    save(fig, OUT, "k8s11-outside.svg")


# ── 그림 3: 신청서와 디스크 짝짓기 ─────────────────────────────────────
def pvc(ax, x, y, hot=False, w=4.3, h=3.4):
    ec, c = (RED, RED) if hot else (INK, "#222")
    box(ax, x, y, w, h, fc=PINK if hot else "white", ec=ec, lw=2.0 if hot else 1.5, round_=False)
    label(ax, x + 0.3, y + h - 0.45, "PVC (디스크 신청서)", fs=11.5, ha="left", bold=True, color=c)
    for k, s in enumerate(["이름: 주문 장부", "크기: 10Gi", "한 노드에서 읽고 쓰기"]):
        label(ax, x + 0.4, y + h - 1.25 - k * 0.65, s, fs=10.5, ha="left", color=c)


def claim():
    fig, ax = canvas(7.2, 3.4, 12, 5.8)
    pvc(ax, 0.4, 1.0)
    label(ax, 9.6, 5.3, "이미 있는 PV", fs=10.5, color=INK, bold=True)
    cell(ax, 7.9, 3.5, 3.4, 1.1, "PV · 5Gi", dim=True, fs=11.5)
    cell(ax, 7.9, 1.0, 3.4, 1.1, "PV · 20Gi", hot=True, fs=11.5)
    label(ax, 6.3, 4.2, "작음 ✗", fs=11, color=INK)
    ax.plot([4.75, 7.85], [2.4, 1.55], color=RED, lw=4)
    label(ax, 6.3, 2.35, "짝", fs=11.5, color=RED, bold=True)
    save(fig, OUT, "k8s11-claim.svg")


# ── 그림 4: 맞는 디스크가 없으면 CSI 드라이버가 만들어요 ─────────────────
def step_no(ax, x, y, n):
    label(ax, x, y, n, fs=12, color=RED, bold=True)


def dynamic():
    fig, ax = canvas(7.2, 3.8, 12, 6.6)
    pvc(ax, 0.3, 3.2, w=4.0, h=3.0)
    box(ax, 0.3, 0.4, 4.0, 1.5, fc=PAPER)
    label(ax, 2.3, 1.4, "StorageClass", fs=11, bold=True)
    label(ax, 2.3, 0.8, "만드는 쪽: CSI 드라이버", fs=10, color=INK)
    arrow(ax, (2.3, 3.1), (2.3, 2.0), color=RED, ms=14)
    step_no(ax, 2.75, 2.55, "①")
    box(ax, 4.9, 0.65, 2.6, 1.0, fc=NOTE)
    label(ax, 6.2, 1.15, "CSI 드라이버", fs=11, bold=True)
    arrow(ax, (4.35, 1.15), (4.85, 1.15), color=RED, ms=14)
    step_no(ax, 4.6, 1.8, "②")
    box(ax, 8.0, 0.3, 3.6, 2.7, fc="white")
    label(ax, 9.8, 2.65, "저장 장치", fs=10.5, color=INK, bold=True)
    cylinder(ax, 8.7, 0.8, 2.2, 1.0, "", fc=PINK, ec=RED)
    label(ax, 9.8, 1.3, "새 디스크", fs=10.5, color=RED)
    arrow(ax, (7.55, 1.15), (8.6, 1.15), color=RED, ms=14)
    step_no(ax, 7.75, 1.65, "③")
    cell(ax, 8.2, 4.6, 3.2, 1.1, "PV · 10Gi", hot=True, fs=11.5)
    arrow(ax, (9.8, 3.05), (9.8, 4.5), color=RED, ms=14)
    step_no(ax, 10.25, 3.75, "④")
    ax.plot([4.35, 8.15], [5.0, 5.15], color=RED, lw=4)
    label(ax, 6.2, 5.45, "짝", fs=11.5, color=RED, bold=True)
    save(fig, OUT, "k8s11-dynamic.svg")


# ── 그림 5~7: 파드가 뜬 노드에 디스크를 붙여요 (장면 띠 3장) ─────────────
NODES = {"A": 0.3, "B": 4.1}


def attach(ax, step):
    for n, x in NODES.items():
        box(ax, x, 3.5, 3.4, 2.8, fc="white")
        label(ax, x + 0.25, 6.0, f"노드 {n}", fs=10.5, ha="left", bold=True, color=INK)
    box(ax, 0.3, 0.3, 7.2, 2.4, fc="white")
    label(ax, 0.55, 2.4, "저장 장치", fs=10.5, ha="left", bold=True, color=INK)
    cylinder(ax, 2.7, 0.75, 2.4, 1.1, "", fc=NOTE)
    label(ax, 3.9, 1.3, "PV · 주문 장부", fs=10.5)
    box(ax, 8.4, 4.4, 3.2, 1.0, fc=PAPER)
    label(ax, 10.0, 4.9, "CSI 드라이버", fs=11, bold=True)
    if step == 1:
        pod(ax, 0.7, 4.0, 2.6, 1.6, hot=True)
        ax.plot([3.4, 2.0], [1.95, 3.95], color=RED, lw=3.5)
        label(ax, 10.0, 2.6, "A에 붙임", fs=12, color=RED, bold=True)
    elif step == 2:
        pod(ax, 0.7, 4.0, 2.6, 1.6, dim=True)
        cross(ax, 2.0, 4.6, s=0.4)
        pod(ax, 4.5, 4.0, 2.6, 1.6, name="새 파드", hot=True)
        ax.plot([3.4, 2.0], [1.95, 3.95], color=GREY, lw=3.5)
        label(ax, 5.8, 4.55, "?", fs=16, color=RED, bold=True)
        label(ax, 10.0, 2.6, "아직 A에 붙어 있음", fs=12, color=RED, bold=True)
    else:
        pod(ax, 4.5, 4.0, 2.6, 1.6, name="새 파드", hot=True)
        ax.plot([3.4, 2.0], [1.95, 3.95], color=GREY, lw=1.5, ls="--")
        ax.plot([4.4, 5.8], [1.95, 3.95], color=RED, lw=3.5)
        label(ax, 10.0, 2.6, "A에서 뗌 → B에 붙임", fs=12, color=RED, bold=True)


# ── 그림 8: 판단 ───────────────────────────────────────────────────
def decide():
    fig, ax = canvas(10, 4.2, 15, 6.4)
    box(ax, 0.3, 4.6, 6.0, 1.3, fc=NOTE)
    label(ax, 3.3, 5.25, "파드가 사라져도 남아야 하나요?", fs=10.5, bold=True)
    arrow(ax, (6.4, 5.25), (8.4, 5.25))
    label(ax, 7.4, 5.55, "아니요", fs=10, color=INK)
    box(ax, 8.5, 4.6, 6.2, 1.3, fc=PAPER)
    label(ax, 11.6, 5.25, "컨테이너 안 (임시 파일)", fs=10.5)
    arrow(ax, (3.3, 4.5), (3.3, 3.5))
    label(ax, 3.6, 4.0, "예", fs=10, color=INK, ha="left")
    box(ax, 0.3, 2.2, 6.0, 1.2, fc=NOTE)
    label(ax, 3.3, 2.8, "여러 노드에서 동시에 고치나요?", fs=10.5, bold=True)
    arrow(ax, (6.4, 2.8), (8.4, 2.8))
    label(ax, 7.4, 3.1, "예", fs=10, color=INK)
    box(ax, 8.5, 2.2, 6.2, 1.2, fc=PAPER)
    label(ax, 11.6, 2.8, "함께 쓰는 저장소 (ReadWriteMany)", fs=10.5)
    arrow(ax, (3.3, 2.1), (3.3, 1.3), color=RED)
    label(ax, 3.6, 1.7, "아니요", fs=10, color=RED, ha="left")
    box(ax, 0.3, 0.1, 6.0, 1.1, fc=PINK, ec=RED)
    label(ax, 3.3, 0.65, "PVC (ReadWriteOnce)", fs=11, color=RED, bold=True)
    save(fig, OUT, "k8s11-decide.svg")


if __name__ == "__main__":
    lost()
    outside()
    claim()
    dynamic()
    stage(attach, 3, OUT, "k8s11-attach", (7.2, 3.8), (12, 6.6))
    decide()
