import queue

messages = queue.Queue()
units = {}
impulseCounter = {True: 0, False: 0}
part2 = True

def sendMessage(sender, signal):
    for d in units[sender][1]:
        messages.put((sender, signal, d))
    impulseCounter[signal] += len(units[sender][1])

def processQueue():
    countImpulses = 0
    while not messages.empty():
        message = messages.get()
        #print(message)
        sender = message[0]
        signal = message[1]
        unitName = message[2]
        if part2 and unitName == "rx" and not signal:
            #print("rx: ", message)
            return True
        if unitName not in units:
            continue
        unit = units[unitName]
        if unit[0] == "%":
            if not signal:
                unit[2] = not unit[2]
                sendMessage(unitName, unit[2])
            continue
        if unit[0] == "&":
            unit[2][sender] = signal
            response = not all(unit[2].values())
            sendMessage(unitName, response)
            continue
    return False

def broadcast(signal):
    impulseCounter[signal] += 1
    sendMessage("broadcaster", signal)
    return processQueue()


f = open("resources/day20_input.txt", "r")
lines = f.read().splitlines()
f.close()
for line in lines:
    name = line.split(" -> ")[0]
    destinations = line.split(" -> ")[1].split(", ")
    if name[0] in "&%":
        unitType = name[0]
        name = name[1:]
    else:
        unitType = None
    if unitType == "%":
        units[name] = [unitType, destinations, False]
    elif unitType == "&":
        units[name] = [unitType, destinations, {}]
    else:
        units[name] = [unitType, destinations]
print(units)
for unitName in units:
    for d in units[unitName][1]:
        if d not in units:
            continue
        destUnit = units[d]
        if destUnit[0] == "&":
            destUnit[2][unitName] = False
print(units)
i = 0
while i < 1000 or part2:
    i += 1
    if broadcast(False):
        break
print(impulseCounter)
print("Mult of impulses: ", impulseCounter[True] * impulseCounter[False])
print("Button pushes: ", i)
