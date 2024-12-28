import json
from collections import defaultdict

INF = 1 << 31


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
    def __init__(self, raw: list[str]):
        guide = {
            '#': -1,
            '.': INF,
            'E': INF,
            'S': 42
        }
        self.M: list[list[int]] = []
        self.start = -1, -1
        self.end = -1, -1
        for i, e in enumerate(raw):
            L: list[int] = []
            self.M.append(L)
            for j, c in enumerate(e):
                if c == 'S':
                    self.start = i, j
                elif c == 'E':
                    self.end = i, j
                val = guide[c]
                L.append(val)
            L[0] = -2
            L[-1] = -2
        M=self.M
        for i in range(len(M[0])):
            M[0][i] = -2
            M[-1][i] = -2
        return

    def get(self, i, j) -> int:
        return self.M[i][j]

    def set(self, i, j, v: int):
        self.M[i][j] = v

    def get_neigh(self, i, j, minval=0):
        base = {(i, j - 1), (i, j + 1), (i - 1, j), (i + 1, j)}
        return {e for e in base if self.get(*e) >= minval}

    def get_neigh_2(self, i, j, minval=0):
        start = i, j
        neigh = self.get_neigh(*start, -1)
        res = set()
        for el in neigh:
            res |= self.get_neigh(*el)
        res.remove(start)
        return {e for e in res if self.get(*e) >= minval}

    def traverse(self):
        curset = {self.start}
        curval = -1
        while curset:
            curval += 1
            nexset = set()
            for cur in curset:
                if self.get(*cur) <= curval:
                    continue
                self.set(*cur, v=curval)
                nexset |= self.get_neigh(*cur)
            curset = nexset
        return self.get(*self.end)

    def getBestNeigh(self, i, j):
        best = INF
        for di, dj in self.get_neigh(i, j):
            val = self.M[di][dj]
            if val in range(best):
                best = val
        return {INF: -1}.get(best, best)

    def cheat(self, start, minimum: int, log: defaultdict[int, int]):
        res = 0
        val = self.get(*start)
        for nex in self.get_neigh_2(*start):
            dist = self.get(*nex) - val
            if dist - 2 >= minimum:
                res += 1
                log[dist - 2] += 1
        return res

    def cheat_all(self, ref: int, minimum: int, log: defaultdict[int, int]):
        res = 0
        for i, row in enumerate(self.M):
            for j, el in enumerate(row):
                if el < 0 or el > ref - minimum:
                    continue
                res += self.cheat((i, j), minimum, log)
        return res


def process_1(data):
    grid = Grid(data)
    ref = grid.traverse()
    minimum = 0 if len(grid.M) < 20 else 100
    for E in grid.M:
        for e in E:
            pe = ('█ ' + str(e % 10))[(e >= 0) + (e in range(999))]
            print(pe, end='')
        print()
    log = defaultdict(int)
    res = grid.cheat_all(ref, minimum, log)
    res-=log[0]
    L=list(log)
    L.sort()
    for e in L:
        print(e, ":", log[e])
    return res


def process_2(data):
    return process_1(data)


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
