f = open("resources/day1_input.txt", "r")
lines = f.read().splitlines()
f.close()

#patterns = {"1": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9}
patterns = {"1": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9,
             "one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9}

result = 0
for line in lines:
    print(line)
    minPositions = {line.find(x): patterns[x] for x in patterns.keys()}
    minPositions.pop(-1)
    print(minPositions)
    firstDigit = minPositions[min(minPositions.keys())]
    print(firstDigit)
    maxPositions = {line.rfind(x): patterns[x] for x in patterns.keys()}
    maxPositions.pop(-1)
    print(maxPositions)
    secondDigit = maxPositions[max(maxPositions.keys())]
    print(secondDigit)
    number = int(firstDigit) * 10 + int(secondDigit)
    result += number
print("Result: ", result)

