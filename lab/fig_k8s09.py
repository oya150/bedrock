"""쿠버네티스 9편 그림 만들기. 실행: python lab/fig_k8s09.py  → docs/kubernetes/img/09/*.svg

그림 안 글씨는 낱말과 숫자만 둔다. 장면 띠는 라벨 절의 세 장뿐이다.
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


# ── 1절: 파드 IP가 바뀌어 주문이 막힘 ────────────────────────────
def opening(ax, step):
    if step == 1:
        phone(ax, "주문 완료", msg_hot=True, btn_hot=True)
        web(ax, x=4.0, y=3.25, addr="10.1.0.5")
        arrow(ax, (3.3, 3.55), (3.95, 3.85), color=RED, ms=12)
        for k, ip in enumerate(OLD):
            ip_pod(ax, 8.6, PY[k], ip, hot=k == 0)
        arrow(ax, (6.95, 3.9), (8.55, 5.15), color=RED, ms=14)
    else:
        phone(ax, "주문 실패", msg_hot=True, btn_hot=True)
        web(ax, x=4.0, y=3.25, addr="10.1.0.5", hot=True)
        arrow(ax, (3.3, 3.55), (3.95, 3.85), color=RED, ms=12)
        label(ax, 10.1, 5.95, "교대 뒤 새 파드", fs=10, color=INK)
        for k, ip in enumerate(NEW):
            ip_pod(ax, 8.6, PY[k], ip)
        ip_pod(ax, 4.2, 5.35, "10.1.0.5", gone=True, w=2.6, h=0.85)
        arrow(ax, (5.5, 4.6), (5.5, 5.3), color=RED, ms=12)


# ── 2절: Service ───────────────────────────────────────────────────
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
    if step == 2:
        ips[1] = "10.1.0.11"
    for k, ip in enumerate(ips):
        ip_pod(ax, 8.6, PY[k], ip, hot=k == 1)
    arrow(ax, (3.3, 3.4), (4.15, 3.4), color=RED if step == 1 else INK, ms=13)
    arrow(ax, (7.3, 3.4), (8.55, PY[1] + 0.47), color=RED, ms=13)


# ── 3·4절: 라벨 셀렉터와 주소 목록 ──────────────────────────────────
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
    service(ax, x=4.2, y=4.0, sel="app=order", sel_hot=step == 1)
    pods = [("10.1.0.8", "app=order"), ("10.1.0.9", "app=order"), ("10.1.0.10", "app=order")]
    for k, (ip, tag) in enumerate(pods):
        gone = step == 3 and k == 1
        ip_pod(ax, 8.0, LY[k], ip, tag=tag, tag_hot=step == 1, gone=gone, w=2.4, h=0.9)
    ip_pod(ax, 0.3, 1.9, "10.1.0.4", tag="app=web", name="주문 화면 파드", w=2.4, h=0.9)
    if step == 1:
        label(ax, 1.5, 1.4, "제외", fs=10, color=RED, bold=True)
        eplist(ax, [(ip, "") for ip, _ in pods], y=0.3)
        for k in range(3):
            arrow(ax, (7.25, 4.3), (7.95, LY[k] + 0.45), color=RED, ms=11)
    elif step == 2:
        ip_pod(ax, 8.0, LY[3], "10.1.0.11", tag="app=order", wait=True, w=2.4, h=0.9, name="새 파드")
        eplist(ax, [(ip, "") for ip, _ in pods], y=0.3)
    else:
        ip_pod(ax, 8.0, LY[3], "10.1.0.11", tag="app=order", w=2.4, h=0.9)
        eplist(ax, [("10.1.0.8", ""), ("10.1.0.9", "gone"), ("10.1.0.10", ""), ("10.1.0.11", "hot")], y=0.1)


# ── 5절: DNS ───────────────────────────────────────────────────────
def dns():
    fig, ax = canvas(7.2, 3.8, 12, 6.6)
    web(ax, x=0.3, y=2.6, addr="order")
    box(ax, 7.6, 3.9, 4.1, 2.3, fc=NOTE, ec=INK)
    label(ax, 9.65, 5.8, "DNS", fs=11, bold=True)
    rows = [("order", SVC_IP), ("pay", "10.96.0.31"), ("ledger", "10.96.0.47")]
    for k, (n, ip) in enumerate(rows):
        hot = k == 0
        label(ax, 8.0, 5.25 - k * 0.5, n, fs=10, family=MONO, ha="left", color=RED if hot else "#222", bold=hot)
        label(ax, 11.4, 5.25 - k * 0.5, ip, fs=10, family=MONO, ha="right", color=RED if hot else "#222", bold=hot)
    arrow(ax, (3.3, 3.95), (7.5, 5.25), color=RED, ms=13)
    label(ax, 5.2, 4.95, "① order?", fs=10, color=RED)
    arrow(ax, (7.5, 4.75), (3.3, 3.55), color=RED, ms=13)
    label(ax, 5.9, 3.75, f"② {SVC_IP}", fs=10, family=MONO, color=RED)
    service(ax, x=7.9, y=0.5)
    arrow(ax, (3.3, 2.9), (7.85, 1.15), color=RED, ms=13)
    label(ax, 5.0, 1.55, "③ 보내기", fs=10, color=RED)
    save(fig, OUT, "k8s09-dns.svg")


# ── 6절: 보통 Service와 headless ───────────────────────────────────
def headless():
    fig, ax = canvas(7.8, 3.6, 13.4, 6.2)
    pods_n = ["10.1.0.8", "10.1.0.9", "10.1.0.10"]
    pods_h = ["10.1.0.21", "10.1.0.22", "10.1.0.23"]
    for col, (title, name, ans, pods, hot) in enumerate((
            ("보통 Service", "order", [SVC_IP], pods_n, False),
            ("headless Service", "ledger", pods_h, pods_h, True))):
        x0 = 0.2 + col * 6.8
        label(ax, x0 + 3.0, 5.8, title, fs=12, bold=True, color=RED if hot else "#222")
        box(ax, x0, 3.6, 2.4, 1.6, fc=NOTE)
        label(ax, x0 + 1.2, 4.95, "DNS", fs=10.5, bold=True)
        label(ax, x0 + 1.2, 4.45, name, fs=10, family=MONO)
        arrow(ax, (x0 + 2.5, 4.4), (x0 + 3.35, 4.4), color=RED if hot else INK, ms=12)
        for k, a in enumerate(ans):
            label(ax, x0 + 4.6, 4.4 + (len(ans) - 1) * 0.22 - k * 0.44, a, fs=10, family=MONO,
                  color=RED if hot else "#222", bold=hot)
        name2 = "장부 파드" if hot else "주문 처리"
        for k, ip in enumerate(pods):
            ip_pod(ax, x0 + k * 2.1, 0.7, ip, w=1.95, h=0.95, name=name2)
            if hot:
                arrow(ax, (x0 + 4.6, 3.75), (x0 + 0.97 + k * 2.1, 1.7), color=RED, ms=10)
        if not hot:
            arrow(ax, (x0 + 4.6, 4.1), (x0 + 3.07, 1.7), color=INK, ms=10)
        if hot:
            label(ax, x0 + 3.2, 0.25, "부르는 쪽이 선택", fs=10, color=RED)
        else:
            label(ax, x0 + 3.2, 0.25, "셋 중 아무나", fs=10, color=INK)
    ax.plot([6.6, 6.6], [0.3, 6.0], color=GREY, lw=1.2, ls="--")
    save(fig, OUT, "k8s09-headless.svg")


def one(draw, step, name, size=(7.2, 3.8), lim=(12, 6.6)):
    fig, ax = canvas(*size, *lim)
    ax.add_patch(Rectangle((0, 0), *lim, fill=False, ec="none"))
    draw(ax, step)
    save(fig, OUT, name)


if __name__ == "__main__":
    one(opening, 1, "k8s09-open-1.svg")
    one(opening, 2, "k8s09-open-2.svg")
    one(svc_strip, 1, "k8s09-svc-1.svg")
    one(svc_strip, 2, "k8s09-svc-2.svg")
    stage(label_strip, 3, OUT, "k8s09-label", (7.2, 3.8), (12, 6.6))
    dns()
    headless()
