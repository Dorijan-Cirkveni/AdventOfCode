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


def preprocess_all(data):
    curset=defaultdict(set)
    ind=0
    for i,entry in enumerate(data):
        for j,e in enumerate(entry):
            if e=='0':
                curset[(i,j)].add(ind)
                ind+=1
        data[i]=entry+' '
    data.append(' '*len(data[0]))
    return curset


def preprocess_all_2(data):
    curset=defaultdict(int)
    for i,entry in enumerate(data):
        for j,e in enumerate(entry):
            if e=='0':
                curset[(i,j)]=1
        data[i]=entry+' '
    data.append(' '*len(data[0]))
    return curset

def get_neigh(mat:list,e:tuple,vs:set,target:str,nexset:defaultdict[tuple,set]):
    i,j=e
    for nei,nej in [(i,j-1),(i,j+1),(i-1,j),(i+1,j)]:
        cur=mat[nei][nej]
        if cur==target:
            nexset[(nei,nej)]|=vs

def get_neigh_2(mat:list,e:tuple,v:int,target:str,nexset:defaultdict[tuple,int]):
    i,j=e
    for nei,nej in [(i,j-1),(i,j+1),(i-1,j),(i+1,j)]:
        cur=mat[nei][nej]
        if cur==target:
            nexset[(nei,nej)]+=v



def process_1(data):
    curset=preprocess_all(data)
    print(curset)
    for i in range(1,10):
        c=str(i)
        nexset=defaultdict(set)
        for E,v in curset.items():
            get_neigh(data,E,v,c,nexset)
        curset=nexset
        print(curset)
    res=0
    for V in curset.values():
        res+=len(V)
    return res

def process_2(data):
    curset:defaultdict[tuple,int]=preprocess_all_2(data)
    print(curset)
    for i in range(1,10):
        c=str(i)
        nexset:defaultdict[tuple,int]=defaultdict(int)
        for E,v in curset.items():
            get_neigh_2(data,E,v,c,nexset)
        curset=nexset
        print(curset)
    res=0
    for V in curset.values():
        res+=V
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
