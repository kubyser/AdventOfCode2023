import time

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


pool = {((1, 0, 'R', 0), 0), ((0, 1, 'D', 0), 0)}
#visited = {(0, 0, 'R', 0): 0}
visited = {(0, 0): 0}
res = None

start = time.time()
while len(pool) > 0:
    cell = min(pool, key=lambda x: x[1])
    pool.remove(cell)
    x = cell[0][0]
    y = cell[0][1]
    direction = cell[0][2]
    straight = cell[0][3]
    heatLoss = cell[1]
    vCell = x, y, direction, straight if straight < 3 else -1
    if vCell in visited:
        #if (x, y) in visited:
        vis = visited[vCell]
        if heatLoss >= vis[0] and straight >= vis[1]:
            continue
    visited[vCell] = (heatLoss, straight)
    #visited[(x, y)] = heatLoss
    heatLoss += data[y][x]
    if x == width-1 and y == height-1 and straight >= 3:
        if res is None or res > heatLoss:
            res = heatLoss
        continue
    newDir = getDirections(x, y, direction, straight)
    for d in newDir:
        pool.add(((d[0], d[1], d[2], d[3]), heatLoss))
end = time.time()

print("Min heatloss: ", res)
print("time ", end-start)



