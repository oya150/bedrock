"""쿠버네티스 18편 그림 만들기. 실행: python lab/fig_k8s18.py  → docs/kubernetes/img/18/*.svg

본문 절은 장면 띠로 그린다: 같은 무대를 여러 장 그리고 장마다 바뀐 곳만 빨강으로 칠한다.
예시는 17편을 잇는 빵집 주문 앱. 주문 처리 앱은 Secret order-db(주문 장부 비밀번호 croissant)만 읽으면 된다.
같은 곳에 admin-login(관리 화면 비밀번호), mail-key(주문 알림 메일 열쇠)도 있다. 값과 이름은 모두 지어낸 것.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "es"))
from figkit import (GREY, INK, LIGHT, NOTE, PAPER, PINK, RED, arrow, box, canvas, cell,  # noqa: E402
                    cylinder, label, moral, outdir, save, stage)
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
def opening(ax, step):
    rulecard(ax, [("list", "secrets")], hot=(step == 1))
    if step == 1:
        terminal(ax, [("$ kubectl get secrets", False, False)])
        label(ax, 10.05, 2.1, "목록만 보면 되겠지?", fs=10.5, color=RED)
    elif step == 2:
        terminal(ax, [("$ kubectl get secrets", False, False), ("NAME", False, False)]
                 + [(n, True, False) for n, _ in SECRETS])
        label(ax, 10.05, 2.1, "이름 셋이 보여요", fs=10.5, color=RED)
    else:
        lines = [("$ kubectl get secrets -o yaml", False, False)]
        for n, v in SECRETS:
            lines += [(f"- name: {n}", False, False), (f"  password: {v}", True, False)]
        terminal(ax, lines)
        label(ax, 10.05, 2.1, "값까지 셋 다 나왔어요", fs=10.5, color=RED, bold=True)
        moral(ax, 6.0, 0.35, "목록 권한 하나로 Secret 세 개의 값이 다 보였어요")


# ── 요청마다 확인하는 세 가지 ─────────────────────────────────────
API = (5.0, 3.6, 2.4, 1.4)


def request_card(ax, x, y, verb, target, hot=False, dim=False):
    ec = RED if hot else (GREY if dim else INK)
    c = RED if hot else (GREY if dim else "#222")
    box(ax, x, y, 4.2, 1.7, fc=PINK if hot else ("white" if dim else PAPER), ec=ec)
    label(ax, x + 0.2, y + 1.35, "누가: 주문 처리 앱", fs=10, ha="left", color=c)
    label(ax, x + 0.2, y + 0.85, f"무엇을: {verb}", fs=10, ha="left", color=c, bold=hot)
    label(ax, x + 0.2, y + 0.35, f"어디에: {target}", fs=10, ha="left", color=c, bold=hot)


def check(ax, step):
    request_card(ax, 0.3, 3.45, "get", "secrets / order-db", hot=(step == 1), dim=(step == 3))
    arrow(ax, (4.6, 4.3), (4.9, 4.3), color=RED if step == 1 else GREY, ms=12)
    box(ax, *API, fc=NOTE)
    label(ax, API[0] + API[2] / 2, API[1] + API[3] / 2, "API 서버", fs=12, bold=True)
    rulecard(ax, [("get", "secrets / order-db")], x=8.0, y=3.6, w=3.8, hot=(step == 2),
             title="허락한 일 목록 (Role)")
    ax.plot([7.5, 7.9], [4.3, 4.3], color=RED if step == 2 else GREY, lw=1.6, ls="--")
    if step == 2:
        label(ax, 9.9, 3.2, "목록에 같은 줄이 있나요?", fs=10.5, color=RED)
        label(ax, 6.2, 3.1, "✓ 통과", fs=13, color=RED, bold=True)
    if step == 3:
        request_card(ax, 0.3, 0.9, "get", "secrets / admin-login", hot=True)
        arrow(ax, (4.6, 1.75), (5.6, 3.5), color=RED, ms=12)
        label(ax, 6.6, 2.3, "✗ 목록에 없어서 거절", fs=12, color=RED, bold=True, ha="left")
        moral(ax, 8.4, 0.9, "적힌 일만 되고\n나머지는 모두 거절돼요", fs=11.5)


# ── 동사: get, list, watch ─────────────────────────────────────────
SX = [0.4, 4.3, 8.2]


def secret_box(ax, x, name, val, hot=False, dim=False, show=False):
    ec = RED if hot else (GREY if dim else INK)
    box(ax, x, 2.7, 3.4, 1.5, fc=PINK if hot else (LIGHT if dim else NOTE), ec=ec)
    c = RED if hot else (GREY if dim else "#222")
    label(ax, x + 1.7, 3.8, name, fs=11, bold=True, color=c)
    label(ax, x + 1.7, 3.15, val if show else "password: ……", fs=9.5, color=c, family=MONO)


def verbs(ax, step):
    titles = {1: "get order-db : 이름을 대고 하나", 2: "list : 전부 한꺼번에", 3: "watch : 바뀔 때마다 계속"}
    label(ax, 6.0, 5.9, titles[step], fs=12.5, color=RED, bold=True, family=None)
    for k, (n, v) in enumerate(SECRETS):
        on = (step == 1 and k == 0) or step >= 2
        secret_box(ax, SX[k], n, v, hot=on, dim=not on, show=on)
        if on:
            arrow(ax, (SX[k] + 1.7, 2.6), (SX[k] + 1.7, 1.7), color=RED, ms=12)
    label(ax, 6.0, 1.3, "돌려받는 것: 이름과 값", fs=11, color=RED)
    if step == 3:
        label(ax, 6.0, 4.75, "누가 값을 고치면 고친 값이 또 날아와요", fs=10.5, color=RED)
        moral(ax, 6.0, 0.5, "get · list · watch 모두 값까지 돌려줘요")


# ── 방 열쇠처럼 좁혀 주기 ─────────────────────────────────────────
def narrow(ax, step):
    rulecard(ax, [("list", "secrets")], x=0.3, y=4.3, w=4.0, title="처음 준 권한")
    ax.plot([0.4, 4.2], [4.4, 5.7], color=GREY, lw=1.5)
    arrow(ax, (4.5, 4.95), (5.3, 4.95), color=GREY if step > 1 else RED, ms=12)
    rulecard(ax, [("get", "secrets / order-db")], x=5.5, y=4.3, w=4.3, hot=(step == 1), title="새로 준 권한")
    if step == 1:
        label(ax, 7.65, 3.8, "동사 하나, 대상 하나, 이름 하나", fs=10.5, color=RED)
    else:
        rows = [("get order-db", "✓ Y3JvaXNzYW50", True), ("get admin-login", "✗ 거절", True),
                ("list (전부)", "✗ 거절", True)]
        for k, (a, b, hot) in enumerate(rows):
            y = 2.9 - k * 0.75
            cell(ax, 0.6, y, 3.6, 0.6, a, fs=10.5, fc=PAPER)
            arrow(ax, (4.3, y + 0.3), (5.2, y + 0.3), color=RED, ms=11)
            cell(ax, 5.3, y, 3.8, 0.6, b, hot=hot, fs=10.5)
        moral(ax, 6.0, 0.35, "주문 처리 앱은 주문 장부 비밀번호만 열어요")


# ── 데이터베이스에서도 똑같아요 ───────────────────────────────────
DBS = [("orders", "주문 장부"), ("recipes", "레시피 장부"), ("mysql", "계정 목록 (시스템)")]
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
            arrow(ax, (DBX[k] + 1.8, 5.3), (DBX[k] + 1.8, 4.5), color=RED if on else GREY, ms=12)
        if no:
            label(ax, DBX[k] + 1.8, 4.85, "✗", fs=15, color=RED, bold=True)
    if hash_hot is not None and 2 in read:
        c = RED if hash_hot else INK
        box(ax, 8.2, 0.75, 3.6, 1.2, fc=PINK if hash_hot else "white", ec=c)
        label(ax, 10.0, 1.6, "user        비밀번호 해시", fs=9.5, color=c)
        label(ax, 10.0, 1.1, "baker       9f2c…e1", fs=9.5, color=c, family=MONO)


def db(ax, step):
    if step == 1:
        db_stage(ax, "모든 데이터베이스 읽기 (*.*)", read=(0, 1, 2), hot_grant=True, hash_hot=False)
    elif step == 2:
        db_stage(ax, "모든 데이터베이스 읽기 (*.*)", read=(0, 1, 2), hash_hot=True)
        label(ax, 4.0, 1.35, "다른 계정들의 비밀번호 해시까지\n읽혀요", fs=10.5, color=RED)
    else:
        db_stage(ax, "orders만 읽기 (orders.*)", read=(0,), deny=(1, 2), hot_grant=True, hash_hot=None)
        moral(ax, 6.0, 0.9, "필요한 데이터베이스 하나만 열어 줘요")


# ── 판단 (한 장) ───────────────────────────────────────────────────
def decide():
    fig, ax = canvas(10, 4.2, 15, 6.4)
    box(ax, 0.3, 4.6, 6.0, 1.3, fc=NOTE)
    label(ax, 3.3, 5.25, "이 권한이 없으면 일이 멈추나요?", fs=10.5, bold=True)
    arrow(ax, (6.4, 5.25), (8.4, 5.25)); label(ax, 7.4, 5.55, "아니요", fs=10, color=INK)
    box(ax, 8.5, 4.6, 6.2, 1.3, fc=PAPER)
    label(ax, 11.6, 5.25, "주지 않아요", fs=10.5)
    arrow(ax, (3.3, 4.5), (3.3, 3.5)); label(ax, 3.6, 4.0, "예", fs=10, color=INK, ha="left")
    box(ax, 0.3, 2.2, 6.0, 1.2, fc=NOTE)
    label(ax, 3.3, 2.8, "어느 것이 필요한지 이름을 아나요?", fs=10.5, bold=True)
    arrow(ax, (6.4, 2.8), (8.4, 2.8)); label(ax, 7.4, 3.1, "예", fs=10, color=RED)
    box(ax, 8.5, 2.2, 6.2, 1.2, fc=PINK, ec=RED)
    label(ax, 11.6, 2.8, "get + 그 이름만", fs=10.5, color=RED, bold=True)
    arrow(ax, (3.3, 2.1), (3.3, 1.3)); label(ax, 3.6, 1.7, "아니요, 늘 전부 지켜봐야 해요", fs=10, color=INK, ha="left")
    box(ax, 0.3, 0.1, 6.0, 1.1, fc=PAPER)
    label(ax, 3.3, 0.65, "그 종류에만 list · watch", fs=10.5)
    save(fig, OUT, "k8s18-decide.svg")


# ── 정리: 처음 장면으로 돌아가기 ───────────────────────────────────
def back(ax, step):
    if step == 1:
        rulecard(ax, [("list", "secrets")], title="처음 준 권한")
        lines = [("$ kubectl get secrets -o yaml", False, True)]
        for n, v in SECRETS:
            lines += [(f"- name: {n}", False, True), (f"  password: {v}", False, True)]
        terminal(ax, lines)
        label(ax, 10.05, 2.1, "처음: 셋 다 보였어요", fs=10.5, color=INK)
    elif step == 2:
        rulecard(ax, [("get", "secrets / order-db")], w=3.6, hot=True, title="새로 준 권한")
        terminal(ax, [("$ kubectl get secret order-db -o yaml", False, False), ("data:", False, False),
                      ("  password: Y3JvaXNzYW50", True, False)])
        label(ax, 10.05, 1.5, "주문 장부 비밀번호 하나", fs=10.5, color=RED)
    else:
        rulecard(ax, [("get", "secrets / order-db")], w=3.6, title="새로 준 권한")
        terminal(ax, [("$ kubectl get secret order-db -o yaml", False, True), ("data:", False, True),
                      ("  password: Y3JvaXNzYW50", False, True), ("", False, False),
                      ("$ kubectl get secrets -o yaml", False, False),
                      ("Error from server (Forbidden)", True, False)])
        label(ax, 10.05, 1.5, "목록은 거절돼요", fs=10.5, color=RED, bold=True)
        moral(ax, 6.0, 0.35, "방 열쇠 하나로는 그 방만 열려요")


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

    x, y = card(0, "RBAC", "누가 무엇을 어디에 할지\n허락을 적어 두는 방식")
    cell(ax, x + 0.3, y + 1.6, 4.0, 0.8, "get  secrets / order-db", hot=True, fs=10)
    x, y = card(1, "최소 권한", "일에 꼭 필요한 만큼만\n권한을 주는 원칙")
    cell(ax, x + 0.3, y + 1.6, 1.9, 0.8, "만능 열쇠", fc=LIGHT, fs=10)
    arrow(ax, (x + 2.3, y + 2.0), (x + 2.7, y + 2.0), color=RED, ms=11)
    cell(ax, x + 2.8, y + 1.6, 1.5, 0.8, "방 열쇠", hot=True, fs=10)
    x, y = card(2, "동사", "무엇을 할지\nget · list · watch …")
    for k, v in enumerate(["get", "list", "watch"]):
        cell(ax, x + 0.3 + k * 1.35, y + 1.6, 1.2, 0.8, v, hot=(k == 0), fs=10.5)
    x, y = card(3, "대상", "어디에 할지\n물건 종류와 이름")
    cell(ax, x + 0.3, y + 1.6, 1.8, 0.8, "secrets", fs=10.5)
    cell(ax, x + 2.2, y + 1.6, 2.1, 0.8, "order-db", hot=True, fs=10.5)
    save(fig, OUT, "k8s18-cards.svg")


if __name__ == "__main__":
    S, L = (7.2, 3.8), (12, 6.6)
    stage(opening, 3, OUT, "k8s18-open", S, L)
    stage(check, 3, OUT, "k8s18-check", S, L)
    stage(verbs, 3, OUT, "k8s18-verbs", S, L)
    stage(narrow, 2, OUT, "k8s18-narrow", S, L)
    stage(db, 3, OUT, "k8s18-db", S, L)
    decide()
    stage(back, 3, OUT, "k8s18-back", S, L)
    cards()
