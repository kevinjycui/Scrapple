class TrieNode:
    def __init__(self, letter='', parent=None, is_initial=False, is_terminal=False):
        self.letter = letter
        self.parent = parent
        self.children = {}
        self.is_initial = is_initial
        self.is_terminal = False

    def __str__(self):
        return self.letter

    def add_word(self, word):
        return self.add_child(word, True)

    def add_child(self, word, is_initial=False):
        c = word[0]
        tail = word[1:]
        child_terminal = len(tail) == 0
        
        child_node = self.children.setdefault((c, child_terminal), TrieNode(c, self, is_initial, child_terminal))
        
        if child_terminal:
            child_node.is_terminal = True
            return child_node
        return child_node.add_child(tail)

    def get_terminal_children(self):
        return list(filter(lambda x:x.is_terminal, self.children))

    def get_middle_children(self, suffix):
        return list(filter(lambda x:x.search(suffix), self.children))

    def get(self, word):
        if word == '':
            return self if self.is_terminal else None
            
        letter = word[0]
        if len(word) == 1:
            if (letter, True) not in self.children:
                return None
            else:
                return self.children[(letter, True)]
        elif (letter, False) not in self.children:
            return None
        return self.children[(letter, False)].get(word[1:]) 

    def search(self, word):
        return self.get(word) is not None

    def prefix(self):
        if self.parent is None:
            return ''
        if self.is_initial:
            return self.letter
        return self.parent.prefix() + self.letter
    
    def read(self):
        s = []
        if self.is_terminal:
            s.append(self.letter)
        for child in self.children.values():
            for suf in child.read():
                s.append(self.letter + suf)
        return s

    def map(self, letter_map):
        if self.letter != '':
            letter_map[self.letter].append(self)
        for child in self.children.values():
            child.map(letter_map)