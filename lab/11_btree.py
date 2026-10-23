"""11편 '창고 속 카드는 어떻게 빨리 찾을까요' 실측.

실행: python3 lab/11_btree.py
1) 카드 500장(1~1,000 사이 서로 다른 수)을 작은 수부터 10장씩 상자 50개에 담아 창고에 둔다.
   책상에는 상자 하나만 둘 수 있고, 다른 상자를 보려면 창고에 다녀와야 한다(한 번 = 창고 다녀오기 1번).
   - 3편 업다운처럼 가운데 카드를 보며 반씩 버리기: 볼 카드가 든 상자를 가져와야 한다.
   - 안내 상자(맨 위 1개 → 가운데 5개 → 카드 상자 50개)를 따라가기.
2) SQLite(파이썬 sqlite3)로 100만 줄 표에서 한 줄 찾기: 색인 없음 vs 색인 있음, 실행 계획과 시간.
결과는 컴퓨터마다 다르다(창고 다녀오기 수는 같다). 문서에 실린 시간은 이 스크립트를 한 번 돌린 결과다.
"""
import os
import platform
import random
import sqlite3
import tempfile
import time

random.seed(11)
cards = sorted(random.sample(range(1, 1001), 500))
BOX = 10
boxes = [cards[i:i + BOX] for i in range(0, len(cards), BOX)]          # 카드 상자 50개
middle = [[b[0] for b in boxes[i:i + BOX]] for i in range(0, len(boxes), BOX)]   # 가운데 안내 상자 5개
top = [m[0] for m in middle]                                          # 맨 위 안내 상자 1개


def updown_trips(x):
    """반씩 버리며 찾기. 보려는 카드가 책상 위 상자에 없으면 창고에 다녀온다."""
    lo, hi, trips, desk = 0, len(cards) - 1, 0, None
    while lo <= hi:
        mid = (lo + hi) // 2
        if mid // BOX != desk:
            desk = mid // BOX
            trips += 1
        if cards[mid] == x:
            return trips
        if cards[mid] < x:
            lo = mid + 1
        else:
            hi = mid - 1
    return trips


def guide_trips(x):
    """안내 상자 따라가기: 맨 위 → 가운데 → 카드 상자. 상자마다 창고 한 번."""
    m = max(i for i, v in enumerate(top) if v <= x) if x >= top[0] else 0
    b = max(i for i, v in enumerate(middle[m]) if v <= x) if x >= middle[m][0] else 0
    return 3, x in boxes[m * BOX + b]


print(f"# {platform.python_implementation()} {platform.python_version()} / {platform.machine()}")
print("\n## 1. 창고 상자")
print(f"  카드 {len(cards)}장, 카드 상자 {len(boxes)}개, 가운데 안내 상자 {len(middle)}개, 맨 위 안내 상자 1개")
print(f"  맨 위 안내 카드: {top}")
print(f"  가운데 안내 상자 1번(0부터 세면 0번): {middle[0]}")
x = cards[123]
print(f"  예: {x} 찾기. 맨 위에서 {max(v for v in top if v <= x)} 이상 → 가운데 상자에서 "
      f"{max(v for v in middle[[i for i, v in enumerate(top) if v <= x][-1]] if v <= x)} 이상 → 카드 상자")
for i, v in enumerate(top):
    if v <= x:
        mi = i
print(f"    그 카드 상자: {boxes[mi * BOX + max(i for i, v in enumerate(middle[mi]) if v <= x)]}")
print(f"  {x} 찾기 창고 다녀오기: 업다운 {updown_trips(x)}번, 안내 상자 {guide_trips(x)[0]}번")
ups = [updown_trips(c) for c in cards]
print(f"  모든 카드: 업다운 가장 많을 때 {max(ups)}번, 평균 {sum(ups) / len(ups):.1f}번 / 안내 상자 늘 3번")

print("\n## 2. SQLite: 100만 줄에서 한 줄 찾기")
path = os.path.join(tempfile.mkdtemp(), "lab11.db")
con = sqlite3.connect(path)
con.execute("CREATE TABLE member(id INTEGER PRIMARY KEY, phone TEXT)")
con.executemany("INSERT INTO member(phone) VALUES (?)",
                ((f"010{random.randrange(10**8):08d}",) for _ in range(1_000_000)))
con.commit()
target = con.execute("SELECT phone FROM member WHERE id = 777777").fetchone()[0]
q = "SELECT id FROM member WHERE phone = ?"


def timed():
    t = time.perf_counter()
    for _ in range(20):
        con.execute(q, (target,)).fetchall()
    return (time.perf_counter() - t) / 20


print("  색인 없음:", con.execute("EXPLAIN QUERY PLAN " + q, (target,)).fetchall()[0][-1],
      f"{timed() * 1e3:,.2f} ms")
con.execute("CREATE INDEX idx_phone ON member(phone)")
print("  색인 있음:", con.execute("EXPLAIN QUERY PLAN " + q, (target,)).fetchall()[0][-1],
      f"{timed() * 1e3:,.3f} ms")
print(f"  페이지 크기 {con.execute('PRAGMA page_size').fetchone()[0]} 바이트, "
      f"파일 {os.path.getsize(path) / 1e6:,.0f} MB, SQLite {sqlite3.sqlite_version}")
con.close()
