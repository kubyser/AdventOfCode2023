f = open("resources/day8_input.txt", "r")
lines = f.read().splitlines()
f.close()
inst = lines[0]
nodes = {}
for l in lines[2:]:
    a = l.split(" = ")[0]
    b = l.split(" = ")[1].replace("(", "").replace(")", "").split(", ")
    nodes[a] = b
print(nodes)
part2 = True
if not part2:
    curNode = "AAA"
    inPos = 0
    steps = 0
    while curNode != "ZZZ":
        curNode = nodes[curNode][0] if inst[inPos] == 'L' else nodes[curNode][1]
        inPos = 0 if inPos+1 == len(inst) else inPos+1
        steps += 1
    print("part 1 steps: ", steps)
else:
    startNodes = [x for x in nodes.keys() if x[2] == 'A']
    paths = {}
    inPos = 0
    steps = 0
    for n in startNodes:
        curNode = n
        inPos = 0
        steps = 0
        while curNode[2] != "Z":
            curNode = nodes[curNode][0] if inst[inPos] == 'L' else nodes[curNode][1]
            inPos = 0 if inPos+1 == len(inst) else inPos+1
            steps += 1
        paths[n] = steps
    print(paths.values())



