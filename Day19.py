f = open("resources/day19_input.txt", "r")
lines = f.read().splitlines()
f.close()
rules = {}


def processPart(part, name):
    flow = rules[name]
    target = None
    for f in flow:
        if f[1] is None:
            target = f[0]
        else:
            cond = f[1]
            res = part[cond[0]] > cond[2] if cond[1] == ">" else part[cond[0]] < cond[2]
            if res:
                target = f[0]
        if target is None:
            continue
        if target == 'R':
            return False
        if target == 'A':
            return True
        return processPart(part, target)


def getSize(ranges):
    s = 1
    for p in "xmas":
        s *= ranges[p][1] - ranges[p][0] + 1
    return s

def adjustRangesFalse(ranges, condition):
    p = condition[0]
    value = condition[2]
    if condition[1] == ">":
        if ranges[p][0] > value:
            return None
        if ranges[p][1] > value:
            ranges[p] = (ranges[p][0], value)
    else:
        if ranges[p][1] < value:
            return None
        if ranges[p][0] < value:
            ranges[p] = (value, ranges[p][1])
    return ranges


def adjustRangesTrue(ranges, condition):
    p = condition[0]
    value = condition[2]
    if condition[1] == ">":
        if ranges[p][1] <= value:
            return None
        if ranges[p][0] <= value:
            ranges[p] = (value+1, ranges[p][1])
    else:
        if ranges[p][0] >= value:
            return None
        if ranges[p][1] >= value:
            ranges[p] = (ranges[p][0], value-1)
    return ranges



def copyRanges(inRanges):
    r = {}
    for x in "xmas":
        r[x] = (inRanges[x][0], inRanges[x][1])
    return r


def findRange(target, ranges):
    rlist = []
    for r in rules:
        rule = rules[r]
        if target in [x[0] for x in rule]:
            length = len(rule)
            for i in range(0, length):
                if rule[i][0] == target:
                    rlist.append((r, i))
    res = 0
    for rName, rPos in rlist:
        rule = rules[rName]
        newRanges = copyRanges(ranges)
        pos = 0
        for r in rule:
            if pos == rPos:
                if r[1] is not None:
                    newRanges = adjustRangesTrue(newRanges, r[1])
                    if newRanges is None:
                        break
                if rName == "in":
                    res += getSize(newRanges)
                else:
                    res += findRange(rName, newRanges)
                break
            pos += 1
            newRanges = adjustRangesFalse(newRanges, r[1])
            if newRanges is None:
                break
    return res

for line in lines:
    if len(line) == 0:
        break
    name = line.split("{")[0]
    rules[name] = []
    rlist = line.split("{")[1][:-1].split(",")
    for r in rlist:
        if ':' in r:
            pars = r.split(":")[0]
            target = r.split(":")[1]
            if '<' in pars:
                cond = "<"
            else:
                cond = ">"
            par = pars.split(cond)[0]
            value = int(pars.split(cond)[1])
            rules[name].append((target, (par, cond, value)))
        else:
            rules[name].append((r, None))
parts = []
for line in lines[len(rules)+1:]:
    part = {}
    attrs = line[1:-1].split(",")
    for a in attrs:
        par = a.split("=")[0]
        value = int(a.split("=")[1])
        part[par] = value
    parts.append(part)

if False:
    print(rules)
    print(parts)
    res = 0
    for part in parts:
        accepted = processPart(part, "in")
        if accepted:
            sumAdd = sum([x for x in part.values()])
            res += sumAdd
            print("Accepted: ", part, " value is ", sumAdd)
        else:
            print("Rejected: ", part)
    print("Sum is ", res)
startRange = {'x': (1, 4000), 'm': (1, 4000), 'a': (1, 4000), 's': (1, 4000), }
part2RangeSize = findRange("A", startRange)
print("Part 2 range size ", part2RangeSize)