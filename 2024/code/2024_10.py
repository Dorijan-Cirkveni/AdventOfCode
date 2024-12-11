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


def preprocess(i:int,s:str,starts:dict):
    for j,e in enumerate(s):
        if e=='0':
            starts[(i,j)]=1

def get_neigh(mat:list,e:tuple,v,target:str,nexset:defaultdict[tuple,int]):
    i,j=e
    for nei,nej in [(i,j-1),(i,j+1),(i-1,j),(i+1,j)]:
        cur=mat[nei][nej]
        if cur==target:
            nexset[(nei,nej)]+=v



def process_1(data):
    for E in data:
        E+=' '
    data.append(' '*len(data[0]))
    curset=dict()
    for i,entry in enumerate(data):
       preprocess(i,entry,curset)
    for i in range(1,10):
        c=str(i)
        nexset=defaultdict(int)
        for E,v in curset.items():
            get_neigh(data,E,v,c,nexset)
        curset=nexset
    return sum(curset.values())


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
