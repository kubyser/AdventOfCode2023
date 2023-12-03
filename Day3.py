from Utilities import Utilities

data = width = height = None
numbers = {}

def hasCharsAround(xPos, yPos):
    for y in range(yPos-1, yPos+2):
        if y < 0 or y >= height:
            continue
        for x in range(xPos-1, xPos+2):
            if x < 0 or x >= width:
                continue
            if not data[(x, y)].isdigit() and data[(x, y)] != '.':
                return True
    return False

def getNumbersAround(xPos, yPos):
    numbersAround = []
    for y in range(yPos-1, yPos+2):
        inNumber = False
        if y < 0 or y >= height:
            continue
        for x in range(xPos-1, xPos+2):
            if x < 0 or x >= width:
                continue
            if data[(x, y)].isdigit():
                if not inNumber:
                    numbersAround.append(numbers[(x, y)])
                inNumber = True
            else:
                inNumber = False
    return numbersAround

def backFillNumber(number, xPos, yPos):
    x = xPos
    while True:
        if x < 0 or not data[(x, yPos)].isdigit():
            return
        numbers[(x, yPos)] = number
        x -= 1


#data, width, height = Utilities.loadMatrixChars("resources/day3_test_input.txt")
data, width, height = Utilities.loadMatrixChars("resources/day3_input.txt")
#print(data)
#print(width, height)
foundNumbers = []
for y in range(height):
    curNum = None
    validNum = False
    for x in range(width):
        c = data[(x, y)]
        if c.isdigit():
            if curNum is None:
                curNum = int(c)
                validNum = hasCharsAround(x, y)
            else:
                curNum *= 10
                curNum += int(c)
                if not validNum:
                    validNum = hasCharsAround(x, y)
        else:
            if curNum is not None:
                backFillNumber(curNum, x-1, y)
                if validNum:
                    foundNumbers.append(curNum)
#                print("Found number: ", curNum, "valid: ", validNum)
                curNum = None
    if curNum is not None:
        backFillNumber(curNum, width-1, y)
        if validNum:
            foundNumbers.append(curNum)
 #       print("Found number: ", curNum, "valid: ", validNum)
    curNum = None
print("Sum of valid numbers: ", sum(foundNumbers))
# part2
sumGearRatios = 0
for y in range(height):
    for x in range(width):
        if data[(x, y)] == '*':
            numbersAround = getNumbersAround(x, y)
            print("* at pos ", x, y, "; numbers around are ", numbersAround)
            if len(numbersAround) == 2:
                sumGearRatios += numbersAround[0] * numbersAround[1]
print("Sum of all gear ratios: ", sumGearRatios)

