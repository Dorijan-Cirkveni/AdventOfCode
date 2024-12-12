def read(filepath):
    M=None
    try:
        file=open(filepath, 'r')
        M = file.read().split('\n')
        file.close()
    except Exception as err:
        print(err)
    return M


def preprocess(_i:int,s:str):
    return list(s+' ')


class Solution:
    def __init__(self,data):
        self.data=[]
        for i,entry in enumerate(data):
            processed=preprocess(i,entry)
            self.data.append(processed)
        self.data.append([' ']*(len(self.data[0])))
        return
    def get_neigh(self,i,j,value,ret_set,nulled=' ')->int:
        if value==nulled:
            return 4
        borders=0
        for di,dj in [(i,j-1),(i,j+1),(i+1,j),(i-1,j)]:
            cur_v=self.data[di][dj]
            if cur_v==value:
                ret_set.add((di,dj))
                continue
            if cur_v!=nulled:
                borders+=1
        return borders
    def traverse_island(self,si,sj,val,nulled=' '):
        curset={(si,sj)}
        perimeter=0
        area=0
        while curset:
            nexset=set()
            area+=len(curset)
            for ci,cj in curset:
                self.data[ci][cj]=nulled
                borders=self.get_neigh(ci,cj,val,nexset,nulled)
                perimeter+=borders
            curset=nexset
        res=area*perimeter
        if nulled=='@':
            print(area,perimeter,res)
        return res
    def process_1(self):
        res=0
        for i,E in enumerate(self.data):
            for j,e in enumerate(E):
                if e==' ':
                    continue
                res+=self.traverse_island(i,j,e,'@')
                self.traverse_island(i, j, '@')
        return res



    def process_2(self):
        return self.process_1()


TASK = __file__.split('\\')[-1][:-3]


def runprocess_withinputfrom(process: callable, suffix:str=""):
    inputbase = f"..\\inputs\\{TASK}{suffix}.txt"
    data = read(inputbase)
    if data is not None:
        sol=Solution(data)
        result = process(sol)
        print(f"Result for {suffix}: {result}")


def runprocess(process: callable, input_files=None):
    if input_files is None:
        input_files = [""]
    for suffix in input_files:
        runprocess_withinputfrom(process,suffix)


def main():
    runprocess(Solution.process_2,["t",""])
    return


if __name__ == "__main__":
    main()
