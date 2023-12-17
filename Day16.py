import time

from Utilities import Utilities

ROWS = 0
COLUMNS = 1
DOWN = 0+1j
UP = 0-1j
LEFT = -1+0j
RIGHT = 1+0j

def ptSetToCrPtSet(inSet):
    crPtSet = [{}, {}]
    for p in inSet:
        x = p[0]
        y = p[1]
        val = inSet[p]
        if val != '-':
            if y in crPtSet[ROWS]:
                crPtSet[ROWS][y][x] = val
            else:
                crPtSet[ROWS][y] = {x: val}
        if val != '|':
            if x in crPtSet[COLUMNS]:
                crPtSet[COLUMNS][x][y] = val
            else:
                crPtSet[COLUMNS][x] = {y: val}
    return crPtSet


def findNearest(crPtData, x, y, d):
    if d == RIGHT:
        pos = [p for p in crPtData[ROWS][y] if p > x and crPtData[ROWS][y][p] != '-']
        if len(pos) == 0:
            return None
        return min(pos), y
    elif d == LEFT:
        pos = [p for p in crPtData[ROWS][y] if p < x and crPtData[ROWS][y][p] != '-']
        if len(pos) == 0:
            return None
        return max(pos), y
    elif d == DOWN:
        pos = [p for p in crPtData[COLUMNS][x] if p > y and crPtData[COLUMNS][x][p] != '|']
        if len(pos) == 0:
            return None
        return x, min(pos)
    elif d == UP:
        pos = [p for p in crPtData[COLUMNS][x] if p < y and crPtData[COLUMNS][x][p] != '|']
        if len(pos) == 0:
            return None
        return x, max(pos)
    return None


def addEnergized(energized, x1, y1, x2, y2, d):
    if d == RIGHT:
        toAdd = [(x, y1) for x in range(x1+1, x2+1)]
        for a in toAdd:
            energized.add(a)
    elif d == LEFT:
        toAdd = [(x, y1) for x in range(x2, x1)]
        for a in toAdd:
            energized.add(a)
    elif d == DOWN:
        toAdd = [(x1, y) for y in range(y1+1, y2+1)]
        for a in toAdd:
            energized.add(a)
    elif d == UP:
        toAdd = [(x1, y) for y in range(y2, y1)]
        for a in toAdd:
            energized.add(a)

def addEnergizedToEnd(energized, x1, y1, d):
    if d == RIGHT:
        toAdd = [(x, y1) for x in range(x1+1, width)]
        for a in toAdd:
            energized.add(a)
    elif d == LEFT:
        toAdd = [(x, y1) for x in range(0, x1)]
        for a in toAdd:
            energized.add(a)
    elif d == DOWN:
        toAdd = [(x1, y) for y in range(y1+1, height)]
        for a in toAdd:
            energized.add(a)
    elif d == UP:
        toAdd = [(x1, y) for y in range(0, y1)]
        for a in toAdd:
            energized.add(a)


dirMap = {(RIGHT, '-'): [RIGHT], (RIGHT, '|'): [UP, DOWN], (RIGHT, '/'): [UP], (RIGHT, '\\'): [DOWN],
          (LEFT, '-'): [LEFT], (LEFT, '|'): [UP, DOWN], (LEFT, '/'): [DOWN], (LEFT, '\\'): [UP],
          (UP, '-'): [RIGHT, LEFT], (UP, '|'): [UP], (UP, '/'): [RIGHT], (UP, '\\'): [LEFT],
          (DOWN, '-'): [RIGHT, LEFT], (DOWN, '|'): [DOWN], (DOWN, '/'): [LEFT], (DOWN, '\\'): [RIGHT]}


data, width, height = Utilities.loadMatrixChars("resources/day16_input.txt", ".")
crPtData = ptSetToCrPtSet(data)
#print(data)


def tryFrom(startPos):
    energized = set()
    toProcess = {startPos}
    visited = set()
    while len(toProcess) > 0:
        light = toProcess.pop()
        #print(light, toProcess)
        pos = findNearest(crPtData, light[0], light[1], light[2])
        if pos is None:
            addEnergizedToEnd(energized, light[0], light[1], light[2])
        else:
            addEnergized(energized, light[0], light[1], pos[0], pos[1], light[2])
        #print(energized)
            if (pos[0], pos[1], light[2]) not in visited:
                visited.add((pos[0], pos[1], light[2]))
                if (pos[0], pos[1]) in data:
                    tile = data[pos[0], pos[1]]
                    newDirs = dirMap[(light[2], tile)]
                    for a in newDirs:
                        toProcess.add((pos[0], pos[1], a))
    return len(energized)

# part1
#maxRes = tryFrom((-1, 0, RIGHT))
#print(maxRes)
#exit(0)

# part 2
maxRes = 0

startTime = time.time()
for x in range(width):
    maxRes = max([maxRes, tryFrom((x, -1, DOWN))])
    maxRes = max([maxRes, tryFrom((x, height, UP))])
for y in range(height):
    maxRes = max([maxRes, tryFrom((-1, y, RIGHT))])
    maxRes = max([maxRes, tryFrom((width, y, LEFT))])
endTime = time.time()

print("Result: ", maxRes)
print("Elapsed time: ", endTime - startTime)





