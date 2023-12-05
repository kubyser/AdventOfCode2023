#f = open("resources/day5_test_input.txt", "r")
f = open("resources/day5_input.txt", "r")
lines = f.read().splitlines()
f.close()
seeds = [int(x) for x in lines[0].split(":")[1].split()]
maps = []


def parseMap(seed, mapNum):
    shift = 0
    starts = [x[0] for x in maps[mapNum] if x[0] > seed]
    nextRange = None if len(starts) == 0 else min(starts)
    for m in maps[mapNum]:
        if seed in range(m[0], m[1]):
            nextRange = m[1]
            shift = m[2]
            break
    newShift = 0
    if mapNum < len(maps)-1:
        newShift, newRange = parseMap(seed + shift, mapNum+1)
        nextRange = min([nextRange, newRange - shift]) if nextRange is not None and newRange is not None \
            else newRange - shift if newRange is not None else nextRange
    return shift + newShift, nextRange


for line in lines[2:]:
    if len(line) == 0:
        continue
    if line.find("map:") > 0:
        maps.append([])
        continue
    mapRaw = [int(x) for x in line.split()]
    maps[len(maps)-1].append([mapRaw[1], mapRaw[1] + mapRaw[2], mapRaw[0] - mapRaw[1]])
# part 1
values = [s + parseMap(s, 0)[0] for s in seeds]
print("Part 1 minimum ", min(values))
# part 1
values = []
pairs = list(zip(seeds[::2], seeds[1::2]))
for p in pairs:
    seed = p[0]
    while seed < p[0] + p[1]:
        shift, nextRange = parseMap(seed, 0)
        values.append(seed + shift)
        seed = nextRange if nextRange is not None else seed+1
print("Part 2 minimum ", min(values))
