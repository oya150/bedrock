"""AI 갈래 실측이 함께 쓰는 말뭉치.

커밋 8bf17a2 시점의 bedrock 본문(docs 아래 .md)에서 문장을 뽑는다. 본문이 바뀌어도 숫자가 그대로 나오게 커밋을 고정했다.
"""
import pathlib
import re
import subprocess

REPO = pathlib.Path(__file__).resolve().parents[2]
COMMIT = "8bf17a2"


def git(*args):
    return subprocess.run(["git", "-C", str(REPO), *args], capture_output=True, text=True, check=True).stdout


def sentences():
    out = []
    for p in sorted(git("ls-tree", "-r", "--name-only", COMMIT, "docs").split()):
        if not p.endswith(".md"):
            continue
        text = git("show", f"{COMMIT}:{p}")
        text = re.sub(r"```.*?```", " ", text, flags=re.S)        # 코드 덩어리
        text = re.sub(r"!\[[^\]]*\]\([^)]*\)", " ", text)         # 그림
        text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)      # 링크는 글자만
        text = re.sub(r"\[\^[^\]]*\]:?", " ", text)               # 각주 표시
        for line in text.splitlines():
            line = line.strip()
            if not line or line[0] in "#|!<>-*?{" or line.startswith("    "):
                continue
            line = re.sub(r"[*`_\"“”()]", "", line)
            for s in re.split(r"(?<=[.?!])\s+", line):
                w = s.split()
                if len(w) >= 3 and re.search(r"[가-힣]", s):
                    out.append(w)
    return out
