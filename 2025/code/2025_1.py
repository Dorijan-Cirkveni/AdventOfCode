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
    n=int(s[1:])
    return n if s[0]=='L' else -n



def process_1(data):
    res=0
    state=50
    for entry in data:
        processed=preprocess(entry)
        state+=processed
        state%=100
        res+=state==0
    return res


def process_2(data):
    res=0
    state=50
    counter=dict()
    for entry in data:
        processed=preprocess(entry)
        nex=state+processed
        round1=(state+int(processed<0))//100
        round2=(nex+int(processed<0))//100
        diff=abs(round1-round2)
        res+=diff
        counter[diff]=counter.get(diff,0)+1
        state=nex%100
    print(counter)
    return res


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
