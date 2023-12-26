import functools
import platform
import queue
import time

DIRECTIONS = {'>': [(1, 0)], '<': [(-1, 0)], '^': [(0, -1)], 'v': [(0, 1)],  '.': [(-1, 0), (1, 0), (0, -1), (0, 1)]}

f = open("resources/day23_test_input.txt", "r")
lines = f.read().splitlines()
f.close()
data = []
for line in lines:
    data.append(list(line))
width = len(data[0])
height = len(data)
#print(data)


def findNext(pos, prevpos, visited = None):
    res = []
    #for d in DIRECTIONS[data[pos[1]][pos[0]]]:
    for d in DIRECTIONS['.']:
        nx = pos[0] + d[0]
        ny = pos[1] + d[1]
        if not 0 <= nx < width or not 0 <= ny < height:
            continue
        if (nx, ny) != prevpos and data[ny][nx] != '#' and (visited is None or (nx, ny) not in visited):
            res.append((nx, ny))
    return res


@functools.lru_cache(maxsize=None)
def findTunnelEnd(pos, prev):
    length = 0
    while True:
        neighbors = findNext(pos, prev)
        if len(neighbors) == 1:
            length += 1
            prev = pos
            pos = neighbors[0]
            continue
        return pos, length


graph = {}

def scanMap(pos):
    graph[pos] = []
    neighbors = findNext(pos, None)
    for n in neighbors:
        fin, length = findTunnelEnd(n, pos)
        graph[pos].append((fin, length+1))
        if fin not in graph:
            scanMap(fin)


def hashOfSet(s):
    ns = sorted(s)
    return str(ns)

def printMap(path):
    for y in range(height):
        s = ""
        for x in range(width):
            if (x, y) in path:
                s += 'O'
            else:
                s += data[y][x]
        print(s)

#print(platform.python_version())
#exit(0)


start = time.time()
startPos = data[0].index('.'), 0
finishPos = data[height-1].index('.'), height-1

scanMap(startPos)


path = (startPos, set(), 0)
pathsCache = {}
maxPath = 0
pathsQueue = queue.LifoQueue()
pathsQueue.put(path)
#tunnelsCache = {}
while not pathsQueue.empty():
    #print(pathsQueue.qsize())
    path = pathsQueue.get()
    pos = path[0]
    visited = path[1]
    length = path[2]
    hashPos = (pos, hashOfSet(visited))
    if hashPos in pathsCache:
        knownLength = pathsCache[hashPos]
        if knownLength >= length:
            continue
    pathsCache[hashPos] = length
    #if (pos, prevPos) in tunnelsCache:
    #    (pos, prevPos, lengthIncrement) = tunnelsCache[(pos, prevPos)]
    #    newLength += lengthIncrement
    #else:
    reachable = graph[pos]


    (pos, prevPos, lengthIncrement) = findTunnelEnd(pos, prevPos)
    if pos in visited:
        continue
    #    tunnelsCache[(pos, prevPos)] = (posNew, prevPosNew, lengthIncrement)
    #    pos = posNew
    #    prevPos = prevPosNew
    length += lengthIncrement
    if pos == finishPos:
        if length > maxPath:
            maxPath = length
            print("Path found: ", length)
        continue
    neighbors = findNext(pos, prevPos, visited)
    prevPos = pos
    if len(neighbors) == 0:
        hitBlock = True
        continue
    visited.add(pos)
    for index, n in enumerate(neighbors):
        if index > 0:
            newPath = (n, prevPos, set(visited), length+1)
        else:
            newPath = (n, prevPos, visited, length+1)
        pathsQueue.put(newPath)
end = time.time()
print("Max length: ", maxPath)
print("Elapsed time: ", end-start)





