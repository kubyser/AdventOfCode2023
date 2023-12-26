import queue
import sys
import time

f = open("resources/day25_test_input.txt", "r")
lines = f.read().splitlines()
f.close()
sys.setrecursionlimit(100000)


def addOrIncrease(dic, key, value=1):
    if key in dic:
        dic[key] += value
    else:
        dic[key] = value



def karger(items):
    while len(items) > 2:
        a = list(items)[0]
        b = list(items[a])[0]
        for bchild in items[b]:
            if bchild == a:
                continue
            value = items[b][bchild]
            addOrIncrease(items[a], bchild, value)
        del items[a][b]
        for c in items:
            if c != a and b in items[c]:
                value = items[c][b]
                del items[c][b]
                addOrIncrease(items[c], a, value)
        del items[b]
    print(items)
    return list(list(items.values())[0].values())[0]



items = {}
for line in lines:
    name = line.split(": ")[0]
    if name not in items:
        items[name] = {}
    connected = line.split(": ")[1].split()
    for c in connected:
        if c not in items:
            items[c] = {}
        addOrIncrease(items[name], c)
        addOrIncrease(items[c], name)
print(items)
#print(countGroups(items))
startTime = time.time()

minSplit = karger(items)
endTime = time.time()
print(minSplit)
print("Time: ", endTime-startTime)
