import queue
import sys
import time

f = open("resources/day25_input.txt", "r")
lines = f.read().splitlines()
f.close()
sys.setrecursionlimit(100000)


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


visited = {}
timeCounter = 0
allBrokenLinks = []


def dfs(items, node, brokenLinks = None, parent=None):
    global timeCounter
    visited[node] = (timeCounter, timeCounter)
    timeCounter += 1
    for c in items[node]:
        if brokenLinks is None or (node, c) not in brokenLinks and (c, node) not in brokenLinks:
            if c == parent:
                continue
            if c in visited:
                newLow = min(visited[node][1], visited[c][0])
                if newLow != visited[node][1]:
                    visited[node] = (visited[node][0], newLow)
            else:
                dfs(items, c, brokenLinks, node)
                newLow = min(visited[node][1], visited[c][1])
                if newLow != visited[node][1]:
                    visited[node] = (visited[node][0], newLow)
                if (visited[c][1] > visited[node][0]):
                    print("Bridge: ", node, c)
                    allBrokenLinks.append((node, c))


items = {}
links = set()
for line in lines:
    name = line.split(": ")[0]
    if name not in items:
        items[name] = set()
    connected = line.split(": ")[1].split()
    for c in connected:
        if c not in items:
            items[c] = set()
        items[name].add(c)
        items[c].add(name)
        if (c, name) not in links:
            links.add((name, c))
print(items)
allBrokenLinks=[('dhn', 'xvh'), ('ptj', 'qmr'), ('lsv', 'lxt')]
res = countGroups(items, allBrokenLinks)
print(res)
print("product ", res[1][0] * res[1][1])
exit(0)
#print(countGroups(items))
print(links)
listLinks = list(links)
print(len(listLinks))
startItem = list(items.keys())[0]
startTime = time.time()


for i in range(len(listLinks)-2):
    endTime = time.time()
    print(i, "Time: ", endTime-startTime)
    startTime = endTime
    a = listLinks[i]
    for j in range(i+1, len(listLinks)-1):
        b = listLinks[j]
        visited.clear()
        timeCounter = 0
        brokenLinks = [a, b]
        dfs(items, startItem, brokenLinks)

allBrokenLinks=[('dhn', 'xvh'), ('ptj', 'qmr'), ('lsv', 'lxt')]
res = countGroups(items, allBrokenLinks)
print(res)
print("product ", res[1][0] * res[1][1])



