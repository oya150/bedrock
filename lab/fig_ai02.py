"""AI 2편 그림 만들기. 실행: python lab/fig_ai02.py  → docs/ai/img/02/*.svg

본문 절은 장면 띠로 그린다: 같은 무대를 여러 장 그리고 장마다 바뀐 곳만 빨강으로 칠한다.
여는 장면은 챗봇 화면과 1편 무대(보낸 메시지, 자판, 언어 모델 원통)로 연다. 돌아오는 장면은 1편 무대를 다시 쓴다.
장면마다 할 일이 하나다(v4: 한 끗 차이 장면은 합쳤다). 예시와 숫자는 .claude/writing/work/cal/units-ai02-v3.md 의 메시지 7개뿐이다. 실험 숫자는 쓰지 않는다.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "es"))
from figkit import (GREY, INK, LIGHT, NOTE, PINK, RED, arrow, box, bubble, canvas, cell,  # noqa: E402
                    cylinder, label, moral, outdir, save, stage)
from matplotlib.patches import Rectangle  # noqa: E402

OUT = outdir("02", "ai")

# 1편 메시지 5개 + 2편에서 더 보낸 2개
MSGS = [["오늘", "점심", "뭐", "먹지"], ["오늘", "날씨", "좋다"], ["내일", "점심", "같이", "먹자"],
        ["오늘", "저녁", "뭐", "먹을까"], ["날씨", "뭐", "이래"], ["어제", "뭐", "먹었어"], ["점심", "먹었지"]]
TYPED = ["내일", "저녁", "뭐", "먹었니"]
WORDS = []
for _m in MSGS:
    for _w in _m:
        if _w not in WORDS:
            WORDS.append(_w)  # 낱말 사전 15개 (처음 나온 차례)
CHARS = []
for _m in MSGS:
    for _ch in "".join(_m):
        if _ch not in CHARS:
            CHARS.append(_ch)  # 글자 사전 24개
RULES = [("오", "늘"), ("점", "심"), ("먹", "었"), ("날", "씨")]
NI = [235, 139, 136]  # "니"(45768)를 UTF-8로 적은 바이트
assert len(WORDS) == 15 and len(CHARS) == 24 and "니" not in CHARS
assert list("니".encode()) == NI and ord("니") == 45768


def pieces(word, rules):
    """합친 순서 목록을 차례로 적용해 낱말을 조각으로 자른다."""
    w = list(word)
    for a, b in rules:
        i = 0
        while i + 1 < len(w):
            if w[i] == a and w[i + 1] == b:
                w[i:i + 2] = [a + b]
            else:
                i += 1
    return w


SLOTS = [sum(len(pieces(w, RULES[:k])) for m in MSGS for w in m) for k in range(5)]
assert SLOTS == [45, 42, 39, 37, 35]
assert [p for w in MSGS[0] for p in pieces(w, RULES)] == ["오늘", "점심", "뭐", "먹", "지"]
assert pieces("먹었니", RULES) == ["먹었", "니"]


def empty(ax, x, y, w, h, s="", color=GREY):
    ax.add_patch(Rectangle((x, y), w, h, fc="white", ec=color, lw=1.2, ls="--"))
    if s:
        label(ax, x + w / 2, y + h / 2, s, fs=12, color=color, bold=color == RED)


# ── 0. 챗봇은 글을 토큰으로 세요 ──────────────────────────────────
def chat(ax, step):
    """챗봇 화면. 주고받을 수 있는 글의 양과 한 번에 읽는 길이를 토큰으로 센다."""
    box(ax, 0.4, 0.9, 5.6, 5.55, fc="white")
    ax.add_patch(Rectangle((0.4, 5.95), 5.6, 0.5, fc=LIGHT, ec=INK, lw=1.2))
    label(ax, 0.65, 6.2, "챗봇", fs=11, ha="left", color=INK, bold=True)
    ax.add_patch(Rectangle((2.7, 4.95), 3.05, 0.55, fc=NOTE, ec=INK, lw=1.2))
    label(ax, 4.22, 5.22, "오늘 점심 뭐 먹지", fs=11.5)
    ax.add_patch(Rectangle((0.65, 4.05), 2.6, 0.55, fc=LIGHT, ec=GREY, lw=1.2))
    label(ax, 1.95, 4.32, "김밥 어때요?", fs=11.5)
    ax.add_patch(Rectangle((0.6, 1.1), 5.2, 0.5, fc="white", ec=INK, lw=1.2))
    label(ax, 0.8, 1.35, "|", fs=12, ha="left")
    for k, (name, fill) in enumerate([("주고받을 수 있는 글의 양", 0.35), ("한 번에 읽는 길이", 0.6)]):
        y = 5.5 - k * 1.45
        label(ax, 6.6, y + 0.45, name, fs=10.5, ha="left", bold=True)
        ax.add_patch(Rectangle((6.6, y - 0.2), 3.0, 0.36, fc="white", ec=INK, lw=1.2))
        ax.add_patch(Rectangle((6.6, y - 0.2), 3.0 * fill, 0.36, fc=LIGHT, ec="none"))
        label(ax, 9.8, y - 0.02, "토큰으로 세요", fs=10, ha="left", color=INK)


# ── 무대: 1편의 휴대폰 자판과 언어 모델 원통 ──────────────────────
CYL = (7.2, 3.35, 4.0, 1.45)
SAY = (6.3, 0.95, 5.5, 1.55)
TAIL = (9.2, 3.1)


def phone(ax, typed=(), hot_word=None, cand="empty"):
    """typed=낱말 목록. hot_word=빨갛게 칠할 낱말 번호. cand=empty(회색 점선)/miss(빨간 점선과 물음표)."""
    box(ax, 0.4, 0.9, 4.8, 5.55, fc="white")
    label(ax, 0.65, 6.17, "보낸 메시지", fs=10, ha="left", color=INK)
    for k, m in enumerate(MSGS):
        s = " ".join(m)
        w = 0.21 * len(s.replace(" ", "")) + 0.1 * (len(m) - 1) + 0.35
        y = 5.62 - k * 0.4
        ax.add_patch(Rectangle((5.0 - w, y), w, 0.33, fc=NOTE, ec=GREY, lw=1.0))
        label(ax, 5.0 - w / 2, y + 0.165, s, fs=9)
    ax.add_patch(Rectangle((0.6, 2.72), 4.4, 0.46, fc="white", ec=INK, lw=1.4))
    x = 0.8
    for k, wd in enumerate(typed):
        w = 0.26 * len(wd)
        on = k == hot_word
        if on:
            ax.add_patch(Rectangle((x - 0.06, 2.76), w + 0.12, 0.38, fc=PINK, ec=RED, lw=1.6))
        label(ax, x, 2.95, wd, fs=11.5, ha="left", color=RED if on else "#222", bold=on)
        x += w + 0.15
    label(ax, x - 0.05, 2.95, "|", fs=12, ha="left")
    for k in range(3):
        if cand == "miss":
            empty(ax, 0.6 + k * 1.5, 2.08, 1.4, 0.48, "?", color=RED)
        else:
            empty(ax, 0.6 + k * 1.5, 2.08, 1.4, 0.48)
    for r in range(2):
        for k in range(8):
            ax.add_patch(Rectangle((0.65 + k * 0.54 + r * 0.27, 1.45 - r * 0.42), 0.44, 0.33, fc=LIGHT, ec="none"))


def program(ax, lines=(), hot=False, name="언어 모델"):
    x, y, w, h = CYL
    cylinder(ax, *CYL, name)
    gap = 0.45 if len(lines) > 2 else 0.5
    for k, t in enumerate(lines):
        label(ax, x + w / 2, y + 1.1 - k * gap, t, fs=10, color=RED if hot else "#222", bold=hot)


# ── 1. 낱말 사전에 없는 "먹었니" (휴대폰과 사전 한 컷) ─────────────
def opening(ax, step):
    phone(ax, TYPED, hot_word=3, cand="miss")
    label(ax, 6.6, 6.3, "언어 모델의 낱말 사전 (15개)", fs=11, ha="left", bold=True)
    for k, w in enumerate(WORDS):
        x, y = 6.6 + (k % 3) * 1.6, 5.45 - (k // 3) * 0.5
        cell(ax, x, y, 1.5, 0.4, w, fs=10)
    label(ax, 6.6, 2.65, "\"먹었니\"를 찾아요", fs=10.5, ha="left", color=INK)
    cell(ax, 6.6, 1.85, 1.5, 0.45, "먹었니", hot=True, fs=10.5)
    label(ax, 8.3, 2.07, "→  ?", fs=12, ha="left", color=RED, bold=True)
    label(ax, 9.15, 2.07, "사전에 없어요", fs=10.5, ha="left", color=RED, bold=True)
    moral(ax, 6.0, 0.35, "사전에 없는 낱말 다음에는 후보를 못 띄워요")


# ── 3. "먹" 나뭇가지 ───────────────────────────────────────────────
L1 = [("지", 5.7, 1), ("자", 5.15, 1), ("을까", 4.6, 1), ("어요", 4.05, 2), ("는다", 3.5, 2)]
L2 = [("어", 2.85, 1), ("지", 2.3, 1), ("니", 1.75, 2), ("대", 1.2, 2)]
EAT = (3.0, 2.35)  # "었" 칸


def branch(ax):
    label(ax, 0.3, 6.3, "\"먹\"으로 시작하는 낱말", fs=11.5, ha="left", bold=True)
    rx, ry = 1.4, 3.5
    cell(ax, 0.6, ry - 0.28, 0.8, 0.56, "먹", fs=14)

    def leaf(x, y, s, word, when, parent):
        late = when == 2
        ax.plot([parent[0], x], [parent[1], y], color=RED if late else INK, lw=1.4, ls="--" if late else "-")
        if late:
            empty(ax, x, y - 0.22, 0.85, 0.44, s, color=RED)
        else:
            cell(ax, x, y - 0.22, 0.85, 0.44, s, fs=11)
        label(ax, x + 1.0, y, word, fs=10.5, ha="left", color=RED if late else "#222", bold=late)

    for s, y, when in L1:
        leaf(EAT[0], y, s, "먹" + s, when, (rx, ry))
    ax.plot([rx, EAT[0]], [ry, EAT[1]], color=INK, lw=1.4)
    cell(ax, EAT[0], EAT[1] - 0.22, 0.85, 0.44, "었", fs=11)
    for s, y, when in L2:
        leaf(4.6, y, s, "먹었" + s, when, (EAT[0] + 0.85, EAT[1]))
    label(ax, 9.6, 3.6, "끝은 얼마든지\n더 붙어요 …", fs=10.5, color=RED)
    label(ax, 9.6, 2.5, "점선 = 아직 사전에 없는 낱말", fs=9.5, color=INK)
    moral(ax, 6.0, 0.45, "끝이 바뀔 때마다 사전에 없는 낱말이 생겨요")


# ── 4. 메시지를 더할 때 낱말 사전과 글자 사전 (한 컷) ───────────────
def grow(ax, step):
    old = MSGS[:5]
    old_w = set(w for m in old for w in m)
    old_c = set("".join(w for m in old for w in m))
    src = {}
    for n in (5, 6):
        for w in MSGS[n]:
            src.setdefault(w, n + 1)
            for c in w:
                src.setdefault(c, n + 1)
    label(ax, 0.3, 6.25, "보낸 메시지 1 ~ 5번에 6번과 7번을 더하면", fs=11.5, ha="left", bold=True)
    label(ax, 0.3, 5.65, "6번 \"어제 뭐 먹었어\"   7번 \"점심 먹었지\"", fs=10.5, ha="left", color=INK)
    label(ax, 0.3, 4.6, "낱말 사전", fs=11, ha="left", bold=True)
    x = 1.7
    for w in WORDS:
        cw = 0.26 * len(w) + 0.1
        new = w not in old_w
        cell(ax, x, 4.35, cw, 0.5, w, hot=new, fs=9)
        if new:
            label(ax, x + cw / 2, 4.12, f"{src[w]}번", fs=8.5, color=RED)
        x += cw
    label(ax, 1.7, 3.7, "12개 → 15개   메시지마다 새 낱말이 생겼어요", fs=10, ha="left", color=RED, bold=True)
    label(ax, 0.3, 2.8, "글자 사전", fs=11, ha="left", bold=True)
    for k, c in enumerate(CHARS):
        new = c not in old_c
        cell(ax, 1.7 + k * 0.405, 2.55, 0.38, 0.5, c, hot=new, fs=9.5)
        if new:
            label(ax, 1.7 + k * 0.405 + 0.19, 2.32, f"{src[c]}번", fs=8.5, color=RED)
    label(ax, 1.7, 1.9, "21개 → 24개   7번은 새 글자가 0개", fs=10, ha="left", color=RED, bold=True)
    moral(ax, 6.0, 0.7, "낱말은 끝없이 생기고 한글 글자는 가짓수가 정해져 있어요")


# ── 5. 글자로 자르면 조각이 많아져요 (한 컷) ──────────────────────
def longer(ax, step):
    label(ax, 0.3, 6.25, "\"오늘 점심 뭐 먹지\"를 자르면", fs=11.5, ha="left", bold=True)
    label(ax, 0.3, 4.55, "낱말로 자르면", fs=11, ha="left")
    for k, wd in enumerate(["오늘", "점심", "뭐", "먹지"]):
        cell(ax, 2.6 + k * 1.2, 4.3, 1.1, 0.55, wd, fs=11.5)
    label(ax, 7.6, 4.57, "4조각", fs=11, ha="left", color=INK)
    label(ax, 0.3, 2.85, "글자로 자르면", fs=11, ha="left", color=RED, bold=True)
    for k, ch in enumerate("오늘점심뭐먹지"):
        cell(ax, 2.6 + k * 0.68, 2.6, 0.6, 0.55, ch, hot=True, fs=11.5)
    label(ax, 7.6, 2.87, "7조각", fs=11, ha="left", color=RED, bold=True)
    moral(ax, 6.0, 1.2, "글자로 자르면 같은 말이 더 많은 조각이 돼요")


# ── 6. 합치기: 오+늘 → 점+심 → 먹+었 → 날+씨 ───────────────────────
PAIRS = [("오 + 늘", "3번"), ("점 + 심", "3번"), ("먹 + 었", "2번"), ("날 + 씨", "2번"), ("나머지 짝", "1번씩")]
CW = 0.4


def merge(ax, step, prev):
    """step=합친 횟수+1. prev=앞 장의 step. 앞 장 뒤로 합친 곳을 모두 빨갛게 칠한다."""
    done = RULES[:step - 1]
    new = RULES[max(prev - 1, 0):step - 1]
    label(ax, 0.3, 6.3, "보낸 메시지 7개를 글자로 자른 칸", fs=11, ha="left", bold=True)
    for r, m in enumerate(MSGS):
        y = 5.55 - r * 0.6
        label(ax, 0.42, y + 0.21, str(r + 1), fs=9.5, color=INK)
        x = 0.7
        for wd in m:
            for p in pieces(wd, done):
                w = CW * len(p)
                if step == 1:
                    on = wd == "오늘"
                else:
                    on = len(p) == 2 and (p[0], p[1]) in new
                cell(ax, x, y, w, 0.42, p, hot=on, fs=10.5)
                x += w
            x += 0.16
    label(ax, 6.3, 6.3, "붙어 나온 짝 (낱말 안에서만)", fs=11, ha="left", bold=True)
    for k, (pair, n) in enumerate(PAIRS):
        y = 5.75 - k * 0.42
        used = k < step - 1
        on = step == 1 and k == 0
        c = RED if on else (GREY if used else "#222")
        label(ax, 6.5, y, pair, fs=10.5, ha="left", color=c, bold=on)
        label(ax, 8.2, y, n, fs=10.5, ha="left", color=c, bold=on)
        if used:
            ax.plot([6.45, 8.9], [y, y], color=GREY, lw=1.2)
    label(ax, 6.3, 3.35, "합친 순서", fs=11, ha="left", bold=True)
    label(ax, 9.6, 3.35, f"처음 {SLOTS[0]}칸", fs=10.5, ha="left", color=INK)
    for k in range(4):
        y = 2.65 - k * 0.55
        if k < step - 1:
            a, b = RULES[k]
            on = RULES[k] in new
            cell(ax, 6.5, y, 2.9, 0.45, f"{'①②③④'[k]} {a} + {b} → {a}{b}", hot=on, fs=10.5)
            label(ax, 9.6, y + 0.22, f"{SLOTS[k] - SLOTS[k + 1]}칸 줄어 {SLOTS[k + 1]}칸", fs=10.5, ha="left",
                  color=RED if on else INK, bold=on)
        else:
            empty(ax, 6.5, y, 2.9, 0.45)
    if step == 1:
        label(ax, 0.3, 1.4, "\"오\" 다음 \"늘\"이 1번 · 2번 · 4번 메시지에서 3번", fs=10, ha="left", color=RED)
        label(ax, 0.3, 0.95, "띄어 쓴 두 글자는 짝으로 세지 않아요", fs=10, ha="left", color=INK)
    if step == 2:
        moral(ax, 6.0, 0.35, "합치기 한 번에 붙은 두 칸이 한 칸이 돼요")
    if step == 5:
        label(ax, 0.3, 1.25, "사전: 글자 24개 + 합친 조각 4개 = 28개", fs=10.5, ha="left", color=RED, bold=True)
        moral(ax, 6.0, 0.35, "합친 순서가 쌓여 사전이 돼요")


# ── 7. 새 낱말은 합친 순서대로 ────────────────────────────────────
def cutnew(ax, step):
    label(ax, 0.3, 6.3, "처음 보는 낱말 \"먹었니\"", fs=11.5, ha="left", bold=True)
    label(ax, 7.3, 6.3, "합친 순서", fs=11, ha="left", bold=True)
    for k, (a, b) in enumerate(RULES):
        y = 5.55 - k * 0.6
        ok = k == 2
        cell(ax, 7.3, y, 2.4, 0.45, f"{'①②③④'[k]} {a} + {b} → {a}{b}", hot=ok, fs=10.5)
        label(ax, 9.9, y + 0.22, "있어요 → 합쳐요" if ok else "없어요", fs=10, ha="left", color=RED, bold=ok)
    label(ax, 0.3, 4.3, "글자로 자르면", fs=10.5, ha="left", color=INK)
    for k, ch in enumerate("먹었니"):
        cell(ax, 2.8 + k * 0.75, 4.05, 0.7, 0.55, ch, fs=12)
    label(ax, 0.3, 3.0, "합친 순서대로", fs=10.5, ha="left", color=RED, bold=True)
    cell(ax, 2.8, 2.75, 1.45, 0.55, "먹었", hot=True, fs=12)
    cell(ax, 4.3, 2.75, 0.7, 0.55, "니", hot=True, fs=12)
    label(ax, 0.3, 1.8, "\"니\"는 글자 사전에 없어요", fs=10.5, ha="left", color=RED, bold=True)
    for k, c in enumerate(CHARS):
        cell(ax, 0.3 + k * 0.42, 0.95, 0.38, 0.48, c, fs=9)
    label(ax, 0.3 + 24 * 0.42 + 0.1, 1.19, "니 ✗", fs=11, ha="left", color=RED, bold=True)


# ── 8. "니"를 바이트로 ─────────────────────────────────────────────
BDICT = ["0", "1", "2", "…", "136", "…", "139", "…", "235", "…", "255"]


def byte(ax, step):
    on = step == 1
    label(ax, 0.4, 6.3, "글자", fs=11, ha="left", bold=True)
    cell(ax, 0.4, 5.0, 0.8, 0.8, "니", fs=14)
    arrow(ax, (1.35, 5.4), (2.0, 5.4), color=RED if on else GREY, ms=12)
    label(ax, 2.1, 6.3, "글자 번호", fs=11, ha="left", bold=True)
    cell(ax, 2.1, 5.0, 1.6, 0.8, "45768", hot=on, fs=13)
    arrow(ax, (3.85, 5.4), (4.5, 5.4), color=RED if on else GREY, ms=12)
    label(ax, 4.6, 6.3, "바이트 3개", fs=11, ha="left", bold=True, color=RED if on else "#222")
    for k, b in enumerate(NI):
        cell(ax, 4.6 + k * 0.9, 5.0, 0.8, 0.8, b, hot=on, fs=13)
    label(ax, 7.5, 5.62, "바이트 = 0 ~ 255 가운데 숫자 하나", fs=10, ha="left", color=RED if on else INK)
    label(ax, 7.5, 5.18, "45768을 약속대로 셋에 나눠 담아요", fs=10, ha="left", color=RED if on else INK)
    if on:
        label(ax, 0.4, 3.75, "바이트 사전", fs=10.5, ha="left", color=GREY)
        empty(ax, 3.0, 3.5, 8.5, 0.5)
        label(ax, 0.4, 2.35, "\"먹었니\"는", fs=10.5, ha="left", color=GREY)
        empty(ax, 2.2, 2.1, 3.65, 0.55)
        return
    label(ax, 0.4, 3.75, "바이트 사전 (256개)", fs=10.5, ha="left", bold=True, color=RED)
    for k, s in enumerate(BDICT):
        cell(ax, 3.0 + k * 0.78, 3.5, 0.72, 0.5, s, hot=s in ("136", "139", "235"), fs=9.5)
    label(ax, 0.4, 2.35, "\"먹었니\"는", fs=10.5, ha="left", bold=True)
    cell(ax, 2.2, 2.1, 1.3, 0.55, "먹었", fs=12)
    for k, b in enumerate(NI):
        cell(ax, 3.6 + k * 0.75, 2.1, 0.7, 0.55, b, hot=True, fs=11)
    label(ax, 6.0, 2.37, "토큰 4개", fs=10.5, ha="left", color=RED, bold=True)
    moral(ax, 6.0, 0.8, "바이트 256개를 사전에 넣어 두면 어떤 글자든 잘려요")


# ── 9. 사전을 만든 글이 조각 수를 정해요 ────────────────────────────
def lang(ax, step):
    """두 사전과 자른 결과를 한 컷에. 빨강은 두 사전이 갈리는 곳(합친 조각, 한글 0개)과 조각 수."""
    box(ax, 0.3, 3.75, 5.5, 2.25, fc="white", ec=INK, lw=1.4)
    label(ax, 0.55, 5.65, "한국어 메시지 7개로 만든 사전", fs=10.5, ha="left", bold=True, color="#222")
    label(ax, 0.55, 5.1, "한글 글자 24개", fs=10, ha="left", color=INK)
    label(ax, 0.55, 4.6, "합친 조각", fs=10, ha="left", color=INK)
    for k, t in enumerate(["오늘", "점심", "먹었", "날씨"]):
        cell(ax, 1.8 + k * 0.9, 4.35, 0.82, 0.48, t, hot=True, fs=10)
    label(ax, 0.55, 4.05, "바이트 256개", fs=10, ha="left", color=INK)
    box(ax, 6.2, 3.75, 5.5, 2.25, fc="white", ec=INK, lw=1.4)
    label(ax, 6.45, 5.65, "영어 메시지만으로 만든 사전", fs=10.5, ha="left", bold=True, color="#222")
    label(ax, 6.45, 5.1, "영어 글자 a ~ z", fs=10, ha="left", color=INK)
    label(ax, 6.45, 4.6, "합친 조각: 영어 짝만", fs=10, ha="left", color=INK)
    label(ax, 6.45, 4.05, "바이트 256개", fs=10, ha="left", color=INK)
    label(ax, 9.3, 5.1, "한글 글자 0개", fs=10.5, ha="left", color=RED, bold=True)
    label(ax, 0.3, 3.15, "\"오늘 점심 뭐 먹지\"를 자르면", fs=10.5, ha="left", bold=True)
    label(ax, 0.3, 2.35, "한국어 사전", fs=10, ha="left", color=INK)
    label(ax, 0.3, 1.25, "영어 사전", fs=10, ha="left", color=INK)
    x = 2.2
    for t in ["오늘", "점심", "뭐", "먹", "지"]:
        w = 0.42 * len(t) + 0.2
        cell(ax, x, 2.1, w, 0.5, t, hot=True, fs=11)
        x += w + 0.06
    label(ax, x + 0.2, 2.35, "5조각", fs=11, ha="left", color=RED, bold=True)
    x = 2.2
    for ch in "오늘점심뭐먹지":
        label(ax, x + 0.47, 1.7, ch, fs=9.5, color=RED)
        for _ in range(3):
            ax.add_patch(Rectangle((x, 1.0), 0.3, 0.5, fc=PINK, ec=RED, lw=1.2))
            x += 0.32
        x += 0.1
    label(ax, x + 0.1, 1.25, "21조각", fs=11, ha="left", color=RED, bold=True)
    label(ax, x + 0.1, 0.85, "글자마다 바이트 3개", fs=9, ha="left", color=INK)
    moral(ax, 6.0, 0.25, "사전은 만들 때 본 글에서만 합쳐요")


# ── 10. 정리: 처음 장면으로 돌아가기 ───────────────────────────────
def back(ax, step):
    phone(ax, TYPED, hot_word=3)
    program(ax, ["토큰 사전", "먹었니 → 먹었 · 니", "니 → 235 · 139 · 136"], hot=True)
    bubble(ax, *SAY, "합친 순서대로 자르고\n없는 글자는 바이트로 잘라요", TAIL, hot=True, fs=10.5)
    moral(ax, 6.0, 0.35, "처음 보는 낱말도 사전에 있는 토큰으로 잘랐어요")


# ── 11. 정리: 낱말 카드 ────────────────────────────────────────────
def cards():
    """이 편 본문에서 이름 붙인 말 넷. 카드마다 본문 그림을 작게 다시 그리고 한 줄 뜻."""
    fig, ax = canvas(6.4, 8.3, 9.8, 12.7)
    W, H = 9.4, 2.9

    def card(i, name, line):
        x, y = 0.2, 9.65 - i * 3.15
        box(ax, x, y, W, H, fc="white")
        label(ax, x + 0.3, y + H - 0.45, name, fs=12.5, ha="left", bold=True)
        label(ax, x + 7.3, y + 1.1, line, fs=10, color=INK)
        return x, y

    x, y = card(0, "토큰", "글을 자른\n조각 하나")
    xx = x + 0.4
    for p in ["오늘", "점심", "뭐", "먹", "지"]:
        w = 0.38 * len(p) + 0.2
        cell(ax, xx, y + 0.8, w, 0.55, p, hot=True, fs=10.5)
        xx += w + 0.06
    x, y = card(1, "BPE", "자주 붙어 나오는 두 조각을\n하나로 합치기를 되풀이")
    cell(ax, x + 0.5, y + 0.8, 0.55, 0.55, "오", fs=11)
    cell(ax, x + 1.05, y + 0.8, 0.55, 0.55, "늘", fs=11)
    arrow(ax, (x + 1.75, y + 1.07), (x + 2.45, y + 1.07), color=RED, ms=12)
    cell(ax, x + 2.6, y + 0.8, 1.1, 0.55, "오늘", hot=True, fs=11)
    label(ax, x + 4.0, y + 1.07, "3칸 줄어요", fs=10, ha="left", color=INK)
    x, y = card(2, "바이트", "0 ~ 255 가운데\n숫자 하나")
    cell(ax, x + 0.5, y + 0.75, 0.65, 0.65, "니", fs=12)
    arrow(ax, (x + 1.25, y + 1.07), (x + 1.8, y + 1.07), color=GREY, ms=10)
    for k, b in enumerate(NI):
        cell(ax, x + 1.95 + k * 0.85, y + 0.75, 0.75, 0.65, b, hot=True, fs=11)
    x, y = card(3, "토크나이저", "글을 토큰으로\n자르는 도구")
    label(ax, x + 0.4, y + 1.07, "오늘 점심 뭐 먹지", fs=10, ha="left")
    arrow(ax, (x + 2.75, y + 1.07), (x + 3.25, y + 1.07), color=GREY, ms=10)
    xx = x + 3.35
    for p in ["오늘", "점심", "뭐", "먹", "지"]:
        w = 0.27 * len(p) + 0.15
        cell(ax, xx, y + 0.8, w, 0.55, p, hot=True, fs=9)
        xx += w + 0.04
    save(fig, OUT, "ai02-cards.svg")


if __name__ == "__main__":
    S, L = (7.2, 3.8), (12, 6.6)
    stage(chat, 1, OUT, "ai02-chat", S, L)
    stage(opening, 1, OUT, "ai02-open", S, L)
    stage(lambda ax, k: branch(ax), 1, OUT, "ai02-branch", S, L)
    stage(grow, 1, OUT, "ai02-grow", S, L)
    stage(longer, 1, OUT, "ai02-long", S, L)
    stage(lambda ax, k: merge(ax, *[(1, 0), (2, 1), (5, 2)][k - 1]), 3, OUT, "ai02-merge", S, L)
    stage(cutnew, 1, OUT, "ai02-cut", S, L)
    stage(byte, 2, OUT, "ai02-byte", S, L)
    stage(lang, 1, OUT, "ai02-lang", S, L)
    stage(back, 1, OUT, "ai02-back", S, L)
    cards()
