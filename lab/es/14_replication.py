"""Elasticsearch 14편: 시퀀스 번호와 체크포인트로 복제본을 맞추는 일, 과반수로 마스터를 뽑는 일을 흉내 낸다.

실행: python lab/es/14_replication.py
1) 주 샤드 하나와 복제본 둘. 쓰기마다 주 샤드가 시퀀스 번호를 매겨 복제본에 보낸다.
   복제본마다 '여기까지는 빈틈없이 받았다'(로컬 체크포인트)를 두고, 모두의 최솟값이 글로벌 체크포인트다.
2) 주 샤드가 죽으면 복제본 하나가 주 샤드가 된다. 글로벌 체크포인트 뒤쪽만 맞추면 된다.
3) 마스터 후보 3개와 5개에서 몇 개가 죽어도 마스터를 뽑을 수 있는지, 둘로 갈라지면 어느 쪽이 뽑는지 센다.
"""
import random

random.seed(14)


class Copy:
    def __init__(self, name):
        self.name, self.ops = name, {}

    def apply(self, seq, doc):
        self.ops[seq] = doc

    def local_checkpoint(self):
        # 0부터 빈틈없이 받은 마지막 번호
        n = -1
        while n + 1 in self.ops:
            n += 1
        return n


def replication():
    primary, r1, r2 = Copy("주 샤드"), Copy("복제본 1"), Copy("복제본 2")
    copies = [primary, r1, r2]
    for seq in range(10):
        doc = f"주문{seq}"
        primary.apply(seq, doc)
        # 네트워크가 늦어 복제본에 순서가 뒤섞여 도착하거나 아직 안 간 것도 있다
        if seq < 8 or seq == 9:
            r1.apply(seq, doc)
        if seq < 6:
            r2.apply(seq, doc)
    print("1) 쓰기 10건(시퀀스 번호 0~9) 뒤")
    for c in copies:
        print(f"  {c.name}: 받은 번호 {sorted(c.ops)} → 로컬 체크포인트 {c.local_checkpoint()}")
    gcp = min(c.local_checkpoint() for c in copies)
    print(f"  글로벌 체크포인트 = 최솟값 {gcp} (0~{gcp}는 세 곳 모두에 있음)")

    print("2) 주 샤드가 죽고 복제본 1이 새 주 샤드가 됨")
    new_primary = r1
    top = max(new_primary.ops)
    gaps = [s for s in range(gcp + 1, top + 1) if s not in new_primary.ops]
    for s in gaps:
        new_primary.apply(s, "빈 작업")          # 새 주 샤드는 빈 번호를 빈 작업(no-op)으로 채운다
    behind = list(range(gcp + 1, top + 1))
    print(f"  새 주 샤드의 빈 번호 {gaps}는 빈 작업으로 채움")
    print(f"  맞춰 볼 구간: 글로벌 체크포인트 {gcp} 뒤의 번호 {behind}만 복제본 2에 다시 보냄")
    for s in behind:
        r2.apply(s, new_primary.ops[s])
    print(f"  복제본 2: 로컬 체크포인트 {r2.local_checkpoint()} (0~{gcp}는 다시 보내지 않음)")
    print("  번호 6 이후 쓰기는 복제본 2에 닿기 전이라 클라이언트가 성공 응답을 받지 못했던 것들")


def quorum():
    print("3) 마스터 후보 수와 버틸 수 있는 고장")
    for n in (1, 2, 3, 4, 5):
        need = n // 2 + 1
        print(f"  후보 {n}개: 과반 {need}표 필요 → {n - need}개까지 죽어도 마스터를 뽑음")
    print("  후보 5개가 네트워크로 3 대 2로 갈라지면")
    for side in (3, 2):
        ok = side >= 5 // 2 + 1
        print(f"    {side}개 쪽: {'마스터를 뽑음' if ok else '과반이 안 돼 뽑지 못함'}")


if __name__ == "__main__":
    replication()
    quorum()
