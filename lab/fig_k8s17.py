"""쿠버네티스 17편 그림 만들기. 실행: python lab/fig_k8s17.py  → docs/kubernetes/img/17/*.svg

그림 하나가 한 장면. 그림 안에는 낱말과 숫자만 두고 지금 볼 곳만 빨강으로 칠한다.
예시는 빵집 주문 앱. 주문 처리(앱 서버)가 주문 장부(데이터베이스)에 접속하는 비밀번호를
Secret "order-db"에 넣는다. 비밀번호는 지어낸 값 croissant, base64로 Y3JvaXNzYW50.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "es"))
from figkit import (GREY, INK, LIGHT, NOTE, PAPER, PINK, RED, arrow, bits, box,  # noqa: E402
                    canvas, cell, cylinder, label, outdir, save)
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


def opening():
    fig, ax = canvas(*S, *L)
    lines = [("$ kubectl get secret order-db -o yaml", False, False),
             ("data:", False, False),
             (f"  password: {B64}", False, False),
             ("", False, False),
             (f"$ echo {B64} | base64 -d", False, False),
             (PW, True, False)]
    terminal(ax, lines)
    envelope(ax, 8.8, 3.3, open_=True, note=PW, hot=True)
    label(ax, 10.1, 2.85, "Secret order-db", fs=11, bold=True)
    save(fig, OUT, "k8s17-open.svg")


# ── base64가 하는 일 ──────────────────────────────────────────────
BYTES = ["01100011", "01110010", "01101111"]
SIX = ["011000", "110111", "001001", "101111"]
NUMS = ["24", "55", "9", "47"]
OUTS = ["Y", "3", "J", "v"]


def b64():
    fig, ax = canvas(*S, *L)
    for k, ch in enumerate("cro"):
        x = 0.3 + k * 3.55
        cell(ax, x + 0.96, 5.5, 0.8, 0.7, ch, fs=13)
        bits(ax, x, 4.5, BYTES[k], w=0.34, h=0.55)
    label(ax, 10.5, 4.77, "8칸씩", fs=10.5, ha="left", color=INK)
    for k in range(4):
        x = 0.3 + k * 2.6
        bits(ax, x, 3.2, SIX[k], w=0.34, h=0.55)
        label(ax, x + 1.02, 2.6, NUMS[k], fs=12, color="#222", bold=True)
        arrow(ax, (x + 1.02, 2.3), (x + 1.02, 1.6), color=RED, ms=11)
        cell(ax, x + 0.67, 0.85, 0.7, 0.65, OUTS[k], hot=True, fs=13)
    label(ax, 10.5, 3.47, "6칸씩", fs=10.5, ha="left", color=INK)
    label(ax, 10.5, 2.6, "숫자", fs=10.5, ha="left", color=INK)
    label(ax, 10.5, 1.17, "글자", fs=10.5, ha="left", color=RED, bold=True)
    save(fig, OUT, "k8s17-b64.svg")


def b64table():
    """번호 → 글자 표(일부)."""
    fig, ax = canvas(7.2, 2.4, 12, 4.0)
    label(ax, 0.3, 3.6, "base64 표", fs=11, ha="left", bold=True)
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


# ── 암호와 base64 나란히 ───────────────────────────────────────────
def compare():
    fig, ax = canvas(7.2, 3.0, 12, 5.0)
    label(ax, 0.3, 4.6, "암호", fs=11.5, ha="left", bold=True)
    cell(ax, 0.4, 3.3, 2.4, 0.75, "바다 가자", fs=11)
    arrow(ax, (2.9, 3.67), (4.6, 3.67), ms=12)
    label(ax, 3.75, 4.05, "열쇠 3", fs=10.5, color=INK)
    cell(ax, 4.7, 3.3, 2.4, 0.75, "자바 라타", fs=11)
    arrow(ax, (7.2, 3.67), (8.6, 3.67), ms=12)
    cell(ax, 8.7, 3.3, 2.9, 0.75, "열쇠 없으면 ✗", fs=10.5, fc=PAPER)
    label(ax, 0.3, 2.1, "base64", fs=11.5, ha="left", bold=True, color=RED)
    cell(ax, 0.4, 0.8, 2.4, 0.75, PW, fs=11)
    arrow(ax, (2.9, 1.17), (4.6, 1.17), color=RED, ms=12)
    label(ax, 3.75, 1.55, "열쇠 없음", fs=10.5, color=RED, bold=True)
    cell(ax, 4.7, 0.8, 2.4, 0.75, B64, fs=10.5)
    arrow(ax, (7.2, 1.17), (8.6, 1.17), color=RED, ms=12)
    cell(ax, 8.7, 0.8, 2.9, 0.75, f"누구나 → {PW}", hot=True, fs=10.5)
    save(fig, OUT, "k8s17-compare.svg")


# ── 쿠버네티스 안: 보내는 쪽 → API 서버 → etcd ───────────────────
API = (4.2, 3.9, 2.9, 1.5)
ETCD = (8.7, 3.6, 2.8, 1.5)
BACKUP = (8.7, 0.9, 2.8, 1.0)


def cluster(ax, inside=PW, inside_hot=False, key=False, key_hot=False, backup_s=None, backup_hot=False):
    box(ax, 0.3, 4.1, 2.8, 1.1, fc=PAPER)
    label(ax, 1.7, 4.65, "Secret 만들기", fs=10.5)
    label(ax, 1.7, 3.6, f"password: {B64}", fs=9, color=INK, family=MONO)
    arrow(ax, (3.2, 4.65), (4.1, 4.65), color=GREY, ms=12)
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
    arrow(ax, (10.1, 3.4), (10.1, 2.0), color=GREY, ms=12)
    box(ax, *BACKUP, fc=PINK if backup_hot else "white", ec=RED if backup_hot else INK)
    label(ax, 10.1, 1.6, "etcd 백업 파일", fs=10, color=INK)
    label(ax, 10.1, 1.15, backup_s, fs=10.5, color=RED if backup_hot else "#222", family=MONO)


def store():
    fig, ax = canvas(*S, *L)
    cluster(ax, inside_hot=True, backup_s=PW, backup_hot=True)
    save(fig, OUT, "k8s17-store.svg")


def encrypt():
    fig, ax = canvas(*S, *L)
    cluster(ax, inside=SCRAMBLED, inside_hot=True, key=True, key_hot=True, backup_s=SCRAMBLED, backup_hot=True)
    label(ax, 5.65, 1.9, "EncryptionConfiguration", fs=10, color=INK, family=MONO)
    save(fig, OUT, "k8s17-encrypt.svg")


# ── 읽기: 권한 있음 / 없음 ─────────────────────────────────────────
def read():
    fig, ax = canvas(*S, *L)
    ax_api = (5.0, 2.6, 2.4, 1.6)
    box(ax, *ax_api, fc=NOTE)
    label(ax, 6.2, 3.4, "API 서버", fs=12, bold=True)
    cylinder(ax, 9.0, 2.65, 2.7, 1.5, "etcd")
    label(ax, 10.35, 3.6, "password:", fs=9.5, color=INK)
    label(ax, 10.35, 3.1, SCRAMBLED, fs=10.5, family=MONO)
    arrow(ax, (7.5, 3.4), (8.9, 3.4), color=GREY, ms=12)
    box(ax, 5.05, 0.6, 2.3, 0.9, fc="white")
    label(ax, 6.2, 1.05, "열쇠", fs=11, color=INK)
    ax.plot([6.2, 6.2], [1.5, 2.55], color=INK, lw=1.6, ls="--")
    # 위: 권한 있음
    box(ax, 0.3, 5.0, 3.0, 0.9, fc=PAPER)
    label(ax, 1.8, 5.45, "읽기 권한 있음", fs=10.5)
    arrow(ax, (3.4, 5.35), (5.0, 4.25), color=GREY, ms=12)
    arrow(ax, (5.0, 3.85), (3.4, 4.05), color=RED, ms=12)
    cell(ax, 0.3, 3.7, 3.0, 0.75, PW, hot=True, fs=11.5)
    # 아래: 권한 없음
    box(ax, 0.3, 1.9, 3.0, 0.9, fc=PAPER)
    label(ax, 1.8, 2.35, "읽기 권한 없음", fs=10.5)
    arrow(ax, (3.4, 2.45), (4.95, 2.9), color=GREY, ms=12)
    arrow(ax, (4.95, 2.6), (3.4, 1.05), color=INK, ms=12)
    label(ax, 4.45, 1.6, "✗", fs=16, color=INK, bold=True)
    cell(ax, 0.3, 0.65, 3.0, 0.75, "Forbidden", fs=11, fc=LIGHT)
    save(fig, OUT, "k8s17-read.svg")


# ── 앱이 받아 쓰는 두 길 ───────────────────────────────────────────
def use():
    fig, ax = canvas(*S, *L)
    box(ax, 0.2, 3.3, 3.6, 1.5, fc=NOTE)
    label(ax, 2.0, 4.35, "Secret order-db", fs=11, bold=True)
    label(ax, 2.0, 3.75, f"password: {B64}", fs=8.5, color=INK, family=MONO)
    box(ax, 5.7, 0.9, 6.1, 5.0, fc="white")
    label(ax, 8.75, 5.55, "주문 처리 컨테이너", fs=11.5, bold=True)
    arrow(ax, (3.9, 4.4), (5.85, 4.4), color=INK, ms=12)
    label(ax, 4.6, 5.15, "① 환경 변수", fs=10, color=INK, bold=True)
    cell(ax, 5.95, 4.0, 2.65, 0.75, "DB_PASSWORD", fs=10.5, fc=LIGHT)
    cell(ax, 8.7, 4.0, 2.6, 0.75, PW, hot=True, fs=11)
    label(ax, 8.75, 3.45, "시작할 때 한 번", fs=10, color=INK)
    arrow(ax, (3.9, 3.5), (5.85, 2.5), color=INK, ms=12)
    label(ax, 4.4, 2.6, "② 파일", fs=10, color=INK, bold=True)
    cell(ax, 5.95, 2.15, 2.65, 0.7, "/etc/db/password", fs=10, fc=LIGHT)
    cell(ax, 8.7, 2.15, 2.6, 0.7, PW, hot=True, fs=11)
    label(ax, 8.75, 1.55, "Secret을 고치면 따라 바뀜", fs=10, color=INK)
    save(fig, OUT, "k8s17-use.svg")


S, L = (7.2, 3.8), (12, 6.6)

if __name__ == "__main__":
    opening()
    b64()
    b64table()
    compare()
    store()
    encrypt()
    read()
    use()
