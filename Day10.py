from Utilities import Utilities

connectionsMap = {"-": [(-1, 0), (1, 0)], "|": [(0, -1), (0, 1)], "F": [(1, 0), (0, 1)], "J": [(-1, 0), (0, -1)],
        "7": [(-1, 0), (0, 1)], "L": [(1, 0), (0, -1)]}

data, width, height = Utilities.loadMatrixChars("resources/day10_input.txt")
startPos = (0, 0)
path = []

def getConnected(x, y):
    c = data[(x, y)]
    if c == ".":
        return []
    cm = [(x+nx, y+ny) for (nx, ny) in connectionsMap[c]]
    return cm

def getStartConnections(x, y):
    conn = []
    for py in range(y-1, y+2):
        if py < 0 or py >= height:
            continue
        for px in range(x-1, x+2):
            if px < 0 or px >= width or px == x and py == y:
                continue
            c = getConnected(px, py)
            if (x, y) in c:
                conn.append((px, py))
    return conn

def calculateDistance(startPos):
    conn = getStartConnections(startPos[0], startPos[1])
    print(conn)
    dist = 1
    pos = conn[0]
    path.append(startPos)
    prevPos = startPos
    while pos != startPos:
        path.append(pos)
        conn = [p for p in getConnected(pos[0], pos[1]) if p != prevPos]
        prevPos = pos
        pos = conn[0]
        path.append(pos)
        dist += 1
    print("Distance: ", dist, dist/2)

stop = False
for y in range(height):
    if stop:
        break
    for x in range(width):
        if data[(x, y)] == 'S':
            startPos = (x, y)
            stop = True
            break
print(data, startPos)
calculateDistance(startPos)

insideArea = 0
insideList = []

def printPathInsideOut():
    for y in range(height):
        s = ''
        for x in range(width):
            s += data[(x, y)] if (x, y) in path else 'x' if (x, y) in insideList else '.'
        print(s)


conn = getStartConnections(startPos[0], startPos[1])
offsetsStart = [(p[0]-startPos[0], p[1]-startPos[1]) for p in conn]
realS = [x for x in connectionsMap.keys() if offsetsStart[0] in connectionsMap[x] and offsetsStart[1] in connectionsMap[x]][0]
print(realS)
data[startPos] = realS
printPathInsideOut()

for y in range(height):
    inside = False
    flipChar = ''
    for x in range(width):
        if (x, y) in path:
            c = data[(x, y)]
            if c == '|':
                inside = not inside
            elif c == 'L':
                flipChar = '7'
            elif c == 'F':
                flipChar = 'J'
            elif c == '7' or c == 'J':
                inside = not inside if c == flipChar else inside
        else:
            if inside:
                insideArea += 1
                insideList.append((x, y))
print("Inside area: ", insideArea)
printPathInsideOut()



