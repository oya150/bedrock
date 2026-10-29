"""Elasticsearch 6편 그림 만들기. 실행: python lab/fig_es06.py  → docs/elasticsearch/img/06/*.svg"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "es"))
from figkit import (GREY, INK, LIGHT, NOTE, PAPER, PINK, RED, arrow, box, canvas, cell, cells,  # noqa: E402
                    label, outdir, save, story)
from matplotlib.patches import Circle, Rectangle  # noqa: E402

OUT = outdir("06")


def open_():
    fig, ax = canvas(9, 3.4, 13, 5.0)
    for k, (title, mb, h) in enumerate((("낱말 글자만 늘어놓기", "2.2 MB", 3.0), ("역색인\n(용어 사전 + 포스팅 목록)", "1.6 MB", 2.2))):
        x = 1.3 + k * 4.4
        ax.add_patch(Rectangle((x, 1.0), 1.8, h, fc=NOTE if k == 0 else PINK, ec=RED if k else INK, lw=1.6))
        label(ax, x + 0.9, 0.45, title, fs=10.5, color=RED if k else "#222")
        label(ax, x + 0.9, 1.0 + h / 2, mb, fs=11, color=RED if k else INK, bold=True)
    label(ax, 9.3, 2.6, "글 번호까지\n붙었는데\n더 작아요", fs=12, color=RED, ha="left", bold=True)
    save(fig, OUT, "es06-open.svg")


def map_():
    """정리 절: 이 편이 한 말을 결론 문장으로."""
    story(["용어 사전은 낱말을 블록으로 묶고 같은 앞부분은 한 번만 적어요",
           "작은 안내판으로 블록 하나를 골라 그 블록만 읽어요",
           "꼬리가 같은 칸까지 합친 FST는 트라이보다 더 작아요",
           "포스팅 목록은 앞 번호와의 차이만 필요한 비트만큼 적어요",
           "작게 담은 파일은 운영체제가 남는 메모리에 올려 빨리 읽어요"], 3, OUT, "es06-map.svg")


def block():
    fig, ax = canvas(10, 4.0, 15, 6.3)
    words = ["seal", "search", "searched", "searching", "season", "seat"]
    label(ax, 1.8, 5.0, "정렬된 낱말", fs=11, bold=True)
    for k, w in enumerate(words):
        label(ax, 1.8, 4.3 - k * 0.6, w, fs=11, color=INK)
    arrow(ax, (3.4, 2.8), (5.2, 2.8), color=RED)
    box(ax, 5.4, 0.9, 9.2, 3.9, fc=NOTE)
    label(ax, 5.7, 4.45, "블록 하나", fs=11, ha="left", bold=True)
    ax.add_patch(Rectangle((5.8, 5.25), 3.4, 0.75, fc="white", ec=RED, lw=1.5, ls="--"))
    label(ax, 7.5, 5.62, "sea", fs=12, color=RED, bold=True)
    label(ax, 9.5, 5.62, "← 함께 쓰는 앞부분 sea는 블록 밖에 한 번만", fs=10.5, color=RED, ha="left")
    rest = ["l", "rch", "rched", "rching", "son", "t"]
    for k, r in enumerate(rest):
        cell(ax, 5.8 + k * 1.4, 2.7, 1.25, 0.8, r, fs=10.5)
    label(ax, 10.0, 1.9, "낱말마다 나머지 글자만 적어요", fs=10.5, color=INK)
    label(ax, 7.5, 0.4, "실제 블록에는 낱말이 수십 개 들어요", fs=10.5, color=INK)
    save(fig, OUT, "es06-block.svg")


def node(ax, x, y, final=False, hot=False):
    ax.add_patch(Circle((x, y), 0.28, fc=PINK if hot else "white", ec=RED if hot else INK, lw=2.2 if final else 1.3))
    if final:
        ax.add_patch(Circle((x, y), 0.19, fc="none", ec=RED if hot else INK, lw=1.0))


def edge(ax, a, b, ch, hot=False):
    arrow(ax, a, b, color=RED if hot else INK, lw=1.5, ms=10)
    ax.text((a[0] + b[0]) / 2, (a[1] + b[1]) / 2 + 0.22, ch, ha="center", fontsize=11, color=RED if hot else "#222")


def trie():
    fig, ax = canvas(11, 4.4, 18, 7.2)
    label(ax, 0.3, 6.8, "낱말 넷: tap, taps, top, tops", fs=12, ha="left", bold=True)
    # 트라이
    label(ax, 4.2, 6.0, "트라이: 앞부분만 나눠 써요 (칸 8개)", fs=11, color=INK)
    P = {"r": (0.6, 3.2), "t": (1.9, 3.2), "ta": (3.2, 4.5), "to": (3.2, 1.9), "tap": (4.5, 4.5), "top": (4.5, 1.9),
         "taps": (5.8, 4.5), "tops": (5.8, 1.9)}
    for k, (x, y) in P.items():
        node(ax, x, y, final=k in ("tap", "taps", "top", "tops"))
    for a, b, ch in (("r", "t", "t"), ("t", "ta", "a"), ("t", "to", "o"), ("ta", "tap", "p"), ("to", "top", "p"),
                     ("tap", "taps", "s"), ("top", "tops", "s")):
        (x1, y1), (x2, y2) = P[a], P[b]
        edge(ax, (x1 + 0.28, y1), (x2 - 0.28, y2), ch)
    label(ax, 3.2, 0.9, "p, s 칸이 두 번씩 있어요", fs=10, color=INK)
    # 최소 자동자
    label(ax, 13.3, 6.0, "FST: 꼬리도 나눠 써요 (칸 5개)", fs=11, color=RED)
    Q = {"r": (9.8, 3.2), "t": (11.1, 3.2), "m": (12.6, 3.2), "p": (14.1, 3.2), "s": (15.6, 3.2)}
    for k, (x, y) in Q.items():
        node(ax, x, y, final=k in ("p", "s"), hot=k in ("m", "p", "s"))
    edge(ax, (10.08, 3.2), (10.82, 3.2), "t")
    arrow(ax, (11.35, 3.35), (12.35, 3.35), color=RED, lw=1.5, ms=10, rad=-0.5)
    ax.text(11.85, 4.05, "a", ha="center", fontsize=11, color=RED)
    arrow(ax, (11.35, 3.05), (12.35, 3.05), color=RED, lw=1.5, ms=10, rad=0.5)
    ax.text(11.85, 2.2, "o", ha="center", fontsize=11, color=RED)
    edge(ax, (12.88, 3.2), (13.82, 3.2), "p", hot=True)
    edge(ax, (14.38, 3.2), (15.32, 3.2), "s", hot=True)
    label(ax, 12.9, 0.9, "ta-와 to-가 같은 꼬리 p, ps를 함께 써요", fs=10, color=RED)
    label(ax, 9.0, 0.2, "이중 원 = 여기서 끝나는 낱말이 있어요", fs=10, color=INK)
    save(fig, OUT, "es06-trie.svg")


def index():
    fig, ax = canvas(11, 4.8, 18, 7.8)
    label(ax, 0.3, 7.4, "메모리", fs=12, ha="left", bold=True)
    box(ax, 0.3, 4.5, 9.4, 2.6, fc=PINK, ec=RED)
    label(ax, 0.6, 6.75, "안내판", fs=11, ha="left", color=RED, bold=True)
    P = {"r": (1.2, 5.6), "s": (2.6, 5.6), "sa": (4.0, 6.5), "se": (4.0, 5.6), "sea": (5.4, 5.6), "sh": (4.0, 4.9)}
    for k, (x, y) in P.items():
        node(ax, x, y, hot=k in ("s", "se", "sea"))
    for a, b, ch, dy in (("r", "s", "s", 0.22), ("s", "sa", "a", 0.3), ("s", "se", "e", 0.12), ("se", "sea", "a", 0.22),
                         ("s", "sh", "h", -0.55)):
        (x1, y1), (x2, y2) = P[a], P[b]
        hot = (a, b) in (("r", "s"), ("s", "se"), ("se", "sea"))
        arrow(ax, (x1 + 0.28, y1), (x2 - 0.28, y2), color=RED if hot else INK, lw=1.5, ms=10)
        ax.text((x1 + x2) / 2 + (0.15 if dy == 0.12 else 0), (y1 + y2) / 2 + dy, ch, ha="center", fontsize=11,
                color=RED if hot else "#222")
    for k, (x, y, t) in {"sa": (4.4, 6.5, "→ 블록 41"), "sea": (5.8, 5.6, "→ 블록 42"), "sh": (4.4, 4.9, "→ 블록 43")}.items():
        label(ax, x, y, t, fs=10.5, ha="left", color=RED if k == "sea" else INK)
    ax.plot([0.2, 17.8], [4.1, 4.1], color=GREY, lw=1.5, ls="--")
    label(ax, 0.3, 3.65, "디스크", fs=12, ha="left", bold=True)
    for k, (name, ts) in enumerate((("블록 41", "sable … sawyer"), ("블록 42", "seal … seat"), ("블록 43", "shack … shy"))):
        x = 0.3 + k * 4.4
        hot = k == 1
        box(ax, x, 1.2, 4.0, 1.9, fc=PINK if hot else NOTE, ec=RED if hot else INK, round_=False)
        label(ax, x + 2.0, 2.65, name, fs=11, color=RED if hot else "#222", bold=hot)
        label(ax, x + 2.0, 1.85, ts, fs=10, color=INK)
    label(ax, 14.9, 2.15, "블록은 일부만 그렸어요", fs=10, color=INK)
    box(ax, 13.6, 5.2, 4.0, 1.1, fc=PAPER)
    label(ax, 15.6, 5.75, "찾기: search", fs=12)
    arrow(ax, (13.5, 5.75), (9.8, 5.75), color=RED)
    label(ax, 11.65, 6.55, "① 안내판을 s, e, a로 따라가\n블록 42를 골라요", fs=10, color=RED)
    arrow(ax, (6.9, 5.2), (6.6, 3.2), color=RED)
    label(ax, 7.2, 3.6, "② 블록 42만 읽어 차례로 훑어요", fs=10, color=RED, ha="left")
    save(fig, OUT, "es06-index.svg")


def postings():
    fig, ax = canvas(11, 3.4, 18, 7.0)
    ids = [3, 7, 8, 15, 21, 22, 40]
    d = [ids[0]] + [b - a for a, b in zip(ids, ids[1:])]
    label(ax, 0.3, 6.5, "환불의 포스팅 목록", fs=12, ha="left", bold=True)
    label(ax, 0.3, 5.45, "글 번호", fs=11, ha="left", color=INK)
    cells(ax, 3.0, 5.05, ids, w=1.1, h=0.8)
    label(ax, 11.6, 5.45, "번호가 커질수록 자리도 커져요", fs=10, color=INK, ha="left")
    label(ax, 0.3, 3.75, "차이값", fs=11, ha="left", color=RED)
    cells(ax, 3.0, 3.35, d, w=1.1, h=0.8, hot=range(len(d)))
    label(ax, 11.6, 3.75, "앞 번호와의 차이만 적어요", fs=10, color=RED, ha="left")
    for k in range(1, len(ids)):
        ax.annotate("", xy=(3.55 + k * 1.18, 4.2), xytext=(3.55 + k * 1.18, 5.0), arrowprops=dict(arrowstyle="->", color=GREY))
    label(ax, 8.0, 1.9, "번호는 커져도 차이는 작아요. 첫 번호는 0과의 차이예요", fs=11, color=INK)
    save(fig, OUT, "es06-postings.svg")


def pack():
    fig, ax = canvas(10.5, 3.6, 16, 5.4)
    box(ax, 0.3, 3.9, 15.4, 1.0, fc=LIGHT, ec=GREY)
    label(ax, 8.0, 4.4, "그대로 적으면: 128개 × 32비트 = 512바이트", fs=11, color=INK)
    blocks = [("묶음 1", 18, 5), ("묶음 2", 9, 4), ("묶음 3", 40, 6)]
    for k, (n, mx, b) in enumerate(blocks):
        x = 0.3 + k * 5.3
        hot = k == 0
        box(ax, x, 1.5, 4.8, 1.9, fc=PINK if hot else NOTE, ec=RED if hot else INK)
        label(ax, x + 2.4, 3.0, f"{n}: 가장 큰 차이 {mx}", fs=10.5, color=RED if hot else "#222", bold=True)
        label(ax, x + 2.4, 2.2, f"{b}비트 × 128 = {b * 16}바이트", fs=10.5, color=RED if hot else INK)
    label(ax, 8.0, 0.7, "묶음마다 가장 큰 값에 맞춰 비트 수를 정해요", fs=11, color=INK, bold=True)
    save(fig, OUT, "es06-pack.svg")


def cache():
    fig, ax = canvas(10.5, 4.0, 16, 6.0)
    label(ax, 0.3, 5.6, "컴퓨터 메모리 16 GB", fs=12, ha="left", bold=True)
    W = 15.2
    for row, (heap, y) in enumerate(((8, 4.3), (14, 2.6))):
        hw = W * heap / 16
        box(ax, 0.4, y, hw, 0.9, fc=LIGHT, ec=GREY, round_=False)
        label(ax, 0.4 + hw / 2, y + 0.45, f"ES 전용 메모리(자바 힙) {heap} GB", fs=10, color=INK)
        box(ax, 0.4 + hw, y, W - hw, 0.9, fc=PINK, ec=RED, round_=False)
        txt = f"남는 메모리 {16 - heap} GB:\n용어 사전·포스팅 목록" if row == 0 else f"{16 - heap} GB"
        label(ax, 0.4 + hw + (W - hw) / 2, y + 0.45, txt, fs=10 if row == 0 else 9.5, color=RED)
    label(ax, 15.7, 2.2, "힙을 키우면 파일이 올라갈 자리가 좁아져요", fs=10, color=RED, ha="right")
    box(ax, 0.4, 0.3, W, 1.0, fc=NOTE)
    label(ax, 8.0, 0.8, "디스크: 역색인 파일 전체. 남는 메모리에 없는 부분은 디스크에서 읽어요", fs=10.5, color=INK)
    save(fig, OUT, "es06-cache.svg")


def decide():
    fig, ax = canvas(10, 3.8, 15, 5.7)
    box(ax, 2.0, 4.4, 11.0, 1.0, fc=LIGHT, ec=GREY)
    label(ax, 7.5, 4.9, "값이 모두 다르고 앞부분도 겹치지 않는 필드 (무작위 요청 번호처럼)", fs=10.5, color=INK)
    arrow(ax, (7.5, 4.3), (7.5, 3.7), ms=12)
    box(ax, 3.5, 2.8, 8.0, 0.9, fc=NOTE)
    label(ax, 7.5, 3.25, "이 필드로 글을 찾거나 거르나요?", fs=10.5, bold=True)
    arrow(ax, (5.0, 2.7), (3.3, 1.9)); label(ax, 3.7, 2.45, "예", fs=10, color=INK)
    box(ax, 0.3, 0.4, 6.4, 1.4, fc=PAPER)
    label(ax, 3.5, 1.1, "역색인을 둬요\n(사전이 커도 찾으려면 필요해요)", fs=10)
    arrow(ax, (10.0, 2.7), (11.7, 1.9), color=RED); label(ax, 11.4, 2.45, "아니요", fs=10, color=RED)
    box(ax, 8.3, 0.4, 6.4, 1.4, fc=PINK, ec=RED)
    label(ax, 11.5, 1.1, "\"index\": false로 역색인을 만들지 않아요\n(원본에는 그대로 남아요)", fs=10, color=RED)
    save(fig, OUT, "es06-decide.svg")


def output():
    """FST의 값: 화살표에 붙은 값을 더하면 낱말마다 다른 값이 나온다."""
    fig, ax = canvas(10.5, 3.6, 16, 5.6)
    Q = {"r": (1.0, 2.8), "t": (3.2, 2.8), "m": (6.4, 2.8), "p": (9.6, 2.8), "s": (12.8, 2.8)}
    for k, (x, y) in Q.items():
        node(ax, x, y, final=k in ("p", "s"))
    def lab(x, y, s, hot=False):
        ax.text(x, y, s, ha="center", fontsize=11, color=RED if hot else "#222")
    arrow(ax, (1.3, 2.8), (2.9, 2.8), lw=1.5, ms=10); lab(2.1, 3.05, "t / 5")
    arrow(ax, (3.45, 2.95), (6.15, 2.95), lw=1.5, ms=10, rad=-0.4); lab(4.8, 3.75, "a / 0")
    arrow(ax, (3.45, 2.65), (6.15, 2.65), color=RED, lw=1.5, ms=10, rad=0.4); lab(4.8, 1.65, "o / 4", hot=True)
    arrow(ax, (6.7, 2.8), (9.3, 2.8), lw=1.5, ms=10); lab(8.0, 3.05, "p / 0")
    arrow(ax, (9.9, 2.8), (12.5, 2.8), lw=1.5, ms=10); lab(11.2, 3.05, "s / 1")
    label(ax, 0.3, 5.2, "글자 / 값: 지나는 화살표의 값을 더해요", fs=11, ha="left", bold=True)
    rows = ["tap = 5+0+0 = 5", "taps = 5+0+0+1 = 6", "top = 5+4+0 = 9", "tops = 5+4+0+1 = 10"]
    for k, r in enumerate(rows):
        label(ax, 13.6 + (k % 2) * 0.0, 4.9 - k * 0.45, r, fs=10, ha="left", color=RED if r.startswith("to") else INK)
    label(ax, 8.0, 0.6, "꼬리 p, s를 함께 써도 o 화살표의 4 덕분에 top과 tap의 값이 달라요", fs=10.5, color=INK)
    save(fig, OUT, "es06-output.svg")


if __name__ == "__main__":
    open_(); map_(); block(); index(); trie(); output(); postings(); pack(); cache(); decide()
