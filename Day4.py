f = open("resources/day4_input.txt", "r")
lines = f.read().splitlines()
f.close()
data = {}
size = 0
matches = {}
for s in lines:
    s = s.split(":")[1].split("|")
    d = [[int(x) for x in s[0].split()], [int(x) for x in s[1].split()]]
    data[size] = d
    matches[size] = sum([1 if x in d[0] else 0 for x in d[1]])
    size += 1
part1answer = sum(0 if matches[x] == 0 else pow(2, matches[x]-1) for x in matches.keys())
print("Part 1 answer: ", part1answer)
count = {x: 1 for x in data.keys()}
for x in matches.keys():
    for m in range(x+1, min(x+1+matches[x], size)):
        count[m] += count[x]
part2answer = sum(count.values())
print("Part 2 answer: ", part2answer)

