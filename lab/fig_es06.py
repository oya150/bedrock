"""Elasticsearch 6편 그림 만들기. 실행: python lab/fig_es06.py  → docs/elasticsearch/img/06/*.svg

본문 절은 장면 띠로 그린다: 같은 무대를 여러 장 그리고 장마다 바뀐 곳만 빨강으로 칠한다.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "es"))
from figkit import (BLUE, GREY, INK, LIGHT, NOTE, PAPER, PINK, RED, arrow, bits, box, bubble, canvas, cell, cells,  # noqa: E402
                    cylinder, label, letters, moral, outdir, save, stage)
from matplotlib.patches import Circle, Rectangle  # noqa: E402

OUT = outdir("06")


# ── 여는 장면과 돌아오는 장면: 저장 공간 화면 ──────────────────────
# 무대: 왼쪽은 파일 크기를 막대로 보여 주는 저장 공간 화면, 오른쪽은 일하는 ES 원통.
CYL = (8.1, 2.75, 3.6, 1.75)
SAY = (7.3, 0.3, 4.55, 1.45)
TAIL = (9.9, 2.5)
MB = 2.45  # 1 MB 막대 길이
ROW_A, ROW_B = 4.35, 2.45


def doc_icon(ax, x, y, color=INK):
    """작은 파일 모양 (모서리 접힌 종이)."""
    from matplotlib.patches import Polygon
    ax.add_patch(Polygon([(x, y), (x + 0.42, y), (x + 0.42, y + 0.4), (x + 0.28, y + 0.54), (x, y + 0.54)],
                         closed=True, fc="white", ec=color, lw=1.3))
    for k in range(3):
        ax.plot([x + 0.08, x + 0.32], [y + 0.12 + k * 0.11] * 2, color=color, lw=0.8)


def size_row(ax, y, name, sub, mb, hot=False, ghost=False):
    """저장 공간 화면의 한 줄: 파일 이름, 설명, 크기 막대."""
    c = RED if hot else "#222"
    doc_icon(ax, 0.85, y + 0.05, color=RED if hot else INK)
    label(ax, 1.45, y + 0.42, name, fs=12, ha="left", color=c, bold=hot)
    label(ax, 1.45, y - 0.05, sub, fs=10, ha="left", color=RED if hot else INK)
    if ghost:
        ax.add_patch(Rectangle((0.85, y - 0.75), 5.6, 0.36, fc="white", ec=GREY, lw=1.0, ls="--"))
        label(ax, 6.55, y + 0.3, "?", fs=12, ha="right", color=GREY)
        return
    label(ax, 6.55, y + 0.3, f"{mb} MB", fs=12, ha="right", color=c, bold=True)
    ax.add_patch(Rectangle((0.85, y - 0.75), 5.6, 0.36, fc=LIGHT, ec="none"))
    ax.add_patch(Rectangle((0.85, y - 0.75), mb * MB, 0.36, fc=PINK if hot else BLUE, ec=RED if hot else INK, lw=1.4))


def storage(ax, b_state):
    """b_state: 'ghost'=역색인 아직 없음, 'new'=막 생김(빨강), 'plain'."""
    box(ax, 0.6, 0.8, 6.15, 5.6, fc="white", round_=False)
    ax.add_patch(Rectangle((0.6, 5.95), 6.15, 0.45, fc=LIGHT, ec=INK, lw=1.2))
    label(ax, 0.8, 6.17, "저장 공간", fs=11, ha="left", color=INK)
    size_row(ax, ROW_A, "낱말 목록 (글자만)", "영어 낱말 23만 개", 2.2)
    size_row(ax, ROW_B, "ES 역색인", "용어 사전 + 포스팅 목록", 1.6, hot=b_state == "new", ghost=b_state == "ghost")


def es_inside(ax, step_hot=False, blocks=False, blocks_hot=False):
    """원통 안: 용어 사전과 포스팅 목록. blocks=True면 용어 사전을 앞부분 sea + 나머지 글자로 연다."""
    x, y, w, h = CYL
    if blocks:
        cell(ax, x + 0.15, y + 1.0, 0.65, 0.45, "sea", hot=blocks_hot, fs=9.5)
        cells(ax, x + 0.88, y + 1.0, ["l", "rch", "son", "t"], w=0.62, h=0.45, gap=0.04, fs=9.5)
        label(ax, x + w / 2, y + 0.74, "용어 사전 (블록)", fs=9, color=RED if blocks_hot else INK)
    else:
        cell(ax, x + 0.2, y + 0.85, w - 0.4, 0.5, "용어 사전", hot=step_hot, fs=10)
    cell(ax, x + 0.2, y + (0.1 if blocks else 0.15), w - 0.4, 0.4 if blocks else 0.5, "포스팅 목록", hot=step_hot and not blocks, fs=10)


def opening(ax, step):
    storage(ax, "ghost" if step < 3 else "new")
    cylinder(ax, *CYL, "ES")
    if step >= 2:
        es_inside(ax, step_hot=step == 2)
        arrow(ax, (6.95, ROW_A - 0.5), (CYL[0] - 0.1, CYL[1] + 0.9), color=RED if step == 2 else GREY, ms=14)
    if step == 1:
        bubble(ax, *SAY, "낱말 23만 개를 글 하나에\n하나씩 받을게요", TAIL)
    elif step == 2:
        bubble(ax, *SAY, "역색인을 만들었어요\n낱말마다 글 번호도 붙였어요", TAIL, hot=True)
    else:
        bubble(ax, *SAY, "다 담고 보니 1.6 MB예요", TAIL, hot=True)
        moral(ax, 3.7, 0.3, "글 번호까지 붙었는데 낱말 글자보다 작아요")


def back(ax, step):
    storage(ax, "new" if step == 3 else "plain")
    cylinder(ax, *CYL, "ES")
    es_inside(ax, blocks=step >= 2, blocks_hot=step == 2)
    arrow(ax, (6.95, ROW_A - 0.5), (CYL[0] - 0.1, CYL[1] + 0.9), color=GREY, ms=14)
    if step == 1:
        bubble(ax, *SAY, "그때 글자 2.2 MB를\n1.6 MB에 담았어요", TAIL)
    elif step == 2:
        bubble(ax, *SAY, "정렬해 블록으로 묶고\n앞부분 sea는 한 번만 적어요", TAIL, hot=True)
    else:
        bubble(ax, *SAY, "나눠 쓴 앞부분만큼\n글자보다 작아졌어요", TAIL, hot=True)
        moral(ax, 3.7, 0.3, "같은 앞부분을 한 번만 적어서 더 작게 담겨요")


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
    for a, b, ch, dy in (("r", "s", "s", 0.3), ("s", "sa", "a", 0.25), ("s", "se", "e", None), ("se", "sea", "a", 0.3),
                         ("s", "sh", "h", -0.42)):
        (x1, y1), (x2, y2) = P[a], P[b]
        hot = hot_path and (a, b) in (("r", "s"), ("s", "se"), ("se", "sea"))
        edge(ax, (x1 + 0.28, y1), (x2 - 0.28, y2), ch, hot=hot, dy=dy or 0, at=None if dy else (2.65, 4.9))
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
    label(ax, X(0), 3.55, "0", fs=9.5, color=INK)
    prev = 0
    for k, n in enumerate(IDS):
        ax.add_patch(Circle((X(n), 4.0), 0.15, fc=RED if step == 1 else INK, ec="none"))
        sh = {7: -0.15, 8: 0.15, 21: -0.15, 22: 0.15}.get(n, 0)
        label(ax, X(n) + sh, 3.55, str(n), fs=12, color=RED if step == 1 else "#222", bold=step == 1)
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
    first = step == 1
    bits(ax, 0.5, 5.25, b18, w=0.34, h=0.58, hot=range(27, 32) if first else (), dim=range(27))
    label(ax, 5.2, 4.85, "18이면 앞 27칸은 모두 0", fs=11, color=GREY)
    label(ax, 10.3, 4.85, "18을 0과 1로 적으면 10010\n5칸이면 돼요", fs=11, color=RED if first else INK)
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
    label(ax, 6.0, 0.8, "32칸씩이면 512바이트, 5칸씩이면 80바이트", fs=12, color=INK)


def pack_sum():
    """묶음마다 다른 칸 수: 바이트를 막대 길이로."""
    fig, ax = canvas(7.2, 3.8, 12, 6.6)
    label(ax, 0.3, 5.7, "차이값 128개 묶음 하나를 적는 데 드는 바이트", fs=12.5, ha="left", bold=True)
    rows = [("그대로 (32칸씩)", 512, None, False), ("묶음 1: 가장 큰 차이 18 → 5칸", 80, 5, True),
            ("묶음 2: 가장 큰 차이 9 → 4칸", 64, 4, False), ("묶음 3: 가장 큰 차이 33 → 6칸", 96, 6, False)]
    for k, (name, b, _, hot) in enumerate(rows):
        y = 4.4 - k * 1.05
        label(ax, 0.3, y + 0.55, name, fs=11, ha="left", color=RED if hot else "#222")
        L = 11.0 * b / 512
        ax.add_patch(Rectangle((0.3, y), L, 0.32, fc=PINK if hot else (LIGHT if k == 0 else NOTE),
                               ec=RED if hot else INK, lw=1.2))
        label(ax, 0.45 + L, y + 0.16, f"{b}바이트", fs=11, ha="left", color=RED if hot else INK, bold=hot)
    moral(ax, 6.0, 0.45, "묶음마다 가장 큰 값에 맞춘 칸 수로 꽉 채워 적어요", fs=12)
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
    arrow(ax, (3.6, 3.2), (0.5 + (heap + 0.5) * w, 4.7), color=RED if step == 1 else GREY, lw=1.5, ms=12)
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
    fig, ax = canvas(7.2, 3.8, 12, 6.6)
    a = ["IMG_20261029_093512", "IMG_20261029_093547", "IMG_20261029_094102", "IMG_20261029_094230"]
    b = ["2c71e0b4d9…", "9f3a5d12e0…", "a0e4c7f981…", "e58b0a63c2…"]
    label(ax, 0.3, 6.2, "찍은 시각 꼴 (정렬)", fs=12, ha="left", bold=True)
    label(ax, 7.6, 6.2, "무작위 32글자 (정렬, 앞 10글자만)", fs=12, ha="left", bold=True)
    for k, s in enumerate(a):
        letters(ax, 0.3, 5.1 - k * 0.6, s, w=0.32, h=0.5, hot=range(15), fs=9.5)
    for k, s in enumerate(b):
        letters(ax, 7.6, 5.1 - k * 0.6, s, w=0.32, h=0.5, hot=(), fs=9.5)
    label(ax, 3.2, 2.7, "빨간 앞부분을 함께 써요", fs=11.5, color=RED)
    label(ax, 9.4, 2.7, "함께 쓸 앞부분이 없어요", fs=11.5, color=INK)
    for x0, (txt, inv), hot in ((0.3, (1.9, 0.54), True), (7.6, (3.2, 2.9), False)):
        for k, (what, mb) in enumerate((("글자", txt), ("역색인", inv))):
            y = 1.75 - k * 0.85
            on = hot and k == 1
            label(ax, x0, y + 0.55, f"{what} {mb} MB", fs=10.5, ha="left", color=RED if on else INK, bold=on)
            ax.add_patch(Rectangle((x0, y), mb * 1.1, 0.32, fc=PINK if on else (BLUE if k == 1 else LIGHT),
                                   ec=RED if on else INK, lw=1.2))
    label(ax, 6.0, 0.25, "사진 이름 10만 개, ES 7.17로 잰 값", fs=10.5, color=INK)
    ax.plot([6.9, 6.9], [0.7, 6.2], color=GREY, lw=1, ls="--")
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


# ── 정리: 낱말 카드 ────────────────────────────────────────────────
def cards():
    fig, ax = canvas(6.4, 10.4, 9.8, 16.25)
    W, H = 4.6, 3.8

    def card(i, name, line):
        col, row = i % 2, i // 2
        x, y = 0.2 + col * 4.9, 12.25 - row * 4.05
        box(ax, x, y, W, H, fc="white")
        label(ax, x + 0.25, y + H - 0.4, name, fs=12.5, ha="left", bold=True)
        label(ax, x + W / 2, y + 0.5, line, fs=10, color=INK)
        return x, y

    x, y = card(0, "블록", "정렬된 낱말을 수십 개씩\n묶어 디스크에 적은 덩어리")
    cell(ax, x + 0.4, y + 2.25, 0.8, 0.5, "sea", hot=True, fs=10)
    box(ax, x + 0.4, y + 1.35, 3.8, 0.7, fc="none", ec=INK, lw=1.0, round_=False)
    cells(ax, x + 0.5, y + 1.45, ["l", "rch", "son", "t"], w=0.8, h=0.5, gap=0.1, fs=10)
    x, y = card(1, "안내판 (용어 색인)", "어느 블록을 읽을지\n고르는 작은 길잡이")
    for k, ch in enumerate("sea"):
        node(ax, x + 0.5 + k * 0.95, y + 2.05, hot=True)
        edge(ax, (x + 0.78 + k * 0.95, y + 2.05), (x + 1.17 + k * 0.95, y + 2.05), ch, hot=True, dy=0.25)
    node(ax, x + 3.35, y + 2.05, hot=True)
    label(ax, x + 3.35, y + 1.5, "블록 42", fs=10, color=RED)
    x, y = card(2, "트라이", "같은 앞부분을 한 번만 적고\n가지처럼 갈라지는 나무")
    mini_tree(ax, x, y, merged=False)
    x, y = card(3, "FST", "꼬리가 같은 칸까지 합친 길,\n따라가며 값을 더해요")
    mini_tree(ax, x, y, merged=True)
    x, y = card(4, "차이값 (델타 인코딩)", "번호 대신 적는\n앞 번호와의 차이")
    cells(ax, x + 0.5, y + 2.3, [3, 7, 8, 15], w=0.8, h=0.5, gap=0.1, fs=10)
    cells(ax, x + 0.5, y + 1.5, [3, 4, 1, 7], w=0.8, h=0.5, gap=0.1, hot=range(4), fs=10)
    x, y = card(5, "비트 패킹", "묶음에서 가장 큰 값에 맞춘\n비트 수로 꽉 채워 담기")
    xx = x + 0.55
    for d in (3, 18):
        bits(ax, xx, y + 1.75, format(d, "05b"), w=0.3, h=0.55, hot=range(5) if d == 18 else (), fs=9)
        label(ax, xx + 0.75, y + 2.55, str(d), fs=9.5, color=RED if d == 18 else INK)
        xx += 5 * 0.3 + 0.5
    x, y = card(6, "페이지 캐시", "운영체제가 남는 메모리에\n읽은 파일을 놓아두는 곳")
    mini_memory(ax, x, y, hot_cache=True)
    x, y = card(7, "자바 힙", "ES가 시작할 때 자기만\n쓰려고 정해 두는 메모리")
    mini_memory(ax, x, y, hot_cache=False)
    save(fig, OUT, "es06-cards.svg")


def mini_tree(ax, x, y, merged):
    """카드용 작은 sea 뒤 나무: l·t로 갈라지고 s 꼬리. merged=True면 두 길이 한 칸으로 모인다."""
    a = (x + 0.6, y + 2.05)
    up, dn = (x + 1.9, y + 2.65), (x + 1.9, y + 1.45)
    node(ax, *a)
    label(ax, x + 0.6, y + 1.55, "sea까지 5" if merged else "sea", fs=9.5, color=INK)
    if merged:
        m = (x + 2.1, y + 2.05)
        node(ax, *m, final=True, hot=True)
        edge(ax, (a[0] + 0.2, a[1] + 0.2), (m[0] - 0.22, m[1] + 0.15), "l / 0", dy=0.55, rad=-0.3)
        edge(ax, (a[0] + 0.2, a[1] - 0.2), (m[0] - 0.22, m[1] - 0.15), "t / 4", dy=-0.62, rad=0.3, hot=True)
        node(ax, x + 3.5, y + 2.05, final=True)
        edge(ax, (m[0] + 0.28, m[1]), (x + 3.22, y + 2.05), "s / 1")
        label(ax, x + 3.5, y + 1.3, "seat = 5 + 4 = 9", fs=9.5, color=RED)
        return
    for p, ch, dy in ((up, "l", 0.3), (dn, "t", -0.35)):
        node(ax, *p, final=True, hot=True)
        edge(ax, (a[0] + 0.25, a[1] + (0.15 if ch == "l" else -0.15)), (p[0] - 0.26, p[1] + (-0.1 if ch == "l" else 0.1)),
             ch, dy=dy, hot=True)
        node(ax, x + 3.3, p[1], final=True)
        edge(ax, (p[0] + 0.28, p[1]), (x + 3.02, p[1]), "s")


def mini_memory(ax, x, y, hot_cache):
    """카드용 메모리 8칸: 앞 4칸 자바 힙, 뒤 4칸 남는 메모리에 파일 조각."""
    w = 0.5
    for k in range(8):
        xx = x + 0.3 + k * w
        heap = k < 4
        hot = (heap and not hot_cache) or (not heap and hot_cache)
        if heap:
            ax.add_patch(Rectangle((xx, y + 1.65), w, 0.7, fc=PINK if hot else LIGHT, ec=RED if hot else GREY, lw=1.2))
        else:
            ax.add_patch(Rectangle((xx, y + 1.65), w, 0.7, fc="white", ec=INK, lw=1))
            ax.add_patch(Rectangle((xx + 0.08, y + 1.75), w - 0.16, 0.5, fc=PINK if hot else NOTE,
                                   ec=RED if hot else INK, lw=1.1))
    label(ax, x + 0.3 + 2 * w, y + 2.6, "자바 힙", fs=9.5, color=INK if hot_cache else RED)
    label(ax, x + 0.3 + 6 * w, y + 2.6, "남는 메모리", fs=9.5, color=RED if hot_cache else INK)


if __name__ == "__main__":
    S, L = (7.2, 3.8), (12, 6.6)
    stage(opening, 3, OUT, "es06-open", S, L)
    stage(block, 3, OUT, "es06-block", S, L)
    stage(index, 3, OUT, "es06-index", S, L)
    stage(trie, 3, OUT, "es06-trie", S, L)
    stage(output, 2, OUT, "es06-output", S, L)
    stage(postings, 2, OUT, "es06-postings", S, L)
    stage(pack, 2, OUT, "es06-pack", S, L); pack_sum()
    stage(cache, 2, OUT, "es06-cache", S, L)
    names(); decide()
    stage(back, 3, OUT, "es06-back", S, L)
    cards()
