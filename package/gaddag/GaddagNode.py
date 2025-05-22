class GaddagNode:
    def __init__(self, letter=''):
        self.letter = letter
        self.children = {}
        self.is_terminal = False

    def get(self, letter):
        nodes = []
        if (letter, True) in self.children:
            nodes.append(self.children[(letter, True)])
        if (letter, False) in self.children:
            nodes.append(self.children[(letter, False)])
        return nodes

    def add_child(self, word):
        c = word[0]
        tail = word[1:]
        child_terminal = len(tail) == 0
        
        child_node = self.children.setdefault((c, child_terminal), GaddagNode(c))
        
        if child_terminal:
            child_node.is_terminal = True
            return child_node
        return child_node.add_child(tail)
    
    def add_word(self, word):
        for i in range(1, len(word)+1):
            gaddag_word = word[:i][::-1] + '+' + word[i:]
            self.add_child(gaddag_word)

    def read_suffix(self):
        s = []
        if self.is_terminal:
            s.append(self.letter.replace('+', ''))
        for child in self.children.values():
            for suf in child.read_suffix():
                if self.letter == '+':
                    s.append(suf)
                else:
                    s.append(self.letter + suf)
        return s
    
    def read_prefix(self):
        s = []
        for child in self.children.values():
            if child.letter != '+':
                for word in child.read_prefix():
                    pref = word[0]
                    suf = word[1]
                    s.append((pref + self.letter, suf))
            else:
                for suf in child.read_suffix():
                    s.append((self.letter, suf))
        return s

    def read(self):
        return [pref + suf for pref, suf in self.read_prefix()]
    