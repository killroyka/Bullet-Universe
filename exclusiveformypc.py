a = [[1, 2, 3],
     [1, 2, 3],
     [1, 2, 3]]
b = []
for x in range(len(a)):
    b.append([])
    for y in range(len(a[x])):
        b[x].append(a[x][y])
for x in range(len(a)):
    for y in range(len(a[x])):
        b[x][y] += 1
print(a)