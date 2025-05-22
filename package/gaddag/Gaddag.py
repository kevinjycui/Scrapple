from .GaddagNode import GaddagNode

class Gaddag:
    def __init__(self):
        self.root = GaddagNode()
        
    def add_word(self, word):
        self.root.add_word(word)

    def get(self, letter):
        return self.root.get(letter)

    def read(self):
        return set(self.root.read())
