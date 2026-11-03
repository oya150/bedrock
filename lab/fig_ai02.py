"""AI 2편 그림 만들기. 실행: python lab/fig_ai02.py  → docs/ai/img/02/*.svg

본문 절은 장면 띠로 그린다: 같은 무대를 여러 장 그리고 장마다 바뀐 곳만 빨강으로 칠한다.
여는 장면과 돌아오는 장면은 1편 무대(보낸 메시지 다섯 개, 자판, 언어 모델 원통)를 그대로 잇는다.
예시와 숫자는 .claude/writing/work/cal/units-ai02.md, 실측은 lab/ai/02_pieces.py(이 사이트 본문 문장 7,537개)다.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "es"))
from figkit import (GREY, INK, LIGHT, NOTE, PINK, RED, arrow, bits, box, bubble, canvas, cell,  # noqa: E402
                    cylinder, label, moral, outdir, save, stage)
from matplotlib.patches import Rectangle  # noqa: E402

OUT = outdir("02", "ai")

# 1편과 같은 메시지 다섯 개
MSGS = [["오늘", "점심", "뭐", "먹지"], ["오늘", "날씨", "좋다"], ["내일", "점심", "같이", "먹자"],
        ["오늘", "저녁", "뭐", "먹을까"], ["날씨", "뭐", "이래"]]
TYPED = ["내일", "저녁", "뭐", "먹었니"]
CHARS = list("오늘점심뭐먹지날씨좋다내일같이자저녁을까래")  # 메시지 다섯 개의 글자 사전 21개
RULES = [("오", "늘"), ("점", "심"), ("날", "씨")]


def empty(ax, x, y, w, h, s="", color=GREY):
    ax.add_patch(Rectangle((x, y), w, h, fc="white", ec=color, lw=1.2, ls="--"))
    if s:
        label(ax, x + w / 2, y + h / 2, s, fs=12, color=color, bold=color == RED)


# ── 무대: 1편의 휴대폰 자판과 언어 모델 원통 ──────────────────────
CYL = (7.2, 3.35, 4.0, 1.45)
SAY = (6.3, 0.95, 5.5, 1.55)
TAIL = (9.2, 3.1)


def phone(ax, typed, hot_word=None):
    """typed=낱말 목록. hot_word=빨갛게 칠할 낱말 번호. 후보 칸 셋은 빈 점선(이 편은 후보를 띄우지 않는다)."""
    box(ax, 0.4, 0.9, 4.8, 5.55, fc="white")
    label(ax, 0.65, 6.15, "보낸 메시지", fs=10, ha="left", color=INK)
    for k, m in enumerate(MSGS):
        s = " ".join(m)
        w = 0.24 * len(s.replace(" ", "")) + 0.12 * (len(m) - 1) + 0.4
        y = 5.5 - k * 0.52
        ax.add_patch(Rectangle((5.0 - w, y), w, 0.42, fc=NOTE, ec=GREY, lw=1.0))
        label(ax, 5.0 - w / 2, y + 0.21, s, fs=10)
    ax.add_patch(Rectangle((0.6, 2.75), 4.4, 0.5, fc="white", ec=INK, lw=1.4))
    x = 0.8
    for k, wd in enumerate(typed):
        w = 0.27 * len(wd)
        on = k == hot_word
        if on:
            ax.add_patch(Rectangle((x - 0.06, 2.8), w + 0.12, 0.4, fc=PINK, ec=RED, lw=1.6))
        label(ax, x, 3.0, wd, fs=12, ha="left", color=RED if on else "#222", bold=on)
        x += w + 0.16
    label(ax, x - 0.05, 3.0, "|", fs=12, ha="left")
    for k in range(3):
        empty(ax, 0.6 + k * 1.5, 2.05, 1.4, 0.5)
    for r in range(2):
        for k in range(8):
            ax.add_patch(Rectangle((0.65 + k * 0.54 + r * 0.27, 1.45 - r * 0.42), 0.44, 0.33, fc=LIGHT, ec="none"))


def program(ax, name, lines=(), hot=False):
    x, y, w, h = CYL
    cylinder(ax, *CYL, name)
    for k, t in enumerate(lines):
        label(ax, x + w / 2, y + 1.0 - k * 0.55, t, fs=10.5, color=RED if hot else "#222", bold=hot)


def opening(ax, step):
    program(ax, "언어 모델", ["낱말 사전 12개", "오늘 · 점심 · 뭐 · 먹지 …"])
    if step == 1:
        phone(ax, TYPED)
        bubble(ax, *SAY, "낱말마다 사전에서\n찾아요", TAIL)
    else:
        phone(ax, TYPED, hot_word=3)
        bubble(ax, *SAY, "\"먹었니\"는 사전에\n없어요", TAIL, hot=True)
        moral(ax, 6.0, 0.4, "처음 보는 낱말은 표에 줄도 칸도 없어요")


# ── 글자로 자르기 ──────────────────────────────────────────────────
LW = 0.48  # 글자 칸 하나의 폭


def word_cells(ax, x, y, words, hot=(), w=LW, h=0.5, gap=0.2, fs=11):
    """띄어쓰기 덩어리마다 글자 칸으로. hot={(낱말 번호, 글자 번호)} 또는 'all'."""
    for i, wd in enumerate(words):
        for j, ch in enumerate(wd):
            cell(ax, x + j * w, y, w, h, ch, hot=hot == "all" or (i, j) in hot, fs=fs)
        x += len(wd) * w + gap
    return x


def chars(ax, step):
    label(ax, 0.3, 6.2, "보낸 메시지를 글자로 잘라요", fs=11.5, ha="left", bold=True)
    for r, m in enumerate(MSGS):
        y = 5.3 - r * 0.62
        label(ax, 0.45, y + 0.25, str(r + 1), fs=10, color=INK)
        word_cells(ax, 0.75, y, m)
    hot = step == 1
    label(ax, 6.4, 6.2, "글자 사전 (21개)", fs=11.5, ha="left", bold=True, color=RED if hot else "#222")
    for k, ch in enumerate(CHARS):
        cell(ax, 6.4 + (k % 7) * 0.6, 5.3 - (k // 7) * 0.62, 0.52, 0.5, ch, hot=hot, fs=11)
    if step == 1:
        return
    label(ax, 6.4, 3.05, "\"먹었니\"를 글자로 자르면", fs=11, ha="left", color=INK)
    for k, ch in enumerate("먹었니"):
        x = 6.4 + k * 1.2
        cell(ax, x, 1.95, 0.9, 0.6, ch, hot=k > 0, fs=12)
        label(ax, x + 0.45, 1.6, "있음" if k == 0 else "없음", fs=10, color=INK if k == 0 else RED, bold=k > 0)
    label(ax, 9.1, 1.1, "작은 예에서는 아직 구멍이 있어요", fs=10.5, color=RED)


def longer(ax, step):
    s = ["오늘", "점심", "뭐", "먹지"]
    label(ax, 0.3, 6.2, "같은 문장 \"오늘 점심 뭐 먹지\"", fs=11.5, ha="left", bold=True)
    label(ax, 0.3, 5.3, "낱말로 자르면 4조각", fs=11, ha="left")
    xs = [3.6 + k * 1.15 for k in range(4)]
    for k, wd in enumerate(s):
        cell(ax, xs[k], 5.05, 1.05, 0.55, wd, fs=11.5)
    # 앞 낱말 2개로 "먹지"를 맞힌다(1편)
    ax.plot([xs[1], xs[1], xs[2] + 1.05, xs[2] + 1.05], [5.7, 5.85, 5.85, 5.7], color=INK, lw=1.4)
    label(ax, (xs[1] + xs[2] + 1.05) / 2, 6.1, "앞 2조각: 점심 · 뭐", fs=10, color=INK)
    label(ax, xs[3] + 0.52, 4.75, "다음", fs=10, color=INK)
    hot = step == 2
    label(ax, 0.3, 3.3, "글자로 자르면 7조각", fs=11, ha="left", color=RED if hot else "#222", bold=hot)
    letters = list("오늘점심뭐먹지")
    for k, ch in enumerate(letters):
        x = 3.6 + k * 0.62
        if hot:
            cell(ax, x, 3.05, 0.55, 0.55, ch, hot=k in (3, 4), fs=11.5)
        else:
            empty(ax, x, 3.05, 0.55, 0.55)
    if hot:
        x1, x2 = 3.6 + 3 * 0.62, 3.6 + 4 * 0.62 + 0.55
        ax.plot([x1, x1, x2, x2], [3.7, 3.85, 3.85, 3.7], color=RED, lw=1.6)
        label(ax, (x1 + x2) / 2, 4.1, "앞 2조각: 심 · 뭐", fs=10, color=RED, bold=True)
        label(ax, 3.6 + 5 * 0.62 + 0.27, 2.75, "다음", fs=10, color=RED)
        label(ax, 8.4, 3.32, "\"점\"이 안 보여요", fs=10.5, ha="left", color=RED)
        moral(ax, 6.0, 1.3, "글자로 자르면 앞 2조각이 보는 범위가 좁아져요")


# ── 합치기: 오+늘 → 점+심 → 날+씨 ─────────────────────────────────
def pieces(word, rules):
    w = list(word)
    for a, b in rules:
        i = 0
        while i + 1 < len(w):
            if w[i] == a and w[i + 1] == b:
                w[i:i + 2] = [a + b]
            else:
                i += 1
    return w


TALLY = [("오 + 늘", "3번"), ("점 + 심", "2번"), ("날 + 씨", "2번"), ("나머지 짝", "1번씩")]


def merge(ax, step):
    done = RULES[:step - 1]
    label(ax, 0.3, 6.2, "보낸 메시지 (글자에서 시작)", fs=11.5, ha="left", bold=True)
    for r, m in enumerate(MSGS):
        y = 5.3 - r * 0.7
        label(ax, 0.45, y + 0.25, str(r + 1), fs=10, color=INK)
        x = 0.75
        for wd in m:
            for p in pieces(wd, done):
                w = LW * len(p)
                if step == 1:
                    on = wd == "오늘"
                else:
                    on = len(p) == 2 and (p[0], p[1]) == RULES[step - 2]
                cell(ax, x, y, w, 0.5, p, hot=on, fs=11)
                x += w
            x += 0.2
    label(ax, 6.6, 6.2, "두 글자가 붙어 나온 횟수", fs=11, ha="left", bold=True)
    for k, (pair, n) in enumerate(TALLY):
        y = 5.4 - k * 0.48
        used = k < step - 1
        on = step == 1 and k == 0
        c = RED if on else (GREY if used else "#222")
        label(ax, 6.8, y, pair, fs=10.5, ha="left", color=c, bold=on)
        label(ax, 8.5, y, n, fs=10.5, ha="left", color=c, bold=on)
        if used:
            ax.plot([6.75, 9.3], [y, y], color=GREY, lw=1.2)
    label(ax, 6.6, 3.2, "합친 순서", fs=11, ha="left", bold=True)
    for k in range(3):
        y = 2.5 - k * 0.6
        if k < step - 1:
            a, b = RULES[k]
            on = k == step - 2
            cell(ax, 6.8, y, 2.6, 0.48, f"{'①②③'[k]} {a} + {b} → {a}{b}", hot=on, fs=10.5)
        else:
            empty(ax, 6.8, y, 2.6, 0.48)
    if step == 1:
        label(ax, 3.0, 1.35, "\"오\" 다음에 \"늘\"이 3번 붙어 나왔어요", fs=10.5, color=RED)
        label(ax, 3.0, 0.85, "띄어쓰기로 나눈 낱말 안에서만 세요", fs=10, color=INK)
    if step == 4:
        moral(ax, 3.2, 1.0, "가장 자주 붙어 나온 둘부터 하나로 합쳤어요", fs=11.5)


# ── 합치기 횟수: 사전 크기와 문장 길이 ─────────────────────────────
TRADE = [("0번", 1071, 23.9), ("500번", 1571, 16.1), ("2,000번", 3071, 12.7), ("8,000번", 9071, 10.3)]


def trade():
    fig, ax = canvas(7.2, 3.8, 12, 6.6)
    label(ax, 0.3, 6.25, "합치기 횟수", fs=11, ha="left", bold=True)
    label(ax, 2.0, 6.25, "토큰 사전 크기 (한 칸 = 1,000개)", fs=11, ha="left", bold=True)
    label(ax, 6.5, 6.25, "시험 문장 하나의 토큰 수 (한 칸 = 1개)", fs=11, ha="left", bold=True)
    for k, (name, size, n) in enumerate(TRADE):
        y = 5.0 - k * 1.05
        label(ax, 0.3, y + 0.25, name, fs=11, ha="left")
        for i in range(10):
            fill = min(max(size / 1000 - i, 0), 1)
            if fill <= 0:
                break
            ax.add_patch(Rectangle((2.0 + i * 0.3, y), 0.26, 0.5, fc="white", ec=INK, lw=0.8))
            ax.add_patch(Rectangle((2.0 + i * 0.3, y), 0.26 * fill, 0.5, fc=PINK, ec="none"))
        label(ax, 2.0, y - 0.3, f"{size:,}개", fs=9.5, ha="left", color=INK)
        for i in range(24):
            fill = min(max(n - i, 0), 1)
            if fill <= 0:
                break
            ax.add_patch(Rectangle((6.5 + i * 0.19, y), 0.16, 0.5, fc="white", ec=INK, lw=0.6))
            ax.add_patch(Rectangle((6.5 + i * 0.19, y), 0.16 * fill, 0.5, fc=PINK, ec="none"))
        label(ax, 6.5, y - 0.3, f"{n}개", fs=9.5, ha="left", color=INK)
    arrow(ax, (5.6, 5.2), (5.6, 2.0), color=RED, ms=14)
    label(ax, 5.75, 3.6, "커져요", fs=10.5, ha="left", color=RED, bold=True)
    arrow(ax, (11.4, 5.2), (11.4, 2.0), color=RED, ms=14)
    label(ax, 11.25, 3.6, "짧아져요", fs=10.5, ha="right", color=RED, bold=True)
    moral(ax, 6.0, 0.6, "합치기를 늘리면 사전은 커지고 문장은 짧아졌어요")
    save(fig, OUT, "ai02-trade.svg")


# ── 처음 보는 낱말도 아는 토큰으로 ─────────────────────────────────
NEW = [("설명만으로는", ["설명", "만", "으로는"]), ("늘어나기도", ["늘어", "나", "기도"]), ("확실하게", ["확", "실", "하게"])]


def newword(ax, step):
    label(ax, 0.4, 6.2, "처음 보는 낱말", fs=11.5, ha="left", bold=True)
    label(ax, 3.3, 6.2, "낱말 사전", fs=11.5, ha="left", bold=True)
    label(ax, 5.3, 6.2, "토큰 사전(합치기 2,000번)으로 자르면", fs=11.5, ha="left", bold=True)
    for k, (wd, ps) in enumerate(NEW):
        y = 5.0 - k * 1.1
        if k > 0 and step < 3:
            continue
        row_hot = (k == 0 and step == 1) or (k > 0 and step == 3)
        cell(ax, 0.4, y, 2.6, 0.55, wd, hot=row_hot, fs=11.5)
        label(ax, 3.4, y + 0.27, "✗ 없어요", fs=11, ha="left", color=RED if row_hot else INK, bold=row_hot)
        if k == 0 and step == 1:
            empty(ax, 5.3, y, 3.0, 0.55)
            continue
        on = (k == 0 and step == 2) or (k > 0 and step == 3)
        x = 5.3
        for p in ps:
            w = 0.42 * len(p) + 0.2
            cell(ax, x, y, w, 0.55, p, hot=on, fs=11.5)
            x += w + 0.08
        label(ax, x + 0.15, y + 0.27, "✓ 모두 사전에 있어요", fs=10.5, ha="left", color=RED if on else INK)
    if step == 3:
        moral(ax, 6.0, 1.0, "처음 보는 낱말도 사전에 있는 토큰으로 잘랐어요")


# ── 전환: 남는 문제 ────────────────────────────────────────────────
def turn(ax, step):
    program(ax, "언어 모델", ["토큰 사전(합치기 2,000번)", "먹었니 → 먹 · 었 · 니"])
    if step == 1:
        phone(ax, TYPED)
        bubble(ax, *SAY, "\"먹었니\"도 아는 토큰으로\n잘랐어요", TAIL)
        return
    phone(ax, TYPED)
    bubble(ax, 6.3, 0.2, 5.6, 2.45, "", TAIL, hot=True)
    label(ax, 9.1, 2.25, "그래도 남는 문제가 있어요", fs=11.5, color=RED, bold=True)
    for k, t in enumerate(["① 사전에 없는 글자는 못 잘라요", "② 언어마다 토큰 수가 달라요", "③ 뜻과 상관없이 잘라요"]):
        label(ax, 6.55, 1.65 - k * 0.52, t, fs=10.5, ha="left", color=RED)


# ── 첫째: 바이트 ───────────────────────────────────────────────────
BYTES = [236, 151, 136]  # "었"을 UTF-8로 적은 바이트
DICT = ["0", "1", "2", "…", "136", "…", "151", "…", "236", "…", "255"]


def byte(ax, step):
    label(ax, 0.4, 6.2, "글자", fs=11, ha="left", bold=True)
    cell(ax, 0.4, 4.9, 0.9, 0.8, "었", hot=step == 1, fs=14)
    label(ax, 0.85, 4.5, "사전에 없는 글자", fs=9.5, color=RED if step == 1 else INK)
    if step >= 2:
        on = step == 2
        arrow(ax, (1.45, 5.3), (2.15, 5.3), color=RED if on else GREY, ms=12)
        label(ax, 2.25, 6.2, "글자 번호", fs=11, ha="left", bold=True, color=RED if on else "#222")
        cell(ax, 2.25, 4.9, 1.7, 0.8, "50,632", hot=on, fs=13)
    if step >= 3:
        on = step == 3
        arrow(ax, (4.1, 5.3), (4.8, 5.3), color=RED if on else GREY, ms=12)
        label(ax, 4.9, 6.2, "UTF-8 규칙으로 바이트 3개에 적어요", fs=11, ha="left", bold=True, color=RED if on else "#222")
        for k, b in enumerate(BYTES):
            cell(ax, 4.9 + k * 1.0, 4.9, 0.9, 0.8, b, hot=on, fs=13)
        label(ax, 8.0, 5.3, "번호를 그냥 셋으로\n나눈 숫자가 아니에요", fs=9.5, ha="left", color=RED if on else INK)
        bits(ax, 4.9, 3.7, "11101100", w=0.3, h=0.45, hot=range(8) if on else ())
        ax.plot([4.9, 5.35], [4.85, 4.2], color=GREY, lw=1.0)
        label(ax, 7.4, 3.92, "바이트 하나 = 0·1 칸 8개 = 0 ~ 255", fs=10, ha="left", color=RED if on else INK)
    if step >= 4:
        label(ax, 0.4, 2.85, "바이트 사전 (256개 전부)", fs=11, ha="left", bold=True, color=RED)
        for k, s in enumerate(DICT):
            cell(ax, 0.4 + k * 0.92, 2.0, 0.84, 0.55, s, hot=s in ("136", "151", "236"), fs=10.5)
        moral(ax, 6.0, 1.0, "바이트 256개를 사전에 넣어 두면 어떤 글자도 자를 수 있어요")


# ── 둘째: 언어마다 토큰 수 ─────────────────────────────────────────
# 옛 공개 토크나이저는 "오늘 점심 뭐 먹지?"를 14토큰으로 자른다. 글자 하나가 바이트 조각 여럿으로 갈리기도 한다.
OLD_KO = [("오", 1), ("늘", 2), ("점", 2), ("심", 2), ("뭐", 2), ("먹", 3), ("지", 1), ("?", 1)]
EN = ["What", "should", "I", "eat", "for", "lunch", "today", "?"]
NEW_KO = ["오늘", "점", "심", "뭐", "먹", "지", "?"]


def lang(ax, step):
    X0 = 3.7
    rows = [(5.2, "옛 공개 토크나이저", "한국어 14토큰"), (3.7, "옛 공개 토크나이저", "영어 8토큰"),
            (2.2, "새 공개 토크나이저", "한국어 7토큰")]
    for k, (y, who, what) in enumerate(rows):
        on = step == k + 1
        shown = step > k
        label(ax, 0.3, y + 0.45, who, fs=10.5, ha="left", color=INK)
        label(ax, 0.3, y + 0.05, what, fs=11, ha="left", bold=True, color=RED if on else ("#222" if shown else GREY))
        if not shown:
            empty(ax, X0, y - 0.1, 7.6, 0.55)
            continue
        x = X0
        if k == 0:
            for ch, n in OLD_KO:
                if n == 1:
                    cell(ax, x, y - 0.1, 0.5, 0.55, ch, hot=on, fs=11)
                    x += 0.64
                    continue
                gx = x
                for _ in range(n):
                    ax.add_patch(Rectangle((x, y - 0.1), 0.26, 0.55, fc=PINK if on else LIGHT, ec=RED if on else INK, lw=1.2))
                    x += 0.32
                label(ax, (gx + x - 0.06) / 2, y + 0.65, ch, fs=10.5, color=RED if on else INK)
                ax.plot([gx, gx, x - 0.06, x - 0.06], [y + 0.5, y + 0.55, y + 0.55, y + 0.5], color=RED if on else INK, lw=1.0)
                x += 0.14
            label(ax, X0, y - 0.45, "가는 칸 = 글자 하나를 바이트로 쪼갠 토큰", fs=9.5, ha="left", color=RED if on else INK)
        elif k == 1:
            for wd in EN:
                w = 0.16 * len(wd) + 0.3
                cell(ax, x, y - 0.1, w, 0.55, wd, hot=on, fs=10.5)
                x += w + 0.06
        else:
            for wd in NEW_KO:
                w = 0.4 * len(wd) + 0.12
                cell(ax, x, y - 0.1, w, 0.55, wd, hot=on, fs=11)
                x += w + 0.06
    if step == 3:
        moral(ax, 6.0, 0.9, "같은 뜻 문장도 토큰 사전에 따라 토큰 수가 달라요")


# ── 셋째: 뜻과 다른 자름 ───────────────────────────────────────────
BPE_CUT = ["주", "말", "에", "도", "서", "관", "에서", "책", "을", "읽", "었", "어요"]
KIWI_CUT = ["주말", "에", "도서관", "에서", "책", "을", "읽", "었", "어요"]


def row_cut(ax, x, y, parts, hot_parts=(), dim=False, fs=11):
    for k, p in enumerate(parts):
        w = 0.42 * len(p) + 0.12
        if dim:
            empty(ax, x, y, w, 0.55)
        else:
            cell(ax, x, y, w, 0.55, p, hot=k in hot_parts, fs=fs)
        x += w + 0.06
    return x


def kiwi(ax, step):
    label(ax, 0.3, 6.2, "주말에 도서관에서 책을 읽었어요", fs=12, ha="left", bold=True)
    label(ax, 0.3, 5.0, "합치기 2,000번으로", fs=11, ha="left")
    row_cut(ax, 3.4, 4.75, BPE_CUT, hot_parts=(3, 4, 5) if step == 1 else ())
    if step == 1:
        label(ax, 6.0, 4.3, "\"도서관\"이 세 토큰으로 갈렸어요", fs=10.5, color=RED)
    on = step == 2
    label(ax, 0.3, 3.3, "형태소 분석기로", fs=11, ha="left", color=RED if on else "#222", bold=on)
    row_cut(ax, 3.4, 3.05, KIWI_CUT, hot_parts=(2,) if on else (), dim=not on)
    if on:
        label(ax, 6.0, 2.6, "\"도서관\"을 한 덩어리로 남겨요", fs=10.5, color=RED)
        moral(ax, 6.0, 1.3, "합치기는 횟수만 보고 뜻은 보지 않아요")


# ── 어떤 자르기를 언제 쓸까: 갈림길 ────────────────────────────────
def decide():
    fig, ax = canvas(9.4, 3.6, 14, 5.4)
    box(ax, 0.3, 3.3, 5.0, 1.5, fc=NOTE)
    label(ax, 2.8, 4.05, "기계가 다음 토큰을\n맞혀야 하나요?", fs=11.5, bold=True)
    arrow(ax, (5.4, 4.05), (6.9, 4.05), color=RED)
    label(ax, 6.15, 4.4, "예", fs=10.5, color=RED)
    box(ax, 7.0, 3.1, 6.7, 1.9, fc=PINK, ec=RED)
    label(ax, 10.35, 4.05, "BPE로 잘라요\n모르는 글자는 바이트로\n(언어 모델의 입력)", fs=10.5, color=RED)
    arrow(ax, (2.8, 3.2), (2.8, 2.0))
    label(ax, 3.05, 2.6, "아니요", fs=10.5, color=INK, ha="left")
    box(ax, 0.3, 0.5, 5.0, 1.4, fc=LIGHT, ec=GREY)
    label(ax, 2.8, 1.2, "사람이 뜻으로 찾거나\n고쳐야 해요", fs=10.5)
    arrow(ax, (5.4, 1.2), (6.9, 1.2))
    box(ax, 7.0, 0.5, 6.7, 1.4, fc=LIGHT, ec=GREY)
    label(ax, 10.35, 1.2, "형태소 분석기로 잘라요\n(검색 엔진이 글을 정리할 때,\n맞춤법 검사)", fs=10.5)
    save(fig, OUT, "ai02-decide.svg")


# ── 정리: 처음 장면으로 돌아가기 ───────────────────────────────────
def back(ax, step):
    if step == 1:
        phone(ax, TYPED, hot_word=None)
        program(ax, "언어 모델", ["낱말 사전 12개"])
        bubble(ax, *SAY, "처음엔 \"먹었니\"가 사전에\n없어서 막혔어요", TAIL)
    elif step == 2:
        phone(ax, TYPED)
        program(ax, "언어 모델", ["글자 21개 · 합친 토큰", "· 바이트 256개"], hot=True)
        bubble(ax, *SAY, "토큰 사전으로 바꿨어요", TAIL, hot=True)
    else:
        phone(ax, TYPED, hot_word=3)
        program(ax, "언어 모델", ["먹었니 → 먹 · 었 · 니", "었 · 니는 바이트 3개씩"])
        bubble(ax, *SAY, "사전에 없는 글자는\n바이트로 잘라요", TAIL)
        moral(ax, 6.0, 0.4, "어떤 낱말이든 사전에 있는 토큰으로 잘랐어요")


# ── 정리: 낱말 카드 ────────────────────────────────────────────────
def cards():
    """이 편 본문에서 이름 붙인 말 셋. 카드마다 본문 그림을 작게 다시 그리고 한 줄 뜻."""
    fig, ax = canvas(6.4, 6.3, 9.8, 9.6)
    W, H = 9.4, 2.9

    def card(i, name, line):
        x, y = 0.2, 6.5 - i * 3.15
        box(ax, x, y, W, H, fc="white")
        label(ax, x + 0.3, y + H - 0.45, name, fs=12.5, ha="left", bold=True)
        label(ax, x + 7.0, y + 1.1, line, fs=10, color=INK)
        return x, y

    x, y = card(0, "토큰", "글을 자른\n조각 하나")
    xx = x + 0.4
    for p in ["설명", "만", "으로는"]:
        w = 0.4 * len(p) + 0.2
        cell(ax, xx, y + 0.8, w, 0.55, p, hot=True, fs=10.5)
        xx += w + 0.08
    x, y = card(1, "BPE", "자주 붙어 나오는 두 조각을\n하나로 합치기를 되풀이")
    cell(ax, x + 0.5, y + 0.8, 0.55, 0.55, "오", fs=11)
    cell(ax, x + 1.05, y + 0.8, 0.55, 0.55, "늘", fs=11)
    arrow(ax, (x + 1.75, y + 1.07), (x + 2.45, y + 1.07), color=RED, ms=12)
    cell(ax, x + 2.6, y + 0.8, 1.1, 0.55, "오늘", hot=True, fs=11)
    label(ax, x + 4.0, y + 1.07, "3번", fs=10, ha="left", color=INK)
    x, y = card(2, "바이트", "0 ~ 255 숫자\n하나를 담는 칸")
    cell(ax, x + 0.5, y + 0.75, 0.65, 0.65, "었", fs=12)
    arrow(ax, (x + 1.25, y + 1.07), (x + 1.8, y + 1.07), color=GREY, ms=10)
    for k, b in enumerate(BYTES):
        cell(ax, x + 1.95 + k * 0.85, y + 0.75, 0.75, 0.65, b, hot=True, fs=11)
    save(fig, OUT, "ai02-cards.svg")


if __name__ == "__main__":
    S, L = (7.2, 3.8), (12, 6.6)
    stage(opening, 2, OUT, "ai02-open", S, L)
    stage(chars, 2, OUT, "ai02-chars", S, L)
    stage(longer, 2, OUT, "ai02-long", S, L)
    stage(merge, 4, OUT, "ai02-merge", S, L)
    trade()
    stage(newword, 3, OUT, "ai02-new", S, L)
    stage(turn, 2, OUT, "ai02-turn", S, L)
    stage(byte, 4, OUT, "ai02-byte", S, L)
    stage(lang, 3, OUT, "ai02-lang", S, L)
    stage(kiwi, 2, OUT, "ai02-kiwi", S, L)
    decide()
    stage(back, 3, OUT, "ai02-back", S, L)
    cards()
