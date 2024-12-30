import heapq
import math
from collections import defaultdict


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
    return s

DIRECTIONS={
    '^':(-1,0),
    '<':(0,-1),
    'v':(1,0),
    '>':(0,1)
}
def diffToSet(start:int,end:int,c1:str,c2:str,curset:set):
    if start==end:
        return
    curset.add(c1 if start>end else c2)
    return

def combine_directions(curset:set[str],dirset:dict,nexset:defaultdict[str,set]):
    for cur in curset:
        for cdir,val in dirset.items():
            nexset[cdir].add(cur+val)

class GroupedPriorityQueue:
    def __init__(self):
        self.pq=[]
        self.groups={}
    def add(self,key,value):
        if key in self.groups:
            self.groups[key].add(value)
        else:
            heapq.heappush(self.pq,key)
            self.groups[key]={value}
    def check(self):
        return bool(self.pq)
    def pop_group(self)->[int,set]:
        key=heapq.heappop(self.pq)
        value=self.groups.pop(key)
        return key,value
    def pop(self):
        key=self.pq[0]

def add_A(direction_costs:dict[tuple,int],sub_direction_costs:dict[tuple,dict[tuple,int]], ack:tuple):
    res=float('inf')
    for last,cost in direction_costs.items():
        if last == ack:
            continue
        cost+=sub_direction_costs[last][ack]
        if res>cost:
            res=cost
    assert res!=float('inf')
    return int(res)


class Keypad:
    def __init__(self,raw:str):
        raw+=' '*16
        positions={e:divmod(i,4) for i,e in enumerate(raw) if e!=' '}
        self.neigh=[set() for _ in range(16)]
        for i in range(4):
            for j in range(3):
                a=i*4+j
                self.setNeigh(a,a+1,raw)
                a=j*4+i
                self.setNeigh(a,a+4,raw)
        self.directions:dict[tuple,dict[tuple,set]]={}
        for si,sj in positions.values():
            curdir:dict[tuple,set]={}
            self.directions[(si,sj)]=curdir
            for (ei,ej) in positions.values():
                curset=set()
                curdir[(ei,ej)]=curset
                diffToSet(si,ei,'^','v',curset)
                diffToSet(sj,ej,'<','>',curset)
        self.positions=positions
        return
    def setNeigh(self,a,b,raw:str):
        if ' ' in raw[a]+raw[b]:
            return
        self.neigh[a].add(b)
        self.neigh[b].add(a)
    def getNeigh(self,a,b):
        a<<=2
        a|=b
        nei=self.neigh[a]
        return {divmod(e,4) for e in nei}
    def getMoves(self,sc:str,ec:str)->list[str]:
        start=self.positions[sc]
        end=self.positions[ec]
        cur_val={start:{''}}
        while end not in cur_val:
            nex_val=defaultdict(set)
            for cur,curset in cur_val.values():
                dirset=self.directions[cur]
                combine_directions(curset,dirset,nex_val)
        res=cur_val.pop(end)
        return list(res)
    def evaluateMoveset(self,moves:str,direction_costs=None,last:str='A'):
        if direction_costs is None:
            direction_costs = {}
        res=0
        for e in moves:
            res+=direction_costs.get((last,e),1)
            last=e
        return res
    def getComplexity(self,start:str,end:str,direction_costs=None):
        if direction_costs is None:
            direction_costs = {}
        move_sets:list[str]=self.getMoves(start,end)
        res=float('inf')
        while move_sets:
            moves=move_sets.pop()
            cures=self.evaluateMoveset(moves,direction_costs)
            if res>cures:
                res=cures
        return res
    def makeMoveCosts(self,sub_direction_costs=None)->dict[tuple,dict[tuple,int]]:
        if sub_direction_costs is None:
            sub_direction_costs = {}
        dir_costs:dict[tuple,dict[tuple,dict[tuple,int]]]={e:{} for e in self.directions}
        gpq=GroupedPriorityQueue()
        for e in dir_costs:
            gpq.add(1,(e,'A',e))
        while gpq.check():
            cur_cost,values=gpq.pop_group()
            while values:
                cur,last,target=values.pop()
                if dir_costs[cur].setdefault(target,{}).get(last,cur_cost+1)<=cur_cost:
                    continue
                dir_costs[cur][target][last]=cur_cost
                for dest in self.getNeigh(*target):
                    curdir=self.directions[cur]
                    val=min(curdir[dest]) if curdir[dest] else 'A'
                    if dir_costs[cur].setdefault(dest,{}).get(val,cur_cost+1)<=cur_cost:
                        continue
                    cost=sub_direction_costs.get(last,{}).get(val,1)
                    cost+=cur_cost
                    gpq.add(cost,(cur,val,dest))
        res={}
        for e1, v1 in dir_costs.items():
            res1={}
            res[e1]=res1
            for e2, v2 in v1.items():
                res2=add_A(v2,sub_direction_costs,self.positions['A'])
                res1[e2]=res2
        return res
    def makeDirCosts(self,sub_direction_costs=None):
        move_costs=self.makeMoveCosts(sub_direction_costs)
        anti_positions={e:i for i,e in self.positions.items()}
        res={}
        for e,v in move_costs.items():
            e:tuple[int,int]
            res1={}
            f=anti_positions[e]
            res[f]=res1
            for e2,v2 in v.items():
                e2:tuple[int,int]
                f2=anti_positions[e2]
                res1[f2]=v2
        return res

num_keypad=Keypad('789 456 123  0A')
dir_keypad=Keypad(' ^A <v>')
def print_dists(dists:dict[tuple,dict[tuple,int]]):
    L=list(dists)
    L.sort()
    print(" "+"".join(L))
    for e in L:
        V=dists[e]
        L2=[str(V[f]) for f in L]
        print(e+"".join(L2))

first=dir_keypad.makeDirCosts()
second=dir_keypad.makeDirCosts(first)
third=num_keypad.makeDirCosts(second)
print_dists(first)
print_dists(second)
print_dists(third)


def process_1(data):
    res=0
    for entry in data:
        processed=preprocess(entry)
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
