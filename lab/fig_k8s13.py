"""쿠버네티스 13편 그림 만들기. 실행: python lab/fig_k8s13.py  → docs/kubernetes/img/13/*.svg

본문 절은 장면 띠로 그린다: 같은 무대를 여러 장 그리고 장마다 바뀐 곳만 빨강으로 칠한다.
예시는 빵집 주문 앱의 주문 장부 디스크. 블록 8칸, 블록 1~5에 주문 1~5, 6~8은 빈칸.
오후 3시에 스냅샷을 찍고, 그 뒤 주문 6이 들어오고 주문 3이 엉망으로 덮어써진다.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "es"))
from figkit import (GREY, INK, LIGHT, NOTE, PAPER, PINK, RED, arrow, box, bubble,  # noqa: E402
                    canvas, cell, cylinder, label, moral, outdir, save, stage)
from matplotlib.patches import Rectangle  # noqa: E402

OUT = outdir("13", topic="kubernetes")
FILM = "#eaf2fb"
BASE = ["주문 1", "주문 2", "주문 3", "주문 4", "주문 5", "", "", ""]
X0, W, GAP = 2.6, 1.0, 0.1


def bx(i):
    return X0 + i * (W + GAP)


def row(ax, y, items, name, hot=(), dim=(), film=False, name_hot=False, nums=False, h=0.75):
    """블록 8칸 한 줄. film=투명 필름 층(빈칸은 점선)."""
    c = RED if name_hot else INK
    label(ax, 0.2, y + h / 2, name, fs=10, ha="left", color=c, bold=name_hot)
    for i, s in enumerate(items):
        x = bx(i)
        if nums:
            label(ax, x + W / 2, y + h + 0.25, str(i + 1), fs=9, color=INK)
        if film and not s:
            ax.add_patch(Rectangle((x, y), W, h, fc=FILM, ec=RED if i in hot else GREY, lw=1.0, ls="--"))
        elif not s:
            ax.add_patch(Rectangle((x, y), W, h, fc="white", ec=GREY if i in dim else INK, lw=1.0))
        else:
            cell(ax, x, y, W, h, s, hot=i in hot, dim=i in dim, fs=9.5,
                 fc=(PINK if i in hot else (FILM if film else None)))


def film_frame(ax, y, hot=False, h=0.75):
    ax.add_patch(Rectangle((X0 - 0.12, y - 0.12), 8 * (W + GAP) - GAP + 0.24, h + 0.24,
                           fill=False, ec=RED if hot else "#7da2c8", lw=2.0 if hot else 1.3, ls="--"))


# ── 여는 장면: 관리 화면의 스냅샷 찍기 ─────────────────────────────
def screen(ax, pressed=False, done_hot=False, done=False, grey_done=False, list2=False):
    box(ax, 0.4, 0.75, 7.4, 5.6, fc="white", round_=False)
    ax.add_patch(Rectangle((0.4, 5.9), 7.4, 0.45, fc=LIGHT, ec=INK, lw=1.2))
    label(ax, 0.6, 6.12, "빵집 앱 관리 화면", fs=11, ha="left", color=INK)
    box(ax, 0.8, 4.3, 6.6, 1.25, fc=NOTE)
    label(ax, 1.0, 5.15, "주문 장부 디스크", fs=12, ha="left", bold=True)
    ax.add_patch(Rectangle((1.0, 4.5), 2.5, 0.35, fc=LIGHT, ec=INK, lw=1.0))
    ax.add_patch(Rectangle((1.0, 4.5), 2.3, 0.35, fc="#9aa3ad", ec="none"))
    label(ax, 3.65, 4.67, "거의 가득", fs=10, ha="left", color=INK)
    hot = pressed
    ax.add_patch(Rectangle((5.3, 4.55), 1.9, 0.6, fc=PINK if hot else LIGHT, ec=RED if hot else INK, lw=1.8 if hot else 1.2))
    label(ax, 6.25, 4.85, "스냅샷 찍기", fs=10.5, color=RED if hot else "#222", bold=hot)
    label(ax, 0.9, 3.75, "찍어 둔 스냅샷", fs=10.5, ha="left", color=INK)
    ax.plot([0.9, 7.3], [3.5, 3.5], color=INK, lw=1.0)
    if done:
        c = RED if done_hot else (GREY if grey_done else "#222")
        if done_hot:
            ax.add_patch(Rectangle((0.9, 2.7), 6.4, 0.55, fc=PINK, ec=RED, lw=1.6))
        label(ax, 1.1, 2.97, "오후 3:00", fs=11, ha="left", color=c, bold=done_hot)
        label(ax, 7.1, 2.97, "완료 ✓", fs=11, ha="right", color=c, bold=done_hot)
    if list2:
        ax.add_patch(Rectangle((0.9, 2.05), 6.4, 0.55, fc=PINK, ec=RED, lw=1.6))
        label(ax, 1.1, 2.32, "다음 날 오후 3:00", fs=11, ha="left", color=RED, bold=True)
        label(ax, 7.1, 2.32, "완료 ✓", fs=11, ha="right", color=RED, bold=True)


def opening(ax, step):
    if step == 1:
        screen(ax, pressed=True)
        bubble(ax, 8.2, 3.6, 3.6, 1.4, "가격표를 바꾸기 전에\n지금 모습을 찍어 둬요", (7.3, 4.85), hot=True, fs=10.5)
    else:
        screen(ax, done=True, done_hot=True)
        bubble(ax, 8.2, 3.6, 3.6, 1.4, "누르자마자\n완료가 떴어요", (7.3, 3.0), hot=True, fs=10.5)
        moral(ax, 4.1, 0.25, "디스크는 거의 가득 찼는데 찍기는 눈 깜짝할 새 끝나요")


# ── 디스크는 블록으로 나뉘어 있어요 ─────────────────────────────────
def blocks(ax, step):
    if step == 1:
        cylinder(ax, 1.0, 1.8, 2.6, 2.6, "주문 장부")
        box(ax, 5.2, 2.0, 5.8, 2.6, fc=NOTE)
        label(ax, 8.1, 3.3, "주문 장부 디스크", fs=13, bold=True)
        arrow(ax, (3.8, 3.1), (5.1, 3.1), ms=14)
        label(ax, 4.45, 3.45, "적어요", fs=10, color=INK)
        ax.add_patch(Rectangle((5.0, 1.8), 6.2, 3.0, fill=False, ec=RED, lw=2.0, ls="--"))
        label(ax, 8.1, 1.35, "안을 들여다보면?", fs=11, color=RED, bold=True)
    else:
        label(ax, 6.9, 5.7, "주문 장부 디스크", fs=12, bold=True)
        row(ax, 3.6, BASE, "블록 번호", nums=True, hot=range(8))
        label(ax, 6.9, 2.6, "크기가 같은 칸이 번호 순서로 줄지어 있어요", fs=10.5, color=INK)
        moral(ax, 6.0, 1.2, "디스크는 블록 칸에 나눠 담아요")


# ── 다 복사하면 오래 걸려요 ─────────────────────────────────────────
def copy(ax, step):
    row(ax, 4.4, BASE, "디스크", nums=True)
    label(ax, 0.2, 2.15, "복사본", fs=10, ha="left", color=INK)
    n = 3 if step == 1 else 8
    for i in range(8):
        x = bx(i)
        if i < n:
            cell(ax, x, 1.8, W, 0.75, BASE[i] or "빈칸", hot=(step == 1 and i == n - 1) or step == 2, fs=9.5)
        else:
            ax.add_patch(Rectangle((x, 1.8), W, 0.75, fc="white", ec=GREY, lw=1.0, ls="--"))
    i = n - 1 if step == 1 else 7
    arrow(ax, (bx(i) + W / 2, 4.32), (bx(i) + W / 2, 2.62), color=RED, ms=13)
    if step == 1:
        label(ax, 6.9, 3.4, "한 칸씩 옮겨 적는 중 · 아직 다섯 칸 남았어요", fs=10.5, color=RED)
    else:
        label(ax, 6.9, 3.4, "여덟 칸을 다 옮겨 적었어요", fs=10.5, color=RED)
        moral(ax, 6.0, 0.8, "다 복사하면 디스크가 클수록 오래 걸려요")


# ── 투명 필름 한 장 ─────────────────────────────────────────────────
def film(ax, step):
    if step == 1:
        row(ax, 2.3, BASE, "지금 디스크", nums=True)
        label(ax, 6.9, 4.6, "오후 3시, 스냅샷 찍기를 눌렀어요", fs=11, color=INK)
    else:
        row(ax, 2.3, BASE, "오후 3시 층", name_hot=(step == 2), nums=True)
        ax.add_patch(Rectangle((X0 - 0.12, 2.18), 8 * (W + GAP) - GAP + 0.24, 0.99,
                               fill=False, ec=RED if step == 2 else INK, lw=2.0 if step == 2 else 1.2))
        label(ax, bx(7) + W / 2, 1.85, "잠금", fs=10, color=RED if step == 2 else INK, bold=(step == 2))
        if step == 2:
            label(ax, 6.9, 1.35, "지금까지 쓴 칸은 그대로 두고 더는 고치지 않아요", fs=10.5, color=RED)
    if step == 3:
        row(ax, 4.4, [""] * 8, "새 필름", film=True, name_hot=True, hot=range(8))
        film_frame(ax, 4.4, hot=True)
        label(ax, 6.9, 5.6, "그 위에 빈 투명 필름을 한 장 덮어요", fs=10.5, color=RED)
        moral(ax, 6.0, 1.0, "빈 필름 한 장만 덮으니 찍기는 순식간이에요")


# ── 찍은 뒤의 쓰기와 읽기 ───────────────────────────────────────────
def write(ax, step):
    top = [""] * 8
    hot = ()
    if step >= 1:
        top[5] = "주문 6"
    if step >= 2:
        top[2] = "엉망"
    if step == 1:
        hot = (5,)
    elif step == 2:
        hot = (2,)
    row(ax, 4.2, top, "새 필름", film=True, hot=hot, nums=True)
    film_frame(ax, 4.2)
    row(ax, 2.3, BASE, "오후 3시 층", dim=(2,) if step >= 2 else ())
    ax.add_patch(Rectangle((X0 - 0.12, 2.18), 8 * (W + GAP) - GAP + 0.24, 0.99, fill=False, ec=INK, lw=1.2))
    if step == 1:
        label(ax, 6.9, 1.4, "새 주문 6은 새 필름의 블록 6에 써요", fs=10.5, color=RED)
    elif step == 2:
        label(ax, 6.9, 1.4, "블록 3을 고쳐 써도 아래층 주문 3은 그대로예요", fs=10.5, color=RED)
    else:
        for i, c in ((0, RED), (2, RED)):
            x = bx(i) + W / 2
            ax.annotate("", xy=(x, 4.97) if i == 2 else (x, 3.07), xytext=(x, 5.85),
                        arrowprops=dict(arrowstyle="-|>", color=c, lw=1.8, mutation_scale=13))
        label(ax, bx(0) + W / 2, 6.1, "블록 1 읽기", fs=9.5, color=RED)
        label(ax, bx(2) + W / 2 + 0.4, 6.1, "블록 3 읽기", fs=9.5, color=RED)
        label(ax, bx(0) + W / 2 + 0.12, 3.6, "비었으니 아래로", fs=9, color=RED, ha="left")
        moral(ax, 6.0, 1.1, "위층에 있으면 위층을, 없으면 아래층을 읽어요")


# ── 되돌리기 ───────────────────────────────────────────────────────
def revert(ax, step):
    top = [""] * 8
    top[2], top[5] = "엉망", "주문 6"
    app_hot = step == 1
    box(ax, 0.2, 5.55, 2.6, 0.75, fc=PINK if app_hot else (LIGHT if step > 1 else NOTE), ec=RED if app_hot else INK)
    label(ax, 1.5, 5.92, "주문 처리 멈춤" if step >= 1 else "주문 처리", fs=10.5, color=RED if app_hot else INK, bold=app_hot)
    if step == 1:
        label(ax, 3.0, 5.92, "되돌리는 동안 디스크를 아무도 쓰지 않아요", fs=10.5, ha="left", color=RED)
    if step < 3:
        hot = range(8) if step == 2 else ()
        row(ax, 3.9, top, "새 필름", film=True, hot=hot)
        film_frame(ax, 3.9, hot=(step == 2))
        if step == 2:
            ax.plot([X0 - 0.1, bx(7) + W + 0.1], [3.8, 4.75], color=RED, lw=2.2)
            label(ax, 6.9, 5.1, "새 필름을 통째로 떼어 내요", fs=10.5, color=RED, bold=True)
    else:
        ax.add_patch(Rectangle((X0 - 0.12, 3.78), 8 * (W + GAP) - GAP + 0.24, 0.99, fc="white", ec=GREY, lw=1.0, ls=":"))
        label(ax, 6.9, 4.27, "떼어 낸 자리", fs=10, color=GREY)
    row(ax, 2.0, BASE, "오후 3시 층", hot=range(5) if step == 3 else ())
    if step == 3:
        label(ax, 6.9, 1.2, "주문 3은 돌아오고, 찍은 뒤 들어온 주문 6은 사라져요", fs=10.5, color=RED)
        moral(ax, 6.0, 0.35, "되돌리기는 찍은 뒤에 덮은 층을 떼어 내는 일이에요")


# ── 스냅샷과 백업 ───────────────────────────────────────────────────
def backup(ax, step):
    box(ax, 0.3, 1.4, 6.6, 4.4, fc="white")
    label(ax, 0.5, 5.45, "디스크", fs=11, ha="left", bold=True)
    cell(ax, 0.8, 3.6, 5.6, 0.8, "새 필름", fc=FILM, fs=10.5)
    cell(ax, 0.8, 2.3, 5.6, 0.8, "오후 3시 층 (스냅샷)", fs=10.5)
    box(ax, 8.2, 1.4, 3.5, 4.4, fc=PAPER, ec=RED if step == 2 else INK)
    label(ax, 9.95, 5.45, "다른 곳의 보관소", fs=10.5, color=RED if step == 2 else INK, bold=(step == 2))
    if step == 1:
        ax.plot([0.5, 6.7], [1.6, 5.6], color=RED, lw=2.5)
        ax.plot([0.5, 6.7], [5.6, 1.6], color=RED, lw=2.5)
        label(ax, 3.6, 0.95, "디스크가 고장 나면 스냅샷도 함께 사라져요", fs=10.5, color=RED, bold=True)
        label(ax, 9.95, 3.5, "비어 있어요", fs=10.5, color=GREY)
    else:
        arrow(ax, (6.5, 2.7), (8.6, 2.7), color=RED, ms=14)
        label(ax, 7.55, 3.05, "복사", fs=10.5, color=RED, bold=True)
        cell(ax, 8.6, 2.3, 2.75, 0.8, "오후 3시 백업", hot=True, fs=10.5)
        moral(ax, 6.0, 0.6, "백업은 스냅샷을 다른 곳에 복사해 둔 것이에요")


# ── 저장소 두 개를 같은 순간으로 ────────────────────────────────────
def orders(ax, x, y, n, hot=(), ghost=False, title="", title_hot=False):
    label(ax, x + 1.6, y + 2.25, title, fs=10.5, color=RED if title_hot else INK, bold=title_hot)
    for k in range(6):
        yy = y + 1.55 - k * 0.32
        if k < n:
            on = (k + 1) in hot
            c = RED if on else "#222"
            label(ax, x + 0.3, yy, f"주문 {k + 1}" + (" ← 장부엔 없어요" if ghost and on else ""), fs=9.5, ha="left",
                  color=c, bold=on)


def pair(ax, step):
    cylinder(ax, 0.6, 3.7, 2.2, 1.3, "주문 장부")
    cylinder(ax, 7.4, 3.7, 2.2, 1.3, "주문 검색 저장소")
    arrow(ax, (3.0, 4.35), (7.2, 4.35), ms=14)
    label(ax, 5.1, 4.65, "바뀐 주문을 보내요", fs=10, color=INK)
    wrong = step <= 2
    if step in (1, 3):
        s = ("① 장부 찍기 → 주문 6이 장부와 검색에 들어옴 → ② 검색 찍기" if wrong
             else "① 검색 찍기 → 주문 6이 장부와 검색에 들어옴 → ② 장부 찍기")
        label(ax, 6.0, 3.2, s, fs=10, color=RED, bold=True)
        led_n, sea_n = (5, 6) if wrong else (6, 5)
        orders(ax, 0.4, 0.3, led_n, title="① 장부 사진" if wrong else "② 장부 사진")
        orders(ax, 7.2, 0.3, sea_n, title="② 검색 사진" if wrong else "① 검색 사진")
    elif step == 2:
        label(ax, 6.0, 3.2, "두 사진으로 되돌리면", fs=10.5, color=INK)
        orders(ax, 0.4, 0.3, 5, title="장부")
        orders(ax, 7.2, 0.3, 6, hot=(6,), ghost=True, title="검색 저장소", title_hot=True)
        moral(ax, 6.0, -0.25, "장부를 먼저 찍으면 검색이 장부보다 앞서 나가요")
    else:
        label(ax, 6.0, 3.2, "두 사진으로 되돌리면", fs=10.5, color=INK)
        orders(ax, 0.4, 0.3, 6, title="장부")
        orders(ax, 7.2, 0.3, 6, hot=(6,), title="검색 저장소", title_hot=True)
        arrow(ax, (3.0, 0.15), (7.3, 0.15), color=RED, ms=13, rad=0.0)
        label(ax, 5.15, 0.45, "주문 6을 다시 받아 따라잡아요", fs=10, color=RED, bold=True)
        moral(ax, 6.0, -0.45, "뒤쪽부터 찍으면 따라잡기만 하면 돼요")


# ── 판단 (한 장) ───────────────────────────────────────────────────
def decide():
    fig, ax = canvas(10, 5.4, 15, 8.4)
    ax.set_ylim(-0.3, 8.4)
    box(ax, 0.3, 6.7, 6.4, 1.2, fc=NOTE)
    label(ax, 3.5, 7.3, "곧 위험한 작업을 하나요?", fs=10.5, bold=True)
    arrow(ax, (6.8, 7.3), (8.4, 7.3)); label(ax, 7.6, 7.6, "예", fs=10, color=INK)
    box(ax, 8.5, 6.7, 6.2, 1.2, fc=PAPER)
    label(ax, 11.6, 7.3, "직전에 스냅샷을 찍어 둬요", fs=10.5)
    arrow(ax, (3.5, 6.6), (3.5, 5.6)); label(ax, 3.8, 6.1, "아니요", fs=10, color=INK, ha="left")
    box(ax, 0.3, 4.3, 6.4, 1.2, fc=NOTE)
    label(ax, 3.5, 4.9, "디스크 고장에 대비하나요?", fs=10.5, bold=True)
    arrow(ax, (6.8, 4.9), (8.4, 4.9)); label(ax, 7.6, 5.2, "예", fs=10, color=INK)
    box(ax, 8.5, 4.3, 6.2, 1.2, fc=PAPER)
    label(ax, 11.6, 4.9, "백업으로 다른 곳에 복사해요", fs=10.5)
    arrow(ax, (3.5, 4.2), (3.5, 3.2)); label(ax, 3.8, 3.7, "아니요", fs=10, color=INK, ha="left")
    box(ax, 0.3, 1.9, 6.4, 1.2, fc=NOTE)
    label(ax, 3.5, 2.5, "저장소 여럿을 같이 되돌려야 하나요?", fs=10.5, bold=True)
    arrow(ax, (6.8, 2.5), (8.4, 2.5), color=RED); label(ax, 7.6, 2.8, "예", fs=10, color=RED)
    box(ax, 8.5, 1.9, 6.2, 1.2, fc=PINK, ec=RED)
    label(ax, 11.6, 2.5, "받아 쓰는 뒤쪽부터 찍어요", fs=10.5, color=RED, bold=True)
    arrow(ax, (3.5, 1.8), (3.5, 0.9)); label(ax, 3.8, 1.35, "아니요", fs=10, color=INK, ha="left")
    box(ax, 0.3, 0.0, 6.4, 0.8, fc=PAPER)
    label(ax, 3.5, 0.4, "스냅샷이 없어도 돼요", fs=10.5)
    save(fig, OUT, "k8s13-decide.svg")


# ── 정리: 처음 장면으로 돌아가기 ───────────────────────────────────
def back(ax, step):
    if step == 1:
        screen(ax, done=True, grey_done=True)
        bubble(ax, 8.2, 3.6, 3.6, 1.4, "처음엔 왜 이렇게\n빠른지 몰랐어요", (7.3, 3.0), fs=10.5)
    elif step == 2:
        screen(ax, pressed=True, done=True, grey_done=True)
        bubble(ax, 8.2, 3.6, 3.6, 1.4, "다음 날도\n찍기를 눌러요", (7.3, 4.85), hot=True, fs=10.5)
    else:
        screen(ax, done=True, grey_done=True, list2=True)
        bubble(ax, 8.2, 3.3, 3.6, 1.7, "블록을 복사하지 않고\n빈 필름만 한 장\n더 덮었어요", (7.3, 2.35), hot=True, fs=10.5)
        moral(ax, 4.1, 0.25, "디스크가 얼마나 크든 빈 필름 한 장이면 끝나요")


# ── 정리: 낱말 카드 ────────────────────────────────────────────────
def cards():
    fig, ax = canvas(6.4, 5.4, 9.8, 8.35)
    W_, H_ = 4.6, 3.8

    def card(i, name, line):
        col, row_ = i % 2, i // 2
        x, y = 0.2 + col * 4.9, 4.35 - row_ * 4.05
        box(ax, x, y, W_, H_, fc="white")
        label(ax, x + 0.25, y + H_ - 0.4, name, fs=12.5, ha="left", bold=True)
        label(ax, x + W_ / 2, y + 0.6, line, fs=10, color=INK)
        return x, y

    x, y = card(0, "블록", "디스크를 같은 크기로 나눈\n번호 붙은 칸")
    for i in range(5):
        cell(ax, x + 0.35 + i * 0.8, y + 1.65, 0.7, 0.7, str(i + 1), hot=(i == 2), fs=10.5)
    x, y = card(1, "스냅샷", "찍은 순간의 층을 잠그고\n빈 필름을 덮어 남긴 모습")
    ax.add_patch(Rectangle((x + 0.5, y + 2.15), 3.6, 0.5, fc=FILM, ec=RED, lw=1.6, ls="--"))
    cell(ax, x + 0.5, y + 1.45, 3.6, 0.55, "오후 3시 층", fs=10)
    x, y = card(2, "되돌리기", "찍은 뒤 덮은 층을\n떼어 내는 일")
    ax.add_patch(Rectangle((x + 0.5, y + 2.15), 3.6, 0.5, fc=FILM, ec=GREY, lw=1.2, ls="--"))
    ax.plot([x + 0.5, x + 4.1], [y + 2.15, y + 2.65], color=RED, lw=2.0)
    cell(ax, x + 0.5, y + 1.45, 3.6, 0.55, "오후 3시 층", hot=True, fs=10)
    x, y = card(3, "백업", "스냅샷을 다른 곳에\n복사해 둔 것")
    cell(ax, x + 0.4, y + 1.6, 1.6, 0.8, "스냅샷", fs=10)
    arrow(ax, (x + 2.1, y + 2.0), (x + 2.6, y + 2.0), color=RED, ms=11)
    cell(ax, x + 2.7, y + 1.6, 1.5, 0.8, "보관소", hot=True, fs=10)
    save(fig, OUT, "k8s13-cards.svg")


def fixed(draw):
    """장마다 그림 크기가 같도록 무대 테두리를 흰색으로 그린다."""
    def f(ax, step):
        ax.add_patch(Rectangle((0, -0.6), 12, 7.2, fill=False, ec="white", lw=0.5))
        draw(ax, step)
    return f


if __name__ == "__main__":
    S, L = (7.2, 3.8), (12, 6.6)
    stage(fixed(opening), 2, OUT, "k8s13-open", S, L)
    stage(fixed(blocks), 2, OUT, "k8s13-block", S, L)
    stage(fixed(copy), 2, OUT, "k8s13-copy", S, L)
    stage(fixed(film), 3, OUT, "k8s13-film", S, L)
    stage(fixed(write), 3, OUT, "k8s13-write", S, L)
    stage(fixed(revert), 3, OUT, "k8s13-revert", S, L)
    stage(fixed(backup), 2, OUT, "k8s13-backup", S, L)
    stage(fixed(pair), 4, OUT, "k8s13-order", S, (12, 6.6))
    decide()
    stage(fixed(back), 3, OUT, "k8s13-back", S, L)
    cards()
