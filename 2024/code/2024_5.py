import re
from collections import defaultdict


def read(filepath):
    with open(filepath,'r') as file:
        MM=file.read().split('\n\n')
    for i,e in enumerate(MM):
        MM[i]=e.split('\n')
    return MM

def setup_reqs(order):
    reqs=defaultdict(set)
    while order:
        a,b=order.pop().split('|')
        reqs[b].add(a)
    return reqs

def process_entry(entry,reqs:dict):
    L=entry.split(',')
    forbidden=set()
    for e in L:
        if e in forbidden:
            return 0
        forbidden|=reqs.get(e,set())
    return int(L[len(L)//2])


def process_1(MM):
    reqs=setup_reqs(MM[0])
    res=0
    for e in MM[1]:
        res+=process_entry(e,reqs)
    return res

def process_2(M):
    res = 0
    for e in M[1]:
        return 0
    return res


TASK=__file__.split('\\')[-1][:-3]

def runprocess(process:callable):
    inputbase=f"..\\inputs\\{TASK}.txt"
    data=read(inputbase)
    result=process(data)
    print(result)

def runproc2():
    inputbase=f"..\\inputs\\{TASK}.txt"
    data=read(inputbase)
    result=defaultdict(int)
    for s in data[1]:
        result[len(s.split(','))&1]+=1
    print(result)

def main():
    runprocess(process_1)
    return


if __name__ == "__main__":
    main()
