def read(filepath):
    M = None
    try:
        file = open(filepath, 'r')
        raw = file.read()
        assert raw
        A, B = raw.split('\n\n')
        file.close()
    except Exception as err:
        print(err)
        A, B = None, None
    return A, B


class TrieNode:
    def __init__(self):
        self.isFinal = False
        self.subnodes = {}

    def setdefault(self, key: str):
        return self.subnodes.setdefault(key, TrieNode())

    def get(self, key: str) -> ['TrieNode', None]:
        return self.subnodes.get(key, None)

    def repr(self, count=None):
        if not count:
            return self
        return self,count

    def step(self, key: str, returns: list, count=None):
        nexnode: [TrieNode, None] = self.get(key)
        if not nexnode:
            return False
        nexnode: TrieNode
        repr=nexnode.repr(count)
        returns.append(repr)
        return nexnode.isFinal


class StringTrie:
    def __init__(self, contents: list[str]):
        self.root = TrieNode()
        for el in contents:
            self.add(el)

    def add(self, el: str):
        cur = self.root
        for c in el:
            cur = cur.setdefault(c)
        cur.isFinal = True

    def isValid(self, pattern: str,*_args):
        curlist = [self.root]
        valid = True
        for c in pattern:
            nexlist = []
            valid = False
            for cur in curlist:
                now_valid = cur.step(c, nexlist)
                valid = valid or now_valid
            if valid:
                nexlist.append(self.root)
            curlist = nexlist
        return valid

    def countValid(self, pattern: str,*_args):
        curlist = [(self.root, 1)]
        valid = 1
        for c in pattern:
            nexlist = []
            valid = 0
            for cur, val in curlist:
                if cur.step(c, nexlist, val):
                    valid += val
            if valid:
                nexlist.append((self.root, valid))
            curlist = nexlist
        return valid


def process_1(data,function=StringTrie.isValid):
    raw_towels: str
    raw_designs: str
    raw_towels, raw_designs = data
    res = 0
    towels = raw_towels.split(', ')
    designs = raw_designs.split('\n')
    trie = StringTrie(towels)
    for entry in designs:
        valid = function(trie,entry)
        print(entry, valid)
        res += valid
    return res


def process_2(data):
    return process_1(data,StringTrie.countValid)


TASK = __file__.split('\\')[-1][:-3]


def runprocess_withinputfrom(process: callable, suffix: str = ""):
    inputbase = f"..\\inputs\\{TASK}{suffix}.txt"
    data = read(inputbase)
    if None not in data:
        result = process(data)
        print(f"Result for {suffix}: {result}")


def runprocess(process: callable, input_files=None):
    if input_files is None:
        input_files = [""]
    for suffix in input_files:
        runprocess_withinputfrom(process, suffix)


def main():
    runprocess(process_2, ["t", ""])
    return


if __name__ == "__main__":
    main()
