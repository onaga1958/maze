VWALL = ":"
HWALL = "."
ROOM = " "
CROSS = "+"
n = list(map(int, input().split()))
print(len(n))
for el in n:
    print(el)
    for i in range(el - 1):
        print((ROOM + VWALL)*(el - 1) + ROOM)
        print((HWALL + CROSS)*(el - 1) + HWALL)
    print((ROOM + VWALL)*(el - 1) + ROOM)

