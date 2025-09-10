import bisect
from math import trunc


class TrieNode:
    def __init__(self):
        self.branches:dict[str,TrieNode]={}
    def setdefault(self,key):
        return self.branches.setdefault(key,TrieNode())
class StringTrie:
    def __init__(self):
        self.root:TrieNode=TrieNode()
    def add(self,sequence:list[str]):
        cur:TrieNode=self.root
        for el in sequence:
            cur=cur.setdefault(el)
        return cur


class Network:
    def __init__(self):
        self.connections:dict[str,set[str]]={}
    def add_connection(self,a,b):
        if a==b:
            return
        curset=self.connections.setdefault(a,set())
        curset.add(b)
        curset=self.connections.setdefault(b,set())
        curset.add(a)
    def get_threes(self, first, target_crit='t', res:set=None)->set[tuple]:
        if res is None:
            res = set()
        curset=set()
        for neigh in self.connections.get(first,set()):
            if neigh.startswith(target_crit) and neigh<first:
                continue
            for third in curset:
                if third in self.connections.get(neigh,set()):
                    cur=[first,neigh,third]
                    cur.sort()
                    res.add(tuple(cur))
            curset.add(neigh)
        return res
    def get_all_threes(self, target_crit='t')->set[tuple]:
        res:set[tuple]=set()
        for first in self.connections:
            if first.startswith(target_crit):
                self.get_threes(first, target_crit, res)
        return res



    def find_largest(self):
        largest:tuple=tuple()
        conns=sorted(list(self.connections))
        first_list=conns[::-1]
        first=first_list.pop()
        base:dict[tuple,list]={
            tuple():first_list
        }
        next_nodes:dict[str,dict[tuple,list]]={first:base}
        for name in conns:
            # print({e:len(v) for e,v in next_nodes.items()})
            cur_groups=next_nodes.pop(name)
            name_conns=self.connections[name]
            for cur_group,possible_conns in cur_groups.items():
                new_name=cur_group+(name,)
                if len(cur_group)==len(largest):
                    largest=new_name
                if not possible_conns:
                    continue
                new_next_nodes=[el for el in possible_conns if el in name_conns]
                if new_next_nodes:
                    temp=next_nodes.setdefault(new_next_nodes.pop(),{})
                    temp[new_name]=new_next_nodes
                nex_name=possible_conns.pop()
                next_nodes.setdefault(nex_name,{})[cur_group]=possible_conns
        return ",".join(largest)




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
    raw=s.replace(" ","")
    res=tuple(raw.split('-'))
    return res if raw else ("","")



def process_1(data):
    net=Network()
    for entry in data:
        a,b=preprocess(entry)
        net.add_connection(a,b)
    threes=net.get_all_threes()
    return len(threes)


def process_2(data):
    net=Network()
    for entry in data:
        a,b=preprocess(entry)
        net.add_connection(a,b)
    largest=net.find_largest()
    return largest


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
