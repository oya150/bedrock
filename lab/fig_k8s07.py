"""쿠버네티스 7편 그림 만들기. 실행: python lab/fig_k8s07.py  → docs/kubernetes/img/07/*.svg

그림마다 지금 볼 곳만 빨강으로 칠한다. 그림 안 글씨는 낱말과 숫자만 둔다.
예시는 동네 빵집 주문 앱의 주문 처리 파드 3개(Deployment order)를 끝까지 쓴다.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "es"))
from figkit import (GREY, INK, LIGHT, NOTE, PAPER, PINK, RED, arrow, box, bubble,  # noqa: E402
                    canvas, cylinder, label, outdir, save)
from matplotlib.patches import Circle, FancyArrowPatch, Rectangle  # noqa: E402

OUT = outdir("07", topic="kubernetes")
MONO = ["Menlo", "Apple SD Gothic Neo", "monospace"]


# ── 공통 부품 ──────────────────────────────────────────────────────
def terminal(ax, x, y, w, h, lines, title="터미널"):
    """터미널 창. lines=[(글, 상태)] 상태는 ""·"hot"·"dim"·"cmd"."""
    ax.add_patch(Rectangle((x, y), w, h, fc="white", ec=INK, lw=1.5))
    ax.add_patch(Rectangle((x, y + h - 0.42), w, 0.42, fc=LIGHT, ec=INK, lw=1.2))
    for k, c in enumerate(("#e4572e", "#f6c445", "#8fb58f")):
        ax.add_patch(Circle((x + 0.25 + k * 0.25, y + h - 0.21), 0.07, fc=c, ec="none"))
    label(ax, x + w / 2, y + h - 0.21, title, fs=10, color=INK)
    ty = y + h - 0.75
    for s, st in lines:
        if st == "hot":
            ax.add_patch(Rectangle((x + 0.12, ty - 0.21), w - 0.24, 0.42, fc=PINK, ec=RED, lw=1.4))
        color = RED if st == "hot" else (GREY if st == "dim" else "#222")
        ax.text(x + 0.25, ty, s, fontsize=10.5, family=MONO, color=color, ha="left", va="center",
                fontweight="bold" if st in ("hot", "cmd") else "normal")
        ty -= 0.5


def pod(ax, x, y, name, hot=False, dim=False, gone=False, w=1.9, h=0.75, fs=10):
    """파드 한 개. gone=지워진 자리(점선과 ✗)."""
    if gone:
        ax.add_patch(Rectangle((x, y), w, h, fill=False, ec=RED, lw=1.6, ls="--"))
        label(ax, x + w / 2, y + h / 2, name, fs=fs, color=RED)
        label(ax, x + w - 0.15, y + h - 0.12, "✗", fs=13, color=RED, bold=True)
        return
    box(ax, x, y, w, h, fc=PINK if hot else (LIGHT if dim else NOTE),
        ec=RED if hot else (GREY if dim else INK), lw=2.0 if hot else 1.4)
    label(ax, x + w / 2, y + h / 2, name, fs=fs, color=RED if hot else (GREY if dim else "#222"), bold=hot)


def manifest(ax, x, y, lines, hot=(), w=3.4, title="order.yaml", fs=10.5, dim=False):
    """원하는 상태를 적은 문서. 오른쪽 위 모서리를 접은 종이로 그린다."""
    h = 0.55 + 0.45 * len(lines)
    ec = GREY if dim else INK
    ax.add_patch(Rectangle((x, y), w, h, fc="white", ec=ec, lw=1.5))
    ax.plot([x + w - 0.35, x + w], [y + h, y + h - 0.35], color=ec, lw=1.2)
    label(ax, x + 0.15, y + h + 0.22, title, fs=10, ha="left", color=GREY if dim else INK)
    ty = y + h - 0.4
    for k, s in enumerate(lines):
        on = k in hot
        if on:
            ax.add_patch(Rectangle((x + 0.08, ty - 0.2), w - 0.16, 0.4, fc=PINK, ec=RED, lw=1.3))
        ax.text(x + 0.2, ty, s, fontsize=fs, family=MONO, ha="left", va="center",
                color=RED if on else (GREY if dim else "#222"), fontweight="bold" if on else "normal")
        ty -= 0.45
    return h


DOC = ["kind: Deployment", "name: order", "replicas: 3", "image: order:1"]

P1, P2, P3, P4 = "order-7c9d-k2p4q", "order-7c9d-m8x1z", "order-7c9d-t5r7v", "order-7c9d-w8n3m"
HEAD = "NAME                READY   AGE"


# ── 1절: 지운 파드가 다시 생겨요 (터미널 한 장) ─────────────────────
def opening():
    fig, ax = canvas(7.2, 4.3, 12, 7.2)
    lines = [("$ kubectl get pods", "cmd"), (HEAD, ""), (f"{P1}    1/1     2d", ""),
             (f"{P2}    1/1     2d", ""), (f"{P3}    1/1     2d", ""),
             (f"$ kubectl delete pod {P1}", "hot"), (f'pod "{P1}" deleted', ""),
             ("$ kubectl get pods", "cmd"), (HEAD, ""), (f"{P2}    1/1     2d", ""),
             (f"{P3}    1/1     2d", ""), (f"{P4}    1/1     3s", "hot")]
    terminal(ax, 0.3, 0.3, 11.4, 6.8, lines)
    save(fig, OUT, "k8s07-open.svg")


# ── 2절: 온도 조절기 (세 칸 나란히) ────────────────────────────────
def thermo():
    fig, ax = canvas(7.6, 3.4, 15, 6.6)
    panels = [("①", "18도", "켜짐", False, ("heat",)),
              ("②", "22도", "꺼짐", False, ("now", "heat")),
              ("③", "19도", "켜짐", True, ("now", "heat", "win"))]
    for k, (no, now, heat, win, hot) in enumerate(panels):
        x = 0.2 + k * 5.0
        ax.add_patch(Rectangle((x, 0.3), 4.6, 5.6, fc="white", ec=INK, lw=1.5))
        label(ax, x + 0.3, 5.5, no, fs=13, bold=True, ha="left")
        # 지금 온도
        h = "now" in hot
        box(ax, x + 0.3, 3.4, 1.9, 1.5, fc=PINK if h else NOTE, ec=RED if h else INK)
        label(ax, x + 1.25, 4.5, "지금 온도", fs=9.5, color=RED if h else INK)
        label(ax, x + 1.25, 3.85, now, fs=14, bold=True, color=RED if h else "#222")
        # 원하는 온도(조절기)
        box(ax, x + 2.4, 3.4, 1.9, 1.5, fc=NOTE)
        label(ax, x + 3.35, 4.5, "원하는 온도", fs=9.5, color=INK)
        label(ax, x + 3.35, 3.85, "22도", fs=14, bold=True)
        # 히터
        on = heat == "켜짐"
        box(ax, x + 0.3, 1.0, 2.6, 1.3, fc=PINK if on else LIGHT, ec=RED if on else GREY)
        label(ax, x + 1.6, 1.65, f"히터 {heat}", fs=11, bold=on, color=RED if on else GREY)
        # 창문
        if win:
            ax.add_patch(Rectangle((x + 3.55, 0.9), 0.35, 1.6, fc=PINK, ec=RED, lw=1.8))
            label(ax, x + 3.72, 2.8, "창문 열림", fs=9.5, color=RED, bold=True)
        else:
            ax.add_patch(Rectangle((x + 3.55, 0.9), 0.35, 1.6, fc=LIGHT, ec=INK, lw=1.2))
            label(ax, x + 3.72, 2.8, "창문", fs=9.5, color=INK)
    save(fig, OUT, "k8s07-thermo.svg")


# ── 쿠버네티스 무대: 문서 → API 서버 → 저장소 / 컨트롤러 / 노드 ───────
def world(ax, *, doc_lines, doc_hot=(), send=False, stored=None, stored_hot=False,
          ctrl=None, ctrl_hot=False, pods=(), now_hot=False, ask=None, user=None, short=False, now=None):
    """pods=[(이름, 상태)] 상태는 ""·"hot"·"gone"."""
    manifest(ax, 0.3, 3.55, doc_lines, hot=doc_hot, w=3.3, fs=9.5)
    arrow(ax, (3.75, 4.6), (4.85, 4.6), color=RED if send else GREY, ms=14)
    box(ax, 4.95, 4.05, 2.4, 1.1, fc=PAPER)
    label(ax, 6.15, 4.6, "API 서버", fs=11, bold=True)
    cylinder(ax, 8.0, 3.95, 3.7, 1.2, "", fc=PINK if stored_hot else NOTE, ec=RED if stored_hot else INK)
    label(ax, 9.85, 5.65, "저장소", fs=10.5, color=INK)
    arrow(ax, (7.45, 4.6), (8.1, 4.6), color=RED if send else GREY, ms=12)
    label(ax, 9.85, 4.55, stored, fs=10.5, color=RED if stored_hot else "#222", bold=stored_hot)
    if ctrl is not None:
        box(ax, 0.3, 1.25, 2.6, 1.0, fc=PINK if ctrl_hot else NOTE, ec=RED if ctrl_hot else INK)
        label(ax, 1.6, 1.75, "컨트롤러", fs=11.5, bold=True, color=RED if ctrl_hot else "#222")
        if ctrl:
            bubble(ax, 0.3, 2.6, 3.4, 0.8, ctrl, (1.6, 2.27), hot=ctrl_hot, fs=10.5)
    ax.add_patch(Rectangle((5.0, 0.6), 6.7, 2.65, fc="white", ec=INK, lw=1.3, ls="--"))
    label(ax, 5.15, 3.0, "노드", fs=10, ha="left", color=INK)
    n = sum(1 for _, s in pods if s != "gone") if now is None else now
    label(ax, 11.55, 3.0, f"지금 상태: 파드 {n}개", fs=10.5, ha="right", color=RED if now_hot else INK, bold=now_hot)
    cols = 4 if short else 3
    w = 1.5 if short else 2.05
    for k, (nm, st) in enumerate(pods):
        x = 5.2 + k * (w + 0.13)
        pod(ax, x, 1.6, nm, hot=st == "hot", gone=st == "gone", w=w, fs=10 if short else 8)
    if ask:
        arrow(ax, (2.95, 1.75), (5.1, 1.95), color=RED, ms=14)
        label(ax, 3.95, 1.3, ask, fs=10, color=RED, bold=True)
    if user:
        label(ax, 8.35, 0.25, user, fs=10, color=RED, bold=True, family=MONO)
    return cols


DOC = ["kind: Deployment", "name: order", "replicas: 3", "image: order:1"]
STORED = "원하는 상태\norder 파드 3개"


def manifest_fig():
    fig, ax = canvas(7.2, 3.9, 12, 6.4)
    world(ax, doc_lines=DOC, doc_hot=(2, 3), send=True, stored=STORED, stored_hot=True)
    label(ax, 2.0, 2.9, "kubectl apply -f order.yaml", fs=10, color=RED, bold=True, family=MONO)
    save(fig, OUT, "k8s07-manifest.svg")


def ctrl_fig():
    fig, ax = canvas(7.2, 3.9, 12, 6.4)
    world(ax, doc_lines=DOC, stored=STORED, ctrl="원하는 3개 · 지금 0개", ctrl_hot=True,
          ask="3개 만들기", pods=[(n, "hot") for n in (P1, P2, P3)], now_hot=True)
    save(fig, OUT, "k8s07-ctrl.svg")


def loop_fig():
    fig, ax = canvas(7.2, 3.9, 12, 6.4)
    short = lambda p: p.split("-")[-1]  # noqa: E731
    world(ax, doc_lines=DOC, stored=STORED, ctrl="원하는 3개 · 지금 2개", ctrl_hot=True, ask="1개 만들기",
          pods=[(short(P1), "gone"), (short(P2), ""), (short(P3), ""), (short(P4), "hot")],
          now_hot=True, user=f"kubectl delete pod {P1}", short=True, now=2)
    label(ax, 5.2 + 3 * 1.63 + 0.75, 1.32, "만드는 중", fs=9.5, color=RED, bold=True)
    save(fig, OUT, "k8s07-loop.svg")


def cycle():
    fig, ax = canvas(6.4, 4.4, 10, 6.9)
    pts = {"watch": (5.0, 5.9), "cmp": (8.2, 1.4), "act": (1.8, 1.4)}
    names = {"watch": "① 지켜보기\n지금 상태", "cmp": "② 비교하기\n원하는 상태 ↔ 지금 상태",
             "act": "③ 맞추기\n차이만큼 만들기·지우기"}
    for k, (x, y) in pts.items():
        box(ax, x - 1.6, y - 0.65, 3.2, 1.3, fc=NOTE)
        label(ax, x, y, names[k], fs=10.5)
    for a, b in (("watch", "cmp"), ("cmp", "act"), ("act", "watch")):
        (x1, y1), (x2, y2) = pts[a], pts[b]
        ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>", mutation_scale=16, color=RED, lw=2,
                                     connectionstyle="arc3,rad=-0.35", shrinkA=42, shrinkB=42))
    label(ax, 5.0, 3.0, "되풀이", fs=13, color=RED, bold=True)
    save(fig, OUT, "k8s07-cycle.svg")


# ── 6절: 명령으로 바꾼 것은 다음 apply가 덮어요 ──────────────────────
def overwrite():
    fig, ax = canvas(7.6, 2.9, 15, 5.6)
    steps = [("3", False), ("5", False), ("3", True)]
    cmds = ["kubectl scale\n--replicas=5", "kubectl apply\n-f order.yaml"]
    for k, (v, hot) in enumerate(steps):
        x = 0.4 + k * 5.2
        cylinder(ax, x, 1.6, 3.6, 1.5, "", fc=PINK if hot else NOTE, ec=RED if hot else INK)
        label(ax, x + 1.8, 2.25, f"원하는 상태\n파드 {v}개", fs=11, color=RED if hot else "#222", bold=hot)
    for k, c in enumerate(cmds):
        x = 4.1 + k * 5.2
        hot = k == 1
        arrow(ax, (x, 2.3), (x + 1.4, 2.3), color=RED if hot else INK, ms=14)
        label(ax, x + 0.7, 0.85, c, fs=9.5, family=MONO, color=RED if hot else INK, bold=hot)
    ax.add_patch(Rectangle((10.4, 4.2), 3.6, 1.2, fc="white", ec=RED, lw=1.4))
    ax.text(10.55, 4.8, "order.yaml\nreplicas: 3", fontsize=9.5, family=MONO, color=RED, ha="left", va="center")
    arrow(ax, (12.2, 4.15), (12.2, 3.75), color=RED, ms=12)
    save(fig, OUT, "k8s07-overwrite.svg")


def fix():
    fig, ax = canvas(7.2, 2.9, 12, 4.6)
    manifest(ax, 0.3, 1.2, ["kind: Deployment", "name: order", "replicas: 2", "image: order:1"], hot=(2,), w=3.9)
    terminal(ax, 4.6, 0.3, 7.1, 3.9, [("$ kubectl apply -f order.yaml", "hot"),
                                     ("deployment.apps/order configured", ""),
                                     ("$ kubectl get pods", "cmd"), (HEAD, ""),
                                     (f"{P2}    1/1     2d", ""), (f"{P4}    1/1     5m", "")])
    save(fig, OUT, "k8s07-fix.svg")


if __name__ == "__main__":
    opening()
    thermo()
    manifest_fig()
    ctrl_fig()
    loop_fig()
    cycle()
    overwrite()
    fix()
