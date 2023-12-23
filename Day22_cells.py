import math
import time
NEIGHBORS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

cells = {}

def getHash(positions, prev):
    return str(sorted(list(positions))) + str(sorted(list(prev)))


def getHashEquivalent(positions, prev):
    pos = {(x % width, y % height) for x, y in positions}
    posPrev = {(x % width, y % height) for x, y in prev}
    return str(sorted(list(pos))) + str(sorted(list(posPrev)))


filename = "resources/day21_test_input.txt"
#filename = "resources/day21_input.txt"
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
    #if nx in (0, width-1) or ny in (0, height):
    #    return '.'
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
    for y in range(-height*(scale-1), height*scale):
        s = ""
        for x in range(-width*(scale-1), width*scale):
            if (x, y) in position:
                s += "O"
            else:
                s += infiniteData(x, y)
        print(s)
    print("===============")


def printCells(cells, num = None):
    print("== Cycle: ", num, " =============")
    cy = 0
    for y in range(0, height):
        s = ""
        for cx in range(-1, 1):
            for x in range(width):
                if (cx, cy) in cells and (x, y) in cells[(cx, cy)][0][0]:
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
# cell[x, y] = inside positions + inside prev
# cellhash[hash] = list of cell indexes with this layout
# for each cell hash:
# process cell (pos + prev), result = new cell(pos+prev) and list of spills
# save result in cache
# pass spills to bordering cells results

# step 1 - create cache for pos + prev, check hits


cells[(0, 0)] = (position, prev)

ph = getHashEquivalent(position[0], prev[0])
cellhash = {}
start = time.time()
results = [None]*(cycles+1)
results[0] = 1
results[1] = position[1] - 1
inCycle = None
prevCycleRes = 0
for cycle in range(2, cycles+1):
    reachCells = {}
    for cellCoord in cells:
        cell = cells[cellCoord]
        reach = set()
        position = cell[0]
        prev = cell[1]
        # look in cache. if found, extract list of reaches for this and neighbouring cells
        #ph = getHashEquivalent(position[0], prev[0])
        #if ph in cellhash:
        #    #print("Hit cache!")
        #    (thisReach, spillReaches) = cellhash[ph]
        #else:
        for p in position[0]:
            newReach = findNeighbors(p[0], p[1], prev[0], infiniteSpace)
            reach.update(newReach)
        # process spills
        spillReaches = set()
        thisReach = set()
        for a in reach:
            if a[0] < 0 or a[0] >= width or a[1] < 0 or a[1] >= height:
                spillReaches.add(a)
            else:
                thisReach.add(a)
            #cellhash[ph] = (tuple(thisReach), tuple(spillReaches))
        for r in spillReaches:
            cnx = cellCoord[0] + (-1 if r[0]<0 else 1 if r[0] >= width else 0)
            cny = cellCoord[1] + (-1 if r[1]<0 else 1 if r[1] >= height else 0)
            nc = (r[0]%width, r[1]%height)
            if (cnx, cny) not in cells or nc not in cells[(cnx, cny)][1][0]: # not in other cell's prev set
                if (cnx, cny) in reachCells:
                    reachCells[(cnx, cny)].add(nc)
                else:
                    reachCells[(cnx, cny)] = {nc}
        if len(thisReach) > 0:
            if cellCoord in reachCells:
                reachCells[cellCoord].update(thisReach)
            else:
                reachCells[cellCoord] = thisReach
    # all reaches added, calculate new states
    for cellCoord in cells:
        cell = cells[cellCoord]
        position = cell[0]
        prev = cell[1]
        if cellCoord in reachCells:
            reach = reachCells[cellCoord]
            del reachCells[cellCoord]
        else:
            reach = set()
        newLength = prev[1] + len(reach)
        prev = position
        position = (reach, newLength)
        ph = getHashEquivalent(position[0], prev[0])
        cells[cellCoord] = (position, prev)
    for cellCoord in reachCells:
        position = (reachCells[cellCoord], len(reachCells[cellCoord]))
        prev = (set(), 0)
        cells[cellCoord] = (position, prev)
    res = 0
    for cellCoords in cells:
        res += cells[cellCoords][0][1]
    #for cellCoord in [c for c in cells if c[1] == 0]:
    #    res += cells[cellCoord][0][1]
    #print("Cycle ", cycle, "size ", res)
    results[cycle] = res - prevCycleRes
    prevCycleRes = res
    if cycle > width:
        if inCycle is None:
            if results[cycle-width] == results[cycle]:
                inCycle = 1
        else:
            if results[cycle-width] == results[cycle]:
                inCycle += 1
            else:
                inCycle = None
    if inCycle == width:
        print("line zero cycle found! start ", cycle-inCycle*2+1, "size ", inCycle, ", increment ", sum(results[cycle-inCycle:cycle]))
        exit(0)

    #printSection(position[0], cycle)
    printCells(cells, cycle)
end = time.time()
print("Cell implementation, ", "INFINITE" if infiniteSpace else "LIMITED", " space, ", cycles, " cycles, file=", filename)
res = 0
for cellCoord in [c for c in cells if c[1] == 0 and c[0] <= 0]:
    res += cells[cellCoord][0][1]
print(res)
print("Time elapsed: ", end-start)
