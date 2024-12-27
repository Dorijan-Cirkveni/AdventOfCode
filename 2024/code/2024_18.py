import json


def read(filepath):
    M = None
    try:
        file = open(filepath, 'r')
        M = file.read().split('\n')
        file.close()
    except Exception as err:
        print(err)
    return M


class Grid:
    def __init__(self, n: int = 71, m: int = 71):
        self.M = [[float('inf')] * m + [-1] for _ in range(n)]
        L = [-1] * m
        self.M.append(L)

    def occupy(self, i, j):
        self.M[j][i] = -1

    def get_neigh(self, i, j, ):
        return {(i, j - 1), (i, j + 1), (i - 1, j), (i + 1, j)}

    def traverse(self, start, goal):
        curset = {start}
        curval = -1
        while curset:
            curval += 1
            nexset = set()
            for i, j in curset:
                if self.M[i][j] <= curval:
                    continue
                self.M[i][j] = curval
                nexset |= self.get_neigh(i, j)
            curset = nexset
        i, j = goal
        return self.M[i][j]

    def getBestNeigh(self, i, j):
        best = 1 << 31
        for di, dj in self.get_neigh(i, j):
            val = self.M[di][dj]
            if val in range(best):
                best = val
        return {1 << 31: -1}.get(best, best)

    def block(self, i, j, goal):
        curset = self.get_neigh(i, j)
        self.M[i][j] = -1
        for E in self.M:
            for i,e in enumerate(E):
                E[i]=float('inf') if e>=0 else -1
        res=self.traverse((0,0),goal)
        return {float('inf'):-1}.get(res,res)


def preprocess(s: str):
    return tuple(json.loads(f'[{s}]'))


def process_1(data):
    data = data[:1024]
    procdata = []
    size = 71, 71
    for entry in data:
        entry: str
        if entry[0] == 's':
            ind = entry.index(':') + 1
            entry = entry[ind:]
            size = preprocess(entry)
            continue
        processed = preprocess(entry)
        procdata.append(processed)
    grid = Grid(*size)
    for i, j in procdata:
        grid.occupy(i, j)
    a, b = size
    res = grid.traverse((0, 0), (a - 1, b - 1))
    for E in grid.M:
        for e in E:
            pe = ('█ ' + str(e % 10))[(e >= 0) + (e in range(999))]
            print(pe, end='')
        print()
    return res


def process_2(data):
    procdata = []
    size = 71, 71
    for entry in data:
        entry: str
        if entry[0] == 's':
            ind = entry.index(':') + 1
            entry = entry[ind:]
            size = preprocess(entry)
            continue
        processed = preprocess(entry)
        procdata.append(processed)
    grid = Grid(*size)
    a, b = size
    grid.traverse((0, 0), (a - 1, b - 1))
    for i, e in enumerate(procdata):
        state = grid.block(*e, goal=(a - 1, b - 1))
        print(i,e)
        if state == -1:
            return e
    for E in grid.M:
        for e in E:
            pe = ('█ ' + str(e % 10))[(e >= 0) + (e in range(999))]
            print(pe, end='')
        print()
    return -1, -1


TASK = __file__.split('\\')[-1][:-3]


def runprocess_withinputfrom(process: callable, suffix: str = ""):
    inputbase = f"..\\inputs\\{TASK}{suffix}.txt"
    data = read(inputbase)
    if data is not None:
        result = process(data)
        print(f"Result for {suffix}: {result}")


def runprocess(process: callable, input_files=None):
    if input_files is None:
        input_files = [""]
    for suffix in input_files:
        runprocess_withinputfrom(process, suffix)


def main():
    runprocess(process_2, ["t", ""])
    return


if __name__ == "__main__":
    main()
