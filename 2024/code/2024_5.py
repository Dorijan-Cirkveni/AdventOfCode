import re
from collections import defaultdict


def read(filepath):
    with open(filepath,'r') as file:
        MM=file.read().split('\n\n')
    for i,e in enumerate(MM):
        MM[i]=e.split('\n')
    return MM

def order(reqs:dict):
    counter={e:0 for e in reqs}
    for e,V in reqs.items():
        for f in V:
            counter.setdefault(f,0)
            counter[f]+=1
    curs=[e for e,v in counter.items() if not v]
    ind=-1
    while curs:
        nexes=[]
        while curs:
            cur=curs.pop()
            counter[cur]=ind
            for e in reqs[cur]:
                counter[e]-=1
                if not counter[e]:
                    nexes.append(e)
        ind-=1
        curs=nexes
    return counter



class Requirements:
    def __init__(self,order):
        reqs=defaultdict(set)
        while order:
            a,b=order.pop().split('|')
            reqs[b].add(a)
        self.reqs=reqs
        return

    def process_entry(self,entry):
        L=entry.split(',')
        forbidden=set()
        for e in L:
            if e in forbidden:
                return 0
            forbidden|=self.reqs.get(e,set())
        return int(L[len(L)//2])

    def filter_reqs(self,EL:list):
        SE=set(EL)
        res={}
        for k,S in self.reqs.items():
            S&=SE
            if S:
                res[k]=S
        return res



    def correct_entry(self,entry:str):
        EL=entry.split(',')
        valid=False
        for i,e in enumerate(EL):
            for j in range(i+1,len(EL)):
                if EL[j] in self.reqs[e]:
                    EL[i]=EL[j]
                    EL[j]=e
                    e=EL[i]
                    valid=True
        if valid:
            return int(EL[len(EL)//2])
        return 0


def process_1(MM):
    reqs=Requirements(MM[0])
    res=0
    for e in MM[1]:
        res+=reqs.process_entry(e)
    return res

def process_2(MM,debug=False):
    reqs=Requirements(MM[0])
    res=0
    for e in MM[1]:
        temp=reqs.correct_entry(e)
        if debug:
            print(f"{e}->{temp}",end=",")
        res+=temp
    return res


TASK=__file__.split('\\')[-1][:-3]

def runprocess(process:callable):
    inputbase=f"..\\inputs\\{TASK}.txt"
    data=read(inputbase)
    datatemp=[
        "75,97,47,61,53",
        "61,13,29",
        "1,2,3",
        "97,13,75,29,47"
    ]
    result=process([data[0][:],datatemp],True)
    print(result)
    result=process(data)
    print(result)

def main():
    runprocess(process_2)
    return


if __name__ == "__main__":
    main()
