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

def filter_reqs(EL:list,reqs):
    SE=set(EL)
    res={}
    for k,S in reqs.items():
        S&=SE
        if S:
            res[k]=S
    return res

def flatten_group_reqs(groups:dict,start):
    while groups[start]!=groups[groups[start]]:
        groups[start] != groups[groups[start]]


def group_reqs(reqs:dict):
    res={e:e for e in reqs}
    for e,v in reqs.items():
        while res[e]!=res[res[e]]:
            res[e]=res[]

def correct_entry(entry:str,reqs:dict):
    eL=entry.split(',')
    reqs=filter_reqs(EL,reqs)
    logged={}
    valid=False
    if valid:
        return int(L[len(L)//2])
    return 0

def process_2(MM):
    reqs=setup_reqs(MM[0])
    res=0
    for e in MM[1]:
        res+=correct_entry(e,reqs)
    return res


TASK=__file__.split('\\')[-1][:-3]

def runprocess(process:callable):
    inputbase=f"..\\inputs\\{TASK}.txt"
    data=read(inputbase)
    result=process(data)
    print(result)

def main():
    runprocess(process_2)
    return


if __name__ == "__main__":
    main()
