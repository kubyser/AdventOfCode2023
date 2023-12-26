import queue
import sys
import time

f = open("resources/day25_input.txt", "r")
lines = f.read().splitlines()
f.close()
sys.setrecursionlimit(100000)
mapItemsToNums = {}
mapNumsToItems = {}


def countGroups(items, brokenLinks = None):
    item = list(items.keys())[0]
    visited = {item}
    toVisit = queue.Queue()
    for c in items[item]:
        if brokenLinks is None or ((item, c) not in brokenLinks and (c, item) not in brokenLinks):
            toVisit.put(c)
    while not toVisit.empty():
        item = toVisit.get()
        visited.add(item)
        for c in items[item]:
            if brokenLinks is None or ((item, c) not in brokenLinks and (c, item) not in brokenLinks):
                if c not in visited:
                    toVisit.put(c)
    if len(visited) == len(items):
        return 1, [len(visited)]
    return 2, [len(visited), len(items)-len(visited)]


visited = [None]*len(mapItemsToNums)
timeCounter = 0
allBrokenLinks = []


def dfs(node, parent=None):
    global timeCounter
    visited[node] = [timeCounter, timeCounter]
    timeCounter += 1
    for c in items[node]:
        if brokenLinks is None or (node, c) not in brokenLinks and (c, node) not in brokenLinks:
            if c == parent:
                continue
            if visited[c] is not None:
                newLow = min(visited[node][1], visited[c][0])
                if newLow != visited[node][1]:
                    visited[node][1] = newLow
            else:
                dfs(c, node)
                newLow = min(visited[node][1], visited[c][1])
                if newLow != visited[node][1]:
                    visited[node][1] = newLow
                if (visited[c][1] > visited[node][0]):
                    print("Bridge: ", node, c, mapNumsToItems[node], mapNumsToItems[c])
                    print("Broken links: ", brokenLinks, [(mapNumsToItems[x[0]], mapNumsToItems[x[1]]) for x in [b for b in brokenLinks]])
                    allBrokenLinks.append((node, c))
                    exit(0)


def dfsQueue(node):
    toVisit = queue.LifoQueue()
    toVisit.put(node)
    visited = set()
    while not toVisit.empty():
        node = toVisit.get()
        visited.add(node)
        for c in items[node]:
            if brokenLinks is None or (node, c) not in brokenLinks and (c, node) not in brokenLinks:
                if c not in visited:
                    toVisit.put(c)



items = []
links = set()
for line in lines:
    name = line.split(": ")[0]
    if name not in mapItemsToNums:
        mapItemsToNums[name] = len(items)
        mapNumsToItems[len(items)] = name
        items.append(set())
    nameNum = mapItemsToNums[name]
    connected = line.split(": ")[1].split()
    for c in connected:
        if c not in mapItemsToNums:
            mapItemsToNums[c] = len(items)
            mapNumsToItems[len(items)] = c
            items.append(set())
        cNum = mapItemsToNums[c]
        items[nameNum].add(cNum)
        items[cNum].add(nameNum)
        if (cNum, nameNum) not in links:
            links.add((nameNum, cNum))
print(items)
#print(countGroups(items))
print(links)
listLinks = list(links)
print(len(listLinks))
startItem = 0
startTime = time.time()

globalTime = time.time()
for i in range(len(listLinks)-2):
    endTime = time.time()
    print(i, "Time: ", endTime-startTime)
    startTime = endTime
    a = listLinks[i]
    for j in range(i+1, len(listLinks)-1):
        b = listLinks[j]
        visited = [None]*len(mapItemsToNums)
        timeCounter = 0
        brokenLinks = [a, b]
        dfs(startItem)
print("Global time: ", time.time() - globalTime)
#res = countGroups(items, allBrokenLinks)
#print(res)
#print("product ", res[1][0] * res[1][1])




