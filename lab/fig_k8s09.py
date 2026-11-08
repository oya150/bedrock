"""쿠버네티스 9편 그림 만들기. 실행: python lab/fig_k8s09.py  → docs/kubernetes/img/09/*.svg

본문 절은 장면 띠로 그린다: 같은 무대를 여러 장 그리고 장마다 바뀐 곳만 빨강으로 칠한다.
예시는 빵집 주문 앱. 주문 화면 파드가 주문 처리 파드(order)를 찾아간다.
옛 파드 IP 10.1.0.5~7, 8편 교대 뒤 10.1.0.8~10, Service order 의 주소 10.96.0.20.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "es"))
sys.path.insert(0, os.path.dirname(__file__))
from figkit import (GREY, INK, LIGHT, NOTE, PAPER, PINK, RED, arrow, box, bubble,  # noqa: E402
                    canvas, label, moral, outdir, save, stage)
from matplotlib.patches import Rectangle  # noqa: E402
from fig_k8s07 import MONO  # noqa: E402

OUT = outdir("09", topic="kubernetes")
SVC_IP = "10.96.0.20"


def ip_pod(ax, x, y, ip, tag=None, hot=False, dim=False, gone=False, wait=False, tag_hot=False, w=3.0, h=0.95,
           name="주문 처리 파드"):
    """IP가 적힌 파드. tag=라벨 글(app=order)."""
    if gone:
        ax.add_patch(Rectangle((x, y), w, h, fill=False, ec=RED, lw=1.6, ls="--"))
        label(ax, x + w / 2, y + h * 0.66, name, fs=9.5, color=RED)
        label(ax, x + w / 2, y + h * 0.3, ip, fs=10, color=RED, family=MONO)
        label(ax, x + w - 0.15, y + h - 0.15, "✗", fs=13, color=RED, bold=True)
    else:
        c = RED if (hot or wait) else (GREY if dim else "#222")
        ax.add_patch(Rectangle((x, y), w, h, fc=PINK if (hot or wait) else (LIGHT if dim else NOTE),
                               ec=RED if (hot or wait) else (GREY if dim else INK), lw=1.8 if hot else 1.3,
                               ls="--" if wait else "-"))
        label(ax, x + w / 2, y + h * 0.66, name + (" (준비 중)" if wait else ""), fs=9.5, color=c, bold=hot)
        label(ax, x + w / 2, y + h * 0.3, ip, fs=10, color=c, family=MONO, bold=hot)
    if tag:
        tc = RED if tag_hot else INK
        ax.text(x + w + 0.1, y + h / 2, tag, fontsize=9, family=MONO, color=tc, ha="left", va="center",
                bbox=dict(boxstyle="round,pad=0.25", fc=PINK if tag_hot else "white", ec=tc, lw=1.1))


def web(ax, x=0.3, y=2.75, addr="10.1.0.5", hot=False):
    box(ax, x, y, 2.9, 1.3, fc=NOTE)
    label(ax, x + 1.45, y + 0.95, "주문 화면 파드", fs=10.5, bold=True)
    label(ax, x + 1.45, y + 0.5, "주문 처리 주소:", fs=9, color=INK)
    label(ax, x + 1.45, y + 0.18, addr, fs=9.5, family=MONO, color=RED if hot else "#222", bold=hot)


def phone(ax, msg=None, msg_hot=False, btn_hot=False, dim=False):
    ec = GREY if dim else INK
    box(ax, 0.4, 0.7, 2.8, 5.5, fc="white", ec=ec, lw=1.8)
    ax.add_patch(Rectangle((0.4, 5.6), 2.8, 0.6, fc=LIGHT, ec=ec, lw=1.2))
    c = GREY if dim else "#222"
    label(ax, 1.8, 5.9, "동네 빵집", fs=11, bold=True, color=c)
    label(ax, 0.65, 5.1, "크루아상", fs=10.5, ha="left", color=c)
    label(ax, 2.95, 5.1, "2", fs=10.5, ha="right", color=c)
    label(ax, 0.65, 4.55, "식빵", fs=10.5, ha="left", color=c)
    label(ax, 2.95, 4.55, "1", fs=10.5, ha="right", color=c)
    ax.plot([0.6, 3.0], [4.2, 4.2], color=GREY, lw=0.8)
    ax.add_patch(Rectangle((0.7, 3.25), 2.2, 0.6, fc=PINK if btn_hot else LIGHT, ec=RED if btn_hot else ec, lw=1.5))
    label(ax, 1.8, 3.55, "주문하기", fs=11, color=RED if btn_hot else c, bold=btn_hot)
    if msg:
        label(ax, 1.8, 2.2, msg, fs=10, color=RED if msg_hot else c, bold=msg_hot)


OLD = ["10.1.0.5", "10.1.0.6", "10.1.0.7"]
NEW = ["10.1.0.8", "10.1.0.9", "10.1.0.10"]
PY = [4.7, 3.25, 1.8]


# ── 여는 장면 ──────────────────────────────────────────────────────
def opening(ax, step):
    if step == 1:
        phone(ax, "주문이 들어갔어요", msg_hot=True, btn_hot=True)
        web(ax, x=4.0, y=3.25)
        arrow(ax, (3.3, 3.55), (3.95, 3.85), color=RED, ms=12)
        for k, ip in enumerate(OLD):
            ip_pod(ax, 8.6, PY[k], ip)
        arrow(ax, (6.95, 3.9), (8.55, 5.15), color=RED, ms=14)
    elif step == 2:
        phone(ax)
        web(ax, x=4.0, y=3.25)
        for k, ip in enumerate(NEW):
            ip_pod(ax, 8.6, PY[k], ip, hot=True)
        label(ax, 10.1, 0.95, "8편의 교대로 파드가\n모두 새로 떴어요", fs=10.5, color=RED, bold=True)
    else:
        phone(ax, "주문을 보낼 수\n없어요", msg_hot=True, btn_hot=True)
        web(ax, x=4.0, y=3.25, hot=True)
        arrow(ax, (3.3, 3.55), (3.95, 3.85), color=RED, ms=12)
        for k, ip in enumerate(NEW):
            ip_pod(ax, 8.6, PY[k], ip)
        ip_pod(ax, 4.2, 5.35, "10.1.0.5", gone=True, w=2.6, h=0.85)
        arrow(ax, (5.5, 4.6), (5.5, 5.3), color=RED, ms=12)
        moral(ax, 6.0, 0.25, "적어 둔 주소의 파드가 이제 없어요")


def ipchange():
    fig, ax = canvas(7.2, 2.6, 12, 4.4)
    ip_pod(ax, 0.5, 1.6, "10.1.0.5", gone=True)
    arrow(ax, (3.7, 2.07), (7.7, 2.07), color=RED, ms=16)
    label(ax, 5.7, 2.55, "지우고 새로 만들어요", fs=10.5, color=RED)
    label(ax, 5.7, 1.6, "(7편 컨트롤러, 8편 교대)", fs=10, color=INK)
    ip_pod(ax, 7.9, 1.6, "10.1.0.8", hot=True)
    label(ax, 2.0, 0.9, "옛 파드", fs=10.5, color=INK)
    label(ax, 9.4, 0.9, "새 파드는 새 IP", fs=10.5, color=RED, bold=True)
    moral(ax, 6.0, 0.25, "파드를 새로 만들면 IP도 새로 받아요")
    save(fig, OUT, "k8s09-ip.svg")


# ── Service ────────────────────────────────────────────────────────
def service(ax, x=4.2, y=2.75, hot=False, sel=None, sel_hot=False):
    ec = RED if hot else INK
    box(ax, x, y, 3.0, 1.3, fc=PINK if hot else PAPER, ec=ec, lw=2.0 if hot else 1.5)
    label(ax, x + 1.5, y + 0.95, "Service order", fs=11, bold=True, color=RED if hot else "#222")
    label(ax, x + 1.5, y + 0.4, SVC_IP, fs=10.5, family=MONO, color=RED if hot else "#222")
    if sel:
        tc = RED if sel_hot else INK
        ax.text(x + 1.5, y - 0.4, f"셀렉터 {sel}", fontsize=9.5, family=MONO, color=tc, ha="center", va="center",
                bbox=dict(boxstyle="round,pad=0.25", fc=PINK if sel_hot else "white", ec=tc, lw=1.2),
                fontweight="bold" if sel_hot else "normal")


def svc_strip(ax, step):
    web(ax, addr=SVC_IP, hot=step == 1)
    service(ax, hot=step == 1)
    ips = NEW[:]
    if step == 3:
        ips[1] = "10.1.0.11"
    for k, ip in enumerate(ips):
        ip_pod(ax, 8.6, PY[k], ip, hot=(step == 2 and k == 1) or (step == 3 and k == 1))
    if step == 1:
        label(ax, 5.7, 5.4, "바뀌지 않는 주소 하나를 앞에 세워요", fs=11, color=RED, bold=True)
        for k in range(3):
            arrow(ax, (7.3, 3.4), (8.55, PY[k] + 0.47), color=GREY, ms=11)
    elif step == 2:
        arrow(ax, (3.3, 3.4), (4.15, 3.4), color=RED, ms=13)
        arrow(ax, (7.3, 3.4), (8.55, PY[1] + 0.47), color=RED, ms=13)
        label(ax, 5.7, 5.4, "주문은 셋 중 한 파드로 가요", fs=11, color=RED, bold=True)
    else:
        arrow(ax, (3.3, 3.4), (4.15, 3.4), color=GREY, ms=13)
        arrow(ax, (7.3, 3.4), (8.55, PY[1] + 0.47), color=RED, ms=13)
        label(ax, 5.7, 5.4, "10.1.0.9가 바뀌어도 같은 주소로 보내요", fs=11, color=RED, bold=True)
        moral(ax, 6.0, 0.6, "주소는 그대로이고 받는 파드만 바뀌어요")


# ── 라벨 셀렉터 ────────────────────────────────────────────────────
LY = [5.2, 3.95, 2.7, 1.45]


def eplist(ax, items, x=4.0, y=0.1):
    """주소 목록(EndpointSlice). items=[(ip, 상태)] 상태 ""·"hot"·"gone"."""
    box(ax, x, y, 3.6, 0.5 + 0.42 * len(items), fc="white")
    label(ax, x + 1.8, y + 0.25 + 0.42 * len(items), "주소 목록", fs=10, color=INK, bold=True)
    for k, (ip, st) in enumerate(items):
        yy = y + 0.05 + 0.42 * (len(items) - k) - 0.15
        c = RED if st else "#222"
        label(ax, x + 1.8, yy, ip, fs=10, family=MONO, color=c, bold=st == "hot")
        if st == "gone":
            ax.plot([x + 1.0, x + 2.6], [yy, yy], color=RED, lw=1.6)


def label_strip(ax, step):
    web(ax, y=4.0, addr=SVC_IP)
    service(ax, x=4.2, y=4.0, sel="app=order", sel_hot=step == 1)
    pods = [("10.1.0.8", "app=order"), ("10.1.0.9", "app=order"), ("10.1.0.10", "app=order")]
    for k, (ip, tag) in enumerate(pods):
        gone = step == 3 and k == 1
        ip_pod(ax, 8.0, LY[k], ip, tag=tag, tag_hot=step == 1, gone=gone, w=2.4, h=0.9)
    ip_pod(ax, 0.3, 1.9, "10.1.0.4", tag="app=web", name="주문 화면 파드", w=2.4, h=0.9)
    if step == 1:
        label(ax, 1.5, 1.4, "라벨이 달라서 빠져요", fs=9.5, color=RED)
        eplist(ax, [(ip, "") for ip, _ in pods], y=0.3)
        arrow(ax, (7.25, 4.3), (7.95, LY[0] + 0.45), color=RED, ms=11)
        arrow(ax, (7.25, 4.3), (7.95, LY[1] + 0.45), color=RED, ms=11)
        arrow(ax, (7.25, 4.3), (7.95, LY[2] + 0.45), color=RED, ms=11)
    elif step == 2:
        ip_pod(ax, 8.0, LY[3], "10.1.0.11", tag="app=order", wait=True, w=2.4, h=0.9, name="새 파드")
        eplist(ax, [(ip, "") for ip, _ in pods], y=0.3)
        label(ax, 9.2, 0.95, "라벨은 맞지만\n아직 목록에 없어요", fs=9.5, color=RED)
    else:
        ip_pod(ax, 8.0, LY[3], "10.1.0.11", tag="app=order", w=2.4, h=0.9)
        eplist(ax, [("10.1.0.8", ""), ("10.1.0.9", "gone"), ("10.1.0.10", ""), ("10.1.0.11", "hot")], y=0.1)
        moral(ax, 9.5, 0.45, "라벨이 맞고 준비된\n파드만 목록에 올라요", fs=11)


# ── DNS ────────────────────────────────────────────────────────────
def dns_strip(ax, step):
    web(ax, x=0.3, y=1.2, addr="order")
    box(ax, 7.6, 3.6, 4.1, 2.4, fc=NOTE, ec=RED if step == 1 else INK)
    label(ax, 9.65, 5.6, "DNS (이름 → 주소)", fs=11, bold=True)
    rows = [("order", SVC_IP), ("pay", "10.96.0.31"), ("ledger", "10.96.0.47")]
    for k, (n, ip) in enumerate(rows):
        hot = k == 0 and step == 2
        label(ax, 8.0, 5.0 - k * 0.5, n, fs=10, family=MONO, ha="left", color=RED if hot else "#222", bold=hot)
        label(ax, 11.4, 5.0 - k * 0.5, ip, fs=10, family=MONO, ha="right", color=RED if hot else "#222", bold=hot)
    service(ax, x=7.9, y=0.6)
    if step == 1:
        bubble(ax, 0.3, 3.6, 4.6, 1.2, "order는 어느 주소예요?", (1.7, 2.55), hot=True)
        arrow(ax, (5.0, 4.2), (7.5, 4.6), color=RED, ms=13)
    else:
        bubble(ax, 0.3, 3.6, 4.6, 1.2, f"{SVC_IP}로 보낼게요", (1.7, 2.55), hot=True)
        arrow(ax, (7.5, 4.9), (5.0, 4.5), color=RED, ms=13)
        label(ax, 6.25, 5.1, SVC_IP, fs=10, family=MONO, color=RED)
        arrow(ax, (3.3, 1.85), (7.85, 1.25), color=RED, ms=13)
        moral(ax, 4.0, 0.25, "이름만 알면 주소는 DNS가 알려 줘요")


# ── 갈림길 ─────────────────────────────────────────────────────────
def decide():
    fig, ax = canvas(7.6, 4.6, 15, 9)
    box(ax, 0.3, 7.4, 8.4, 1.2, fc=NOTE)
    label(ax, 4.5, 8.0, "다른 파드가 이 파드들을 찾아와야 하나요?", fs=11, bold=True)
    arrow(ax, (8.8, 8.0), (10.0, 8.0)); label(ax, 9.4, 8.35, "아니요", fs=10, color=INK)
    box(ax, 10.1, 7.2, 4.6, 1.6, fc=PAPER)
    label(ax, 12.4, 8.0, "Service가 필요 없어요\n(혼자 도는 정리 작업)", fs=10.5)
    arrow(ax, (4.5, 7.3), (4.5, 6.1)); label(ax, 4.8, 6.7, "예", fs=10, color=INK, ha="left")
    box(ax, 0.3, 4.6, 8.4, 1.4, fc=NOTE)
    label(ax, 4.5, 5.3, "그중 아무 파드나 받아도 되나요?", fs=10.5, bold=True)
    arrow(ax, (8.8, 5.3), (10.0, 5.3), color=RED); label(ax, 9.4, 5.65, "예", fs=10, color=RED)
    box(ax, 10.1, 4.5, 4.6, 1.6, fc=PINK, ec=RED)
    label(ax, 12.4, 5.3, "보통 Service\n이름 하나, 주소 하나", fs=10.5, color=RED, bold=True)
    arrow(ax, (4.5, 4.5), (4.5, 3.3)); label(ax, 4.8, 3.9, "아니요, 정해진 파드 하나를 불러야 해요", fs=10, color=INK, ha="left")
    box(ax, 0.3, 1.6, 8.4, 1.6, fc=PAPER)
    label(ax, 4.5, 2.4, "대표 주소 없는 Service (headless)\nDNS가 파드 주소들을 그대로 알려 줘요", fs=10.5)
    save(fig, OUT, "k8s09-decide.svg")


# ── 정리 ───────────────────────────────────────────────────────────
def back(ax, step):
    if step == 1:
        phone(ax, "주문을 보낼 수\n없어요", dim=True)
        web(ax, x=4.0, y=3.25)
        ip_pod(ax, 4.2, 5.35, "10.1.0.5", dim=True, w=2.6, h=0.85)
        for k, ip in enumerate(NEW):
            ip_pod(ax, 8.6, PY[k], ip, dim=True)
        label(ax, 6.0, 0.6, "처음: IP를 적어 둬서 파드가 바뀌자 주문이 막혔어요", fs=11.5, color=INK)
    elif step == 2:
        phone(ax)
        web(ax, x=4.0, y=3.25, addr="order", hot=True)
        for k, ip in enumerate(NEW):
            ip_pod(ax, 8.6, PY[k], ip)
        label(ax, 5.45, 2.7, "IP 대신 Service 이름을 적어요", fs=10.5, color=RED, bold=True)
    else:
        phone(ax, "주문이 들어갔어요", msg_hot=True, btn_hot=True)
        web(ax, x=4.0, y=3.25, addr="order")
        arrow(ax, (3.3, 3.55), (3.95, 3.85), color=RED, ms=12)
        box(ax, 4.15, 5.3, 2.6, 0.75, fc=PINK, ec=RED)
        label(ax, 5.45, 5.68, "DNS: order → Service", fs=9.5, color=RED)
        arrow(ax, (5.45, 4.6), (5.45, 5.25), color=RED, ms=10)
        box(ax, 4.15, 1.6, 2.6, 0.95, fc=PINK, ec=RED)
        label(ax, 5.45, 2.07, f"Service {SVC_IP}", fs=9.5, color=RED)
        arrow(ax, (5.45, 3.2), (5.45, 2.6), color=RED, ms=10)
        for k, ip in enumerate(NEW):
            ip_pod(ax, 8.6, PY[k], ip, hot=k == 2)
        arrow(ax, (6.8, 2.07), (8.55, PY[2] + 0.47), color=RED, ms=12)
        moral(ax, 7.2, 0.2, "이름 하나로 지금 떠 있는 파드를 찾아가요")


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

    x, y = card(0, "Service", "바뀌지 않는 이름과 주소\n뒤의 파드 중 하나로 넘겨요")
    box(ax, x + 0.4, y + 1.55, 1.9, 0.9, fc=PINK, ec=RED)
    label(ax, x + 1.35, y + 2.0, "order", fs=10.5, color=RED, bold=True, family=MONO)
    for k in range(3):
        arrow(ax, (x + 2.4, y + 2.0), (x + 3.1, y + 2.55 - k * 0.5), ms=9)
        box(ax, x + 3.15, y + 2.35 - k * 0.5, 1.0, 0.38, fc=NOTE, lw=1.1)
    x, y = card(1, "라벨 셀렉터", "라벨이 맞는 파드를\n모두 고르는 조건")
    ax.text(x + 0.5, y + 2.0, "app=order", fontsize=10, family=MONO, color=RED, ha="left", va="center",
            bbox=dict(boxstyle="round,pad=0.25", fc=PINK, ec=RED, lw=1.2))
    ax.text(x + 2.6, y + 2.35, "app=order ✓", fontsize=9, family=MONO, color="#222", ha="left", va="center")
    ax.text(x + 2.6, y + 1.65, "app=web", fontsize=9, family=MONO, color=GREY, ha="left", va="center")
    x, y = card(2, "DNS", "이름을 주소로 바꿔 주는\n전화번호부")
    label(ax, x + 2.3, y + 2.0, f"order → {SVC_IP}", fs=10.5, family=MONO, color=RED, bold=True)
    x, y = card(3, "EndpointSlice", "Service 뒤에 선 준비된 파드의\n주소 목록 (계속 고쳐져요)")
    for k, (ip, st) in enumerate((("10.1.0.8", ""), ("10.1.0.10", ""), ("10.1.0.11", "hot"))):
        label(ax, x + 2.3, y + 2.55 - k * 0.42, ip, fs=10, family=MONO, color=RED if st else "#222", bold=bool(st))
    save(fig, OUT, "k8s09-cards.svg")


if __name__ == "__main__":
    S, L = (7.2, 3.8), (12, 6.6)
    stage(opening, 3, OUT, "k8s09-open", S, L)
    ipchange()
    stage(svc_strip, 3, OUT, "k8s09-svc", S, L)
    stage(label_strip, 3, OUT, "k8s09-label", S, L)
    stage(dns_strip, 2, OUT, "k8s09-dns", S, L)
    decide()
    stage(back, 3, OUT, "k8s09-back", S, L)
    cards()
