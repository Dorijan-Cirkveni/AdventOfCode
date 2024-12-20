import heapq
from collections import defaultdict
from dataclasses import dataclass
from heapq import heappush
from typing import Optional

from numpy.ma.extras import count_masked


def read(filepath):
    M=None
    try:
        file=open(filepath, 'r')
        M = file.read().split('\n')
        file.close()
    except Exception as err:
        print(err)
    return M


def preprocess(s:str):
    L=[]
    ind=0
    used=True
    for e in s:
        cur=[ind if used else -1]*int(e)
        L.extend(cur)
        used=not used
        ind+=used
    return L


def preprocess_2(s:str):
    L=[-2]
    ind=0
    rawind=0
    used=True
    free:dict[int,list[int]]={}
    for e in s:
        n=int(e)
        cur=[ind if used else -1]*n
        L.extend(cur)
        if not used:
            free.setdefault(n,[]).append(rawind)
        used=not used
        ind+=used
        rawind+=n
    return L,free

def find_first_free(free:dict[int,list[int]],minsize:int, limit:int):
    X=[]
    remove:set=set()
    for key, e in free.items():
        if key < minsize:
            continue
        if e[0]>=limit:
            remove.add(key)
            continue
        E=e[0],key,e
        X.append(E)
    for e in remove:
        free.pop(e)
    return min(X) if X else None

def get_first_free(free:dict[int,list[int]],minsize:int, limit:int):
    E=find_first_free(free, minsize, limit)
    if not E:
        return -1
    ind, size, heap=E
    heapq.heappop(heap)
    if not heap:
        free.pop(size)
    new_size=size-minsize
    if new_size:
        new_ind=ind+minsize
        heappush(free[new_size],new_ind)
    return ind

def compact(L:list):
    curFree=0
    while True:
        L.append(-2)
        while L[curFree]>=0:
            curFree+=1
        if L[curFree]==-2:
            L.pop()
            return
        L.pop()
        e=L.pop()
        L[curFree]=e
        while L[-1]<0:
            L.pop()

def compact_2(L:list, free:defaultdict[int,list[int]]):
    right=[]
    curind=len(L)-1
    while L[-1]!=-2:
        cur=L[-1]
        count=0
        while L[-1]==cur:
            L.pop()
            count+=1
        curind-=count
        if cur==-1:
            right+=[cur]*count
            continue
        free_spot=get_first_free(free,count,curind)
        if free_spot != -1:
            for i in range(free_spot+1,free_spot+count+1):
                L[i]=cur
            cur=-1
        right+=[cur]*count
    L.pop()
    right.reverse()
    return right

def checksum(disk:list[int])->int:
    res=0
    for i,e in enumerate(disk):
        if e<0:
            continue
        res+=i*e
    return res



def process_1(data):
    res=0
    for entry in data:
        if not entry:
            continue
        processed=preprocess(entry)
        compact(processed)
        cures=checksum(processed)
        res+=cures
    return res


def process_2(data):
    res=0
    for entry in data:
        if not entry:
            continue
        processed,free=preprocess_2(entry)
        processed=compact_2(processed,free)
        for e in '':
            print('.' if e==-1 else e,end='')
        cures=checksum(processed)
        res+=cures
    return res


TASK = __file__.split('\\')[-1][:-3]


def runprocess_withinputfrom(process: callable, suffix:str=""):
    inputbase = f"..\\inputs\\{TASK}{suffix}.txt"
    data = read(inputbase)
    if data is not None:
        result = process(data)
        print(f"Result for {suffix}: {result}")


def runprocess(process: callable, input_files=None):
    if input_files is None:
        input_files = [""]
    for suffix in input_files:
        runprocess_withinputfrom(process,suffix)


def main():
    runprocess(process_2,["t",""])
    return


if __name__ == "__main__":
    main()
