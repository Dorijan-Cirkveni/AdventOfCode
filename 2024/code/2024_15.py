def read(filepath):
    M=None
    try:
        file=open(filepath, 'r')
        M = file.read().split('\n')
        for i,e in enumerate(M):
            M[i]=list()
        file.close()
    except Exception as err:
        print(err)
    return M


def make_warehouse(raw:list[str]):
    res=[]
    loc=None
    obstacles=
    for i,E in enumerate(raw):
        le=



def process_1(data):
    res=0
    if not data:
        return
    warehouse,instructions=data.split("\n\n")
    return res


def process_2(data):
    return process_1(data)


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
