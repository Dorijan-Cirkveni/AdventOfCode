import re
from collections import Counter, defaultdict, deque


def read(filepath):
    M=[]
    with open(filepath,'r') as file:
        for line in file:
            if not line:
                continue
            L=line[:-1]
            M.append(L)
    return M

def check_line(s):
    res=0
    for m in re.finditer(r'mul\(\d{1,3},\d{1,3}\)',s):
        a,b=m.group()[4:][:-1].split(',')
        res+=int(a)*int(b)
    return res

def check_line_2(s,status:bool):
    res=0
    pattern=r"(mul\(\d{1,3},\d{1,3}\))|(do\(\))|(don\'t\(\))"
    for m in re.finditer(pattern,s):
        g=m.group()
        match g[2]:
            case '(':
                status=True
            case 'n':
                status=False
            case 'l':
                if not status:
                    continue
                a,b=g[4:][:-1].split(',')
                res+=int(a)*int(b)
    return res,status


def process_1(M):
    res=0
    while M:
        L=M.pop()
        res+=check_line(L)
    return res

def make_counter(A):
    D=defaultdict(int)
    while A:
        D[A.pop()]+=1
    return D

def process_2(M):
    res = 0
    status=True
    for L in M:
        temp, status = check_line_2(L,status)
        res+=temp
    return res


TASK=__file__.split('\\')[-1][:-3]

def runprocess(process:callable):
    test=["don't()mul(2,2)","mul(2,2),do()mul(1,2)"],
    result=process(*test)
    print(result)
    inputbase=f"..\\inputs\\{TASK}.txt"
    data=read(inputbase),
    result=process(*data)
    print(result)

def main():
    runprocess(process_2)
    return


if __name__ == "__main__":
    main()
