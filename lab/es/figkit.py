"""Elasticsearch 갈래 그림 공통 도구. 각 lab/fig_esNN.py 가 가져다 쓴다.

글자는 SVG 안에 글자로 남긴다(글꼴 모양을 파일에 넣지 않는다). 보는 쪽 글꼴로 그려진다.
상자는 차분한 색으로, 지금 보는 것만 빨강으로 칠한다.
검토용 PNG가 필요하면 FIG_FMT=png FIG_OUT=<폴더> 로 실행한다.
"""
import os

import matplotlib

FMT = os.environ.get("FIG_FMT", "svg")
matplotlib.use("agg" if FMT == "png" else "svg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Rectangle  # noqa: E402

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
PINK = "#fbe3dc"


def outdir(nn):
    out = os.environ.get("FIG_OUT") or os.path.join(os.path.dirname(__file__), "..", "..", "docs", "elasticsearch", "img", nn)
    os.makedirs(out, exist_ok=True)
    return out


def save(fig, out, name):
    if FMT == "png":
        name = name.replace(".svg", ".png")
    fig.savefig(os.path.join(out, name), bbox_inches="tight", pad_inches=0.25, dpi=110)
    plt.close(fig)


def canvas(w, h, xmax, ymax):
    fig, ax = plt.subplots(figsize=(w, h))
    ax.set_xlim(0, xmax); ax.set_ylim(0, ymax); ax.axis("off")
    return fig, ax


def box(ax, x, y, w, h, fc="white", ec=INK, lw=1.8, round_=True):
    if round_:
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.06", fc=fc, ec=ec, lw=lw))
    else:
        ax.add_patch(Rectangle((x, y), w, h, fc=fc, ec=ec, lw=lw))


def label(ax, x, y, s, fs=12, color="#222", ha="center", va="center", bold=False, **kw):
    ax.text(x, y, s, fontsize=fs, color=color, ha=ha, va=va, fontweight="bold" if bold else "normal", **kw)


def arrow(ax, a, b, color=INK, lw=2, rad=0.0, ms=18, style="-|>"):
    ax.add_patch(FancyArrowPatch(a, b, arrowstyle=style, mutation_scale=ms, color=color, lw=lw,
                                 connectionstyle=f"arc3,rad={rad}"))


def cell(ax, x, y, w, h, s, hot=False, dim=False, fs=12, fc=None):
    """칸 하나. hot=빨강 강조, dim=흐리게."""
    face = fc or (PINK if hot else (LIGHT if dim else NOTE))
    ax.add_patch(Rectangle((x, y), w, h, fc=face, ec=RED if hot else (GREY if dim else INK), lw=2.2 if hot else 1.2))
    ax.text(x + w / 2, y + h / 2, str(s), ha="center", va="center", fontsize=fs,
            color=RED if hot else (GREY if dim else "#222"), fontweight="bold" if hot else "normal")


def cells(ax, x, y, items, w=0.9, h=0.8, gap=0.08, hot=(), dim=(), fs=12):
    for k, s in enumerate(items):
        cell(ax, x + k * (w + gap), y, w, h, s, hot=(k in hot), dim=(k in dim), fs=fs)
    return x + len(items) * (w + gap) - gap


def story(steps, hot, out, name):
    """정리 절 그림: 이 편이 한 말을 결론 문장 칸으로 위에서 아래로 잇는다. hot=빨강 칸 번호(0부터)."""
    n = len(steps)
    H = 1.15
    fig, ax = canvas(9, 0.62 * n + 0.3, 14, n * (H + 0.45) + 0.2)
    for k, s in enumerate(steps):
        y = (n - 1 - k) * (H + 0.45) + 0.25
        on = k == hot
        box(ax, 0.3, y, 13.4, H, fc=PINK if on else NOTE, ec=RED if on else INK)
        label(ax, 0.75, y + H / 2, str(k + 1), fs=11, color=RED if on else INK, bold=True)
        label(ax, 1.4, y + H / 2, s, fs=11.5, ha="left", color=RED if on else "#222")
        if k < n - 1:
            arrow(ax, (7.0, y - 0.03), (7.0, y - 0.42), ms=12)
    save(fig, out, name)


def stage(draw, n, out, prefix, size=(7.2, 3.6), lim=(12, 6)):
    """장면 띠: 같은 무대를 n장 그린다. draw(ax, step)은 step(1부터)에 따라 바뀐 곳만 칠한다. → prefix-1.svg …"""
    for k in range(1, n + 1):
        fig, ax = canvas(*size, *lim)
        ax.add_patch(Rectangle((0, 0), *lim, fill=False, ec="none"))  # 장마다 잘리는 테두리를 같게
        draw(ax, k)
        save(fig, out, f"{prefix}-{k}.svg")


def moral(ax, x, y, s, fs=12.5):
    """장면 띠 마지막 장 아래의 결론 한 줄."""
    label(ax, x, y, s, fs=fs, color=RED, bold=True)


def letters(ax, x, y, word, w=0.55, h=0.6, hot=(), dim=(), blank=(), fs=12):
    """글자 하나를 칸 하나로. blank=글자를 지운 빈칸(점선). 끝 x를 돌려준다."""
    for k, ch in enumerate(word):
        if k in blank:
            ax.add_patch(Rectangle((x + k * w, y), w, h, fc="white", ec=GREY, lw=1.0, ls="--"))
        else:
            cell(ax, x + k * w, y, w, h, ch, hot=k in hot, dim=k in dim, fs=fs)
    return x + len(word) * w


def bits(ax, x, y, s, w=0.32, h=0.5, hot=(), dim=(), fs=9.5):
    """0/1 비트 칸 줄. 끝 x를 돌려준다."""
    return letters(ax, x, y, s, w=w, h=h, hot=hot, dim=dim, fs=fs)
