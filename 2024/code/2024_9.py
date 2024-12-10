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
    last:Optional['Fragment'] = None

    def occupy_last(self,new:'Fragment'):
        last:Fragment=self.last
        if last.id>=0:
            return -1
        diff=last.size-new.size
        if diff<0:
            return diff
        prev:Fragment=last.last
        last.last=new
        new.last=prev
        if diff==0:
            self.last=new
        last.size=diff
        return diff

    def print(self,limit=100):
        if limit<=0:
            return "..."
        cur=f"[{str(self.id) if self.id>=0 else 'X'}:{self.size}]"
        limit-=len(cur)
        last="|"
        if self.last:
            last=self.last.print(limit)
        return last+cur

def diffprint(cur,last,groups=5):
    d=len(last)-len(cur)
    cur+=" "*d
    last+=" "*(-d)
    res=''
    for a,b in zip(cur,last):
        if a==b and a not in protected:
            res+=' '
        else:
            res+=a
    return res


def preprocess_2(s:str)->tuple[Fragment,dict]:
    last=None
    free={}
    ind=0
    used=True
    pending_append=None
    rawind=0
    for i,e in enumerate(s):
        size=int(e)
        cur=ind if used else -1
        fr=Fragment(cur,size,last)
        if size:
            if pending_append is not None:
                L,remind=pending_append
                L.append((remind,fr))
                pending_append=None
            if not used:
                pending_append=free.setdefault(size,[]),rawind
            last=fr
        used=not used
        ind+=used
        rawind+=size
    if used:
        free[last.size].pop()
        last=last.last
    print({e:[(f[0],f[1].last.size) for f in v] for e,v in free.items()})
    return last,free


def compact_2(last:Fragment, free:dict):
    right_arch=Fragment(0,0,last)
    right_cur_arch=right_arch
    lastprint=right_arch.print()
    while free:
        nex=last.last
        target=last.size if last.id>=0 else -1
        possible={e for e in free if e>=target}
        if possible:
            print("Possible")
            chosen=min(possible)
            que:list=free[chosen]
            ff:Fragment
            ind,ff=heapq.heappop(que)
            if not que:
                free.pop(chosen)
            diff=ff.occupy_last(last)
            ind+=last.size
            if diff:
                print("New")
                que=free.setdefault(diff,[])
                heapq.heappush(que,(ind,ff))
        else:
            right_cur_arch.last=last
            right_cur_arch=last
        last=nex
        right_cur_arch.last=last
        nowprint=right_arch.last.print()
        print(diffprint(nowprint,lastprint))
        lastprint=nowprint
    return right_arch.last

def checksum(disk:list[int])->int:
    res=0
    for i,e in enumerate(disk):
        res+=i*e
    ind=0
    return res


def checksum_2(last:Fragment)->int:
    L=[]
    while last:
        L.append((last.id,last.size))
        last=last.last
    res=0
    ind=0
    while L:
        cur_id,cur_size=L.pop()
        cur_size+=ind
        temp=cur_size*(cur_size+1)//2
        temp-=ind*(ind+1)//2
        res+=temp*cur_id
        ind=cur_size
    return res



def process_1(data):
    res=0
    for entry in data:
        processed=preprocess(entry)
        compact(processed)
        cures=checksum(processed)
        res+=cures
    return res


def process_2(data):
    res=0
    for entry in data:
        processed,free=preprocess_2(entry)
        print(processed.print())
        resf=compact_2(processed,free)
        print(resf.print())
        cures=checksum_2(resf)
        print(cures)
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
