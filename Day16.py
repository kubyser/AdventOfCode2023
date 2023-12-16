from Utilities import Utilities

def findNearest(data, x, y, d):
    if d == 'R':
        pos = [p[0] for p in data if p[1] == y and p[0] > x and data[p] != '-']
        if len(pos) == 0:
            return None
        return min(pos), y
    elif d == 'L':
        pos = [p[0] for p in data if p[1] == y and p[0] < x and data[p] != '-']
        if len(pos) == 0:
            return None
        return max(pos), y
    elif d == 'D':
        pos = [p[1] for p in data if p[0] == x and p[1] > y and data[p] != '|']
        if len(pos) == 0:
            return None
        return x, min(pos)
    elif d == 'U':
        pos = [p[1] for p in data if p[0] == x and p[1] < y and data[p] != '|']
        if len(pos) == 0:
            return None
        return x, max(pos)
    return None


def addEnergized(energized, x1, y1, x2, y2, d):
    if d == 'R':
        toAdd = [(x, y1) for x in range(x1+1, x2+1)]
        for a in toAdd:
            energized.add(a)
    elif d == 'L':
        toAdd = [(x, y1) for x in range(x2, x1)]
        for a in toAdd:
            energized.add(a)
    elif d == 'D':
        toAdd = [(x1, y) for y in range(y1+1, y2+1)]
        for a in toAdd:
            energized.add(a)
    elif d == 'U':
        toAdd = [(x1, y) for y in range(y2, y1)]
        for a in toAdd:
            energized.add(a)

def addEnergizedToEnd(energized, x1, y1, d):
    if d == 'R':
        toAdd = [(x, y1) for x in range(x1+1, width)]
        for a in toAdd:
            energized.add(a)
    elif d == 'L':
        toAdd = [(x, y1) for x in range(0, x1)]
        for a in toAdd:
            energized.add(a)
    elif d == 'D':
        toAdd = [(x1, y) for y in range(y1+1, height)]
        for a in toAdd:
            energized.add(a)
    elif d == 'U':
        toAdd = [(x1, y) for y in range(0, y1)]
        for a in toAdd:
            energized.add(a)


dirMap = {('R', '-'): ['R'], ('R', '|'): ['U', 'D'], ('R', '/'): ['U'], ('R', '\\'): 'D',
          ('L', '-'): ['L'], ('L', '|'): ['U', 'D'], ('L', '/'): ['D'], ('L', '\\'): 'U',
          ('U', '-'): ['R', 'L'], ('U', '|'): ['U'], ('U', '/'): ['R'], ('U', '\\'): 'L',
          ('D', '-'): ['R', 'L'], ('D', '|'): ['D'], ('D', '/'): ['L'], ('D', '\\'): 'R'}


data, width, height = Utilities.loadMatrixChars("resources/day16_input.txt", ".")
print(data)


def tryFrom(startPos):
    energized = set()
    toProcess = {startPos}
    visited = set()
    while len(toProcess) > 0:
        light = toProcess.pop()
        #print(light, toProcess)
        pos = findNearest(data, light[0], light[1], light[2])
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
#maxRes = tryFrom((-1, 0, 'R'))
# part 2
maxRes = 0

for x in range(width):
    maxRes = max([maxRes, tryFrom((x, -1, 'D'))])
    maxRes = max([maxRes, tryFrom((x, height, 'U'))])
for y in range(height):
    maxRes = max([maxRes, tryFrom((-1, y, 'R'))])
    maxRes = max([maxRes, tryFrom((width, y, 'L'))])

print(maxRes)





