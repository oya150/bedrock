"""쿠버네티스 5편 그림 만들기. 실행: python lab/fig_k8s05.py  → docs/kubernetes/img/05/*.svg

본문 절은 장면 띠로 그린다: 같은 무대를 여러 장 그리고 장마다 바뀐 곳만 빨강으로 칠한다.
갈래 공통 무대(건물·집·땅)는 1편 생성기(fig_k8s01)의 모양을 그대로 쓴다.
예시는 빵집 주문 앱. 인터넷에 열린 주문 화면만 따로 떼어 작은 집(microVM)에 넣는다.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "es"))
sys.path.insert(0, os.path.dirname(__file__))
from figkit import (GREY, INK, LIGHT, NOTE, PAPER, PINK, RED, arrow, box, bubble,  # noqa: E402
                    canvas, cell, label, moral, outdir, save, stage)
from fig_k8s01 import building, ground, house, window  # noqa: E402
from matplotlib.patches import Rectangle  # noqa: E402

OUT = outdir("05", topic="kubernetes")
PARTS = ["주문 화면", "주문 처리", "주문 장부"]


def crack(ax, x, y, s="✗ 뚫림"):
    ax.plot([x, x + 0.25, x + 0.05, x + 0.3], [y - 0.25, y, y + 0.1, y + 0.35], color=RED, lw=2.2)
    label(ax, x + 0.85, y + 0.05, s, fs=10, color=RED, bold=True)


def bar(ax, x, y, w, frac, hot=False, done=False):
    ax.add_patch(Rectangle((x, y), w, 0.32, fc="white", ec=INK, lw=1.0))
    ax.add_patch(Rectangle((x, y), w * frac, 0.32, fc=PINK if hot else LIGHT, ec=RED if hot else GREY, lw=1.0))
    if done:
        label(ax, x + w + 0.25, y + 0.16, "✓", fs=13, color=RED if hot else INK, bold=True)


# ── 여는 장면: 주문 화면 띄우기 창 ──────────────────────────────────
def launch(ax, rows_, title="주문 화면 띄우기"):
    window(ax, 0.6, 1.2, 10.8, 5.0, title)
    label(ax, 1.0, 5.25, "띄우는 방법", fs=10, ha="left", color=INK)
    label(ax, 5.2, 5.25, "진행", fs=10, ha="left", color=INK)
    ax.plot([0.85, 11.15], [5.0, 5.0], color=INK, lw=0.8)
    for k, (name, state, frac, hot, done) in enumerate(rows_):
        y = 4.35 - k * 1.05
        c = RED if hot else "#222"
        label(ax, 1.0, y, name, fs=11.5, ha="left", color=c, bold=hot)
        bar(ax, 5.2, y - 0.16, 3.6, frac, hot=hot, done=done)
        label(ax, 9.25 if not done else 9.55, y, state, fs=10, ha="left", color=c)


CT = ("컨테이너", "다 떴어요", 1.0, False, True)


def opening(ax, step):
    if step == 1:
        launch(ax, [("컨테이너", "띄우는 중", 0.3, True, False), ("가상 머신", "켜는 중", 0.08, True, False)])
    else:
        launch(ax, [CT, ("가상 머신", "아직 켜는 중", 0.25, True, False)])
        moral(ax, 6.0, 0.35, "가상 머신은 더 안전하지만 늦게 떠요")


# ── 따로 지은 집에는 관리실도 따로 있어요 ──────────────────────────
HX = [0.6, 4.4, 8.2]


def houses(ax, step):
    if step == 1:
        building(ax, 2.0, 1.0, 8.0, 4.2, PARTS, kern_hot=True, kern="공용 관리실 · 커널")
        crack(ax, 2.5, 1.45, "")
        label(ax, 6.0, 0.4, "관리실 하나가 뚫리면 모든 칸이 열려요 (4편)", fs=11, color=RED, bold=True)
        return
    ground(ax, 0.3, 11.7, 1.3)
    for k, p in enumerate(PARTS):
        house(ax, HX[k], 1.3, 3.2, 3.0, p, kern_hot=(step == 2) or (step == 3 and k == 0))
    if step == 2:
        label(ax, 6.0, 6.25, "집마다 자기 관리실(커널)이 있어요", fs=11.5, color=RED, bold=True)
    else:
        crack(ax, HX[0] + 0.3, 1.75, "")
        label(ax, 6.0, 6.25, "주문 화면 집의 관리실만 뚫렸어요", fs=11.5, color=RED, bold=True)
        moral(ax, 6.0, 0.2, "뚫려도 그 집 안에서 끝나요")


# ── 하이퍼바이저: 땅을 나눠 주고 집 사이를 지켜요 ─────────────────
def hyper_band(ax, hot=False):
    ax.add_patch(Rectangle((0.3, 1.3), 11.4, 0.5, fc=PINK if hot else NOTE, ec=RED if hot else INK, lw=1.6))
    label(ax, 6.0, 1.55, "하이퍼바이저 (CPU의 가상화 기능을 써요)", fs=10.5, color=RED if hot else INK, bold=hot)


def hyper(ax, step):
    ground(ax, 0.3, 11.7, 1.3)
    hyper_band(ax, hot=(step == 1))
    for k, p in enumerate(PARTS):
        house(ax, HX[k], 1.8, 3.2, 2.8, p)
    if step == 1:
        label(ax, 6.0, 6.25, "실제 컴퓨터 위에서 집을 짓고 메모리·CPU를 나눠 줘요", fs=11, color=RED, bold=True)
    elif step == 2:
        crack(ax, HX[0] + 0.3, 2.25, "")
        arrow(ax, (HX[0] + 3.0, 3.2), (HX[1] + 0.2, 3.2), color=RED, ms=13)
        label(ax, HX[1] - 0.25, 3.2, "✗", fs=18, color=RED, bold=True)
        label(ax, 6.0, 6.25, "옆집 메모리를 건드리면 CPU가 멈추고 하이퍼바이저에 넘겨요", fs=10.5,
              color=RED, bold=True)
    else:
        crack(ax, HX[0] + 0.3, 2.25, "")
        label(ax, HX[0] + 1.6, 3.05, "① 집 관리실", fs=10.5, color=RED, bold=True)
        label(ax, 1.6, 1.55, "②", fs=11, color=RED, bold=True)
        ax.add_patch(Rectangle((0.3, 1.3), 11.4, 0.5, fill=False, ec=RED, lw=2.0))
        label(ax, 6.0, 6.25, "침입자는 벽을 두 겹 넘어야 해요", fs=11.5, color=RED, bold=True)
        moral(ax, 6.0, 0.15, "집 사이 벽은 하드웨어 가상화가 세워요")


# ── 흉내 낸 장치: 문이 많을수록 뚫을 곳이 많아요 ─────────────────
DEV_PC = ["화면", "키보드", "마우스", "USB", "소리", "디스크", "네트워크", "…"]
DEV_MICRO = {"디스크", "네트워크", "콘솔", "재부팅 신호"}


def big_house(ax, kern_hot=False):
    ground(ax, 0.3, 11.7, 1.4)
    ax.add_patch(Rectangle((0.3, 1.4), 11.4, 0.45, fc=NOTE, ec=INK, lw=1.4))
    label(ax, 6.0, 1.62, "하이퍼바이저", fs=10, color=INK)
    house(ax, 0.6, 1.85, 3.6, 3.3, "주문 화면", kern_hot=kern_hot)


def doors(ax, names, hot=(), dim=(), x0=5.0, y0=4.6):
    for k, s in enumerate(names):
        col, row = k % 2, k // 2
        x, y = x0 + col * 2.4, y0 - row * 0.7
        cell(ax, x, y, 2.2, 0.55, s, hot=s in hot, dim=s in dim, fs=10)
        if s in dim:
            label(ax, x + 2.0, y + 0.27, "✗", fs=11, color=GREY)


def device(ax, step):
    big_house(ax, kern_hot=(step == 1))
    label(ax, 7.4, 5.55, "흉내 낸 장치 = 집의 문", fs=11, bold=True, color=RED if step == 1 else INK)
    if step == 1:
        doors(ax, ["디스크"], hot=("디스크",))
        arrow(ax, (3.9, 2.35), (5.0, 4.5), color=RED, ms=12, rad=-0.2)
        label(ax, 6.2, 3.5, "관리실은 진짜 디스크인 줄\n알고 부탁해요", fs=10, color=RED)
        label(ax, 6.2, 2.55, "하이퍼바이저가 받아서\n실제 디스크에 써요", fs=10, color=INK)
    elif step == 2:
        doors(ax, DEV_PC, hot=DEV_PC)
        label(ax, 10.75, 3.5, "보통 VM:\n문이 많아요", fs=10.5, color=RED, bold=True)
    else:
        names = ["디스크", "네트워크", "콘솔", "재부팅 신호", "화면", "USB", "소리", "…"]
        doors(ax, names, hot=DEV_MICRO, dim=("화면", "USB", "소리", "…"))
        label(ax, 10.75, 3.5, "꼭 필요한\n문 몇 개만", fs=10.5, color=RED, bold=True)
        moral(ax, 6.0, 0.15, "문이 적을수록 뚫을 곳이 적어요")


# ── 켜는 단계: 덜어 내면 빨리 떠요 ─────────────────────────────────
STEPS = ["펌웨어가\n장치 점검", "부트로더가\n커널 찾기", "커널이\n장치 준비", "프로그램\n시작"]


def boot(ax, step):
    label(ax, 0.3, 5.9, "보통 VM", fs=11.5, ha="left", bold=True)
    for k, s in enumerate(STEPS):
        x = 0.3 + k * 2.9
        box(ax, x, 4.3, 2.5, 1.1, fc=PAPER if step == 1 else LIGHT, ec=RED if step == 1 else GREY,
            lw=1.6 if step == 1 else 1.2)
        label(ax, x + 1.25, 4.85, s, fs=10, color=RED if step == 1 else INK)
        if k < 3:
            arrow(ax, (x + 2.55, 4.85), (x + 2.85, 4.85), color=RED if step == 1 else GREY, ms=11)
    if step == 1:
        label(ax, 6.0, 3.6, "장치가 많을수록 점검·준비할 것도 많아요", fs=10.5, color=RED)
        return
    label(ax, 0.3, 3.25, "microVM", fs=11.5, ha="left", bold=True, color=RED)
    for k, s in enumerate(STEPS):
        x = 0.3 + k * 2.9
        if k < 2:
            ax.add_patch(Rectangle((x, 1.6), 2.5, 1.1, fc="white", ec=GREY, lw=1.0, ls="--"))
            label(ax, x + 1.25, 2.15, "건너뛰어요", fs=10, color=GREY)
            continue
        s2 = "커널을 바로\n올려 장치 몇 개만" if k == 2 else s
        box(ax, x, 1.6, 2.5, 1.1, fc=PINK, ec=RED, lw=1.6)
        label(ax, x + 1.25, 2.15, s2, fs=9.5, color=RED, bold=True)
        if k < 3:
            arrow(ax, (x + 2.55, 2.15), (x + 2.85, 2.15), color=RED, ms=11)
    moral(ax, 6.0, 0.7, "덜어 낸 단계만큼 빨리 떠요")


# ── Kata Containers: 파드를 microVM에 넣어요 ───────────────────────
def kata(ax, step):
    window(ax, 0.3, 3.9, 3.6, 2.3, "쿠버네티스")
    label(ax, 2.1, 4.75, "주문 화면 파드를\n띄워 주세요", fs=10, color=INK)
    ground(ax, 4.6, 11.7, 1.3)
    ax.add_patch(Rectangle((4.6, 1.3), 7.1, 0.45, fc=NOTE, ec=INK, lw=1.4))
    label(ax, 8.15, 1.52, "하이퍼바이저", fs=10, color=INK)
    house(ax, 6.4, 1.75, 3.4, 3.2, "", kern_hot=(step == 1))
    label(ax, 2.1, 3.3, "Kata Containers", fs=11, bold=True, color=RED if step == 1 else INK)
    arrow(ax, (2.1, 3.85), (2.1, 3.55), color=GREY, ms=11)
    if step == 1:
        arrow(ax, (3.4, 3.1), (6.3, 3.1), color=RED, ms=13)
        label(ax, 4.8, 3.45, "microVM 한 채", fs=10, color=RED)
        label(ax, 8.1, 6.25, "파드마다 작은 집을 지어요", fs=11, color=RED, bold=True)
    else:
        cell(ax, 6.75, 3.15, 2.7, 0.55, "에이전트", hot=True, fs=10)
        arrow(ax, (8.1, 3.75), (8.1, 4.05), color=RED, ms=11)
        cell(ax, 6.75, 4.1, 2.7, 0.55, "주문 화면 컨테이너", hot=True, fs=9.5)
        label(ax, 8.1, 6.25, "집 안의 에이전트가 컨테이너를 띄워요", fs=11, color=RED, bold=True)
        moral(ax, 6.0, 0.25, "밖에서는 보통 파드, 안에는 자기 커널")


# ── 언제 쓸모 있을까요: 갈림길 ──────────────────────────────────────
def decide():
    fig, ax = canvas(7.4, 4.4, 15, 9)
    box(ax, 2.5, 7.4, 10.0, 1.1, fc=NOTE)
    label(ax, 7.5, 7.95, "커널 버그를 노리는 코드까지 막아야 하나요?", fs=11, bold=True)
    arrow(ax, (4.5, 7.3), (2.8, 6.0)); label(ax, 3.2, 6.8, "아니요", fs=10, color=INK)
    box(ax, 0.3, 4.4, 5.4, 1.5, fc=PAPER)
    label(ax, 3.0, 5.15, "컨테이너로 충분해요 (4편)", fs=10.5)
    arrow(ax, (10.5, 7.3), (11.6, 6.0), color=RED); label(ax, 11.6, 6.8, "예", fs=10, color=RED)
    box(ax, 8.6, 4.4, 6.1, 1.5, fc=NOTE)
    label(ax, 11.65, 5.15, "GPU 같은 특별한 장치가\n필요한가요?", fs=10.5, bold=True)
    arrow(ax, (10.3, 4.3), (8.6, 3.0)); label(ax, 8.9, 3.8, "예", fs=10, color=INK)
    box(ax, 4.6, 1.2, 5.0, 1.7, fc=PAPER)
    label(ax, 7.1, 2.05, "장치를 더 흉내 내는\n보통 VM", fs=10.5)
    arrow(ax, (13.0, 4.3), (13.0, 3.0), color=RED); label(ax, 13.3, 3.65, "아니요", fs=10, color=RED, ha="left")
    box(ax, 10.2, 1.2, 4.5, 1.7, fc=PINK, ec=RED)
    label(ax, 12.45, 2.05, "microVM\n(Kata Containers 등)", fs=10.5, color=RED, bold=True)
    save(fig, OUT, "k8s05-decide.svg")


# ── 정리: 처음 장면으로 돌아가기 ───────────────────────────────────
def back(ax, step):
    if step == 1:
        launch(ax, [CT, ("가상 머신", "아직 켜는 중", 0.25, False, False)])
        label(ax, 6.0, 0.4, "처음 장면: 안전하면 늦고, 빠르면 커널을 같이 써요", fs=11, color=INK)
    else:
        launch(ax, [CT, ("가상 머신", "아직 켜는 중", 0.25, False, False),
                    ("microVM", "다 떴어요", 1.0, True, True)])
        moral(ax, 6.0, 0.35, "자기 커널을 갖고도 금방 떴어요")


# ── 정리: 낱말 카드 ────────────────────────────────────────────────
def cards():
    fig, ax = canvas(6.4, 5.4, 9.8, 8.3)
    W, H = 4.6, 3.8

    def card(i, name, line):
        col, row = i % 2, i // 2
        x, y = 0.2 + col * 4.9, 4.3 - row * 4.05
        box(ax, x, y, W, H, fc="white")
        label(ax, x + 0.25, y + H - 0.4, name, fs=12.5, ha="left", bold=True)
        label(ax, x + W / 2, y + 0.6, line, fs=10, color=INK)
        return x, y

    x, y = card(0, "가상 머신 (VM)", "커널까지 갖춘 컴퓨터를\n통째로 흉내 낸 것 (따로 지은 집)")
    house(ax, x + 1.5, y + 1.3, 1.6, 1.0, "")
    x, y = card(1, "하이퍼바이저", "실제 컴퓨터 위에서 VM을 만들고\n나눠 주며 사이를 지키는 프로그램")
    for k in range(2):
        cell(ax, x + 0.5 + k * 1.9, y + 2.2, 1.7, 0.55, "VM", fs=10)
    cell(ax, x + 0.5, y + 1.45, 3.6, 0.55, "하이퍼바이저", hot=True, fs=10)
    x, y = card(2, "흉내 낸 장치", "VM 안 커널이 진짜로 알고 쓰는\n가짜 디스크·네트워크 (집의 문)")
    for k, s in enumerate(["디스크", "네트워크"]):
        cell(ax, x + 0.4 + k * 2.0, y + 1.8, 1.8, 0.6, s, hot=True, fs=10)
    x, y = card(3, "microVM", "장치와 켜는 단계를 덜어\n작게 만든 VM")
    house(ax, x + 1.8, y + 1.25, 1.1, 0.9, "", kern_hot=True, kern="커널")
    save(fig, OUT, "k8s05-cards.svg")


if __name__ == "__main__":
    S, L = (7.2, 3.8), (12, 6.6)
    stage(opening, 2, OUT, "k8s05-open", S, L)
    stage(houses, 3, OUT, "k8s05-house", S, L)
    stage(hyper, 3, OUT, "k8s05-hyper", S, L)
    stage(device, 3, OUT, "k8s05-device", S, L)
    stage(boot, 2, OUT, "k8s05-boot", S, L)
    stage(kata, 2, OUT, "k8s05-kata", S, L)
    decide()
    stage(back, 2, OUT, "k8s05-back", S, L)
    cards()
