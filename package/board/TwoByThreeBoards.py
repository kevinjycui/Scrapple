import numpy as np

from .Board import Board

class TwoByThreeBoardsIter:
    def __init__(self, boards):
        self.boards = boards
        self.index = 0

    def __next__(self):
        if self.index == 6:
            raise StopIteration
        i = self.index % 3
        j = self.index // 3
        self.index += 1
        return self.boards.get(i, j)
        
class TwoByThreeBoards:
    def __init__(self, trie, trie_reverse, INITIAL_LETTER_BANK, closeness_threshold):
        self.trie = trie
        self.trie_reverse = trie_reverse
        self.INITIAL_LETTER_BANK = INITIAL_LETTER_BANK
        self.closeness_threshold = closeness_threshold
        self.boards = [[Board(self), Board(self)], [Board(self), Board(self)], [Board(self), Board(self)]]

    def get(self, i, j):
        return self.boards[i][j]

    def __iter__(self):
        return TwoByThreeBoardsIter(self)

    def clear(self):
        for board in self:
            board.clear()

    def array(self):
        top = np.concatenate((self.boards[0][0].board, self.boards[1][0].board, self.boards[2][0].board), axis=0)
        bottom = np.concatenate((self.boards[0][1].board, self.boards[1][1].board, self.boards[2][1].board), axis=0)
        return np.concatenate((top, bottom), axis=1)