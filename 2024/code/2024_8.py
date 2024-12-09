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
    return {i:e for i,e in enumerate(s) if s not in set('.#')}

class AntennaField:
    def __init__(self,grid_data):
        self.antennas={}
        for i,line in enumerate(grid_data):


def process_1(data):
    res=0
    antenna_locs={}
    for entry in data:
        processed=preprocess(entry)
    return res


def process_2(data):
    return process_1(data)


TASK = __file__.split('\\')[-1][:-3]


def runprocess_withinputfrom(process: callable, suffix:str=""):
    inputbase = f"..\\inputs\\{TASK}{suffix}.txt"
    data = read(inputbase)
    if data is not None:
        result = process(data)
        print(result)


def runprocess(process: callable, input_files=None):

    if input_files is None:
        input_files = [""]
    for suffix in input_files:
        runprocess_withinputfrom(process,suffix)


def main():
    runprocess(process_2,["","t"])
    return


if __name__ == "__main__":
    main()
