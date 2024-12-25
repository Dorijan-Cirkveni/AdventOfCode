import heapq

from numpy.f2py.crackfortran import traverse

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


def preprocess(s: str):
    return s


def deltaFunction(i=0, j=0):
    return (i, j + 1), (i, j - 1), (i + 1, j), (i - 1, j)


def shift(pos, delta):
    a, b = pos
    da, db = delta
    return a + da, b + db


def turn(i, j):
    a = j, i
    b = -j, -i
    return a, b


class PriorityQueue:
    def __init__(self):
        self.times = []
        self.content: dict[int, list] = {}

    def add(self, time, event):
        if time not in self.content:
            self.content[time] = []
            heapq.heappush(self.times, time)
        self.content[time].append(event)

    def pop(self):
        time = self.times[0]
        stack = self.content[time]
        res = stack.pop()
        if not stack:
            self.content.pop(time)
            heapq.heappop(self.times)
        return time, res

    def __bool__(self):
        return bool(self.times)


class Grid:
    def __init__(self, raw: list[str]):
        self.grid = []
        self.start = -1, -1
        self.goal = -1, -1
        for i, row in enumerate(raw):
            curlist = []
            for j, el in enumerate(row):
                value = [INF, INF]
                if el == 'E':
                    self.goal = i, j
                elif el == 'S':
                    self.start = i, j
                elif el == '#':
                    value = [-1, -1]
                curlist.append(value)
            self.grid.append(curlist)
        self.prio = PriorityQueue()
        return

    def getTile(self, i, j):
        return self.grid[i][j]

    def addPrio(self, position, delta, time):
        newdata = shift(position, delta), delta
        self.prio.add(time + 1, newdata)

    def step(self):
        time, (position, delta) = self.prio.pop()
        dimensions = [0, 1]
        if delta[0] == 0:
            dimensions.reverse()
        place = self.getTile(*position)
        antidelta = -delta[0], -delta[1]
        deltas = (delta, antidelta)
        for dimension in dimensions:
            if place[dimension] <= time:
                return
            place[dimension] = time
            for new_delta in deltas:
                self.addPrio(position, new_delta, time)
            time += 1000
            deltas = turn(*delta)
        return

    def traverse(self, delta=(0, 1)):
        start = self.start, delta
        self.prio.add(0, start)
        while self.prio and min(self.getTile(*self.goal)) == INF:
            self.step()
        return min(self.getTile(*self.goal))

    def retroverse(self, data):
        antigrid = Grid(data)
        antigrid.goal = self.start
        antigrid.start = self.goal
        X = self.getTile(*self.goal)
        for i, b in enumerate(X):
            if b != min(X):
                continue
            antigrid.traverse((1 ^ i, i))
        antigrid.getTile(*self.goal)
        antigrid.print_state()
        true_res = self.countBestTilesCore(antigrid, min(X))
        return true_res

    def print_state(self):
        for i, row in enumerate(self.grid):
            s = ''
            for j, el in enumerate(row):
                if el[-1] == -1:
                    s += '█'
                    continue
                chk = [e != INF for e in el]
                n = chk[0] + chk[1] * 2
                s += ' |-+'[n]
            print(s)
        print()

    def countBestTilesCore(self, antigrid, minimum):
        antigrid: Grid
        res = 0
        i = -1
        for row, antigrid_row in zip(self.grid, antigrid.grid):
            i += 1
            j = -1
            s = ''
            for el, antigrid_el in zip(row, antigrid_row):
                j += 1
                if el == [-1, -1]:
                    s += '█'
                    continue
                a1, b1 = el
                a2, b2 = antigrid_el

                if a1 + a2 == minimum or b1 + b2 == minimum:
                    res += 1
                    s += 'X'
                else:
                    s += ' '
            print(s)
        print()
        return res


def process_1(data):
    grid = Grid(data)
    res = grid.traverse()
    grid.print_state()
    return res


def process_2(data):
    grid = Grid(data)
    grid.traverse()
    res=grid.retroverse(data)
    return res


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
    runprocess(process_2, ["t", "t2", ""])
    return


if __name__ == "__main__":
    main()
