"""인체 9편 그림 만들기. 실행: python lab/fig_b09.py  → docs/body/img/09/*.svg

글자는 SVG 안에 글자로 남긴다(글꼴 모양을 파일에 넣지 않는다). 보는 쪽 글꼴로 그려진다.
카드는 차분한 색으로, 강조(새로 받은 카드, 비교 화살표, 많이 든 일)만 빨강으로 칠한다.
"""
import itertools
import os

import matplotlib

matplotlib.use("svg")
import matplotlib.pyplot as plt
from matplotlib.patches import Arc, Circle, FancyArrowPatch, FancyBboxPatch, Rectangle

OUT = os.environ.get("FIG_OUT") or os.path.join(os.path.dirname(__file__), "..", "docs", "body", "img", "09")
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

import math
from matplotlib.patches import Ellipse, Polygon

BONE = "#efe6d2"
MUSCLE = "#e8a598"
TENDON = "#c9b79c"
SKIN = "#f6d8c4"
CELL = "#fbe3dc"


def bone(ax, p, q, w=0.5):
    (x1, y1), (x2, y2) = p, q
    L = math.hypot(x2 - x1, y2 - y1)
    a = math.degrees(math.atan2(y2 - y1, x2 - x1))
    ax.add_patch(FancyBboxPatch((0, -w / 2), L, w, boxstyle=f"round,pad=0,rounding_size={w/2}", fc=BONE, ec=INK,
                                lw=1.4, transform=__import__("matplotlib").transforms.Affine2D().rotate_deg(a).translate(x1, y1) + ax.transData))


def muscle(ax, p, q, fat=0.6, fc=MUSCLE, ec=RED, lw=1.4):
    (x1, y1), (x2, y2) = p, q
    cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
    L = math.hypot(x2 - x1, y2 - y1)
    a = math.degrees(math.atan2(y2 - y1, x2 - x1))
    ax.add_patch(Ellipse((cx, cy), L, fat, angle=a, fc=fc, ec=ec, lw=lw))


def arm(ax, sx, sy, ang, upper=4.0, fore=3.6, bent=True, label=True):
    """어깨(sx, sy)에서 위팔은 아래로, 아래팔은 ang 도로."""
    ex, ey = sx, sy - upper
    hx, hy = ex + fore * math.cos(math.radians(ang)), ey + fore * math.sin(math.radians(ang))
    bone(ax, (sx, sy), (ex, ey), w=0.5)
    bone(ax, (ex, ey), (hx, hy), w=0.42)
    ax.add_patch(Circle((ex, ey), 0.38, fc=BONE, ec=INK, lw=1.4))
    # 앞 근육: 어깨 앞 → 아래팔 (팔꿈치 조금 아래)
    ins = (ex + 0.9 * math.cos(math.radians(ang)), ey + 0.9 * math.sin(math.radians(ang)))
    front_fat = 1.1 if bent else 0.55
    back_fat = 0.55 if bent else 1.0
    muscle(ax, (sx + 0.55, sy - 0.4), (ins[0] + 0.1, ins[1] + 0.25), fat=front_fat,
           fc=RED if bent else MUSCLE)
    muscle(ax, (sx - 0.55, sy - 0.4), (ex - 0.45, ey - 0.1), fat=back_fat, fc=MUSCLE if bent else RED)
    return (ex, ey), (hx, hy)


# 1. 알통: 위팔, 아래팔, 팔꿈치
fig, ax = canvas(6.0, 4.6, 8.0, 6.2)
kid(ax, 3.0, 0.4, 3.0)
ax.plot([3.0 + 1.05, 4.9], [0.4 + 3.0, 0.4 + 3.0], color=INK, lw=2)
ax.plot([4.9, 4.9], [3.4, 5.2], color=INK, lw=2)
ax.add_patch(Ellipse((4.3, 3.65), 0.95, 0.55, fc=CELL, ec=RED, lw=1.6))
ax.text(4.3, 4.35, "알통", ha="center", va="center", fontsize=13, color=RED, fontweight="bold")
ax.text(4.0, 2.95, "위팔", ha="center", va="center", fontsize=11)
ax.text(5.15, 4.6, "아래팔", ha="left", va="center", fontsize=11)
ax.text(5.15, 3.25, "팔꿈치", ha="left", va="center", fontsize=11)
save(fig, "b09-flex.svg")

# 2. 뼈가 하는 일: 받치기, 지키기, 피 세포 만들기
fig, ax = canvas(11.0, 4.4, 18.0, 7.2)
ax.add_patch(Polygon([(0.6, 1.4), (2.8, 5.4), (5.0, 1.4)], closed=True, fc=CELL, ec=INK, lw=1.4))
ax.plot([2.8, 2.8], [1.4, 5.4], color=RED, lw=3.5)
ax.text(3.1, 4.2, "기둥", ha="left", va="center", fontsize=11, color=RED, fontweight="bold")
ax.text(2.8, 0.6, "받치기", ha="center", va="center", fontsize=13, fontweight="bold")
for k in range(5):
    ax.add_patch(Arc((9.0, 3.6), 3.4 - k * 0.1, 3.2 - k * 0.5, theta1=200, theta2=340, color=INK, lw=2.4))
    ax.add_patch(Arc((9.0, 3.6), 3.4 - k * 0.1, 3.2 - k * 0.5, theta1=20, theta2=160, color=INK, lw=2.4))
ax.add_patch(Ellipse((9.2, 3.5), 0.9, 1.1, fc=MUSCLE, ec=RED, lw=1.4))
ax.text(9.0, 5.9, "갈비뼈", ha="center", va="center", fontsize=11)
ax.text(10.0, 3.5, "심장", ha="left", va="center", fontsize=10, color=RED)
ax.text(9.0, 0.6, "지키기", ha="center", va="center", fontsize=13, fontweight="bold")
bone(ax, (13.0, 3.6), (17.0, 3.6), w=1.4)
ax.add_patch(Ellipse((15.0, 3.6), 2.6, 0.7, fc="#f2b8a6", ec=RED, lw=1))
for k in range(5):
    ax.add_patch(Circle((14.1 + k * 0.45, 3.6 + 0.12 * (k % 2)), 0.12, fc=RED, ec=RED))
ax.text(15.0, 5.0, "뼈 속 붉은 곳", ha="center", va="center", fontsize=11, color=RED)
ax.text(15.0, 0.6, "피 세포 만들기", ha="center", va="center", fontsize=13, fontweight="bold")
save(fig, "b09-bone.svg")

# 3. 근육은 힘줄로 뼈를 당겨요
fig, ax = canvas(8.0, 3.6, 12.6, 5.8)
bone(ax, (1.0, 2.0), (6.0, 2.0), w=0.5)
bone(ax, (6.4, 2.0), (11.6, 2.0), w=0.5)
ax.add_patch(Circle((6.2, 2.0), 0.35, fc=BONE, ec=INK, lw=1.4))
muscle(ax, (1.6, 3.2), (6.9, 3.0), fat=1.0, fc=RED)
ax.plot([6.9, 7.6], [3.0, 2.3], color=TENDON, lw=3.5)
ax.plot([1.6, 1.4], [3.2, 2.3], color=TENDON, lw=3.5)
arrow(ax, (6.2, 4.4), (3.6, 4.4), color=RED, lw=2.2)
ax.text(4.9, 5.0, "짧아져요", ha="center", va="center", fontsize=12, color=RED, fontweight="bold")
ax.text(4.0, 3.1, "근육", ha="center", va="center", fontsize=11, color="white", fontweight="bold")
ax.text(8.0, 3.0, "힘줄", ha="left", va="center", fontsize=11, color="#8a6d3b", fontweight="bold")
ax.text(3.5, 1.2, "뼈", ha="center", va="center", fontsize=11)
ax.text(9.0, 1.2, "뼈", ha="center", va="center", fontsize=11)
save(fig, "b09-pull.svg")

# 4. 줄은 당길 수만 있어요
fig, ax = canvas(10.0, 3.2, 17.0, 5.4)
def crate(x, y):
    ax.add_patch(Rectangle((x, y), 1.4, 1.4, fc=BONE, ec=INK, lw=1.4))
crate(5.6, 1.6)
ax.plot([1.0, 5.6], [2.3, 2.3], color="#b58b5a", lw=4)
arrow(ax, (1.6, 3.2), (0.4, 3.2), color=INK, lw=2)
arrow(ax, (6.9, 3.4), (5.9, 3.4), color=INK, lw=1.6, ms=12)
ax.text(3.6, 0.7, "당기기", ha="center", va="center", fontsize=13, fontweight="bold")
ax.text(1.0, 4.0, "당겨요", ha="center", va="center", fontsize=10)
ax.text(6.3, 4.2, "끌려와요", ha="center", va="center", fontsize=10)
ax.plot([8.5, 8.5], [0.3, 4.8], color=GREY, lw=1.2, ls="--")
crate(14.8, 1.6)
xs = [10.0, 10.9, 11.8, 12.7, 13.6, 14.8]
ys = [2.3, 3.0, 1.6, 3.0, 1.6, 2.3]
ax.plot(xs, ys, color=RED, lw=4)
arrow(ax, (9.2, 3.6), (10.4, 3.6), color=INK, lw=2)
ax.text(9.6, 4.3, "밀어요", ha="center", va="center", fontsize=10)
ax.text(15.5, 3.6, "그대로", ha="center", va="center", fontsize=10)
ax.text(12.4, 0.7, "밀기", ha="center", va="center", fontsize=13, fontweight="bold", color=RED)
ax.text(12.4, 4.4, "휘어요", ha="center", va="center", fontsize=11, color=RED, fontweight="bold")
save(fig, "b09-rope.svg")

# 5. 짝 근육: 굽히기 / 펴기
fig, ax = canvas(10.0, 5.2, 18.0, 9.0)
arm(ax, 3.0, 7.6, ang=60, bent=True)
ax.text(3.6, -0.5, "굽힐 때", ha="center", va="center", fontsize=13, fontweight="bold")
ax.text(5.4, 6.2, "앞", ha="left", va="center", fontsize=12, color=RED, fontweight="bold")
ax.text(1.4, 6.2, "뒤", ha="right", va="center", fontsize=12, fontweight="bold")
ax.plot([9.0, 9.0], [0.0, 8.4], color=GREY, lw=1.2, ls="--")
arm(ax, 12.0, 7.6, ang=-90, bent=False)
ax.text(13.0, -0.5, "펼 때", ha="center", va="center", fontsize=13, fontweight="bold")
ax.text(14.4, 6.2, "앞", ha="left", va="center", fontsize=12, fontweight="bold")
ax.text(10.4, 6.2, "뒤", ha="right", va="center", fontsize=12, color=RED, fontweight="bold")
ax.set_ylim(-1.0, 8.4)
save(fig, "b09-pair.svg")

# 6. 관절: 뼈와 뼈가 만나 움직이는 곳
fig, ax = canvas(6.4, 5.6, 9.0, 8.0)
J = dict(shoulder_r=(5.0, 5.6), elbow_r=(6.2, 4.4), wrist_r=(7.2, 5.4), shoulder_l=(3.0, 5.6),
         elbow_l=(2.2, 4.2), wrist_l=(2.4, 2.9), hip=(4.0, 3.2), knee_r=(5.0, 1.8), ankle_r=(4.9, 0.4),
         knee_l=(3.2, 1.9), ankle_l=(3.4, 0.4))
ax.add_patch(Circle((4.0, 6.6), 0.55, fc="white", ec=INK, lw=1.6))
segs = [((4.0, 6.05), (4.0, 3.2)), (J["shoulder_l"], J["shoulder_r"]), (J["shoulder_r"], J["elbow_r"]),
        (J["elbow_r"], J["wrist_r"]), (J["shoulder_l"], J["elbow_l"]), (J["elbow_l"], J["wrist_l"]),
        ((3.4, 3.2), (4.6, 3.2)), ((4.6, 3.2), J["knee_r"]), (J["knee_r"], J["ankle_r"]),
        ((3.4, 3.2), J["knee_l"]), (J["knee_l"], J["ankle_l"])]
for a, b in segs:
    ax.plot([a[0], b[0]], [a[1], b[1]], color=INK, lw=3, solid_capstyle="round")
for k in ["shoulder_r", "elbow_r", "wrist_r", "shoulder_l", "elbow_l", "wrist_l", "knee_r", "ankle_r", "knee_l", "ankle_l"]:
    ax.add_patch(Circle(J[k], 0.17, fc=RED, ec=RED, zorder=5))
lab = {"elbow_r": ("팔꿈치", 0.3, -0.1, "left"), "wrist_r": ("손목", 0.3, 0.1, "left"),
       "shoulder_r": ("어깨", 0.3, 0.3, "left"), "knee_r": ("무릎", 0.35, 0.0, "left"),
       "ankle_r": ("발목", 0.35, 0.0, "left")}
for k, (t, dx, dy, ha) in lab.items():
    ax.text(J[k][0] + dx, J[k][1] + dy, t, ha=ha, va="center", fontsize=11, color=RED, fontweight="bold")
save(fig, "b09-joints.svg")

# 7. 팔꿈치는 문 경첩처럼
fig, ax = canvas(10.0, 4.2, 17.0, 7.0)
ax.plot([1.0, 1.0], [0.6, 6.4], color=INK, lw=5)
ax.text(0.6, 6.0, "벽", ha="right", va="center", fontsize=11)
ax.plot([1.0, 7.0], [1.6, 1.6], color="#d8c4a4", lw=7, solid_capstyle="round")
ax.plot([1.0, 6.4], [1.6, 4.6], color="#b58b5a", lw=8, solid_capstyle="round")
ax.add_patch(Circle((1.0, 1.6), 0.34, fc=RED, ec=INK, lw=1.4, zorder=5))
ax.add_patch(Arc((1.0, 1.6), 12.0, 12.0, theta1=4, theta2=26, color=INK, lw=1.4, ls="--"))
ax.text(1.5, 0.8, "경첩", ha="left", va="center", fontsize=12, color=RED, fontweight="bold")
ax.text(4.6, 4.7, "문짝", ha="center", va="center", fontsize=11)
ax.plot([8.7, 8.7], [0.3, 6.6], color=GREY, lw=1.2, ls="--")
bone(ax, (10.6, 6.2), (10.6, 1.8), w=0.5)
bone(ax, (10.6, 1.8), (15.6, 1.8), w=0.42)
ax.plot([10.6, 15.0], [1.8, 4.6], color=INK, lw=1.2, ls=":")
ax.add_patch(Circle((10.6, 1.8), 0.42, fc=RED, ec=INK, lw=1.4, zorder=5))
ax.add_patch(Arc((10.6, 1.8), 10.6, 10.6, theta1=4, theta2=30, color=INK, lw=1.4, ls="--"))
ax.text(10.0, 4.5, "위팔뼈", ha="right", va="center", fontsize=11)
ax.text(13.6, 1.0, "아래팔뼈", ha="center", va="center", fontsize=11)
ax.text(10.9, 0.7, "팔꿈치", ha="left", va="center", fontsize=12, color=RED, fontweight="bold")
save(fig, "b09-hinge.svg")

# 8. 관절 가까이를 조금 당기면 끝은 크게 움직여요
fig, ax = canvas(10.0, 4.2, 18.0, 7.2)
ax.plot([1.0, 1.0], [0.8, 6.6], color=INK, lw=5)
ax.plot([1.0, 7.6], [1.6, 4.4], color="#b58b5a", lw=8, solid_capstyle="round")
ax.add_patch(Circle((1.0, 1.6), 0.32, fc=YEL, ec=INK, lw=1.4, zorder=5))
ax.text(1.6, 0.9, "경첩", ha="left", va="center", fontsize=11)
arrow(ax, (2.4, 1.5), (2.05, 2.4), color=RED, lw=2, ms=12)
ax.text(2.7, 1.5, "조금", ha="left", va="center", fontsize=12, color=RED, fontweight="bold")
ax.add_patch(Arc((1.0, 1.6), 14.4, 14.4, theta1=23, theta2=48, color=INK, lw=1.4, ls="--"))
ax.text(6.4, 6.4, "크게", ha="center", va="center", fontsize=12, fontweight="bold")
ax.text(7.9, 4.3, "문 끝", ha="left", va="center", fontsize=11)
ax.plot([9.4, 9.4], [0.4, 6.8], color=GREY, lw=1.2, ls="--")
bone(ax, (11.4, 6.2), (11.4, 2.4), w=0.5)
bone(ax, (11.4, 2.4), (16.6, 4.6), w=0.42)
ax.add_patch(Circle((11.4, 2.4), 0.42, fc=YEL, ec=INK, lw=1.6, zorder=5))
muscle(ax, (11.9, 5.8), (12.4, 2.95), fat=0.8, fc=RED)
ax.text(10.9, 1.6, "팔꿈치", ha="center", va="center", fontsize=11)
arrow(ax, (12.9, 3.0), (12.6, 3.9), color=RED, lw=2, ms=12)
ax.text(13.1, 2.7, "조금", ha="left", va="center", fontsize=12, color=RED, fontweight="bold")
ax.add_patch(Arc((11.4, 2.4), 11.0, 11.0, theta1=23, theta2=48, color=INK, lw=1.4, ls="--"))
ax.text(15.6, 6.6, "크게", ha="center", va="center", fontsize=12, fontweight="bold")
ax.text(16.9, 4.5, "손", ha="left", va="center", fontsize=11)
ax.set_ylim(-0.1, 7.2)
save(fig, "b09-lever.svg")
