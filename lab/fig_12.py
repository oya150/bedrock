"""알고리즘 12편 그림 만들기. 실행: python lab/fig_12.py  → docs/algorithms/img/12/*.svg
확인용 PNG: FIG_FMT=png FIG_OUT=<폴더> python lab/fig_12.py

글자는 SVG 안에 글자로 남긴다(글꼴 모양을 파일에 넣지 않는다). 보는 쪽 글꼴로 그려진다.
카드는 차분한 색으로, 강조(새로 받은 카드, 비교 화살표, 많이 든 일)만 빨강으로 칠한다.
"""
import itertools
import os

import matplotlib

matplotlib.use("svg")
import matplotlib.pyplot as plt
from matplotlib.patches import Arc, Circle, FancyArrowPatch, FancyBboxPatch, Rectangle

OUT = os.environ.get("FIG_OUT") or os.path.join(os.path.dirname(__file__), "..", "docs", "algorithms", "img", "12")
FMT = os.environ.get("FIG_FMT", "svg")
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
    if FMT != "svg":
        name = name.rsplit(".", 1)[0] + "." + FMT
    fig.savefig(os.path.join(OUT, name), bbox_inches="tight", pad_inches=0.25, dpi=110)
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


# 그림 1. 친구 그림
fig, ax = canvas(11.6, 5.2, 16.0, 8.6)
graph(ax, color={"나": RED})
ax.text(8.0, 8.3, "소식: 나 → … → 서준?", ha="center", va="center",
        fontsize=12, bbox=dict(boxstyle="round,pad=0.4", fc="white", ec=INK, lw=1.2))
save(fig, "a12-friends.svg")

# 그림 2. 줄 세우기: 꺼낸 친구와 남은 줄(새로 선 친구는 빨강)
lines = [("나", ["민준", "서연"], 2), ("민준", ["서연", "지우", "하준"], 2), ("서연", ["지우", "하준", "도윤"], 1),
         ("지우", ["하준", "도윤", "하은"], 1), ("하준", ["도윤", "하은"], 0), ("도윤", ["하은"], 0),
         ("하은", ["서준"], 1), ("서준", [], 0)]
fig, ax = canvas(7.6, 6.6, 11.0, 9.6)
ax.text(0.4, 9.0, "꺼낸 친구", ha="left", va="center", fontsize=12, fontweight="bold")
ax.text(4.2, 9.0, "남은 줄 (앞 ← → 뒤)", ha="left", va="center", fontsize=12, fontweight="bold")
for k, (who, q, new) in enumerate(lines):
    y = 8.0 - k * 1.0
    ax.text(0.6, y, f"{k + 1}. {who}", ha="left", va="center", fontsize=12, fontweight="bold")
    for j, nm in enumerate(q):
        hot = j >= len(q) - new
        ax.text(4.8 + j * 1.9, y, nm, ha="center", va="center", fontsize=11, color=RED if hot else "#222",
                fontweight="bold" if hot else "normal",
                bbox=dict(boxstyle="round,pad=0.3", fc="#fbe3dc" if hot else NOTE, ec=RED if hot else INK,
                          lw=1.4 if hot else 0.8))
    if not q:
        ax.text(4.2, y, "(빈 줄)", ha="left", va="center", fontsize=11, color=INK)
save(fig, "a12-queue.svg")

# 그림 3. 가까운 친구부터: 선을 몇 번 건너야 닿는지
STEP = {"나": 0, "민준": 1, "서연": 1, "지우": 2, "하준": 2, "도윤": 2, "하은": 3, "서준": 4}
SHADE = {0: RED, 1: "#f2a58e", 2: "#f8d3c7", 3: "#fbe3dc", 4: "#fdf1ec"}
fig, ax = canvas(11.6, 5.2, 16.0, 8.6)
graph(ax, color={k: SHADE[v] for k, v in STEP.items()}, label={k: str(v) for k, v in STEP.items() if v})
save(fig, "a12-bfs.svg")

# 그림 4. 서준에게 소식이 온 길
fig, ax = canvas(11.6, 5.2, 16.0, 8.6)
route = [("나", "민준"), ("민준", "지우"), ("지우", "하은"), ("하은", "서준")]
graph(ax, color={"나": RED, "서준": RED}, hot_edges=route)
save(fig, "a12-path.svg")

# 그림 5. 한 길로 끝까지: 찾은 순서와 돌아가기
ORDER = {"나": 1, "민준": 2, "지우": 3, "하은": 4, "도윤": 5, "서연": 6, "하준": 7, "서준": 8}
fig, ax = canvas(11.6, 5.6, 16.0, 9.2)
path = [("나", "민준"), ("민준", "지우"), ("지우", "하은"), ("하은", "도윤"), ("도윤", "서연"), ("서연", "하준"),
        ("하은", "서준")]
graph(ax, color={"나": RED}, label={k: str(v) for k, v in ORDER.items()}, hot_edges=path)
for a, b in path:
    (x1, y1), (x2, y2) = POS[a], POS[b]
    ax.add_patch(FancyArrowPatch((x1 + (x2 - x1) * 0.35, y1 + (y2 - y1) * 0.35),
                                 (x1 + (x2 - x1) * 0.6, y1 + (y2 - y1) * 0.6),
                                 arrowstyle="-|>", mutation_scale=16, color=RED, lw=0))
for a, b in [("하준", "서연"), ("서연", "도윤"), ("도윤", "하은")]:
    (x1, y1), (x2, y2) = POS[a], POS[b]
    dx_, dy_ = x2 - x1, y2 - y1
    n = (dx_ ** 2 + dy_ ** 2) ** 0.5
    ox, oy = -dy_ / n * 0.38, dx_ / n * 0.38
    ax.add_patch(FancyArrowPatch((x1 + dx_ * 0.2 + ox, y1 + dy_ * 0.2 + oy),
                                 (x1 + dx_ * 0.8 + ox, y1 + dy_ * 0.8 + oy),
                                 arrowstyle="-|>", mutation_scale=12, color=INK, lw=1.2, ls="--"))
ax.text(9.0, 8.8, "빨간 화살표: 가기   점선 화살표: 돌아가기", ha="center", va="center", fontsize=11)
save(fig, "a12-dfs.svg")

# 그림 6. 접시 쌓기: 걸어온 길을 쌓았다가 돌아가며 빼기
fig, ax = canvas(12.4, 5.0, 20.4, 8.2)
stacks = [(["나", "민준", "지우", "하은", "도윤", "서연", "하준"], "① 하준까지"),
          (["나", "민준", "지우", "하은"], "② 하준, 서연, 도윤 빼기"),
          (["나", "민준", "지우", "하은", "서준"], "③ 서준 쌓기")]
for k, (st, cap) in enumerate(stacks):
    x = 1.0 + k * 6.6
    for j, nm in enumerate(st):
        top = j == len(st) - 1
        ax.add_patch(Rectangle((x + 0.6, 1.2 + j * 0.8), 3.2, 0.62, fc=RED if top else NOTE, ec=INK, lw=1.2))
        ax.text(x + 2.2, 1.51 + j * 0.8, nm, ha="center", va="center", fontsize=11,
                color="white" if top else "#222", fontweight="bold")
    ax.text(x + 2.2, 0.5, cap, ha="center", va="center", fontsize=11, fontweight="bold")
save(fig, "a12-stack.svg")

# 그림 7. 큐와 스택: 민준, 서연 차례로 넣고 하나 꺼내기
fig, ax = canvas(11.6, 4.4, 19.0, 7.2)
ax.text(4.6, 6.6, "큐", ha="center", va="center", fontsize=14, fontweight="bold")
for j, nm in enumerate(["민준", "서연"]):
    hot = nm == "민준"
    ax.add_patch(Rectangle((2.4 + j * 2.2, 3.0), 2.0, 1.0, fc="#fbe3dc" if hot else NOTE, ec=RED if hot else INK,
                           lw=2.0 if hot else 1.2))
    ax.text(3.4 + j * 2.2, 3.5, nm, ha="center", va="center", fontsize=12, fontweight="bold",
            color=RED if hot else "#222")
ax.plot([2.2, 7.0], [2.85, 2.85], color=INK, lw=1.2)
ax.plot([2.2, 7.0], [4.15, 4.15], color=INK, lw=1.2)
arrow(ax, (8.6, 3.5), (7.0, 3.5), color=INK, lw=1.6)
ax.text(8.0, 2.4, "넣기", ha="center", va="center", fontsize=11)
arrow(ax, (2.2, 3.5), (0.4, 3.5), color=RED, lw=2.0)
ax.text(1.2, 2.4, "꺼내기", ha="center", va="center", fontsize=11, color=RED, fontweight="bold")
ax.text(4.6, 1.2, "먼저 넣은 민준", ha="center", va="center", fontsize=12, color=RED, fontweight="bold")
ax.text(14.4, 6.6, "스택", ha="center", va="center", fontsize=14, fontweight="bold")
for j, nm in enumerate(["민준", "서연"]):
    hot = nm == "서연"
    ax.add_patch(Rectangle((13.2, 2.0 + j * 1.2), 2.4, 1.0, fc="#fbe3dc" if hot else NOTE, ec=RED if hot else INK,
                           lw=2.0 if hot else 1.2))
    ax.text(14.4, 2.5 + j * 1.2, nm, ha="center", va="center", fontsize=12, fontweight="bold",
            color=RED if hot else "#222")
ax.plot([13.0, 13.0, 15.8, 15.8], [5.0, 1.85, 1.85, 5.0], color=INK, lw=1.2)
arrow(ax, (12.0, 5.8), (13.6, 4.6), color=INK, lw=1.6)
ax.text(11.6, 6.2, "넣기", ha="center", va="center", fontsize=11)
arrow(ax, (15.2, 4.6), (16.8, 5.8), color=RED, lw=2.0)
ax.text(17.4, 6.2, "꺼내기", ha="center", va="center", fontsize=11, color=RED, fontweight="bold")
ax.text(14.4, 1.0, "나중에 넣은 서연", ha="center", va="center", fontsize=12, color=RED, fontweight="bold")
save(fig, "a12-compare.svg")
