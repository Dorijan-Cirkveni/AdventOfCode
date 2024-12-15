import numpy


def read(filepath):
    M = None
    try:
        file = open(filepath, 'r')
        M = file.read().split('\n\n')
        file.close()
    except Exception as err:
        print(err)
    return M


def process_line(s: str) -> numpy.array:
    ind = s.index(':')
    s2 = s[ind + 2:]
    L=s2.split(', ')
    L2=[int(e[2:]) for e in L]
    res = numpy.array(L2)
    return res


def preprocess(s: str):
    L = s.split('\n')
    a, b, target = [process_line(e) for e in L[:3]]
    return a, b, target


def calculate_best(first, second, target):
    print(first)
    print(second)
    print(target)
    M=numpy.column_stack([first,second])
    if numpy.linalg.det(M)==0:
        ratio=
    res=numpy.linalg.solve([first,second],target)
    print(res)
    return 0


def process_1(data):
    res = 0
    for entry in data:
        A: tuple[int, int]
        B: tuple[int, int]
        T: tuple[int, int]
        A, B, T = preprocess(entry)
        res = calculate_best(A, B, T)
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
