"""쿠버네티스 2편 그림 만들기. 실행: python lab/fig_k8s02.py  → docs/kubernetes/img/02/*.svg

대표 비유는 투명 필름 겹치기. 층(레이어) 하나 = 비스듬한 필름 한 장, 파일 = 필름 위 칸.
예시는 빵집 주문 앱: 주문 화면 이미지(a3f 바탕 · 7c2 실행 도구 · e91 주문 화면 코드)를 먼저 받고,
주문 처리 이미지(a3f · 7c2 · 4b8 주문 처리 코드)를 나중에 받는다. 고치는 파일은 바탕 층의 설정 파일.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "es"))
from figkit import (GREY, INK, PAPER, PINK, RED, arrow, box, canvas, cell,  # noqa: E402
                    label, outdir, save, stage)
from fig_k8s01 import building, window  # noqa: E402
from matplotlib.patches import Polygon, Rectangle  # noqa: E402

OUT = outdir("02", topic="kubernetes")
BASE = ("a3f", "바탕 층")
RUN = ("7c2", "실행 도구 층")
WEB = ("e91", "주문 화면 코드 층")
APP = ("4b8", "주문 처리 코드 층")


# ── 필름 한 장 ─────────────────────────────────────────────────────
def film(ax, x, y, w, name, chips, hot=False, dim=False, hot_chips=(), dim_chips=(), skew=0.5, fs=9.5):
    """비스듬한 투명 필름. chips=[(필름 왼쪽에서 x, 글자)]. 왼쪽에 층 이름."""
    ec = RED if hot else (GREY if dim else INK)
    ax.add_patch(Polygon([(x, y), (x + w, y), (x + w + skew, y + 0.6), (x + skew, y + 0.6)], closed=True,
                         fc=PINK if hot else "#eef3f8", ec=ec, lw=1.8 if hot else 1.2, alpha=0.9))
    if name:
        label(ax, x - 0.15, y + 0.3, name, fs=10, ha="right", color=ec, bold=hot)
    for k, (cx, s) in enumerate(chips):
        cw = max(1.25, 0.21 * len(s) + 0.35)
        cell(ax, x + cx, y + 0.12, cw, 0.38, s, hot=(k in hot_chips), dim=dim or (k in dim_chips), fs=fs)


def blank(ax, x, y, w, h):
    ax.add_patch(Rectangle((x, y), w, h, fc="white", ec=GREY, lw=1.0, ls="--"))


# ── 여는 장면: 이미지 받기 화면 ───────────────────────────────────
def pull_win(ax, x, y, title, lines, hot=(), dim=False):
    """lines=[(지문, 층 이름, 상태)]."""
    window(ax, x, y, 5.6, 2.6, title)
    for k, (d, n, st) in enumerate(lines):
        yy = y + 1.65 - k * 0.5
        on = k in hot
        if on:
            ax.add_patch(Rectangle((x + 0.1, yy - 0.21), 5.4, 0.42, fc=PINK, ec=RED, lw=1.5))
        c = RED if on else (GREY if dim else "#222")
        label(ax, x + 0.25, yy, d, fs=10.5, ha="left", color=c, bold=on, family="monospace")
        label(ax, x + 0.9, yy, n, fs=10.5, ha="left", color=c, bold=on)
        label(ax, x + 5.4, yy, st, fs=10.5, ha="right", color=c, bold=on)


def opening(ax):
    first = [(*BASE, "다 받았어요"), (*RUN, "다 받았어요"), (*WEB, "다 받았어요")]
    second = [(*BASE, "이미 있어요"), (*RUN, "이미 있어요"), (*APP, "받는 중")]
    pull_win(ax, 0.3, 3.6, "주문 화면 이미지 받기", first, dim=True)
    pull_win(ax, 6.1, 0.7, "주문 처리 이미지 받기", second, hot=(2,))
    label(ax, 3.1, 2.4, "새로 받는 층: 1개", fs=11, color=RED, bold=True)


# ── 이미지: 칸 안의 파일은 어디서 오나 ─────────────────────────────
FILES = ["기본 도구", "설정 파일", "실행 도구", "주문 처리 코드"]


def image_box(ax, x, y, hot=False, name="주문 처리 이미지"):
    box(ax, x, y, 3.4, 2.7, fc=PINK if hot else PAPER, ec=RED if hot else INK)
    label(ax, x + 1.7, y + 2.35, name, fs=10.5, color=RED if hot else "#222", bold=True)
    for k, f in enumerate(FILES):
        cell(ax, x + 0.4, y + 1.65 - k * 0.5, 2.6, 0.42, f, fs=9.5)


def image(ax):
    building(ax, 0.4, 0.8, 6.6, 3.8, ["주문 화면", "주문 처리", "주문 장부"], room_hot=(1,), fs=9.5)
    image_box(ax, 8.2, 1.6, hot=True)
    arrow(ax, (8.1, 4.0), (3.75, 3.75), color=RED, ms=14, rad=0.3)
    label(ax, 9.9, 1.1, "파일 묶음 + 실행 방법", fs=10.5, color=RED)


# ── 통째 한 덩어리로 두면 ─────────────────────────────────────────
def whole(ax):
    box(ax, 0.3, 0.9, 11.4, 4.6, fc="white")
    label(ax, 0.55, 5.15, "이 컴퓨터의 디스크", fs=10.5, ha="left", color=INK, bold=True)
    for k, (name, last) in enumerate((("주문 화면 이미지", "주문 화면 코드"), ("주문 처리 이미지", "주문 처리 코드"))):
        x = 0.8 + k * 5.6
        box(ax, x, 1.3, 4.6, 3.3, fc=PAPER)
        label(ax, x + 2.3, 4.25, name, fs=10.5, bold=True)
        for j, f in enumerate(["기본 도구", "설정 파일", "실행 도구", last]):
            cell(ax, x + 0.5, 3.45 - j * 0.6, 3.6, 0.5, f, hot=(k == 1 and j < 3), fs=10)
    label(ax, 6.0, 6.0, "같은 파일 3개 × 2번", fs=11.5, color=RED, bold=True)


# ── 투명 필름 겹치기 ──────────────────────────────────────────────
FX, FW = 2.6, 5.4
FY = [0.9, 2.0, 3.1]


def films(ax):
    film(ax, FX, FY[0], FW, "a3f 바탕 층", [(0.2, "기본 도구"), (1.75, "설정 파일")])
    film(ax, FX, FY[1], FW, "7c2 실행 도구 층", [(3.0, "실행 도구")])
    film(ax, FX, FY[2], FW, "4b8 코드 층", [(3.4, "주문 처리 코드")], fs=9)
    ax.annotate("", xy=(8.9, 4.5), xytext=(8.9, 5.6), arrowprops=dict(arrowstyle="-|>", color=RED, lw=1.8))
    label(ax, 8.75, 5.95, "위에서 내려다보면", fs=10.5, color=RED, bold=True)
    box(ax, 9.3, 0.9, 2.5, 3.2, fc=PINK, ec=RED)
    label(ax, 10.55, 3.75, "보이는 파일", fs=9.5, color=RED, bold=True)
    for k, f in enumerate(FILES):
        cell(ax, 9.5, 2.9 - k * 0.55, 2.1, 0.45, f, fs=9)


# ── 같은 층은 한 번만 ──────────────────────────────────────────────
def layer_chip(ax, x, y, d, n, hot=False, dim=False, w=3.2):
    cell(ax, x, y, w, 0.55, f"{d}  {n}", hot=hot, dim=dim, fs=10)


def share(ax, step):
    box(ax, 0.3, 0.8, 5.2, 4.6, fc="white")
    label(ax, 2.9, 5.05, "이 컴퓨터에 있는 층", fs=10.5, color=INK, bold=True)
    have = [BASE, RUN, WEB] + ([APP] if step == 3 else [])
    for k, (d, n) in enumerate(have):
        layer_chip(ax, 0.6, 4.1 - k * 0.8, d, n, w=4.6, hot=(step == 2 and k < 2) or (step == 3 and k == 3))
    box(ax, 7.0, 2.2, 4.7, 3.2, fc=PAPER)
    label(ax, 9.35, 5.05, "주문 처리 이미지의 층 목록", fs=10.5, bold=True)
    for k, (d, n) in enumerate([BASE, RUN, APP]):
        layer_chip(ax, 7.25, 4.1 - k * 0.8, d, n, w=4.2, hot=(step == 2 and k < 2) or (step == 3 and k == 2))
    if step == 2:
        for k in range(2):
            arrow(ax, (7.15, 4.37 - k * 0.8), (5.3, 4.37 - k * 0.8), color=RED, ms=12)
            label(ax, 6.25, 4.6 - k * 0.8, "같은 지문", fs=9, color=RED)
        label(ax, 9.35, 1.6, "a3f · 7c2: 이미 있음", fs=10.5, color=RED, bold=True)
    else:
        arrow(ax, (7.15, 2.77), (5.3, 1.97), color=RED, ms=12)
        label(ax, 9.35, 1.6, "4b8만 받음", fs=10.5, color=RED, bold=True)


# ── 쓸 때 복사 ─────────────────────────────────────────────────────
SX = 1.9
TOPS = [(1.0, "컨테이너 1"), (6.6, "컨테이너 2")]


def cow_stage(ax, top1=(), top2=(), hot1=(), hot2=(), base_hot=False, base_dim=False):
    film(ax, 3.4, 0.6, 5.0, "a3f 바탕 층", [(0.2, "기본 도구"), (1.75, "설정 파일")], hot_chips=(1,) if base_hot else (),
         dim_chips=(1,) if base_dim else ())
    film(ax, 3.4, 1.45, 5.0, "7c2 실행 도구 층", [(3.0, "실행 도구")])
    film(ax, 3.4, 2.3, 5.0, "4b8 코드 층", [(3.0, "주문 처리 코드")], fs=9)
    label(ax, 9.5, 1.75, "이미지 층:\n읽기만\n(둘이 같이)", fs=9.5, ha="left", color=INK)
    for k, (x, name) in enumerate(TOPS):
        y = 3.75
        chips, hot = (top1, hot1) if k == 0 else (top2, hot2)
        film(ax, x, y, 4.3, "", [(c, s) for c, s in chips], hot=bool(hot), hot_chips=hot)
        label(ax, x + 2.4, y + 1.05, f"{name} 쓰기 층", fs=10, bold=True)
        ax.plot([x + 2.4, 5.9 + (k - 0.5) * 1.2], [y - 0.05, 2.95], color=GREY, lw=1.2, ls=":")


def cow(ax, step):
    if step == 1:
        cow_stage(ax, top1=[(1.75, "설정 파일")], hot1=(0,), base_hot=True)
        ax.annotate("", xy=(2.9, 3.85), xytext=(5.0, 1.05),
                    arrowprops=dict(arrowstyle="-|>", color=RED, lw=1.8, connectionstyle="arc3,rad=-0.3"))
        label(ax, 6.0, 0.15, "① 복사  ② 복사본 고치기", fs=10.5, color=RED, bold=True)
    else:
        cow_stage(ax, top1=[(1.75, "설정 파일*")], hot1=(0,))
        label(ax, 3.2, 5.2, "보이는 것: 설정 파일*", fs=9.5, color=RED)
        label(ax, 8.8, 5.2, "보이는 것: 원래 설정 파일", fs=9.5, color=INK)


# ── 컨테이너를 지우면 ─────────────────────────────────────────────
def remove(ax):
    building(ax, 0.4, 0.8, 6.6, 3.8, ["주문 화면", "주문 처리", "주문 장부"], room_hot=(2,), fs=9.5)
    cyl_x = 8.6
    box(ax, cyl_x, 1.2, 3.0, 2.2, fc=PINK, ec=RED)
    label(ax, cyl_x + 1.5, 2.6, "따로 붙인 디스크", fs=10.5, color=RED, bold=True)
    cell(ax, cyl_x + 0.4, 1.55, 2.2, 0.5, "주문 장부 파일", hot=True, fs=9.5)
    arrow(ax, (5.9, 2.7), (cyl_x - 0.1, 2.3), color=RED, ms=14)
    label(ax, 10.1, 4.1, "컨테이너를 지워도 남음", fs=10, color=RED)


def one(draw, name, size=(7.2, 3.8), lim=(12, 6.6)):
    """한 장 그림."""
    fig, ax = canvas(*size, *lim)
    draw(ax)
    save(fig, OUT, name)


if __name__ == "__main__":
    S, L = (7.2, 3.8), (12, 6.6)
    one(opening, "k8s02-open.svg")
    one(image, "k8s02-image.svg")
    one(whole, "k8s02-whole.svg")
    one(films, "k8s02-film.svg")
    stage(lambda ax, k: share(ax, k + 1), 2, OUT, "k8s02-share", S, L)
    stage(cow, 2, OUT, "k8s02-cow", S, L)
    one(remove, "k8s02-remove.svg")
