"""Elasticsearch 6편: 용어 사전과 포스팅 목록을 얼마나 줄일 수 있는지 직접 센다.

실행: python lab/es/06_terms_postings.py
1) 낱말 목록을 트라이(앞부분 공유)와 최소 자동자(앞·뒷부분 공유)로 만들어 칸(상태) 수를 센다.
   낱말은 macOS·리눅스에 있는 /usr/share/dict/words(영어 낱말 약 23만 개)를 쓴다.
   최소 자동자는 정렬된 낱말을 차례로 넣으며 같은 꼬리를 합치는 방법(Daciuk 외 2000)으로 만든다.
   Lucene의 FST는 여기에 낱말마다 값(출력)을 붙인 것이다.
2) 포스팅 목록을 그대로 쓴 크기, 차이값(델타)으로 바꾼 크기, 128개씩 묶어 비트를 맞춘 크기를 센다.
"""
import random

WORDS_FILE = "/usr/share/dict/words"


def load_words():
    with open(WORDS_FILE) as f:
        return sorted({w.strip().lower() for w in f if w.strip()})


def trie_nodes(words):
    root = {}
    n = 1
    for w in words:
        node = root
        for ch in w:
            if ch not in node:
                node[ch] = {}
                n += 1
            node = node[ch]
    return n


class State:
    __slots__ = ("edges", "final")

    def __init__(self):
        self.edges = {}
        self.final = False

    def key(self):
        return (self.final, tuple(sorted((c, id(s)) for c, s in self.edges.items())))


def minimal_automaton(words):
    """정렬된 낱말로 최소 비순환 자동자를 만든다. 같은 모양의 꼬리는 하나로 합친다. (시작 칸, 칸 수)를 돌려준다."""
    register = {}
    root = State()
    prev = ""
    unchecked = []          # (부모, 글자, 자식) — 아직 합칠지 안 본 꼬리

    def minimize(down_to):
        while len(unchecked) > down_to:
            parent, ch, child = unchecked.pop()
            k = child.key()
            if k in register:
                parent.edges[ch] = register[k]
            else:
                register[k] = child

    for w in words:
        common = 0
        while common < min(len(w), len(prev)) and w[common] == prev[common]:
            common += 1
        minimize(common)
        node = unchecked[-1][2] if unchecked else root
        for ch in w[common:]:
            nxt = State()
            node.edges[ch] = nxt
            unchecked.append((node, ch, nxt))
            node = nxt
        node.final = True
        prev = w
    minimize(0)
    return root, len(register) + 1


def minimal_automaton_states(words):
    return minimal_automaton(words)[1]


def accepts(root, w):
    node = root
    for ch in w:
        node = node.edges.get(ch)
        if node is None:
            return False
    return node.final


def postings_sizes(doc_ids, block=128):
    raw = 4 * len(doc_ids)                                   # 정수 하나에 4바이트
    deltas = [doc_ids[0]] + [b - a for a, b in zip(doc_ids, doc_ids[1:])]
    vint = sum((d.bit_length() + 6) // 7 or 1 for d in deltas)   # 7비트씩 끊어 쓰는 가변 길이
    packed = 0
    for i in range(0, len(deltas), block):
        chunk = deltas[i:i + block]
        bits = max(d.bit_length() for d in chunk) or 1           # 블록에서 가장 큰 값에 맞춘 비트 수
        packed += 1 + (bits * len(chunk) + 7) // 8               # 비트 수 1바이트 + 값들
    return raw, vint, packed, max(deltas)


if __name__ == "__main__":
    words = load_words()
    chars = sum(len(w) for w in words)
    t = trie_nodes(words)
    root, m = minimal_automaton(words)
    assert all(accepts(root, w) for w in words)                       # 사전의 낱말은 모두 받아들이고
    assert not any(accepts(root, w + "qz") for w in words[::50])       # 사전에 없는 말은 받지 않는다
    print(f"낱말 {len(words):,}개, 글자 {chars:,}개")
    print(f"트라이(앞부분만 공유) 칸: {t:,}개")
    print(f"최소 자동자(앞·뒤 공유) 칸: {m:,}개  → 트라이의 {m / t:.0%}")

    random.seed(6)
    N = 10_000_000
    for name, p in (("흔한 낱말(문서 10개 중 1개꼴)", 0.1), ("드문 낱말(문서 1만 개 중 1개꼴)", 0.0001)):
        k = int(N * p)
        ids = sorted(random.sample(range(N), k))
        raw, vint, packed, mx = postings_sizes(ids)
        print(f"{name}: 문서 {k:,}개, 가장 큰 차이 {mx:,}")
        print(f"   그대로 {raw:,} B / 차이값+가변길이 {vint:,} B / 차이값+128개 묶음 비트 맞춤 {packed:,} B ({packed / raw:.0%})")
