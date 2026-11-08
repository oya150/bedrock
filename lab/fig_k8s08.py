"""쿠버네티스 8편 그림 만들기. 실행: python lab/fig_k8s08.py  → docs/kubernetes/img/08/*.svg

본문 절은 장면 띠로 그린다: 같은 무대를 여러 장 그리고 장마다 바뀐 곳만 빨강으로 칠한다.
예시는 7편의 주문 처리 Deployment order를 잇는다. 마감 시간 환경 변수 CLOSE_TIME 을 21:00 → 22:00 으로 바꾼다.
옛 틀의 지문 7c9d, 새 틀의 지문 5f8b.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "es"))
sys.path.insert(0, os.path.dirname(__file__))
from figkit import (GREY, INK, LIGHT, NOTE, PAPER, PINK, RED, arrow, box, bubble,  # noqa: E402
                    canvas, label, moral, outdir, save, stage)
from matplotlib.patches import Rectangle  # noqa: E402
from fig_k8s07 import MONO, pod, terminal  # noqa: E402

OUT = outdir("08", topic="kubernetes")
OLD = ["order-7c9d-m8x1z", "order-7c9d-t5r7v", "order-7c9d-w8n3m"]
NEW = ["order-5f8b-a3k9d", "order-5f8b-h6q2s", "order-5f8b-z7c4p"]


def code(ax, x, y, s, hot=False, dim=False, fs=10.5):
    ax.text(x, y, s, fontsize=fs, family=MONO, ha="left", va="center",
            color=RED if hot else (GREY if dim else "#222"), fontweight="bold" if hot else "normal")


def deploy_doc(ax, x=0.3, y=1.0, w=4.6, replicas="3", close="21:00", hot=(), tpl_hot=False, tpl_label=True):
    """Deployment 매니페스트. hot 은 'replicas'·'image'·'env'·'hosts' 중에서."""
    h = 4.9
    ax.add_patch(Rectangle((x, y), w, h, fc="white", ec=INK, lw=1.5))
    ax.plot([x + w - 0.35, x + w], [y + h, y + h - 0.35], color=INK, lw=1.2)
    label(ax, x + 0.15, y + h + 0.22, "order.yaml", fs=10, ha="left", color=INK)
    rows = [("kind: Deployment", None), ("name: order", None), (f"replicas: {replicas}", "replicas")]
    ty = y + h - 0.45
    for s, key in rows:
        on = key in hot
        if on:
            ax.add_patch(Rectangle((x + 0.08, ty - 0.2), w - 0.16, 0.4, fc=PINK, ec=RED, lw=1.3))
        code(ax, x + 0.2, ty, s, hot=on)
        ty -= 0.48
    code(ax, x + 0.2, ty, "template:")
    ty -= 0.3
    # 틀 상자
    tx, tw, th = x + 0.3, w - 0.5, 1.75
    ax.add_patch(Rectangle((tx, ty - th), tw, th, fc=PINK if tpl_hot else PAPER, ec=RED if tpl_hot else INK,
                           lw=2.0 if tpl_hot else 1.2, ls="-"))
    if tpl_label:
        label(ax, tx + tw, ty - th - 0.28, "파드 템플릿", fs=10.5, ha="right", color=RED if tpl_hot else INK, bold=tpl_hot)
    ry = ty - 0.35
    for s, key in (("image: order:1", "image"), (f"env: CLOSE_TIME={close}", "env"), ("hostAliases: ledger", "hosts")):
        on = key in hot
        if on:
            ax.add_patch(Rectangle((tx + 0.06, ry - 0.2), tw - 0.12, 0.4, fc=PINK, ec=RED, lw=1.3))
        code(ax, tx + 0.15, ry, s, hot=on, fs=10)
        ry -= 0.52
    return tx, ty - th, tw, th


def rs(ax, x, y, name, pods, hot=False, dim=False, w=6.2, note=None):
    """ReplicaSet 상자와 안의 파드들(한 줄에 3개). pods=[(이름, 상태)] 상태 ""·"hot"·"gone". y는 상자 아래."""
    rows = max(1, (len(pods) + 2) // 3)
    h = 0.55 + 0.9 * rows
    ec = RED if hot else (GREY if dim else INK)
    ax.add_patch(Rectangle((x, y), w, h, fc="white", ec=ec, lw=2.0 if hot else 1.3))
    label(ax, x + 0.15, y + h - 0.25, f"ReplicaSet {name}", fs=10, ha="left", color=ec, bold=hot)
    if note:
        label(ax, x + w - 0.15, y + h - 0.25, note, fs=10, ha="right", color=ec, bold=hot)
    for k, (nm, st) in enumerate(pods):
        px = x + 0.2 + (k % 3) * 2.0
        py = y + h - 1.25 - (k // 3) * 0.9
        pod(ax, px, py, nm, hot=st == "hot", gone=st == "gone", dim=dim, w=1.8, h=0.7, fs=7.8)


# ── 여는 장면 ──────────────────────────────────────────────────────
def opening(ax, step):
    if step == 1:
        deploy_doc(ax, close="22:00", hot=("env",), tpl_label=False)
        label(ax, 5.4, 3.75, "21:00 → 22:00\n한 줄만 바꿨어요", fs=11.5, color=RED, bold=True, ha="left")
        terminal(ax, 5.4, 1.0, 6.3, 1.9, [("$ kubectl apply -f order.yaml", "cmd"), ("deployment.apps/order configured", "")])
    elif step == 2:
        lines = [("$ kubectl get pods", "cmd"), ("NAME                READY   AGE", ""),
                 (f"{OLD[1]}    1/1     2d", ""), (f"{OLD[2]}    1/1     2d", ""), (f"{NEW[0]}    1/1     8s", "hot")]
        terminal(ax, 0.3, 1.6, 11.4, 3.9, lines)
        label(ax, 6.0, 0.8, "조금 뒤: 낯선 이름의 파드가 하나 생기고 옛 파드 하나가 사라졌어요", fs=11.5, color=RED)
    else:
        lines = [("$ kubectl get pods", "cmd"), ("NAME                READY   AGE", ""),
                 (f"{NEW[0]}    1/1     40s", "hot"), (f"{NEW[1]}    1/1     25s", "hot"), (f"{NEW[2]}    1/1     9s", "hot")]
        terminal(ax, 0.3, 1.6, 11.4, 3.9, lines)
        moral(ax, 6.0, 0.8, "한 줄 바꿨는데 3개가 모두 새 파드예요")


# ── 파드 템플릿 ────────────────────────────────────────────────────
def template(ax, step):
    tx, ty, tw, th = deploy_doc(ax, tpl_hot=step == 1)
    if step == 1:
        label(ax, 5.5, 4.4, "파드를 찍어 내는 틀", fs=11.5, color=RED, bold=True, ha="left")
        label(ax, 5.5, 5.2, "replicas는 틀 밖에 있어요", fs=11, color=INK, ha="left")
        arrow(ax, (5.4, 5.2), (3.0, 4.5), color=GREY, ms=12)
    else:
        for k in range(3):
            arrow(ax, (tx + tw + 0.1, ty + th / 2), (6.6, 4.6 - k * 1.2), color=RED, ms=13)
            pod(ax, 6.7, 4.2 - k * 1.2, OLD[k], hot=True, w=2.6, fs=9.5)
        label(ax, 9.35, 5.3, "틀 하나로 3개를 똑같이", fs=11, color=RED, bold=True)
        moral(ax, 6.0, 0.25, "파드는 모두 틀에 적힌 대로 만들어져요")


# ── 지문(해시) ─────────────────────────────────────────────────────
def finger(ax, x, y, s, hot=False, note=None):
    box(ax, x, y, 2.0, 0.9, fc=PINK if hot else NOTE, ec=RED if hot else INK)
    label(ax, x + 1.0, y + 1.15, "지문", fs=10, color=RED if hot else INK)
    label(ax, x + 1.0, y + 0.45, s, fs=14, family=MONO, color=RED if hot else "#222", bold=True)
    if note:
        label(ax, x + 1.0, y - 0.3, note, fs=10, color=RED if hot else INK, bold=hot)


def hashing(ax, step):
    close = "21:00" if step == 1 else "22:00"
    tx, ty, tw, th = deploy_doc(ax, close=close, hot=("env",) if step == 2 else ())
    fp = "7c9d" if step == 1 else "5f8b"
    arrow(ax, (tx + tw + 0.1, ty + th / 2), (5.55, 4.85), color=RED if step < 3 else GREY, ms=13)
    finger(ax, 5.6, 4.4, fp, hot=step < 3)
    rs(ax, 5.5, 2.2, "order-7c9d", [(n, "") for n in OLD])
    if step == 1:
        label(ax, 8.1, 5.0, "틀 전체를 짧게 줄인 글자", fs=10.5, color=RED, ha="left")
        arrow(ax, (6.6, 4.35), (6.6, 3.7), color=GREY, ms=11)
        label(ax, 6.8, 3.95, "이 지문의 파드 묶음", fs=10, color=INK, ha="left")
    elif step == 2:
        label(ax, 8.1, 5.0, "한 줄만 달라져도\n지문이 통째로 바뀌어요", fs=10.5, color=RED, ha="left", bold=True)
    else:
        rs(ax, 5.5, 0.55, "order-5f8b", [], hot=True, note="파드 0개")
        label(ax, 8.1, 5.0, "지문 5f8b의 묶음이\n아래에 새로 생겨요", fs=10.5, color=INK, ha="left")
        moral(ax, 6.0, 0.05, "새 지문으로 새 묶음이 생겨요")


# ── 대수만 바꾸면 ──────────────────────────────────────────────────
def scale(ax, step):
    tx, ty, tw, th = deploy_doc(ax, replicas="5", hot=("replicas",) if step == 1 else ())
    arrow(ax, (tx + tw + 0.1, ty + th / 2), (5.55, 4.85), color=GREY, ms=13)
    finger(ax, 5.6, 4.4, "7c9d", note="그대로" if step == 1 else None, hot=False)
    pods = [(n, "") for n in OLD]
    if step == 1:
        label(ax, 8.0, 5.0, "틀 밖의 replicas만\n3 → 5로 바꿨어요", fs=10.5, color=RED, ha="left", bold=True)
        rs(ax, 5.5, 2.2, "order-7c9d", pods)
    else:
        rs(ax, 5.5, 1.3, "order-7c9d", pods + [("order-7c9d-b4n6r", "hot"), ("order-7c9d-q1w8e", "hot")])
        moral(ax, 6.0, 0.4, "지문이 그대로라 같은 묶음에 2개만 더해요. 옛 파드는 그대로예요")


def where():
    fig, ax = canvas(7.6, 3.6, 15, 7.2)
    head = [("바꾼 칸", 1.9), ("틀 안?", 6.0), ("지문", 8.6), ("파드는", 12.2)]
    for s, x in head:
        label(ax, x, 6.7, s, fs=11, bold=True, color=INK)
    ax.plot([0.3, 14.7], [6.35, 6.35], color=INK, lw=1.0)
    rows = [("env: CLOSE_TIME", "안", "7c9d → 5f8b", "전부 교대해요", True),
            ("hostAliases", "안", "7c9d → 5f8b", "전부 교대해요", True),
            ("image", "안", "7c9d → 5f8b", "전부 교대해요", True),
            ("replicas", "밖", "7c9d 그대로", "개수만 맞춰요", False)]
    for k, (a, b, c, d, hot) in enumerate(rows):
        y = 5.6 - k * 1.45
        if hot:
            ax.add_patch(Rectangle((0.3, y - 0.55), 14.4, 1.1, fc=PINK, ec="none"))
        code(ax, 0.5, y, a, hot=hot, fs=10.5)
        label(ax, 6.0, y, b, fs=11.5, color=RED if hot else "#222", bold=hot)
        label(ax, 8.6, y, c, fs=11, color=RED if hot else "#222", family=MONO)
        label(ax, 12.2, y, d, fs=11, color=RED if hot else "#222", bold=hot)
    save(fig, OUT, "k8s08-where.svg")


# ── 롤링 업데이트 ──────────────────────────────────────────────────
def counter(ax, ready, total, hot=False):
    box(ax, 9.3, 4.75, 2.4, 1.45, fc=PINK if hot else NOTE, ec=RED if hot else INK)
    label(ax, 10.5, 5.75, f"일하는 파드 {ready}개", fs=10.5, color=RED if hot else "#222", bold=hot)
    label(ax, 10.5, 5.2, f"모두 {total}개", fs=10.5, color=RED if hot else "#222")


def roll(ax, step):
    o = [(n, "") for n in OLD]
    n = []
    if step == 1:
        label(ax, 0.3, 5.5, "시작: 옛 틀의 파드 3개가 주문을 받아요", fs=11, ha="left", color=INK)
        counter(ax, 3, 3)
    elif step == 2:
        n = [(NEW[0], "wait")]
        label(ax, 0.3, 5.5, "① 새 틀로 파드 하나를 먼저 띄워요", fs=11, ha="left", color=RED, bold=True)
        counter(ax, 3, 4, hot=True)
    elif step == 3:
        o = [(OLD[0], "gone")] + o[1:]
        n = [(NEW[0], "")]
        label(ax, 0.3, 5.5, "② 새 파드가 준비되면 옛 파드 하나를 내려요", fs=11, ha="left", color=RED, bold=True)
        counter(ax, 3, 3)
    elif step == 4:
        o = [("", "none")] + [(OLD[1], "gone"), (OLD[2], "")]
        n = [(NEW[0], ""), (NEW[1], "hot")]
        label(ax, 0.3, 5.5, "③ 같은 일을 한 번 더: 새 파드 하나 뜨고 옛 파드 하나 내려요", fs=11, ha="left", color=RED,
              bold=True)
        counter(ax, 3, 3)
    else:
        o = []
        n = [(NEW[0], ""), (NEW[1], ""), (NEW[2], "hot")]
        label(ax, 0.3, 5.5, "④ 마지막 하나까지 바꿔 끼웠어요", fs=11, ha="left", color=RED, bold=True)
        counter(ax, 3, 3)
    o = [p for p in o if p[1] != "none"] if step != 4 else o
    # 옛 묶음
    x0 = 0.3
    ax.add_patch(Rectangle((x0, 2.85), 6.3, 1.45, fc="white", ec=GREY if step == 5 else INK, lw=1.3))
    label(ax, x0 + 0.15, 4.05, "ReplicaSet order-7c9d (옛 틀)", fs=10, ha="left", color=GREY if step == 5 else INK)
    for k, (nm, st) in enumerate(o):
        if st == "none":
            continue
        pod(ax, x0 + 0.15 + k * 2.05, 3.0, nm, gone=st == "gone", w=1.9, fs=7.8)
    if step == 5:
        label(ax, x0 + 3.15, 3.4, "파드 0개 (지우지 않고 남겨 둬요)", fs=10, color=GREY)
    # 새 묶음
    ax.add_patch(Rectangle((x0, 0.9), 6.3, 1.45, fc="white", ec=INK, lw=1.3))
    label(ax, x0 + 0.15, 2.1, "ReplicaSet order-5f8b (새 틀)", fs=10, ha="left", color=INK)
    for k, (nm, st) in enumerate(n):
        px = x0 + 0.15 + k * 2.05
        if st == "wait":
            ax.add_patch(Rectangle((px, 1.05), 1.9, 0.75, fc=PINK, ec=RED, lw=1.6, ls="--"))
            label(ax, px + 0.95, 1.43, f"{nm}\n준비 중", fs=7.5, color=RED)
        else:
            pod(ax, px, 1.05, nm, hot=st == "hot", w=1.9, fs=7.8)
    if step == 5:
        moral(ax, 6.0, 0.25, "교대하는 내내 주문을 받는 파드는 3개 아래로 내려가지 않았어요")


# ── 갈림길 ─────────────────────────────────────────────────────────
def decide():
    fig, ax = canvas(7.6, 4.6, 15, 9)
    box(ax, 0.3, 7.4, 8.4, 1.2, fc=NOTE)
    label(ax, 4.5, 8.0, "바꾸려는 칸이 파드 템플릿 안에 있나요?", fs=11, bold=True)
    arrow(ax, (8.8, 8.0), (10.0, 8.0)); label(ax, 9.4, 8.35, "아니요", fs=10, color=INK)
    box(ax, 10.1, 7.2, 4.6, 1.6, fc=PAPER)
    label(ax, 12.4, 8.0, "교대 없이 바뀌어요\n(replicas는 개수만)", fs=10.5)
    arrow(ax, (4.5, 7.3), (4.5, 6.1), color=RED); label(ax, 4.8, 6.7, "예", fs=10, color=RED, ha="left")
    box(ax, 0.3, 4.6, 8.4, 1.4, fc=PINK, ec=RED)
    label(ax, 4.5, 5.3, "파드가 전부 새로 떠요 (롤링 업데이트)\n교대하는 동안 버틸 준비가 됐나요?", fs=10.5, color=RED, bold=True)
    arrow(ax, (4.5, 4.5), (4.5, 3.3)); label(ax, 4.8, 3.9, "그전에 볼 것", fs=10, color=INK, ha="left")
    box(ax, 0.3, 1.0, 8.4, 2.2, fc=NOTE)
    label(ax, 4.5, 2.1, "새 파드가 뜨는 동안 노드에 한 개 더 띄울 자리\n새 파드가 준비됐는지 알리는 확인\n여러 칸을 바꿀 거면 한 번에 모아서", fs=10.5)
    arrow(ax, (12.4, 7.1), (12.4, 6.3)); label(ax, 12.6, 6.7, "단,", fs=10, color=INK, ha="left")
    box(ax, 10.1, 3.8, 4.6, 2.4, fc=PAPER)
    label(ax, 12.4, 5.0, "틀 밖에서 읽는 값\n(ConfigMap 내용)을 바꿨나요?\n→ 파드는 모르니\n다시 띄워야 해요", fs=10)
    save(fig, OUT, "k8s08-decide.svg")


# ── 정리 ───────────────────────────────────────────────────────────
def back(ax, step):
    if step == 1:
        lines = [("$ kubectl apply -f order.yaml   # CLOSE_TIME=22:00", "dim"), ("$ kubectl get pods", "dim"),
                 (f"{NEW[0]}    1/1     40s", "dim"), (f"{NEW[1]}    1/1     25s", "dim"), (f"{NEW[2]}    1/1     9s", "dim")]
        terminal(ax, 0.3, 1.6, 11.4, 3.9, lines)
        label(ax, 6.0, 0.8, "처음: 한 줄 바꿨더니 파드 3개가 모두 새 이름이 됐어요", fs=11.5, color=INK)
    elif step == 2:
        lines = [("$ kubectl get replicasets", "cmd"), ("NAME          DESIRED   READY", ""),
                 ("order-7c9d    0         0", ""), ("order-5f8b    3         3", "hot")]
        terminal(ax, 0.3, 1.6, 11.4, 3.9, lines)
        moral(ax, 6.0, 0.8, "이름 가운데 7c9d와 5f8b가 틀의 지문이에요. 틀이 바뀌어 묶음이 바뀌었어요")
    else:
        lines = [("$ kubectl scale deployment order --replicas=5", "cmd"), ("$ kubectl get pods", "cmd"),
                 (f"{NEW[0]}    1/1     10m", ""), (f"{NEW[1]}    1/1     10m", ""), (f"{NEW[2]}    1/1     10m", ""),
                 ("order-5f8b-c2v5n    1/1     4s", "hot"), ("order-5f8b-k9j3x    1/1     4s", "hot")]
        terminal(ax, 0.3, 1.0, 11.4, 5.3, lines)
        moral(ax, 6.0, 0.4, "틀 밖의 개수만 바꾸면 있던 파드는 그대로 두고 더하기만 해요")


def cards():
    fig, ax = canvas(6.4, 5.4, 9.8, 8.3)
    W, H = 4.6, 3.8

    def card(i, name, line):
        col, row = i % 2, i // 2
        x, y = 0.2 + col * 4.9, 4.3 - row * 4.05
        box(ax, x, y, W, H, fc="white")
        label(ax, x + 0.25, y + H - 0.4, name, fs=12.5, ha="left", bold=True)
        label(ax, x + W / 2, y + 0.6, line, fs=10, color=INK)
        return x, y

    x, y = card(0, "파드 템플릿", "파드를 찍어 내는 틀\nDeployment 안의 template 칸")
    ax.add_patch(Rectangle((x + 0.5, y + 1.35), 1.6, 1.4, fc=PINK, ec=RED, lw=1.8))
    label(ax, x + 1.3, y + 2.05, "틀", fs=11, color=RED, bold=True)
    for k in range(3):
        arrow(ax, (x + 2.2, y + 2.05), (x + 3.0, y + 2.55 - k * 0.5), ms=9)
        pod(ax, x + 3.05, y + 2.35 - k * 0.5, "파드", w=1.1, h=0.4, fs=8)
    x, y = card(1, "해시 (지문)", "틀 전체를 짧게 줄인 글자\n틀이 바뀌면 지문도 바뀌어요")
    code(ax, x + 0.6, y + 2.05, "7c9d", fs=13)
    arrow(ax, (x + 1.8, y + 2.05), (x + 2.6, y + 2.05), color=RED, ms=11)
    code(ax, x + 2.8, y + 2.05, "5f8b", fs=13, hot=True)
    x, y = card(2, "ReplicaSet", "같은 틀의 파드를 정한 개수만큼\n지키는 묶음 (지문마다 하나)")
    ax.add_patch(Rectangle((x + 0.4, y + 1.4), 3.8, 1.25, fc="white", ec=INK, lw=1.2))
    label(ax, x + 0.55, y + 2.45, "order-5f8b", fs=9, ha="left", color=INK)
    for k in range(3):
        pod(ax, x + 0.5 + k * 1.22, y + 1.5, "5f8b", hot=k == 2, w=1.1, h=0.55, fs=8)
    x, y = card(3, "롤링 업데이트", "새 파드를 띄우고 옛 파드를 내리기를\n하나씩 되풀이하는 교대")
    for k in range(3):
        pod(ax, x + 0.4 + k * 1.3, y + 2.25, "옛", gone=k == 0, dim=k > 0, w=1.1, h=0.5, fs=8)
        if k == 0:
            pod(ax, x + 0.4 + k * 1.3, y + 1.55, "새", hot=True, w=1.1, h=0.5, fs=8)
    save(fig, OUT, "k8s08-cards.svg")


if __name__ == "__main__":
    S, L = (7.2, 3.8), (12, 6.6)
    stage(opening, 3, OUT, "k8s08-open", S, L)
    stage(template, 2, OUT, "k8s08-template", S, L)
    stage(hashing, 3, OUT, "k8s08-hash", S, L)
    stage(scale, 2, OUT, "k8s08-scale", S, L)
    where()
    stage(roll, 5, OUT, "k8s08-roll", S, L)
    decide()
    stage(back, 3, OUT, "k8s08-back", S, L)
    cards()
