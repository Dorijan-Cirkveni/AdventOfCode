from collections import Counter, defaultdict


def read(filepath):
    A=[]
    B=[]
    with open(filepath,'r') as file:
        for line in file:
            if not line:
                continue
            if line[-1]!='\n':
                line+='\n'
            a,b=line[:-1].split('   ')
            A.append(int(a))
            B.append(int(b))
    return A,B

def process_1(A,B):
    A.sort(reverse=True)
    B.sort(reverse=True)
    res=0
    best=0
    while A:
        a=A.pop()
        b=B.pop()
        res+=abs(a-b)
        best=max(best,abs(a-b))
    print(best)
    return res

def make_counter(A):
    D=defaultdict(int)
    while A:
        D[A.pop()]+=1
    return D

def process_2(A,B):
    AD=make_counter(A)
    BD=make_counter(B)
    res=0
    for e,v in AD.items():
        if e not in BD:
            continue
        res+=e*v*BD[e]
    return res


TASKNUM=1

def main():
    test=[0,1,2],[1,1,1]
    result=process_2(*test)
    print(result)
    inputbase="..\\inputs\\2024_{}.txt".format(TASKNUM)
    data=read(inputbase)
    result=process_2(*data)
    print(result)
    return


if __name__ == "__main__":
    main()
