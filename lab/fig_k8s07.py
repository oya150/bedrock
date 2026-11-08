"""쿠버네티스 7편 그림 만들기. 실행: python lab/fig_k8s07.py  → docs/kubernetes/img/07/*.svg

본문 절은 장면 띠로 그린다: 같은 무대를 여러 장 그리고 장마다 바뀐 곳만 빨강으로 칠한다.
예시는 동네 빵집 주문 앱의 주문 처리 파드 3개(Deployment order)를 끝까지 쓴다.
"""
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "es"))
from figkit import (GREY, INK, LIGHT, NOTE, PAPER, PINK, RED, arrow, box, bubble,  # noqa: E402
                    canvas, cylinder, label, moral, outdir, save, stage)
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

# ── 여는 장면: 지운 파드가 다시 생겨요 ─────────────────────────────
P1, P2, P3, P4 = "order-7c9d-k2p4q", "order-7c9d-m8x1z", "order-7c9d-t5r7v", "order-7c9d-w8n3m"


def opening(ax, step):
    head = ("NAME                READY   AGE", "")
    if step == 1:
        lines = [("$ kubectl get pods", "cmd"), head, (f"{P1}    1/1     2d", ""),
                 (f"{P2}    1/1     2d", ""), (f"{P3}    1/1     2d", "")]
        terminal(ax, 0.3, 1.6, 11.4, 3.9, lines)
        label(ax, 6.0, 0.8, "주문 처리 파드가 3개 떠 있어요", fs=11.5, color=INK)
    elif step == 2:
        lines = [("$ kubectl get pods", "dim"), ("...", "dim"),
                 (f"$ kubectl delete pod {P1}", "hot"), (f'pod "{P1}" deleted', "hot")]
        terminal(ax, 0.3, 1.6, 11.4, 3.9, lines)
        label(ax, 6.0, 0.8, "그중 하나를 지웠어요", fs=11.5, color=RED, bold=True)
    else:
        lines = [("$ kubectl get pods", "cmd"), head, (f"{P2}    1/1     2d", ""),
                 (f"{P3}    1/1     2d", ""), (f"{P4}    1/1     3s", "hot")]
        terminal(ax, 0.3, 1.6, 11.4, 3.9, lines)
        moral(ax, 6.0, 0.8, "다시 보니 3개 그대로예요. 3초 전에 생긴 새 파드가 있어요")


# ── 온도 조절기 ────────────────────────────────────────────────────
def room(ax, now, want, heater, window=False, now_hot=False, want_hot=False, heat_hot=False):
    ax.add_patch(Rectangle((0.4, 0.9), 7.0, 5.0, fc="white", ec=INK, lw=1.6))
    label(ax, 0.6, 5.6, "방", fs=11, ha="left", color=INK)
    # 온도계(지금 온도)
    box(ax, 1.0, 3.3, 2.4, 1.4, fc=PINK if now_hot else NOTE, ec=RED if now_hot else INK)
    label(ax, 2.2, 4.3, "지금 온도", fs=10, color=RED if now_hot else INK)
    label(ax, 2.2, 3.7, now, fs=15, bold=True, color=RED if now_hot else "#222")
    # 조절기(원하는 온도)
    box(ax, 4.4, 3.3, 2.4, 1.4, fc=PINK if want_hot else NOTE, ec=RED if want_hot else INK)
    label(ax, 5.6, 4.95, "온도 조절기", fs=10.5, bold=True)
    label(ax, 5.6, 4.3, "원하는 온도", fs=10, color=RED if want_hot else INK)
    label(ax, 5.6, 3.7, want, fs=15, bold=True, color=RED if want_hot else "#222")
    # 히터
    on = heater == "켜짐"
    box(ax, 1.0, 1.3, 2.4, 1.1, fc=PINK if heat_hot else (NOTE if on else LIGHT),
        ec=RED if heat_hot else (INK if on else GREY))
    label(ax, 2.2, 1.85, f"히터 {heater}", fs=11.5, bold=heat_hot, color=RED if heat_hot else ("#222" if on else GREY))
    # 창문
    if window:
        ax.add_patch(Rectangle((7.25, 1.6), 0.3, 2.2, fc=PINK, ec=RED, lw=1.8))
        label(ax, 7.0, 1.25, "창문 열림", fs=10.5, color=RED, ha="right", bold=True)
    else:
        ax.add_patch(Rectangle((7.25, 1.6), 0.3, 2.2, fc=LIGHT, ec=INK, lw=1.2))


SAY = (7.9, 4.75, 4.0, 1.35)
TT = (8.05, 4.25)


def thermo(ax, step):
    if step == 1:
        room(ax, "18도", "22도", "꺼짐", want_hot=True)
        bubble(ax, *SAY, "원하는 온도를\n22도로 받았어요", TT, hot=True)
    elif step == 2:
        room(ax, "18도", "22도", "켜짐", heat_hot=True)
        bubble(ax, *SAY, "18도는 22도보다 낮아요\n히터를 켜요", TT, hot=True)
    elif step == 3:
        room(ax, "22도", "22도", "꺼짐", now_hot=True)
        bubble(ax, *SAY, "22도가 됐어요\n히터를 꺼요", TT, hot=True)
    else:
        room(ax, "19도", "22도", "켜짐", window=True, now_hot=True, heat_hot=True)
        bubble(ax, *SAY, "19도로 떨어졌어요\n다시 켜요", TT, hot=True)
        moral(ax, 6.0, 0.35, "원하는 온도만 받고 켜고 끄기는 조절기가 정해요")


# ── 쿠버네티스 무대: 문서 → API 서버 → 원하는 상태 / 컨트롤러 / 노드의 파드 ──
def world(ax, *, doc_hot=(), send=False, stored=None, stored_hot=False, ctrl=None, ctrl_hot=False,
          pods=(), now_label=None, now_hot=False, ask=False, doc_lines=DOC, user=None):
    """pods=[(이름, 상태)] 상태는 ""·"hot"·"gone"."""
    manifest(ax, 0.3, 3.55, doc_lines, hot=doc_hot, w=3.3)
    arrow(ax, (3.75, 4.6), (4.85, 4.6), color=RED if send else GREY, ms=14)
    # API 서버와 저장소
    box(ax, 4.95, 4.05, 2.4, 1.1, fc=PAPER)
    label(ax, 6.15, 4.6, "API 서버", fs=11, bold=True)
    cylinder(ax, 8.0, 3.95, 3.7, 1.2, "", fc=PINK if stored_hot else NOTE, ec=RED if stored_hot else INK)
    label(ax, 9.85, 5.65, "저장소", fs=10.5, color=INK)
    arrow(ax, (7.45, 4.6), (8.1, 4.6), color=RED if send else GREY, ms=12)
    label(ax, 9.85, 4.55, stored or "원하는 상태\n(비었음)", fs=10.5,
          color=RED if stored_hot else ("#222" if stored else GREY), bold=stored_hot)
    # 컨트롤러
    if ctrl is not None:
        box(ax, 0.3, 1.25, 2.6, 1.0, fc=PINK if ctrl_hot else NOTE, ec=RED if ctrl_hot else INK)
        label(ax, 1.6, 1.75, "컨트롤러", fs=11.5, bold=True, color=RED if ctrl_hot else "#222")
        if ctrl:
            bubble(ax, 0.3, 2.45, 4.4, 0.85, ctrl, (1.6, 2.3), hot=ctrl_hot, fs=10.5)
    # 노드(지금 상태)
    ax.add_patch(Rectangle((5.0, 0.6), 6.7, 2.65, fc="white", ec=INK, lw=1.3, ls="--"))
    label(ax, 5.15, 3.0, "노드 (컴퓨터)", fs=10, ha="left", color=INK)
    label(ax, 11.55, 3.0, now_label or f"지금 상태: 파드 {sum(1 for _, s in pods if s != 'gone')}개", fs=10.5,
          ha="right", color=RED if now_hot else INK, bold=now_hot)
    for k, (nm, st) in enumerate(pods):
        x = 5.25 + (k % 3) * 2.15
        y = 1.75
        pod(ax, x, y, nm, hot=st == "hot", gone=st == "gone", w=2.05, fs=8)
    if ask:
        arrow(ax, (2.95, 1.75), (5.15, 1.95), color=RED, ms=14)
        label(ax, 3.9, 1.3, "만들어 주세요", fs=10, color=RED, bold=True)
    if user:
        label(ax, 8.35, 0.25, user, fs=10, color=RED, bold=True)


STORED = "원하는 상태\norder 파드 3개"
PODS3 = [(P1, ""), (P2, ""), (P3, "")]


def manifest_strip(ax, step):
    if step == 1:
        world(ax, doc_hot=(2, 3))
        label(ax, 2.0, 2.9, "주문 처리 파드를\n3개 띄워 두고 싶어요", fs=11, color=RED, bold=True)
    else:
        world(ax, send=True, stored=STORED, stored_hot=True)
        label(ax, 2.0, 2.9, "kubectl apply -f order.yaml", fs=10, color=RED, bold=True, family=MONO)
        moral(ax, 6.0, 0.15, "문서는 저장소에 원하는 상태로 남아요. 파드는 아직 0개예요")


def ctrl_strip(ax, step):
    if step == 1:
        world(ax, stored=STORED, ctrl="원하는 건 3개, 지금은 0개\n3개 모자라요", ctrl_hot=True)
    elif step == 2:
        world(ax, stored=STORED, ctrl="모자란 3개를 만들어 달라고 할게요", ask=True,
              pods=[(n, "hot") for n, _ in PODS3], now_hot=True)
    else:
        world(ax, stored=STORED, ctrl="원하는 건 3개, 지금도 3개\n할 일이 없어요", ctrl_hot=True, pods=PODS3)
        moral(ax, 6.0, 0.15, "컨트롤러는 원하는 상태와 지금 상태를 비교해서 차이만큼 움직여요")


def loop_strip(ax, step):
    if step == 1:
        world(ax, stored=STORED, ctrl="", pods=[(P1, "gone")] + PODS3[1:], now_hot=True,
              user="kubectl delete pod order-7c9d-k2p4q")
    elif step == 2:
        world(ax, stored=STORED, ctrl="원하는 건 3개, 지금은 2개\n하나 모자라요", ctrl_hot=True, pods=PODS3[1:])
    else:
        world(ax, stored=STORED, ctrl="하나를 새로 만들어 달라고 할게요", ask=True,
              pods=PODS3[1:] + [(P4, "hot")], now_hot=True)
        moral(ax, 6.0, 0.15, "지운 것은 지금 상태예요. 원하는 상태는 그대로라 다시 채워요")


def cycle():
    fig, ax = canvas(6.4, 4.6, 10, 7.2)
    pts = {"watch": (5.0, 6.0), "cmp": (8.2, 2.4), "act": (1.8, 2.4)}
    names = {"watch": "① 지켜보기\n지금 상태를 봐요", "cmp": "② 비교하기\n원하는 상태와 다른지 봐요",
             "act": "③ 맞추기\n차이만큼 만들거나 지워요"}
    for k, (x, y) in pts.items():
        hot = k == "act"
        box(ax, x - 1.55, y - 0.65, 3.1, 1.3, fc=PINK if hot else NOTE, ec=RED if hot else INK)
        label(ax, x, y, names[k], fs=10.5, color=RED if hot else "#222")
    for a, b in (("watch", "cmp"), ("cmp", "act"), ("act", "watch")):
        (x1, y1), (x2, y2) = pts[a], pts[b]
        ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>", mutation_scale=16, color=RED, lw=2,
                                     connectionstyle="arc3,rad=-0.35", shrinkA=42, shrinkB=42))
    label(ax, 5.0, 3.4, "멈추지 않고\n계속 돌아요", fs=11.5, color=RED, bold=True)
    label(ax, 5.0, 0.35, "끝나지 않는 이 되풀이가 조정 루프예요", fs=11, color=INK)
    save(fig, OUT, "k8s07-cycle.svg")


# ── 언제 쓸모 있을까요: 갈림길 ──────────────────────────────────────
def decide():
    fig, ax = canvas(7.6, 4.6, 15, 9)
    box(ax, 0.3, 7.4, 8.4, 1.2, fc=NOTE)
    label(ax, 4.5, 8.0, "바꾼 것이 앞으로도 계속 남아야 하나요?", fs=11, bold=True)
    arrow(ax, (8.8, 8.0), (10.0, 8.0), color=RED); label(ax, 9.4, 8.35, "예", fs=10, color=RED)
    box(ax, 10.1, 7.2, 4.6, 1.6, fc=PINK, ec=RED)
    label(ax, 12.4, 8.0, "매니페스트를 고쳐서\n다시 보내요 (apply)", fs=10.5, color=RED, bold=True)
    arrow(ax, (4.5, 7.3), (4.5, 6.1)); label(ax, 4.8, 6.7, "아니요", fs=10, color=INK, ha="left")
    box(ax, 0.3, 4.6, 8.4, 1.4, fc=NOTE)
    label(ax, 4.5, 5.3, "고장 난 파드 하나를\n새로 띄우고 싶나요?", fs=10.5, bold=True)
    arrow(ax, (8.8, 5.3), (10.0, 5.3)); label(ax, 9.4, 5.65, "예", fs=10, color=INK)
    box(ax, 10.1, 4.5, 4.6, 1.6, fc=PAPER)
    label(ax, 12.4, 5.3, "그 파드를 지워요\n컨트롤러가 새로 만들어요", fs=10.5)
    arrow(ax, (4.5, 4.5), (4.5, 3.3)); label(ax, 4.8, 3.9, "아니요, 지금 모습만 보고 싶어요", fs=10, color=INK, ha="left")
    box(ax, 0.3, 1.8, 8.4, 1.4, fc=PAPER)
    label(ax, 4.5, 2.5, "명령으로 봐요\n(kubectl get, kubectl logs)", fs=10.5)
    save(fig, OUT, "k8s07-decide.svg")


# ── 정리: 처음 장면으로 돌아가기 ───────────────────────────────────
def back(ax, step):
    if step == 1:
        lines = [(f"$ kubectl delete pod {P1}", "dim"), ("$ kubectl get pods", "dim"),
                 (f"{P2}    1/1     2d", "dim"), (f"{P3}    1/1     2d", "dim"), (f"{P4}    1/1     3s", "dim")]
        terminal(ax, 0.3, 1.6, 11.4, 3.9, lines)
        label(ax, 6.0, 0.8, "처음: 지운 파드는 컨트롤러가 다시 채웠어요", fs=11.5, color=INK)
    elif step == 2:
        manifest(ax, 0.6, 2.2, ["kind: Deployment", "name: order", "replicas: 2", "image: order:1"], hot=(2,), w=4.2)
        terminal(ax, 5.4, 2.2, 6.3, 2.0, [("$ kubectl apply -f order.yaml", "hot"),
                                         ("deployment.apps/order configured", "")])
        label(ax, 6.0, 1.2, "이번에는 원하는 상태를 3개에서 2개로 고쳐 보내요", fs=11.5, color=RED, bold=True)
    else:
        lines = [("$ kubectl get pods", "cmd"), ("NAME                READY   AGE", ""),
                 (f"{P2}    1/1     2d", ""), (f"{P4}    1/1     5m", ""), ("# 2개만 남았어요", "hot")]
        terminal(ax, 0.3, 1.6, 11.4, 3.9, lines)
        moral(ax, 6.0, 0.8, "파드를 줄이려면 지우지 말고 원하는 상태를 고쳐요")


# ── 정리: 낱말 카드 ────────────────────────────────────────────────
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

    x, y = card(0, "매니페스트", "원하는 상태를 적은 문서")
    ax.add_patch(Rectangle((x + 1.2, y + 1.25), 2.2, 1.6, fc="white", ec=INK, lw=1.3))
    for k, (s, on) in enumerate((("name: order", False), ("replicas: 3", True))):
        ax.text(x + 1.35, y + 2.5 - k * 0.5, s, fontsize=9.5, family=MONO, ha="left", va="center",
                color=RED if on else "#222", fontweight="bold" if on else "normal")
    x, y = card(1, "Deployment", "파드를 몇 개, 어떤 모습으로\n띄울지 적는 문서 종류")
    for k in range(3):
        pod(ax, x + 0.4 + k * 1.3, y + 1.6, "order", hot=k == 2, w=1.1, h=0.7, fs=9)
    x, y = card(2, "컨트롤러", "원하는 상태와 지금 상태를\n계속 비교해서 맞추는 일꾼")
    label(ax, x + 1.2, y + 2.3, "원하는 3", fs=10.5)
    label(ax, x + 3.3, y + 2.3, "지금 2", fs=10.5, color=RED, bold=True)
    label(ax, x + 2.25, y + 2.3, "≠", fs=13, color=RED, bold=True)
    label(ax, x + 2.3, y + 1.6, "→ 하나 더 만들어요", fs=10, color=RED)
    x, y = card(3, "조정 루프", "지켜보기·비교하기·맞추기를\n멈추지 않고 되풀이하는 것")
    cx, cy, r = x + 2.3, y + 2.05, 0.6
    for a, b in ((90, 330), (330, 210), (210, 90)):
        p1 = (cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a)))
        p2 = (cx + r * math.cos(math.radians(b)), cy + r * math.sin(math.radians(b)))
        ax.add_patch(FancyArrowPatch(p1, p2, arrowstyle="-|>", mutation_scale=11, color=RED, lw=1.8,
                                     connectionstyle="arc3,rad=-0.5"))
    save(fig, OUT, "k8s07-cards.svg")


if __name__ == "__main__":
    S, L = (7.2, 3.8), (12, 6.6)
    stage(opening, 3, OUT, "k8s07-open", S, L)
    stage(thermo, 4, OUT, "k8s07-thermo", S, L)
    stage(manifest_strip, 2, OUT, "k8s07-manifest", S, L)
    stage(ctrl_strip, 3, OUT, "k8s07-ctrl", S, L)
    stage(loop_strip, 3, OUT, "k8s07-loop", S, L)
    cycle()
    decide()
    stage(back, 3, OUT, "k8s07-back", S, L)
    cards()
