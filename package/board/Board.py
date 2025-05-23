import numpy as np

from .Direction import Direction
from .PossibilityMatrix import PossibilityMatrix

import random

def INITIAL_LETTER_BANK():
    return {
        'A': 9,
        'B': 2,
        'C': 2,
        'D': 4,
        'E': 12,
        'F': 2,
        'G': 3,
        'H': 2,
        'I': 9,
        'J': 1,
        'K': 1,
        'L': 4,
        'M': 2,
        'N': 6,
        'O': 8,
        'P': 2,
        'Q': 1,
        'R': 6,
        'S': 4,
        'T': 6,
        'U': 4,
        'V': 2,
        'W': 2,
        'X': 1,
        'Y': 2,
        'Z': 1,
        '#': 2
    }

def distance_from_point(x, y, xt, yt):
    return abs(x - xt) + abs(y - yt)

class Board:
    def __init__(self, context):
        self.context = context
        self.board = np.empty((15,15), dtype='S1')
        self.board.fill('-')
        self.adjacents = {(7, 7)}
        self.possibilities = {
            Direction.DOWN: PossibilityMatrix(self, Direction.DOWN), 
            Direction.RIGHT: PossibilityMatrix(self, Direction.RIGHT)
        }
        self.letter_bank = INITIAL_LETTER_BANK()

    def is_blank(self, x, y):
        letter = self.board[x,y].decode("utf-8")
        return letter != '-' and letter == letter.lower()

    def get_letter(self, x, y):
        return self.board[x,y].decode("utf-8").upper()

    def is_empty(self, x, y):
        return self.get_letter(x, y) == '-'

    def get_remaining_letter_count(self):
        return sum(self.letter_bank.values())

    def clear(self):
        self.board.fill('-')
        self.adjacents = {(7, 7)}
        self.possibilities[Direction.RIGHT].clear()
        self.possibilities[Direction.DOWN].clear()
        self.letter_bank = INITIAL_LETTER_BANK()

    def draw_tiles(self, number):
        available = list(map(lambda x: x[0], filter(lambda x: x[1] > 0, self.letter_bank.items())))
        draw = []
        for i in range(number):
            if len(available) == 0:
                return draw
            tile = random.choice(available)
            self.letter_bank[tile] -= 1
            if self.letter_bank[tile] == 0:
                available.remove(tile)
            draw.append(tile)
        return draw

    def update_adjacent(self, x, y):
        if self.is_empty(x, y):
            self.adjacents.add((x, y))
        else:
            self.adjacents.discard((x, y))
    
    def update_adjacents(self, word, pos, direction):
        self.adjacents.discard((7, 7))
        x, y = pos
        if direction == Direction.RIGHT:
            for i in range(x, x+len(word)):
                self.adjacents.discard((i, y))
                if y-1 >= 0:
                    self.update_adjacent(i, y-1)
                if y+1 < 15:
                    self.update_adjacent(i, y+1)
            if x-1 >= 0:
                self.update_adjacent(x-1, y)
            if x+len(word) < 15:
                self.update_adjacent(x+len(word), y)
            
        elif direction == Direction.DOWN:
            for j in range(y, y+len(word)):
                self.adjacents.discard((x, j))
                if x-1 >= 0:
                    self.update_adjacent(x-1, j)
                if x+1 < 15:
                    self.update_adjacent(x+1, j)
            if y-1 >= 0:
                self.update_adjacent(x, y-1)
            if y+len(word) < 15:
                self.update_adjacent(x, y+len(word))

    def can_place_letter(self, letter, pos, direction):
        x, y = pos
        if self.possibilities[direction].is_possible(x, y, letter):
            return True
        return False

    def place_word(self, word, pos, direction):
        x, y = pos
        for c in word:
            c_utf = c.encode("utf-8")
            self.board[x,y] = c_utf
            self.possibilities[Direction.RIGHT].place_letter(c, (x, y))
            self.possibilities[Direction.DOWN].place_letter(c, (x, y))
            x += direction.value[0]
            y += direction.value[1]
        self.update_adjacents(word, pos, direction)
        for adjacent in self.adjacents:
            self.possibilities[Direction.RIGHT].update_possibilities(adjacent)
            self.possibilities[Direction.DOWN].update_possibilities(adjacent)

    def place_root_word(self, word, shift):
        self.place_word(word, (7 - len(word)//2 + shift, 7), Direction.RIGHT)
