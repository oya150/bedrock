"""쿠버네티스 17편 그림 만들기. 실행: python lab/fig_k8s17.py  → docs/kubernetes/img/17/*.svg

본문 절은 장면 띠로 그린다: 같은 무대를 여러 장 그리고 장마다 바뀐 곳만 빨강으로 칠한다.
예시는 빵집 주문 앱. 주문 처리(앱 서버)가 주문 장부(데이터베이스)에 접속하는 비밀번호를
Secret "order-db"에 넣는다. 비밀번호는 지어낸 값 croissant, base64로 Y3JvaXNzYW50.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "es"))
from figkit import (GREY, INK, LIGHT, NOTE, PAPER, PINK, RED, arrow, bits, box, bubble,  # noqa: E402
                    canvas, cell, cells, cylinder, label, letters, moral, outdir, save, stage)
from matplotlib.patches import Polygon, Rectangle  # noqa: E402

OUT = outdir("17", topic="kubernetes")
PW, B64 = "croissant", "Y3JvaXNzYW50"
SCRAMBLED = "k3#Qz9!wP@x…"
MONO = "monospace"


# ── 터미널 화면 ───────────────────────────────────────────────────
def terminal(ax, lines, x=0.3, y=0.9, w=8.0, h=5.3):
    """lines=[(글, 빨강?, 흐림?)]. 위에서부터 한 줄씩."""
    box(ax, x, y, w, h, fc="white", round_=False)
    ax.add_patch(Rectangle((x, y + h - 0.45), w, 0.45, fc=LIGHT, ec=INK, lw=1.2))
    label(ax, x + 0.2, y + h - 0.22, "터미널", fs=10.5, ha="left", color=INK)
    for k, (s, hot, dim) in enumerate(lines):
        yy = y + h - 0.9 - k * 0.55
        c = RED if hot else (GREY if dim else "#222")
        fam = MONO if s.isascii() else None
        label(ax, x + 0.25, yy, s, fs=10.5, ha="left", color=c, bold=hot, family=fam)


def envelope(ax, x, y, w=2.6, h=1.6, open_=False, note=None, hot=False):
    ec = RED if hot else INK
    ax.add_patch(Rectangle((x, y), w, h, fc=NOTE, ec=ec, lw=1.8))
    if open_:
        ax.add_patch(Polygon([(x, y + h), (x + w, y + h), (x + w / 2, y + h + 0.8)], closed=True,
                             fc=NOTE, ec=ec, lw=1.8))
        if note:
            cell(ax, x + 0.3, y + h - 0.25, w - 0.6, 0.6, note, hot=hot, fs=11)
    else:
        ax.add_patch(Polygon([(x, y + h), (x + w, y + h), (x + w / 2, y + h * 0.45)], closed=True,
                             fc=PAPER, ec=ec, lw=1.6))


def opening(ax, step):
    lines = [("$ kubectl get secret order-db -o yaml", False, False),
             ("data:", False, False),
             (f"  password: {B64}", step == 1, step > 1)]
    if step >= 2:
        lines += [("", False, False),
                  (f"$ echo {B64} | base64 -d", False, False),
                  (PW, True, False)]
    terminal(ax, lines)
    envelope(ax, 8.8, 3.3, open_=step >= 2, note=PW if step >= 2 else None, hot=step >= 2)
    label(ax, 10.1, 2.85, "Secret order-db", fs=11, bold=True)
    if step == 1:
        label(ax, 10.1, 2.3, "알아볼 수 없어 보여요", fs=10.5, color=RED)
    else:
        label(ax, 10.1, 2.3, "봉투는 잠겨 있지 않았어요", fs=10.5, color=RED)
        moral(ax, 6.0, 0.35, "열쇠 없이 명령 한 줄로 원래 비밀번호가 나왔어요")


# ── base64가 하는 일 ──────────────────────────────────────────────
BYTES = ["01100011", "01110010", "01101111"]
SIX = ["011000", "110111", "001001", "101111"]
NUMS = ["24", "55", "9", "47"]
OUTS = ["Y", "3", "J", "v"]


def b64(ax, step):
    label(ax, 0.3, 6.2, "croissant의 앞 세 글자", fs=11, ha="left", bold=True)
    for k, ch in enumerate("cro"):
        x = 0.3 + k * 3.55
        cell(ax, x + 0.96, 5.2, 0.8, 0.7, ch, fs=13)
        bits(ax, x, 4.3, BYTES[k], w=0.34, h=0.55, dim=range(8) if step > 1 else (), hot=range(8) if step == 1 else ())
    label(ax, 10.5, 4.57, "8칸씩", fs=10, ha="left", color=RED if step == 1 else INK)
    if step == 1:
        label(ax, 6.0, 3.5, "글자 하나 = 0과 1 여덟 칸 (문자 코드)", fs=10.5, color=RED)
    if step >= 2:
        for k in range(4):
            x = 0.3 + k * 2.6
            bits(ax, x, 3.1, SIX[k], w=0.34, h=0.55, hot=range(6) if step == 2 else ())
            label(ax, x + 1.02, 2.55, NUMS[k], fs=12, color=RED if step == 2 else "#222", bold=(step == 2))
        label(ax, 10.5, 3.37, "6칸씩", fs=10, ha="left", color=RED if step == 2 else INK)
    if step == 3:
        for k in range(4):
            x = 0.3 + k * 2.6
            arrow(ax, (x + 1.02, 2.3), (x + 1.02, 1.75), color=RED, ms=11)
            cell(ax, x + 0.67, 1.05, 0.7, 0.65, OUTS[k], hot=True, fs=13)
        label(ax, 10.5, 1.37, "표에서\n글자로", fs=10, ha="left", color=RED)
        moral(ax, 6.0, 0.4, "cro → Y3Jv : 누구나 같은 표로 바꾸고 되돌려요")


def b64table():
    """번호 → 글자 표(일부)."""
    fig, ax = canvas(7.2, 2.4, 12, 4.0)
    label(ax, 0.3, 3.6, "base64 표 (세상 모두가 같은 표를 써요)", fs=11, ha="left", bold=True)
    rows = [("0~25", "A B C … Y Z"), ("26~51", "a b c … y z"), ("52~61", "0 1 … 9"), ("62, 63", "+ /")]
    for k, (n, s) in enumerate(rows):
        y = 2.7 - k * 0.7
        cell(ax, 0.4, y, 1.8, 0.6, n, fs=10.5, fc=LIGHT)
        cell(ax, 2.3, y, 4.2, 0.6, s, fs=10.5)
    for k, (n, ch) in enumerate(zip(NUMS, OUTS)):
        y = 2.7 - k * 0.7
        cell(ax, 7.6, y, 0.9, 0.6, n, fs=11)
        arrow(ax, (8.6, y + 0.3), (9.4, y + 0.3), color=RED, ms=10)
        cell(ax, 9.5, y, 0.7, 0.6, ch, hot=True, fs=12)
    save(fig, OUT, "k8s17-table.svg")


# ── 암호와 base64 견줘 보기 ────────────────────────────────────────
def compare():
    fig, ax = canvas(7.2, 3.6, 12, 6.0)
    label(ax, 0.3, 5.6, "암호 (컴퓨터 10편)", fs=11.5, ha="left", bold=True)
    cell(ax, 0.4, 4.3, 2.4, 0.75, "바다 가자", fs=11)
    arrow(ax, (2.9, 4.67), (4.6, 4.67), ms=12)
    label(ax, 3.75, 5.05, "열쇠 3", fs=10.5, color=INK)
    cell(ax, 4.7, 4.3, 2.4, 0.75, "자바 라타", fs=11)
    arrow(ax, (7.2, 4.67), (8.6, 4.67), ms=12)
    cell(ax, 8.7, 4.3, 2.9, 0.75, "열쇠 없으면 ✗", fs=10.5, fc=PAPER)
    label(ax, 0.3, 3.1, "base64", fs=11.5, ha="left", bold=True, color=RED)
    cell(ax, 0.4, 1.8, 2.4, 0.75, PW, fs=11)
    arrow(ax, (2.9, 2.17), (4.6, 2.17), color=RED, ms=12)
    label(ax, 3.75, 2.55, "열쇠 없음", fs=10.5, color=RED, bold=True)
    cell(ax, 4.7, 1.8, 2.4, 0.75, B64, fs=10.5)
    arrow(ax, (7.2, 2.17), (8.6, 2.17), color=RED, ms=12)
    cell(ax, 8.7, 1.8, 2.9, 0.75, f"누구나 → {PW}", hot=True, fs=10.5)
    moral(ax, 6.0, 0.7, "base64는 암호가 아니라 옮겨 적기예요")
    save(fig, OUT, "k8s17-compare.svg")


# ── 쿠버네티스 안: 보내는 쪽 → API 서버 → etcd ───────────────────
API = (4.2, 3.9, 2.9, 1.5)
ETCD = (8.7, 3.6, 2.8, 1.5)
BACKUP = (8.7, 0.9, 2.8, 1.0)


def cluster(ax, inside=PW, inside_hot=False, key=False, key_hot=False, backup=False, backup_s=None,
            backup_hot=False, sender="Secret 만들기", send_hot=False):
    box(ax, 0.3, 4.1, 2.8, 1.1, fc=PINK if send_hot else PAPER, ec=RED if send_hot else INK)
    label(ax, 1.7, 4.65, sender, fs=10.5, color=RED if send_hot else "#222")
    arrow(ax, (3.2, 4.65), (4.1, 4.65), color=RED if send_hot else GREY, ms=12)
    box(ax, *API, fc=NOTE)
    label(ax, API[0] + API[2] / 2, API[1] + API[3] / 2, "API 서버", fs=12, bold=True)
    arrow(ax, (7.2, 4.65), (8.6, 4.65), color=GREY, ms=12)
    cylinder(ax, *ETCD, "etcd")
    label(ax, 10.1, 4.6, "password:", fs=9.5, color=INK)
    label(ax, 10.1, 4.1, inside, fs=10.5, color=RED if inside_hot else "#222", bold=inside_hot, family=MONO)
    if key:
        c = RED if key_hot else INK
        box(ax, 4.5, 2.4, 2.3, 0.9, fc=PINK if key_hot else "white", ec=c)
        label(ax, 5.65, 2.85, "열쇠", fs=11, color=c, bold=key_hot)
        ax.plot([5.65, 5.65], [3.3, 3.85], color=c, lw=1.6, ls="--")
    if backup:
        arrow(ax, (10.1, 3.4), (10.1, 2.0), color=RED if backup_hot else GREY, ms=12)
        box(ax, *BACKUP, fc=PINK if backup_hot else "white", ec=RED if backup_hot else INK)
        label(ax, 10.1, 1.6, "etcd 백업 파일", fs=10, color=INK)
        label(ax, 10.1, 1.15, backup_s, fs=10.5, color=RED if backup_hot else "#222", family=MONO)


def store(ax, step):
    if step == 1:
        cluster(ax, inside="", send_hot=True)
        label(ax, 1.7, 3.6, f"password: {B64}", fs=9, color=RED, family=MONO)
    elif step == 2:
        cluster(ax, inside_hot=True)
        label(ax, 10.1, 3.0, "암호화 없이 그대로", fs=10.5, color=RED)
    else:
        cluster(ax, backup=True, backup_s=PW, backup_hot=True)
        label(ax, 3.4, 1.4, "백업을 손에 넣은 사람도\n그대로 읽어요", fs=10.5, color=RED)
        moral(ax, 4.0, 0.3, "기본 설정에서 etcd에는 값이 그대로 있어요")


def encrypt(ax, step):
    if step == 1:
        cluster(ax, inside="", key=True, key_hot=True)
        label(ax, 5.65, 1.9, "EncryptionConfiguration", fs=10, color=RED, family=MONO)
    elif step == 2:
        cluster(ax, inside=SCRAMBLED, inside_hot=True, key=True)
        label(ax, 10.1, 3.0, "열쇠로 잠가서 저장", fs=10.5, color=RED)
    else:
        cluster(ax, inside=SCRAMBLED, key=True, backup=True, backup_s=SCRAMBLED, backup_hot=True)
        label(ax, 3.4, 1.4, "백업을 손에 넣어도\n열쇠 없이는 못 읽어요", fs=10.5, color=RED)
        moral(ax, 4.0, 0.3, "저장 시 암호화는 etcd를 훔쳐 가는 사람을 막아요")


def read(ax, step):
    cluster(ax, inside=SCRAMBLED, key=True, sender="읽기 권한 있음" if step == 1 else "읽기 권한 없음",
            send_hot=True)
    if step == 1:
        arrow(ax, (4.1, 4.25), (3.2, 3.2), color=RED, ms=12)
        cell(ax, 0.3, 2.4, 2.8, 0.7, PW, hot=True, fs=11)
        label(ax, 1.7, 1.9, "API 서버가 열쇠로 풀어서 줘요", fs=10, color=RED)
        moral(ax, 6.0, 0.4, "읽을 권한이 있으면 원래 값이 그대로 나와요")
    else:
        label(ax, 3.65, 3.45, "✗", fs=18, color=RED, bold=True)
        cell(ax, 0.3, 2.4, 2.8, 0.7, "거절 (Forbidden)", hot=True, fs=10.5)
        moral(ax, 6.0, 0.4, "값을 지키는 마지막 문은 누가 읽을 수 있는지예요")


# ── 앱이 받아 쓰는 두 길 ───────────────────────────────────────────
def use(ax, step):
    box(ax, 0.2, 3.3, 3.6, 1.5, fc=NOTE)
    label(ax, 2.0, 4.35, "Secret order-db", fs=11, bold=True)
    label(ax, 2.0, 3.75, f"password: {B64}", fs=8.5, color=INK, family=MONO)
    box(ax, 5.2, 0.9, 6.4, 5.0, fc="white")
    label(ax, 8.4, 5.55, "주문 처리 컨테이너", fs=11.5, bold=True)
    on1, on2 = step == 1, step == 2
    arrow(ax, (3.9, 4.4), (5.6, 4.4), color=RED if on1 else GREY, ms=12)
    label(ax, 4.6, 5.15, "① 환경 변수", fs=10, color=RED if on1 else INK, bold=on1)
    cell(ax, 5.7, 4.0, 5.6, 0.75, f"DB_PASSWORD={PW}", hot=on1, fs=11)
    arrow(ax, (3.9, 3.5), (5.6, 2.5), color=RED if on2 else GREY, ms=12)
    label(ax, 4.2, 2.75, "② 파일", fs=10, color=RED if on2 else INK, bold=on2)
    cell(ax, 5.7, 2.15, 2.9, 0.7, "/etc/db/password", fs=10, fc=LIGHT)
    cell(ax, 8.7, 2.15, 2.6, 0.7, PW, hot=on2, fs=11)
    if on1:
        label(ax, 8.5, 3.45, "시작할 때 한 번 받아요", fs=10, color=RED)
    else:
        label(ax, 8.5, 1.55, "Secret을 고치면 파일도 따라 바뀌어요", fs=10, color=RED)
        moral(ax, 6.0, 0.35, "컨테이너 안에서는 base64를 풀어 원래 값으로 받아요")


# ── 판단 (한 장) ───────────────────────────────────────────────────
def decide():
    fig, ax = canvas(10, 4.2, 15, 6.4)
    box(ax, 0.3, 4.6, 6.0, 1.3, fc=NOTE)
    label(ax, 3.3, 5.25, "남이 알면 안 되는 값인가요?", fs=10.5, bold=True)
    arrow(ax, (6.4, 5.25), (8.4, 5.25)); label(ax, 7.4, 5.55, "아니요", fs=10, color=INK)
    box(ax, 8.5, 4.6, 6.2, 1.3, fc=PAPER)
    label(ax, 11.6, 5.25, "보통 설정 (ConfigMap)", fs=10.5)
    arrow(ax, (3.3, 4.5), (3.3, 3.5)); label(ax, 3.6, 4.0, "예 → Secret에 넣어요", fs=10, color=INK, ha="left")
    box(ax, 0.3, 2.2, 6.0, 1.2, fc=NOTE)
    label(ax, 3.3, 2.8, "저장 시 암호화가 켜져 있나요?", fs=10.5, bold=True)
    arrow(ax, (6.4, 2.8), (8.4, 2.8)); label(ax, 7.4, 3.1, "아니요", fs=10, color=INK)
    box(ax, 8.5, 2.2, 6.2, 1.2, fc=PAPER)
    label(ax, 11.6, 2.8, "켜요 (etcd를 훔쳐 가도 못 읽게)", fs=10.5)
    arrow(ax, (3.3, 2.1), (3.3, 1.3), color=RED); label(ax, 3.6, 1.7, "예", fs=10, color=RED, ha="left")
    box(ax, 0.3, 0.1, 6.0, 1.1, fc=PINK, ec=RED)
    label(ax, 3.3, 0.65, "읽을 수 있는 쪽을 꼭 필요한 곳만으로", fs=10.5, color=RED, bold=True)
    save(fig, OUT, "k8s17-decide.svg")


# ── 정리: 처음 장면으로 돌아가기 ───────────────────────────────────
def back(ax, step):
    if step == 1:
        lines = [("$ kubectl get secret order-db -o yaml", False, True), ("data:", False, True),
                 (f"  password: {B64}", False, True), ("", False, False),
                 (f"$ echo {B64} | base64 -d", False, True), (PW, False, True)]
        terminal(ax, lines)
        envelope(ax, 8.8, 3.3, open_=True, note=PW)
        label(ax, 10.1, 2.85, "처음", fs=11, bold=True)
        label(ax, 10.1, 2.3, "누구나 읽을 수 있었어요", fs=10.5, color=INK)
    elif step == 2:
        lines = [("$ kubectl get secret order-db -o yaml", False, False),
                 ("Error from server (Forbidden)", True, False)]
        terminal(ax, lines)
        envelope(ax, 8.8, 3.3, hot=True)
        label(ax, 10.1, 2.85, "권한 없는 사람", fs=11, bold=True)
        label(ax, 10.1, 2.3, "봉투를 받지도 못해요", fs=10.5, color=RED)
    else:
        lines = [("주문 처리 컨테이너 안", False, False), (f"DB_PASSWORD={PW}", True, False),
                 ("", False, False), ("etcd 백업 파일", False, False), (SCRAMBLED, True, False)]
        terminal(ax, lines)
        envelope(ax, 8.8, 3.3, open_=True, note=PW, hot=True)
        label(ax, 10.1, 2.85, "주문 처리 앱", fs=11, bold=True)
        label(ax, 10.1, 2.3, "꼭 필요한 곳만 열어요", fs=10.5, color=RED)
        moral(ax, 6.0, 0.35, "값을 지키는 건 base64가 아니라 권한과 저장 시 암호화예요")


# ── 정리: 낱말 카드 ────────────────────────────────────────────────
def cards():
    fig, ax = canvas(6.4, 7.8, 9.8, 12.2)
    W, H = 4.6, 3.8

    def card(i, name, line):
        col, row = i % 2, i // 2
        x, y = 0.2 + col * 4.9, 8.2 - row * 4.05
        box(ax, x, y, W, H, fc="white")
        label(ax, x + 0.25, y + H - 0.4, name, fs=12.5, ha="left", bold=True)
        label(ax, x + W / 2, y + 0.6, line, fs=10, color=INK)
        return x, y

    x, y = card(0, "Secret", "비밀번호 같은 값을 담는\n쿠버네티스 물건")
    cell(ax, x + 0.5, y + 1.6, 3.6, 0.8, "password: Y3Jv…", fs=10.5)
    x, y = card(1, "base64", "아무 데이터나 64가지 글자로\n옮겨 적는 방법, 열쇠 없음")
    cell(ax, x + 0.3, y + 1.6, 1.4, 0.8, "cro", fs=11)
    arrow(ax, (x + 1.8, y + 2.0), (x + 2.6, y + 2.0), color=RED, ms=11)
    cell(ax, x + 2.7, y + 1.6, 1.5, 0.8, "Y3Jv", hot=True, fs=11)
    x, y = card(2, "저장 시 암호화", "etcd에 쓸 때 열쇠로 잠가\n저장하는 일, 따로 켜야 해요")
    cell(ax, x + 0.3, y + 1.6, 1.4, 0.8, PW, fs=9.5)
    label(ax, x + 2.15, y + 2.35, "열쇠", fs=9.5, color=RED)
    arrow(ax, (x + 1.8, y + 2.0), (x + 2.6, y + 2.0), color=RED, ms=11)
    cell(ax, x + 2.7, y + 1.6, 1.5, 0.8, "k3#Qz…", hot=True, fs=10)
    x, y = card(3, "etcd", "쿠버네티스가 모든 물건을\n적어 두는 저장소")
    cylinder(ax, x + 1.6, y + 1.45, 1.4, 0.8, "")
    save(fig, OUT, "k8s17-cards.svg")


if __name__ == "__main__":
    S, L = (7.2, 3.8), (12, 6.6)
    stage(opening, 2, OUT, "k8s17-open", S, L)
    stage(b64, 3, OUT, "k8s17-b64", S, L)
    b64table()
    compare()
    stage(store, 3, OUT, "k8s17-store", S, L)
    stage(encrypt, 3, OUT, "k8s17-encrypt", S, L)
    stage(read, 2, OUT, "k8s17-read", S, L)
    stage(use, 2, OUT, "k8s17-use", S, L)
    decide()
    stage(back, 3, OUT, "k8s17-back", S, L)
    cards()
