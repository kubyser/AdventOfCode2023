RED = "red"
GREEN = "green"
BLUE = "blue"

maxCubes = {RED: 12, GREEN: 13, BLUE: 14}

f = open("resources/day2_input.txt", "r")
lines = f.read().splitlines()
f.close()
games = {}
cal = 0
for line in lines:
    gameNum = int(line.split(": ")[0].replace("Game ", ""))
    game = []
    gameSets = line.split(": ")[1].split("; ")
    for gameSet in gameSets:
        newSet = {}
        cubes = gameSet.split(", ")
        for cube in cubes:
            num = int(cube.split(" ")[0])
            color = cube.split(" ")[1]
            newSet[color] = num
        game.append(newSet)
    games[gameNum] = game
print(games)

# part1
sumPossibleGames = 0;
for i in games.keys():
    game = games[i]
    possible = True
    for s in game:
        for color in s.keys():
            if s[color] > maxCubes[color]:
                possible = False
                break
        if not possible:
            break
    if possible:
        print("Possible game: ", i)
        sumPossibleGames += i
print("Sum of possible games: ", sumPossibleGames)

# part2
sumPowers = 0
for i in games.keys():
    game = games[i]
    minCubes = {RED: 0, GREEN: 0, BLUE: 0}
    for s in game:
        for color in s.keys():
            if s[color] > minCubes[color]:
                minCubes[color] = s[color]
    gamePower = minCubes[RED] * minCubes[GREEN] * minCubes[BLUE]
    print("Power of game ", i, ": ", gamePower)
    sumPowers += gamePower

print("Minimum cubes: ", sumPowers)
