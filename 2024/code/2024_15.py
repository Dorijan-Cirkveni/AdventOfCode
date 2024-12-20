import numpy


def read(filepath):
    M=None
    try:
        file=open(filepath, 'r')
        A,B = file.read().split('\n\n')
        M=[e.split('\n') for e in (A,B)]
        file.close()
    except Exception as err:
        print(err)
    return M


def shift(i:int,j:int,di:int,dj:int):
    return i+di,j+dj

def double(half_row:str):
    row=''
    for e in half_row:
        de={'O':'[]','@':'@.'}.get(e,e*2)
        row+=de
    return row

def box_shift(boxes:set,curset:set,delta:tuple):
    boxset=boxes&curset
    boxes-=boxset
    boxes|={shift(*el,*delta) for el in boxset}


class Warehouse:
    def __init__(self,objects:list[str]):
        self.walls=[]
        self.agents=[]
        self.boxes=set()
        for i,row in enumerate(objects):
            self.walls.append(row)
            for j,el in enumerate(row):
                self.add_el(i,j,el)
        return
    def add_el(self,i,j,el):
        loc=i,j
        if el=='O':
            self.boxes.add(loc)
        elif el=='@':
            self.agents.append(loc)
    def is_wall(self,i,j):
        return self.walls[i][j]=='#'
    def get_next(self,i:int,j:int,di:int,dj:int):
        res=shift(i,j,di,dj)
        resl={res}
        return resl
    def select_next(self,loc:tuple[int,int]):
        return loc in self.boxes
    def push(self,delta:tuple):
        curset=set()
        curlist=self.agents.copy()
        while curlist:
            cur=curlist.pop()
            curset.add(cur)
            for nex in self.get_next(*cur,*delta):
                if nex in curset:
                    continue
                if self.is_wall(*nex):
                    return
                if self.select_next(nex):
                    curlist.append(nex)
        self.finalise_push(curset,delta)
        return
    def finalise_push(self,curset:set,delta:tuple):
        self.boxes-=curset
        self.boxes|={shift(*el,*delta) for el in curset}
        self.agents=[shift(*el,*delta) for el in self.agents]
        self.boxes-=set(self.agents)
        return
    def all_instructions(self,ins:str):
        directions={
            '>':(0,1),
            '<':(0,-1),
            '^':(-1,0),
            'v':(1,0)
        }
        translated=[directions[e] for e in ins]
        for e in translated:
            self.push(e)
        return
    def print(self):
        print(self.boxes,self.agents)
        for i,e in enumerate(self.walls):
            for j,f in enumerate(e):
                if (i, j) in self.boxes:
                    f='o'
                elif (i, j) in self.agents:
                    f='@'
                elif f!='#':
                    f='.'
                print(f,end='')
            print()

    def value(self):
        res=0
        for i,j in self.boxes:
            res+=i*100+j
        return res


class Widehouse(Warehouse):
    def __init__(self, objects: list[str]):
        self.box_ends=set()
        for i, half_row in enumerate(objects):
            row = double(half_row)
            objects[i]=row
        super().__init__(objects)
        return
    def add_el(self,i,j,el):
        loc=i,j
        if el=='[':
            self.boxes.add(loc)
        elif el==']':
            self.box_ends.add(loc)
        elif el=='@':
            self.agents.append(loc)

    def get_next(self, i: int, j: int, di: int, dj: int):
        res = shift(i, j, di, dj)
        resl = {res}
        if (i,j) in self.boxes:
            resl.add((i,j+1))
        elif (i,j) in self.box_ends:
            resl.add((i,j-1))
        return resl
    def select_next(self,loc:tuple[int,int]):
        return loc in self.boxes or loc in self.box_ends
    def finalise_push(self,curset:set,delta:tuple):
        curset-=set(self.agents)
        box_shift(self.boxes,curset,delta)
        box_shift(self.box_ends,curset,delta)
        self.agents=[shift(*el,*delta) for el in self.agents]
        assert not (self.boxes&self.box_ends)
        return
    def print(self):
        print(self.boxes)
        print(self.box_ends)
        print(self.agents)
        for i,e in enumerate(self.walls):
            for j,f in enumerate(e):
                if (i, j) in self.boxes:
                    f='['
                elif (i, j) in self.box_ends:
                    f=']'
                elif (i, j) in self.agents:
                    f='@'
                elif f!='#':
                    f='.'
                print(f,end='')
            print()






def process_1(data):
    if not data:
        return
    objects,ins_lines=data
    warehouse=Warehouse(objects)
    instructions=''.join(ins_lines)
    warehouse.all_instructions(instructions)
    res=warehouse.value()
    return res


def process_2(data):
    if not data:
        return
    objects,ins_lines=data
    warehouse=Widehouse(objects)
    instructions=''.join(ins_lines)
    warehouse.all_instructions(instructions)
    res=warehouse.value()
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
    runprocess(process_2,["t","b",""])
    return


if __name__ == "__main__":
    main()
