"""쿠버네티스 8편 그림 만들기. 실행: python lab/fig_k8s08.py  → docs/kubernetes/img/08/*.svg

그림마다 지금 볼 곳만 빨강으로 칠한다. 그림 안 글씨는 낱말과 숫자만 둔다.
예시는 7편의 주문 처리 Deployment order를 잇는다. 마감 시간 환경 변수 CLOSE_TIME 을 21:00 → 22:00 으로 바꾼다.
옛 틀의 지문 7c9d, 새 틀의 지문 5f8b.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "es"))
sys.path.insert(0, os.path.dirname(__file__))
from figkit import (GREY, INK, NOTE, PAPER, PINK, RED, arrow, box,  # noqa: E402
                    canvas, label, outdir, save)
from matplotlib.patches import Rectangle  # noqa: E402
from fig_k8s07 import MONO, pod, terminal  # noqa: E402

OUT = outdir("08", topic="kubernetes")
OLD = ["order-7c9d-m8x1z", "order-7c9d-p2v6x", "order-7c9d-w8n3m"]
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


def short(name):
    """그림 칸이 좁아 앞의 order- 를 뗀다. 가운데 지문은 남긴다."""
    return name.split("-", 1)[1] if name.startswith("order-") else name


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
        pod(ax, px, py, short(nm), hot=st == "hot", gone=st == "gone", dim=dim, w=1.8, h=0.7, fs=9)



# ── 1절: 한 줄 바꿨더니 파드가 모두 새 이름 ─────────────────────────
def opening():
    fig, ax = canvas(7.2, 3.9, 12, 6.6)
    deploy_doc(ax, close="22:00", hot=("env",), tpl_label=False)
    terminal(ax, 5.3, 0.6, 6.4, 5.5, [("$ kubectl apply -f order.yaml", "cmd"),
                                      ("deployment.apps/order configured", ""),
                                      ("$ kubectl get pods", "cmd"), ("NAME                READY   AGE", ""),
                                      (f"{NEW[0]}    1/1     40s", "hot"), (f"{NEW[1]}    1/1     25s", "hot"),
                                      (f"{NEW[2]}    1/1     9s", "hot")])
    save(fig, OUT, "k8s08-open.svg")


# ── 2절: 파드 템플릿 하나로 파드 3개 ───────────────────────────────
def template():
    fig, ax = canvas(7.2, 3.9, 12, 6.6)
    tx, ty, tw, th = deploy_doc(ax, tpl_hot=True)
    for k in range(3):
        arrow(ax, (tx + tw + 0.1, ty + th / 2), (6.6, 4.6 - k * 1.2), color=RED, ms=13)
        pod(ax, 6.7, 4.2 - k * 1.2, OLD[k], w=2.6, fs=9.5)
    label(ax, 5.5, 5.3, "틀 밖", fs=10.5, color=INK, ha="left")
    arrow(ax, (5.45, 5.3), (3.3, 5.0), color=GREY, ms=11)
    save(fig, OUT, "k8s08-template.svg")


# ── 3절: 틀이 바뀌면 지문이 바뀌고 새 묶음이 생겨요 ───────────────────
def mini_tpl(ax, x, y, close, hot=False):
    w, h = 3.9, 1.5
    ax.add_patch(Rectangle((x, y), w, h, fc=PAPER, ec=INK, lw=1.3))
    label(ax, x + 0.1, y + h + 0.22, "파드 템플릿", fs=10, ha="left", color=INK)
    code(ax, x + 0.15, y + 1.1, "image: order:1", fs=9.5)
    if hot:
        ax.add_patch(Rectangle((x + 0.06, y + 0.38), w - 0.12, 0.4, fc=PINK, ec=RED, lw=1.3))
    code(ax, x + 0.15, y + 0.58, f"CLOSE_TIME={close}", fs=9.5, hot=hot)
    return x + w, y + h / 2


def hashing():
    fig, ax = canvas(7.6, 3.6, 15, 6.4)
    for row, (close, fp, name, pods, hot) in enumerate((
            ("21:00", "7c9d", "order-7c9d", [(n, "") for n in OLD], False),
            ("22:00", "5f8b", "order-5f8b", [], True))):
        y = 3.4 - row * 3.1
        ex, ey = mini_tpl(ax, 0.3, y + 0.6, close, hot=hot)
        arrow(ax, (ex + 0.1, ey), (4.85, ey), color=RED if hot else INK, ms=13)
        finger(ax, 4.9, ey - 0.45, fp, hot=hot)
        arrow(ax, (7.0, ey), (7.75, ey), color=RED if hot else INK, ms=13)
        rs(ax, 7.8, y + 0.85, name, pods, hot=hot, note="파드 0개" if hot else None, w=6.6)
    save(fig, OUT, "k8s08-hash.svg")


# ── 4절: 개수만 바꾸면 지문이 그대로 ────────────────────────────────
def scale():
    fig, ax = canvas(7.2, 3.9, 12, 6.6)
    tx, ty, tw, th = deploy_doc(ax, replicas="5", hot=("replicas",))
    arrow(ax, (tx + tw + 0.1, ty + th / 2), (5.55, 4.85), color=GREY, ms=13)
    finger(ax, 5.6, 4.4, "7c9d", note="그대로")
    rs(ax, 5.5, 1.0, "order-7c9d", [(n, "") for n in OLD] + [("order-7c9d-b4n6r", "hot"), ("order-7c9d-q1w8e", "hot")])
    save(fig, OUT, "k8s08-scale.svg")


# ── 지문(해시) ─────────────────────────────────────────────────────
def finger(ax, x, y, s, hot=False, note=None):
    box(ax, x, y, 2.0, 0.9, fc=PINK if hot else NOTE, ec=RED if hot else INK)
    label(ax, x + 1.0, y + 1.15, "지문", fs=10, color=RED if hot else INK)
    label(ax, x + 1.0, y + 0.45, s, fs=14, family=MONO, color=RED if hot else "#222", bold=True)
    if note:
        label(ax, x + 1.0, y - 0.3, note, fs=10, color=RED if hot else INK, bold=hot)


def where():
    fig, ax = canvas(7.6, 3.6, 15, 7.2)
    head = [("바꾼 칸", 1.9), ("틀 안?", 6.0), ("지문", 8.6), ("파드는", 12.2)]
    for s, x in head:
        label(ax, x, 6.7, s, fs=11, bold=True, color=INK)
    ax.plot([0.3, 14.7], [6.35, 6.35], color=INK, lw=1.0)
    rows = [("env: CLOSE_TIME", "안", "7c9d → 5f8b", "전부 교대", True),
            ("hostAliases", "안", "7c9d → 5f8b", "전부 교대", True),
            ("image", "안", "7c9d → 5f8b", "전부 교대", True),
            ("replicas", "밖", "7c9d 그대로", "개수만 맞춤", False)]
    for k, (a, b, c, d, hot) in enumerate(rows):
        y = 5.6 - k * 1.45
        if hot:
            ax.add_patch(Rectangle((0.3, y - 0.55), 14.4, 1.1, fc=PINK, ec="none"))
        code(ax, 0.5, y, a, hot=hot, fs=10.5)
        label(ax, 6.0, y, b, fs=11.5, color=RED if hot else "#222", bold=hot)
        label(ax, 8.6, y, c, fs=11, color=RED if hot else "#222", family=MONO)
        label(ax, 12.2, y, d, fs=11, color=RED if hot else "#222", bold=hot)
    save(fig, OUT, "k8s08-where.svg")



# ── 5절: 하나씩 바꿔 끼우기 (한 장에 다섯 줄) ──────────────────────
def roll():
    fig, ax = canvas(7.6, 5.4, 17, 12)
    OX, NX, CX, PW = 1.4, 8.4, 15.8, 2.0
    label(ax, OX + 3.1, 11.4, "옛 묶음 order-7c9d", fs=10.5, bold=True, color=INK)
    label(ax, NX + 3.1, 11.4, "새 묶음 order-5f8b", fs=10.5, bold=True, color=INK)
    label(ax, CX, 11.6, "일하는 파드", fs=10, bold=True, color=INK)
    label(ax, CX, 11.1, "/ 모두", fs=10, bold=True, color=INK)
    ax.plot([0.2, 16.8], [10.75, 10.75], color=INK, lw=1.0)
    rows = [
        ("시작", [(OLD[0], ""), (OLD[1], ""), (OLD[2], "")], [], (3, 3, False)),
        ("①", [(OLD[0], ""), (OLD[1], ""), (OLD[2], "")], [(NEW[0], "wait")], (3, 4, True)),
        ("②", [(OLD[0], "gone"), (OLD[1], ""), (OLD[2], "")], [(NEW[0], "")], (3, 3, False)),
        ("③", [None, (OLD[1], "gone"), (OLD[2], "")], [(NEW[0], ""), (NEW[1], "hot")], (3, 3, False)),
        ("④", [None, None, (OLD[2], "gone")], [(NEW[0], ""), (NEW[1], ""), (NEW[2], "hot")], (3, 3, False)),
    ]
    for r, (tag, old, new, (ready, total, hot)) in enumerate(rows):
        y = 9.4 - r * 2.1
        label(ax, 0.6, y + 0.4, tag, fs=12, bold=True, color=INK)
        for k, p in enumerate(old):
            if p is None:
                continue
            nm, st = p
            pod(ax, OX + k * (PW + 0.18), y, short(nm), gone=st == "gone", w=PW, fs=9)
        for k, (nm, st) in enumerate(new):
            px = NX + k * (PW + 0.18)
            if st == "wait":
                ax.add_patch(Rectangle((px, y), PW, 0.75, fc=PINK, ec=RED, lw=1.6, ls="--"))
                label(ax, px + PW / 2, y + 0.38, f"{short(nm)}\n준비 중", fs=8.5, color=RED)
            else:
                pod(ax, px, y, short(nm), hot=st == "hot", w=PW, fs=9)
        label(ax, CX, y + 0.38, f"{ready} / {total}", fs=12, bold=hot, color=RED if hot else "#222")
        if r < len(rows) - 1:
            ax.plot([0.2, 16.8], [y - 0.55, y - 0.55], color=GREY, lw=0.6)
    save(fig, OUT, "k8s08-roll.svg")


# ── 6절: ConfigMap 내용만 바꾸면 지문도 파드도 그대로 ───────────────
def configmap():
    fig, ax = canvas(7.4, 3.6, 14, 6.8)
    # ConfigMap
    ax.add_patch(Rectangle((0.3, 3.9), 4.4, 1.9, fc="white", ec=RED, lw=1.8))
    label(ax, 0.4, 6.05, "ConfigMap order-config", fs=10, ha="left", color=RED, bold=True)
    code(ax, 0.5, 5.15, "CLOSE_TIME=21:00", fs=10, dim=True)
    ax.plot([0.5, 3.0], [5.15, 5.15], color=GREY, lw=1.2)
    code(ax, 0.5, 4.45, "CLOSE_TIME=22:00", fs=10, hot=True)
    # 파드 템플릿
    ax.add_patch(Rectangle((0.3, 0.6), 4.4, 1.9, fc=PAPER, ec=INK, lw=1.3))
    label(ax, 0.4, 2.75, "파드 템플릿", fs=10, ha="left", color=INK)
    code(ax, 0.5, 1.9, "image: order:1", fs=9.5)
    code(ax, 0.5, 1.2, "envFrom: order-config", fs=9.5)
    arrow(ax, (2.5, 2.55), (2.5, 3.8), color=GREY, ms=11)
    arrow(ax, (4.8, 1.55), (5.85, 1.55), color=INK, ms=13)
    finger(ax, 5.9, 1.1, "7c9d", note="그대로")
    # 파드
    ax.add_patch(Rectangle((8.6, 0.6), 5.1, 5.2, fc="white", ec=INK, lw=1.3, ls="--"))
    label(ax, 8.75, 5.5, "떠 있는 파드", fs=10, ha="left", color=INK)
    for k in range(3):
        y = 4.2 - k * 1.3
        box(ax, 8.9, y, 4.5, 0.95, fc=PINK, ec=RED, lw=1.6)
        label(ax, 11.15, y + 0.62, OLD[k], fs=8.5, color=INK)
        code(ax, 9.1, y + 0.25, "CLOSE_TIME=21:00", fs=9.5, hot=True)
    save(fig, OUT, "k8s08-configmap.svg")


if __name__ == "__main__":
    opening()
    template()
    hashing()
    scale()
    where()
    roll()
    configmap()
