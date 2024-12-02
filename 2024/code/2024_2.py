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


TASKNUM=2

def main():
    test=[3,4,2,1,3,3],[4,3,5,3,9,3]
    result=process_2(*test)
    print(result)
    inputbase="..\\inputs\\2024_{}.txt".format(TASKNUM)
    data=read(inputbase)
    result=process_2(*data)
    print(result)
    return


if __name__ == "__main__":
    main()
