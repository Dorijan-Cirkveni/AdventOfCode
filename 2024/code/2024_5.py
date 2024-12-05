import re


def read(filepath):
    with open(filepath,'r') as file:
        MM=file.read().split('\n\n')
    for i,e in enumerate(MM):
        MM[i]=e.split('\n')
    return MM

def setup_reqs(order):
    while order:
        

def process_1(M):
    res=0
    return res

def process_2(M):
    res = 0
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
