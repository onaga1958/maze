n = list(map(int, input().split()))
print(len(n))
for el in n:
    print(el)
    for i in range(el - 1):
        print(" :"*(el - 1) + " ")
        print("\u2026+"*(el - 1) + "\u2026")
    print(" :"*(el - 1) + " ")

