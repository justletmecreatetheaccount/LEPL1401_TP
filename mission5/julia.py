def iterate(z, c, max, r):
    z = z
    i = 0
    while abs(z) < r and i < max:
        z = z ** 2
        z += c
        i += 1
    print(i == max)

iterate(0, -1, 1000, 5)