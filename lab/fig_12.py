"""알고리즘 12편 그림 만들기. 실행: python lab/fig_12.py  → docs/algorithms/img/12/*.svg

글자는 SVG 안에 글자로 남긴다(글꼴 모양을 파일에 넣지 않는다). 보는 쪽 글꼴로 그려진다.
카드는 차분한 색으로, 강조(새로 받은 카드, 비교 화살표, 많이 든 일)만 빨강으로 칠한다.
"""
import itertools
import os

import matplotlib

matplotlib.use("svg")
import matplotlib.pyplot as plt
from matplotlib.patches import Arc, Circle, FancyArrowPatch, FancyBboxPatch, Rectangle

OUT = os.path.join(os.path.dirname(__file__), "..", "docs", "algorithms", "img", "12")
os.makedirs(OUT, exist_ok=True)

plt.rcParams.update({
    "font.family": ["Apple SD Gothic Neo", "Noto Sans KR", "Malgun Gothic", "sans-serif"],
    "svg.fonttype": "none",
    "text.color": "#222",
    "figure.facecolor": "white",
    "savefig.facecolor": "white",
})

RED, GREY, INK, PAPER, NOTE, YEL = "#e4572e", "#c9ccd1", "#555", "#f4f6f8", "#fffdf5", "#f6c445"
BLUE, GREEN = "#7da2c8", "#8fb58f"
LIGHT = "#e9ecef"


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), bbox_inches="tight", pad_inches=0.25)
    plt.close(fig)


def canvas(w, h, xmax, ymax):
    fig, ax = plt.subplots(figsize=(w, h))
    ax.set_xlim(0, xmax); ax.set_ylim(0, ymax); ax.axis("off")
    return fig, ax


def box(ax, x, y, w, h, fc="white", ec=INK, lw=1.8):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.08", fc=fc, ec=ec, lw=lw))


def arrow(ax, a, b, color=INK, lw=2, rad=0.0, ms=18):
    ax.add_patch(FancyArrowPatch(a, b, arrowstyle="-|>", mutation_scale=ms, color=color, lw=lw,
                                 connectionstyle=f"arc3,rad={rad}"))


def kid(ax, cx, y, s=1.0):
    ax.add_patch(Circle((cx, y + 1.55 * s), 0.32 * s, fc="white", ec=INK, lw=1.6))
    ax.add_patch(Circle((cx - 0.11 * s, y + 1.6 * s), 0.035 * s, fc=INK))
    ax.add_patch(Circle((cx + 0.11 * s, y + 1.6 * s), 0.035 * s, fc=INK))
    ax.add_patch(Arc((cx, y + 1.5 * s), 0.3 * s, 0.2 * s, theta1=200, theta2=340, color=INK, lw=1.4))
    ax.plot([cx, cx], [y + 1.23 * s, y + 0.55 * s], color=INK, lw=2)
    ax.plot([cx, cx - 0.3 * s], [y + 0.55 * s, y], color=INK, lw=2)
    ax.plot([cx, cx + 0.3 * s], [y + 0.55 * s, y], color=INK, lw=2)
    ax.plot([cx - 0.35 * s, cx + 0.35 * s], [y + 1.0 * s, y + 1.0 * s], color=INK, lw=2)


def card(ax, x, y, w, h, num, hot=False, gone=False, fs=12):
    fc = LIGHT if gone else ("#fbe3dc" if hot else NOTE)
    ax.add_patch(Rectangle((x, y), w, h, fc=fc, ec=RED if hot else (GREY if gone else INK), lw=2.2 if hot else 1.2))
    ax.text(x + w / 2, y + h / 2, str(num), ha="center", va="center", fontsize=fs,
            color=RED if hot else (GREY if gone else "#222"), fontweight="bold")


def stones(ax, x, y, n, color=INK, r=0.13, gap=0.34):
    for k in range(n):
        ax.add_patch(Circle((x + k * gap, y), r, fc=color, ec=color))


def row(ax, x, y, nums, cw=0.9, ch=1.1, gap=0.1, hot=(), fs=12, gone=()):
    for k, n in enumerate(nums):
        card(ax, x + k * (cw + gap), y, cw, ch, n, hot=(k in hot), gone=(k in gone), fs=fs)
    return x + len(nums) * (cw + gap) - gap


POS = {"나": (1.2, 4.0), "민준": (4.2, 6.2), "서연": (4.2, 1.8), "하준": (7.2, 4.0), "지우": (8.4, 7.0),
       "도윤": (8.4, 1.0), "하은": (11.4, 4.0), "서준": (14.4, 4.0)}
EDGES = [("나", "민준"), ("나", "서연"), ("민준", "지우"), ("민준", "하준"), ("서연", "도윤"), ("서연", "하준"),
         ("지우", "하은"), ("도윤", "하은"), ("하은", "서준")]


def graph(ax, dx=0.0, dy=0.0, s=1.0, color=None, label=None, hot_edges=(), fs=11, r=0.62):
    color = color or {}
    label = label or {}
    for a, b in EDGES:
        (x1, y1), (x2, y2) = POS[a], POS[b]
        hot = (a, b) in hot_edges or (b, a) in hot_edges
        ax.plot([dx + x1 * s, dx + x2 * s], [dy + y1 * s, dy + y2 * s], color=RED if hot else GREY,
                lw=2.6 if hot else 1.6, zorder=0)
    for name, (x, y) in POS.items():
        fc = color.get(name, NOTE)
        ax.add_patch(Circle((dx + x * s, dy + y * s), r * s, fc=fc, ec=RED if fc != NOTE else INK, lw=1.8))
        ax.text(dx + x * s, dy + y * s, name, ha="center", va="center", fontsize=fs, fontweight="bold",
                color="white" if fc == RED else "#222")
        if name in label:
            ax.text(dx + x * s + 0.75 * s, dy + y * s + 0.62 * s, label[name], ha="center", va="center",
                    fontsize=fs - 1, color=RED, fontweight="bold",
                    bbox=dict(boxstyle="circle,pad=0.15", fc="white", ec=RED, lw=1.0))


# 1. 여는 장면: 친구 그림
fig, ax = canvas(11.6, 5.2, 16.0, 8.6)
graph(ax, color={"나": RED})
ax.text(8.0, 8.3, "선으로 이어진 사이는 서로 친구예요. 서준이까지 소식이 가려면?", ha="center", va="center",
        fontsize=12, bbox=dict(boxstyle="round,pad=0.4", fc="white", ec=INK, lw=1.2))
save(fig, "a12-friends.svg")

# 2. 이 편의 지도
fig, ax = canvas(13.6, 2.9, 24.2, 4.6)
titles = ["친구 그림", "가까운 친구부터", "줄 서서 차례로", "한 길로 끝까지", "접시 쌓고 돌아가기"]
for i, t in enumerate(titles):
    x = 0.3 + i * 4.8
    box(ax, x, 0.4, 3.8, 3.6)
    ax.text(x + 1.9, 0.95, t, ha="center", va="center", fontsize=12, fontweight="bold")
    if i == 0:
        pts = {"a": (0.5, 2.6), "b": (1.3, 3.3), "c": (1.3, 1.9), "d": (2.1, 2.6), "e": (2.9, 3.3), "f": (3.3, 2.0)}
        for u, v in [("a", "b"), ("a", "c"), ("b", "d"), ("c", "d"), ("b", "e"), ("d", "f"), ("e", "f")]:
            ax.plot([x + pts[u][0], x + pts[v][0]], [pts[u][1], pts[v][1]], color=GREY, lw=1.2)
        for u, (px, py) in pts.items():
            ax.add_patch(Circle((x + px, py), 0.17, fc=RED if u == "a" else NOTE, ec=INK, lw=1))
    elif i == 1:
        for k, rr in enumerate([0.3, 0.75, 1.2]):
            ax.add_patch(Circle((x + 1.9, 2.6), rr, fc="none", ec=RED if k == 0 else GREY, lw=1.4))
        ax.add_patch(Circle((x + 1.9, 2.6), 0.12, fc=RED, ec=RED))
    elif i == 2:
        for k in range(4):
            ax.add_patch(Circle((x + 0.7 + k * 0.8, 2.6), 0.25, fc=RED if k == 0 else NOTE, ec=INK, lw=1))
        arrow(ax, (x + 0.5, 3.3), (x + 0.1, 3.3), color=RED, lw=1.2, ms=9)
    elif i == 3:
        pts = [(0.5, 3.2), (1.3, 2.6), (2.1, 3.2), (2.9, 2.4)]
        for (a1, b1), (a2, b2) in zip(pts, pts[1:]):
            arrow(ax, (x + a1, b1), (x + a2, b2), color=RED, lw=1.4, ms=9)
    else:
        for k in range(4):
            ax.add_patch(Rectangle((x + 1.2, 1.5 + k * 0.45), 1.4, 0.35, fc=RED if k == 3 else NOTE, ec=INK, lw=1))
    if i < 4:
        arrow(ax, (x + 3.95, 2.2), (x + 4.65, 2.2))
save(fig, "a12-map.svg")

# 3. 가까운 친구부터: 단계 색칠 + 줄 상태
STEP = {"나": 0, "민준": 1, "서연": 1, "지우": 2, "하준": 2, "도윤": 2, "하은": 3, "서준": 4}
SHADE = {0: RED, 1: "#f2a58e", 2: "#f8d3c7", 3: "#fbe3dc", 4: "#fdf1ec"}
fig, ax = canvas(12.4, 9.4, 20.4, 15.6)
graph(ax, dx=2.0, dy=6.6, s=1.0, color={k: SHADE[v] for k, v in STEP.items()},
      label={k: str(v) for k, v in STEP.items() if v})
ax.text(10.2, 15.2, "동그라미 옆 숫자: 나에게서 친구 선을 몇 번 건너야 닿는지", ha="center", va="center", fontsize=11)
lines = [("나", ["민준", "서연"]), ("민준", ["서연", "지우", "하준"]), ("서연", ["지우", "하준", "도윤"]),
         ("지우", ["하준", "도윤", "하은"]), ("하준", ["도윤", "하은"]), ("도윤", ["하은"]), ("하은", ["서준"]),
         ("서준", [])]
ax.text(0.4, 6.0, "꺼낸 친구", ha="left", va="center", fontsize=11, fontweight="bold")
ax.text(3.6, 6.0, "남은 줄 (앞 ← → 뒤)", ha="left", va="center", fontsize=11, fontweight="bold")
for k, (who, q) in enumerate(lines):
    y = 5.3 - k * 0.68
    ax.text(0.6, y, f"{k + 1}. {who}", ha="left", va="center", fontsize=11, color=RED, fontweight="bold")
    for j, nm in enumerate(q):
        ax.text(3.9 + j * 1.6, y, nm, ha="center", va="center", fontsize=10,
                bbox=dict(boxstyle="round,pad=0.25", fc=NOTE, ec=INK, lw=0.8))
save(fig, "a12-bfs.svg")

# 4. 한 길로 끝까지: 걸어온 길과 돌아가기
ORDER = {"나": 1, "민준": 2, "지우": 3, "하은": 4, "도윤": 5, "서연": 6, "하준": 7, "서준": 8}
fig, ax = canvas(12.4, 7.0, 20.4, 11.6)
path = [("나", "민준"), ("민준", "지우"), ("지우", "하은"), ("하은", "도윤"), ("도윤", "서연"), ("서연", "하준"),
        ("하은", "서준")]
graph(ax, dx=2.0, dy=2.4, s=1.0, color={"나": RED}, label={k: str(v) for k, v in ORDER.items()}, hot_edges=path)
for a, b in path:
    (x1, y1), (x2, y2) = POS[a], POS[b]
    mx, my = 2.0 + (x1 + x2) / 2, 2.4 + (y1 + y2) / 2
    ax.add_patch(FancyArrowPatch((2.0 + x1 + (x2 - x1) * 0.35, 2.4 + y1 + (y2 - y1) * 0.35),
                                 (2.0 + x1 + (x2 - x1) * 0.6, 2.4 + y1 + (y2 - y1) * 0.6),
                                 arrowstyle="-|>", mutation_scale=16, color=RED, lw=0))
for a, b in [("하준", "서연"), ("서연", "도윤"), ("도윤", "하은")]:
    (x1, y1), (x2, y2) = POS[a], POS[b]
    dx_, dy_ = x2 - x1, y2 - y1
    n = (dx_ ** 2 + dy_ ** 2) ** 0.5
    ox, oy = -dy_ / n * 0.38, dx_ / n * 0.38
    ax.add_patch(FancyArrowPatch((2.0 + x1 + dx_ * 0.2 + ox, 2.4 + y1 + dy_ * 0.2 + oy),
                                 (2.0 + x1 + dx_ * 0.8 + ox, 2.4 + y1 + dy_ * 0.8 + oy),
                                 arrowstyle="-|>", mutation_scale=12, color=INK, lw=1.2, ls="--"))
ax.text(10.2, 11.0, "빨간 선을 따라 한 길로 가요. 동그라미 옆 숫자는 찾은 순서", ha="center", va="center", fontsize=11)
ax.text(10.2, 0.9, "하준에서 더 갈 곳이 없어 서연, 도윤, 하은으로 돌아가요. 하은에서 서준으로 가요", ha="center",
        va="center", fontsize=11, color=RED, fontweight="bold")
save(fig, "a12-dfs.svg")

# 5. 접시 쌓기: 걸어온 길을 쌓았다가 돌아가며 빼기
fig, ax = canvas(12.4, 5.0, 20.4, 8.2)
stacks = [(["나", "민준", "지우", "하은", "도윤", "서연", "하준"], "① 하준까지 왔어요"),
          (["나", "민준", "지우", "하은"], "② 하준, 서연, 도윤 접시를 빼며 돌아가요"),
          (["나", "민준", "지우", "하은", "서준"], "③ 하은에서 서준으로 가요")]
for k, (st, cap) in enumerate(stacks):
    x = 1.0 + k * 6.6
    for j, nm in enumerate(st):
        top = j == len(st) - 1
        ax.add_patch(Rectangle((x + 0.6, 1.2 + j * 0.8), 3.2, 0.62, fc=RED if top else NOTE, ec=INK, lw=1.2))
        ax.text(x + 2.2, 1.51 + j * 0.8, nm, ha="center", va="center", fontsize=11,
                color="white" if top else "#222", fontweight="bold")
    ax.text(x + 2.2, 0.5, cap, ha="center", va="center", fontsize=10, fontweight="bold")
ax.text(10.2, 7.6, "맨 위 접시가 지금 있는 친구예요. 새 친구는 위에 쌓아요. 돌아갈 때는 맨 위부터 빼요", ha="center",
        va="center", fontsize=11, color=RED)
save(fig, "a12-stack.svg")
