def read(filepath):
    with open(filepath, 'r') as file:
        M = file.read().split('\n')
    return M


def preprocess(s:str):
    ca,cb=s.split(': ')
    return int(ca),[int(e) for e in cb.split()]

def check_forward(target:int,parts:list):
    L={0:""}
    for cur in parts:
        NL={}
        for e in L:
            v=L[e]
            if e+cur<=target:
                NL[e+cur]=v+'+'
            if e*cur<=target:
                NL[e*cur]=v+'*'
        L=NL
    return L.get(target,'')

def verify(data,ops,res):
    ops=list(ops)
    while data:
        cur=data.pop()
        op=ops.pop()
        if op=='+':
            res-=cur
        else:
            if res%cur!=0:
                return False
            res//=cur
    return res==0



def process_1(data):
    res=0
    res0=0
    for entry in data:
        processed=preprocess(entry)
        ops=check_forward(*processed)
        if ops:
            res+=processed[0]
            if not verify(processed[1][:],ops,processed[0]):
                raise Exception(processed)
    return res


def process_2(data):
    return process_1(data)


TASK = __file__.split('\\')[-1][:-3]


def runprocess(process: callable):
    inputbase = f"..\\inputs\\{TASK}.txt"
    data = read(inputbase)
    result = process(data)
    print(result)


def main():
    c=verify([1,1,1],'+++',4)
    runprocess(process_2)
    return

'''
5540634308465 too high
'''


if __name__ == "__main__":
    main()
