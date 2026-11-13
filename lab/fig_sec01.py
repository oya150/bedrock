"""보안 1편 그림 만들기. 실행: python lab/fig_sec01.py  → docs/security/img/01/*.svg

예시는 출입증 하나("민지, 3시까지")와 장난감 열쇠 한 쌍(n=33, e=3, d=7)을 편 끝까지 잇는다.
내용의 요약 숫자는 4, 바꾼 내용의 요약 숫자는 5로 둔다(본문에서 이렇게 가정한다).
계산은 모두 손으로 다시 해 볼 수 있다: 4^7 mod 33 = 16, 16^3 mod 33 = 4, 5^7 mod 33 = 14, 14^3 mod 33 = 5.
그림 안 글씨는 낱말과 숫자만 둔다(쉬운글-정책 5장).
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "es"))
from figkit import GREY, INK, RED, arrow, box, canvas, cell, label, outdir, save  # noqa: E402

OUT = outdir("01", "security")
N, E, D = 33, 3, 7
assert (E * D) % ((3 - 1) * (11 - 1)) == 1
assert pow(4, D, N) == 16 and pow(16, E, N) == 4
assert pow(5, D, N) == 14 and pow(14, E, N) == 5


def card(ax, x, y, name, until, sig=None, hot_name=False, hot_until=False, hot_sig=False, w=2.6):
    """출입증 한 장. 위에 내용 두 줄, 아래에 서명 칸."""
    h = 2.1 if sig is not None else 1.5
    box(ax, x, y, w, h, fc="white")
    top = y + h
    cell(ax, x + 0.15, top - 0.65, w - 0.3, 0.5, f"이름  {name}", hot=hot_name, fs=11.5)
    cell(ax, x + 0.15, top - 1.25, w - 0.3, 0.5, f"만료  {until}", hot=hot_until, fs=11.5)
    if sig is not None:
        cell(ax, x + 0.15, top - 1.9, w - 0.3, 0.5, f"서명  {sig}", hot=hot_sig, fs=11.5)


def fig_note():
    fig, ax = canvas(7.2, 2.4, 12, 4)
    label(ax, 2.9, 3.6, "로그인 서버가 준 출입증", fs=11, color=INK)
    card(ax, 1.6, 1.4, "민지", "3시")
    label(ax, 9.1, 3.6, "누가 고쳐 쓴 출입증", fs=11, color=INK)
    card(ax, 7.8, 1.4, "민지", "9시", hot_until=True)
    arrow(ax, (4.5, 2.15), (7.5, 2.15), color=GREY)
    label(ax, 6.0, 2.45, "고쳐 쓰기", fs=10.5, color=INK)
    save(fig, OUT, "sec01-note-1")


def fig_hash():
    fig, ax = canvas(7.2, 2.6, 12, 4.4)
    for row, (until, h, hot) in enumerate([("3시", 4, False), ("9시", 5, True)]):
        y = 2.7 - row * 1.8
        card(ax, 0.6, y - 0.5, "민지", until, hot_until=hot)
        arrow(ax, (3.4, y + 0.25), (5.6, y + 0.25))
        label(ax, 4.5, y + 0.6, "요약", fs=10.5, color=INK)
        cell(ax, 5.9, y - 0.05, 1.0, 0.6, str(h), hot=hot, fs=14)
    save(fig, OUT, "sec01-hash-1")


def fig_keys():
    fig, ax = canvas(7.2, 2.4, 12, 4)
    box(ax, 0.8, 0.6, 4.6, 2.6, fc="white")
    label(ax, 3.1, 2.75, "개인키 (주인만)", fs=12, color=RED, bold=True)
    label(ax, 2.15, 2.05, "나누는 수", fs=10.5, color=INK)
    cell(ax, 1.55, 1.0, 1.2, 0.7, "33", fs=14)
    label(ax, 4.05, 2.05, "거듭제곱", fs=10.5, color=INK)
    cell(ax, 3.45, 1.0, 1.2, 0.7, "7", hot=True, fs=14)
    box(ax, 6.6, 0.6, 4.6, 2.6, fc="white")
    label(ax, 8.9, 2.75, "공개키 (누구나)", fs=12, color=INK, bold=True)
    label(ax, 7.95, 2.05, "나누는 수", fs=10.5, color=INK)
    cell(ax, 7.35, 1.0, 1.2, 0.7, "33", fs=14)
    label(ax, 9.85, 2.05, "거듭제곱", fs=10.5, color=INK)
    cell(ax, 9.25, 1.0, 1.2, 0.7, "3", fs=14)
    label(ax, 6.0, 1.65, "짝", fs=12, color=INK)
    save(fig, OUT, "sec01-keys-1")


def calc_row(ax, x, y, parts, hot_last=False):
    """[a] → [식] → [b] 한 줄."""
    a, expr, b = parts
    cell(ax, x, y, 0.9, 0.6, a, fs=13)
    arrow(ax, (x + 1.0, y + 0.3), (x + 1.7, y + 0.3))
    cell(ax, x + 1.8, y, 3.0, 0.6, expr, fs=12)
    arrow(ax, (x + 4.9, y + 0.3), (x + 5.6, y + 0.3))
    cell(ax, x + 5.7, y, 0.9, 0.6, b, hot=hot_last, fs=13)


def fig_sign():
    fig, ax = canvas(7.2, 2.6, 12, 4.4)
    label(ax, 1.15, 3.9, "요약", fs=10.5, color=INK)
    label(ax, 4.3, 3.9, "개인키로 계산", fs=10.5, color=RED)
    label(ax, 7.15, 3.9, "서명", fs=10.5, color=INK)
    calc_row(ax, 0.7, 3.0, ("4", "4⁷ ÷ 33 의 나머지", "16"), hot_last=True)
    card(ax, 8.6, 0.3, "민지", "3시", sig=16, hot_sig=True, w=2.9)
    arrow(ax, (7.15, 2.9), (9.3, 2.45), color=GREY, rad=-0.2)
    save(fig, OUT, "sec01-sign-1")


def check(ax, y, h, s, back, ok):
    """받는 쪽 확인 두 줄: 내용 요약 / 서명을 공개키로 푼 값."""
    label(ax, 0.3, y + 1.55, "내용 요약", fs=10.5, color=INK, ha="left")
    cell(ax, 2.4, y + 1.25, 0.9, 0.6, str(h), hot=not ok, fs=13)
    label(ax, 0.3, y + 0.3, "서명 풀기", fs=10.5, color=INK, ha="left")
    cell(ax, 2.4, y, 0.9, 0.6, str(s), fs=13)
    arrow(ax, (3.4, y + 0.3), (4.1, y + 0.3))
    cell(ax, 4.2, y, 3.0, 0.6, f"{s}³ ÷ 33 의 나머지", fs=12)
    arrow(ax, (7.3, y + 0.3), (8.0, y + 0.3))
    cell(ax, 8.1, y, 0.9, 0.6, str(back), hot=not ok, fs=13)
    mark = "같음  통과" if ok else "다름  거부"
    label(ax, 10.4, y + 0.95, mark, fs=12.5, color=RED if not ok else INK, bold=True)


def fig_verify():
    fig, ax = canvas(7.2, 1.7, 12, 2.4)
    check(ax, 0.3, 4, 16, 4, True)
    save(fig, OUT, "sec01-verify-1")


def fig_forge():
    fig, ax = canvas(7.2, 1.7, 12, 2.4)
    check(ax, 0.3, 5, 16, 4, False)
    save(fig, OUT, "sec01-forge-1")


def fig_jwt():
    fig, ax = canvas(7.2, 2.6, 12, 4.4)
    parts = [("머리", ["방식  RS256", "이름표  key-1"]), ("본문", ["이름  민지", "만료  3시"]), ("서명", ["16"])]
    x = 0.4
    for k, (title, lines) in enumerate(parts):
        w = 3.5
        label(ax, x + w / 2, 3.95, title, fs=12, color=RED if title == "서명" else INK, bold=True)
        for i, s in enumerate(lines):
            cell(ax, x, 2.9 - i * 0.75, w, 0.6, s, hot=title == "서명", fs=11.5)
        if k < 2:
            label(ax, x + w + 0.2, 2.65, ".", fs=26, color=INK)
        x += w + 0.4
    label(ax, 6.0, 0.55, "머리 . 본문 . 서명", fs=13, color=INK)
    save(fig, OUT, "sec01-jwt-1")


def fig_leak():
    fig, ax = canvas(7.2, 2.6, 12, 4.4)
    label(ax, 0.3, 3.85, "새어 나간 개인키로", fs=11, color=RED, ha="left")
    calc_row(ax, 0.3, 3.0, ("5", "5⁷ ÷ 33 의 나머지", "14"), hot_last=True)
    check(ax, 0.3, 5, 14, 5, True)
    save(fig, OUT, "sec01-leak-1")


def fig_rotate():
    fig, ax = canvas(7.2, 2.4, 12, 4)
    label(ax, 3.0, 3.55, "공개키 목록 (전)", fs=11, color=INK)
    cell(ax, 1.2, 2.3, 3.6, 0.7, "key-1  33, 3", hot=True, fs=11.5)
    arrow(ax, (5.2, 2.65), (6.6, 2.65))
    label(ax, 9.0, 3.55, "공개키 목록 (후)", fs=11, color=INK)
    cell(ax, 7.2, 2.3, 3.6, 0.7, "key-2  새 열쇠", fs=11.5)
    cell(ax, 7.2, 1.3, 3.6, 0.7, "key-1  내림", dim=True, fs=11.5)
    save(fig, OUT, "sec01-rotate-1")


if __name__ == "__main__":
    for f in (fig_note, fig_hash, fig_keys, fig_sign, fig_verify, fig_forge, fig_jwt, fig_leak, fig_rotate):
        f()
    print("ok", OUT)
