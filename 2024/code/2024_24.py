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
        self.values[dest]=[False,True,False][mode]
        self.mode[dest]=mode
    def set_orig(self):
        for orig,dest_list in self.dest.items():
            for dest in dest_list:
                self.orig.setdefault(dest,set()).add(orig)
    def simplify(self):
        stack=[]
        for key in self.orig:
            if key not in self.dest:
                stack.append(key)
        while stack:
            cur:str=stack.pop()
            val=self.values[cur]
            next_dict=self.dest.pop(cur,{})
            for nex,mode in next_dict.items():
                old=self.values[nex]
                new=[old|val,old&val,old^val][mode]
                self.values[nex]=new
                self.orig[nex]-={cur}
                if not self.orig[nex]:
                    stack.append(nex)
                    self.orig.pop(nex)
        return {e:v for e,v in self.values.items() if e[0]=='z'}

    def process(self):
        stack=[]
        for key in self.values:
            if key not in self.orig:
                stack.append(key)
        while stack:
            cur:str=stack.pop()
            val=self.values[cur]
            next_dict=self.dest.pop(cur,{})
            for nex,mode in next_dict.items():
                old=self.values[nex]
                new=[old|val,old&val,old^val][mode]
                self.values[nex]=new
                self.orig[nex]-={cur}
                if not self.orig[nex]:
                    stack.append(nex)
                    self.orig.pop(nex)
        return {e:v for e,v in self.values.items() if e[0]=='z'}




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
