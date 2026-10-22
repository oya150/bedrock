"""컴퓨터 6편 '더 깊이'의 반복 예를 직접 실행해 본다. 실행: python lab/c06_repeat.py"""

position = 0


def move_right():
    global position
    position += 1
    print("오른쪽으로 한 칸 →", position, "번째 칸")


for i in range(5):
    move_right()

print("반복 안의 반복:")
count = 0
for line in range(3):
    for step in range(5):
        count += 1
print("모두", count, "번")
