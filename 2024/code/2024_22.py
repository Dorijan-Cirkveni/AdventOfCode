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
    return int(s)

MOD=16777216

def step1(n):
    n^=n<<6
    n%=MOD
    return n
def step2(n):
    n^=n>>5
    n%=MOD
    return n
def step3(n):
    n^=n<<11
    n%=MOD
    return n
def all_step(n):
    a=step1(n)
    b=step2(a)
    c=step3(b)
    return c

def full(n,steps=2000):
    for _ in range(steps):
        n=all_step(n)
    return n


def process_1(data):
    res=0
    for entry in data:
        processed:int=preprocess(entry)
        res_temp=full(processed)

        print(f"{processed}: {res_temp}")
        res+=res_temp
    return res


def log_price_change_sequence_rewards(start_number,profit_log:defaultdict[tuple,int],steps=2000):
    changes=tuple()
    found={}
    last_price=start_number%10
    for _ in range(steps):
        next_number=all_step(start_number)
        next_price=next_number%10
        delta=next_price-last_price
        changes=changes[-3:]+(delta,)
        if len(changes)==4 and changes not in found:
            found[changes]=next_price
            profit_log[changes]+=next_price
        last_price=next_price
        start_number=next_number
    return found



def process_2(data):
    res=0
    profit_log=defaultdict(int)
    for entry in data:
        processed:int=preprocess(entry)
        res_temp=log_price_change_sequence_rewards(processed,profit_log)
        print(set(res_temp.values()))
    print(set(profit_log.values()))
    res=max(profit_log.values())
    return res


TASK = __file__.split('\\')[-1][:-3]


def runprocess_withinputfrom(process: callable, suffix:str=""):
    inputbase = f"..\\inputs\\{TASK}{suffix}.txt"
    data = read(inputbase)
    if data is not None:
        result = process(data)
        print(f"Result for {suffix}: {result}")
        input("Press Enter to continue:")


def runprocess(process: callable, input_files=None):
    if input_files is None:
        input_files = [""]
    for suffix in input_files:
        runprocess_withinputfrom(process,suffix)


def main():
    runprocess(process_2,["tt","t2",""])
    return


if __name__ == "__main__":
    main()
