
def read(filepath):
    with open(filepath, 'r') as file:
        M = file.read().split('\n')
    return M


def preprocess(M):
    for e in M:
        e += ' '
    M.append(' ' * len(M[-1]))
    RES =[list(e) for e in M]
    for E in RES:
        E.append(' ')
    return RES


class Matrix:
    def __init__(self, M):
        self.M = preprocess(M)
        self.i = -1
        self.j = -1
        self.dir:tuple[int,int] = -1, 0
        return

    def getNex(self, di, dj):
        nei = self.i + di
        nej = self.j + dj
        return nei, nej

    def step(self):
        self.M[self.i][self.j] = "$"
        nei,nej=-1,-1
        for i in range(4):
            nei, nej = self.getNex(*self.dir)
            if self.M[nei][nej] != "#":
                self.i, self.j = nei, nej
                break
            print(nei, nej)
            self.dir = self.dir[1], -self.dir[0]
        return self.M[nei][nej]!="$"

    def count(self):
        for i, s in enumerate(self.M):
            if "^" in s:
                self.i, self.j = i, s.index('^')
                break
        res = 0
        while self.M[self.i][self.j] != ' ':
            res += self.step()
        return res


def process_1(data):
    M = Matrix(data)
    res = M.count()
    return res


def process_2(data):
    return process_1(data)


TASK = __file__.split('\\')[-1][:-3]


def runprocess(process: callable):
    inputbase = f"..\\inputs\\{TASK}.txt"
    data = read(inputbase)
    datatemp = '''....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...'''.split('\n')
    result = process(datatemp)
    print(result)
    result = process(data)
    print(result)


def main():
    runprocess(process_2)
    return


if __name__ == "__main__":
    main()
