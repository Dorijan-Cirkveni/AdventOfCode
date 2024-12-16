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

def signum(n):
    return int(n>=0)+int(n>0)

def process_entry(
        start: numpy.array, step: numpy.array, moves: numpy.array, wrap: numpy.array, result: list[list[int]]
):
    start += step * moves
    start %= wrap
    start -= wrap // 2
    result[signum(start[0])][signum(start[1])] += 1
    return


def process_1(data, moves_int: int = 100, dimensions=(101, 103)):
    moves = numpy.array([moves_int] * len(dimensions)) % dimensions
    RES = [[0]*3 for _ in 3*[0]]
    for entry in data:
        if ' ' not in entry:
            dimensions=tuple([int(e) for e in entry.split(',')])
            moves = numpy.array([moves_int] * len(dimensions)) % dimensions
            continue
        processed=preprocess(entry)
        start, step = processed
        # step%=dimensions
        if any(start%dimensions-start)!=0:
            raise Exception(start,dimensions)
        process_entry(start, step, moves, numpy.array(dimensions), RES)
    res=1
    for e in RES:
        print(e)
    for i in range(-1,1):
        for j in range(-1,1):
            res*=RES[i][j]
    return res

def process_tree(
        start: numpy.array, step: numpy.array, wrap: numpy.array, result: list[list[str]]
):
    start += step
    start %= wrap
    a,b=start
    a:int
    b:int
    temp:list[str]=result[b]
    temp[a]='.'
    return

def doDisplay(positions:list[numpy.array],dimensions:tuple=(101, 103)):
    RES = [[' ']*dimensions[0] for _ in range(dimensions[1])]
    for pos in positions:
        RES[pos[1]][pos[0]]='.'
    return RES

def printDisplay(RES):
    print("_"*160)
    for E in RES:
        print("".join(E))

def doStep(positions:list[numpy.array],moves:list[numpy.array],dimensions:tuple=(101, 103)):
    for i,(cur,delta) in enumerate(zip(positions,moves)):
        cur+=delta
        cur%=dimensions
        positions[i]=cur
    return

def getNeigh(M,i,j,target,curset:set):
    for di,dj in [(i,j-1),(i,j+1)]:
        if M[di][dj]!=target:
            continue
        curset.add((di,dj))
    return

def traverseIsland(M,e,land:str,checked:str):
    curset={e}
    count=0
    while curset:
        nexset=set()
        for i,j in curset:
            M[i][j]=checked
            count+=1
            getNeigh(M,i,j,land,nexset)
        curset=nexset
    return count

def detectClumps(M:list[list[str]], threshold=20, land:str='.', cleared:str='█'):
    M.append([' ' for _ in M[0]])
    res=False
    for i,E in enumerate(M):
        E.append(' ')
        for j,e in enumerate(E):
            if e!=land:
                continue
            cur_res=traverseIsland(M,(i,j),land,cleared)
            if cur_res>=threshold:
                res=True
                continue
            traverseIsland(M, (i, j),cleared,land)
    return res


def process_2(data, dimensions=(101, 103)):
    positions=[]
    moves=[]
    for entry in data:
        if ' ' not in entry:
            dimensions=tuple([int(e) for e in entry.split(',')])
            continue
        processed=preprocess(entry)
        start, step = processed
        positions.append(start)
        moves.append(step)
    threshold=int('0'+input("Clump threshold:"))
    batch=int('0'+input("Batch size:"))
    batch=batch if batch else 1000
    batchp=int('0'+input("Batch print size:"))
    batchp=batchp if batch else 100
    res=0
    order=''
    M=doDisplay(positions,dimensions)
    det=detectClumps(M)
    while not order:
        while not det and (det is None or res%batch):
            if not res%batchp:
                print(res)
            res+=1
            doStep(positions,moves,dimensions)
            M=doDisplay(positions,dimensions)
            det=detectClumps(M,threshold)
        printDisplay(M)
        print(det)
        order=input(f"Move {res}:")
        det=None
    return res


TASK = __file__.split('\\')[-1][:-3]


def runprocess_withinputfrom(process: callable, suffix: str = "", *args):
    inputbase = f"..\\inputs\\{TASK}{suffix}.txt"
    data = read(inputbase)
    if data is not None:
        result = process(data, *args)
        print(f"Result for {suffix}: {result}")


def runprocess(process: callable, input_files=None, *args):
    if input_files is None:
        input_files = [""]
    for suffix in input_files:
        runprocess_withinputfrom(process, suffix, *args)


def main():
    runprocess(process_2, ["t", ""])
    return


if __name__ == "__main__":
    main()
