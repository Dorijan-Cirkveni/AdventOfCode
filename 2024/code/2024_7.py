from os.path import curdir


def read(filepath):
    with open(filepath, 'r') as file:
        M = file.read().split('\n')
    return M


def preprocess(s:str):
    ca,cb=s.split(': ')
    return int(ca),[int(e) for e in cb.split()]

def check(target:int,parts:list,use_concat=False):
    L={target:""}
    while parts:
        NL={}
        e=parts.pop()
        for cur,v in L.items():
            if e<=cur:
                NL[cur-e]='+'+v
            if not parts:
                continue
            if cur%e==0:
                NL[cur//e]='*'+v
            if use_concat and str(cur).endswith(str(e)):
                lim=-len(str(e))
                new=int('0'+str(cur)[:lim])
                NL[new]='|'+v
        L=NL
    return L.get(0,'')



def process_1(data,use_concat=False):
    res=0
    res0=0
    for entry in data:
        processed=preprocess(entry)
        print(processed,end="->")
        ops=check(*processed,use_concat)
        print(ops)
        if ops:
            res+=processed[0]
    return res0,res


def process_2(data):
    return process_1(data,True)


TASK = __file__.split('\\')[-1][:-3]


def runprocess(process: callable):
    inputbase = f"..\\inputs\\{TASK}.txt"
    data = read(inputbase)
    result = process(data)
    print(result)


def main():
    runprocess(process_2)
    return

'''
5540634308465 too high
5540634308362
'''


if __name__ == "__main__":
    main()
