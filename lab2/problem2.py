sequence = input("Enter sequence: ")

gcCount = 0
atCount = 0
cCount = 0
gCount = 0
aCount = 0
tCount = 0

for x in sequence:
    if x == 'G' or x == 'g':
        gcCount += 1
        gCount += 1
    elif x == 'C' or x == 'c':
        gcCount += 1
        cCount += 1
    elif x == 'A' or x == 'a':
        atCount += 1
        aCount += 1
    elif x == 'T' or x == 't':
        atCount += 1
        tCount += 1

tm = (4 * gcCount) + (2 * atCount)

print("Melting Temperature (Tm):", tm, "C")
print("Frequency of G:", gCount)
print("Frequency of C:", cCount)
print("Frequency of A:", aCount)
print("Frequency of T:", tCount)
