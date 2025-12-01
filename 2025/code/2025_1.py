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
    return n if s[0]=='R' else -n



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
    for entry in data:
        processed=preprocess(entry)
        if processed==0:
            continue
        prefix=1 if processed>0 else -1
        diff,processed=divmod(abs(processed),100)
        processed*=prefix
        res += diff
        for cur in range(state+processed,state,-prefix):
            if cur in (0,100):
                res+=1
        # print(entry,state,diff,processed,prefix,res,(state+processed),sep="\t")
        state+=processed
        state%=100
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
