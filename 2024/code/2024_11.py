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


def preprocess(s:str):
    res=defaultdict(int)
    for e in s.split():
        n=int(e)
        res[n]+=1
    return res

def single_blink(n:int):
    if n==0:
        return [1]
    s=str(n)
    match len(s)%2:
        case 0:
            k=len(s)>>1
            s1=s[:k]
            s2=s[k:]
            n1=int(s1)
            n2=int(s2)
            return [n1,n2]
        case 1:
            return [n*2024]



def blink(census:defaultdict[int,int]):
    sus=defaultdict(int)
    for e,v in census.items():
        for f in single_blink(e):
            sus[f]+=v
    return sus



def process_1(data, blinks=25):
    res=0
    for entry in data:
        processed=preprocess(entry)
        for _ in range(blinks):
            processed=blink(processed)
    return sum(processed.values())


def process_2(data):
    return process_1(data, 75)


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
