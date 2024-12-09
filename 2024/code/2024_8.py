import math
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

class AntennaField:
    def __init__(self,grid_data):
        self.antennas={}
        self.n=len(grid_data)
        self.m=len(grid_data[0])
        for i,line in enumerate(grid_data):
            for j,el in enumerate(line):
                if el in '.#':
                    continue
                L:list=self.antennas.setdefault(el,[])
                L.append((i,j))
        return

    def check_antpair(self,x1:int,y1:int,x2:int,y2:int,res:set):
        dx=x2-x1
        dy=y2-y1
        A0=x1-dx,y1-dy
        A3=x2+dx,y2+dy
        for x,y in (A0,A3):
            if x not in range(self.n):
                continue
            if y not in range(self.m):
                continue
            res.add((x,y))

    def check_antray(self,st_x,st_y,dx,dy,res:set):
        while st_x in range(self.n) and st_y in range(self.m):
            res.add((st_x,st_y))
            st_x+=dx
            st_y+=dy

    def check_antline(self,x1:int,y1:int,x2:int,y2:int,res:set):
        dx=x2-x1
        dy=y2-y1
        scale=math.gcd(dx,dy)
        dx//=scale
        dy//=scale
        self.check_antray(x2,y2,dx,dy,res)
        self.check_antray(x2,y2,-dx,-dy,res)


    def check_ant_type(self,mark:str, res:set, is_line=False):
        func:callable=(self.check_antpair,self.check_antline)[is_line]
        L:list=self.antennas.get(mark,[])
        for i,e in enumerate(L):
            for j in range(i):
                func(*e,*L[j],res=res)

    def get_all_targets(self,res:set, is_line=False):
        for e in self.antennas:
            self.check_ant_type(e,res, is_line)
        return len(res)



def process_1(data):
    AF=AntennaField(data)
    res_set=set()
    res=AF.get_all_targets(res_set)
    return res


def process_2(data):
    AF=AntennaField(data)
    res_set=set()
    res=AF.get_all_targets(res_set,True)
    return res


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
    runprocess(process_2,["t",""])
    return


if __name__ == "__main__":
    main()
