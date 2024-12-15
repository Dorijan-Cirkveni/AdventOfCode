import json
from collections import defaultdict

import numpy


def read(filepath):
    M = None
    try:
        file = open(filepath, 'r')
        raw = file.read()
        M=raw.split('\n') if raw else []
        file.close()
    except Exception as err:
        print(err)
    return M


def preprocess(s: str):
    L = s.split(' ')
    L2 = []
    for e in L:
        e2 = numpy.fromstring(e[2:], int, sep=',')
        L2.append(e2)
    return L2


def process_entry(
        start: numpy.array, step: numpy.array, moves: numpy.array, wrap: numpy.array, result: list[list[int]]
):
    start += step * moves
    start %= wrap
    start -= wrap // 2
    # result[start[0] < 0][start[1] < 0] += 1
    return 0 not in start


def process_1(data, moves_int: int = 100, dimensions=(101, 103)):
    moves = numpy.array([moves_int] * len(dimensions)) % dimensions
    RES = [[0, 0], [0, 0]]
    quad = []
    res = 0
    for entry in data:
        processed=preprocess(entry)
        start, step = processed
        res += process_entry(start, step, moves, numpy.array(dimensions), RES)

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
    runprocess(process_1, ["t", ""])
    runprocess(process_2, ["t", ""])
    return


if __name__ == "__main__":
    main()
