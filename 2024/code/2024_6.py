def read(filepath):
    with open(filepath, 'r') as file:
        M = file.read().split('\n')
    return M


def preprocess(M):
    for e in M:
        e += ' '
    M.append(' ' * len(M[-1]))
    RES = [list(e) for e in M]
    for E in RES:
        E.append(' ')
    return RES


DIRECTIONS = {
    (-1, 0): 'W',
    (0, -1): 'A',
    (0, 1): 'S',
    (1, 0): 'D'
}


class Matrix:
    def __init__(self, M):
        self.M = preprocess(M)
        self.start = -1, -1
        for i, s in enumerate(self.M):
            if "^" in s:
                self.start = i, s.index('^')
                break
        self.set(*self.start, '.')
        return

    def get(self, i, j):
        return self.M[i][j]

    def set(self, i, j, v):
        self.M[i][j] = v

    def getNex(self, i, j, di, dj):
        nei = i + di
        nej = j + dj
        return nei, nej

    def step(self, cur, dir):
        neigh = -1, -1
        for i in range(4):
            neigh = self.getNex(*cur, *dir)
            if self.get(*neigh) != "#":
                cur = neigh
                break
            dir = dir[1], -dir[0]
        return cur, dir

    def count(self, cur):
        res = 1
        delta = -1, 0
        while self.get(*cur) != ' ':
            self.set(*cur, DIRECTIONS[delta])
            cur, delta = self.step(cur, delta)
            res += self.get(*cur) == '.'
        return res

    def log(self, cur, delta=(-1, 0)):
        LD = set()
        while self.get(*cur) != ' ':
            new, newdelta = self.step(cur, delta)
            E = (cur, newdelta, new)
            if E in LD:
                return None
            LD.add(E)
            cur, delta = new, newdelta
        return {e[2] for e in LD}

    def all_loops(self, start):
        LD = self.log(start)
        res = 0
        i=0
        print(len(LD))
        for new in LD:
            temp=self.get(*new)
            self.set(*new, '#')
            RES = self.log(start)
            if not RES:
                res += 1
            self.set(*new, temp)
            i+=1
            if i%100==0:
                print((i,len(LD)))
        return res


def process_1(data):
    M = Matrix(data)
    res = M.count(M.start)
    return res


def process_2(data):
    M = Matrix(data)
    res=M.all_loops(M.start)
    return res


TASK = __file__.split('\\')[-1][:-3]


def runprocess(process: callable):
    inputbase = f"..\\inputs\\{TASK}.txt"
    data = read(inputbase)
    result = process(data)
    print(result)


def main():
    runprocess(process_2)
    return


if __name__ == "__main__":
    main()
