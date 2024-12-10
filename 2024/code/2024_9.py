import heapq
from collections import deque
from dataclasses import dataclass
from typing import Optional


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

@dataclass
class Fragment:
    id:int
    size:int
    branch:Optional['Fragment'] = None

    def occupy(self,other:'Fragment'):
        other.branch=self
        self.size-=other.size
        return occupy_fragment

def occupy_fragment(head:Fragment,new:Fragment):
    arch=Fragment(0,0,head)
    cur_arch=arch
    while head and head.id>=0:
        cur_arch=head
        head=cur_arch.branch
    if head:
        cur_arch.branch=head.occupy(new)
    return arch.branch

def flatten(fr:Fragment,res:list):
    while fr:
        res.append(fr)
        fr=fr.branch
    return


def preprocess_2(s:str):
    L=[]
    free={}
    ind=0
    used=True
    for i,e in enumerate(s):
        cur=ind if used else -1
        fr=Fragment(cur,int(e))
        if not used:
            free.setdefault(e,deque()).append(fr)
        L.append(fr)
        used=not used
        ind+=used
    return L,free

def compact_2(base:list[Fragment], free:dict):
    rightUsed=[]
    while free:
        used_fr:Fragment=base.pop()
        possible={e for e in free if e>=size}
        if possible:
            chosen=min(possible)
            que:deque=free[chosen]
            free_ind=que.pop()
            if not que:
                free.pop(chosen)
        else:
            rightUsed.append((ind,size))
        while


def checksum(disk:list[int])->int:
    res=0
    for i,e in enumerate(disk):
        res+=i*e
    return res



def process_1(data):
    res=0
    for entry in data:
        processed=preprocess(entry)
        compact(processed)
        print(processed[:100])
        cures=checksum(processed)
        res+=cures
    return res


def process_2(data):
    return process_1(data)


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
