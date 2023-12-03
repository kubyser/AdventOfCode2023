class Utilities:

    @staticmethod
    def loadMatrixChars(fileName):
        dataLines = open(fileName).read().splitlines()
        data = {}
        y = 0
        for s in dataLines:
            x = 0
            for c in s:
                data[(x, y)] = c
                x += 1
            y += 1
        return data, x, y
