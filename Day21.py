import time

NEIGHBORS = [(-1, 0), (1, 0), (0, -1), (0, 1)]
f = open("resources/day21_input.txt", "r")
lines = f.read().splitlines()
f.close()
data = []
startPos = None
for line in lines:
    data.append(list(line))
    if 'S' in line:
        startPos = (line.find('S'), len(data)-1)
        data[len(data)-1][line.find('S')] = '.'
width = len(data[0])
height = len(data)
#print(data)
#print(startPos)


def infiniteData(x, y):
    nx = x % width
    ny = y % height
    return data[ny][nx]

def findNeighbors(x, y, prev):
    res = set()
    for n in NEIGHBORS:
        nx = x+n[0]
        ny = y+n[1]
        #if nx < 0 or nx >= width or ny < 0 or ny >= height:
        #    continue
#        if data[ny][nx] == '#' or (nx, ny) in prev:
        if infiniteData(nx, ny) == '#' or (nx, ny) in prev:
            continue
        res.add((nx, ny))
    return res


cycles = 500 # 26501365
results = [None] * (cycles+1)
resSums = [None] * (cycles+1)
resValues = [None] * (cycles+1)


prev = ({startPos}, 1)
neighbors = findNeighbors(startPos[0], startPos[1], {})
position = (set(neighbors), len(neighbors))
results[0] = 1
results[1] = position[1]
start = time.time()
inCycle = None
print(width, height)
for cycle in range(2, cycles+1):
    reach = set()
    for p in position[0]:
        newReach = findNeighbors(p[0], p[1], prev[0])
        reach.update(newReach)
    newLength = prev[1] + len(reach)
    prev = position
    position = (reach, newLength)
    res = newLength - prev[1]
    resValues[cycle] = newLength
    results[cycle] = res
    #print("Cycle ", cycle, " result ", newLength, " diff ", res)
    if cycle > width*2:
        thisSum = sum(results[cycle - width + 1: cycle+1])
        prevSum = sum(results[cycle - width*2 + 1: cycle - width + 1])
        resSums[cycle] = thisSum - prevSum
        #print("Cycle ", cycle, " result ", newLength, " diff ", res, " cyclediff ", resSums[cycle])

c1 = width*2
deltas = results[c1:c1+width]
deltaInc = [results[c1+x] - results[c1+x - width] for x in range(width)]
print(deltas)
print(deltaInc)

c = c1
result = resValues[c1]
while c < 26501365:
    c += 1
    inc = deltas[(c - c1) % width]
    bigDelta = deltaInc[(c - c1) % width]
    mult = int((c-c1) / width)
    bigInc = bigDelta * mult
    result += inc + bigInc
print(c, result)





end = time.time()
print(position[1])
print("Time elapsed: ", end-start)
exit(0)

for length in range(1, int(cycle / width)):
    if lengthCycle[length] is None:
        if results[cycle - width * length] == results[cycle]:
            lengthCycle[length] = 1
    else:
        if results[cycles - width * length] == results[cycle]:
            lengthCycle[length] += 1
        else:
            lengthCycle[length] = None
    if lengthCycle[length] == width * length:
        print("Cycle found! length=", width*length, ", start=", cycle-width*length*2+1, "increment=", sum(results[cycle - width*length+1:cycle+1]))
