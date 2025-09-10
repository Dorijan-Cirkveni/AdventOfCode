class Circuit:
    def __init__(self):
        self.values:dict[str,bool]={}
        self.dest:dict[str,dict[str,int]]={}
        self.orig:dict[str,set[str]]={}
        self.mode:dict[str,int]={}
    def add_value(self,dest:str,value:bool):
        self.values[dest]=value
    def add_gate(self,dest:str,mode:int,orig:list[str]):
        for orig_inst in orig:
            self.dest.setdefault(orig_inst,{})[dest]=mode
        self.orig[dest]=set(orig)
        self.values[dest]=[False,True,False][mode]
        self.mode[dest]=mode
    def set_orig(self):
        self.orig={}
        for orig,dest_list in self.dest.items():
            for dest in dest_list:
                self.orig.setdefault(dest,set()).add(orig)
    def simplify(self):
        stack=[]
        for key in self.dest:
            if key not in self.orig:
                stack.append(key)
        counts={e:len(v) for e,v in self.orig.items()}
        node_prev_sets:dict[str,set[str]]={}
        while stack:
            cur:str=stack.pop()
            next_dict=self.dest.pop(cur,{})
            for nex,mode in next_dict.items():
                counts[nex]-=1
                if counts[nex]:
                    continue
                counts.pop(nex)
                curset=set()
                for old in self.orig[nex]:
                    if self.mode.get(old,-1)==mode:
                        curset|=node_prev_sets.get(old,set())
                    else:
                        curset.add(old)
                node_prev_sets[nex]=curset
                stack.append(nex)
        return

    def process(self):
        values=self.values.copy()
        stack=[]
        for key in values:
            if key not in self.orig:
                stack.append(key)
        while stack:
            cur:str=stack.pop()
            val=values[cur]
            next_dict=self.dest.pop(cur,{})
            for nex,mode in next_dict.items():
                old=values[nex]
                new=[old|val,old&val,old^val][mode]
                values[nex]=new
                self.orig[nex]-={cur}
                if not self.orig[nex]:
                    stack.append(nex)
                    self.orig.pop(nex)
        return {e:v for e,v in values.items() if e[0]=='z'}




def read(filepath):
    M=None
    try:
        file=open(filepath, 'r')
        M = file.read().split('\n')
        file.close()
    except Exception as err:
        print(err)
    return M



def process_1(data):
    circuit=Circuit()
    for entry in data:
        if not entry:
            continue
        detail=entry.split(" ")
        if len(detail)==2:
            name=detail[0][:-1]
            value=bool(int(detail[1]))
            circuit.add_value(name,value)
        else:
            mode=['OR','AND','XOR'].index(detail[1])
            circuit.add_gate(detail[4],mode,[detail[0],detail[2]])
    tempres=circuit.process()
    order=list(tempres)
    order.sort(reverse=True)
    res=[str(int(tempres[e])) for e in order]
    return int("".join(res),2)


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
