"""쿠버네티스 3편 그림 만들기. 실행: python lab/fig_k8s03.py  → docs/kubernetes/img/03/*.svg

대표 비유는 사물함 번호표. 파일 = 사물함, 문 위 번호표 = 주인 번호(UID)·그룹 번호(GID),
프로세스 = 번호를 든 프로그램, 명부 = 번호를 이름으로 바꿔 보여 주는 표(칸마다 따로).
예시는 빵집 주문 앱의 주문 장부. 장부 프로그램은 999번(칸 안 명부 이름 장부지기), 붙인 디스크는 처음에 0번 root 것.
쿠버네티스 설정은 runAsUser 999, runAsGroup 999, fsGroup 2000.
그림 안 글씨는 낱말과 숫자만 둔다. 문장은 본문과 그림 설명에 둔다(쉬운글-정책 5장).
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "es"))
from figkit import (INK, NOTE, PAPER, PINK, RED, arrow, box, canvas, cell,  # noqa: E402
                    label, outdir, save)
from fig_k8s01 import building, window  # noqa: E402
from matplotlib.patches import Circle, Rectangle  # noqa: E402

OUT = outdir("03", topic="kubernetes")


def make(draw, name, y0, y1):
    """가로 0~12, 세로 y0~y1 만 남겨 그린다. 그림마다 글씨 크기가 같게 가로 폭을 고정한다."""
    fig, ax = canvas(7.2, 0.6 * (y1 - y0), 12, y1)
    ax.set_ylim(y0, y1)
    ax.add_patch(Rectangle((0, y0), 12, y1 - y0, fill=False, ec="none"))
    draw(ax)
    save(fig, OUT, name)


# ── 재료 ───────────────────────────────────────────────────────────
def locker(ax, x, y, name, owner, group, hot=False, plate_hot=False, w=2.6, h=2.4, fs=10):
    """사물함 하나(= 파일·폴더). 위에 번호표, 가운데 이름."""
    ec = RED if hot else INK
    ax.add_patch(Rectangle((x, y), w, h, fc=PINK if hot else NOTE, ec=ec, lw=2.0 if hot else 1.5))
    ax.add_patch(Circle((x + w - 0.3, y + h * 0.4), 0.08, fc=ec, ec="none"))
    pc = RED if plate_hot else INK
    ax.add_patch(Rectangle((x + 0.2, y + h - 1.0), w - 0.4, 0.82, fc=PINK if plate_hot else "white", ec=pc,
                           lw=1.8 if plate_hot else 1.2))
    label(ax, x + w / 2, y + h - 0.59, f"주인 {owner}\n그룹 {group}", fs=fs - 0.5, color=pc, bold=plate_hot)
    label(ax, x + w / 2, y + (h - 1.0) / 2, name, fs=fs, color=RED if hot else "#222", bold=hot)


def person(ax, x, y, name, num, groups=None, hot=False, w=2.8):
    """프로세스. 이름 칸과 번호 칸."""
    ec = RED if hot else INK
    box(ax, x, y, w, 1.25 if groups else 0.95, fc=PINK if hot else PAPER, ec=ec)
    c = RED if hot else "#222"
    top = y + (0.95 if groups else 0.65)
    label(ax, x + w / 2, top, name, fs=10, color=c, bold=hot)
    label(ax, x + w / 2, top - 0.38, f"번호 {num}", fs=10, color=c)
    if groups:
        label(ax, x + w / 2, top - 0.72, f"그룹 {groups}", fs=9.5, color=c)


def namebook(ax, x, y, title, entries, hot=(), w=2.9):
    """명부: 번호 → 이름."""
    box(ax, x, y, w, 0.5 + 0.45 * len(entries), fc="white")
    label(ax, x + w / 2, y + 0.25 + 0.45 * len(entries), title, fs=9.5, color=INK, bold=True)
    for k, (n, s) in enumerate(entries):
        yy = y + 0.05 + 0.45 * (len(entries) - 1 - k)
        on = k in hot
        cell(ax, x + 0.15, yy, 0.9, 0.4, n, hot=on, fs=9.5)
        cell(ax, x + 1.1, yy, w - 1.25, 0.4, s, hot=on, fs=9.5)


def perms(ax, x, y, rows_, hot=()):
    """권한 표: [(누구, 읽기, 쓰기)]."""
    label(ax, x, y + 0.4, "누구", fs=9, ha="left", color=INK)
    label(ax, x + 1.7, y + 0.4, "읽기", fs=9, color=INK)
    label(ax, x + 2.4, y + 0.4, "쓰기", fs=9, color=INK)
    for k, (who, r, wr) in enumerate(rows_):
        yy = y - 0.42 * k
        on = k in hot
        if on:
            ax.add_patch(Rectangle((x - 0.1, yy - 0.19), 2.8, 0.38, fc=PINK, ec=RED, lw=1.3))
        c = RED if on else "#222"
        label(ax, x, yy, who, fs=9.5, ha="left", color=c, bold=on)
        label(ax, x + 1.7, yy, "O" if r else "X", fs=9.5, color=c)
        label(ax, x + 2.4, yy, "O" if wr else "X", fs=9.5, color=c, bold=on)


def log(ax, lines, hot=()):
    window(ax, 0.3, 0.3, 6.4, 2.8, "주문 장부 컨테이너 기록")
    for k, s in enumerate(lines):
        yy = 2.2 - k * 0.55
        on = k in hot
        if on:
            ax.add_patch(Rectangle((0.4, yy - 0.23), 6.2, 0.46, fc=PINK, ec=RED, lw=1.5))
        label(ax, 0.6, yy, s, fs=10.5, ha="left", color=RED if on else "#222", bold=on)


def ls_win(ax, rows_, hot=(), x=7.1, y=0.3):
    window(ax, x, y, 4.6, 2.8, "/data 안")
    label(ax, x + 0.2, y + 1.95, "이름", fs=9.5, ha="left", color=INK)
    label(ax, x + 1.8, y + 1.95, "주인", fs=9.5, ha="left", color=INK)
    label(ax, x + 3.2, y + 1.95, "그룹", fs=9.5, ha="left", color=INK)
    ax.plot([x + 0.15, x + 4.45], [y + 1.73, y + 1.73], color=INK, lw=0.8)
    for k, (a, b, c) in enumerate(rows_):
        yy = y + 1.35 - k * 0.5
        on = k in hot
        if on:
            ax.add_patch(Rectangle((x + 0.1, yy - 0.21), 4.4, 0.42, fc=PINK, ec=RED, lw=1.5))
        col = RED if on else "#222"
        label(ax, x + 0.2, yy, a, fs=10.5, ha="left", color=col, bold=on)
        label(ax, x + 1.8, yy, b, fs=10.5, ha="left", color=col, bold=on)
        label(ax, x + 3.2, yy, c, fs=10.5, ha="left", color=col, bold=on)


# ── 그림 1. 권한 없음 ─────────────────────────────────────────────
def fig_open(ax):
    log(ax, ["시작: 장부지기", "열기: /data", "✗ 권한 없음: /data"], hot=(2,))
    ls_win(ax, [(".", "root", "root")], hot=(0,))


# ── 그림 2. 번호표와 명부 ─────────────────────────────────────────
def fig_num(ax):
    person(ax, 0.3, 1.5, "장부 프로그램", "999", hot=True)
    arrow(ax, (3.2, 2.0), (4.3, 2.0), color=RED, ms=13)
    label(ax, 3.75, 2.35, "번호만", fs=9.5, color=RED, bold=True)
    locker(ax, 4.4, 0.8, "장부 파일", "999", "999", plate_hot=True)
    arrow(ax, (7.1, 2.6), (8.5, 2.6), color=INK, ms=12)
    label(ax, 7.8, 2.95, "화면용", fs=9.5, color=INK)
    namebook(ax, 8.6, 1.9, "명부 /etc/passwd", [("0", "root"), ("999", "장부지기")], hot=(1,), w=3.2)


# ── 그림 3. 칸 안과 칸 밖 ─────────────────────────────────────────
def fig_same(ax):
    box(ax, 0.3, 0.3, 5.4, 4.4, fc="white")
    label(ax, 3.0, 4.35, "칸 안", fs=10.5, bold=True)
    box(ax, 6.3, 0.3, 5.4, 4.4, fc="white")
    label(ax, 9.0, 4.35, "칸 밖", fs=10.5, bold=True)
    namebook(ax, 1.55, 2.6, "칸 안 명부", [("0", "root"), ("999", "장부지기")], hot=(1,))
    namebook(ax, 7.55, 2.6, "칸 밖 명부", [("0", "root"), ("1000", "관리자")])
    cell(ax, 1.0, 1.6, 4.4, 0.55, "장부 파일   주인 장부지기", hot=True, fs=10)
    cell(ax, 7.0, 1.6, 4.4, 0.55, "장부 파일   주인 999", hot=True, fs=10)
    person(ax, 7.6, 0.4, "999번 프로그램", "999", w=3.2)
    arrow(ax, (9.2, 1.36), (9.2, 1.58), color=INK, ms=9)


# ── 그림 4. 칸 안 root와 칸 밖 폴더 ───────────────────────────────
def fig_root(ax):
    building(ax, 0.4, 0.3, 6.6, 3.6, [""])
    label(ax, 3.7, 3.5, "주문 장부 칸", fs=10, color=INK, bold=True)
    person(ax, 2.5, 1.8, "칸 안 root", "0", hot=True, w=2.4)
    locker(ax, 8.6, 0.6, "칸 밖 설정 폴더", "0", "0", plate_hot=True, w=3.0)
    label(ax, 10.1, 3.3, "칸 밖", fs=10, color=INK, bold=True)
    arrow(ax, (4.95, 2.3), (8.5, 2.5), color=RED, ms=14)
    label(ax, 6.7, 2.95, "0 = 0", fs=11, color=RED, bold=True)


# ── 그림 5. 나머지 줄 ─────────────────────────────────────────────
def fig_perm(ax):
    person(ax, 0.3, 1.3, "장부 프로그램", "999", groups="999", hot=True)
    arrow(ax, (3.2, 1.9), (4.1, 1.9), color=INK, ms=12)
    locker(ax, 4.2, 0.5, "/data", "0", "0", w=2.8, h=2.8)
    arrow(ax, (7.1, 1.85), (8.15, 1.8), color=RED, ms=12)
    perms(ax, 8.3, 2.6, [("주인 0", True, True), ("그룹 0", True, False), ("나머지", True, False)], hot=(2,))


# ── 그림 6·7. fsGroup ─────────────────────────────────────────────
def spec(ax, hot=()):
    box(ax, 0.3, 2.4, 3.9, 2.2, fc=PAPER)
    label(ax, 0.55, 4.25, "파드 설정", fs=10, ha="left", color=INK, bold=True)
    for k, s in enumerate(["runAsUser: 999", "runAsGroup: 999", "fsGroup: 2000"]):
        on = k in hot
        if on:
            ax.add_patch(Rectangle((0.45, 3.62 - k * 0.5), 3.6, 0.42, fc=PINK, ec=RED, lw=1.4))
        label(ax, 0.6, 3.83 - k * 0.5, s, fs=10.5, ha="left", color=RED if on else "#222", bold=on,
              family="monospace")


def fig_fs1(ax):
    spec(ax, hot=(2,))
    person(ax, 0.6, 0.3, "장부 프로그램", "999", groups="999, 2000", hot=True)
    arrow(ax, (3.5, 0.9), (5.5, 1.2), color=RED, ms=13)
    locker(ax, 5.6, 0.3, "/data", "0", "2000", plate_hot=True, w=2.6, h=2.8)
    perms(ax, 8.9, 1.5, [("주인 0", True, True), ("그룹 2000", True, True), ("나머지", True, False)], hot=(1,))


def fig_fs2(ax):
    spec(ax)
    person(ax, 0.6, 0.3, "장부 프로그램", "999", groups="999, 2000")
    locker(ax, 5.6, 0.3, "/data", "0", "2000", w=2.6, h=2.8)
    arrow(ax, (8.3, 1.6), (9.1, 1.6), color=INK, ms=12)
    label(ax, 8.7, 1.95, "새 파일", fs=9.5, color=INK)
    locker(ax, 9.2, 0.5, "장부 파일", "999", "2000", hot=True, plate_hot=True, w=2.4, h=2.3, fs=9.5)


# ── 그림 8. 고르는 길 ─────────────────────────────────────────────
def fig_decide(ax):
    box(ax, 0.3, 3.9, 5.0, 1.0, fc=NOTE)
    label(ax, 2.8, 4.4, "꼭 root(0번)?", fs=10.5, bold=True)
    arrow(ax, (5.4, 4.4), (6.9, 4.4))
    label(ax, 6.15, 4.7, "예", fs=10, color=INK)
    box(ax, 7.0, 3.9, 4.7, 1.0, fc=PAPER)
    label(ax, 9.35, 4.4, "사용자 네임스페이스", fs=10.5)
    arrow(ax, (2.8, 3.8), (2.8, 3.0))
    label(ax, 3.0, 3.4, "아니요 → runAsUser", fs=10, color=INK, ha="left")
    box(ax, 0.3, 1.9, 5.0, 1.0, fc=NOTE)
    label(ax, 2.8, 2.4, "붙인 디스크에 쓰기?", fs=10.5, bold=True)
    arrow(ax, (5.4, 2.4), (6.9, 2.4))
    label(ax, 6.15, 2.7, "아니요", fs=10, color=INK)
    box(ax, 7.0, 1.9, 4.7, 1.0, fc=PAPER)
    label(ax, 9.35, 2.4, "runAsUser만", fs=10.5)
    arrow(ax, (2.8, 1.8), (2.8, 1.2), color=RED)
    label(ax, 3.0, 1.5, "예", fs=10, color=RED, ha="left")
    box(ax, 0.3, 0.2, 5.0, 0.95, fc=PINK, ec=RED)
    label(ax, 2.8, 0.67, "runAsUser + fsGroup", fs=10.5, color=RED, bold=True)


# ── 그림 9. 다시 켜기 ─────────────────────────────────────────────
def fig_back(ax):
    log(ax, ["시작: 장부지기", "열기: /data", "열림: /data/장부 파일"], hot=(2,))
    ls_win(ax, [(".", "root", "2000"), ("장부 파일", "장부지기", "2000")], hot=(0, 1))


if __name__ == "__main__":
    make(fig_open, "k8s03-open-1.svg", 0, 3.4)
    make(fig_num, "k8s03-num-1.svg", 0.5, 3.6)
    make(fig_same, "k8s03-same-1.svg", 0, 5.0)
    make(fig_root, "k8s03-root-1.svg", 0, 4.6)
    make(fig_perm, "k8s03-perm-1.svg", 0.2, 3.6)
    make(fig_fs1, "k8s03-fs-1.svg", 0, 4.8)
    make(fig_fs2, "k8s03-fs-2.svg", 0, 4.8)
    make(fig_decide, "k8s03-decide.svg", 0, 5.1)
    make(fig_back, "k8s03-back-1.svg", 0, 3.4)
