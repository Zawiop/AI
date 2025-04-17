a, b = [2,3], [2,3]
a.append([4,5])
b.append([4,5])
a[2] = b[2] = b
a = [*a]
a[1] = 6
print (
    a[2] == b[2]
)
