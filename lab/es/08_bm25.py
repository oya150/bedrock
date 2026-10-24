"""Elasticsearch 8편: BM25 점수를 손으로 계산해 ES explain과 맞춰 보고, 문서 모음이 바뀌면 순위가 뒤집히는 걸 본다.

실행: ES=http://localhost:9200 python lab/es/08_bm25.py
ES 7 이후 Lucene BM25(기본 k1=1.2, b=0.75):
  idf = ln(1 + (N - n + 0.5) / (n + 0.5))          N: 그 필드가 있는 문서 수, n: 낱말이 든 문서 수
  tf  = f / (f + k1 * (1 - b + b * dl / avgdl))    f: 문서 안 횟수, dl: 문서 길이(낱말 수), avgdl: 평균 길이
  점수 = 2.2 * idf * tf (검색어 낱말마다 더한다). 2.2는 k1+1로, ES explain에 boost로 찍힌다(7.17, 9.2 확인)
Lucene은 문서 길이를 1바이트로 줄여 저장하므로(norms) dl이 길면 손계산과 조금 달라질 수 있다. 여기서는 짧은 문서만 쓴다.
"""
import json
import math
import os
import urllib.request

ES = os.environ.get("ES", "http://localhost:9200")
K1, B = 1.2, 0.75


def req(method, path, body=None, ndjson=False):
    data = body if isinstance(body, bytes) else (json.dumps(body).encode() if body is not None else None)
    r = urllib.request.Request(ES + path, method=method, data=data,
                               headers={"Content-Type": "application/x-ndjson" if ndjson else "application/json"})
    try:
        return json.load(urllib.request.urlopen(r))
    except urllib.error.HTTPError as e:
        return json.load(e)


def bm25(query, doc, docs):
    N = len(docs)
    avgdl = sum(len(d.split()) for d in docs) / N
    words = doc.split()
    score = 0.0
    for q in query.split():
        n = sum(q in d.split() for d in docs)
        f = words.count(q)
        if f == 0:
            continue
        idf = math.log(1 + (N - n + 0.5) / (n + 0.5))
        tf = f / (f + K1 * (1 - B + B * len(words) / avgdl))
        score += (K1 + 1) * idf * tf
    return score


def run(name, docs, query, shards=1, dfs=False):
    req("DELETE", "/bm25")
    req("PUT", "/bm25", {"settings": {"number_of_shards": shards, "number_of_replicas": 0},
                         "mappings": {"properties": {"body": {"type": "text", "analyzer": "whitespace"}}}})
    lines = []
    for i, d in enumerate(docs):
        lines.append(json.dumps({"index": {"_id": str(i)}}))
        lines.append(json.dumps({"body": d}))
    req("POST", "/bm25/_bulk?refresh=true", ("\n".join(lines) + "\n").encode(), ndjson=True)
    st = "?search_type=dfs_query_then_fetch" if dfs else ""
    res = req("POST", f"/bm25/_search{st}", {"query": {"match": {"body": query}}, "size": 2})
    print(f"== {name} (샤드 {shards}{', dfs' if dfs else ''})")
    for h in res["hits"]["hits"]:
        mine = bm25(query, docs[int(h["_id"])], docs)
        print(f"   문서 {h['_id']} \"{docs[int(h['_id'])]}\": ES {h['_score']:.4f} / 손계산 {mine:.4f}")


A = "환불 환불 문의"          # 환불이 두 번
B_ = "배송 지연 문의"          # 배송이 한 번
query = "환불 배송"

# 모음 1: 환불 이야기가 드물고 배송 이야기가 흔한 곳(배송 문의가 많은 쇼핑몰)
small = [A, B_] + ["배송 언제 와요"] * 30 + ["상품 문의"] * 20
# 모음 2: 같은 두 문서, 그런데 환불 이야기가 흔한 곳(환불 시즌)
big = [A, B_] + ["환불 언제 돼요"] * 30 + ["상품 문의"] * 20

def shards_demo():
    """똑같은 문서 두 개를 서로 다른 샤드에 넣고, 한 샤드에만 환불 문서를 잔뜩 넣는다."""
    req("DELETE", "/bm25s")
    req("PUT", "/bm25s", {"settings": {"number_of_shards": 2, "number_of_replicas": 0},
                          "mappings": {"properties": {"body": {"type": "text", "analyzer": "whitespace"}}}})
    # routing 값 a, b는 샤드 2개짜리 인덱스에서 서로 다른 샤드로 간다(3편의 계산, _cat/shards로 확인)
    lines = [json.dumps({"index": {"_id": "x1", "routing": "a"}}), json.dumps({"body": "환불 문의"}),
             json.dumps({"index": {"_id": "x2", "routing": "b"}}), json.dumps({"body": "환불 문의"})]
    for i in range(40):
        lines += [json.dumps({"index": {"_id": f"f{i}", "routing": "a"}}), json.dumps({"body": "환불 언제 돼요"})]
    for i in range(40):
        lines += [json.dumps({"index": {"_id": f"g{i}", "routing": "b"}}), json.dumps({"body": "상품 문의 드려요"})]
    req("POST", "/bm25s/_bulk?refresh=true", ("\n".join(lines) + "\n").encode(), ndjson=True)
    for dfs in (False, True):
        st = "?search_type=dfs_query_then_fetch" if dfs else ""
        res = req("POST", f"/bm25s/_search{st}",
                  {"query": {"bool": {"must": {"match": {"body": "환불"}}, "filter": {"ids": {"values": ["x1", "x2"]}}}}})
        print(f"== 같은 글 \"환불 문의\" 두 개, 샤드 2개{' + dfs_query_then_fetch' if dfs else ''}")
        for h in res["hits"]["hits"]:
            print(f"   {h['_id']}: {h['_score']:.4f}")


if __name__ == "__main__":
    run("배송이 흔한 모음", small, query)
    run("환불이 흔한 모음", big, query)
    shards_demo()
