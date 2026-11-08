"""쿠버네티스 12편 그림 만들기. 실행: python lab/fig_k8s12.py  → docs/kubernetes/img/12/*.svg

본문 절은 장면 띠로 그린다: 같은 무대를 여러 장 그리고 장마다 바뀐 곳만 빨강으로 칠한다.
예시는 11편의 빵집 주문 장부를 잇는다. 주문 1~3이 이미 있고 주문 4, 5가 새로 들어온다.
노드 A(주문 장부 파드와 엔진), B, C(볼륨 레플리카), D(비어 있다가 재구축 자리).
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "es"))
from figkit import (GREY, INK, LIGHT, NOTE, PAPER, PINK, RED, arrow, box, bubble,  # noqa: E402
                    canvas, cell, cylinder, label, moral, outdir, save, stage)
from matplotlib.patches import Rectangle  # noqa: E402

OUT = outdir("12", topic="kubernetes")
ORDERS = ["1   크루아상 2개", "2   식빵 1개", "3   단팥빵 3개"]
NX = {"A": 0.25, "B": 3.2, "C": 6.15, "D": 9.1}
NW, NY, NH = 2.65, 0.4, 3.0


def cross(ax, x, y, s=0.5, color=RED):
    ax.plot([x - s, x + s], [y - s, y + s], color=color, lw=3)
    ax.plot([x - s, x + s], [y + s, y - s], color=color, lw=3)


def node(ax, n, dead=False, hot=False):
    x = NX[n]
    box(ax, x, NY, NW, NH, fc=LIGHT if dead else "white", ec=RED if hot else (GREY if dead else INK),
        lw=2.0 if hot else 1.5)
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
    box(ax, x, 1.6, NW - 0.3, 0.5, fc=PINK if hot else (LIGHT if dim else PAPER),
        ec=RED if hot else (GREY if dim else INK), lw=1.8 if hot else 1.3)
    label(ax, x + (NW - 0.3) / 2, 1.85, "엔진", fs=10, color=c, bold=hot)


def replica(ax, n, k=3, hot=(), dim=False, err=False, miss=(), title="레플리카", hotbox=False):
    """노드 아래쪽 볼륨 레플리카. k=든 주문 수(1부터), hot=빨간 칸 번호, miss=빈 점선 칸."""
    x, y = NX[n] + 0.12, 0.55
    ec = RED if (hotbox or err) else (GREY if dim else INK)
    box(ax, x, y, NW - 0.24, 0.9, fc=PINK if hotbox else ("white" if not dim else LIGHT), ec=ec,
        lw=1.8 if (hotbox or err) else 1.2)
    label(ax, x + 0.1, y + 0.72, title, fs=8.5, ha="left", color=RED if (hotbox or err) else (GREY if dim else INK))
    for j in range(5):
        cx = x + 0.12 + j * 0.47
        if j < k:
            cell(ax, cx, y + 0.08, 0.42, 0.45, str(j + 1), hot=(j + 1) in hot, dim=dim, fs=9)
        elif (j + 1) in miss:
            ax.add_patch(Rectangle((cx, y + 0.08), 0.42, 0.45, fc="white", ec=RED, lw=1.4, ls="--"))
    if err:
        label(ax, x + NW - 0.45, y + 0.72, "오류", fs=9, color=RED, bold=True)


def screen(ax, rows="on", hot=False, err=None):
    box(ax, 0.3, 3.85, 5.4, 2.6, fc="white", round_=False)
    ax.add_patch(Rectangle((0.3, 6.05), 5.4, 0.4, fc=LIGHT, ec=INK, lw=1.2))
    label(ax, 0.45, 6.25, "빵집 주문 장부", fs=10, ha="left", color=INK)
    for k, s in enumerate(ORDERS):
        y = 5.7 - k * 0.5
        c = RED if hot else (GREY if rows == "grey" else "#222")
        if hot:
            ax.add_patch(Rectangle((0.5, y - 0.2), 5.0, 0.4, fc=PINK, ec=RED, lw=1.5))
        label(ax, 0.65, y, s, fs=10, ha="left", color=c, bold=hot)
    if err:
        label(ax, 3.0, 4.15, err, fs=10, color=RED, bold=True,
              bbox=dict(boxstyle="round,pad=0.3", fc=PINK, ec=RED, lw=1.4))


def localdisk(ax, n, hot=False, dim=False, rows="주문 1, 2, 3"):
    x = NX[n] + 0.35
    c = RED if hot else (GREY if dim else INK)
    cylinder(ax, x, 0.75, NW - 0.7, 0.85, "", fc=PINK if hot else (LIGHT if dim else NOTE), ec=c)
    label(ax, x + (NW - 0.7) / 2, 1.17, rows, fs=9, color=c)
    label(ax, x + (NW - 0.7) / 2, 2.0, "디스크", fs=9.5, color=c)


# ── 여는 장면: 디스크가 한 노드에만 있어요 ───────────────────────────
def opening(ax, step):
    deadA = step >= 2
    for n in "ABC":
        node(ax, n, dead=(n == "A" and deadA))
    if step == 1:
        screen(ax)
        podbox(ax, "A")
        localdisk(ax, "A", hot=True)
        label(ax, 8.8, 5.0, "주문 장부 디스크는\n노드 A 안에만 있어요", fs=11.5, color=RED, bold=True)
    elif step == 2:
        screen(ax, rows="grey")
        podbox(ax, "A", dim=True)
        localdisk(ax, "A", dim=True)
        cross(ax, NX["A"] + NW / 2, NY + NH / 2, s=1.0)
        label(ax, 9.0, 5.0, "노드 A가 고장 났어요", fs=12, color=RED, bold=True)
    else:
        screen(ax, rows="grey", err="주문 장부를 열 수 없어요")
        podbox(ax, "A", dim=True)
        localdisk(ax, "A", dim=True)
        cross(ax, NX["A"] + NW / 2, NY + NH / 2, s=1.0)
        podbox(ax, "B", s="새 주문 장부 파드", hot=True)
        label(ax, NX["B"] + NW / 2, 1.5, "디스크가\n고장 난 A 안에 있어요", fs=9.5, color=RED)
        moral(ax, 8.8, 5.0, "디스크가 한 노드에만 있으면\n그 노드와 함께 멈춰요", fs=11.5)


# ── 가끔 복사하면 마지막 주문을 잃어요 ─────────────────────────────
def copy(ax, step):
    for n in "AB":
        node(ax, n, dead=(n == "A" and step == 2))
    podbox(ax, "A", dim=(step == 2))
    if step == 1:
        localdisk(ax, "A", rows="주문 1, 2, 3")
        label(ax, NX["A"] + NW / 2, 3.75, "주문 3은 복사한 뒤에 들어왔어요", fs=10, color=RED, bold=True)
    else:
        localdisk(ax, "A", dim=True)
        cross(ax, NX["A"] + NW / 2, NY + NH / 2, s=1.0)
    x = NX["B"] + 0.35
    hot = step == 2
    cylinder(ax, x, 0.75, NW - 0.7, 0.85, "", fc=PINK if hot else NOTE, ec=RED if hot else INK)
    label(ax, x + (NW - 0.7) / 2, 1.17, "주문 1, 2", fs=9, color=RED if hot else INK)
    label(ax, x + (NW - 0.7) / 2, 2.0, "어젯밤 복사본", fs=9.5, color=RED if hot else INK)
    box(ax, 6.4, 0.4, 5.3, 3.0, fc=PAPER)
    label(ax, 9.05, 3.05, "복사본의 주문", fs=10, color=INK, bold=True)
    for j in range(3):
        if j < 2:
            cell(ax, 7.3 + j * 1.2, 1.9, 1.0, 0.7, f"주문 {j + 1}", fs=10)
        else:
            ax.add_patch(Rectangle((7.3 + j * 1.2, 1.9), 1.0, 0.7, fc="white", ec=RED if hot else GREY,
                                   lw=1.5, ls="--"))
    if hot:
        label(ax, 9.05, 1.35, "주문 3이 없어요", fs=10.5, color=RED, bold=True)
        moral(ax, 6.0, 4.6, "가끔 복사하면 마지막 주문을 잃어요")


# ── 엔진이 받아 레플리카 모두에 보내요 ─────────────────────────────
def engine_strip(ax, step):
    for n in "ABC":
        node(ax, n)
    podbox(ax, "A", s="주문 장부 파드")
    engine(ax, "A", hot=(step == 1))
    for n in "ABC":
        replica(ax, n, k=4 if step == 2 else 3, hot=(4,) if step == 2 else ())
    if step == 1:
        arrow(ax, (NX["A"] + 1.32, 2.33), (NX["A"] + 1.32, 2.13), color=RED, ms=10)
        bubble(ax, 0.3, 4.0, 5.6, 1.4, "데이터베이스가 쓴 주문 4를\n엔진이 받았어요", (1.6, 3.45), hot=True, fs=10.5)
    else:
        for n in "ABC":
            tx = NX[n] + 2.1
            arrow(ax, (NX["A"] + 2.3, 1.75), (tx, 1.48), color=RED, ms=11, lw=1.8, rad=-0.12 if n != "A" else 0)
        bubble(ax, 0.3, 4.0, 5.6, 1.4, "주문 4를 레플리카 셋에\n모두 보내요", (1.6, 3.45), hot=True, fs=10.5)
        moral(ax, 9.0, 4.95, "엔진 하나가 받아\n레플리카 모두에 보내요", fs=11.5)


# ── 블록 저장소: 엔진은 번호 붙은 칸만 다뤄요 ──────────────────────
def block(ax, step):
    box(ax, 0.3, 3.7, 5.2, 2.7, fc="white")
    label(ax, 2.9, 6.05, "데이터베이스가 보는 것", fs=10.5, bold=True, color=INK)
    box(ax, 1.2, 4.1, 3.4, 1.5, fc=NOTE, round_=False)
    label(ax, 2.9, 5.25, "주문 장부 파일", fs=10.5)
    label(ax, 2.9, 4.6, "… 주문 4 크루아상 1개", fs=10, color=RED if step == 1 else INK)
    box(ax, 6.2, 3.7, 5.5, 2.7, fc="white")
    label(ax, 8.95, 6.05, "엔진이 보는 것", fs=10.5, bold=True, color=INK)
    for j in range(8):
        cell(ax, 6.5 + j * 0.62, 4.6, 0.55, 0.65, str(j), hot=(step == 2 and j == 5), fs=10)
    label(ax, 8.95, 4.15, "번호 붙은 칸이 줄지어 있어요", fs=9.5, color=INK)
    if step == 1:
        bubble(ax, 0.6, 0.9, 5.0, 1.4, "주문 4를\n장부 파일에 적어요", (2.9, 3.6), hot=True, fs=10.5)
    else:
        bubble(ax, 0.6, 0.9, 5.0, 1.4, "주문 4를\n장부 파일에 적어요", (2.9, 3.6), fs=10.5)
        arrow(ax, (5.55, 4.9), (6.4, 4.9), color=GREY, ms=11)
        bubble(ax, 6.4, 0.9, 5.3, 1.4, "5번 칸을 이렇게\n바꿔요", (9.95, 3.6), hot=True, fs=10.5)
        moral(ax, 6.0, 0.35, "엔진은 파일을 몰라요. 칸 번호와 내용만 보내요", fs=11.5)


# ── 레플리카가 있는 노드가 죽으면 ──────────────────────────────────
def fail(ax, step):
    for n in "ABCD":
        node(ax, n, dead=(n == "C"))
    podbox(ax, "A")
    engine(ax, "A")
    k = 4 if step == 1 else 5
    replica(ax, "A", k=k, hot=(5,) if step == 2 else ())
    replica(ax, "B", k=k, hot=(5,) if step == 2 else ())
    replica(ax, "C", k=4, dim=step > 1, err=(step == 1))
    cross(ax, NX["C"] + NW / 2, NY + NH / 2 + 0.3, s=0.6, color=RED if step == 1 else GREY)
    if step == 1:
        bubble(ax, 0.3, 4.0, 6.4, 1.4, "노드 C의 레플리카가 답이 없어요\n오류로 표시해요", (1.6, 3.45), hot=True, fs=10.5)
    elif step == 2:
        for n in "AB":
            arrow(ax, (NX["A"] + 2.3, 1.75), (NX[n] + 2.1, 1.48), color=RED, ms=11, lw=1.8,
                  rad=-0.12 if n != "A" else 0)
        bubble(ax, 0.3, 4.0, 6.4, 1.4, "주문 5는 남은 둘에 보내요\n주문 장부는 그대로 돌아요", (1.6, 3.45), hot=True, fs=10.5)
    elif step == 3:
        replica(ax, "D", k=0, hotbox=True, title="새 레플리카")
        arrow(ax, (NX["B"] + 1.3, 1.55), (NX["D"] + 1.3, 1.55), color=RED, ms=13, rad=-0.3)
        label(ax, 9.3, 4.7, "남은 레플리카를 보고\n다시 채워요", fs=11, color=RED, bold=True)
        bubble(ax, 0.3, 4.0, 6.4, 1.4, "노드 D에 빈 레플리카를\n새로 만들어요", (1.6, 3.45), hot=True, fs=10.5)
    else:
        replica(ax, "D", k=5, hot=(1, 2, 3, 4, 5))
        bubble(ax, 0.3, 4.0, 6.4, 1.4, "레플리카가 다시 셋이 됐어요", (1.6, 3.45), hot=True, fs=10.5)
        moral(ax, 9.3, 4.7, "남은 것으로 이어 가고\n새것을 다시 채워요", fs=11.5)


# ── 판단 (한 장) ───────────────────────────────────────────────────
def decide():
    fig, ax = canvas(10, 4.2, 15, 6.4)
    box(ax, 0.3, 4.6, 6.0, 1.3, fc=NOTE)
    label(ax, 3.3, 5.25, "노드가 고장 나도 남아야 하나요?", fs=10.5, bold=True)
    arrow(ax, (6.4, 5.25), (8.4, 5.25))
    label(ax, 7.4, 5.55, "아니요", fs=10, color=INK)
    box(ax, 8.5, 4.6, 6.2, 1.3, fc=PAPER)
    label(ax, 11.6, 5.25, "노드 자기 디스크에 둬요", fs=10.5)
    arrow(ax, (3.3, 4.5), (3.3, 3.5)); label(ax, 3.6, 4.0, "예", fs=10, color=INK, ha="left")
    box(ax, 0.3, 2.2, 6.0, 1.2, fc=NOTE)
    label(ax, 3.3, 2.8, "저장 장치가 이미 복사본을 두나요?", fs=10.5, bold=True)
    arrow(ax, (6.4, 2.8), (8.4, 2.8)); label(ax, 7.4, 3.1, "예", fs=10, color=INK)
    box(ax, 8.5, 2.2, 6.2, 1.2, fc=PAPER)
    label(ax, 11.6, 2.8, "그 저장 장치의 CSI 드라이버를 써요", fs=10.5)
    arrow(ax, (3.3, 2.1), (3.3, 1.3), color=RED); label(ax, 3.6, 1.7, "아니요, 노드 디스크뿐이에요", fs=10, color=RED, ha="left")
    box(ax, 0.3, 0.1, 6.0, 1.1, fc=PINK, ec=RED)
    label(ax, 3.3, 0.65, "노드들의 디스크를 묶어 Longhorn으로", fs=10.5, color=RED, bold=True)
    save(fig, OUT, "k8s12-decide.svg")


# ── 정리: 처음 장면으로 돌아가기 ───────────────────────────────────
def back(ax, step):
    for n in "ABCD":
        node(ax, n, dead=(n == "A"))
    podbox(ax, "A", dim=True)
    engine(ax, "A", dim=True)
    replica(ax, "A", k=3, dim=True)
    cross(ax, NX["A"] + NW / 2, NY + NH / 2, s=1.0, color=RED if step == 1 else GREY)
    replica(ax, "B")
    replica(ax, "C")
    if step == 1:
        screen(ax, rows="grey")
        label(ax, 8.8, 5.0, "이번에도 노드 A가\n고장 났어요", fs=12, color=RED, bold=True)
        return
    podbox(ax, "B", s="새 주문 장부 파드", hot=(step == 2))
    engine(ax, "B", hot=(step == 2))
    if step == 2:
        screen(ax, hot=True)
        label(ax, 8.8, 5.0, "B에 새 엔진이 떠서\n남은 레플리카로 이어 가요", fs=11, color=RED, bold=True)
    else:
        screen(ax)
        replica(ax, "D", k=3, hot=(1, 2, 3), title="새 레플리카")
        arrow(ax, (NX["C"] + 1.3, 1.55), (NX["D"] + 1.3, 1.55), color=RED, ms=13, rad=-0.35)
        moral(ax, 8.8, 5.0, "노드 하나가 죽어도\n남은 레플리카로 이어 가요", fs=11.5)


# ── 정리: 낱말 카드 ────────────────────────────────────────────────
def cards():
    fig, ax = canvas(6.4, 5.4, 9.8, 8.2)
    W, H = 4.6, 3.8

    def card(i, name, line):
        col, row = i % 2, i // 2
        x, y = 0.2 + col * 4.9, 4.15 - row * 4.05
        box(ax, x, y, W, H, fc="white")
        label(ax, x + 0.25, y + H - 0.4, name, fs=12.5, ha="left", bold=True)
        label(ax, x + W / 2, y + 0.6, line, fs=10, color=INK)
        return x, y

    x, y = card(0, "블록 저장소", "디스크를 번호 붙은 칸으로 보고\n칸 단위로 읽고 쓰는 저장소")
    for j in range(6):
        cell(ax, x + 0.5 + j * 0.62, y + 1.7, 0.55, 0.65, str(j), hot=(j == 5), fs=10)
    x, y = card(1, "엔진", "볼륨마다 하나, 파드 곁에서\n쓰기를 받아 레플리카에 보내요")
    cell(ax, x + 0.4, y + 1.7, 1.4, 0.7, "엔진", hot=True, fs=10.5)
    for j in range(3):
        arrow(ax, (x + 1.9, y + 2.05), (x + 3.0, y + 2.7 - j * 0.6), color=RED, ms=9, lw=1.4)
        cell(ax, x + 3.05, y + 2.45 - j * 0.6, 1.1, 0.45, "레플리카", fs=8)
    x, y = card(2, "볼륨 레플리카", "노드마다 하나씩 두는\n볼륨의 온전한 복사본")
    for j in range(3):
        cell(ax, x + 0.35 + j * 1.35, y + 1.7, 1.2, 0.7, f"노드 {'ABC'[j]}", hot=(j == 1), fs=9.5)
    x, y = card(3, "재구축", "잃은 레플리카 대신 새것을 만들어\n남은 레플리카로 채우기")
    cell(ax, x + 0.4, y + 1.7, 1.4, 0.7, "1 2 3", fs=10)
    arrow(ax, (x + 1.9, y + 2.05), (x + 2.7, y + 2.05), color=RED, ms=11)
    cell(ax, x + 2.8, y + 1.7, 1.4, 0.7, "1 2 3", hot=True, fs=10)
    save(fig, OUT, "k8s12-cards.svg")


if __name__ == "__main__":
    S, L = (7.2, 3.8), (12, 6.6)
    stage(opening, 3, OUT, "k8s12-open", S, L)
    stage(copy, 2, OUT, "k8s12-copy", S, L)
    stage(engine_strip, 2, OUT, "k8s12-engine", S, L)
    stage(block, 2, OUT, "k8s12-block", S, L)
    stage(fail, 4, OUT, "k8s12-fail", S, L)
    decide()
    stage(back, 3, OUT, "k8s12-back", S, L)
    cards()
