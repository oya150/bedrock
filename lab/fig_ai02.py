"""AI 2편 그림 만들기. 실행: python lab/fig_ai02.py  → docs/ai/img/02/*.svg

예시는 1편의 보낸 메시지 다섯 개에 두 개를 더한 일곱 개를 편 끝까지 잇는다.
그림 안 글씨는 낱말과 숫자만 둔다. 문장은 본문과 그림 설명에 둔다(쉬운글-정책 5장).
숫자는 모두 이 일곱 메시지로 직접 센 것이다.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "es"))
from figkit import GREY, INK, PINK, RED, arrow, box, canvas, cell, label, outdir, save  # noqa: E402
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


def make(draw, name, y0, y1):
    """가로 0~12, 세로 y0~y1 만 남겨 그린다. 빈 아래쪽이 남지 않게."""
    fig, ax = canvas(7.2, 0.6 * (y1 - y0), 12, y1)
    ax.set_ylim(y0, y1)
    ax.add_patch(Rectangle((0, y0), 12, y1 - y0, fill=False, ec="none"))
    draw(ax)
    save(fig, OUT, name)


def empty(ax, x, y, w, h, s="", color=GREY):
    ax.add_patch(Rectangle((x, y), w, h, fc="white", ec=color, lw=1.2, ls="--"))
    if s:
        label(ax, x + w / 2, y + h / 2, s, fs=12, color=color, bold=color == RED)


# ── 낱말 사전에 없는 "먹었니" ─────────────────────────────────────
def opening(ax):
    label(ax, 0.3, 6.95, "보낸 메시지", fs=11.5, ha="left", bold=True)
    for r, m in enumerate(MSGS):
        y = 6.15 - r * 0.6
        label(ax, 0.45, y + 0.23, str(r + 1), fs=10, color=INK)
        for k, wd in enumerate(m):
            cell(ax, 0.75 + k * 1.0, y, 0.94, 0.46, wd, fs=10.5)
    label(ax, 0.3, 1.78, "입력", fs=10.5, ha="left", color=INK)
    x = 1.1
    for k, wd in enumerate(TYPED):
        w = 0.3 * len(wd) + 0.3
        cell(ax, x, 1.55, w, 0.46, wd, hot=k == 3, fs=10.5)
        x += w + 0.08
    label(ax, 0.3, 1.0, "후보", fs=10.5, ha="left", color=INK)
    for k in range(3):
        empty(ax, 1.1 + k * 1.05, 0.77, 0.95, 0.46, "?", color=RED)
    label(ax, 6.3, 6.95, "낱말 사전 15개", fs=11.5, ha="left", bold=True)
    for k, w in enumerate(WORDS):
        cell(ax, 6.3 + (k % 3) * 1.6, 6.15 - (k // 3) * 0.6, 1.5, 0.46, w, fs=10.5)
    cell(ax, 6.3, 2.35, 1.5, 0.5, "먹었니", hot=True, fs=11)
    arrow(ax, (7.95, 2.6), (8.6, 2.6), color=RED, ms=12)
    label(ax, 8.85, 2.6, "?", fs=15, color=RED, bold=True)


# ── 메시지 6, 7번을 더할 때 낱말 사전과 글자 사전 ─────────────────
def grow(ax):
    old = MSGS[:5]
    old_w = set(w for m in old for w in m)
    old_c = set("".join(w for m in old for w in m))
    src = {}
    for n in (5, 6):
        for w in MSGS[n]:
            src.setdefault(w, n + 1)
            for c in w:
                src.setdefault(c, n + 1)
    for k, n in enumerate((5, 6)):
        y = 6.3 - k * 0.6
        label(ax, 0.3, y + 0.23, f"{n + 1}번", fs=10.5, ha="left", color=INK)
        for j, wd in enumerate(MSGS[n]):
            cell(ax, 1.0 + j * 1.05, y, 1.0, 0.46, wd, fs=10.5)
    label(ax, 0.3, 4.55, "낱말 사전", fs=11, ha="left", bold=True)
    x = 1.7
    for w in WORDS:
        cw = 0.26 * len(w) + 0.1
        new = w not in old_w
        cell(ax, x, 4.3, cw, 0.5, w, fs=9)
        if new:
            label(ax, x + cw / 2, 4.07, f"{src[w]}번", fs=8.5, color=INK)
        x += cw
    label(ax, 1.7, 3.6, "12개 → 15개", fs=10.5, ha="left", color=INK, bold=True)
    label(ax, 4.0, 3.6, "6번 +2", fs=10.5, ha="left", color=INK)
    label(ax, 5.4, 3.6, "7번 +1", fs=10.5, ha="left", color=INK)
    label(ax, 0.3, 2.65, "글자 사전", fs=11, ha="left", bold=True)
    for k, c in enumerate(CHARS):
        new = c not in old_c
        cell(ax, 1.7 + k * 0.405, 2.4, 0.38, 0.5, c, fs=9.5)
        if new:
            label(ax, 1.7 + k * 0.405 + 0.19, 2.17, f"{src[c]}번", fs=8.5, color=INK)
    label(ax, 1.7, 1.7, "21개 → 24개", fs=10.5, ha="left", color=INK, bold=True)
    label(ax, 4.0, 1.7, "6번 +3", fs=10.5, ha="left", color=INK)
    label(ax, 5.4, 1.7, "7번 +0", fs=14, ha="left", color=RED, bold=True)


# ── 같은 말을 낱말로, 글자로 ──────────────────────────────────────
def longer(ax):
    label(ax, 0.3, 4.6, "낱말", fs=11, ha="left")
    for k, wd in enumerate(["오늘", "점심", "뭐", "먹지"]):
        cell(ax, 1.6 + k * 1.2, 4.3, 1.1, 0.55, wd, fs=11.5)
    label(ax, 6.7, 4.57, "4조각", fs=11.5, ha="left", color=INK, bold=True)
    label(ax, 0.3, 3.4, "글자", fs=11, ha="left", color=RED, bold=True)
    for k, ch in enumerate("오늘점심뭐먹지"):
        cell(ax, 1.6 + k * 0.68, 3.1, 0.6, 0.55, ch, hot=True, fs=11.5)
    label(ax, 6.7, 3.37, "7조각", fs=11.5, ha="left", color=RED, bold=True)


# ── 합치기: 오+늘 → 점+심 → 먹+었 → 날+씨 ───────────────────────────
PAIRS = [("오 + 늘", "3번"), ("점 + 심", "3번"), ("먹 + 었", "2번"), ("날 + 씨", "2번"), ("나머지", "1번씩")]
CW = 0.4


def merge(ax, step, prev):
    """step=합친 횟수+1. prev=앞 장의 step. 앞 장 뒤로 합친 곳을 모두 빨갛게 칠한다."""
    done = RULES[:step - 1]
    new = RULES[max(prev - 1, 0):step - 1]
    label(ax, 0.3, 6.3, "보낸 메시지", fs=11, ha="left", bold=True)
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
                    on = step < 5 and len(p) == 2 and (p[0], p[1]) in new
                cell(ax, x, y, w, 0.42, p, hot=on, fs=10.5)
                x += w
            x += 0.16
    label(ax, 6.3, 6.3, "붙어 나온 짝", fs=11, ha="left", bold=True)
    for k, (pair, n) in enumerate(PAIRS):
        y = 5.75 - k * 0.42
        used = k < step - 1
        on = step == 1 and k < 2
        c = RED if on else (GREY if used else "#222")
        label(ax, 6.5, y, pair, fs=10.5, ha="left", color=c, bold=on)
        label(ax, 8.2, y, n, fs=10.5, ha="left", color=c, bold=on)
        if used:
            ax.plot([6.45, 8.9], [y, y], color=GREY, lw=1.2)
    label(ax, 6.3, 3.35, "합친 순서", fs=11, ha="left", bold=True)
    label(ax, 9.6, 3.35, f"처음 {SLOTS[0]}조각", fs=10.5, ha="left", color=INK)
    for k in range(4):
        y = 2.65 - k * 0.55
        if k < step - 1:
            a, b = RULES[k]
            on = step < 5 and RULES[k] in new
            cell(ax, 6.5, y, 2.9, 0.45, f"{'①②③④'[k]} {a} + {b} → {a}{b}", hot=on, fs=10.5)
            label(ax, 9.6, y + 0.22, f"−{SLOTS[k] - SLOTS[k + 1]}  {SLOTS[k + 1]}조각", fs=10.5, ha="left",
                  color=RED if on else INK, bold=on)
        else:
            empty(ax, 6.5, y, 2.9, 0.45)
    if step == 5:
        label(ax, 0.3, 1.1, "사전  글자 24개 + 합친 조각 4개 = 28개", fs=10.5, ha="left", color=RED, bold=True)


# ── 처음 보는 "먹었니"를 합친 순서대로 ─────────────────────────────
def cutnew(ax):
    label(ax, 7.3, 6.3, "합친 순서", fs=11, ha="left", bold=True)
    for k, (a, b) in enumerate(RULES):
        y = 5.55 - k * 0.6
        cell(ax, 7.3, y, 2.6, 0.45, f"{'①②③④'[k]} {a} + {b} → {a}{b}", hot=k == 2, fs=10.5)
    label(ax, 0.3, 5.82, "글자", fs=11, ha="left", color=INK)
    for k, ch in enumerate("먹었니"):
        cell(ax, 2.2 + k * 0.75, 5.55, 0.7, 0.55, ch, fs=12)
    arrow(ax, (3.35, 5.45), (3.35, 4.8), color=RED, ms=12)
    label(ax, 3.6, 5.12, "③", fs=11, ha="left", color=RED, bold=True)
    label(ax, 0.3, 4.42, "자른 결과", fs=11, ha="left", color=RED, bold=True)
    cell(ax, 2.2, 4.15, 1.45, 0.55, "먹었", hot=True, fs=12)
    cell(ax, 3.7, 4.15, 0.7, 0.55, "니", hot=True, fs=12)
    label(ax, 0.3, 2.8, "글자 사전 24개", fs=11, ha="left", bold=True)
    for k, c in enumerate(CHARS):
        cell(ax, 0.3 + k * 0.42, 1.95, 0.38, 0.48, c, fs=9)
    empty(ax, 0.3 + 24 * 0.42 + 0.15, 1.95, 0.48, 0.48, "니", color=RED)
    label(ax, 0.3 + 24 * 0.42 + 0.39, 1.6, "없음", fs=9.5, color=RED, bold=True)


# ── "니"를 바이트로 ───────────────────────────────────────────────
BDICT = ["0", "1", "2", "…", "136", "…", "139", "…", "235", "…", "255"]


def byte(ax):
    label(ax, 0.4, 6.3, "글자", fs=11, ha="left", bold=True)
    cell(ax, 0.4, 5.0, 0.8, 0.8, "니", fs=14)
    arrow(ax, (1.35, 5.4), (2.0, 5.4), color=RED, ms=12)
    label(ax, 2.1, 6.3, "글자 번호", fs=11, ha="left", bold=True)
    cell(ax, 2.1, 5.0, 1.6, 0.8, "45768", fs=13)
    arrow(ax, (3.85, 5.4), (4.5, 5.4), color=RED, ms=12)
    label(ax, 4.6, 6.3, "바이트 3개", fs=11, ha="left", bold=True, color=RED)
    for k, b in enumerate(NI):
        cell(ax, 4.6 + k * 0.9, 5.0, 0.8, 0.8, b, hot=True, fs=13)
    label(ax, 7.6, 5.4, "바이트 하나 = 0 ~ 255", fs=10.5, ha="left", color=INK)
    label(ax, 0.4, 3.75, "바이트 256개", fs=11, ha="left", bold=True)
    for k, s in enumerate(BDICT):
        cell(ax, 2.6 + k * 0.78, 3.5, 0.72, 0.5, s, hot=s in ("136", "139", "235"), fs=9.5)
    label(ax, 0.4, 2.37, "먹었니", fs=11, ha="left", bold=True)
    arrow(ax, (1.4, 2.37), (2.05, 2.37), color=GREY, ms=10)
    cell(ax, 2.2, 2.1, 1.3, 0.55, "먹었", fs=12)
    for k, b in enumerate(NI):
        cell(ax, 3.6 + k * 0.75, 2.1, 0.7, 0.55, b, hot=True, fs=11)
    label(ax, 6.0, 2.37, "토큰 4개", fs=11, ha="left", color=RED, bold=True)


# ── 사전을 만든 글에 따라 조각 수가 달라요 ──────────────────────────
def lang(ax):
    box(ax, 0.3, 3.75, 5.5, 2.25, fc="white", ec=INK, lw=1.4)
    label(ax, 0.55, 5.65, "한국어 메시지로 만든 사전", fs=10.5, ha="left", bold=True)
    label(ax, 0.55, 5.1, "한글 글자 24개", fs=10, ha="left", color=INK)
    label(ax, 0.55, 4.6, "합친 조각", fs=10, ha="left", color=INK)
    for k, t in enumerate(["오늘", "점심", "먹었", "날씨"]):
        cell(ax, 1.8 + k * 0.9, 4.35, 0.82, 0.48, t, hot=True, fs=10)
    label(ax, 0.55, 4.05, "바이트 256개", fs=10, ha="left", color=INK)
    box(ax, 6.2, 3.75, 5.5, 2.25, fc="white", ec=INK, lw=1.4)
    label(ax, 6.45, 5.65, "영어 글로만 만든 사전", fs=10.5, ha="left", bold=True)
    label(ax, 6.45, 5.1, "영어 글자 a ~ z", fs=10, ha="left", color=INK)
    label(ax, 6.45, 4.6, "합친 조각  영어 짝", fs=10, ha="left", color=INK)
    label(ax, 6.45, 4.05, "바이트 256개", fs=10, ha="left", color=INK)
    label(ax, 9.3, 5.1, "한글 0개", fs=10.5, ha="left", color=RED, bold=True)
    label(ax, 0.3, 3.15, "오늘 점심 뭐 먹지", fs=11, ha="left", bold=True)
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
    label(ax, x + 0.1, 0.85, "7 × 3", fs=9.5, ha="left", color=INK)


if __name__ == "__main__":
    make(opening, "ai02-open-1.svg", 0.5, 7.3)
    make(grow, "ai02-grow-1.svg", 1.4, 6.95)
    make(longer, "ai02-long-1.svg", 2.9, 5.05)
    for k, (step, prev) in enumerate([(1, 0), (2, 1), (5, 2)]):
        make(lambda ax, s=step, p=prev: merge(ax, s, p), f"ai02-merge-{k + 1}.svg", 0.8, 6.6)
    make(cutnew, "ai02-cut-1.svg", 1.3, 6.6)
    make(byte, "ai02-byte-1.svg", 1.8, 6.6)
    make(lang, "ai02-lang-1.svg", 0.6, 6.2)
