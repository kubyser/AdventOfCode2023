import time

NEIGHBORS = [(-1, 0), (1, 0), (0, -1), (0, 1)]
fileName = "resources/day21_input.txt"
f = open(fileName, "r")
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

def findNeighbors(x, y, infiniteSpace):
    res = set()
    for n in NEIGHBORS:
        nx = x+n[0]
        ny = y+n[1]
        if not infiniteSpace and (nx < 0 or nx >= width or ny < 0 or ny >= height):
            continue
        #        if data[ny][nx] == '#' or (nx, ny) in prev:
        if infiniteData(nx, ny) == '#':
            continue
        res.add((nx, ny))
    return res

infiniteSpace = False
cycles = 1000 # 26501365
position = {startPos}
start = time.time()
for cycle in range(cycles):
    reach = set()
    for p in position:
        newReach = findNeighbors(p[0], p[1], infiniteSpace)
        reach.update(newReach)
    position = reach
end = time.time()
print("Straightforward implementation, ", "INFINITE" if infiniteSpace else "LIMITED", " space, ", cycles, " cycles, file=", fileName)
print(len(position))
print("Time elapsed: ", end-start)
