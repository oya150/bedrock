"""쿠버네티스 3편 그림 만들기. 실행: python lab/fig_k8s03.py  → docs/kubernetes/img/03/*.svg

대표 비유는 사물함 번호표. 파일 = 사물함, 문 위 번호표 = 주인 번호(UID)·그룹 번호(GID),
프로세스 = 번호표 열쇠를 든 사람, 명부 = 번호를 이름으로 바꿔 보여 주는 표(칸마다 따로).
예시는 빵집 주문 앱의 주문 장부. 장부 프로그램은 999번(안 명부 이름 장부지기), 붙인 디스크는 처음에 0번 root 것.
쿠버네티스 설정은 runAsUser 999, runAsGroup 999, fsGroup 2000.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "es"))
from figkit import (GREY, INK, LIGHT, NOTE, PAPER, PINK, RED, arrow, box, canvas, cell,  # noqa: E402
                    label, moral, outdir, save, stage)
from fig_k8s01 import building, window  # noqa: E402
from matplotlib.patches import Circle, Rectangle  # noqa: E402

OUT = outdir("03", topic="kubernetes")


# ── 재료 ───────────────────────────────────────────────────────────
def locker(ax, x, y, name, owner, group, hot=False, plate_hot=False, dim=False, w=2.6, h=2.4, fs=10):
    """사물함 하나(= 파일·폴더). 위에 번호표, 가운데 이름."""
    ec = RED if hot else (GREY if dim else INK)
    ax.add_patch(Rectangle((x, y), w, h, fc=PINK if hot else NOTE, ec=ec, lw=2.0 if hot else 1.5))
    ax.add_patch(Circle((x + w - 0.3, y + h * 0.4), 0.08, fc=ec, ec="none"))
    pc = RED if plate_hot else (GREY if dim else INK)
    ax.add_patch(Rectangle((x + 0.2, y + h - 1.0), w - 0.4, 0.82, fc=PINK if plate_hot else "white", ec=pc,
                           lw=1.8 if plate_hot else 1.2))
    label(ax, x + w / 2, y + h - 0.59, f"주인 {owner}\n그룹 {group}", fs=fs - 0.5, color=pc, bold=plate_hot)
    label(ax, x + w / 2, y + (h - 1.0) / 2, name, fs=fs, color=RED if hot else (GREY if dim else "#222"), bold=hot)


def person(ax, x, y, name, num, groups=None, hot=False, dim=False, w=2.8):
    """프로세스(= 번호 열쇠를 든 사람). 이름 칸과 번호 칸."""
    ec = RED if hot else (GREY if dim else INK)
    box(ax, x, y, w, 1.25 if groups else 0.95, fc=PINK if hot else PAPER, ec=ec)
    c = RED if hot else (GREY if dim else "#222")
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
    label(ax, x, y + 0.35, "누가", fs=9, ha="left", color=INK)
    label(ax, x + 1.7, y + 0.35, "읽기", fs=9, color=INK)
    label(ax, x + 2.4, y + 0.35, "쓰기", fs=9, color=INK)
    for k, (who, r, wr) in enumerate(rows_):
        yy = y - 0.4 * k
        on = k in hot
        if on:
            ax.add_patch(Rectangle((x - 0.1, yy - 0.18), 2.8, 0.36, fc=PINK, ec=RED, lw=1.3))
        c = RED if on else "#222"
        label(ax, x, yy, who, fs=9.5, ha="left", color=c, bold=on)
        label(ax, x + 1.7, yy, "O" if r else "X", fs=9.5, color=c)
        label(ax, x + 2.4, yy, "O" if wr else "X", fs=9.5, color=c, bold=on)


# ── 여는 장면: 권한이 없어요 ───────────────────────────────────────
def log(ax, lines, hot=()):
    window(ax, 0.3, 3.0, 6.4, 3.2, "주문 장부 컨테이너 기록")
    for k, s in enumerate(lines):
        yy = 5.25 - k * 0.55
        on = k in hot
        if on:
            ax.add_patch(Rectangle((0.4, yy - 0.23), 6.2, 0.46, fc=PINK, ec=RED, lw=1.5))
        label(ax, 0.6, yy, s, fs=10.5, ha="left", color=RED if on else "#222", bold=on)


def ls_win(ax, rows_, hot=(), x=7.1, y=3.0):
    window(ax, x, y, 4.6, 3.2, "/data 안")
    label(ax, x + 0.2, y + 2.3, "이름", fs=9.5, ha="left", color=INK)
    label(ax, x + 1.8, y + 2.3, "주인", fs=9.5, ha="left", color=INK)
    label(ax, x + 3.2, y + 2.3, "그룹", fs=9.5, ha="left", color=INK)
    ax.plot([x + 0.15, x + 4.45], [y + 2.08, y + 2.08], color=INK, lw=0.8)
    for k, (a, b, c) in enumerate(rows_):
        yy = y + 1.7 - k * 0.5
        on = k in hot
        if on:
            ax.add_patch(Rectangle((x + 0.1, yy - 0.21), 4.4, 0.42, fc=PINK, ec=RED, lw=1.5))
        col = RED if on else "#222"
        label(ax, x + 0.2, yy, a, fs=10.5, ha="left", color=col, bold=on)
        label(ax, x + 1.8, yy, b, fs=10.5, ha="left", color=col, bold=on)
        label(ax, x + 3.2, yy, c, fs=10.5, ha="left", color=col, bold=on)


ERR = ["장부 프로그램을 켜요 (장부지기)", "장부 파일을 여는 중…", "✗ 권한이 없어요: /data"]


def opening(ax, step):
    if step == 1:
        log(ax, ERR, hot=(2,))
        label(ax, 3.5, 2.4, "붙인 디스크 /data에 쓰지 못하고 멈췄어요", fs=11, color=RED)
    elif step == 2:
        log(ax, ERR)
        ls_win(ax, [(".", "root", "root")], hot=(0,))
        label(ax, 9.4, 2.4, "/data는 root 것이에요", fs=11, color=RED)
    else:
        log(ax, ["장부 프로그램을 켜요 (root)", "장부 파일을 여는 중…", "장부 파일을 열었어요"], hot=(0, 2))
        ls_win(ax, [(".", "root", "root")])
        label(ax, 3.5, 2.4, "root로 바꿔 켜니 열렸어요", fs=11, color=RED)
        moral(ax, 6.0, 1.2, "그런데 컨테이너 안의 root는 어떤 사람일까요?")


# ── 번호표 ─────────────────────────────────────────────────────────
def num(ax, step):
    locker(ax, 4.6, 1.6, "장부 파일", "999", "999", plate_hot=(step == 1))
    person(ax, 0.4, 2.2, "장부 프로그램", "999", hot=(step == 1))
    if step == 1:
        arrow(ax, (3.3, 2.7), (4.5, 3.4), color=RED, ms=13)
        label(ax, 6.0, 5.5, "커널은 번호표의 숫자와 프로그램 번호만 맞춰 봐요", fs=11, color=RED, bold=True)
    else:
        namebook(ax, 8.4, 2.1, "이 칸의 명부", [("0", "root"), ("999", "장부지기")], hot=(1,))
        arrow(ax, (7.3, 3.7), (8.3, 2.95), color=RED, ms=12)
        label(ax, 10.0, 4.05, "화면에 보일 때만\n이름으로 바꿔요", fs=10, color=RED)
        label(ax, 6.0, 5.5, "999가 누구 이름인지는 명부에만 적혀 있어요", fs=11, color=INK)
        moral(ax, 6.0, 0.7, "파일에 적힌 주인은 번호예요. 이름은 명부에서 찾아요")


# ── 이름은 달라도 번호가 같으면 ───────────────────────────────────
def same(ax, step):
    box(ax, 0.3, 0.9, 5.4, 5.0, fc="white")
    label(ax, 3.0, 5.55, "주문 장부 칸 안에서", fs=10.5, bold=True)
    box(ax, 6.3, 0.9, 5.4, 5.0, fc="white")
    label(ax, 9.0, 5.55, "칸 밖 컴퓨터에서", fs=10.5, bold=True)
    namebook(ax, 1.55, 3.55, "칸 안 명부", [("0", "root"), ("999", "장부지기")], hot=(1,) if step == 1 else ())
    namebook(ax, 7.55, 3.55, "칸 밖 명부", [("0", "root"), ("1000", "관리자")])
    for x0, shown in ((1.0, "장부지기"), (7.0, "999")):
        cell(ax, x0, 2.15, 4.4, 0.55, f"장부 파일   주인 {shown}", hot=(step == 1), fs=10)
    if step == 1:
        label(ax, 6.0, 1.45, "같은 파일이 안에서는 장부지기, 밖에서는 999로 보여요", fs=10.5, color=RED, bold=True)
    else:
        person(ax, 7.0, 1.0, "칸 밖 999번 프로그램", "999", hot=True, w=4.4)
        label(ax, 3.0, 1.45, "칸 밖 명부에는 999가 없어서\n번호 그대로 보여요", fs=10, color=INK)
        moral(ax, 6.0, 0.35, "칸 밖의 999번도 이 파일의 주인이에요: 번호가 같으면 같은 사람")


# ── 컨테이너 안의 root ─────────────────────────────────────────────
def root(ax, step):
    building(ax, 0.4, 0.9, 7.0, 4.0, [""], room_hot=(0,) if step >= 2 else (), kern_hot=(step == 1))
    label(ax, 3.9, 4.4, "주문 장부 칸", fs=10, color=INK, bold=True)
    person(ax, 2.5, 3.0, "칸 안 root", "0", hot=(step >= 2), w=2.4)
    if step == 1:
        label(ax, 3.9, 1.7, "", fs=9)
        namebook(ax, 8.4, 3.6, "칸 밖 명부", [("0", "root")])
        label(ax, 9.85, 2.9, "밖의 root도 0번", fs=10.5, color=INK)
        label(ax, 6.0, 6.3, "관리실은 하나: 안의 0번과 밖의 0번을 구별하지 않아요", fs=10.5, color=RED, bold=True)
    else:
        locker(ax, 8.6, 1.4, "칸 밖 설정 폴더", "0", "0", hot=(step == 2), w=3.0)
        arrow(ax, (4.95, 3.5), (8.5, 2.8), color=RED, ms=14)
        label(ax, 10.1, 4.35, "칸 밖 폴더를\n칸 안에 붙였어요", fs=10, color=INK)
        if step == 2:
            label(ax, 10.1, 0.95, "칸 안 0번이 고칠 수 있어요", fs=10.5, color=RED, bold=True)
        else:
            label(ax, 10.1, 0.95, "주인 0번과 번호가 같으니까", fs=10.5, color=RED, bold=True)
            moral(ax, 6.0, 0.3, "번호로는 칸 안 root도 칸 밖 root와 같은 0번이에요")


# ── 번호가 안 맞으면 ──────────────────────────────────────────────
DATA_ROWS = [("주인 0", True, True), ("그룹 0", True, False), ("나머지", True, False)]


def perm(ax, step):
    if step < 3:
        locker(ax, 4.4, 1.6, "/data", "0", "0", hot=(step == 1), w=2.8, h=2.8)
    if step == 1:
        person(ax, 0.3, 2.4, "장부 프로그램", "999", groups="999", hot=True)
        perms(ax, 8.4, 4.0, DATA_ROWS, hot=(2,))
        label(ax, 9.7, 2.4, "999는 주인도 그룹도 아니어서\n나머지 줄: 쓰기 X", fs=10, color=RED, bold=True)
    elif step == 2:
        person(ax, 0.3, 2.4, "장부 프로그램", "0", groups="0", dim=True)
        perms(ax, 8.4, 4.0, DATA_ROWS)
        label(ax, 9.7, 2.4, "root(0번)로 돌리면 주인 줄이라\n쓰지만, 앞 절의 위험이 남아요", fs=10, color=INK)
    else:
        person(ax, 0.3, 2.4, "장부 프로그램", "999", groups="999, 2000", hot=True)
        locker(ax, 4.4, 1.6, "/data", "0", "2000", plate_hot=True, w=2.8, h=2.8)
        perms(ax, 8.4, 4.0, [("주인 0", True, True), ("그룹 2000", True, True), ("나머지", True, False)], hot=(1,))
        label(ax, 9.7, 2.4, "같은 그룹 줄에 들고\n그 줄에 쓰기가 있으면 돼요", fs=10, color=RED, bold=True)
        moral(ax, 6.0, 0.7, "root가 아니어도 디스크 그룹에 들면 써요")


# ── fsGroup ────────────────────────────────────────────────────────
def spec(ax, hot=()):
    box(ax, 0.3, 3.6, 3.9, 2.4, fc=PAPER)
    label(ax, 0.55, 5.65, "파드 설정", fs=10, ha="left", color=INK, bold=True)
    for k, s in enumerate(["runAsUser: 999", "runAsGroup: 999", "fsGroup: 2000"]):
        on = k in hot
        if on:
            ax.add_patch(Rectangle((0.45, 5.02 - k * 0.5), 3.6, 0.42, fc=PINK, ec=RED, lw=1.4))
        label(ax, 0.6, 5.23 - k * 0.5, s, fs=10.5, ha="left", color=RED if on else "#222", bold=on,
              family="monospace")


def fs(ax, step):
    if step == 1:
        spec(ax, hot=(0, 1))
        person(ax, 0.6, 1.0, "장부 프로그램", "999", groups="999", hot=True)
        locker(ax, 6.4, 1.0, "/data", "0", "0", w=2.6, h=2.8)
        label(ax, 7.8, 4.5, "디스크는 아직 그대로", fs=10, color=INK)
        label(ax, 5.2, 5.7, "① 프로그램을 999번으로 켜요", fs=10.5, ha="left", color=RED, bold=True)
    elif step == 2:
        spec(ax, hot=(2,))
        person(ax, 0.6, 1.0, "장부 프로그램", "999", groups="999")
        locker(ax, 6.4, 1.0, "/data", "0", "2000", plate_hot=True, w=2.6, h=2.8)
        perms(ax, 9.25, 2.3, [("그룹 2000", True, True)], hot=(0,))
        label(ax, 5.2, 5.7, "② 디스크를 붙이기 전에 그룹을 2000으로,\n   그룹에 쓰기를 열어 둬요", fs=10.5,
              ha="left", color=RED, bold=True)
    elif step == 3:
        spec(ax, hot=(2,))
        person(ax, 0.6, 1.0, "장부 프로그램", "999", groups="999, 2000", hot=True)
        locker(ax, 6.4, 1.0, "/data", "0", "2000", w=2.6, h=2.8)
        arrow(ax, (3.5, 1.6), (6.3, 1.9), color=RED, ms=13)
        label(ax, 5.2, 5.7, "③ 프로그램도 그룹 2000에 넣어요 → 쓸 수 있어요", fs=10.5, ha="left", color=RED,
              bold=True)
    else:
        spec(ax)
        person(ax, 0.6, 1.0, "장부 프로그램", "999", groups="999, 2000")
        locker(ax, 6.4, 1.0, "/data", "0", "2000", w=2.6, h=2.8)
        locker(ax, 9.75, 1.3, "장부 파일", "999", "2000", hot=True, plate_hot=True, w=2.2, h=2.2, fs=9.5)
        label(ax, 5.2, 5.7, "④ 새로 만든 파일도 그룹 2000을 물려받아요", fs=10.5, ha="left", color=RED, bold=True)
        moral(ax, 6.0, 0.3, "실행 번호와 디스크 그룹을 맞추면 root 없이 써요")


# ── 판단 (한 장) ──────────────────────────────────────────────────
def decide():
    fig, ax = canvas(10, 4.2, 15, 6.4)
    box(ax, 0.3, 4.6, 6.2, 1.3, fc=NOTE)
    label(ax, 3.4, 5.25, "프로그램이 꼭 root(0번)로\n돌아야 하나요?", fs=10.5, bold=True)
    arrow(ax, (6.6, 5.25), (8.4, 5.25)); label(ax, 7.5, 5.55, "예", fs=10, color=INK)
    box(ax, 8.5, 4.6, 6.2, 1.3, fc=PAPER)
    label(ax, 11.6, 5.25, "칸 안 0번을 밖에서 다른 번호로\n바꾸는 사용자 네임스페이스", fs=10.5)
    arrow(ax, (3.4, 4.5), (3.4, 3.5)); label(ax, 3.7, 4.0, "아니요: runAsUser로 0이 아닌 번호", fs=10,
                                             color=INK, ha="left")
    box(ax, 0.3, 2.1, 6.2, 1.3, fc=NOTE)
    label(ax, 3.4, 2.75, "붙인 디스크에 쓰나요?", fs=10.5, bold=True)
    arrow(ax, (6.6, 2.75), (8.4, 2.75)); label(ax, 7.5, 3.05, "아니요", fs=10, color=INK)
    box(ax, 8.5, 2.1, 6.2, 1.3, fc=PAPER)
    label(ax, 11.6, 2.75, "실행 번호만 정하면 돼요", fs=10.5)
    arrow(ax, (3.4, 2.0), (3.4, 1.3), color=RED); label(ax, 3.7, 1.65, "예", fs=10, color=RED, ha="left")
    box(ax, 0.3, 0.1, 6.2, 1.1, fc=PINK, ec=RED)
    label(ax, 3.4, 0.65, "fsGroup으로 디스크 그룹을 맞춰요", fs=10.5, color=RED, bold=True)
    save(fig, OUT, "k8s03-decide.svg")


# ── 정리: 처음 장면으로 돌아가기 ───────────────────────────────────
def back(ax, step):
    if step == 1:
        log(ax, ERR, hot=(2,))
        ls_win(ax, [(".", "root", "root")], hot=(0,))
        label(ax, 6.0, 2.3, "처음엔 999번 장부지기가 0번 root의 /data에 쓰려 했어요", fs=10.5, color=INK)
    else:
        log(ax, ["장부 프로그램을 켜요 (장부지기)", "장부 파일을 여는 중…", "장부 파일을 열었어요"], hot=(2,))
        ls_win(ax, [(".", "root", "2000"), ("장부 파일", "장부지기", "2000")], hot=(0, 1))
        label(ax, 6.0, 2.3, "runAsUser 999 · fsGroup 2000을 주고 다시 켰어요", fs=10.5, color=RED, bold=True)
        moral(ax, 6.0, 1.3, "root로 바꾸지 않고 번호를 맞췄더니 열렸어요")


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

    x, y = card(0, "사용자 번호(UID)", "커널이 사람을 구별하는 번호\n파일 주인도 이 번호로 적어요")
    locker(ax, x + 1.0, y + 1.15, "", "999", "999", plate_hot=True, w=2.6, h=1.75)
    x, y = card(1, "그룹 번호(GID)", "사람 묶음의 번호\n같은 그룹 줄의 권한을 받아요")
    perms(ax, x + 0.9, y + 2.3, [("그룹 2000", True, True)], hot=(0,))
    x, y = card(2, "명부", "번호를 이름으로 바꿔\n보여 주는 표, 칸마다 따로")
    namebook(ax, x + 0.85, y + 1.3, "칸 안 명부", [("0", "root"), ("999", "장부지기")], hot=(1,))
    x, y = card(3, "root", "0번 사용자\n칸 안과 밖이 같은 0번이에요")
    cell(ax, x + 0.7, y + 1.7, 1.4, 0.6, "안 0", hot=True, fs=10.5)
    label(ax, x + 2.3, y + 2.0, "=", fs=14, color=RED, bold=True)
    cell(ax, x + 2.5, y + 1.7, 1.4, 0.6, "밖 0", hot=True, fs=10.5)
    x, y = card(4, "runAsUser", "컨테이너 프로그램을\n몇 번으로 켤지 정하는 설정")
    person(ax, x + 1.0, y + 1.5, "장부 프로그램", "999", hot=True, w=2.6)
    x, y = card(5, "fsGroup", "붙인 디스크의 그룹을 맞추고\n프로그램도 그 그룹에 넣는 설정")
    locker(ax, x + 1.0, y + 1.15, "", "0", "2000", plate_hot=True, w=2.6, h=1.75)
    save(fig, OUT, "k8s03-cards.svg")


if __name__ == "__main__":
    S, L = (7.2, 3.8), (12, 6.6)
    stage(opening, 3, OUT, "k8s03-open", S, L)
    stage(num, 2, OUT, "k8s03-num", S, L)
    stage(same, 2, OUT, "k8s03-same", S, L)
    stage(root, 3, OUT, "k8s03-root", S, L)
    stage(perm, 3, OUT, "k8s03-perm", S, L)
    stage(fs, 4, OUT, "k8s03-fs", S, L)
    decide()
    stage(back, 2, OUT, "k8s03-back", S, L)
    cards()
