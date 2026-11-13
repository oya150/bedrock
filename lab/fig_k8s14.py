"""쿠버네티스 14편 그림 만들기. 실행: python lab/fig_k8s14.py  → docs/kubernetes/img/14/*.svg

예시는 빵집 주문 앱의 주문 장부(디스크를 쓰는 프로그램)가 다시 뜨는 데 오래 걸리는 장면. 디스크에 부탁하는 일은 "블록 6 읽기".
그림 안 글씨는 낱말과 숫자만 둔다. 지금 볼 곳만 빨강.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "es"))
from figkit import (GREY, INK, LIGHT, NOTE, PINK, RED, arrow, box, canvas, cell,  # noqa: E402
                    label, outdir, save)
from matplotlib.patches import Rectangle  # noqa: E402

OUT = outdir("14", topic="kubernetes")


def one(draw, name, ylo=0.0, yhi=6.4):
    """가로 0~12, 세로 ylo~yhi 만큼만 그린다. 그림 높이는 세로 폭에 맞춘다."""
    fig, ax = canvas(7.2, 7.2 * (yhi - ylo) / 12, 12, yhi)
    ax.set_ylim(ylo, yhi)
    draw(ax)
    save(fig, OUT, name)


def part(ax, x, y, w, h, s, hot=False, dim=False, fs=11, fc=None):
    ec = RED if hot else (GREY if dim else INK)
    box(ax, x, y, w, h, fc=fc or (PINK if hot else (LIGHT if dim else NOTE)), ec=ec, lw=2.0 if hot else 1.5)
    label(ax, x + w / 2, y + h / 2, s, fs=fs, color=RED if hot else (GREY if dim else "#222"), bold=hot)


# 그림 1: 프로그램 → 커널 → 디스크, 프로그램은 기다림
def path(ax):
    part(ax, 0.3, 3.4, 3.2, 1.1, "주문 장부", dim=True, fs=11)
    part(ax, 4.4, 3.4, 3.2, 1.1, "커널", fs=11)
    part(ax, 8.5, 3.4, 3.2, 1.1, "디스크", hot=True, fs=11)
    arrow(ax, (3.6, 3.95), (4.3, 3.95), ms=14)
    arrow(ax, (7.7, 3.95), (8.4, 3.95), ms=14)
    label(ax, 3.95, 5.35, "시스템 호출", fs=10, color=INK, bold=True)
    label(ax, 3.95, 4.95, "블록 6 읽어 줘", fs=10, color=INK)
    label(ax, 1.9, 2.8, "기다리는 중", fs=10.5, color=GREY)
    label(ax, 10.1, 2.8, "블록 6 찾는 중", fs=10.5, color=RED, bold=True)


# 그림 2: 인터럽트
def interrupt(ax):
    label(ax, 2.7, 5.55, "CPU", fs=10.5, color=INK, bold=True)
    part(ax, 0.5, 4.2, 4.4, 1.1, "하던 일 멈춤", hot=True, fs=10.5)
    part(ax, 8.3, 4.2, 3.4, 1.1, "디스크 · 블록 6 끝", fs=10.5)
    arrow(ax, (8.2, 4.75), (5.0, 4.75), color=RED, ms=15, lw=2.2)
    label(ax, 6.6, 5.1, "인터럽트", fs=11, color=RED, bold=True)
    part(ax, 0.5, 1.6, 4.4, 1.0, "주문 장부 · 블록 6 받음", fs=10.5)
    arrow(ax, (2.7, 4.1), (2.7, 2.7), ms=14)
    label(ax, 2.9, 3.4, "깨우기", fs=10.5, ha="left", color=INK)


# 그림 3: 폴링
def polling(ax):
    label(ax, 2.2, 5.15, "CPU 코어 하나", fs=10, color=INK, bold=True)
    part(ax, 0.5, 3.6, 3.4, 1.1, "확인 담당", hot=True, fs=11)
    box(ax, 5.2, 2.9, 2.8, 2.0, fc="white")
    label(ax, 6.5, 5.15, "끝난 일 목록", fs=10, color=INK, bold=True)
    cell(ax, 5.3, 3.55, 2.4, 0.7, "블록 6 끝", fs=10.5)
    part(ax, 9.2, 3.6, 2.5, 1.1, "디스크", fs=11)
    arrow(ax, (4.0, 4.35), (4.9, 4.35), color=RED, ms=13)
    arrow(ax, (4.9, 3.75), (4.0, 3.75), color=RED, ms=13)
    label(ax, 2.2, 3.1, "아직? 아직? 아직?", fs=10.5, color=RED, bold=True)
    arrow(ax, (9.1, 4.15), (8.1, 4.15), ms=13)
    label(ax, 8.6, 4.55, "적기", fs=9.5, color=INK)


# 그림 4·5: 보통 길과 커널을 건너뛰는 길
def bypass(skip):
    def draw(ax):
        ax.plot([0.2, 11.8], [4.0, 4.0], color=GREY, lw=1.3, ls="--")
        ax.plot([0.2, 11.8], [2.1, 2.1], color=GREY, lw=1.3, ls="--")
        label(ax, 0.3, 5.6, "프로그램", fs=10, ha="left", color=INK, bold=True)
        label(ax, 0.3, 3.7, "커널", fs=10, ha="left", color=INK, bold=True)
        label(ax, 0.3, 1.8, "장치", fs=10, ha="left", color=INK, bold=True)
        part(ax, 4.6, 0.6, 2.8, 0.95, "디스크", fs=11)
        if not skip:
            part(ax, 4.6, 4.5, 2.8, 1.0, "저장 엔진", fs=10.5)
            part(ax, 4.6, 2.55, 2.8, 1.0, "디스크 드라이버", hot=True, fs=10)
            arrow(ax, (6.0, 4.45), (6.0, 3.62), color=RED, ms=13)
            arrow(ax, (6.0, 2.5), (6.0, 1.62), color=RED, ms=13)
            label(ax, 6.2, 4.25, "시스템 호출", fs=10, ha="left", color=RED)
            label(ax, 6.2, 1.8, "인터럽트", fs=10, ha="left", color=RED)
        else:
            part(ax, 4.6, 4.5, 2.8, 1.0, "SPDK 엔진", hot=True, fs=10.5)
            part(ax, 4.6, 2.55, 2.8, 1.0, "디스크 드라이버", dim=True, fs=10)
            ax.annotate("", xy=(4.5, 1.05), xytext=(4.5, 4.95),
                        arrowprops=dict(arrowstyle="-|>", color=RED, lw=2.2, mutation_scale=14,
                                        connectionstyle="arc3,rad=0.5"))
            label(ax, 2.4, 3.05, "직접 · 폴링", fs=10.5, color=RED, bold=True)
            label(ax, 8.2, 3.05, "손 뗌", fs=10, color=GREY, ha="left")
    return draw


# 그림 6: 밤에도 꽉 찬 코어 하나
def core(ax):
    label(ax, 0.3, 6.1, "밤 · 주문 없음", fs=11.5, ha="left", bold=True)
    for i in range(4):
        x = 0.5 + i * 2.9
        box(ax, x, 1.6, 2.4, 3.6, fc="white")
        label(ax, x + 1.2, 5.55, f"코어 {i + 1}", fs=10.5, color=INK)
        if i == 0:
            ax.add_patch(Rectangle((x + 0.2, 1.8), 2.0, 3.2, fc=PINK, ec=RED, lw=1.8))
            label(ax, x + 1.2, 3.4, "확인 담당", fs=10.5, color=RED, bold=True)
        else:
            ax.add_patch(Rectangle((x + 0.2, 1.8), 2.0, 3.2 * 0.08, fc="#c9d6e3", ec="none"))
            label(ax, x + 1.2, 1.8 + 3.2 * 0.08 + 0.3, "앱", fs=9.5, color=INK)


# 그림 7·8: 페이지가 옮겨 가면 / 큰 페이지
def pages(big):
    def draw(ax):
        label(ax, 0.3, 6.0, "메모리", fs=11, ha="left", bold=True)
        for r in range(2):
            for c in range(10):
                if big and c < 4:
                    continue
                x, y = 0.5 + c * 0.75, 4.6 - r * 0.75
                moved = (not big) and (r, c) == (0, 3)
                ax.add_patch(Rectangle((x, y), 0.65, 0.65, fc="white" if moved else NOTE,
                                       ec=RED if moved else INK, lw=1.8 if moved else 1.0,
                                       ls="--" if moved else "-"))
        part(ax, 9.0, 4.4, 2.6, 0.9, "디스크", fs=11)
        if not big:
            cell(ax, 0.5 + 3 * 0.75, 4.6, 0.65, 0.65, "?", hot=True)
            ax.add_patch(Rectangle((0.5 + 3 * 0.75, 4.6), 0.65, 0.65, fill=False, ec=RED, lw=1.8, ls="--"))
            cell(ax, 0.5 + 7 * 0.75, 4.6, 0.65, 0.65, "", fc=LIGHT)
            arrow(ax, (0.5 + 3 * 0.75 + 0.33, 5.35), (0.5 + 7 * 0.75 + 0.33, 5.35), ms=12, rad=-0.4)
            label(ax, 0.5 + 5 * 0.75 + 0.33, 6.2, "옮김", fs=10, color=INK)
            arrow(ax, (8.9, 4.7), (0.5 + 3 * 0.75 + 0.75, 4.75), color=RED, ms=13)
            label(ax, 6.2, 3.45, "블록 6 쓰기", fs=10, color=RED, bold=True)
        else:
            ax.add_patch(Rectangle((0.45, 3.8), 2.95, 1.5, fc=PINK, ec=RED, lw=2.2))
            label(ax, 1.97, 4.55, "큰 페이지", fs=10.5, color=RED, bold=True)
            arrow(ax, (8.9, 4.85), (3.5, 4.85), color=RED, ms=13)
            label(ax, 6.2, 3.45, "블록 6 쓰기", fs=10, color=RED, bold=True)
            label(ax, 1.97, 3.4, "옮기지 않음", fs=10, color=INK)
    return draw


# 그림 9: 다시 뜨는 시간 나누기
def bar(ax, y, disk_w, prog_w, title, hot_disk=False):
    label(ax, 0.3, y + 0.35, title, fs=10.5, ha="left", bold=True)
    x = 2.6
    ax.add_patch(Rectangle((x, y), disk_w, 0.7, fc=PINK if hot_disk else "#c9d6e3",
                           ec=RED if hot_disk else INK, lw=1.8 if hot_disk else 1.0))
    ax.add_patch(Rectangle((x + disk_w, y), prog_w, 0.7, fc=NOTE, ec=INK, lw=1.0))
    if disk_w > 1.2:
        label(ax, x + disk_w / 2, y + 0.35, "디스크", fs=10)
    label(ax, x + disk_w + prog_w / 2, y + 0.35, "프로그램 준비", fs=10)


def measure(ax):
    bar(ax, 4.0, 6.6, 1.8, "v1")
    bar(ax, 2.2, 2.0, 1.8, "v2", hot_disk=True)
    ax.plot([2.6 + 6.6, 2.6 + 6.6], [4.0, 2.9], color=GREY, lw=1.0, ls=":")
    ax.plot([2.6 + 2.0, 2.6 + 2.0], [4.0, 2.9], color=GREY, lw=1.0, ls=":")
    label(ax, 6.5, 5.3, "주문 장부가 다시 뜨는 시간", fs=11, bold=True)


if __name__ == "__main__":
    one(path, "k8s14-path.svg", 2.3, 5.7)
    one(interrupt, "k8s14-interrupt.svg", 1.3, 5.9)
    one(polling, "k8s14-polling.svg", 2.6, 5.5)
    one(bypass(False), "k8s14-bypass-normal.svg", 0.3, 6.0)
    one(bypass(True), "k8s14-bypass-spdk.svg", 0.3, 6.0)
    one(core, "k8s14-core.svg", 1.3, 6.5)
    one(pages(False), "k8s14-page-move.svg", 3.0, 6.5)
    one(pages(True), "k8s14-page-huge.svg", 3.0, 6.5)
    one(measure, "k8s14-measure.svg", 1.4, 5.7)
