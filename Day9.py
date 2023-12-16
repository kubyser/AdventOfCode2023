f = open("resources/day9_input.txt", "r")
lines = f.read().splitlines()
f.close()
res = 0
for line in lines:
    seq = [[int(x) for x in line.split()]]
    while len([x for x in seq[-1] if x != 0]) > 0:
        seq.append([seq[-1][x+1] - seq[-1][x] for x in range(len(seq[-1])-1)])
    seq[-1].append(0)
    print("Seq:")
    print(seq)
    for i in range(len(seq)-2, -1, -1):
        new = seq[i][0] - seq[i+1][-1]
        seq[i].append(new)
        print(seq[i], new)
    res += seq[0][-1]
print("Result: ", res)



