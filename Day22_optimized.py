import math
import time

NEIGHBORS = [(-1, 0), (1, 0), (0, -1), (0, 1)]
filename = "resources/day21_test_input.txt"
f = open(filename, "r")
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

def getCellNum(x, y):
    cellX = math.floor(x / width)
    cellY = math.floor(y / height)


def findNeighbors(x, y, prev, infiniteSpace):
    res = set()
    for n in NEIGHBORS:
        nx = x+n[0]
        ny = y+n[1]
        if not infiniteSpace and (nx < 0 or nx >= width or ny < 0 or ny >= height):
            continue
        #       if data[ny][nx] == '#' or (nx, ny) in prev:
        if infiniteData(nx, ny) == '#' or (nx, ny) in prev:
            continue
        res.add((nx, ny))
    return res

def printSection(position, num = None):
    print("== Cycle: ", num, " =============")
    scale = 2
    for y in range(-2 * height, 2*height):
        s = ""
        for x in range(-5 * width, width):
            if (x, y) in position:
                s += "O"
            else:
                s += infiniteData(x, y)
        print(s)
    print("===============")



infiniteSpace = True
cycles = 100 # 26501365
prev = ({startPos}, 1)
neighbors = findNeighbors(startPos[0], startPos[1], {}, infiniteSpace)
position = (set(neighbors), len(neighbors))
start = time.time()
for cycle in range(1, cycles):
    reach = set()
    for p in position[0]:
        newReach = findNeighbors(p[0], p[1], prev[0], infiniteSpace)
        reach.update(newReach)
    newLength = prev[1] + len(reach)
    prev = position
    position = (reach, newLength)
    print("Cycle ", cycle, "size ", position[1])
    printSection(position[0], cycle)
end = time.time()
print("Optimized implementation, ", "INFINITE" if infiniteSpace else "LIMITED", " space, ", cycles, " cycles, file=", filename)
print(position[1])
print("Time elapsed: ", end-start)
