"""쿠버네티스 14편 그림 만들기. 실행: python lab/fig_k8s14.py  → docs/kubernetes/img/14/*.svg

본문 절은 장면 띠로 그린다: 같은 무대를 여러 장 그리고 장마다 바뀐 곳만 빨강으로 칠한다.
예시는 빵집 주문 앱의 주문 처리가 다시 뜨는 데 오래 걸리는 장면. 디스크에 부탁하는 일은 "블록 6 읽기".
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "es"))
from figkit import (GREY, INK, LIGHT, NOTE, PAPER, PINK, RED, arrow, box, bubble,  # noqa: E402
                    canvas, cell, label, moral, outdir, save, stage)
from matplotlib.patches import Rectangle  # noqa: E402

OUT = outdir("14", topic="kubernetes")


def fixed(draw):
    """장마다 그림 크기가 같도록 무대 테두리를 흰색으로 그린다."""
    def f(ax, step):
        ax.add_patch(Rectangle((0, -0.6), 12, 7.2, fill=False, ec="white", lw=0.5))
        draw(ax, step)
    return f


def part(ax, x, y, w, h, s, hot=False, dim=False, fs=11, fc=None):
    ec = RED if hot else (GREY if dim else INK)
    box(ax, x, y, w, h, fc=fc or (PINK if hot else (LIGHT if dim else NOTE)), ec=ec, lw=2.0 if hot else 1.5)
    label(ax, x + w / 2, y + h / 2, s, fs=fs, color=RED if hot else (GREY if dim else "#222"), bold=hot)


# ── 여는 장면: 다시 뜨는 데 오래 걸려요 ─────────────────────────────
def screen(ax, engine_hot=False, slow_hot=False, slow_grey=False):
    box(ax, 0.4, 0.75, 7.4, 5.6, fc="white", round_=False)
    ax.add_patch(Rectangle((0.4, 5.9), 7.4, 0.45, fc=LIGHT, ec=INK, lw=1.2))
    label(ax, 0.6, 6.12, "빵집 앱 관리 화면", fs=11, ha="left", color=INK)
    c = RED if slow_hot else (GREY if slow_grey else "#222")
    box(ax, 0.8, 3.9, 6.6, 1.65, fc=PINK if slow_hot else NOTE, ec=RED if slow_hot else INK)
    label(ax, 1.0, 5.15, "주문 처리 · 다시 시작하는 중", fs=11.5, ha="left", color=c, bold=slow_hot)
    ax.add_patch(Rectangle((1.0, 4.3), 4.6, 0.35, fc="white", ec=INK, lw=1.0))
    ax.add_patch(Rectangle((1.0, 4.3), 1.5, 0.35, fc=RED if slow_hot else "#9aa3ad", ec="none"))
    label(ax, 5.8, 4.47, "한참 걸려요", fs=11, ha="left", color=c, bold=slow_hot)
    box(ax, 0.8, 1.3, 6.6, 2.1, fc="white", ec=RED if engine_hot else INK)
    label(ax, 1.0, 3.0, "주문 장부 디스크 · 저장 엔진", fs=11, ha="left", color=RED if engine_hot else INK,
          bold=engine_hot)
    label(ax, 1.2, 2.3, "◉ v1", fs=11.5, ha="left")
    label(ax, 3.0, 2.3, "○ v2 (더 빠름)", fs=11.5, ha="left", color=RED if engine_hot else "#222", bold=engine_hot)


def opening(ax, step):
    if step == 1:
        screen(ax, slow_hot=True)
        bubble(ax, 8.2, 3.9, 3.6, 1.4, "주문 처리가 다시\n뜨는 데 한참 걸려요", (7.45, 4.6), hot=True, fs=10.5)
    else:
        screen(ax, engine_hot=True)
        bubble(ax, 8.2, 1.7, 3.6, 1.4, "엔진을 v2로 바꾸면\n빨라질까요?", (7.45, 2.3), hot=True, fs=10.5)


# ── 디스크에 부탁하면 ───────────────────────────────────────────────
APP = (0.3, 4.6, 3.2, 1.0)
KER = (4.4, 4.6, 3.2, 1.0)
DSK = (8.5, 4.6, 3.2, 1.0)


def path(ax, step):
    part(ax, *APP, "주문 처리\n(프로그램)", dim=(step == 2), fs=10.5)
    part(ax, *KER, "커널", fs=11)
    part(ax, *DSK, "디스크", hot=(step == 2), fs=11)
    if step == 1:
        arrow(ax, (3.6, 5.1), (4.3, 5.1), color=RED, ms=14)
        label(ax, 3.95, 3.95, "시스템 호출\n블록 6 읽어 줘", fs=10, color=RED, bold=True)
        arrow(ax, (7.7, 5.1), (8.4, 5.1), ms=14)
        label(ax, 6.0, 2.6, "커널이 부탁을 받아 디스크에 전해요", fs=11, color=RED)
    else:
        arrow(ax, (3.6, 5.1), (4.3, 5.1), color=GREY, ms=14)
        arrow(ax, (7.7, 5.1), (8.4, 5.1), color=GREY, ms=14)
        label(ax, 1.9, 3.9, "기다리는 중 …", fs=10.5, color=GREY)
        label(ax, 10.1, 3.9, "블록 6을 찾는 중", fs=10.5, color=RED, bold=True)
        moral(ax, 6.0, 2.4, "디스크가 일하는 동안 프로그램은 기다려요")
        label(ax, 6.0, 1.6, "끝난 걸 어떻게 알까요?", fs=11, color=INK)


# ── 인터럽트 ───────────────────────────────────────────────────────
def cpu(ax, x, y, s, hot=False, dim=False, w=3.4):
    part(ax, x, y, w, 1.1, s, hot=hot, dim=dim, fs=10.5)
    label(ax, x + w / 2, y + 1.35, "CPU", fs=10, color=INK, bold=True)


def interrupt(ax, step):
    cpu(ax, 0.5, 4.2, "하던 일 멈춤 · 인터럽트 처리" if step >= 2 else "다른 프로그램 일",
        hot=(step == 2), w=4.4)
    part(ax, 8.3, 4.2, 3.4, 1.1, "디스크 · 블록 6 끝" if step >= 2 else "디스크 · 블록 6 찾는 중", fs=10.5)
    part(ax, 0.5, 1.6, 4.4, 1.0, "주문 처리 · 블록 6 받음" if step == 3 else "주문 처리 · 기다리는 중",
         hot=(step == 3), dim=(step < 3), fs=10.5)
    if step == 1:
        label(ax, 6.0, 3.3, "디스크가 일하는 동안 CPU는 다른 일을 해요", fs=11, color=RED)
    if step >= 2:
        arrow(ax, (8.2, 4.75), (5.0, 4.75), color=RED if step == 2 else GREY, ms=15, lw=2.2)
        label(ax, 6.6, 5.1, "딩동, 끝났어요!", fs=11, color=RED if step == 2 else GREY, bold=(step == 2))
    if step == 3:
        arrow(ax, (2.7, 4.1), (2.7, 2.7), color=RED, ms=14)
        label(ax, 2.9, 3.4, "커널이 깨워요", fs=10.5, ha="left", color=RED)
        moral(ax, 6.0, 0.6, "끝나면 디스크가 CPU를 불러 세워요")


# ── 폴링 ───────────────────────────────────────────────────────────
def polling(ax, step):
    label(ax, 2.2, 6.15, "CPU 코어 하나", fs=10, color=INK, bold=True)
    part(ax, 0.5, 4.6, 3.4, 1.1, "확인 담당", hot=True, fs=11)
    box(ax, 5.0, 3.9, 3.0, 2.0, fc="white")
    label(ax, 6.5, 6.15, "끝난 일 목록", fs=10, color=INK, bold=True)
    if step == 1:
        label(ax, 6.5, 4.9, "(비었음)", fs=10.5, color=GREY)
    else:
        cell(ax, 5.3, 4.55, 2.4, 0.7, "블록 6 끝", hot=True, fs=10.5)
    part(ax, 9.2, 4.6, 2.5, 1.1, "디스크", fs=11)
    arrow(ax, (4.0, 5.35), (4.9, 5.35), color=RED, ms=13)
    arrow(ax, (4.9, 4.75), (4.0, 4.75), color=RED, ms=13)
    label(ax, 4.45, 5.75, "보고", fs=9.5, color=RED)
    if step == 1:
        label(ax, 4.45, 4.35, "또 보고", fs=9.5, color=RED)
        label(ax, 6.0, 2.9, "아직? 아직? 아직? … 쉬지 않고 들여다봐요", fs=11, color=RED, bold=True)
        arrow(ax, (9.1, 5.15), (8.1, 5.15), color=GREY, ms=12)
    else:
        arrow(ax, (9.1, 5.15), (8.1, 5.15), color=RED, ms=13)
        label(ax, 8.6, 5.55, "적어요", fs=9.5, color=RED)
        label(ax, 6.0, 2.9, "다음 확인에서 바로 찾아요", fs=11, color=RED, bold=True)
        moral(ax, 6.0, 1.7, "끝나자마자 알지만, 코어 하나는 확인만 해요")


# ── 커널 우회 ───────────────────────────────────────────────────────
def bypass(ax, step):
    ax.plot([0.2, 11.8], [4.0, 4.0], color=GREY, lw=1.3, ls="--")
    ax.plot([0.2, 11.8], [2.1, 2.1], color=GREY, lw=1.3, ls="--")
    label(ax, 0.3, 5.9, "프로그램 자리", fs=10, ha="left", color=INK, bold=True)
    label(ax, 0.3, 3.7, "커널 자리", fs=10, ha="left", color=INK, bold=True)
    label(ax, 0.3, 1.8, "장치", fs=10, ha="left", color=INK, bold=True)
    part(ax, 4.6, 0.6, 2.8, 0.95, "디스크", fs=11)
    if step == 1:
        part(ax, 4.6, 4.5, 2.8, 1.0, "저장 엔진", fs=10.5)
        part(ax, 4.6, 2.55, 2.8, 1.0, "커널의 디스크 드라이버", fs=9.5)
        arrow(ax, (6.0, 4.45), (6.0, 3.62), color=RED, ms=13)
        arrow(ax, (6.0, 2.5), (6.0, 1.62), color=RED, ms=13)
        label(ax, 6.2, 4.3, "시스템 호출", fs=10, ha="left", color=RED)
        label(ax, 6.2, 1.8, "인터럽트로 끝을 알려요", fs=10, ha="left", color=RED)
        label(ax, 9.8, 5.0, "보통 길", fs=11, color=RED, bold=True)
    else:
        part(ax, 4.6, 4.5, 2.8, 1.0, "SPDK로 만든 엔진", hot=True, fs=10.5)
        part(ax, 4.6, 2.55, 2.8, 1.0, "커널의 디스크 드라이버", dim=True, fs=9.5)
        label(ax, 9.3, 3.05, "디스크를 내놓았어요", fs=10, color=GREY)
        ax.annotate("", xy=(4.5, 1.05), xytext=(4.5, 4.95),
                    arrowprops=dict(arrowstyle="-|>", color=RED, lw=2.2, mutation_scale=14,
                                    connectionstyle="arc3,rad=0.5"))
        label(ax, 2.0, 3.0, "직접 다뤄요\n(폴링으로 확인)", fs=10, color=RED, bold=True)
        moral(ax, 6.0, -0.2, "커널을 거치지 않고 엔진이 디스크를 직접 다뤄요")


# ── 전환: 얻은 것과 치르는 값 ───────────────────────────────────────
def turn(ax, step):
    part(ax, 0.4, 3.0, 3.0, 1.4, "SPDK로\n만든 엔진", fs=11)
    if step == 1:
        bubble(ax, 4.2, 2.4, 7.4, 2.6,
               "얻은 것\n· 시스템 호출을 건너뛰어요\n· 초인종에 불려 가지 않아요\n· 끝나자마자 알아요",
               (3.45, 3.7), hot=True, fs=11)
    else:
        bubble(ax, 4.2, 2.4, 7.4, 2.6,
               "그 대신\n① CPU 코어 하나를 늘 써요\n② 큰 메모리 페이지를 미리 잡아 둬요",
               (3.45, 3.7), hot=True, fs=11)


# ── 첫째 값: 코어 하나 ──────────────────────────────────────────────
def core(ax, step):
    label(ax, 0.3, 6.1, "낮 · 주문이 몰려요" if step == 1 else "밤 · 주문이 없어요", fs=11.5, ha="left",
          bold=True, color=RED if step == 2 else "#222")
    for i in range(4):
        x = 0.5 + i * 2.9
        box(ax, x, 1.6, 2.4, 3.6, fc="white")
        label(ax, x + 1.2, 5.55, f"코어 {i + 1}", fs=10.5, color=INK)
        if i == 0:
            hot = step == 2
            ax.add_patch(Rectangle((x + 0.2, 1.8), 2.0, 3.2, fc=PINK if hot else "#9aa3ad", ec=RED if hot else "none",
                                   lw=1.8))
            label(ax, x + 1.2, 3.4, "엔진의\n확인 담당", fs=10, color=RED if hot else "white", bold=True)
        else:
            frac = (0.7, 0.5, 0.6)[i - 1] if step == 1 else 0.08
            ax.add_patch(Rectangle((x + 0.2, 1.8), 2.0, 3.2 * frac, fc="#c9d6e3", ec="none"))
            label(ax, x + 1.2, 1.8 + 3.2 * frac + 0.3, "앱", fs=9.5, color=INK)
    if step == 2:
        moral(ax, 6.0, 0.8, "할 일이 없어도 코어 하나는 꽉 차 있어요")


# ── 둘째 값: 큰 메모리 페이지 ───────────────────────────────────────
def pages(ax, step):
    label(ax, 0.3, 6.15, "메모리", fs=11, ha="left", bold=True)
    for r in range(2):
        for c in range(10):
            x, y = 0.5 + c * 0.75, 4.6 - r * 0.75
            moved = step == 1 and (r, c) == (0, 3)
            ax.add_patch(Rectangle((x, y), 0.65, 0.65, fc=PINK if moved else NOTE,
                                   ec=RED if moved else INK, lw=1.8 if moved else 1.0,
                                   ls="--" if moved else "-"))
    part(ax, 9.0, 4.4, 2.6, 0.9, "디스크", fs=11)
    if step == 1:
        cell(ax, 0.5 + 7 * 0.75, 4.6, 0.65, 0.65, "", hot=True)
        arrow(ax, (0.5 + 3 * 0.75 + 0.33, 5.35), (0.5 + 7 * 0.75 + 0.33, 5.35), color=RED, ms=12, rad=-0.4)
        label(ax, 4.0, 6.15, "운영체제는 작은 페이지를 이리저리 옮겨요", fs=10.5, color=RED, ha="left")
        label(ax, 4.0, 2.6, "보통 프로그램은 옮겨도 몰라요. 주소를 운영체제가 바꿔 주니까요", fs=10, color=INK)
    elif step == 2:
        cell(ax, 0.5 + 3 * 0.75, 4.6, 0.65, 0.65, "?", hot=True)
        arrow(ax, (8.9, 4.85), (0.5 + 3 * 0.75 + 0.7, 4.95), color=RED, ms=13)
        label(ax, 6.0, 5.75, "디스크가 메모리 자리에 직접 써요", fs=10, color=RED)
        label(ax, 4.0, 2.6, "쓰는 사이 페이지가 옮겨 가면 엉뚱한 자리에 써요", fs=10.5, color=RED, bold=True)
    else:
        ax.add_patch(Rectangle((0.45, 3.8), 2.95, 1.5, fc=PINK, ec=RED, lw=2.2))
        label(ax, 1.97, 4.55, "큰 페이지\n(미리 잡아 둠)", fs=10, color=RED, bold=True)
        arrow(ax, (8.9, 4.85), (3.6, 4.85), color=RED, ms=13)
        label(ax, 6.2, 5.75, "늘 같은 자리", fs=10, color=RED)
        label(ax, 4.0, 2.6, "이 자리는 다른 프로그램이 쓸 수 없어요", fs=10.5, color=INK)
        moral(ax, 6.0, 1.7, "옮기지 않는 큰 페이지를 미리 떼어 둬요")


# ── 병목 재기: 다시 뜨는 시간 나누기 ────────────────────────────────
def bar(ax, y, disk_w, prog_w, title, hot_disk=False, hot_prog=False, dim=False):
    label(ax, 0.3, y + 0.35, title, fs=10.5, ha="left", color=GREY if dim else "#222", bold=not dim)
    x = 2.6
    ax.add_patch(Rectangle((x, y), disk_w, 0.7, fc=PINK if hot_disk else ("#e5e7eb" if dim else "#c9d6e3"),
                           ec=RED if hot_disk else (GREY if dim else INK), lw=1.8 if hot_disk else 1.0))
    ax.add_patch(Rectangle((x + disk_w, y), prog_w, 0.7, fc=PINK if hot_prog else ("#f3f4f6" if dim else NOTE),
                           ec=RED if hot_prog else (GREY if dim else INK), lw=1.8 if hot_prog else 1.0))
    c = GREY if dim else "#222"
    if disk_w > 1.2:
        label(ax, x + disk_w / 2, y + 0.35, "디스크 기다림", fs=9.5, color=RED if hot_disk else c)
    label(ax, x + disk_w + prog_w / 2, y + 0.35, "프로그램 준비", fs=10, color=RED if hot_prog else c)


def measure(ax, step):
    label(ax, 6.0, 6.1, "주문 처리가 다시 뜨는 시간을 재서 나눠 봐요", fs=11, bold=True)
    bar(ax, 4.3, 1.6, 6.8, "다시 뜨는 시간", hot_prog=(step == 1))
    if step == 1:
        label(ax, 2.6 + 1.6 + 3.4, 3.7, "대부분이 프로그램 준비예요", fs=10.5, color=RED, bold=True)
        label(ax, 2.6 + 0.8, 3.7, "조금", fs=10, color=INK)
    else:
        bar(ax, 2.5, 0.5, 6.8, "v2로 바꾸면", hot_disk=True)
        label(ax, 2.6 + 0.25, 1.95, "줄어든 몫", fs=9.5, color=RED, ha="left")
        moral(ax, 6.0, 0.8, "디스크 몫만 줄어서 전체는 거의 그대로예요")


# ── 판단 (한 장) ───────────────────────────────────────────────────
def decide():
    fig, ax = canvas(10, 4.2, 15, 6.4)
    ax.set_ylim(-0.2, 6.4)
    box(ax, 0.3, 4.6, 6.4, 1.3, fc=NOTE)
    label(ax, 3.5, 5.25, "기다림을 재서 나눠 봤나요?", fs=10.5, bold=True)
    arrow(ax, (6.8, 5.25), (8.4, 5.25)); label(ax, 7.6, 5.55, "아니요", fs=10, color=INK)
    box(ax, 8.5, 4.6, 6.2, 1.3, fc=PAPER)
    label(ax, 11.6, 5.25, "먼저 재요", fs=10.5)
    arrow(ax, (3.5, 4.5), (3.5, 3.5)); label(ax, 3.8, 4.0, "예", fs=10, color=INK, ha="left")
    box(ax, 0.3, 2.2, 6.4, 1.2, fc=NOTE)
    label(ax, 3.5, 2.8, "기다림 대부분이 디스크인가요?", fs=10.5, bold=True)
    arrow(ax, (6.8, 2.8), (8.4, 2.8)); label(ax, 7.6, 3.1, "아니요", fs=10, color=INK)
    box(ax, 8.5, 2.2, 6.2, 1.2, fc=PAPER)
    label(ax, 11.6, 2.8, "엔진을 바꿔도 안 빨라져요", fs=10.5)
    arrow(ax, (3.5, 2.1), (3.5, 1.3), color=RED); label(ax, 3.8, 1.7, "예", fs=10, color=RED, ha="left")
    box(ax, 0.3, 0.1, 6.4, 1.1, fc=PINK, ec=RED)
    label(ax, 3.5, 0.65, "코어 하나·큰 페이지를 내줄 수 있으면 v2", fs=10.5, color=RED, bold=True)
    save(fig, OUT, "k8s14-decide.svg")


# ── 정리: 처음 장면으로 돌아가기 ───────────────────────────────────
def back(ax, step):
    if step == 1:
        screen(ax, slow_grey=True)
        bubble(ax, 8.2, 3.9, 3.6, 1.4, "엔진만 바꾸면\n빨라질 줄 알았어요", (7.45, 4.6), fs=10.5)
    elif step == 2:
        screen(ax, slow_hot=True)
        bubble(ax, 8.2, 3.9, 3.6, 1.6, "먼저 재 보니\n대부분이 프로그램\n준비였어요", (7.45, 4.6), hot=True, fs=10.5)
    else:
        screen(ax, slow_grey=True)
        bubble(ax, 8.2, 1.6, 3.6, 1.6, "그러면 엔진 대신\n프로그램이 뜨는\n과정을 줄여요", (7.45, 2.3), hot=True, fs=10.5)
        moral(ax, 4.1, 0.25, "병목이 디스크일 때만 빠른 엔진이 이득이에요")


# ── 정리: 낱말 카드 ────────────────────────────────────────────────
def cards():
    fig, ax = canvas(6.4, 7.3, 9.8, 12.4)
    W_, H_ = 4.6, 3.8

    def card(i, name, line):
        col, row_ = i % 2, i // 2
        x, y = 0.2 + col * 4.9, 8.4 - row_ * 4.05
        box(ax, x, y, W_, H_, fc="white")
        label(ax, x + 0.25, y + H_ - 0.4, name, fs=12.5, ha="left", bold=True)
        label(ax, x + W_ / 2, y + 0.6, line, fs=10, color=INK)
        return x, y

    x, y = card(0, "인터럽트", "일이 끝나면 장치가\nCPU를 불러 세우는 신호")
    cell(ax, x + 0.4, y + 1.6, 1.4, 0.8, "디스크", fs=10)
    arrow(ax, (x + 1.9, y + 2.0), (x + 2.8, y + 2.0), color=RED, ms=11)
    cell(ax, x + 2.9, y + 1.6, 1.3, 0.8, "CPU", hot=True, fs=10)
    x, y = card(1, "폴링", "끝났는지 쉬지 않고\n직접 들여다보는 방식")
    cell(ax, x + 0.4, y + 1.6, 1.6, 0.8, "확인 담당", hot=True, fs=10)
    arrow(ax, (x + 2.1, y + 2.15), (x + 2.7, y + 2.15), color=RED, ms=10)
    arrow(ax, (x + 2.7, y + 1.85), (x + 2.1, y + 1.85), color=RED, ms=10)
    cell(ax, x + 2.8, y + 1.6, 1.4, 0.8, "목록", fs=10)
    x, y = card(2, "SPDK", "커널을 거치지 않고 폴링으로\n디스크를 다루는 도구 모음")
    cell(ax, x + 0.4, y + 1.6, 1.8, 0.8, "SPDK 엔진", hot=True, fs=10)
    arrow(ax, (x + 2.3, y + 2.0), (x + 2.8, y + 2.0), color=RED, ms=11)
    cell(ax, x + 2.9, y + 1.6, 1.3, 0.8, "디스크", fs=10)
    x, y = card(3, "큰 메모리 페이지", "옮기지 않도록 미리 떼어 둔\n큰 메모리 칸 (hugepage)")
    for c in range(4):
        cell(ax, x + 0.4 + c * 0.5, y + 1.7, 0.42, 0.42, "", fs=8)
    cell(ax, x + 2.6, y + 1.5, 1.6, 0.9, "", hot=True)
    save(fig, OUT, "k8s14-cards.svg")


if __name__ == "__main__":
    S, L = (7.2, 3.8), (12, 6.6)
    stage(fixed(opening), 2, OUT, "k8s14-open", S, L)
    stage(fixed(path), 2, OUT, "k8s14-path", S, L)
    stage(fixed(interrupt), 3, OUT, "k8s14-interrupt", S, L)
    stage(fixed(polling), 2, OUT, "k8s14-polling", S, L)
    stage(fixed(bypass), 2, OUT, "k8s14-bypass", S, L)
    stage(fixed(turn), 2, OUT, "k8s14-turn", S, L)
    stage(fixed(core), 2, OUT, "k8s14-core", S, L)
    stage(fixed(pages), 3, OUT, "k8s14-page", S, L)
    stage(fixed(measure), 2, OUT, "k8s14-measure", S, L)
    decide()
    stage(fixed(back), 3, OUT, "k8s14-back", S, L)
    cards()
