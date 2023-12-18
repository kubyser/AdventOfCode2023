from collections import deque
from queue import Queue

DIRMAP = {"U": (0, -1), "D": (0, 1), "R": (1, 0), "L": (-1, 0)}
CHARTODIR = {0: "R", 1: "D", 2: "L", 3: "U"}


def shoelace(data):
    a = 0
    l = len(data)
    for i in range(l-1):
        y = data[i][1] + data[i+1][1]
        x = data[i][0] - data[i+1][0]
        a += x*y
    a /= 2
    return a


def printData(data):
    minX = min(data, key=lambda x: x[0])[0]
    maxX = max(data, key=lambda x: x[0])[0]
    minY = min(data, key=lambda x: x[1])[1]
    maxY = max(data, key=lambda x: x[1])[1]
    for y in range(minY, maxY+1):
        s= ""
        for x in range(minX, maxX+1):
            if (x,y) in data:
                s += "#"
            else:
                s += "."
        print(s)



f = open("resources/day18_input.txt", "r")
lines = f.read().splitlines()
f.close()
data = []
pos = (0, 0)
perim = 0
for line in lines:
    s = line.split()
    ls = s[2][2:7]
    length = int(ls, 16)
    ds = s[2][7]
    direction = CHARTODIR[int(ds)]

    #direction = s[0]
    #length = int(s[1])

    dirCoords = DIRMAP[direction]
    shift = (dirCoords[0] * length, dirCoords[1] * length)
    pos = (pos[0] + shift[0], pos[1] + shift[1])
    data.append(pos)
    perim += length
print(data)
#printData(data)
print("Perim ", perim)
print(shoelace(data)+perim/2 + 1)



