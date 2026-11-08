"""쿠버네티스 11편 그림 만들기. 실행: python lab/fig_k8s11.py  → docs/kubernetes/img/11/*.svg

본문 절은 장면 띠로 그린다: 같은 무대를 여러 장 그리고 장마다 바뀐 곳만 빨강으로 칠한다.
예시는 빵집 주문 앱의 주문 장부(데이터베이스). 주문 3건: 크루아상 2개, 식빵 1개, 단팥빵 3개.
신청서(PVC)는 주문 장부 · 10Gi · 한 노드에서 읽고 쓰기.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "es"))
from figkit import (GREY, INK, LIGHT, NOTE, PAPER, PINK, RED, arrow, box, bubble,  # noqa: E402
                    canvas, cell, cylinder, label, moral, outdir, save, stage)
from matplotlib.patches import Rectangle  # noqa: E402

OUT = outdir("11", topic="kubernetes")
ORDERS = ["1   크루아상 2개", "2   식빵 1개", "3   단팥빵 3개"]
CYL = (8.4, 3.1, 3.2, 1.5)
SAY = (7.3, 0.6, 4.6, 1.35)
TAIL = (10.0, 2.85)


def empty(ax, x, y, w, h):
    ax.add_patch(Rectangle((x, y), w, h, fc="white", ec=GREY, lw=1.0, ls="--"))


def cross(ax, x, y, s=0.5, color=RED):
    ax.plot([x - s, x + s], [y - s, y + s], color=color, lw=3)
    ax.plot([x - s, x + s], [y + s, y - s], color=color, lw=3)


def pod(ax, x, y, w, h, name="주문 장부 파드", hot=False, dim=False):
    ec = RED if hot else (GREY if dim else INK)
    box(ax, x, y, w, h, fc=PINK if hot else ("white" if dim else NOTE), ec=ec, lw=2.0 if hot else 1.5)
    label(ax, x + w / 2, y + h - 0.3, name, fs=10.5, color=RED if hot else (GREY if dim else "#222"), bold=True)


def disk(ax, x, y, name, rows=3, hot=False, dim=False, w=2.6, h=1.3):
    c = RED if hot else (GREY if dim else INK)
    cylinder(ax, x, y, w, h, name, fc=PINK if hot else NOTE, ec=c, color=c)
    if rows:
        label(ax, x + w / 2, y + h / 2, "주문 " + ", ".join(str(k + 1) for k in range(rows)), fs=10.5, color=c)


# ── 주문 장부 화면 ──────────────────────────────────────────────────
def screen(ax, rows="on", hot=False, tag=None):
    """rows: on=주문 3건, miss=빈 줄 ✗, grey=흐리게."""
    box(ax, 0.5, 0.9, 6.2, 5.4, fc="white", round_=False)
    ax.add_patch(Rectangle((0.5, 5.85), 6.2, 0.45, fc=LIGHT, ec=INK, lw=1.2))
    label(ax, 0.7, 6.07, "빵집 주문 장부 · 오늘 들어온 주문", fs=11, ha="left", color=INK)
    for k, s in enumerate(ORDERS):
        y = 5.0 - k * 0.75
        if rows == "miss":
            ax.add_patch(Rectangle((0.8, y - 0.27), 5.6, 0.54, fill=False, ec=RED, lw=1.5, ls="--"))
            label(ax, 6.05, y, "✗", fs=13, color=RED, bold=True)
            continue
        if hot:
            ax.add_patch(Rectangle((0.8, y - 0.27), 5.6, 0.54, fc=PINK, ec=RED, lw=1.8))
        else:
            ax.plot([0.8, 6.4], [y - 0.3, y - 0.3], color=GREY, lw=0.8)
        label(ax, 1.0, y, s, fs=11.5, ha="left", color=RED if hot else (GREY if rows == "grey" else "#222"),
              bold=hot)
    if tag:
        label(ax, 3.6, 1.35, tag, fs=10.5, color=RED, bold=True,
              bbox=dict(boxstyle="round,pad=0.3", fc=PINK, ec=RED, lw=1.4))


def db(ax):
    cylinder(ax, *CYL, "데이터베이스")


def opening(ax, step):
    db(ax)
    if step == 1:
        screen(ax)
        bubble(ax, *SAY, "주문 3건을\n장부에 적어 뒀어요", TAIL, hot=True)
    elif step == 2:
        screen(ax, rows="grey", tag="주문 장부 파드가 다시 떴어요")
        bubble(ax, *SAY, "방금 새로\n시작했어요", TAIL, hot=True)
    else:
        screen(ax, rows="miss")
        bubble(ax, *SAY, "장부를 열어 보니\n적힌 주문이 없어요", TAIL, hot=True)
        moral(ax, 3.6, 0.35, "파드가 다시 뜨자 주문이 사라졌어요")


# ── 1절: 컨테이너 안 파일은 파드와 함께 사라져요 ──────────────────────
def node1(ax, w=7.0):
    box(ax, 0.3, 0.9, w, 5.4, fc="white")
    label(ax, 0.6, 6.0, "노드 (컴퓨터 한 대)", fs=10.5, ha="left", color=INK, bold=True)


def ctrl(ax, s, hot):
    box(ax, 8.6, 4.6, 3.0, 1.0, fc=PAPER)
    label(ax, 10.1, 5.1, "컨트롤러", fs=11, bold=True)
    bubble(ax, 7.9, 2.4, 4.0, 1.4, s, (10.1, 4.5), hot=hot, fs=10.5)


def inside(ax, step):
    node1(ax)
    if step == 2:
        pod(ax, 1.0, 1.4, 5.6, 4.1, dim=True)
        box(ax, 1.5, 1.8, 4.6, 2.9, fc="white", ec=GREY, lw=1.2)
        label(ax, 3.8, 4.35, "컨테이너", fs=10, color=GREY)
        for k in range(3):
            cell(ax, 1.9 + k * 1.35, 2.5, 1.2, 0.8, f"주문 {k + 1}", dim=True, fs=10)
        cross(ax, 3.8, 3.4, s=1.0)
        label(ax, 3.8, 1.15, "파드가 지워졌어요", fs=11, color=RED, bold=True)
        ctrl(ax, "주문 장부 파드가\n하나 모자라요", hot=True)
        return
    pod(ax, 1.0, 1.4, 5.6, 4.1, name="새 주문 장부 파드" if step == 3 else "주문 장부 파드", hot=(step == 3))
    box(ax, 1.5, 1.8, 4.6, 2.9, fc="white", lw=1.2)
    label(ax, 3.8, 4.35, "컨테이너", fs=10, color=INK)
    for k in range(3):
        if step == 1:
            cell(ax, 1.9 + k * 1.35, 2.5, 1.2, 0.8, f"주문 {k + 1}", hot=True, fs=10)
        else:
            ax.add_patch(Rectangle((1.9 + k * 1.35, 2.5), 1.2, 0.8, fc="white", ec=RED, lw=1.4, ls="--"))
    if step == 1:
        label(ax, 3.8, 2.05, "컨테이너 안에 적어요", fs=10, color=RED)
        ctrl(ax, "파드가 하나 있어요\n그대로 둬요", hot=False)
    else:
        label(ax, 3.8, 2.05, "새 컨테이너는 비어 있어요", fs=10, color=RED, bold=True)
        ctrl(ax, "새 파드를\n하나 만들었어요", hot=False)
        moral(ax, 6.0, 0.4, "컨테이너 안 파일은 파드와 함께 사라져요")


# ── 2절: 파드 바깥의 디스크 ─────────────────────────────────────────
def outside(ax, step):
    node1(ax, w=6.6)
    label(ax, 10.0, 6.0, "파드 바깥", fs=10.5, color=INK, bold=True)
    if step == 2:
        pod(ax, 0.8, 2.2, 5.4, 3.2, dim=True)
        cross(ax, 3.5, 3.6, s=0.9)
        label(ax, 3.5, 1.55, "파드가 지워졌어요", fs=10.5, color=INK)
        disk(ax, 8.7, 2.3, "디스크", hot=True)
        label(ax, 10.0, 1.6, "디스크는 그대로 남아요", fs=10.5, color=RED, bold=True)
        return
    on3 = step == 3
    pod(ax, 0.8, 2.2, 5.4, 3.2, name="새 주문 장부 파드" if on3 else "주문 장부 파드", hot=on3)
    box(ax, 1.2, 2.6, 4.6, 1.9, fc="white", lw=1.2)
    label(ax, 3.5, 3.55, "컨테이너", fs=10, color=INK)
    arrow(ax, (5.85, 3.55), (8.6, 3.0), color=RED, ms=14, style="<|-|>")
    disk(ax, 8.7, 2.3, "디스크", hot=(step == 1))
    if step == 1:
        label(ax, 10.0, 1.6, "파드 바깥에 따로 있어요", fs=10.5, color=RED, bold=True)
        label(ax, 7.75, 3.85, "빌려 써요", fs=10, color=RED)
    else:
        label(ax, 7.75, 3.85, "다시 붙여요", fs=10, color=RED, bold=True)
        moral(ax, 6.0, 0.4, "파드가 바뀌어도 같은 디스크를 다시 붙여요")


# ── 3절: 신청서와 디스크 짝짓기 ─────────────────────────────────────
def pvc(ax, x, y, hot=False, w=4.3, h=3.4, dim=False):
    ec = RED if hot else (GREY if dim else INK)
    c = RED if hot else (GREY if dim else "#222")
    box(ax, x, y, w, h, fc=PINK if hot else "white", ec=ec, lw=2.0 if hot else 1.5, round_=False)
    label(ax, x + 0.3, y + h - 0.45, "PVC (디스크 신청서)", fs=11.5, ha="left", bold=True, color=c)
    for k, s in enumerate(["이름: 주문 장부", "크기: 10Gi", "한 노드에서 읽고 쓰기"]):
        label(ax, x + 0.4, y + h - 1.25 - k * 0.65, s, fs=10.5, ha="left", color=c)


def pvbox(ax, x, y, s, hot=False, dim=False, w=3.4, h=1.1):
    cell(ax, x, y, w, h, s, hot=hot, dim=dim, fs=11.5)


def claim(ax, step):
    pvc(ax, 0.4, 2.0, hot=(step == 1))
    label(ax, 9.6, 6.05, "이미 있는 PV", fs=10.5, color=INK, bold=True)
    pvbox(ax, 7.9, 4.2, "PV · 5Gi", dim=(step == 3))
    pvbox(ax, 7.9, 2.0, "PV · 20Gi", hot=(step == 3))
    if step == 2:
        arrow(ax, (4.8, 4.2), (7.8, 4.75), color=RED, ms=13)
        arrow(ax, (4.8, 3.2), (7.8, 2.55), color=RED, ms=13)
        label(ax, 6.3, 5.0, "작아요 ✗", fs=11, color=RED, bold=True)
        label(ax, 6.3, 2.35, "충분해요 ✓", fs=11, color=RED, bold=True)
    if step == 3:
        ax.plot([4.75, 7.85], [3.0, 2.55], color=RED, lw=4)
        label(ax, 6.3, 3.25, "짝지었어요", fs=11, color=RED, bold=True)
        moral(ax, 6.0, 0.6, "신청서 하나에 디스크 하나를 짝지어요")


# ── 4절: 맞는 디스크가 없으면 CSI 드라이버가 만들어요 ─────────────────
def dynamic(ax, step):
    pvc(ax, 0.3, 2.7, hot=(step == 1), w=4.0, h=3.2)
    box(ax, 0.3, 0.55, 4.0, 1.5, fc=PAPER)
    label(ax, 2.3, 1.55, "StorageClass", fs=11, bold=True, color=RED if step == 2 else "#222")
    label(ax, 2.3, 0.95, "만드는 쪽: CSI 드라이버", fs=10, color=RED if step == 2 else INK)
    on2 = step == 2
    box(ax, 4.9, 1.05, 2.6, 1.0, fc=PINK if on2 else NOTE, ec=RED if on2 else INK)
    label(ax, 6.2, 1.55, "CSI 드라이버", fs=11, bold=True, color=RED if on2 else "#222")
    label(ax, 9.8, 6.1, "PV", fs=11, bold=True, color=INK)
    if step < 3:
        empty(ax, 8.2, 4.6, 3.2, 1.1)
    else:
        pvbox(ax, 8.2, 4.6, "PV · 10Gi", hot=True, w=3.2)
        ax.plot([4.35, 8.15], [4.6, 5.15], color=RED, lw=4)
        label(ax, 6.2, 5.25, "짝지었어요", fs=10.5, color=RED, bold=True)
    if step == 1:
        label(ax, 9.8, 4.25, "맞는 PV가 없어요", fs=10.5, color=RED, bold=True)
    box(ax, 8.0, 0.4, 3.6, 3.2, fc="white")
    label(ax, 9.8, 3.25, "저장 장치", fs=10.5, color=INK, bold=True)
    if step >= 2:
        cylinder(ax, 8.7, 0.95, 2.2, 1.2, "", fc=PINK if on2 else NOTE, ec=RED if on2 else INK)
        label(ax, 9.8, 1.55, "새 디스크", fs=10.5, color=RED if on2 else "#222")
    if on2:
        arrow(ax, (7.55, 1.55), (8.6, 1.55), color=RED, ms=14)
        label(ax, 6.2, 2.5, "새로 만들어요", fs=10.5, color=RED, bold=True)
    if step == 3:
        arrow(ax, (9.8, 3.65), (9.8, 4.5), color=GREY, ms=12)
        moral(ax, 6.15, 3.0, "신청서를 내면\nCSI 드라이버가\n디스크를 만들어요", fs=11.5)


# ── 5절: 파드가 뜬 노드에 디스크를 붙여요 ───────────────────────────
NODES = {"A": 0.3, "B": 4.1}


def nodebox(ax, n):
    x = NODES[n]
    box(ax, x, 3.5, 3.4, 2.8, fc="white")
    label(ax, x + 0.25, 6.0, f"노드 {n}", fs=10.5, ha="left", bold=True, color=INK)


def attach(ax, step):
    for n in NODES:
        nodebox(ax, n)
    box(ax, 0.3, 0.3, 7.2, 2.4, fc="white")
    label(ax, 0.55, 2.4, "저장 장치", fs=10.5, ha="left", bold=True, color=INK)
    cylinder(ax, 2.7, 0.75, 2.4, 1.1, "", fc=NOTE)
    label(ax, 3.9, 1.3, "PV · 주문 장부", fs=10.5)
    box(ax, 8.4, 4.9, 3.2, 1.0, fc=PAPER)
    label(ax, 10.0, 5.4, "CSI 드라이버", fs=11, bold=True)
    if step == 1:
        pod(ax, 0.7, 4.0, 2.6, 1.6, name="주문 장부 파드", hot=True)
        ax.plot([3.4, 2.0], [1.95, 3.95], color=RED, lw=3.5)
        bubble(ax, 7.9, 1.6, 4.0, 1.6, "파드가 뜬 노드 A에\n디스크를 붙였어요", (10.0, 4.8), hot=True, fs=10.5)
    elif step == 2:
        pod(ax, 0.7, 4.0, 2.6, 1.6, dim=True)
        cross(ax, 2.0, 4.8, s=0.55)
        pod(ax, 4.5, 4.0, 2.6, 1.6, name="새 주문 장부 파드", hot=True)
        ax.plot([3.4, 2.0], [1.95, 3.95], color=GREY, lw=3.5)
        label(ax, 4.9, 3.1, "아직 A에 붙어 있어요", fs=10, color=RED, bold=True)
        bubble(ax, 7.9, 1.6, 4.0, 1.6, "B에 붙이려면\nA에서 먼저 떼야 해요", (10.0, 4.8), hot=True, fs=10.5)
    else:
        pod(ax, 4.5, 4.0, 2.6, 1.6, name="새 주문 장부 파드")
        ax.plot([3.4, 2.0], [1.95, 3.95], color=GREY, lw=1.5, ls="--")
        ax.plot([4.4, 5.8], [1.95, 3.95], color=RED, lw=3.5)
        bubble(ax, 7.9, 1.6, 4.0, 1.6, "A에서 떼고\nB에 붙였어요", (10.0, 4.8), hot=True, fs=10.5)
        moral(ax, 9.9, 0.8, "디스크는 파드를 따라\n노드를 옮겨요")


# ── 판단 (한 장) ───────────────────────────────────────────────────
def decide():
    fig, ax = canvas(10, 4.2, 15, 6.4)
    box(ax, 0.3, 4.6, 6.0, 1.3, fc=NOTE)
    label(ax, 3.3, 5.25, "파드가 사라져도 남아야 하나요?", fs=10.5, bold=True)
    arrow(ax, (6.4, 5.25), (8.4, 5.25))
    label(ax, 7.4, 5.55, "아니요", fs=10, color=INK)
    box(ax, 8.5, 4.6, 6.2, 1.3, fc=PAPER)
    label(ax, 11.6, 5.25, "컨테이너 안에 둬요 (임시 파일)", fs=10.5)
    arrow(ax, (3.3, 4.5), (3.3, 3.5)); label(ax, 3.6, 4.0, "예", fs=10, color=INK, ha="left")
    box(ax, 0.3, 2.2, 6.0, 1.2, fc=NOTE)
    label(ax, 3.3, 2.8, "여러 노드의 파드가 동시에 고치나요?", fs=10.5, bold=True)
    arrow(ax, (6.4, 2.8), (8.4, 2.8)); label(ax, 7.4, 3.1, "예", fs=10, color=INK)
    box(ax, 8.5, 2.2, 6.2, 1.2, fc=PAPER)
    label(ax, 11.6, 2.8, "함께 쓰는 저장소 (ReadWriteMany)", fs=10.5)
    arrow(ax, (3.3, 2.1), (3.3, 1.3), color=RED); label(ax, 3.6, 1.7, "아니요, 한 파드가 써요", fs=10, color=RED, ha="left")
    box(ax, 0.3, 0.1, 6.0, 1.1, fc=PINK, ec=RED)
    label(ax, 3.3, 0.65, "PVC로 디스크를 신청해요 (ReadWriteOnce)", fs=10.5, color=RED, bold=True)
    save(fig, OUT, "k8s11-decide.svg")


# ── 정리: 처음 장면으로 돌아가기 ───────────────────────────────────
def back(ax, step):
    db(ax)
    if step == 1:
        screen(ax, rows="miss")
        bubble(ax, *SAY, "그때는 주문이\n파드와 함께 사라졌어요", TAIL)
    elif step == 2:
        screen(ax, rows="grey", tag="+ PVC: 주문 장부")
        bubble(ax, *SAY, "다시 떴어요\n같은 PV를 붙였어요", TAIL, hot=True)
    else:
        screen(ax, hot=True)
        bubble(ax, *SAY, "장부를 열어 보니\n주문 3건이 그대로예요", TAIL, hot=True)
        moral(ax, 3.6, 0.35, "PVC로 받은 디스크는 파드가 바뀌어도 남아요")


# ── 정리: 낱말 카드 ────────────────────────────────────────────────
def cards():
    fig, ax = canvas(6.4, 7.9, 9.8, 12.2)
    W, H = 4.6, 3.8

    def card(i, name, line):
        col, row = i % 2, i // 2
        x, y = 0.2 + col * 4.9, 8.2 - row * 4.05
        box(ax, x, y, W, H, fc="white")
        label(ax, x + 0.25, y + H - 0.4, name, fs=12.5, ha="left", bold=True)
        label(ax, x + W / 2, y + 0.6, line, fs=10, color=INK)
        return x, y

    x, y = card(0, "PV", "실제로 붙는 디스크\n파드와 따로 살아요")
    cylinder(ax, x + 1.5, y + 1.45, 1.6, 0.8, "", fc=PINK, ec=RED)
    x, y = card(1, "PVC", "이만큼 필요하다고 적어 내는\n디스크 신청서")
    box(ax, x + 1.1, y + 1.35, 2.4, 1.45, fc=PINK, ec=RED, round_=False)
    label(ax, x + 2.3, y + 2.3, "주문 장부", fs=10, color=RED)
    label(ax, x + 2.3, y + 1.75, "10Gi", fs=10, color=RED)
    x, y = card(2, "StorageClass", "어떤 디스크를 누가 만들지\n적어 둔 종류표")
    cell(ax, x + 0.6, y + 1.6, 3.4, 0.9, "만드는 쪽: CSI 드라이버", fc=PAPER, fs=9.5)
    x, y = card(3, "CSI 드라이버", "디스크를 만들어\n파드가 뜬 노드에 붙이는 플러그인")
    cell(ax, x + 0.3, y + 1.6, 1.9, 0.8, "CSI 드라이버", fc=NOTE, fs=9.5)
    arrow(ax, (x + 2.3, y + 2.0), (x + 2.9, y + 2.0), color=RED, ms=11)
    cylinder(ax, x + 3.0, y + 1.6, 1.2, 0.6, "", fc=PINK, ec=RED)
    x, y = card(4, "동적 프로비저닝", "맞는 PV가 없으면\n신청서를 보고 새로 만들기")
    cell(ax, x + 0.4, y + 1.6, 1.4, 0.8, "PVC", fc="white", fs=10)
    arrow(ax, (x + 1.9, y + 2.0), (x + 2.6, y + 2.0), color=RED, ms=11)
    cell(ax, x + 2.7, y + 1.6, 1.5, 0.8, "새 PV", hot=True, fs=10)
    x, y = card(5, "ReadWriteOnce", "한 번에 한 노드에만 붙여\n읽고 쓰기")
    cell(ax, x + 0.4, y + 2.1, 1.5, 0.6, "노드 A", fc="white", fs=9.5)
    cell(ax, x + 2.7, y + 2.1, 1.5, 0.6, "노드 B", dim=True, fs=9.5)
    cylinder(ax, x + 1.7, y + 1.25, 1.2, 0.45, "", fc=NOTE)
    ax.plot([x + 2.0, x + 1.4], [y + 1.75, y + 2.05], color=RED, lw=2.5)
    save(fig, OUT, "k8s11-cards.svg")


if __name__ == "__main__":
    S, L = (7.2, 3.8), (12, 6.6)
    stage(opening, 3, OUT, "k8s11-open", S, L)
    stage(inside, 3, OUT, "k8s11-inside", S, L)
    stage(outside, 3, OUT, "k8s11-outside", S, L)
    stage(claim, 3, OUT, "k8s11-claim", S, L)
    stage(dynamic, 3, OUT, "k8s11-dynamic", S, L)
    stage(attach, 3, OUT, "k8s11-attach", S, L)
    decide()
    stage(back, 3, OUT, "k8s11-back", S, L)
    cards()
