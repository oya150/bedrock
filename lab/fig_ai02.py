"""AI 2편 그림 만들기. 실행: python lab/fig_ai02.py  → docs/ai/img/02/*.svg

본문 절은 장면 띠로 그린다: 같은 무대를 여러 장 그리고 장마다 바뀐 곳만 빨강으로 칠한다.
여는 장면과 돌아오는 장면은 1편 무대(보낸 메시지, 자판, 언어 모델 원통)를 그대로 잇는다.
예시와 숫자는 .claude/writing/work/cal/units-ai02-v2.md 의 메시지 7개뿐이다. 실험 숫자는 쓰지 않는다.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "es"))
from figkit import (GREY, INK, LIGHT, NOTE, PINK, RED, arrow, bits, box, bubble, canvas, cell,  # noqa: E402
                    cylinder, label, magnifier, moral, outdir, save, stage)
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


def empty(ax, x, y, w, h, s="", color=GREY):
    ax.add_patch(Rectangle((x, y), w, h, fc="white", ec=color, lw=1.2, ls="--"))
    if s:
        label(ax, x + w / 2, y + h / 2, s, fs=12, color=color, bold=color == RED)


def hbrace(ax, x1, x2, y, s, color=INK, fs=10):
    """칸 위에 묶음 괄호와 이름."""
    ax.plot([x1, x1, x2, x2], [y, y + 0.15, y + 0.15, y], color=color, lw=1.5)
    label(ax, (x1 + x2) / 2, y + 0.42, s, fs=fs, color=color, bold=color == RED)


# ── 무대: 1편의 휴대폰 자판과 언어 모델 원통 ──────────────────────
CYL = (7.2, 3.35, 4.0, 1.45)
SAY = (6.3, 0.95, 5.5, 1.55)
TAIL = (9.2, 3.1)


def phone(ax, typed=(), hot_word=None, hot_msgs=(), cand="empty"):
    """typed=낱말 목록. hot_word=빨갛게 칠할 낱말 번호. cand=empty(회색 점선)/miss(빨간 점선과 물음표)."""
    box(ax, 0.4, 0.9, 4.8, 5.55, fc="white")
    label(ax, 0.65, 6.17, "보낸 메시지", fs=10, ha="left", color=INK)
    for k, m in enumerate(MSGS):
        s = " ".join(m)
        w = 0.21 * len(s.replace(" ", "")) + 0.1 * (len(m) - 1) + 0.35
        y = 5.62 - k * 0.4
        on = k in hot_msgs
        ax.add_patch(Rectangle((5.0 - w, y), w, 0.33, fc=PINK if on else NOTE, ec=RED if on else GREY, lw=1.6 if on else 1.0))
        label(ax, 5.0 - w / 2, y + 0.165, s, fs=9, color=RED if on else "#222", bold=on)
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


# ── 1. 여는 장면 ──────────────────────────────────────────────────
def opening(ax, step):
    program(ax, ["횟수표", "앞 낱말 → 다음 낱말"])
    if step == 1:
        phone(ax, hot_msgs=(5, 6))
        bubble(ax, *SAY, "새로 보낸 메시지 둘도\n횟수표에 셌어요", TAIL)
    else:
        phone(ax, TYPED, hot_word=3, cand="miss")
        bubble(ax, *SAY, "\"먹었니\" 다음에 올\n낱말을 못 띄워요", TAIL, hot=True)
        moral(ax, 6.0, 0.35, "\"먹었니\"까지 치자 후보 칸이 비었어요")


# ── 2. 사전 = 횟수표의 줄 머리 ─────────────────────────────────────
def tally_rows():
    rows = {"(처음)": []}
    for m in MSGS:
        seq = ["(처음)"] + m + ["(끝)"]
        for a, b in zip(seq, seq[1:]):
            rows.setdefault(a, [])
            if b in dict(rows[a]):
                rows[a] = [(x, n + 1 if x == b else n) for x, n in rows[a]]
            else:
                rows[a].append((b, 1))
    return [("(처음)", rows["(처음)"])] + [(w, rows[w]) for w in WORDS]


TALLY = tally_rows()


def dictionary(ax, step):
    label(ax, 0.3, 6.3, "횟수표 (앞 낱말 → 다음 낱말 횟수)", fs=11, ha="left", bold=True)
    for k, (head, nxt) in enumerate(TALLY):
        y = 5.75 - k * 0.33
        is_word = head != "(처음)"
        cell(ax, 0.3, y + 0.02, 1.05, 0.25, head, hot=step == 2 and is_word, dim=not is_word, fs=8.5)
        s = "  ".join(f"{w} {n}" for w, n in nxt)
        label(ax, 1.5, y + 0.145, "→  " + s, fs=9, ha="left", color=INK)
    on = step == 2
    label(ax, 7.1, 6.3, "낱말 사전 (15개)" if step >= 2 else "낱말 사전", fs=11, ha="left", bold=True,
          color=RED if on else "#222")
    for k, w in enumerate(WORDS):
        x, y = 7.1 + (k % 3) * 1.55, 5.45 - (k // 3) * 0.5
        if step == 1:
            empty(ax, x, y, 1.45, 0.4)
        else:
            cell(ax, x, y, 1.45, 0.4, w, hot=on, fs=10)
    if step == 2:
        arrow(ax, (2.9, 0.55), (6.95, 3.3), color=RED, ms=14, rad=0.3)
        label(ax, 9.4, 2.85, "줄 맨 앞 낱말을 모았어요", fs=10.5, color=RED, bold=True)
    if step == 3:
        label(ax, 7.1, 2.65, "\"먹었니\" 줄을 찾아요", fs=10.5, ha="left", color=INK)
        cell(ax, 7.1, 1.85, 1.45, 0.45, "먹었니", hot=True, fs=10.5)
        label(ax, 8.75, 2.07, "→  ?", fs=12, ha="left", color=RED, bold=True)
        label(ax, 9.6, 2.07, "사전에 없어요", fs=10, ha="left", color=RED)
        moral(ax, 6.0, 0.3, "사전에 없는 낱말은 횟수표에 줄이 없어요")


# ── 3. 1편의 막힘과 나란히 ─────────────────────────────────────────
def stuck(ax, step):
    ax.plot([6.0, 6.0], [0.9, 6.3], color=GREY, lw=1.0)
    on1, on2 = step == 1, step == 2
    c1 = RED if on1 else "#222"
    label(ax, 0.3, 6.1, "1편: \"내일 저녁\"에서 막혔어요", fs=11.5, ha="left", bold=True, color=c1)
    label(ax, 0.3, 5.2, "낱말 사전에", fs=10, ha="left", color=INK)
    cell(ax, 2.0, 4.95, 1.0, 0.5, "내일", fs=11)
    label(ax, 3.3, 5.2, "✓", fs=12, color=INK)
    cell(ax, 3.7, 4.95, 1.0, 0.5, "저녁", fs=11)
    label(ax, 5.0, 5.2, "✓", fs=12, color=INK)
    label(ax, 0.3, 3.8, "앞 낱말 2개 표에", fs=10, ha="left", color=INK)
    cell(ax, 2.6, 3.55, 2.0, 0.5, "내일 저녁", hot=on1, fs=11)
    label(ax, 4.8, 3.8, "→ ?", fs=12, ha="left", color=c1, bold=on1)
    label(ax, 3.0, 2.6, "줄이 없어요", fs=10.5, color=c1)
    label(ax, 3.0, 1.6, "처음 보는 묶음", fs=12, color=c1, bold=True)
    label(ax, 6.3, 6.1, "이번: \"먹었니\"에서 막혔어요", fs=11.5, ha="left", bold=True,
          color=RED if on2 else GREY)
    if step == 1:
        empty(ax, 6.3, 3.2, 5.4, 2.3)
        return
    label(ax, 6.3, 5.2, "낱말 사전에", fs=10, ha="left", color=INK)
    cell(ax, 8.0, 4.95, 1.2, 0.5, "먹었니", hot=on2, fs=11)
    label(ax, 9.5, 5.2, "✗", fs=13, color=RED, bold=True)
    label(ax, 9.0, 3.8, "낱말 자체가 없어요", fs=10.5, color=RED)
    label(ax, 9.0, 1.6, "처음 보는 낱말", fs=12, color=RED, bold=True)
    moral(ax, 6.0, 0.45, "1편은 처음 보는 묶음, 이번엔 처음 보는 낱말에서 막혔어요")


# ── 4. "먹" 나뭇가지 ───────────────────────────────────────────────
L1 = [("지", 5.7, 1), ("자", 5.15, 1), ("을까", 4.6, 1), ("어요", 4.05, 3), ("는다", 3.5, 3)]
L2 = [("어", 2.85, 2), ("지", 2.3, 2), ("니", 1.75, 3), ("대", 1.2, 3)]
EAT = (3.0, 2.35)  # "었" 칸


def branch(ax, step):
    label(ax, 0.3, 6.3, "\"먹\"으로 시작하는 낱말", fs=11.5, ha="left", bold=True)
    rx, ry = 1.4, 3.5
    cell(ax, 0.6, ry - 0.28, 0.8, 0.56, "먹", fs=14)

    def leaf(x, y, s, word, when, parent):
        if when > step:
            return
        on = when == step and step > 1
        late = when == 3
        ax.plot([parent[0], x], [parent[1], y], color=RED if on else INK, lw=1.4, ls="--" if late else "-")
        if late:
            empty(ax, x, y - 0.22, 0.85, 0.44, s, color=RED if on else GREY)
        else:
            cell(ax, x, y - 0.22, 0.85, 0.44, s, hot=on, fs=11)
        label(ax, x + 1.0, y, word, fs=10.5, ha="left", color=RED if on else "#222", bold=on)

    for s, y, when in L1:
        leaf(EAT[0], y, s, "먹" + s, when, (rx, ry))
    if step >= 2:
        on = step == 2
        ax.plot([rx, EAT[0]], [ry, EAT[1]], color=RED if on else INK, lw=1.4)
        cell(ax, EAT[0], EAT[1] - 0.22, 0.85, 0.44, "었", hot=on, fs=11)
        for s, y, when in L2:
            leaf(4.6, y, s, "먹었" + s, when, (EAT[0] + 0.85, EAT[1]))
    if step == 1:
        label(ax, 9.6, 4.6, "보낸 메시지 다섯 개에서\n끝이 셋으로 갈렸어요", fs=10.5, color=INK)
    if step == 2:
        label(ax, 9.6, 3.3, "메시지 두 개를 더 보내자\n새 낱말이 둘 생겼어요", fs=10.5, color=RED)
    if step == 3:
        label(ax, 9.6, 3.3, "끝은 얼마든지\n더 붙어요 …", fs=10.5, color=RED)
        label(ax, 9.6, 2.2, "점선 = 아직 사전에 없는 낱말", fs=9.5, color=INK)
        moral(ax, 6.0, 0.45, "끝이 바뀔 때마다 사전에 없는 낱말이 생겨요")


# ── 5. 메시지를 더할 때 낱말 사전과 글자 사전 ──────────────────────
def grow(ax, step):
    n_msg = {1: 5, 2: 6, 3: 7, 4: 7}[step]
    on = step in (2, 3)
    before = MSGS[:n_msg - 1] if on else MSGS[:n_msg]
    old_w = set(w for m in before for w in m)
    old_c = set("".join(w for m in before for w in m))
    words = [w for w in WORDS if any(w in m for m in MSGS[:n_msg])]
    chars = [c for c in CHARS if any(c in "".join(m) for m in MSGS[:n_msg])]
    if step == 1:
        label(ax, 0.3, 6.25, "보낸 메시지 1 ~ 5번으로 만든 사전", fs=11.5, ha="left", bold=True)
    elif on:
        label(ax, 0.3, 6.25, f"{n_msg}번 메시지를 더해요", fs=11.5, ha="left", bold=True)
        x = 3.6
        for w in MSGS[n_msg - 1]:
            cell(ax, x, 5.95, 0.32 * len(w) + 0.25, 0.48, w, fs=11)
            x += 0.32 * len(w) + 0.33
    else:
        label(ax, 0.3, 6.25, "보낸 메시지 1 ~ 7번으로 만든 사전", fs=11.5, ha="left", bold=True)
    label(ax, 0.3, 4.95, "낱말 사전", fs=11, ha="left", bold=True)
    x = 1.7
    for w in words:
        cw = 0.27 * len(w) + 0.1
        cell(ax, x, 4.7, cw, 0.5, w, hot=on and w not in old_w, fs=9)
        x += cw
    new_w = [w for w in words if w not in old_w]
    label(ax, 1.7, 4.4, f"{len(words)}개" + (f"   새 낱말 {len(new_w)}개: " + ", ".join(new_w) if on else ""),
          fs=10, ha="left", color=RED if on else INK, bold=on)
    label(ax, 0.3, 3.35, "글자 사전", fs=11, ha="left", bold=True)
    for k, c in enumerate(chars):
        cell(ax, 1.7 + k * 0.405, 3.1, 0.38, 0.5, c, hot=on and c not in old_c, fs=9.5)
    new_c = [c for c in chars if c not in old_c]
    if on:
        s = f"{len(chars)}개   새 글자 {len(new_c)}개" + (": " + ", ".join(new_c) if new_c else "")
        label(ax, 1.7, 2.8, s, fs=10, ha="left", color=RED, bold=True)
        if not new_c:
            label(ax, 1.7, 2.35, "점, 심, 먹, 었, 지는 모두 이미 있어요", fs=10, ha="left", color=RED)
    else:
        label(ax, 1.7, 2.8, f"{len(chars)}개", fs=10, ha="left", color=INK)
    if step == 4:
        label(ax, 0.3, 1.55, "\"먹었니\"를 글자로", fs=10.5, ha="left", color=RED, bold=True)
        for k, ch in enumerate("먹었니"):
            x = 3.2 + k * 1.3
            cell(ax, x, 1.3, 0.6, 0.5, ch, hot=True, fs=12)
            ok = ch in CHARS
            label(ax, x + 0.75, 1.55, "✓" if ok else "✗ 없어요", fs=10.5, ha="left", color=INK if ok else RED, bold=not ok)
        moral(ax, 6.0, 0.45, "새 글자는 조금만 생겨서 새 낱말도 거의 아는 글자로 잘려요", fs=12)


# ── 6. 글자로 자르면 길어져요 (한 컷) ──────────────────────────────
def longer(ax, step):
    label(ax, 0.3, 6.25, "\"오늘 점심 뭐 먹지\"에서 \"뭐\" 다음을 맞힐 때", fs=11.5, ha="left", bold=True)
    label(ax, 0.3, 4.55, "낱말로 자르면", fs=11, ha="left")
    xs = [2.6 + k * 1.2 for k in range(4)]
    for k, wd in enumerate(["오늘", "점심", "뭐", "먹지"]):
        if k == 3:
            empty(ax, xs[k], 4.3, 1.1, 0.55)
            label(ax, xs[k] + 0.55, 4.0, "다음", fs=9.5, color=INK)
        else:
            cell(ax, xs[k], 4.3, 1.1, 0.55, wd, fs=11.5)
    hbrace(ax, xs[1], xs[2] + 1.1, 4.95, "앞 2조각: 점심 · 뭐")
    label(ax, 8.0, 4.57, "4조각", fs=11, ha="left", color=INK)
    label(ax, 0.3, 2.35, "글자로 자르면", fs=11, ha="left", color=RED, bold=True)
    for k, ch in enumerate("오늘점심뭐먹지"):
        x = 2.6 + k * 0.62
        if k >= 5:
            empty(ax, x, 2.1, 0.55, 0.55)
            if k == 5:
                label(ax, x + 0.27, 1.8, "다음", fs=9.5, color=RED)
        else:
            cell(ax, x, 2.1, 0.55, 0.55, ch, hot=k in (2, 3, 4), fs=11.5)
    hbrace(ax, 2.6 + 2 * 0.62, 2.6 + 4 * 0.62 + 0.55, 2.75, "앞 3조각: 점 · 심 · 뭐", color=RED)
    label(ax, 8.0, 2.37, "7조각", fs=11, ha="left", color=RED, bold=True)
    moral(ax, 6.0, 0.8, "글자로 자르면 같은 뜻을 보려고 앞을 더 많이 봐야 해요")


# ── 6-2. 앞을 많이 보면 처음 보는 묶음 ─────────────────────────────
def unseen(ax, step):
    label(ax, 0.3, 6.3, "\"내일 저녁\" 다음을 맞히려고 앞을 볼 때", fs=11.5, ha="left", bold=True)
    label(ax, 0.3, 5.05, "1편: 앞 낱말 2개", fs=10.5, ha="left", color=INK)
    cell(ax, 3.3, 4.8, 1.0, 0.5, "내일", fs=11)
    cell(ax, 4.35, 4.8, 1.0, 0.5, "저녁", fs=11)
    label(ax, 5.6, 5.05, "→ 표에 없는 묶음", fs=10.5, ha="left", color=INK)
    on = step == 2
    label(ax, 0.3, 3.35, "글자로: 앞 글자 3개", fs=10.5, ha="left", color=RED if on else GREY, bold=on)
    for k, ch in enumerate("일저녁"):
        if on:
            cell(ax, 3.3 + k * 0.55, 3.1, 0.5, 0.5, ch, hot=True, fs=11)
        else:
            empty(ax, 3.3 + k * 0.55, 3.1, 0.5, 0.5)
    if not on:
        return
    label(ax, 5.2, 3.35, "→ 메시지에 이렇게 이어진 곳이 없어요", fs=10.5, ha="left", color=RED, bold=True)
    label(ax, 0.3, 2.2, "메시지에 있는 묶음", fs=10, ha="left", color=INK)
    for k, ch in enumerate("늘저녁"):
        cell(ax, 3.3 + k * 0.55, 1.95, 0.5, 0.5, ch, fs=11)
    label(ax, 5.2, 2.2, "4번 \"오늘 저녁 뭐 먹을까\"", fs=10, ha="left", color=INK)
    moral(ax, 6.0, 0.8, "글자로 자르면 네 조각을 다 보기도 전에 처음 보는 묶음이 나와요", fs=11.5)


# ── 7. 0과 1 칸으로 담는 가짓수 ─────────────────────────────────────
def patterns(n):
    return [format(i, f"0{n}b") for i in range(2 ** n)]


def bitrows(ax, step):
    label(ax, 0.3, 6.3, "0과 1만 적는 칸으로 적을 수 있는 가짓수", fs=11.5, ha="left", bold=True)
    for n, y in ((1, 5.4), (2, 4.4), (3, 3.4)):
        show = step >= (1 if n == 1 else 2)
        on = (n == 1 and step == 1) or (n > 1 and step == 2)
        label(ax, 0.3, y + 0.25, f"칸 {n}개\n{2 ** n}가지" if show else f"칸 {n}개", fs=10.5, ha="left",
              color=RED if on else ("#222" if show else GREY), bold=on)
        if not show:
            empty(ax, 1.6, y - 0.08, 9.6, 0.62)
            continue
        x = 1.6
        for p in patterns(n):
            bits(ax, x, y - 0.08, p, w=0.36, h=0.62, hot=range(n) if on else (), fs=9)
            x += n * 0.36 + 0.13
    if step == 3:
        label(ax, 0.3, 2.45, "칸 4개 16가지 · 5개 32가지 · 6개 64가지 · 7개 128가지", fs=10.5, ha="left", color=RED)
        label(ax, 0.3, 1.55, "칸 8개\n256가지", fs=10.5, ha="left", color=RED, bold=True)
        bits(ax, 1.6, 1.24, "11101011", w=0.42, h=0.62, hot=range(8), fs=10.5)
        label(ax, 5.1, 1.55, "= 235      0 ~ 255 가운데 하나", fs=11, ha="left", color=RED)
        moral(ax, 6.0, 0.35, "칸이 하나 늘 때마다 가짓수가 두 배가 돼요")


# ── 8. "니"를 바이트로 ─────────────────────────────────────────────
BDICT = ["0", "1", "2", "…", "136", "…", "139", "…", "235", "…", "255"]


def byte(ax, step):
    label(ax, 0.4, 6.3, "글자", fs=11, ha="left", bold=True)
    cell(ax, 0.4, 5.0, 0.8, 0.8, "니", hot=step == 1, fs=14)
    if step >= 2:
        on = step == 2
        arrow(ax, (1.35, 5.4), (2.0, 5.4), color=RED if on else GREY, ms=12)
        label(ax, 2.1, 6.3, "글자 번호", fs=11, ha="left", bold=True, color=RED if on else "#222")
        cell(ax, 2.1, 5.0, 1.6, 0.8, "45768", hot=on, fs=13)
    if step >= 3:
        on = step == 3
        arrow(ax, (3.85, 5.4), (4.5, 5.4), color=RED if on else GREY, ms=12)
        label(ax, 4.6, 6.3, "바이트 3개", fs=11, ha="left", bold=True, color=RED if on else "#222")
        for k, b in enumerate(NI):
            cell(ax, 4.6 + k * 0.9, 5.0, 0.8, 0.8, b, hot=on, fs=13)
        label(ax, 7.5, 5.62, "한 칸에 0 ~ 255만 들어가서", fs=10, ha="left", color=RED if on else INK)
        label(ax, 7.5, 5.18, "UTF-8 약속대로 셋에 나눠 담아요", fs=10, ha="left", color=RED if on else INK)
    label(ax, 0.4, 3.75, "글자 사전 (24개)", fs=10.5, ha="left", bold=True)
    for k, c in enumerate(CHARS):
        cell(ax, 2.6 + k * 0.38, 3.5, 0.36, 0.48, c, fs=9)
    if step == 1:
        label(ax, 0.8, 4.6, "글자 사전에 없어요", fs=10, color=RED, bold=True)
    if step < 4:
        return
    label(ax, 0.4, 1.85, "바이트 사전 (256개)", fs=10.5, ha="left", bold=True, color=RED)
    for k, s in enumerate(BDICT):
        cell(ax, 3.0 + k * 0.78, 1.6, 0.72, 0.5, s, hot=s in ("136", "139", "235"), fs=9.5)
    moral(ax, 6.0, 0.6, "바이트 256개를 사전에 넣어 두면 어떤 글자든 잘려요")


# ── 9. 합치기: 오+늘 → 점+심 → 먹+었 → 날+씨 ───────────────────────
PAIRS = [("오 + 늘", "3번"), ("점 + 심", "3번"), ("먹 + 었", "2번"), ("날 + 씨", "2번"), ("나머지 짝", "1번씩")]
CW = 0.4


def merge(ax, step):
    done = RULES[:step - 1]
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
                    on = len(p) == 2 and (p[0], p[1]) == RULES[step - 2]
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
            on = k == step - 2
            cell(ax, 6.5, y, 2.9, 0.45, f"{'①②③④'[k]} {a} + {b} → {a}{b}", hot=on, fs=10.5)
            label(ax, 9.6, y + 0.22, f"{SLOTS[k] - SLOTS[k + 1]}칸 줄어 {SLOTS[k + 1]}칸", fs=10.5, ha="left",
                  color=RED if on else INK, bold=on)
        else:
            empty(ax, 6.5, y, 2.9, 0.45)
    if step == 1:
        label(ax, 0.3, 1.4, "\"오\" 다음 \"늘\"이 1번 · 2번 · 4번 메시지에서 3번", fs=10, ha="left", color=RED)
        label(ax, 0.3, 0.95, "띄어 쓴 두 글자는 짝으로 세지 않아요", fs=10, ha="left", color=INK)
    if step == 5:
        moral(ax, 6.0, 0.35, "많이 나온 짝부터 합치면 칸이 가장 많이 줄어요")


# ── 10. 새 낱말은 합친 순서대로 ────────────────────────────────────
def cutnew(ax, step):
    label(ax, 0.3, 6.3, "처음 보는 낱말 \"먹었니\"", fs=11.5, ha="left", bold=True)
    label(ax, 7.3, 6.3, "합친 순서", fs=11, ha="left", bold=True)
    for k, (a, b) in enumerate(RULES):
        y = 5.55 - k * 0.6
        cell(ax, 7.3, y, 2.4, 0.45, f"{'①②③④'[k]} {a} + {b} → {a}{b}", hot=step == 2 and k == 2, fs=10.5)
        if step == 1 or (step == 2 and k > 2) or (step == 3 and k < 3):
            continue
        ok = k == 2
        on = (step == 2 and k <= 2) or (step == 3 and k == 3)
        label(ax, 9.9, y + 0.22, "있어요 → 합쳐요" if ok else "없어요", fs=10, ha="left",
              color=RED if on else INK, bold=on and ok)
    first = step == 1
    label(ax, 0.3, 4.3, "글자로 자르면", fs=10.5, ha="left", color=RED if first else INK, bold=first)
    for k, ch in enumerate("먹었니"):
        cell(ax, 2.8 + k * 0.75, 4.05, 0.7, 0.55, ch, hot=first, fs=12)
    if first:
        return
    label(ax, 0.3, 3.0, "③을 적용하면", fs=10.5, ha="left", color=RED if step == 2 else INK, bold=step == 2)
    cell(ax, 2.8, 2.75, 1.45, 0.55, "먹었", hot=step == 2, fs=12)
    cell(ax, 4.3, 2.75, 0.7, 0.55, "니", fs=12)
    if step == 3:
        label(ax, 0.3, 1.7, "\"니\"는 바이트로", fs=10.5, ha="left", color=RED, bold=True)
        cell(ax, 2.8, 1.45, 1.45, 0.55, "먹었", fs=12)
        for k, b in enumerate(NI):
            cell(ax, 4.3 + k * 0.75, 1.45, 0.7, 0.55, b, hot=True, fs=11)
        moral(ax, 6.0, 0.45, "합친 순서대로 따라가면 처음 보는 낱말도 잘려요")


# ── 11. 몇 번 합칠까: 사전 크기와 칸 수 ─────────────────────────────
def size(ax, step):
    label(ax, 0.3, 6.3, "합치기", fs=11, ha="left", bold=True)
    label(ax, 1.4, 6.3, "사전 (글자 + 합친 조각)", fs=11, ha="left", bold=True)
    label(ax, 7.0, 6.3, "메시지 7개의 칸", fs=11, ha="left", bold=True)
    shown = {1: 1, 2: 3, 3: 5}[step]
    hot_rows = {1: (), 2: (1, 2), 3: (3, 4)}[step]
    for k in range(5):
        y = 5.35 - k * 1.05
        on = k in hot_rows
        label(ax, 0.3, y + 0.2, f"{k}번", fs=11, ha="left", color=RED if on else ("#222" if k < shown else GREY), bold=on)
        if k >= shown:
            continue
        n = 24 + k
        for i in range(n):
            last = on and i == n - 1
            face = PINK if last else (LIGHT if i >= 24 else NOTE)
            ax.add_patch(Rectangle((1.4 + i * 0.18, y), 0.16, 0.4, fc=face, ec=RED if last else INK, lw=0.7))
        label(ax, 1.4, y - 0.25, f"{n}개" + ("" if k == 0 else f"  (+ {RULES[k - 1][0]}{RULES[k - 1][1]})"),
              fs=9.5, ha="left", color=RED if on else INK, bold=on)
        s = SLOTS[k]
        for i in range(s):
            ax.add_patch(Rectangle((7.0 + i * 0.1, y), 0.085, 0.4, fc=PINK if on else NOTE, ec=RED if on else INK, lw=0.5))
        label(ax, 7.0, y - 0.25, f"{s}칸", fs=9.5, ha="left", color=RED if on else INK, bold=on)
    if step == 3:
        moral(ax, 6.0, 0.3, "합칠수록 사전은 커지고 문장은 짧아져요")


# ── 12. 사전이 크면 횟수표도 커요 ───────────────────────────────────
TOKS = CHARS + ["오늘", "점심", "먹었", "날씨"]


def rows(ax, step):
    n = 24 if step == 1 else 28
    label(ax, 0.3, 6.3, f"토큰 사전 ({n}개)", fs=11, ha="left", bold=True, color=RED if step == 2 else "#222")
    for k in range(n):
        x, y = 0.3 + (k % 7) * 0.68, 5.3 - (k // 7) * 0.58
        cell(ax, x, y, 0.62, 0.46, TOKS[k], hot=step == 2 and k >= 24, fs=9.5)
    label(ax, 6.0, 6.3, f"횟수표 줄 ({n}줄)", fs=11, ha="left", bold=True, color=RED if step == 2 else "#222")
    arrow(ax, (5.15, 4.3), (5.85, 4.3), color=RED if step == 2 else INK, ms=12)
    for k in range(n):
        col, r = divmod(k, 14)
        x, y = 6.0 + col * 2.9, 5.75 - r * 0.36
        on = step == 2 and k >= 24
        cell(ax, x, y + 0.02, 0.75, 0.26, TOKS[k], hot=on, fs=8.5)
        label(ax, x + 0.85, y + 0.15, "→ …", fs=9, ha="left", color=RED if on else INK)
    if step == 1:
        label(ax, 2.6, 2.6, "사전 조각마다\n횟수표에 줄이 하나씩", fs=10.5, color=INK)
    if step == 2:
        label(ax, 2.6, 2.6, "합친 조각 4개가 들어오자\n줄도 4줄 늘었어요", fs=10.5, color=RED)
        moral(ax, 6.0, 0.35, "사전이 하나 늘면 횟수표 줄도 하나 늘어요")


# ── 13. 전환: 남는 것 ──────────────────────────────────────────────
def turn(ax, step):
    program(ax, ["토큰 사전", "글자 24 · 합친 조각 4", "바이트 256"])
    phone(ax, TYPED)
    if step == 1:
        bubble(ax, *SAY, "\"먹었니\"를 먹었 · 니(바이트 3개)로\n잘랐어요", TAIL, fs=10.5)
        return
    bubble(ax, 6.3, 0.2, 5.6, 2.45, "", TAIL, hot=True)
    label(ax, 9.1, 2.2, "그래도 남는 것이 있어요", fs=11.5, color=RED, bold=True)
    for k, t in enumerate(["① 사전을 만든 글이 잘린 조각 수를 정해요", "② 자주 나오는지만 보고 뜻은 안 봐요"]):
        label(ax, 6.5, 1.55 - k * 0.6, t, fs=10.5, ha="left", color=RED)


# ── 14. 첫째: 사전을 만든 글 ───────────────────────────────────────
def lang(ax, step):
    on1, on2, on3 = step == 1, step == 2, step == 3
    box(ax, 0.3, 3.75, 5.5, 2.25, fc=PINK if on1 else "white", ec=RED if on1 else INK, lw=1.4)
    label(ax, 0.55, 5.65, "한국어 메시지 7개로 만든 사전", fs=10.5, ha="left", bold=True, color=RED if on1 else "#222")
    label(ax, 0.55, 5.1, "한글 글자 24개", fs=10, ha="left", color=INK)
    label(ax, 0.55, 4.6, "합친 조각", fs=10, ha="left", color=INK)
    for k, t in enumerate(["오늘", "점심", "먹었", "날씨"]):
        cell(ax, 1.8 + k * 0.9, 4.35, 0.82, 0.48, t, hot=on1, fs=10)
    label(ax, 0.55, 4.05, "바이트 256개", fs=10, ha="left", color=INK)
    if step == 1:
        empty(ax, 6.2, 3.75, 5.5, 2.25)
    else:
        box(ax, 6.2, 3.75, 5.5, 2.25, fc=PINK if on2 else "white", ec=RED if on2 else INK, lw=1.4)
        label(ax, 6.45, 5.65, "영어 메시지만으로 만든 사전", fs=10.5, ha="left", bold=True, color=RED if on2 else "#222")
        label(ax, 6.45, 5.1, "영어 글자 a ~ z", fs=10, ha="left", color=INK)
        label(ax, 6.45, 4.6, "합친 조각: 영어 짝만", fs=10, ha="left", color=INK)
        label(ax, 6.45, 4.05, "바이트 256개", fs=10, ha="left", color=INK)
        label(ax, 9.3, 5.1, "한글 글자 0개", fs=10.5, ha="left", color=RED if on2 else INK, bold=on2)
    label(ax, 0.3, 3.15, "\"오늘 점심 뭐 먹지\"를 자르면", fs=10.5, ha="left", bold=True)
    label(ax, 0.3, 2.35, "한국어 사전", fs=10, ha="left", color=RED if on3 else GREY)
    label(ax, 0.3, 1.25, "영어 사전", fs=10, ha="left", color=RED if on3 else GREY)
    if not on3:
        empty(ax, 2.2, 2.1, 6.0, 0.5)
        empty(ax, 2.2, 1.0, 8.4, 0.5)
        return
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


# ── 15. 둘째: 뜻은 안 봐요 ─────────────────────────────────────────
MEAN = [("점심", 3, ["점심"]), ("저녁", 1, ["저", "녁"]), ("내일", 1, ["내", "일"])]


def mean(ax, step):
    label(ax, 0.3, 6.3, "낱말", fs=11, ha="left", bold=True)
    label(ax, 2.0, 6.3, "메시지에 나온 횟수", fs=11, ha="left", bold=True)
    label(ax, 5.2, 6.3, "합친 순서대로 자르면", fs=11, ha="left", bold=True)
    for k, (w, n, ps) in enumerate(MEAN):
        y = 5.2 - k * 1.1
        on = (step == 1 and k == 0) or (step == 2 and k > 0)
        cell(ax, 0.3, y, 1.2, 0.55, w, fs=11.5)
        label(ax, 2.6, y + 0.27, f"{n}번", fs=11, ha="left", color=RED if on else "#222", bold=on)
        if step == 1 and k > 0:
            empty(ax, 5.2, y, 1.6, 0.55)
            continue
        x = 5.2
        for p in ps:
            cell(ax, x, y, 0.55 * len(p) + 0.25, 0.55, p, hot=on, fs=11.5)
            x += 0.55 * len(p) + 0.3
        label(ax, 7.4, y + 0.27, "한 토큰" if len(ps) == 1 else "두 토큰으로 갈려요", fs=10.5, ha="left",
              color=RED if on else INK)
    if step == 2:
        ax.plot([0.15, 0.15], [2.95, 5.75], color=RED, lw=1.5)
        label(ax, 0.3, 2.45, "사람에게는 셋 다 한 덩어리 뜻인 낱말", fs=10.5, ha="left", color=RED)
        moral(ax, 6.0, 1.2, "합치기는 몇 번 나왔는지만 보고 뜻은 안 봐요")


# ── 16. 형태소 분석기 ──────────────────────────────────────────────
BPE_CUT = [["내", "일"], ["저", "녁"], ["뭐"], ["먹었", 235, 139, 136]]
MORPH = [["내일"], ["저녁"], ["뭐"], ["먹", "었", "니"]]
MEANING = {"먹": "먹다", "었": "지난 일", "니": "묻는 말"}


def morph(ax, step):
    label(ax, 0.3, 6.3, "\"내일 저녁 뭐 먹었니\"를 자르면", fs=11.5, ha="left", bold=True)

    def row(y, groups, hot, dim, notes=False):
        x = 3.1
        for g in groups:
            for p in g:
                s = str(p)
                w = 0.36 * len(s) + 0.28 if isinstance(p, str) else 0.62
                if notes and s in MEANING:
                    w = 1.0
                if dim:
                    empty(ax, x, y, w, 0.55)
                else:
                    cell(ax, x, y, w, 0.55, s, hot=hot, fs=11 if isinstance(p, str) else 9.5)
                if notes and s in MEANING:
                    label(ax, x + w / 2, y - 0.35, MEANING[s], fs=9.5, color=RED)
                x += w + 0.05
            x += 0.3

    label(ax, 0.3, 4.9, "합친 순서대로", fs=10.5, ha="left")
    row(4.65, BPE_CUT, False, False)
    label(ax, 3.1, 4.3, "숫자 칸 = \"니\"의 바이트", fs=9, ha="left", color=INK)
    on = step == 2
    label(ax, 0.3, 3.0, "형태소 분석기로", fs=10.5, ha="left", color=RED if on else GREY, bold=on)
    row(2.75, MORPH, on, not on, notes=on)
    if on:
        moral(ax, 6.0, 0.9, "형태소 분석기는 뜻을 가진 조각으로 잘라요")


# ── 17. 검색에서는 뜻 단위가 나아요 ──────────────────────────────────
def search(ax, step):
    label(ax, 0.3, 6.3, "검색 엔진에 들어온 글", fs=11, ha="left", bold=True)
    box(ax, 0.4, 5.3, 2.7, 0.6, fc="white")
    label(ax, 1.75, 5.6, "도서관 가자", fs=11.5)
    label(ax, 0.3, 4.55, "글자로 잘라 둔 조각", fs=10, ha="left", color=RED if step == 1 else "#222", bold=step == 1)
    xs = {}
    x = 0.4
    for g in ["도서관", "가자"]:
        for ch in g:
            hit = step == 2 and ch == "서"
            cell(ax, x, 3.7, 0.5, 0.5, ch, hot=step == 1 or hit, fs=11)
            xs[ch] = x
            x += 0.52
        x += 0.25
    label(ax, 6.6, 6.3, "검색창", fs=11, ha="left", bold=True)
    box(ax, 6.6, 5.3, 4.9, 0.6, fc="white")
    if step >= 2:
        magnifier(ax, 6.95, 5.6)
        label(ax, 7.3, 5.6, "서울", fs=11.5, ha="left")
        label(ax, 6.6, 4.55, "찾는 말도 글자로", fs=10, ha="left", color=RED if step == 2 else "#222", bold=step == 2)
        cell(ax, 6.7, 3.7, 0.5, 0.5, "서", hot=step == 2, fs=11)
        cell(ax, 7.22, 3.7, 0.5, 0.5, "울", fs=11)
        if step == 2:
            arrow(ax, (6.95, 3.65), (xs["서"] + 0.25, 3.65), color=RED, ms=12, rad=-0.25)
            label(ax, 9.6, 3.95, "\"도서관 가자\"가 걸려요", fs=10.5, color=RED, bold=True)
    label(ax, 0.3, 2.8, "뜻 단위로 잘라 둔 조각", fs=10, ha="left", color=RED if step == 3 else GREY, bold=step == 3)
    if step < 3:
        empty(ax, 0.4, 1.95, 3.6, 0.5)
        empty(ax, 6.7, 1.95, 1.0, 0.5)
        return
    x = 0.4
    for t in ["도서관", "가", "자"]:
        w = 0.42 * len(t) + 0.2
        cell(ax, x, 1.95, w, 0.5, t, hot=True, fs=11)
        x += w + 0.06
    label(ax, 6.6, 2.8, "찾는 말도 뜻 단위로", fs=10, ha="left", color=RED, bold=True)
    cell(ax, 6.7, 1.95, 1.0, 0.5, "서울", hot=True, fs=11)
    label(ax, 10.4, 1.95, "같은 조각이 없어서\n안 걸려요", fs=10.5, color=RED)
    moral(ax, 6.0, 0.7, "뜻 단위로 잘라 두면 엉뚱한 글이 덜 걸려요")


# ── 18. 어떤 자르기를 언제: 갈림길 ──────────────────────────────────
def decide():
    fig, ax = canvas(9.4, 3.6, 14, 5.4)
    box(ax, 0.3, 3.3, 5.0, 1.5, fc=NOTE)
    label(ax, 2.8, 4.05, "기계가 다음 조각을\n맞혀야 하나요?", fs=11.5, bold=True)
    arrow(ax, (5.4, 4.05), (6.9, 4.05), color=RED)
    box(ax, 7.0, 3.1, 6.7, 1.9, fc=PINK, ec=RED)
    label(ax, 10.35, 4.05, "예, 합치기(BPE)로 잘라요\n사전에 없는 글자는 바이트로\n(언어 모델)", fs=10.5, color=RED)
    arrow(ax, (2.8, 3.2), (2.8, 2.0))
    box(ax, 0.3, 0.5, 5.0, 1.4, fc=LIGHT, ec=GREY)
    label(ax, 2.8, 1.2, "아니요, 사람이\n뜻으로 찾아요", fs=10.5)
    arrow(ax, (5.4, 1.2), (6.9, 1.2))
    box(ax, 7.0, 0.5, 6.7, 1.4, fc=LIGHT, ec=GREY)
    label(ax, 10.35, 1.2, "뜻으로 잘라요\n형태소 분석기 (검색 엔진)", fs=10.5)
    save(fig, OUT, "ai02-decide.svg")


# ── 19. 정리: 처음 장면으로 돌아가기 ───────────────────────────────
def back(ax, step):
    if step == 1:
        phone(ax, TYPED, cand="miss")
        program(ax, ["낱말 사전 15개"])
        bubble(ax, *SAY, "처음엔 \"먹었니\"가 사전에\n없어서 막혔어요", TAIL)
    elif step == 2:
        phone(ax, TYPED)
        program(ax, ["토큰 사전", "글자 24 · 합친 조각 4", "바이트 256"], hot=True)
        bubble(ax, *SAY, "토큰 사전으로 바꿨어요", TAIL, hot=True)
    else:
        phone(ax, TYPED, hot_word=3)
        program(ax, ["먹었니 → 먹었 · 니", "니 → 235 · 139 · 136"])
        bubble(ax, *SAY, "합친 순서대로 자르고\n없는 글자는 바이트로 잘라요", TAIL, hot=True, fs=10.5)
        moral(ax, 6.0, 0.35, "처음 보는 낱말도 사전에 있는 토큰으로 잘랐어요")


# ── 20. 정리: 낱말 카드 ────────────────────────────────────────────
def cards():
    """이 편 본문에서 이름 붙인 말 셋. 카드마다 본문 그림을 작게 다시 그리고 한 줄 뜻."""
    fig, ax = canvas(6.4, 6.3, 9.8, 9.6)
    W, H = 9.4, 2.9

    def card(i, name, line):
        x, y = 0.2, 6.5 - i * 3.15
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
    x, y = card(2, "바이트", "0과 1 칸 8개 묶음\n0 ~ 255를 담아요")
    cell(ax, x + 0.5, y + 0.75, 0.65, 0.65, "니", fs=12)
    arrow(ax, (x + 1.25, y + 1.07), (x + 1.8, y + 1.07), color=GREY, ms=10)
    for k, b in enumerate(NI):
        cell(ax, x + 1.95 + k * 0.85, y + 0.75, 0.75, 0.65, b, hot=True, fs=11)
    save(fig, OUT, "ai02-cards.svg")


if __name__ == "__main__":
    S, L = (7.2, 3.8), (12, 6.6)
    stage(opening, 2, OUT, "ai02-open", S, L)
    stage(dictionary, 3, OUT, "ai02-dict", S, L)
    stage(stuck, 2, OUT, "ai02-stuck", S, L)
    stage(branch, 3, OUT, "ai02-branch", S, L)
    stage(grow, 4, OUT, "ai02-grow", S, L)
    stage(longer, 1, OUT, "ai02-long", S, L)
    stage(unseen, 2, OUT, "ai02-unseen", S, L)
    stage(byte, 4, OUT, "ai02-byte", S, L)
    stage(bitrows, 3, OUT, "ai02-bits", S, L)
    stage(merge, 5, OUT, "ai02-merge", S, L)
    stage(cutnew, 3, OUT, "ai02-cut", S, L)
    stage(size, 3, OUT, "ai02-size", S, L)
    stage(rows, 2, OUT, "ai02-rows", S, L)
    stage(turn, 2, OUT, "ai02-turn", S, L)
    stage(lang, 3, OUT, "ai02-lang", S, L)
    stage(mean, 2, OUT, "ai02-mean", S, L)
    stage(morph, 2, OUT, "ai02-morph", S, L)
    stage(search, 3, OUT, "ai02-search", S, L)
    decide()
    stage(back, 3, OUT, "ai02-back", S, L)
    cards()
