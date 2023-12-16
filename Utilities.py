class Utilities:

    @staticmethod
    def loadMatrixChars(fileName, skipChar = None):
        dataLines = open(fileName).read().splitlines()
        data = {}
        y = 0
        for s in dataLines:
            x = 0
            for c in s:
                if skipChar is None or c != skipChar:
                    data[(x, y)] = c
                x += 1
            y += 1
        return data, x, y


    @staticmethod
    def loadMatrixAsRowsColumns(fileName, skipChar = None):
        dataLines = open(fileName).read().splitlines()
        data = {}
        y = 0
        for s in dataLines:
            x = 0
            for c in s:
                if skipChar is None or c != skipChar:
                    data[(x, y)] = c
                x += 1
            y += 1
        return data, x, y
