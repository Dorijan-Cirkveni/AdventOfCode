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
    def pop_group(self):
        key=heapq.heappop(self.pq)
        value=self.groups.pop(key)
        return key,value


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
    def makeDirectionCosts(self,sub_direction_costs=None):
        if sub_direction_costs is None:
            sub_direction_costs = {}
        dir_costs={e:{} for e in self.directions}
        gpq=GroupedPriorityQueue()
        for e in dir_costs:
            gpq.add(1,(e,e))
        while gpq.check():
            cur_cost,values=gpq.pop_group()
            while values:
                cur,target=values.pop()
                if dir_costs[cur].get(target,cur_cost+1)<=cur_cost:
                    continue
                dir_costs[cur][target]=cur_cost
                for dest in self.getNeigh(*target):
                    if dir_costs[cur].get(dest,cur_cost+1)<=cur_cost:
                        continue
                    curdir=self.directions[cur]
                    val=min(curdir[dest])
                    cost=sub_direction_costs.get(val,1)
                    cost+=cur_cost
                    gpq.add(cost,(cur,dest))

        return dir_costs

num_keypad=Keypad('789 456 123  0A')
dir_keypad=Keypad(' ^A <v>')
test=num_keypad.makeDirectionCosts()
for e,v in test.items():
    print(e,v)


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
