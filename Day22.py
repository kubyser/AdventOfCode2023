f = open("resources/day22_test_input.txt", "r")
lines = f.read().splitlines()
f.close()
data = {}

def overlapsXY(b1, b2):
    b1x1 = min(b1[0][0], b1[1][0])
    b1x2 = max(b1[0][0], b1[1][0])
    b2x1 = min(b2[0][0], b2[1][0])
    b2x2 = max(b2[0][0], b2[1][0])
    b1y1 = min(b1[0][1], b1[1][1])
    b1y2 = max(b1[0][1], b1[1][1])
    b2y1 = min(b2[0][1], b2[1][1])
    b2y2 = max(b2[0][1], b2[1][1])
    overlapX = max(0, min(b1x2, b2x2) - max(b1x1, b2x1) + 1)
    if overlapX == 0:
        return False
    overlapY = max(0, min(b1y2, b2y2) - max(b1y1, b2y1) + 1)
    if overlapY == 0:
        return False
    return True




for counter, line in enumerate(lines):
    s = line.split("~")
    c1 = tuple(int(a) for a in s[0].split(","))
    c2 = tuple(int(a) for a in s[1].split(","))
    if c1[2] > c2[2]:
        data[counter] = (c2, c1)
    else:
        data[counter] = (c1, c2)
print(data)
bricks = sorted(data, key=lambda z: data[z][0][2])
print(bricks)
for brNum in bricks:
    br = data[brNum]
    below = [b for b in bricks if data[b][1][2] <= br[0][2] and overlapsXY(br, data[b])]
    if len(below) == 0:
        newZ = 1
    else:
        topBrNum = max(below, key=lambda z: data[z][1][2])
        newZ = data[topBrNum][1][2]
    if br[0][2] > newZ:
        new1 = br[0][0], br[0][1], newZ
        new2 = br[0][0], br[0][1], newZ + br[1][2] - br[0][2]
        data[brNum] = (new1, new2)
print(data)
bricks = sorted(data, key=lambda z: data[z][0][2])
print(bricks)


