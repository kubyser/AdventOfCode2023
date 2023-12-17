import time
import heapq

f = open("resources/day17_input.txt", "r")
lines = f.read().splitlines()
f.close()
data = []
height = len(lines)
width = len(lines[0])
for line in lines:
    dataLine = [int (x) for x in list(line)]
    data.append(dataLine)
print(data)

def getDirections(x, y, direction, straigh):
    res = []
    if straigh >= 3:
        if direction == 'R' or direction == 'L':
            if y > 0:
                res.append((x, y-1, 'U', 0))
            if y < height-1:
                res.append((x, y+1, 'D', 0))
        else:
            if x > 0:
                res.append((x-1, y, 'L', 0))
            if x < width-1:
                res.append((x+1, y, 'R', 0))
    if straigh < 9:
        if direction == 'R':
            if x < width-1:
                res.append((x+1, y, direction, straigh+1))
        elif direction == 'L':
            if x > 0:
                res.append((x-1, y, direction, straigh+1))
        elif direction == 'D':
            if y < height-1:
                res.append((x, y+1, direction, straigh+1))
        else:
            if y > 0:
                res.append((x, y-1, direction, straigh+1))
    return res


pool = []
heapq.heappush(pool, (0, (1, 0, 'R', 0)))
heapq.heappush(pool, (0, (0, 1, 'D', 0)))
visited = {}
res = None

start = time.time()
while pool:
    cell = heapq.heappop(pool)
    x = cell[1][0]
    y = cell[1][1]
    direction = cell[1][2]
    straight = cell[1][3]
    heatLoss = cell[0]
    vCell = x, y, direction, straight if straight < 3 else -1
    if vCell in visited:
        vis = visited[vCell]
        if heatLoss >= vis[0] and straight >= vis[1]:
            continue
    visited[vCell] = (heatLoss, straight)
    heatLoss += data[y][x]
    if x == width-1 and y == height-1 and straight >= 3:
        res = heatLoss
        break
    newDir = getDirections(x, y, direction, straight)
    for d in newDir:
        heapq.heappush(pool, (heatLoss, (d[0], d[1], d[2], d[3])))
end = time.time()

print("Min heatloss: ", res)
print("time ", end-start)



