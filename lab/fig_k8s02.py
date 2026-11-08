"""쿠버네티스 2편 그림 만들기. 실행: python lab/fig_k8s02.py  → docs/kubernetes/img/02/*.svg

대표 비유는 투명 필름 겹치기. 층(레이어) 하나 = 비스듬한 필름 한 장, 파일 = 필름 위 칸.
예시는 빵집 주문 앱: 주문 화면 이미지(a3f 바탕 · 7c2 실행기 · e91 주문 화면 코드)를 먼저 받고,
주문 처리 이미지(a3f · 7c2 · 4b8 주문 처리 코드)를 나중에 받는다. 고치는 파일은 바탕 층의 설정 파일.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "es"))
from figkit import (GREY, INK, LIGHT, NOTE, PAPER, PINK, RED, arrow, box, canvas, cell,  # noqa: E402
                    label, moral, outdir, save, stage)
from fig_k8s01 import building, window  # noqa: E402
from matplotlib.patches import Polygon, Rectangle  # noqa: E402

OUT = outdir("02", topic="kubernetes")
BASE = ("a3f", "바탕 층")
RUN = ("7c2", "실행기 층")
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


def opening(ax, step):
    first = [(*BASE, "받는 중"), (*RUN, "받는 중"), (*WEB, "받는 중")]
    second = [(*BASE, "이미 있어요"), (*RUN, "이미 있어요"), (*APP, "받는 중")]
    if step == 1:
        pull_win(ax, 0.3, 3.6, "주문 화면 이미지 받기", first, hot=(0, 1, 2))
        label(ax, 3.1, 3.1, "처음엔 층 셋을 다 받아요", fs=11, color=RED)
    elif step == 2:
        pull_win(ax, 0.3, 3.6, "주문 화면 이미지 받기", [(d, n, "다 받았어요") for d, n, _ in first], dim=True)
        pull_win(ax, 6.1, 0.7, "주문 처리 이미지 받기", second, hot=(0, 1))
        label(ax, 3.1, 2.4, "두 번째 이미지는\n앞의 두 층이 이미 있대요", fs=11, color=RED)
    else:
        pull_win(ax, 0.3, 3.6, "주문 화면 이미지 받기", [(d, n, "다 받았어요") for d, n, _ in first], dim=True)
        pull_win(ax, 6.1, 0.7, "주문 처리 이미지 받기", second, hot=(2,))
        label(ax, 3.1, 2.4, "새로 받은 건\n맨 아래 한 층뿐이에요", fs=11, color=RED)
        moral(ax, 6.0, 0.25, "두 번째 이미지는 한 층만 받았어요")


# ── 이미지: 칸 안의 파일은 어디서 오나 ─────────────────────────────
FILES = ["기본 도구", "설정 파일", "실행기", "주문 처리 코드"]


def image_box(ax, x, y, hot=False, name="주문 처리 이미지"):
    box(ax, x, y, 3.4, 2.7, fc=PINK if hot else PAPER, ec=RED if hot else INK)
    label(ax, x + 1.7, y + 2.35, name, fs=10.5, color=RED if hot else "#222", bold=True)
    for k, f in enumerate(FILES):
        cell(ax, x + 0.4, y + 1.65 - k * 0.5, 2.6, 0.42, f, fs=9.5)


def image(ax, step):
    building(ax, 0.4, 0.8, 6.6, 3.8, ["주문 화면", "주문 처리", "주문 장부"], room_hot=(1,), fs=9.5)
    if step == 1:
        label(ax, 9.9, 4.8, "주문 처리 칸 안의 파일은\n어디서 올까요?", fs=11, color=RED, bold=True)
        image_box(ax, 8.2, 1.6)
    else:
        image_box(ax, 8.2, 1.6, hot=True)
        arrow(ax, (8.1, 3.9), (3.75, 3.65), color=RED, ms=14, rad=-0.35)
        label(ax, 9.9, 1.1, "파일 묶음 + 실행 방법", fs=10.5, color=RED)
        moral(ax, 6.0, 0.2, "이미지에서 칸 안의 파일을 꺼내 컨테이너를 만들어요")


# ── 통째 한 덩어리로 두면 ─────────────────────────────────────────
def whole(ax, step):
    box(ax, 0.3, 0.9, 11.4, 4.6, fc="white")
    label(ax, 0.55, 5.15, "이 컴퓨터의 디스크", fs=10.5, ha="left", color=INK, bold=True)
    for k, (name, last) in enumerate((("주문 화면 이미지", "주문 화면 코드"), ("주문 처리 이미지", "주문 처리 코드"))):
        x = 0.8 + k * 5.6
        box(ax, x, 1.3, 4.6, 3.3, fc=PAPER)
        label(ax, x + 2.3, 4.25, name, fs=10.5, bold=True)
        for j, f in enumerate(["기본 도구", "설정 파일", "실행기", last]):
            cell(ax, x + 0.5, 3.45 - j * 0.6, 3.6, 0.5, f, hot=(step == 2 and k == 1 and j < 3), fs=10)
    if step == 1:
        label(ax, 6.0, 6.0, "이미지마다 파일을 통째로 한 덩어리로 받아 두면", fs=11, color=INK)
    else:
        label(ax, 6.0, 6.0, "같은 파일 셋을 두 번 받고 두 번 저장해요", fs=11, color=RED, bold=True)
        moral(ax, 6.0, 0.35, "다른 건 코드 한 칸뿐인데 나머지 세 칸까지 또 받아요")


# ── 투명 필름 겹치기 ──────────────────────────────────────────────
FX, FW = 2.6, 5.4
FY = [0.9, 2.0, 3.1]


def films(ax, step):
    film(ax, FX, FY[0], FW, "a3f 바탕 층", [(0.2, "기본 도구"), (1.75, "설정 파일")], hot=(step == 1))
    if step >= 2:
        film(ax, FX, FY[1], FW, "7c2 실행기 층", [(3.0, "실행기")], hot=(step == 2))
    else:
        label(ax, FX + 3.0, FY[1] + 0.3, "", fs=9)
    if step >= 3:
        film(ax, FX, FY[2], FW, "4b8 코드 층", [(3.4, "주문 처리 코드")], hot=(step == 3), fs=9)
    notes = {1: "바탕 층: 기본 도구와 설정 파일을 담아요",
             2: "그 위에 실행기만 더한 층을 얹어요",
             3: "맨 위에 주문 처리 코드만 더한 층을 얹어요"}
    if step < 4:
        label(ax, 6.0, 5.9, notes[step], fs=11, color=RED, bold=True)
    else:
        ax.annotate("", xy=(8.9, 4.5), xytext=(8.9, 5.6), arrowprops=dict(arrowstyle="-|>", color=RED, lw=1.8))
        label(ax, 8.75, 5.95, "위에서 내려다보면", fs=10.5, color=RED, bold=True)
        box(ax, 9.3, 0.9, 2.5, 3.2, fc=PINK, ec=RED)
        label(ax, 10.55, 3.75, "칸 안에 보이는 파일", fs=9.5, color=RED, bold=True)
        for k, f in enumerate(FILES):
            cell(ax, 9.5, 2.9 - k * 0.55, 2.1, 0.45, f, fs=9)
        moral(ax, 5.0, 0.3, "필름을 겹쳐 내려다본 모습이 칸 안의 파일이에요", fs=11.5)


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
    if step == 1:
        label(ax, 9.35, 1.6, "지문 셋을 하나씩 맞춰 봐요", fs=10.5, color=RED, bold=True)
    elif step == 2:
        for k in range(2):
            arrow(ax, (7.15, 4.37 - k * 0.8), (5.3, 4.37 - k * 0.8), color=RED, ms=12)
            label(ax, 6.25, 4.6 - k * 0.8, "같은 지문", fs=9, color=RED)
        label(ax, 9.35, 1.6, "a3f, 7c2는 이미 있어요: 안 받아요", fs=10.5, color=RED, bold=True)
    else:
        arrow(ax, (7.15, 2.77), (5.3, 1.97), color=RED, ms=12)
        label(ax, 9.35, 1.6, "4b8 한 층만 받아요", fs=10.5, color=RED, bold=True)
        moral(ax, 6.0, 0.25, "같은 층은 한 번만 받고 한 번만 저장해요")


# ── 쓸 때 복사 ─────────────────────────────────────────────────────
SX = 1.9
TOPS = [(1.0, "컨테이너 1"), (6.6, "컨테이너 2")]


def cow_stage(ax, top1=(), top2=(), hot1=(), hot2=(), gone1=False, base_hot=False, base_dim=False):
    film(ax, 3.4, 0.6, 5.0, "a3f 바탕 층", [(0.2, "기본 도구"), (1.75, "설정 파일")], hot_chips=(1,) if base_hot else (),
         dim_chips=(1,) if base_dim else ())
    film(ax, 3.4, 1.45, 5.0, "7c2 실행기 층", [(3.0, "실행기")])
    film(ax, 3.4, 2.3, 5.0, "4b8 코드 층", [(3.0, "주문 처리 코드")], fs=9)
    label(ax, 9.5, 1.75, "같은 이미지 층을\n둘이 같이 봐요\n(읽기만)", fs=9.5, ha="left", color=INK)
    for k, (x, name) in enumerate(TOPS):
        y = 3.75
        chips, hot = (top1, hot1) if k == 0 else (top2, hot2)
        if k == 0 and gone1:
            ax.add_patch(Polygon([(x, y), (x + 4.3, y), (x + 4.8, y + 0.6), (x + 0.5, y + 0.6)], closed=True,
                                 fc="white", ec=RED, lw=1.5, ls="--"))
            label(ax, x + 2.4, y + 0.3, "지웠어요", fs=10, color=RED, bold=True)
        else:
            film(ax, x, y, 4.3, "", [(c, s) for c, s in chips], hot=bool(hot), hot_chips=hot)
        label(ax, x + 2.4, y + 1.05, f"{name} 쓰기 층", fs=10, color=RED if (k == 0 and gone1) else "#222", bold=True)
        ax.plot([x + 2.4, 5.9 + (k - 0.5) * 1.2], [y - 0.05, 2.95], color=GREY, lw=1.2, ls=":")


def cow(ax, step):
    if step == 1:
        cow_stage(ax)
        label(ax, 6.0, 0.15, "처음 쓰기 층은 둘 다 비어 있어요", fs=10.5, color=INK)
    elif step == 2:
        cow_stage(ax, top1=[(1.75, "설정 파일")], hot1=(0,), base_hot=True)
        ax.annotate("", xy=(2.9, 3.85), xytext=(5.0, 1.05),
                    arrowprops=dict(arrowstyle="-|>", color=RED, lw=1.8, connectionstyle="arc3,rad=-0.3"))
        label(ax, 6.0, 0.15, "① 설정 파일을 컨테이너 1의 쓰기 층으로 복사  ② 복사본을 고쳐요", fs=10.5, color=RED, bold=True)
    elif step == 3:
        cow_stage(ax, top1=[(1.75, "설정 파일*")], hot1=(0,))
        label(ax, 3.2, 5.2, "컨테이너 1은 고친 설정 파일을 봐요", fs=9.5, color=RED)
        label(ax, 8.8, 5.2, "컨테이너 2는 원래 설정 파일을 봐요", fs=9.5, color=INK)
        moral(ax, 6.0, 0.15, "고친 것은 그 컨테이너의 맨 위 층에만 있어요")


# ── 컨테이너를 지우면 ─────────────────────────────────────────────
def remove(ax, step):
    if step == 1:
        cow_stage(ax, top1=[(1.75, "설정 파일*")], gone1=True)
        moral(ax, 6.0, 0.15, "컨테이너를 지우면 그 쓰기 층도 함께 사라져요")
    else:
        building(ax, 0.4, 0.8, 6.6, 3.8, ["주문 화면", "주문 처리", "주문 장부"], room_hot=(2,), fs=9.5)
        cyl_x = 8.6
        box(ax, cyl_x, 1.2, 3.0, 2.2, fc=PINK, ec=RED)
        label(ax, cyl_x + 1.5, 2.6, "따로 붙인 디스크", fs=10.5, color=RED, bold=True)
        cell(ax, cyl_x + 0.4, 1.55, 2.2, 0.5, "주문 장부 파일", hot=True, fs=9.5)
        arrow(ax, (5.9, 2.7), (cyl_x - 0.1, 2.3), color=RED, ms=14)
        label(ax, 9.4, 4.1, "컨테이너가 없어져도\n남아야 하는 것은 여기에", fs=10, color=RED)
        moral(ax, 6.0, 0.2, "남겨야 할 데이터는 쓰기 층 말고 따로 붙인 디스크에 (11편)")


# ── 판단 (한 장) ──────────────────────────────────────────────────
def decide():
    fig, ax = canvas(10, 4.2, 15, 6.4)
    box(ax, 0.3, 4.6, 6.2, 1.3, fc=NOTE)
    label(ax, 3.4, 5.25, "컨테이너가 쓴 데이터를\n컨테이너를 지운 뒤에도 남기나요?", fs=10.5, bold=True)
    arrow(ax, (6.6, 5.25), (8.4, 5.25)); label(ax, 7.5, 5.55, "예", fs=10, color=INK)
    box(ax, 8.5, 4.6, 6.2, 1.3, fc=PAPER)
    label(ax, 11.6, 5.25, "쓰기 층 말고\n따로 붙인 디스크에 (11편)", fs=10.5)
    arrow(ax, (3.4, 4.5), (3.4, 3.5)); label(ax, 3.7, 4.0, "아니요", fs=10, color=INK, ha="left")
    box(ax, 0.3, 2.1, 6.2, 1.3, fc=NOTE)
    label(ax, 3.4, 2.75, "이미지 여럿이 같은 바탕을 쓰거나\n코드만 자주 바꾸나요?", fs=10.5, bold=True)
    arrow(ax, (6.6, 2.75), (8.4, 2.75)); label(ax, 7.5, 3.05, "아니요", fs=10, color=INK)
    box(ax, 8.5, 2.1, 6.2, 1.3, fc=PAPER)
    label(ax, 11.6, 2.75, "층 순서를 크게 신경 쓰지 않아도 돼요", fs=10.5)
    arrow(ax, (3.4, 2.0), (3.4, 1.3), color=RED); label(ax, 3.7, 1.65, "예", fs=10, color=RED, ha="left")
    box(ax, 0.3, 0.1, 6.2, 1.1, fc=PINK, ec=RED)
    label(ax, 3.4, 0.65, "같은 바탕 층에서 시작하고\n자주 바뀌는 코드는 맨 위 층에", fs=10.5, color=RED, bold=True)
    save(fig, OUT, "k8s02-decide.svg")


# ── 정리: 처음 장면으로 돌아가기 ───────────────────────────────────
def back(ax, step):
    first = [(*BASE, "다 받았어요"), (*RUN, "다 받았어요"), (*WEB, "다 받았어요")]
    second = [(*BASE, "이미 있어요"), (*RUN, "이미 있어요"), (*APP, "받는 중")]
    pull_win(ax, 0.3, 3.6, "주문 화면 이미지 받기", first, hot=(0, 1) if step == 2 else ())
    pull_win(ax, 6.1, 0.7, "주문 처리 이미지 받기", second, hot=(0, 1) if step == 2 else ())
    if step == 1:
        label(ax, 3.1, 2.4, "처음엔 이미 있다는 말이\n무슨 뜻인지 몰랐어요", fs=11, color=INK)
    else:
        label(ax, 3.1, 2.4, "같은 지문 = 같은 층\n이미 저장한 층이에요", fs=11, color=RED, bold=True)
        moral(ax, 6.0, 0.25, "같은 층은 한 번만 받고, 고친 것은 맨 위 층에만 써요")


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

    x, y = card(0, "이미지", "컨테이너를 만드는 틀\n(층 목록 + 실행 방법)")
    box(ax, x + 1.0, y + 1.3, 2.6, 1.6, fc=PINK, ec=RED)
    for k, s in enumerate(["a3f", "7c2", "4b8"]):
        cell(ax, x + 1.4, y + 2.35 - k * 0.45, 1.8, 0.38, s, fs=9)
    x, y = card(1, "레이어", "아래 층에서 바뀐 파일만\n담은 층 하나")
    film(ax, x + 0.5, y + 1.5, 3.0, "", [(1.0, "실행기")], hot=True)
    x, y = card(2, "겹쳐 쓰는 파일시스템", "층을 겹쳐 하나의\n파일 나무로 보여 주는 방법")
    for k in range(3):
        film(ax, x + 0.5, y + 1.25 + k * 0.5, 2.6, "", [], hot=(k == 2), skew=0.4)
    x, y = card(3, "다이제스트", "층 내용으로 계산한 지문\n내용이 같으면 지문도 같아요")
    cell(ax, x + 0.5, y + 1.7, 1.5, 0.6, "a3f", fs=11)
    label(ax, x + 2.3, y + 2.0, "=", fs=14, color=RED, bold=True)
    cell(ax, x + 2.6, y + 1.7, 1.5, 0.6, "a3f", hot=True, fs=11)
    x, y = card(4, "쓰기 층", "컨테이너마다 맨 위에 얹는\n얇은 층, 지우면 함께 사라져요")
    film(ax, x + 0.5, y + 2.0, 3.0, "", [(1.0, "설정 파일*")], hot=True)
    film(ax, x + 0.5, y + 1.3, 3.0, "", [], dim=True)
    x, y = card(5, "쓸 때 복사", "고칠 때 처음 그 파일을\n맨 위 층으로 복사해서 고치기")
    cell(ax, x + 0.5, y + 1.4, 1.6, 0.5, "설정 파일", fs=9.5)
    arrow(ax, (x + 2.2, y + 1.65), (x + 2.6, y + 2.3), color=RED, ms=11)
    cell(ax, x + 2.5, y + 2.3, 1.7, 0.5, "설정 파일*", hot=True, fs=9.5)
    save(fig, OUT, "k8s02-cards.svg")


if __name__ == "__main__":
    S, L = (7.2, 3.8), (12, 6.6)
    stage(opening, 3, OUT, "k8s02-open", S, L)
    stage(image, 2, OUT, "k8s02-image", S, L)
    stage(whole, 2, OUT, "k8s02-whole", S, L)
    stage(films, 4, OUT, "k8s02-film", S, L)
    stage(share, 3, OUT, "k8s02-share", S, L)
    stage(cow, 3, OUT, "k8s02-cow", S, L)
    stage(remove, 2, OUT, "k8s02-remove", S, L)
    decide()
    stage(back, 2, OUT, "k8s02-back", S, L)
    cards()
