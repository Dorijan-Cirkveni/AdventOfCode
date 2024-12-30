import heapq
import math
from collections import defaultdict


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


DIRECTIONS = {
    '^': (-1, 0),
    '<': (0, -1),
    'v': (1, 0),
    '>': (0, 1)
}


def diffToSet(start: int, end: int, c1: str, c2: str, curset: set):
    if start == end:
        return
    curset.add(c1 if start > end else c2)
    return


def combine_directions(curset: set[str], dirset: dict, nexset: defaultdict[str, set]):
    for cur in curset:
        for cdir, valset in dirset.items():
            valset: set
            if not valset:
                continue
            val = min(valset)
            nexset[cdir].add(cur + min(val))


class GroupedPriorityQueue:
    def __init__(self):
        self.pq = []
        self.groups = {}

    def add(self, key, value):
        if key in self.groups:
            self.groups[key].add(value)
        else:
            heapq.heappush(self.pq, key)
            self.groups[key] = {value}

    def check(self):
        return bool(self.pq)

    def pop_group(self) -> [int, set]:
        key = heapq.heappop(self.pq)
        value = self.groups.pop(key)
        return key, value

    def pop(self):
        key = self.pq[0]


class Keypad:
    def __init__(self, raw: str):
        raw += ' ' * 16
        positions = {e: divmod(i, 4) for i, e in enumerate(raw) if e != ' '}
        self.neigh = [set() for _ in range(16)]
        for i in range(4):
            for j in range(3):
                a = i * 4 + j
                self.setNeigh(a, a + 1, raw)
                a = j * 4 + i
                self.setNeigh(a, a + 4, raw)
        self.directions: dict[tuple, dict[tuple, set]] = {}
        for si, sj in positions.values():
            curdir: dict[tuple, set] = {}
            self.directions[(si, sj)] = curdir
            for (ei, ej) in positions.values():
                curset = set()
                curdir[(ei, ej)] = curset
                diffToSet(si, ei, '^', 'v', curset)
                diffToSet(sj, ej, '<', '>', curset)
        self.positions = positions
        return

    def setNeigh(self, a, b, raw: str):
        if ' ' in raw[a] + raw[b]:
            return
        self.neigh[a].add(b)
        self.neigh[b].add(a)

    def getNeigh(self, a, b) -> set:
        a <<= 2
        a |= b
        nei = self.neigh[a]
        return {divmod(e, 4) for e in nei}

    def getMoves(self, sc: str, ec: str) -> list[str]:
        start = self.positions[sc]
        end = self.positions[ec]
        cur_val = {start: {''}}
        while end not in cur_val:
            nex_val = defaultdict(set)
            for cur, curset in cur_val.items():
                neigh = self.getNeigh(*cur)
                dirs = self.directions[cur][end]
                dirset = {e: self.directions[cur][e] for e in neigh}
                final_dirset = {e: v for e, v in dirset.items() if v & dirs}
                combine_directions(curset, final_dirset, nex_val)
            cur_val = nex_val
        res = cur_val[end]
        return [e + 'A' for e in res]

    def evaluateMoveset(self, moves: str, direction_costs=None, last: str = 'A'):
        if direction_costs is None:
            direction_costs = {}
        res = 0
        for e in moves:
            res += direction_costs.get((last, e), 1)
            last = e
        return res

    def getComplexity(self, start: str, end: str, direction_costs=None):
        if direction_costs is None:
            direction_costs = {}
        move_sets: list[str] = self.getMoves(start, end)
        res = float('inf')
        while move_sets:
            moves = move_sets.pop()
            cures = self.evaluateMoveset(moves, direction_costs)
            if res > cures:
                res = cures
        return res

    def makePressCosts(self, sub_direction_costs=None, move_costs=None) -> dict[tuple, int]:
        if move_costs is None:
            move_costs = {}
        res = {}
        for e in self.positions:
            for f in self.positions:
                movesets: list = move_costs.get((e, f), self.getMoves(e, f))
                values = set()
                for moves in movesets:
                    val = self.evaluateMoveset(moves, sub_direction_costs)
                    values.add(val)
                res[(e, f)] = min(values)
        return res

def makeCompoundCosts(subpads:list[Keypad]):
    cur_costs={}
    while subpads:
        pad:Keypad=subpads.pop()
        cur_costs=pad.makePressCosts(cur_costs)
    return cur_costs


def print_dists(dists: dict[tuple[str, str], int]):
    L = list(set(e[0] for e in dists))
    L.sort()
    print(" " + "".join(L))
    for e in L:
        L2 = [str(dists[(e, f)]) for f in L]
        print(e + "".join(L2))


def printfn(els: str, move_costs):
    print("", *els, sep="\t")
    for e in els:
        L = [move_costs[(e, f)] for f in els]
        print(e, *L, sep="\t")


NUM_KEYPAD = Keypad('789 456 123  0A')
DIR_KEYPAD = Keypad(' ^A <v>')

def testfn():
    X = []
    costs={}
    res=NUM_KEYPAD.evaluateMoveset('029A',costs)
    print(res)
    for e in [NUM_KEYPAD, DIR_KEYPAD, DIR_KEYPAD]:
        X.append(e)
        costs=makeCompoundCosts(X[:])
        res=NUM_KEYPAD.evaluateMoveset('029A', costs)
        print(res)
    return costs

FINAL=testfn()
"""
029A: 68
980A: 60
179A: 68
456A: 64
379A: 64
"""



def process_1(data):
    res = 0
    for entry in data:
        score = int(entry[:-1])
        price = NUM_KEYPAD.evaluateMoveset(entry, FINAL)
        print(entry,score,price,score*price)
        res+=score*price
    return res


def process_2(data):
    res = 0
    for entry in data:
        score = int(entry[:-1])
        advanced=makeCompoundCosts([NUM_KEYPAD]+[DIR_KEYPAD]*25)
        price = NUM_KEYPAD.evaluateMoveset(entry, advanced)
        print(entry,score,price,score*price)
        res+=score*price
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
    runprocess(process_2, ["t", ""])
    return


if __name__ == "__main__":
    main()
