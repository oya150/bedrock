"""AI 1편: 앞 낱말 몇 개를 보고 다음 낱말을 고르는 세기 모델을 재 본다.

실행: python lab/ai/01_ngram.py
말뭉치는 corpus.py가 고정한 bedrock 본문이다. 낱말은 띄어쓰기로 자른 덩어리(어절)다.
1) 앞 낱말 1~4개로 다음 낱말 횟수표를 만들고 문장을 뽑아 본다
2) 처음 보는 글(시험 글)에서 "앞 낱말 묶음을 표에서 한 번도 못 본" 비율을 잰다
3) 뽑은 문장이 말뭉치 문장을 그대로 베낀 비율을 잰다
4) 배우는 글을 10%~100%로 바꿔 가며 앞 낱말 2개 묶음을 처음 보는 비율을 잰다
"""
import collections
import random

from corpus import sentences


def table(sents, n):
    t = collections.defaultdict(collections.Counter)
    for w in sents:
        w = ["<처음>"] * n + w + ["<끝>"]
        for i in range(n, len(w)):
            t[tuple(w[i - n:i])][w[i]] += 1
    return t


def generate(t, n, rng, limit=25):
    ctx = ["<처음>"] * n
    out = []
    while len(out) < limit:
        c = t.get(tuple(ctx[-n:]))
        if not c:
            out.append("<막힘>")
            break
        nxt = rng.choices(list(c), weights=c.values())[0]
        if nxt == "<끝>":
            break
        out.append(nxt)
        ctx.append(nxt)
    return out


def main():
    sents = sentences()
    rng = random.Random(1)
    rng.shuffle(sents)
    cut = len(sents) * 9 // 10
    train, test = sents[:cut], sents[cut:]
    words = sum(len(s) for s in train)
    print(f"말뭉치: 문장 {len(sents):,}개, 배우는 쪽 낱말 {words:,}개, 서로 다른 낱말 {len({x for s in train for x in s}):,}개")
    train_set = {" ".join(s) for s in train}
    for n in (1, 2, 3, 4):
        t = table(train, n)
        seen = total = 0
        for w in test:
            w = ["<처음>"] * n + w
            for i in range(n, len(w)):
                total += 1
                seen += tuple(w[i - n:i]) in t
        gen_rng = random.Random(7)
        copies = stuck = 0
        samples = []
        for k in range(200):
            g = generate(t, n, gen_rng)
            if g and g[-1] == "<막힘>":
                stuck += 1
            if " ".join(g) in train_set:
                copies += 1
            if k < 3:
                samples.append(" ".join(g))
        print(f"\n앞 낱말 {n}개: 표의 줄 {len(t):,}개 / 시험 글에서 앞 묶음을 처음 보는 비율 {100 - 100 * seen / total:.1f}%"
              f" / 뽑은 200문장 중 말뭉치 문장 그대로 {copies}개")
        for s in samples:
            print("  ·", s)

    print("\n배우는 글 양을 바꾸면 (앞 낱말 2개)")
    for frac in (0.1, 0.25, 0.5, 1.0):
        sub = train[:int(len(train) * frac)]
        t = table(sub, 2)
        seen = total = 0
        for w in test:
            w = ["<처음>"] * 2 + w
            for i in range(2, len(w)):
                total += 1
                seen += tuple(w[i - 2:i]) in t
        print(f"  낱말 {sum(len(x) for x in sub):,}개: 처음 보는 비율 {100 - 100 * seen / total:.1f}%")


if __name__ == "__main__":
    main()
