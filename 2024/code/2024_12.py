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

def check_state(cur,other,last_cur,last_other):
    if cur==last_cur:
        return last_cur==last_other
    else:
        return True

def match(last:list[int],cur:list[int],sides:list[int]):
    nex_last=-1,-1
    for a,b in zip(last, cur):
        last_a,last_b=nex_last
        nex_last=a,b
        if (last_a,last_b)==(a,b):
            continue
        if a==b:
            continue
        if check_state(a,b,last_a,last_b):
            sides[a]+=1
        if check_state(b,a,last_b,last_a):
            sides[b]+=1
    # print(*sides, sep='\t')


class Solution:
    def __init__(self,data):
        self.data:list[list]=[]
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
    def traverse_island_2(self,si,sj,val,nulled):
        self.data: list[list][int]
        curset={(si,sj)}
        area=0
        while curset:
            nexset=set()
            area+=len(curset)
            for ci,cj in curset:
                self.data[ci][cj]=nulled
                self.get_neigh(ci,cj,val,nexset,nulled)
            curset=nexset
        return area
    def process_1(self):
        res=0
        for i,E in enumerate(self.data):
            for j,e in enumerate(E):
                if e==' ':
                    continue
                res+=self.traverse_island(i,j,e,'@')
                self.traverse_island(i, j, '@')
        return res
    def horizontal_sides(self,sides):
        last=[-1]*len(self.data[0])
        for i,cur in enumerate(self.data):
            match(last,cur,sides)
            last=cur
        return
    def vertical_sides(self,sides):
        n=len(self.data)
        m=len(self.data[0])
        last=[-1]*n
        for j in range(m):
            cur=[self.data[i][j] for i in range(n)]
            match(last,cur,sides)
            last=cur
        print()
        return

    def process_2(self):
        areas=[]
        sides=[]
        ind=0
        for i,E in enumerate(self.data):
            E[-1]=-1
        self.data[-1]=[-1]*len(self.data[0])
        for i,E in enumerate(self.data):
            for j,e in enumerate(E):
                if isinstance(e,int):
                    continue
                area=self.traverse_island_2(i,j,e,ind)
                areas.append(area)
                sides.append(0)
                ind+=1
                print(e,end="\t")
        print()
        print(*areas,sep='\t')
        sides.append(0)
        self.vertical_sides(sides)
        print(*sides,sep='\t')
        self.horizontal_sides(sides)
        sides.pop()
        print(*sides,sep='\t')
        res=0
        while areas:
            area,side=areas.pop(),sides.pop()
            res+=area*side
        return res


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
