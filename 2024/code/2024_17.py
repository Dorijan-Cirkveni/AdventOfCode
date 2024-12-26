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
    regs, programs = preprocess_data(data)
    for program in programs:
        comp = Computer(regs[:])
        output = comp.process(program)
        print(*output, sep=',')
        print(simplified(regs[0]))
    return res


def forwardStep(first: int):
    second = first & 7
    second ^= 2
    third = first >> second
    second ^= third
    second ^= 3
    return second & 7


def getExp(start):
    X = [1 << start]
    X.append(X[-1] << 1)
    X.append(X[-1] << 1)
    return X


def findMaskFor(first: int, found: int, known: int, target: int):
    found |= 3
    # first &= 7
    second = first ^ 2
    iters = ['']

    target^=3

    for i in range(second, second + 3):
        exp = 1 << i
        if found & exp:
            add = '01'[known & exp != 0]
            iters = [add + e for e in iters]
            continue
        found |= exp
        nexiters = []
        for e in iters:
            nexiters += ['0' + e, '1' + e]
    res = []
    nexfirst = first >> 3
    found >>= 3
    for s in iters:
        chosen = int(s, 2)
        newsecond = chosen ^ second
        newsecond &= 7
        if newsecond != target:
            continue
        newknown = known | (chosen << second)
        newel = nexfirst, found, newknown >> 3
        res.append(newel)
    return res


def simplified(start: int):
    res = []
    while start:
        cures = forwardStep(start)
        start >>= 3
        res.append(cures)
    return res


def find_lowest(program: list):
    for start in range(8):
        tres = 0
    return tres


def process_test(data):
    regs, programs = preprocess_data(data)
    program = programs[0]
    print(program)
    tests = [
        [1],
        [7, 1],
        []
    ]
    for testval in [1, 2, 10, 69, 420]:
        regs[0] = testval
        comp = Computer()


def process_2(data):
    regs, programs = preprocess_data(data)
    program = programs[0]
    print(program)
    res = find_lowest(program[:])
    for i in [res]:
        regs[0] = i
        comp = Computer(regs[:])
        output = comp.process(program)
        check = find_lowest(output)
        print(f"{i}:", output, check)
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
    runprocess(process_1, [""])
    return


if __name__ == "__main__":
    main()
