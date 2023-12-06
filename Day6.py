import math

f = open("resources/day6_input.txt", "r")
lines = f.read().splitlines()
f.close()
part1data = zip([int(x) for x in lines[0].split(":")[1].split()], [int(x) for x in lines[1].split(":")[1].split()])
part2data = [[int(lines[0].split(":")[1].replace(" ", "")), int(lines[1].split(":")[1].replace(" ", ""))]]
# (t-x)*x = d -> x^2 - tx + d = 0   x = (t +- sqrt (t^2 - 4d))/2

def solve(data):
    res = 1
    for p in data:
        minTime = int(math.ceil((p[0] - math.sqrt(p[0]*p[0] - 4 * (p[1] + 1))) / 2))
        maxTime = int(math.floor((p[0] + math.sqrt(p[0]*p[0] - 4 * (p[1] + 1))) / 2))
        res *= maxTime - minTime + 1
    return res

print("Part 1 result: ", solve(part1data))
print("Part 2 result: ", solve(part2data))

