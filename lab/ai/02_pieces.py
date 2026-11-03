"""AI 2편: 글을 어떤 조각으로 자를지 재 본다.

실행: python lab/ai/02_pieces.py   (필요한 것: pip install kiwipiepy tiktoken)
말뭉치는 corpus.py가 고정한 bedrock 본문이다. 1편처럼 90%로 배우고 10%로 시험한다.
1) 낱말(띄어쓰기 덩어리) 단위: 시험 글 낱말 중 사전에 없는 비율
2) 글자 단위: 사전 크기, 문장 하나가 몇 조각인지
3) 자주 붙어 나오는 두 조각을 하나로 합치기(BPE)를 0~8,000번 했을 때 사전 크기와 조각 수
4) 형태소 분석기(Kiwi)와 BPE가 같은 문장을 어떻게 자르는지
5) 공개 토크나이저(tiktoken)로 같은 뜻 한국어·영어 문장의 조각 수, 사전에 한글이 든 조각이 몇 개인지
"""
import collections
import random
import re

from corpus import sentences

MSGS = ["오늘 점심 뭐 먹지", "오늘 날씨 좋다", "내일 점심 같이 먹자", "오늘 저녁 뭐 먹을까", "날씨 뭐 이래"]
PAIRS = [
    ("오늘 점심 뭐 먹지?", "What should I eat for lunch today?"),
    ("내일 같이 저녁 먹자.", "Let's have dinner together tomorrow."),
    ("오늘 날씨가 정말 좋다.", "The weather is really nice today."),
    ("어제 산 신발이 너무 작아요.", "The shoes I bought yesterday are too small."),
    ("주말에 도서관에서 책을 읽었어요.", "I read a book at the library on the weekend."),
]


def learn(words, merges):
    """BPE: 낱말을 글자로 쪼갠 뒤 가장 자주 붙어 나오는 두 조각을 merges번 합친다."""
    vocab = {tuple(w): c for w, c in words.items()}
    rules = []
    for _ in range(merges):
        pairs = collections.Counter()
        for w, c in vocab.items():
            for a, b in zip(w, w[1:]):
                pairs[a, b] += c
        if not pairs:
            break
        (a, b), _ = max(pairs.items(), key=lambda kv: (kv[1], kv[0]))
        rules.append((a, b))
        new = {}
        for w, c in vocab.items():
            out, i = [], 0
            while i < len(w):
                if i + 1 < len(w) and w[i] == a and w[i + 1] == b:
                    out.append(a + b)
                    i += 2
                else:
                    out.append(w[i])
                    i += 1
            new[tuple(out)] = new.get(tuple(out), 0) + c
        vocab = new
    return rules


def split(word, rules):
    w = list(word)
    for a, b in rules:
        i = 0
        while i + 1 < len(w):
            if w[i] == a and w[i + 1] == b:
                w[i:i + 2] = [a + b]
            else:
                i += 1
    return w


def main():
    sents = sentences()
    rng = random.Random(1)
    rng.shuffle(sents)
    cut = len(sents) * 9 // 10
    train, test = sents[:cut], sents[cut:]
    words = collections.Counter(w for s in train for w in s)
    test_words = [w for s in test for w in s]
    chars = {ch for w in words for ch in w}

    print("[메시지 5개로 합치기 연습]")
    msg_rules = learn(collections.Counter(w for m in MSGS for w in m.split()), 6)
    for i, (a, b) in enumerate(msg_rules, 1):
        print(f"  {i}번째 합치기: {a} + {b}")
    print("  '먹었니' →", split("먹었니", msg_rules), "/ 사전에 없는 글자:", [c for c in "먹었니" if c not in "".join(MSGS)])

    print("\n[낱말 단위]")
    unseen = sum(w not in words for w in test_words)
    print(f"  사전 크기 {len(words):,} / 시험 글 낱말 {len(test_words):,}개 중 사전에 없는 것 {unseen:,}개 ({100 * unseen / len(test_words):.1f}%)")

    print("\n[글자 단위]")
    test_chars = [c for w in test_words for c in w]
    miss = sum(c not in chars for c in test_chars)
    print(f"  사전 크기 {len(chars):,} / 시험 글 글자 {len(test_chars):,}개 중 사전에 없는 것 {miss}개 ({100 * miss / len(test_chars):.2f}%)")
    print(f"  문장 하나 평균 {len(test_chars) / len(test):.1f}조각")

    print("\n[BPE: 합치기 횟수별]")
    rules = learn(words, 8000)
    for m in (0, 500, 2000, 8000):
        r = rules[:m]
        pieces = sum(len(split(w, r)) for w in test_words)
        size = len(chars) + m
        whole = sum(len(split(w, r)) == 1 for w in test_words)
        print(f"  합치기 {m:>5,}번: 사전 크기 {size:,} / 문장 하나 평균 {pieces / len(test):.1f}조각 / 시험 낱말 중 한 조각으로 남은 것 {100 * whole / len(test_words):.1f}%")
    r = rules[:2000]
    examples = [w for w in test_words if w not in words][:12]
    print("  사전에 없던 낱말을 2,000번 규칙으로 자르면:")
    for w in examples:
        print(f"    {w} → {' | '.join(split(w, r))}")

    print("\n[Kiwi 형태소 vs BPE 2,000번]")
    from kiwipiepy import Kiwi
    kiwi = Kiwi()
    for s in ["내일 저녁 뭐 먹었니", "주말에 도서관에서 책을 읽었어요"]:
        morph = [t.form for t in kiwi.tokenize(s)]
        bpe = [p for w in s.split() for p in split(w, r)]
        print(f"  {s}\n    Kiwi: {' | '.join(morph)}\n    BPE : {' | '.join(bpe)}")

    print("\n[공개 토크나이저: 같은 뜻 한국어·영어]")
    import tiktoken
    for name in ("cl100k_base", "o200k_base"):
        enc = tiktoken.get_encoding(name)
        ko = sum(len(enc.encode(k)) for k, _ in PAIRS)
        en = sum(len(enc.encode(e)) for _, e in PAIRS)
        hangul = 0
        for i in range(enc.n_vocab):
            try:
                hangul += bool(re.search("[가-힣]", enc.decode_single_token_bytes(i).decode("utf-8")))
            except (KeyError, UnicodeDecodeError):
                pass
        print(f"  {name}: 한국어 {ko}조각 / 영어 {en}조각 (문장 {len(PAIRS)}쌍) / 사전 {enc.n_vocab:,}개 중 한글 든 조각 {hangul:,}개")
        k, e = PAIRS[0]
        print(f"    {k} → {[enc.decode_single_token_bytes(t).decode('utf-8', 'replace') for t in enc.encode(k)]}")
        print(f"    {e} → {[enc.decode_single_token_bytes(t).decode('utf-8', 'replace') for t in enc.encode(e)]}")


if __name__ == "__main__":
    main()
