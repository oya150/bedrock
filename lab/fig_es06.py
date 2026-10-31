"""Elasticsearch 6편 그림 만들기. 실행: python lab/fig_es06.py  → docs/elasticsearch/img/06/*.svg

본문 절은 장면 띠로 그린다: 같은 무대를 여러 장 그리고 장마다 바뀐 곳만 빨강으로 칠한다.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "es"))
from figkit import (GREY, INK, LIGHT, NOTE, PAPER, PINK, RED, arrow, bits, box, canvas, cell, cells,  # noqa: E402
                    label, letters, moral, outdir, save, stage, story)
from matplotlib.patches import Circle, Rectangle  # noqa: E402

OUT = outdir("06")


def open_():
    fig, ax = canvas(7.2, 3.6, 12, 6.0)
    for k, (title, mb, h) in enumerate((("낱말 글자만\n늘어놓기", "2.2 MB", 3.6), ("역색인\n(용어 사전 + 포스팅 목록)", "1.6 MB", 2.6))):
        x = 1.0 + k * 4.0
        ax.add_patch(Rectangle((x, 1.4), 2.0, h, fc=NOTE if k == 0 else PINK, ec=RED if k else INK, lw=1.6))
        label(ax, x + 1.0, 0.65, title, fs=12, color=RED if k else "#222")
        label(ax, x + 1.0, 1.4 + h / 2, mb, fs=13, color=RED if k else INK, bold=True)
    label(ax, 8.4, 3.4, "글 번호까지\n붙었는데\n더 작아요", fs=13, color=RED, ha="left", bold=True)
    save(fig, OUT, "es06-open.svg")


def map_():
    """정리 절: 이 편이 한 말을 결론 문장으로."""
    story(["용어 사전은 낱말을 블록으로 묶고 같은 앞부분은 한 번만 적어요",
           "작은 안내판으로 블록 하나를 골라 그 블록만 읽어요",
           "꼬리가 같은 칸까지 합친 FST는 트라이보다 더 작아요",
           "포스팅 목록은 앞 번호와의 차이만 필요한 비트만큼 적어요",
           "작게 담은 파일은 운영체제가 남는 메모리에 올려 빨리 읽어요"], -1, OUT, "es06-map.svg")


# ── 같은 앞부분은 한 번만 ──────────────────────────────────────────
WORDS = ["seal", "search", "searched", "searching", "season", "seat"]
REST = [w[3:] for w in WORDS]


def block(ax, step):
    label(ax, 0.3, 6.35, "정렬된 낱말 여섯", fs=12.5, ha="left", bold=True)
    x0 = 1.2
    for r, w in enumerate(WORDS):
        y = 4.55 - r * 0.68
        if step == 1:
            letters(ax, x0, y, w)
        elif step == 2:
            letters(ax, x0, y, w, hot=(0, 1, 2))
        else:
            letters(ax, x0, y, w, blank=(0, 1, 2))
    if step == 1:
        label(ax, 7.5, 3.0, "글자 칸 37개", fs=13, ha="left", bold=True)
        label(ax, 7.5, 2.3, "정렬하면 앞부분이\n같은 낱말끼리 붙어요", fs=11.5, ha="left", color=INK)
    elif step == 2:
        label(ax, 7.5, 3.0, "sea가 여섯 번", fs=13, ha="left", color=RED, bold=True)
        label(ax, 7.5, 2.3, "같은 글자 18칸이\n되풀이돼요", fs=11.5, ha="left", color=RED)
    else:
        letters(ax, x0, 5.45, "sea", hot=(0, 1, 2))
        label(ax, 3.0, 5.75, "← 블록 밖에 한 번만", fs=11.5, ha="left", color=RED)
        box(ax, x0 + 1.55, 0.95, 5.2, 4.3, fc="none", ec=INK, lw=1.4, round_=False)
        label(ax, x0 + 6.6, 5.05, "블록", fs=11, ha="right", color=INK)
        label(ax, 8.2, 3.0, "블록 안 19칸\n+ 앞부분 3칸", fs=13, ha="left", bold=True)
        label(ax, 8.2, 2.0, "37칸 → 22칸", fs=13, ha="left", color=RED, bold=True)
        moral(ax, 6.0, 0.35, "같은 앞부분은 한 번만 적고 나머지 글자만 적어요")


# ── 안내판 ────────────────────────────────────────────────────────
def node(ax, x, y, final=False, hot=False, dim=False):
    ec = RED if hot else (GREY if dim else INK)
    ax.add_patch(Circle((x, y), 0.28, fc=PINK if hot else "white", ec=ec, lw=2.2 if final else 1.3,
                        ls="--" if dim else "-"))
    if final:
        ax.add_patch(Circle((x, y), 0.19, fc="none", ec=ec, lw=1.0, ls="--" if dim else "-"))


def edge(ax, a, b, ch, hot=False, dim=False, rad=0.0, dy=0.25, at=None):
    color = RED if hot else (GREY if dim else INK)
    arrow(ax, a, b, color=color, lw=1.5, ms=10, rad=rad)
    x, y = at or ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2 + dy)
    ax.text(x, y, ch, ha="center", va="center", fontsize=12, color=color)


def index(ax, step):
    # 찾는 낱말
    box(ax, 8.6, 5.55, 3.1, 0.75, fc=PAPER)
    label(ax, 10.15, 5.92, "찾기: search", fs=12.5)
    # 디스크의 블록 줄
    label(ax, 0.3, 4.1, "디스크", fs=12, ha="left", bold=True)
    names = ["…", "블록 41", "블록 42", "블록 43", "…"]
    for k, n in enumerate(names):
        x = 0.3 + k * 2.35
        hot = step == 2 and k == 2
        if n == "…":
            label(ax, x + 1.0, 3.3, "…", fs=14, color=INK)
            continue
        box(ax, x, 2.9, 2.0, 0.8, fc=PINK if hot else NOTE, ec=RED if hot else INK, round_=False)
        label(ax, x + 1.0, 3.3, n, fs=11.5, color=RED if hot else "#222", bold=hot)
    if step == 1:
        label(ax, 6.0, 2.1, "블록이 수천 개예요. 하나씩 다 열어 보면 느려요", fs=12, color=RED)
        moral(ax, 6.0, 1.2, "search가 든 블록은 어떻게 고를까요?", fs=12)
        return
    # 메모리의 안내판
    label(ax, 0.3, 6.35, "메모리: 안내판", fs=12, ha="left", bold=True, color=RED if step == 2 else "#222")
    P = {"r": (0.7, 5.15), "s": (1.9, 5.15), "sa": (3.1, 5.85), "se": (3.1, 5.15), "sea": (4.3, 5.15), "sh": (3.1, 4.5)}
    hot_path = step == 2
    for k, (x, y) in P.items():
        node(ax, x, y, hot=hot_path and k in ("s", "se", "sea"))
    for a, b, ch, dy in (("r", "s", "s", 0.2), ("s", "sa", "a", 0.25), ("s", "se", "e", 0.15), ("se", "sea", "a", 0.2),
                         ("s", "sh", "h", -0.42)):
        (x1, y1), (x2, y2) = P[a], P[b]
        hot = hot_path and (a, b) in (("r", "s"), ("s", "se"), ("se", "sea"))
        edge(ax, (x1 + 0.28, y1), (x2 - 0.28, y2), ch, hot=hot, dy=dy)
    for k, (x, y, t) in {"sa": (3.45, 5.85, "블록 41"), "sea": (4.65, 5.15, "블록 42"), "sh": (3.45, 4.5, "블록 43")}.items():
        label(ax, x, y, "→ " + t, fs=11, ha="left", color=RED if hot_path and k == "sea" else INK)
    if step == 2:
        arrow(ax, (6.0, 4.95), (6.0, 3.75), color=RED, ms=14)
        label(ax, 6.3, 4.3, "s, e, a를 따라가면 블록 42", fs=11.5, ha="left", color=RED)
        label(ax, 6.0, 2.0, "블록마다 앞부분만 적은 작은 안내판이에요", fs=12, color=INK)
        return
    # step 3: 블록 42를 열어 훑는다
    ax.plot([5.0, 0.3], [2.9, 2.45], color=INK, lw=1, ls=":")
    ax.plot([7.0, 11.7], [2.9, 2.45], color=INK, lw=1, ls=":")
    box(ax, 0.3, 0.85, 11.4, 1.6, fc=NOTE, ec=INK, round_=False)
    label(ax, 0.5, 2.15, "블록 42 (앞부분 sea)", fs=11, ha="left", color=INK)
    label(ax, 11.5, 2.15, "sea + rch = search, 찾았어요", fs=11.5, ha="right", color=RED)
    x = 0.6
    for k, r in enumerate(REST):
        w = 0.36 * len(r) + 0.45
        hit = r == "rch"
        cell(ax, x, 1.05, w, 0.7, r, hot=hit, fs=12)
        x += w + 0.15
    moral(ax, 6.0, 0.3, "안내판으로 블록 하나만 골라 그 블록만 읽어요")


# ── 트라이 → FST ─────────────────────────────────────────────────
# 앞 절과 같은 sea 낱말로 이어 간다.
P4 = {"r": (0.5, 3.5), "s": (1.8, 3.5), "se": (3.1, 3.5), "sea": (4.4, 3.5), "seal": (5.8, 4.7), "seat": (5.8, 2.3),
      "seals": (7.1, 4.7), "seats": (7.1, 2.3)}
R = 0.28


def stem(ax, hot=(), vals=None):
    """s, e, a 줄기. vals가 있으면 '글자 / 값'으로 적는다."""
    for a, b, ch in (("r", "s", "s"), ("s", "se", "e"), ("se", "sea", "a")):
        t = f"{ch} / {vals[ch + b]}" if vals else ch
        edge(ax, (P4[a][0] + R, 3.5), (P4[b][0] - R, 3.5), t, hot=b in hot)


def trie(ax, step):
    label(ax, 0.3, 6.35, "낱말 넷: seal, seals, seat, seats", fs=12.5, ha="left", bold=True)
    for k, (x, y) in P4.items():
        final = k in ("seal", "seals", "seat", "seats")
        if k in ("seat", "seats"):
            if step == 3:
                continue
            node(ax, x, y, final=final, hot=step == 1, dim=step >= 2)
        else:
            node(ax, x, y, final=final, hot=step == 1 and k in ("seal", "seals"))
    stem(ax)
    edge(ax, (P4["sea"][0] + 0.2, 3.7), (P4["seal"][0] - 0.25, 4.6), "l", at=(4.9, 4.35))
    edge(ax, (P4["seal"][0] + R, 4.7), (P4["seals"][0] - R, 4.7), "s", hot=step == 1)
    if step < 3:
        edge(ax, (P4["sea"][0] + 0.2, 3.3), (P4["seat"][0] - 0.25, 2.4), "t", dim=step >= 2, at=(4.9, 2.6))
        edge(ax, (P4["seat"][0] + R, 2.3), (P4["seats"][0] - R, 2.3), "s", hot=step == 1, dim=step >= 2)
    if step >= 2:
        edge(ax, (P4["sea"][0] + R, 3.4), (P4["seal"][0] + 0.1, 4.43), "t", hot=step == 2, rad=0.55, at=(5.8, 3.65))
    if step == 1:
        label(ax, 7.8, 4.7, "← 끝, s 붙으면 또 끝", fs=11.5, ha="left", color=RED)
        label(ax, 7.8, 2.3, "← 똑같은 꼬리", fs=11.5, ha="left", color=RED)
        label(ax, 7.8, 3.5, "트라이: 칸 8개", fs=12.5, ha="left", bold=True)
        label(ax, 6.0, 0.9, "이중 원 = 여기서 끝나는 낱말이 있어요", fs=11, color=INK)
    elif step == 2:
        label(ax, 7.8, 2.3, "← 지워요", fs=12, ha="left", color=GREY)
        label(ax, 7.8, 3.6, "t 길을 위 칸으로\n돌려 함께 써요", fs=12, ha="left", color=RED)
        label(ax, 6.0, 0.9, "seat 뒤 칸들은 seal 뒤 칸들과 모양이 같아요", fs=11.5, color=INK)
    else:
        label(ax, 7.8, 3.5, "FST: 칸 6개", fs=12.5, ha="left", bold=True)
        label(ax, 7.8, 2.8, "칸 8개 → 6개", fs=12.5, ha="left", color=RED, bold=True)
        moral(ax, 6.0, 0.6, "앞부분뿐 아니라 꼬리가 같은 칸도 합쳐요")


def output(ax, step):
    """FST의 값: 지나는 화살표 값을 더한다. 1=seal 길, 2=seat 길."""
    label(ax, 0.3, 6.35, "글자 / 값: 지나는 화살표의 값을 더해요", fs=12.5, ha="left", bold=True)
    for k in ("r", "s", "se", "sea", "seal", "seals"):
        node(ax, *P4[k], final=k in ("seal", "seals"))
    seal, seat = step == 1, step == 2
    stem(ax, hot=("s", "se", "sea"), vals={"ss": 5, "ese": 0, "asea": 0})
    edge(ax, (P4["sea"][0] + 0.2, 3.7), (P4["seal"][0] - 0.25, 4.6), "l / 0", hot=seal, at=(4.6, 4.45))
    edge(ax, (P4["sea"][0] + R, 3.4), (P4["seal"][0] + 0.1, 4.43), "t / 4", hot=seat, rad=0.55, at=(6.1, 3.6))
    edge(ax, (P4["seal"][0] + R, 4.7), (P4["seals"][0] - R, 4.7), "s / 1")
    label(ax, 7.8, 3.9, "seal = 5 + 0 + 0 + 0 = 5", fs=11.5, ha="left", color=RED if seal else INK, bold=seal)
    if seat:
        label(ax, 7.8, 3.1, "seat = 5 + 0 + 0 + 4 = 9", fs=11.5, ha="left", color=RED, bold=True)
        moral(ax, 6.0, 1.0, "꼬리를 함께 써도 갈라지는 화살표의 값이 두 낱말을 갈라요")
    else:
        label(ax, 6.0, 1.3, "s, e, a, l을 따라가며 화살표 값을 더해요", fs=12, color=INK)
        label(ax, 6.0, 0.6, "값은 낱말에 딸린 정보예요 (안내판이라면 블록 위치)", fs=11, color=INK)


# ── 포스팅 목록: 차이값 ──────────────────────────────────────────
IDS = [3, 7, 8, 15, 21, 22, 40]
DIFF = [IDS[0]] + [b - a for a, b in zip(IDS, IDS[1:])]


def postings(ax, step):
    label(ax, 0.3, 6.35, "환불이 든 글 번호", fs=12.5, ha="left", bold=True)
    X = lambda n: 0.6 + n * 0.27  # noqa: E731
    ax.plot([X(0), X(41)], [4.0, 4.0], color=INK, lw=1.4)
    for n in range(0, 41, 5):
        ax.plot([X(n), X(n)], [3.9, 4.1], color=INK, lw=1)
        label(ax, X(n), 3.55, str(n), fs=9.5, color=INK)
    prev = 0
    for k, n in enumerate(IDS):
        ax.add_patch(Circle((X(n), 4.0), 0.15, fc=RED if step == 1 else INK, ec="none"))
        sh = {7: -0.15, 8: 0.15, 21: -0.15, 22: 0.15}.get(n, 0)
        label(ax, X(n) + sh, 4.5, str(n), fs=12, color=RED if step == 1 else "#222", bold=step == 1)
        if step == 2:
            arrow(ax, (X(prev), 4.15), (X(n), 4.15), color=RED, lw=1.4, ms=9, rad=-0.6)
            label(ax, (X(prev) + X(n)) / 2, 4.95 + 0.03 * (n - prev) + (0.35 if n - prev == 1 else 0),
                  f"+{n - prev}", fs=11.5, color=RED, bold=True)
        prev = n
    if step == 1:
        label(ax, 6.0, 2.4, "번호가 커질수록 적는 자리도 커져요 (40은 두 자리)", fs=12, color=INK)
    else:
        label(ax, 0.3, 2.45, "글 번호", fs=11.5, ha="left", color=INK)
        cells(ax, 2.2, 2.1, IDS, w=0.9, h=0.65, fs=11.5)
        label(ax, 0.3, 1.55, "차이값", fs=11.5, ha="left", color=RED)
        cells(ax, 2.2, 1.2, DIFF, w=0.9, h=0.65, hot=range(len(DIFF)), fs=11.5)
        moral(ax, 6.0, 0.4, "번호 대신 앞 번호와의 차이만 적어요. 차이는 작아요")


# ── 비트 패킹 ────────────────────────────────────────────────────
def pack(ax, step):
    label(ax, 0.3, 6.35, "차이값 18을 4바이트(32비트)로 적으면", fs=12.5, ha="left", bold=True)
    b18 = format(18, "032b")
    bits(ax, 0.6, 5.3, b18, hot=range(27, 32), dim=range(27))
    label(ax, 5.2, 4.85, "앞 27칸은 늘 0", fs=11, color=GREY)
    label(ax, 10.3, 4.85, "18을 0과 1로 적으면 10010\n5칸이면 돼요", fs=11, color=RED)
    if step == 1:
        label(ax, 6.0, 3.0, "작은 차이값을 32칸씩 적으면 칸 대부분이 빈 0이에요", fs=12, color=INK)
        moral(ax, 6.0, 1.8, "그럼 몇 칸씩 적어야 할까요?", fs=12)
        return
    label(ax, 0.3, 3.95, "묶음(차이값 128개) 하나를 5칸씩 이어 적으면 (앞 7개만 그림)", fs=12, ha="left", bold=True)
    x = 0.6
    for d in DIFF:
        hot = d == 18
        bits(ax, x, 2.7, format(d, "05b"), w=0.28, hot=range(5) if hot else ())
        label(ax, x + 0.7, 3.45, str(d), fs=11.5, color=RED if hot else INK, bold=hot)
        x += 5 * 0.28 + 0.12
    label(ax, x + 0.1, 2.95, "…", fs=13, ha="left", color=INK)
    label(ax, 6.0, 1.85, "가장 큰 값 18이 칸 수(5)를 정해요. 128개 × 5칸 = 640비트 = 80바이트", fs=11.5, color=INK)
    moral(ax, 6.0, 0.8, "32칸씩이면 512바이트, 5칸씩이면 80바이트")


def pack_sum():
    """묶음마다 다른 칸 수: 바이트를 막대 길이로."""
    fig, ax = canvas(7.2, 3.4, 12, 5.6)
    label(ax, 0.3, 5.2, "차이값 128개 묶음 하나를 적는 데 드는 바이트", fs=12.5, ha="left", bold=True)
    rows = [("그대로 (32칸씩)", 512, None, False), ("묶음 1: 가장 큰 차이 18 → 5칸", 80, 5, True),
            ("묶음 2: 가장 큰 차이 9 → 4칸", 64, 4, False), ("묶음 3: 가장 큰 차이 33 → 6칸", 96, 6, False)]
    for k, (name, b, _, hot) in enumerate(rows):
        y = 4.1 - k * 1.0
        label(ax, 0.3, y + 0.55, name, fs=11, ha="left", color=RED if hot else "#222")
        L = 11.0 * b / 512
        ax.add_patch(Rectangle((0.3, y), L, 0.32, fc=PINK if hot else (LIGHT if k == 0 else NOTE),
                               ec=RED if hot else INK, lw=1.2))
        label(ax, 0.45 + L, y + 0.16, f"{b}바이트", fs=11, ha="left", color=RED if hot else INK, bold=hot)
    moral(ax, 6.0, 0.25, "묶음마다 가장 큰 값에 맞춘 칸 수로 꽉 채워 적어요", fs=12)
    save(fig, OUT, "es06-pack-3.svg")


# ── 페이지 캐시 ──────────────────────────────────────────────────
def cache(ax, step):
    heap = 8 if step == 1 else 14
    label(ax, 0.3, 6.35, f"컴퓨터 메모리 16 GB (한 칸 1 GB), 힙 {heap} GB", fs=12.5, ha="left", bold=True)
    w = 0.66
    for k in range(16):
        x = 0.5 + k * w
        if k < heap:
            ax.add_patch(Rectangle((x, 4.8), w, 0.9, fc=LIGHT, ec=GREY, lw=1))
        else:
            ax.add_patch(Rectangle((x, 4.8), w, 0.9, fc="white", ec=INK, lw=1))
    label(ax, 0.5 + heap * w / 2, 5.25, "자바 힙", fs=11.5, color=INK)
    label(ax, 0.5 + (heap + 16) * w / 2, 4.35, "남는 메모리", fs=11, color=INK)
    label(ax, 0.3, 2.85, "디스크: 역색인 파일 조각 (점선 = 메모리에 올라간 조각)", fs=11, ha="left", color=INK)
    free = 16 - heap
    for k in range(6):
        x = 0.5 + k * 1.2
        up = k < free
        if up:
            mx = 0.5 + (heap + k) * w
            hot = step == 1
            ax.add_patch(Rectangle((mx + 0.08, 4.9), w - 0.16, 0.7, fc=PINK if hot else NOTE, ec=RED if hot else INK, lw=1.2))
            ax.add_patch(Rectangle((x, 1.6), 0.9, 0.8, fc="white", ec=GREY, lw=1, ls="--"))
        else:
            ax.add_patch(Rectangle((x, 1.6), 0.9, 0.8, fc=PINK, ec=RED, lw=1.5))
    arrow(ax, (3.6, 3.2), (0.5 + (heap + 0.5) * w, 4.7), color=GREY, lw=1.5, ms=12)
    label(ax, 0.3 + (heap + 0.5) * w / 2 + 1.8, 3.6, "남는 메모리에 올려요", fs=11, ha="left", color=INK)
    if step == 1:
        label(ax, 8.0, 2.0, "조각 6개가 모두 올라가요", fs=12, ha="left", color=INK)
        label(ax, 6.0, 0.7, "찾을 때 디스크까지 가지 않아요", fs=12, color=INK)
    else:
        label(ax, 8.0, 2.0, "4개는 디스크에서\n읽어야 해요 (느려요)", fs=12, ha="left", color=RED)
        moral(ax, 6.0, 0.6, "힙을 키우면 파일이 올라갈 자리가 줄어요")


# ── 값이 모두 다른 필드 ───────────────────────────────────────────
def names():
    """정렬했을 때 앞부분이 겹치는 이름과 안 겹치는 이름을 나란히."""
    fig, ax = canvas(7.2, 3.8, 12, 6.3)
    a = ["IMG_20261029_093512", "IMG_20261029_093547", "IMG_20261029_094102", "IMG_20261029_094230"]
    b = ["2c71e0b4d9…", "9f3a5d12e0…", "a0e4c7f981…", "e58b0a63c2…"]
    label(ax, 0.3, 5.9, "찍은 시각 꼴 (정렬)", fs=12, ha="left", bold=True)
    label(ax, 7.6, 5.9, "무작위 32글자 (정렬, 앞 10글자만)", fs=12, ha="left", bold=True)
    for k, s in enumerate(a):
        letters(ax, 0.3, 4.8 - k * 0.6, s, w=0.32, h=0.5, hot=range(15), fs=9.5)
    for k, s in enumerate(b):
        letters(ax, 7.6, 4.8 - k * 0.6, s, w=0.32, h=0.5, hot=(), fs=9.5)
    label(ax, 3.2, 2.0, "빨간 앞부분을 함께 써요\n글자 1.9 MB → 역색인 0.54 MB", fs=11.5, color=RED)
    label(ax, 9.4, 2.0, "함께 쓸 앞부분이 없어요\n글자 3.2 MB → 역색인 2.9 MB", fs=11.5, color=INK)
    label(ax, 6.0, 0.6, "사진 이름 10만 개, ES 7.17로 잰 값", fs=10.5, color=INK)
    ax.plot([6.9, 6.9], [1.4, 6.2], color=GREY, lw=1, ls="--")
    save(fig, OUT, "es06-names.svg")


def decide():
    fig, ax = canvas(7.2, 3.8, 12, 6.3)
    box(ax, 0.6, 5.0, 10.8, 1.0, fc=LIGHT, ec=GREY)
    label(ax, 6.0, 5.5, "값이 모두 다르고 앞부분도 겹치지 않는 필드\n(무작위 요청 번호처럼)", fs=11.5, color=INK)
    arrow(ax, (6.0, 4.9), (6.0, 4.3), ms=12)
    box(ax, 2.0, 3.3, 8.0, 0.9, fc=NOTE)
    label(ax, 6.0, 3.75, "이 필드로 글을 찾거나 거르나요?", fs=12, bold=True)
    arrow(ax, (4.0, 3.2), (2.9, 2.3)); label(ax, 3.0, 2.85, "예", fs=11.5, color=INK)
    box(ax, 0.3, 0.6, 5.2, 1.6, fc=PAPER)
    label(ax, 2.9, 1.4, "역색인을 둬요\n(사전이 커도\n찾으려면 필요해요)", fs=11.5)
    arrow(ax, (8.0, 3.2), (9.1, 2.3), color=RED); label(ax, 9.2, 2.85, "아니요", fs=11.5, color=RED)
    box(ax, 6.5, 0.6, 5.2, 1.6, fc=PINK, ec=RED)
    label(ax, 9.1, 1.4, "\"index\": false로\n역색인을 만들지 않아요\n(원본에는 그대로 남아요)", fs=11.5, color=RED)
    save(fig, OUT, "es06-decide.svg")


if __name__ == "__main__":
    S, L = (7.2, 3.8), (12, 6.6)
    open_(); map_()
    stage(block, 3, OUT, "es06-block", S, L)
    stage(index, 3, OUT, "es06-index", S, L)
    stage(trie, 3, OUT, "es06-trie", S, L)
    stage(output, 2, OUT, "es06-output", S, L)
    stage(postings, 2, OUT, "es06-postings", S, L)
    stage(pack, 2, OUT, "es06-pack", S, L); pack_sum()
    stage(cache, 2, OUT, "es06-cache", S, L)
    names(); decide()
