"""글마다 단계 딱지를 달고 단계 사이를 잇는 링크를 붙인다.

- 갈래 폴더로 단계를 정한다(STAGE). 과학 분야는 단계가 하나라 딱지를 달지 않는다.
- 다리는 손으로 적지 않고 본문 링크에서 뽑는다. 단계가 다른 두 글이 서로 링크하면
  높은 단계 글 머리에 "먼저 읽으면 좋은 글", 낮은 단계 글 끝에 "다음 단계에서 이어져요"를 단다.
"""
import os
import re

STAGE = {"computer": 1, "algorithms": 2, "elasticsearch": 3}   # 컴퓨터 분야만 단계가 있다
STAGE_NAME = {1: "1단계 · 누구나", 2: "2단계 · 코드 입문", 3: "3단계 · 실제 소프트웨어"}
TOPIC = {"computer": "컴퓨터", "algorithms": "알고리즘", "elasticsearch": "Elasticsearch"}
LINK = re.compile(r"\]\(([^)#\s]+\.md)(?:#[^)]*)?\)")

_bridges = None   # 글 경로 -> {"before": set(), "after": set()}
_titles = {}


def _scan(docs_dir):
    global _bridges
    _bridges = {}
    for topic in STAGE:
        folder = os.path.join(docs_dir, topic)
        for name in sorted(os.listdir(folder)):
            if not re.match(r"\d+-.*\.md$", name):
                continue
            src = f"{topic}/{name}"
            text = open(os.path.join(folder, name), encoding="utf-8").read()
            _titles[src] = text.split("\n", 1)[0].lstrip("# ").strip()
            for target in LINK.findall(text):
                dst = os.path.normpath(os.path.join(topic, target)).replace(os.sep, "/")
                other = dst.split("/")[0]
                if other not in STAGE or STAGE[other] == STAGE[topic] or not re.search(r"/\d+-", dst):
                    continue
                low, high = (src, dst) if STAGE[topic] < STAGE[other] else (dst, src)
                _bridges.setdefault(high, {"before": set(), "after": set()})["before"].add(low)
                _bridges.setdefault(low, {"before": set(), "after": set()})["after"].add(high)


def _link(src_page, dst, stage=False):
    topic = dst.split("/")[0]
    num = int(dst.split("/")[1].split("-")[0])
    rel = os.path.relpath(dst, os.path.dirname(src_page)).replace(os.sep, "/")
    where = f"{STAGE[topic]}단계 · " if stage else ""
    return f"{where}{TOPIC[topic]} {num}편 [{_titles.get(dst, dst)}]({rel})"


def on_page_markdown(markdown, page, config, files):
    src = page.file.src_uri
    topic = src.split("/")[0]
    if topic not in STAGE or "/" not in src:
        return markdown
    if _bridges is None:
        _scan(config["docs_dir"])
    stage = STAGE[topic]
    paths = os.path.relpath("paths.md", topic).replace(os.sep, "/")
    head = [f"[{STAGE_NAME[stage]}]({paths}){{ .level-tag .level-{stage} }}"]
    b = _bridges.get(src, {"before": set(), "after": set()})
    if b["before"]:
        links = " / ".join(_link(src, d) for d in sorted(b["before"]))
        head.append(f"먼저 읽으면 좋은 글: {links}\n{{: .prereq }}")
    first, _, rest = markdown.partition("\n")
    out = first + "\n\n" + "\n\n".join(head) + "\n" + rest
    if b["after"]:
        items = "\n".join(f"- {_link(src, d, stage=True)}" for d in sorted(b["after"]))
        out = out.rstrip() + "\n\n## 다음 단계에서 이어져요\n\n이 편에서 본 것이 다음 단계 글에서 다시 쓰여요.\n\n" + items + "\n"
    return out


def on_pre_build(config):
    global _bridges
    _bridges = None   # serve 중에 글이 바뀌면 다리를 다시 뽑는다
