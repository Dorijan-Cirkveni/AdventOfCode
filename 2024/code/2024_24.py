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


    def print_dependencies(self):
        stack=[]
        for key in self.values:
            if key not in self.orig:
                stack.append(key)
        core_keys:dict[str,set[str]]={}
        while stack:
            cur:str=stack.pop()
            cur_mode:int=self.mode.get(cur,-1)
            next_dict=self.dest.get(cur,{})
            for nex,mode in next_dict.items():
                self.orig[nex]-={cur}
                curset:set=core_keys.setdefault(nex,set())
                if cur_mode==mode:
                    temp:set=core_keys.get(cur,set())
                    curset|=temp
                else:
                    curset.add(cur)
                if not self.orig[nex]:
                    stack.append(nex)
        valid=set()
        for curset in core_keys.values():
            valid|=curset
        for key,val in core_keys.items():
            if key not in valid:
                continue
            print(key, self.mode.get(key,-1), val)
        return

    def print_dep_tree(self, val, op:int=-1)->list[str]:
        if val not in self.orig:
            return [val]
        new_op=self.mode.get(val,-1)
        results=[]
        curset=self.orig.get(val,set())
        for pre in curset:
            cures=self.print_dep_tree(pre,new_op)
            results.extend(cures)
        if not results:
            results.append(val)
        if op!=new_op:
            sop="+-^?"[op]
            results=[f" {sop} ".join(results)]
        return results





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
    circuit = Circuit()
    for entry in data:
        if not entry:
            continue
        detail = entry.split(" ")
        if len(detail) == 2:
            name = detail[0][:-1]
            value = bool(int(detail[1]))
            circuit.add_value(name, value)
        else:
            mode = ['OR', 'AND', 'XOR'].index(detail[1])
            circuit.add_gate(detail[4], mode, [detail[0], detail[2]])
    exits=[el for el in circuit.values if el[0]=='z']
    for el in exits:
        print(el, end= "->")
        print(circuit.print_dep_tree(el))
    return 0


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
