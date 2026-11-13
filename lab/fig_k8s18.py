"""쿠버네티스 18편 그림 만들기. 실행: python lab/fig_k8s18.py  → docs/kubernetes/img/18/*.svg

그림 하나가 한 장면. 그림 안에는 낱말과 숫자만 두고 지금 볼 곳만 빨강으로 칠한다.
예시는 17편을 잇는 빵집 주문 앱. 주문 처리 앱은 Secret order-db(주문 장부 비밀번호 croissant)만 읽으면 된다.
같은 곳에 admin-login(관리 화면 비밀번호), mail-key(주문 알림 메일 열쇠)도 있다. 값과 이름은 모두 지어낸 것.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "es"))
from figkit import (GREY, INK, LIGHT, NOTE, PAPER, PINK, RED, arrow, box, canvas, cell,  # noqa: E402
                    cylinder, label, outdir, save)
from matplotlib.patches import Rectangle  # noqa: E402

OUT = outdir("18", topic="kubernetes")
MONO = "monospace"
SECRETS = [("order-db", "Y3JvaXNzYW50"), ("admin-login", "YmFndWV0dGU="), ("mail-key", "bWFkZWxlaW5l")]


def terminal(ax, lines, x=0.3, y=0.9, w=7.6, h=5.3):
    box(ax, x, y, w, h, fc="white", round_=False)
    ax.add_patch(Rectangle((x, y + h - 0.45), w, 0.45, fc=LIGHT, ec=INK, lw=1.2))
    label(ax, x + 0.2, y + h - 0.22, "터미널", fs=10.5, ha="left", color=INK)
    for k, (s, hot, dim) in enumerate(lines):
        yy = y + h - 0.85 - k * 0.5
        c = RED if hot else (GREY if dim else "#222")
        label(ax, x + 0.25, yy, s, fs=10.5, ha="left", color=c, bold=hot, family=MONO if s.isascii() else None)


def rulecard(ax, rows, x=8.3, y=2.6, w=3.5, hot=False, title="주문 처리 앱의 권한"):
    """rows=[(동사, 대상)]"""
    h = 0.9 + 0.6 * len(rows)
    box(ax, x, y, w, h, fc=PINK if hot else NOTE, ec=RED if hot else INK)
    label(ax, x + w / 2, y + h - 0.35, title, fs=10.5, bold=True, color=RED if hot else "#222")
    for k, (v, t) in enumerate(rows):
        yy = y + h - 0.9 - k * 0.6
        label(ax, x + 0.25, yy, v, fs=10.5, ha="left", color=RED if hot else "#222", bold=True)
        label(ax, x + 0.95, yy, t, fs=10, ha="left", color=RED if hot else "#222")


# ── 여는 장면: 목록만 보려 했는데 값이 다 나왔어요 ─────────────────
def opening():
    fig, ax = canvas(*S, *L)
    rulecard(ax, [("list", "secrets")])
    lines = [("$ kubectl get secrets -o yaml", False, False)]
    for n, v in SECRETS:
        lines += [(f"- name: {n}", False, False), (f"  password: {v}", True, False)]
    terminal(ax, lines)
    save(fig, OUT, "k8s18-open.svg")


# ── 요청마다 확인하는 세 가지 ─────────────────────────────────────
API = (5.0, 3.6, 2.4, 1.4)


def request_card(ax, x, y, verb, target, hot=False):
    ec = RED if hot else INK
    c = RED if hot else "#222"
    box(ax, x, y, 4.2, 1.7, fc=PINK if hot else PAPER, ec=ec)
    label(ax, x + 0.2, y + 1.35, "누가: 주문 처리 앱", fs=10, ha="left", color=c)
    label(ax, x + 0.2, y + 0.85, f"무엇을: {verb}", fs=10, ha="left", color=c, bold=True)
    label(ax, x + 0.2, y + 0.35, f"어디에: {target}", fs=10, ha="left", color=c, bold=True)


def check():
    fig, ax = canvas(*S, *L)
    request_card(ax, 0.3, 3.45, "get", "secrets / order-db")
    arrow(ax, (4.6, 4.3), (4.9, 4.3), color=INK, ms=12)
    box(ax, *API, fc=NOTE)
    label(ax, API[0] + API[2] / 2, API[1] + API[3] / 2, "API 서버", fs=12, bold=True)
    rulecard(ax, [("get", "secrets / order-db")], x=8.0, y=3.6, w=3.8, title="허락한 일 목록 (Role)")
    ax.plot([7.5, 7.9], [4.3, 4.3], color=INK, lw=1.6, ls="--")
    label(ax, 6.2, 5.4, "✓ 통과", fs=13, color=INK, bold=True)
    request_card(ax, 0.3, 0.9, "get", "secrets / admin-login", hot=True)
    arrow(ax, (4.6, 1.75), (5.6, 3.5), color=RED, ms=12)
    label(ax, 6.3, 2.3, "✗ 거절", fs=13, color=RED, bold=True, ha="left")
    save(fig, OUT, "k8s18-check.svg")


# ── 동사: get, list ───────────────────────────────────────────────
SX = [3.1, 6.05, 9.0]


def secret_box(ax, x, y, name, val, hot=False, dim=False):
    ec = RED if hot else (GREY if dim else INK)
    box(ax, x, y, 2.7, 1.5, fc=PINK if hot else (LIGHT if dim else NOTE), ec=ec)
    c = RED if hot else (GREY if dim else "#222")
    label(ax, x + 1.35, y + 1.05, name, fs=10.5, bold=True, color=c)
    label(ax, x + 1.35, y + 0.45, val if hot else "……", fs=10, color=c, family=MONO)


def verbs():
    fig, ax = canvas(*S, *L)
    for row, (verb, y) in enumerate([("get order-db", 3.9), ("list", 1.2)]):
        label(ax, 0.3, y + 0.75, verb, fs=11, ha="left", bold=True, family=MONO)
        for k, (n, v) in enumerate(SECRETS):
            on = row == 1 or k == 0
            secret_box(ax, SX[k], y, n, v, hot=on, dim=not on)
    ax.plot([0.3, 11.8], [3.3, 3.3], color=LIGHT, lw=1.2)
    save(fig, OUT, "k8s18-verbs.svg")


# ── 방 열쇠처럼 좁혀 주기 ─────────────────────────────────────────
def narrow():
    fig, ax = canvas(*S, *L)
    rulecard(ax, [("list", "secrets")], x=0.3, y=4.3, w=4.0, title="처음 준 권한")
    ax.plot([0.4, 4.2], [4.4, 5.7], color=GREY, lw=1.5)
    arrow(ax, (4.5, 4.95), (5.3, 4.95), color=INK, ms=12)
    rulecard(ax, [("get", "secrets / order-db")], x=5.5, y=4.3, w=4.3, title="새로 준 권한")
    rows = [("get order-db", "✓ Y3JvaXNzYW50", True), ("get admin-login", "✗ 거절", False),
            ("list (전부)", "✗ 거절", False)]
    for k, (a, b, hot) in enumerate(rows):
        y = 2.9 - k * 0.85
        cell(ax, 0.6, y, 3.6, 0.6, a, fs=10.5, fc=PAPER)
        arrow(ax, (4.3, y + 0.3), (5.2, y + 0.3), color=RED if hot else INK, ms=11)
        cell(ax, 5.3, y, 3.8, 0.6, b, hot=hot, fs=10.5, fc=None if hot else LIGHT)
    save(fig, OUT, "k8s18-narrow.svg")


# ── 데이터베이스에서도 똑같아요 ───────────────────────────────────
DBS = [("orders", "주문 장부"), ("recipes", "레시피 장부"), ("mysql", "계정 목록")]
DBX = [0.3, 4.2, 8.1]


def db_stage(ax, grant, read=(), deny=(), hot_grant=False, hash_hot=False):
    box(ax, 0.3, 5.4, 6.2, 0.75, fc=PINK if hot_grant else NOTE, ec=RED if hot_grant else INK)
    label(ax, 0.5, 5.77, f"복제용 계정: {grant}", fs=10.5, ha="left", color=RED if hot_grant else "#222",
          bold=hot_grant)
    for k, (n, desc) in enumerate(DBS):
        on, no = k in read and hot_grant, k in deny
        cylinder(ax, DBX[k] + 0.4, 2.4, 2.8, 1.4, n, ec=RED if on else INK, color=RED if on else "#222")
        label(ax, DBX[k] + 1.8, 3.1, desc, fs=10, color=RED if on else INK)
        if k in read:
            arrow(ax, (DBX[k] + 1.8, 5.3), (DBX[k] + 1.8, 4.5), color=RED if on else INK, ms=12)
        if no:
            label(ax, DBX[k] + 1.8, 4.85, "✗", fs=15, color=RED, bold=True)
    if hash_hot is not None and 2 in read:
        c = RED if hash_hot else INK
        box(ax, 8.2, 0.75, 3.6, 1.2, fc=PINK if hash_hot else "white", ec=c)
        label(ax, 10.0, 1.6, "user        비밀번호 해시", fs=9.5, color=c)
        label(ax, 10.0, 1.1, "baker       9f2c…e1", fs=9.5, color=c, family=MONO)


def db_wide():
    fig, ax = canvas(*S, *L)
    db_stage(ax, "모든 데이터베이스 읽기 (*.*)", read=(0, 1, 2), hash_hot=True)
    save(fig, OUT, "k8s18-db-wide.svg")


def db_narrow():
    fig, ax = canvas(*S, *L)
    db_stage(ax, "orders만 읽기 (orders.*)", read=(0,), deny=(1, 2), hot_grant=True, hash_hot=None)
    save(fig, OUT, "k8s18-db-narrow.svg")


# ── 판단 (한 장) ───────────────────────────────────────────────────
def decide():
    fig, ax = canvas(10, 4.2, 15, 6.4)
    box(ax, 0.3, 4.6, 6.0, 1.3, fc=NOTE)
    label(ax, 3.3, 5.25, "없으면 일이 멈춤?", fs=11, bold=True)
    arrow(ax, (6.4, 5.25), (8.4, 5.25)); label(ax, 7.4, 5.55, "아니요", fs=10, color=INK)
    box(ax, 8.5, 4.6, 6.2, 1.3, fc=PAPER)
    label(ax, 11.6, 5.25, "주지 않기", fs=11)
    arrow(ax, (3.3, 4.5), (3.3, 3.5)); label(ax, 3.6, 4.0, "예", fs=10, color=INK, ha="left")
    box(ax, 0.3, 2.2, 6.0, 1.2, fc=NOTE)
    label(ax, 3.3, 2.8, "필요한 이름을 앎?", fs=11, bold=True)
    arrow(ax, (6.4, 2.8), (8.4, 2.8), color=RED); label(ax, 7.4, 3.1, "예", fs=10, color=RED)
    box(ax, 8.5, 2.2, 6.2, 1.2, fc=PINK, ec=RED)
    label(ax, 11.6, 2.8, "get + 그 이름", fs=11, color=RED, bold=True)
    arrow(ax, (3.3, 2.1), (3.3, 1.3)); label(ax, 3.6, 1.7, "아니요 (늘 전부 지켜봄)", fs=10, color=INK, ha="left")
    box(ax, 0.3, 0.1, 6.0, 1.1, fc=PAPER)
    label(ax, 3.3, 0.65, "그 종류에만 list · watch", fs=11)
    save(fig, OUT, "k8s18-decide.svg")


S, L = (7.2, 3.8), (12, 6.6)

if __name__ == "__main__":
    opening()
    check()
    verbs()
    narrow()
    db_wide()
    db_narrow()
    decide()
