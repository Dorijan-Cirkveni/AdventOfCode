from collections import Counter, defaultdict, deque


def read(filepath):
    M=[]
    with open(filepath,'r') as file:
        for line in file:
            if not line:
                continue
            L=line[:-1].split()
            L2=[int(e) for e in L]
            M.append(L2)
    return M

def check_line(L):
    last=L.pop()
    direction=0
    while L:
        cur=L.pop()
        diff=last-cur
        last=cur
        if diff==0:
            return False # Not ascending or descending
        if direction*diff<0:
            return False # Not consistent
        if direction==0:
            direction=-1 if diff<0 else 1 # Set asc/desc direction
        diff*=direction
        if diff>3:
            return False # Difference too big
    return True


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
    res=len(M)
    while M:
        L=M.pop()
        if check_line(L[:]):
            continue
        L2=[]
        while L:
            e=L.pop()
            if check_line(L+L2[::-1]):
                break
            L2.append(e)
        else:
            res-=1
    return res


TASKNUM=2

def runprocess(process:callable):
    test=[[1,2,3,4,5],[1,2,2,4,5],[1,2,3,0],[1,9,97]],
    result=process(*test)
    print(result)
    inputbase="..\\inputs\\2024_{}.txt".format(TASKNUM)
    data=read(inputbase),
    result=process(*data)
    print(result)

def main():
    runprocess(process_2)
    return


if __name__ == "__main__":
    main()
