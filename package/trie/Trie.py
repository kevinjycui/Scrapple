from .TrieNode import TrieNode

class Trie:
    def __init__(self):
        self.root = TrieNode()
        self.letter_map = {}
        for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZŔÑ":
            self.letter_map[letter] = []
        
    def add_word(self, word):
        self.root.add_word(word)

    def read(self):
        return self.root.read()

    def update_map(self):
        self.root.map(self.letter_map)