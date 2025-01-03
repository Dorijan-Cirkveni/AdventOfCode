import json


def read(filepath):
    try:
        file = open(filepath, 'r')
        data = file.read()
        file.close()
    except Exception as err:
        print(err)
        return None
    return data


def preprocess_line(s: str):
    ind = s.index(': ')
    raw = s[ind + 2:]
    return raw


def preprocess_registers(s: str):
    L = s.split('\n')
    L2 = []
    for e in L:
        raw = preprocess_line(e)
        n = int(raw)
        L2.append(n)
    return L2


def preprocess_programs(s: str):
    L = s.split('\n')
    L2 = []
    for e in L:
        raw = preprocess_line(e)
        nL = json.loads(f'[{raw}]')
        L2.append(nL)
    return L2


def preprocess_data(data):
    ar, br = data.split('\n\n')
    A = preprocess_registers(ar)
    B = preprocess_programs(br)
    return A, B


class Computer:
    def __init__(self, registers: list[int]):
        self.pointer = 0
        self.registers = registers
        self.output = []

    def instantiate(self, new_first: int):
        new = Computer(self.registers)
        new.registers[0] = new_first
        return new

    def get_value(self, operand: int):
        if operand < 4:
            return operand
        if operand < 7:
            return self.registers[operand & 3]
        return 0

    def truncdiv(self, ind: int, combo):
        a = self.registers[0]
        a >>= combo
        self.registers[ind] = a

    def step(self, command: int, literal: int):
        combo = self.get_value(literal)
        match command:
            case 0:
                self.truncdiv(0, combo)
            case 1:
                self.registers[1] ^= literal
            case 2:
                combo &= 7
                self.registers[1] = combo
            case 3:
                if self.registers[0]:
                    self.pointer = literal
                    return
            case 4:
                self.registers[1] ^= self.registers[2]
            case 5:
                combo &= 7
                self.output.append(combo)
            case 6:
                self.truncdiv(1, combo)
            case 7:
                self.truncdiv(2, combo)
        self.pointer += 2
        return

    def process(self, instructions: list[int]):
        self.pointer = 0
        old = self.registers[0]
        while self.pointer < len(instructions) - 1:
            command, variable = instructions[self.pointer], instructions[self.pointer + 1]
            self.step(command, variable)
            match command:
                case 3:
                    old = self.registers[0]
                case 5:
                    simp = forwardStep(old)
                    ref = self.get_value(variable) & 7
                    assert ref & 7 == simp
        return self.output


def process_1(data):
    res = 0
    reqs, programs = preprocess_data(data)
    for program in programs:
        comp = Computer(reqs[:])
        output = comp.process(program)
        print(*output, sep=',')
        print(simplified(reqs[0]))
    return res


P2DATA = preprocess_data(read("..\\inputs\\2024_17.txt"))
P2COMP = Computer(P2DATA[0])


def test_part2(new_first:int):
    assert isinstance(new_first,int)
    cur = P2COMP.instantiate(new_first)
    program=P2DATA[1][0]
    res = cur.process(program)
    return res


def forwardStep(first: int):
    second = first & 7
    second ^= 2
    third = first >> second
    second ^= third
    second ^= 3
    return second & 7


def listToInt(cur: list):
    val = 0
    for i, e in enumerate(cur):
        val |= e << (i * 3)
    return val


def simplified(start: int):
    res = []
    while start:
        cures = forwardStep(start)
        start >>= 3
        res.append(cures)
    return res

def simplified_check()


def isMatchToKnown(value, found, known):
    masked = value & found
    missed = masked & (~known)
    return missed == 0


def findMaskFor(first: int, found: int, known: int, target: int):
    second = first ^ 2
    target ^= 3
    target ^= second
    target <<= second
    if not isMatchToKnown(target, found, known):
        return None
    found |= 7 << second
    known |= target
    return found >> 3, known >> 3


def findOptionsFor(target: int, found: int, known: int, limit: int, cur: list):
    RES = []
    if limit > 8:
        limit = 8
    seconds = [i for i in range(limit) if isMatchToKnown(i ^ 2, found, known)]
    found |= 7
    for second in seconds:
        first = second ^ 2
        res = findMaskFor(first, found, known | first, target)
        solution = cur + [first]
        if res is None:
            continue
        a, b = res
        solres = solution, a, b
        n=listToInt(solution)
        print(solres, oct(n), test_part2(n))
        RES.append(solres)
    return RES


def checkAll(program: list[int]):
    limit = len(program) * 3
    found = 63 << limit
    known = 0
    empty = []
    starter = (empty, found, known)
    curlist = [starter]
    for i, target in enumerate(program):
        nexlist = []
        while curlist:
            cur, found, known = curlist.pop()
            temp = findOptionsFor(target, found, known, limit, cur)
            nexlist += temp
        curlist = nexlist
        print(f"{i + 1}/{len(program)}", len(nexlist))
        limit -= 3
    best = 1 << 32
    while curlist:
        cur = curlist.pop()[0]
        val = listToInt(cur)
        output = test_part2(val)
        print(oct(val), val, output, program)
        if val < best:
            best = val

    return best


def process_2(data):
    reqs, programs = preprocess_data(data)
    program = programs[0]
    for X in [6, 42, 300]:
        print(X, oct(X), test_part2(X))
    program_input = [1, 4, 5]
    print(program_input)
    res = checkAll(program_input[:])
    for i in [res]:
        print(i, test_part2(i))
    return res


TASK = __file__.split('\\')[-1][:-3]


def runprocess_withinputfrom(process: callable, suffix: str = ""):
    inputbase = f"..\\inputs\\{TASK}{suffix}.txt"
    data = read(inputbase)
    if data is not None:
        result = process(data)
        print(f"Result for {suffix}: {result}")
        return result


def runprocess(process: callable, input_files=None):
    if input_files is None:
        input_files = [""]
    for suffix in input_files:
        runprocess_withinputfrom(process, suffix)


def main():
    runprocess(process_2, [""])
    return


if __name__ == "__main__":
    main()
