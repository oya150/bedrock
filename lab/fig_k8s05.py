"""쿠버네티스 5편 그림 만들기. 실행: python lab/fig_k8s05.py  → docs/kubernetes/img/05/*.svg

갈래 공통 무대(건물·집·땅)는 1편 그림의 모양과 같다. 1편 생성기가 바뀌어도 이 편 그림이 흔들리지 않게
필요한 도우미(window·building·house·ground)를 이 파일에 옮겨 두었다.
예시는 빵집 주문 앱. 인터넷에 열린 주문 화면만 따로 떼어 작은 집(microVM)에 넣는다.
그림 안 글씨는 낱말과 숫자만 둔다. 문장은 본문과 그림 설명에 있다.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "es"))
from figkit import (GREY, INK, LIGHT, NOTE, PAPER, PINK, RED, arrow, box,  # noqa: E402
                    canvas, cell, label, outdir, save)
from matplotlib.patches import Circle, Polygon, Rectangle  # noqa: E402

OUT = outdir("05", topic="kubernetes")
PARTS = ["주문 화면", "주문 처리", "주문 장부"]
S, L = (7.2, 3.8), (12, 6.6)


# ── 공통 무대 (1편과 같은 모양) ───────────────────────────────────
def window(ax, x, y, w, h, title):
    ax.add_patch(Rectangle((x, y), w, h, fc="white", ec=INK, lw=1.4))
    ax.add_patch(Rectangle((x, y + h - 0.45), w, 0.45, fc=LIGHT, ec=INK, lw=1.2))
    for k in range(3):
        ax.add_patch(Circle((x + 0.22 + k * 0.22, y + h - 0.225), 0.06, fc=GREY, ec="none"))
    label(ax, x + 0.95, y + h - 0.225, title, fs=10, ha="left", color=INK)


def building(ax, x, y, w, h, rooms, kern_hot=False, kern="공용 관리실 · 커널"):
    ax.add_patch(Rectangle((x, y), w, h, fc="white", ec=INK, lw=2.2))
    ax.add_patch(Rectangle((x - 0.15, y + h), w + 0.3, 0.2, fc=INK, ec=INK))
    label(ax, x + w / 2, y + h + 0.48, "건물 = 컴퓨터 한 대", fs=10.5, color=INK, bold=True)
    kc = RED if kern_hot else INK
    ax.add_patch(Rectangle((x + 0.15, y + 0.15), w - 0.3, 0.6, fc=PINK if kern_hot else LIGHT, ec=kc,
                           lw=1.8 if kern_hot else 1.2))
    label(ax, x + w / 2, y + 0.45, kern, fs=10.5, color=kc, bold=kern_hot)
    n = len(rooms)
    top, bot = y + h - 0.15, y + 0.9
    rw = (w - 0.3) / n
    for k, r in enumerate(rooms):
        rx = x + 0.15 + k * rw
        ax.add_patch(Rectangle((rx + 0.05, bot), rw - 0.1, top - bot, fc=NOTE, ec=INK, lw=1.2))
        cw = min(1.6, rw - 0.25)
        cell(ax, rx + rw / 2 - cw / 2, (top + bot) / 2 - 0.28, cw, 0.56, r, fs=10.5)
    for k in range(1, n):
        wx = x + 0.15 + k * rw
        ax.plot([wx, wx], [bot - 0.05, top], color=INK, lw=3.2, solid_capstyle="butt")


def house(ax, x, y, w, h, prog, kern_hot=False, kern="관리실 · 커널"):
    ax.add_patch(Rectangle((x, y), w, h, fc="white", ec=INK, lw=2.0))
    ax.add_patch(Polygon([(x - 0.15, y + h), (x + w + 0.15, y + h), (x + w / 2, y + h + 0.7)], closed=True,
                         fc=LIGHT, ec=INK, lw=2.0))
    kc = RED if kern_hot else INK
    ax.add_patch(Rectangle((x + 0.12, y + 0.12), w - 0.24, 0.6, fc=PINK if kern_hot else LIGHT, ec=kc,
                           lw=1.8 if kern_hot else 1.1))
    label(ax, x + w / 2, y + 0.42, kern, fs=9.5, color=kc, bold=kern_hot)
    if prog:
        cell(ax, x + w / 2 - 0.8, y + h - 0.85, 1.6, 0.56, prog, fs=10.5)


def ground(ax, x0, x1, y, name="땅 = 실제 컴퓨터"):
    ax.add_patch(Rectangle((x0, y - 0.35), x1 - x0, 0.35, fc=LIGHT, ec=INK, lw=1.2))
    label(ax, (x0 + x1) / 2, y - 0.6, name, fs=10.5, color=INK, bold=True)


def band(ax, x0, x1, y, h=0.5, hot=False, s="하이퍼바이저"):
    ax.add_patch(Rectangle((x0, y), x1 - x0, h, fc=PINK if hot else NOTE, ec=RED if hot else INK,
                           lw=2.0 if hot else 1.4))
    label(ax, (x0 + x1) / 2, y + h / 2, s, fs=10.5, color=RED if hot else INK, bold=hot)


def crack(ax, x, y):
    ax.plot([x, x + 0.25, x + 0.05, x + 0.3], [y - 0.25, y, y + 0.1, y + 0.35], color=RED, lw=2.2)


def one(draw, name, size=S, lim=L):
    fig, ax = canvas(*size, *lim)
    draw(ax)
    save(fig, OUT, name)


# ── 1. 주문 화면 띄우기 창 ───────────────────────────────────────
def bar(ax, x, y, w, frac, hot=False):
    ax.add_patch(Rectangle((x, y), w, 0.32, fc="white", ec=INK, lw=1.0))
    ax.add_patch(Rectangle((x, y), w * frac, 0.32, fc=PINK if hot else LIGHT, ec=RED if hot else GREY, lw=1.0))


def opening(ax):
    window(ax, 0.6, 1.2, 10.8, 4.0, "주문 화면 띄우기")
    label(ax, 1.0, 4.25, "띄우는 방법", fs=10, ha="left", color=INK)
    label(ax, 5.2, 4.25, "진행", fs=10, ha="left", color=INK)
    ax.plot([0.85, 11.15], [4.0, 4.0], color=INK, lw=0.8)
    rows_ = [("컨테이너", "✓ 다 뜸", 1.0, False), ("가상 머신", "켜는 중", 0.25, True)]
    for k, (name, state, frac, hot) in enumerate(rows_):
        y = 3.35 - k * 1.05
        c = RED if hot else "#222"
        label(ax, 1.0, y, name, fs=11.5, ha="left", color=c, bold=hot)
        bar(ax, 5.2, y - 0.16, 3.6, frac, hot=hot)
        label(ax, 9.25, y, state, fs=10.5, ha="left", color=c, bold=hot)


# ── 2. 건물 하나, 관리실 하나 ─────────────────────────────────────
def house_shared(ax):
    building(ax, 2.0, 1.0, 8.0, 4.2, PARTS, kern_hot=True)
    crack(ax, 2.5, 1.45)


# ── 3. 집 세 채, 관리실 셋 ────────────────────────────────────────
HX = [0.6, 4.4, 8.2]


def house_apart(ax):
    ground(ax, 0.3, 11.7, 1.3)
    for k, p in enumerate(PARTS):
        house(ax, HX[k], 1.3, 3.2, 3.0, p, kern_hot=(k == 0))
    crack(ax, HX[0] + 0.3, 1.75)


# ── 4·5. 하이퍼바이저가 집 사이를 지켜요 ─────────────────────────
def hyper_block(ax):
    ground(ax, 0.3, 11.7, 1.3)
    band(ax, 0.3, 11.7, 1.3)
    for k, p in enumerate(PARTS):
        house(ax, HX[k], 1.8, 3.2, 2.8, p, kern_hot=(k == 0))
    crack(ax, HX[0] + 0.3, 2.25)
    arrow(ax, (HX[0] + 1.6, 2.75), (HX[1] - 0.45, 3.2), color=RED, ms=13, rad=-0.2)
    label(ax, HX[1] - 0.3, 3.2, "✗", fs=20, color=RED, bold=True)
    cell(ax, HX[1] + 0.9, 2.95, 1.4, 0.5, "메모리", fs=10)


def hyper_two(ax):
    ground(ax, 0.3, 11.7, 1.3)
    band(ax, 0.3, 11.7, 1.3, hot=True, s="② 하이퍼바이저")
    for k, p in enumerate(PARTS):
        house(ax, HX[k], 1.8, 3.2, 2.8, p, kern_hot=(k == 0), kern="① 관리실 · 커널" if k == 0 else "관리실 · 커널")
    label(ax, HX[0] + 1.6, 3.55, "침입자", fs=10.5, color=RED, bold=True)
    arrow(ax, (HX[0] + 1.6, 3.3), (HX[0] + 1.6, 2.6), color=RED, ms=12)


# ── 6. 흉내 낸 장치 = 집의 문 ────────────────────────────────────
def device_door(ax):
    ground(ax, 0.3, 11.7, 1.4)
    band(ax, 0.3, 11.7, 1.4, h=0.45)
    house(ax, 0.8, 1.85, 4.0, 3.3, "주문 화면", kern_hot=True)
    cell(ax, 3.9, 3.4, 2.4, 0.6, "흉내 낸 디스크", hot=True, fs=10.5)
    arrow(ax, (2.8, 2.6), (3.85, 3.55), color=RED, ms=12)
    arrow(ax, (6.35, 3.7), (8.0, 1.9), color=RED, ms=13, rad=-0.25)
    cell(ax, 9.4, 3.4, 2.1, 0.6, "실제 디스크", fs=10.5)
    arrow(ax, (8.6, 1.9), (9.9, 3.35), color=INK, ms=12, rad=-0.2)


# ── 7. 보통 VM과 microVM의 문 수 ─────────────────────────────────
DEV_PC = ["화면", "키보드", "마우스", "USB", "소리", "디스크", "네트워크", "…"]
DEV_MICRO = ["디스크", "네트워크", "콘솔", "재부팅 신호"]


def device_count(ax):
    # 왼쪽: 보통 VM, 문 두 줄
    label(ax, 3.9, 7.6, "보통 VM", fs=12, bold=True, color=INK)
    house(ax, 0.4, 3.0, 2.2, 2.6, "", kern="커널")
    for k, s in enumerate(DEV_PC):
        cell(ax, 3.0 + (k % 2) * 2.15, 5.3 - (k // 2) * 0.72, 1.95, 0.56, s, fs=10)
    label(ax, 3.9, 2.3, "문 많이", fs=12, bold=True, color=INK)
    ax.plot([8.0, 8.0], [1.2, 7.9], color=GREY, lw=1.0, ls="--")
    # 오른쪽: Firecracker, 문 한 줄
    label(ax, 11.1, 7.6, "microVM", fs=12, bold=True, color=RED)
    house(ax, 8.4, 3.0, 2.2, 2.6, "", kern="커널")
    for k, s in enumerate(DEV_MICRO):
        cell(ax, 11.0, 5.3 - k * 0.72, 2.4, 0.56, s, hot=True, fs=10)
    label(ax, 11.1, 2.3, "문 몇 개", fs=12, bold=True, color=RED)


# ── 8. 켜는 단계 ─────────────────────────────────────────────────
STEPS = ["펌웨어\n장치 점검", "부트로더\n커널 찾기", "커널\n장치 준비", "프로그램\n시작"]


def boot(ax):
    label(ax, 0.3, 5.9, "보통 VM", fs=11.5, ha="left", bold=True)
    for k, s in enumerate(STEPS):
        x = 0.3 + k * 2.9
        box(ax, x, 4.3, 2.5, 1.1, fc=PAPER, ec=INK, lw=1.4)
        label(ax, x + 1.25, 4.85, s, fs=10, color=INK)
        if k < 3:
            arrow(ax, (x + 2.55, 4.85), (x + 2.85, 4.85), color=INK, ms=11)
    label(ax, 0.3, 3.25, "microVM", fs=11.5, ha="left", bold=True, color=RED)
    for k, s in enumerate(STEPS):
        x = 0.3 + k * 2.9
        if k < 2:
            ax.add_patch(Rectangle((x, 1.6), 2.5, 1.1, fc="white", ec=GREY, lw=1.0, ls="--"))
            label(ax, x + 1.25, 2.15, "건너뜀", fs=10.5, color=GREY)
            continue
        s2 = "커널 올리기\n장치 몇 개" if k == 2 else s
        box(ax, x, 1.6, 2.5, 1.1, fc=PINK, ec=RED, lw=1.6)
        label(ax, x + 1.25, 2.15, s2, fs=10, color=RED, bold=True)
        if k < 3:
            arrow(ax, (x + 2.55, 2.15), (x + 2.85, 2.15), color=RED, ms=11)


# ── 9. Kata Containers ───────────────────────────────────────────
def kata(ax):
    window(ax, 0.2, 4.3, 3.4, 1.9, "쿠버네티스")
    label(ax, 1.9, 5.0, "주문 화면 파드", fs=10.5, color=INK)
    label(ax, 1.9, 2.75, "Kata Containers", fs=11, bold=True, color=RED)
    arrow(ax, (1.9, 4.25), (1.9, 3.05), color=INK, ms=12)
    ground(ax, 4.6, 11.7, 1.3)
    band(ax, 4.6, 11.7, 1.3, h=0.45)
    house(ax, 6.1, 1.75, 4.0, 3.6, "", kern="커널")
    arrow(ax, (3.3, 2.75), (6.0, 2.75), color=RED, ms=13)
    label(ax, 4.65, 3.05, "집 짓기", fs=10, color=RED)
    cell(ax, 6.75, 3.05, 2.7, 0.55, "에이전트", hot=True, fs=10.5)
    arrow(ax, (8.1, 3.65), (8.1, 4.0), color=RED, ms=11)
    cell(ax, 6.55, 4.05, 3.1, 0.55, "주문 화면 컨테이너", hot=True, fs=10)
    label(ax, 8.1, 6.25, "microVM", fs=11.5, color=RED, bold=True)


# ── 10. 갈림길 ───────────────────────────────────────────────────
def decide():
    fig, ax = canvas(7.4, 4.4, 15, 9)
    box(ax, 3.5, 7.4, 8.0, 1.1, fc=NOTE)
    label(ax, 7.5, 7.95, "남이 만든 코드나 낯선 요청?", fs=11, bold=True)
    arrow(ax, (4.5, 7.3), (2.8, 6.0)); label(ax, 3.2, 6.8, "아니요", fs=10, color=INK)
    box(ax, 0.6, 4.6, 4.4, 1.3, fc=PAPER)
    label(ax, 2.8, 5.25, "컨테이너", fs=11)
    arrow(ax, (10.5, 7.3), (11.6, 6.0), color=RED); label(ax, 11.6, 6.8, "예", fs=10, color=RED)
    box(ax, 9.0, 4.6, 5.4, 1.3, fc=NOTE)
    label(ax, 11.7, 5.25, "GPU 같은 장치?", fs=11, bold=True)
    arrow(ax, (10.3, 4.5), (8.6, 3.0)); label(ax, 8.9, 3.9, "예", fs=10, color=INK)
    box(ax, 5.0, 1.4, 4.2, 1.4, fc=PAPER)
    label(ax, 7.1, 2.1, "보통 VM", fs=11)
    arrow(ax, (13.0, 4.5), (13.0, 2.9), color=RED); label(ax, 13.3, 3.7, "아니요", fs=10, color=RED, ha="left")
    box(ax, 10.6, 1.4, 4.1, 1.4, fc=PINK, ec=RED)
    label(ax, 12.65, 2.1, "microVM", fs=11.5, color=RED, bold=True)
    save(fig, OUT, "k8s05-decide.svg")


if __name__ == "__main__":
    one(opening, "k8s05-open-1.svg", lim=(12, 5.6))
    one(house_shared, "k8s05-house-1.svg")
    one(house_apart, "k8s05-house-2.svg")
    one(hyper_block, "k8s05-hyper-1.svg")
    one(hyper_two, "k8s05-hyper-2.svg")
    one(device_door, "k8s05-device-1.svg")
    one(device_count, "k8s05-device-2.svg", size=(7.6, 4.6), lim=(14, 8.2))
    one(boot, "k8s05-boot-1.svg")
    one(kata, "k8s05-kata-1.svg")
    decide()
