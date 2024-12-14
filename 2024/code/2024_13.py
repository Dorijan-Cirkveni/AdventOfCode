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


def process_line(s: str)->tuple[int,int]:
    ind = s.index(':')
    s2 = s[ind + 2:]
    L = s.split(', ')
    a = int(L[0][2:])
    b = int(L[1][2:])
    return a, b


def preprocess(s: str):
    L = s.split("\n")
    RES:list[tuple[int,int]] = [process_line(e) for e in L]
    return RES


def isSameDirection(E1: tuple[int, int], E2: tuple[int, int]):
    return E1[0] * E2[1] == E2[0] * E1[1]

def calculate_best(A,B,target):
    for i in range(101):
        div_a
        target=target[0]-A[0],target[1]


def process_1(data):
    res = 0
    for entry in data:
        processed:list[tuple[int,int]] = preprocess(entry)

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
