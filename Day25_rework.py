import heapq
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


timeCounter = 0
allBrokenLinks = []
visited = {}

def dfs_findBridge(node, brokenLinks=None, parent=None):
    global timeCounter
    global visited
    if parent is None:
        visited = {}
    visited[node] = [timeCounter, timeCounter]
    timeCounter += 1
    for c in items[node]:
        if brokenLinks is None or (node, c) not in brokenLinks and (c, node) not in brokenLinks:
            if c == parent:
                continue
            if c in visited:
                newLow = min(visited[node][1], visited[c][0])
                if newLow != visited[node][1]:
                    visited[node][1] = newLow
            else:
                dfs_findBridge(c, brokenLinks, node)
                newLow = min(visited[node][1], visited[c][1])
                if newLow != visited[node][1]:
                    visited[node][1] = newLow
                if (visited[c][1] > visited[node][0]):
                    print("Bridge: ", node, c)
                    brokenLinks.append((node, c))
                    print("Broken links: ", brokenLinks)
                    exit(0)


def pathsToTarget(node, target, path=None):
    if path is None:
        path = [node]
    else:
        path.append(node)
    if node == target:
        return [path]
    pathsList = []
    for c in items[node]:
        if c in path:
            continue
        newPaths = pathsToTarget(c, target, list(path))
        pathsList += newPaths
    return pathsList

def countLinks(paths):
    counter = {}
    for path in paths:
        for i in range(len(path)-1):
            a = path[i]
            b = path[i+1]
            pair = (a, b) if (a, b) in links else (b, a)
            counter[pair] = 1 if pair not in counter else counter[pair] + 1
    return counter



def dijkstra(node):
    visited = {}
    queue = []
    heapq.heappush(queue, (0, node))
    while queue:
        depth, node = heapq.heappop(queue)
        if node not in visited or visited[node] > depth:
            visited[node] = depth
        for c in items[node]:
            if c not in visited:
                heapq.heappush(queue, (depth+1, c))
    return visited




items = {}
links = set()
for line in lines:
    name = line.split(": ")[0]
    if name not in items:
        items[name] = []
    connected = line.split(": ")[1].split()
    for c in connected:
        if c not in items:
            items[c] = []
        items[name].append(c)
        items[c].append(name)
        if (c, name) not in links:
            links.add((name, c))
#print(items)
#print(countGroups(items))
#print(links)
listLinks = list(links)
print(len(listLinks))
startItem = list(items.keys())[0]
startTime = time.time()

allNodesDepth = dijkstra(startItem)
print(allNodesDepth)
furthestNode = [x for x in allNodesDepth if allNodesDepth[x] == max(allNodesDepth.values())][0]
print(furthestNode)
paths = pathsToTarget(startItem, furthestNode)
print(len(paths))
counter = countLinks(paths)
print(counter)
sortedLinks = sorted(counter.keys(), key=lambda x: counter[x], reverse=True)
print(sortedLinks)
allBrokenLinks = sortedLinks[0:2]
dfs_findBridge(startItem, allBrokenLinks)
exit(0)

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




