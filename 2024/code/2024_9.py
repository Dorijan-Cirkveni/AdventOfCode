import heapq
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
    next:Optional['Fragment'] = None

    def add_to_left(self,left):
        new:Fragment
        if left:
            left.next=self
        self.last=left
        return self

    def insert_left(self,new):
        if new is None:
            return self
        new:Fragment
        last=self.last
        self.last=new
        new.last=last
        if last:
            last.next=new
        new.next=self
        return self

    def remove(self):
        last=self.last
        nex=self.next
        if last:
            last.next=nex
        if nex:
            nex.last=last
        return

    def occupy(self,new:'Fragment'):
        diff=self.size-new.size
        if diff<0:
            return diff
        new.last=self.last
        new.next=self
        self.last.next=new
        self.last=new
        self.size=diff
        if diff==0:
            self.remove()
        return diff

    def print(self,limit=100):
        if limit<=0:
            return "..."
        cur=f"[{str(self.id) if self.id>=0 else 'X'}:{self.size}]"
        limit-=len(cur)
        last="|"
        if self.last:
            self.last:Fragment
            last=self.last.print(limit)
        return last+cur

def comprint(cur,last,start,end):
    a=cur[start:end]
    b=last[start:end]
    if a==b:
        return " "*len(a)
    return a

def diffprint(cur,last,groupsize=5,offset=1):
    d=len(last)-len(cur)
    cur+=" "*d
    last+=" "*(-d)
    res=comprint(cur,last,0,offset)
    for i in range(offset,len(cur),groupsize):
        res+=comprint(cur,last,i,i+groupsize)
    return res


def preprocess_2(s:str)->tuple[Fragment,dict]:
    last=None
    free={}
    ind=0
    used=True
    rawind=0
    for i,e in enumerate(s):
        size=int(e)
        cur=ind if used else -1
        fr=Fragment(cur,size)
        if size:
            if not used:
                free.setdefault(size,[]).append((rawind,fr))
            last=fr.add_to_left(last)
        used=not used
        ind+=used
        rawind+=size
        print(last.print())
    if used:
        free[last.size].pop()
        last=last.last
        last.next.remove()
    return last,free,rawind


def compact_2(last:Fragment, free:dict, rawind=int):
    right_arch=Fragment(0,0,last)
    right_cur_arch=right_arch
    lastprint=right_arch.print()
    print("Status:",lastprint)

    while free and last:
        print({e:len(v) for e,v in free.items()})
        nex=last.last
        target=last.size if last.id>=0 else -1
        rawind-=last.size
        for e in set(free):
            E=free[e][0]
            if E[0]>rawind:
                free.pop(e)
        possible={e for e in free if e>=target}
        if possible:
            print("Possible")
            chosen=min(possible)
            que:list=free[chosen]
            ff:Fragment
            ind,ff=heapq.heappop(que)
            if not que:
                free.pop(chosen)
            diff=ff.occupy(last)
            ind+=last.size
            if diff:
                print("New")
                que=free.setdefault(diff,[])
                heapq.heappush(que,(ind,ff))
            last=Fragment(-1,last.size)
        if right_cur_arch.id==last.id:
            right_cur_arch.size+=last.size
        else:
            right_cur_arch.add_to_left(last)
            right_cur_arch=last
        last=nex
        right_cur_arch.add_to_left(last)
        nowprint=right_arch.print()
        print("Status:",diffprint(nowprint,lastprint))
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
        processed,free,size=preprocess_2(entry)
        print(processed.print())
        resf=compact_2(processed,free,size)
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
    runprocess(process_2,["t","q"])
    return


if __name__ == "__main__":
    main()
