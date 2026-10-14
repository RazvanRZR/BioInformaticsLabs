sequence = input("Enter sequence: ")

gcCount = 0
atCount = 0

for x in sequence:
    if x == 'G' or x == 'g' or x == 'C' or x == 'c':
        gcCount += 1
    elif x == 'A' or x == 'a' or x == 'T' or x == 't':
        atCount += 1

tm = (4 * gcCount) + (2 * atCount)

print("Melting Temperature (Tm):", tm, "C")
