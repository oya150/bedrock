"""12편 '친구의 친구까지 빠짐없이 찾으려면' 실측.

실행: python3 lab/12_bfs_dfs.py
본문 친구 그림(8명)을 두 방법으로 찾아간다.
- 가까운 친구부터(BFS): 찾은 친구를 줄 뒤에 세우고, 줄 맨 앞부터 꺼낸다(collections.deque).
- 한 길로 끝까지(DFS): 찾은 친구를 접시처럼 위에 쌓고, 맨 위부터 꺼낸다(list.append/pop).
이미 찾은 친구는 표시해서 다시 넣지 않는다. 결과는 늘 같다.
"""
from collections import deque

# 누가 누구와 친구인지. 친구 이름은 가나다순으로 적어 두고, 그 순서대로 살펴본다.
FRIENDS = {
    "나": ["민준", "서연"],
    "민준": ["나", "지우", "하준"],
    "서연": ["나", "도윤", "하준"],
    "지우": ["민준", "하은"],
    "하준": ["민준", "서연"],
    "도윤": ["서연", "하은"],
    "하은": ["도윤", "지우", "서준"],
    "서준": ["하은"],
}


def bfs(start):
    seen, line, order, step = {start}, deque([start]), [], {start: 0}
    while line:
        who = line.popleft()
        order.append(who)
        for f in sorted(FRIENDS[who]):
            if f not in seen:
                seen.add(f)
                step[f] = step[who] + 1
                line.append(f)
    return order, step


def dfs_path(start):
    """본문 방식: 지금까지 걸어온 길을 접시처럼 쌓아 둔다. 갈 친구가 없으면 맨 위 접시를 빼고 한 걸음 돌아간다."""
    seen, path, order, log = {start}, [start], [start], []
    while path:
        who = path[-1]
        nxt = next((f for f in sorted(FRIENDS[who]) if f not in seen), None)
        if nxt is None:
            log.append(f"{who}에서 더 갈 곳 없음 → 돌아가기")
            path.pop()
        else:
            seen.add(nxt)
            path.append(nxt)
            order.append(nxt)
            log.append(f"{who} → {nxt}  (접시: {' '.join(path)})")
    return order, log


def dfs(start):
    seen, plate, order = set(), [start], []
    while plate:
        who = plate.pop()
        if who in seen:
            continue
        seen.add(who)
        order.append(who)
        for f in sorted(FRIENDS[who], reverse=True):   # 가나다 순서대로 먼저 가도록 거꾸로 쌓는다
            if f not in seen:
                plate.append(f)
    return order


order, step = bfs("나")
print("## 가까운 친구부터(줄 세우기)")
print("  찾은 순서:", " → ".join(order))
for d in range(max(step.values()) + 1):
    print(f"  {d}단계:", [w for w in order if step[w] == d])
print("\n## 한 길로 끝까지(접시 쌓기)")
print("  찾은 순서:", " → ".join(dfs("나")))
order2, log = dfs_path("나")
print("  걸어온 길 쌓기로 찾은 순서:", " → ".join(order2))
for line in log:
    print("   ", line)
print(f"\n## 친구 수 {len(FRIENDS)}명, 친구 사이(선) {sum(len(v) for v in FRIENDS.values()) // 2}개")
