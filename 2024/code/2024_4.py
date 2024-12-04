import re


def read(filepath):
    with open(filepath,'r') as file:
        M=file.read().split('\n')
    return M

def check_line(s):
    X=re.findall(r'XMAS',s)
    return len(X)

def check_both_ways(s):
    return check_line(s)+check_line(s[::-1])

def check_mat(M):
    res=0
    for s in M:
        res+=check_both_ways(s)
    return res

def make_vertical(M):
    V=["" for _ in M[0]]
    for E in M:
        for i,e in enumerate(E):
            V[i]+=e
    return V

def make_diagonal(M,plus=True, crit=4):
    diagonals=["" for _ in range(len(M)+len(M[0]))]
    for i,E in enumerate(M):
        for j,e in enumerate(E):
            k=i+j if plus else i-j
            diagonals[k]+=e
    return [E for E in diagonals if len(E)>=crit]

def count_all(M):
    MM=M,make_vertical(M),make_diagonal(M,True),make_diagonal(M,False)
    res=0
    for CM in MM:
        temp=check_mat(CM)
        res+=temp
    return res

def process_1(M):
    res=count_all(M)
    return res

def check_mas(M,i,j):
    if M[i][j]!='A':
        return False
    if M[i-1][j-1]+M[i+1][j+1] not in 'SMS':
        return False
    if M[i-1][j+1]+M[i+1][j-1] not in 'SMS':
        return False
    return True

def process_2(M):
    res = 0
    for i in range(1,len(M)-1):
        for j in range(1,len(M[0])-1):
            res+=check_mas(M,i,j)
    return res


TASK=__file__.split('\\')[-1][:-3]

def runprocess(process:callable):
    test=[
        "X..X..X",
        ".M.M.M.",
        "..AAA.."]
    test=test+["XMASAMX"]+test[::-1],
    test=["MMSM","AAAA","MMSM"],
    result=process(*test)
    print(result)
    inputbase=f"..\\inputs\\{TASK}.txt"
    data=read(inputbase),
    result=process(*data)
    print(result)

def runproc2():
    test=["MMSM","AAAA","MMSM"]
    test=test+["XMASAMX"]+test[::-1],
    result=process_2(*test)
    print(result)
    inputbase=f"..\\inputs\\{TASK}.txt"
    data=read(inputbase),
    result=process_2(*data)
    print(result)

def main():
    runprocess(process_2)
    return


if __name__ == "__main__":
    main()
