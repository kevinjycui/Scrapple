class PossibilityMatrix:
    FULL = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    
    def __init__(self, board, direction):
        self.board = board
        self.matrix = []
        for i in range(15):
            row = []
            for j in range(15):
                row.append(PossibilityMatrix.FULL)
            self.matrix.append(row)
        self.direction = direction

    def print(self):
        for i in range(15):
            for j in range(15):
                if self.matrix[i][j] == PossibilityMatrix.FULL:
                    print('*', end='\t')
                else:
                    print(self.matrix[i][j], end='\t')
            print()

    def clear(self):
        for i in range(15):
            for j in range(15):
                self.matrix[i][j] = PossibilityMatrix.FULL

    def step(self, x, y):
        return x + self.direction.value[0], y + self.direction.value[1]

    def orth_step(self, x, y):
        return x + self.direction.value[1], y + self.direction.value[0]

    def orth_step_rev(self, x, y):
        return x - self.direction.value[1], y - self.direction.value[0]

    def update_possibilities(self, pos):
        prefix = ''
        suffix = ''

        x, y = pos

        # Not possible or already filled
        if x < 0 or y < 0 or x >= 15 or y >= 15 or not self.board.is_empty(x, y):
            return
        
        # Orthogonal higher
        x1, y1 = self.orth_step_rev(x, y)
        while x1 >= 0 and y1 >= 0 and not self.board.is_empty(x1, y1):
            prefix = self.board.get_letter(x1, y1) + prefix
            x1, y1 = self.orth_step_rev(x1, y1)
        
        # Orthogonal lower
        x2, y2 = self.orth_step(x, y)
        while x2 < 15 and y2 < 15 and not self.board.is_empty(x2, y2):
            suffix += self.board.get_letter(x2, y2)
            x2, y2 = self.orth_step(x2, y2)

        # Has letters orthogonally lower only
        if prefix == '' and suffix != '':
            possible = []
            for head in self.board.context.trie.root.children.values():
                if head.search(suffix):
                    possible.append(head.letter)
            self.matrix[y][x] = ''.join(possible)

        # Has letters orthogonally higher only
        elif prefix != '' and suffix == '':
            possible = []
            for tail in self.board.context.trie_reverse.root.children.values():
                if tail.search(prefix[::-1]):
                    possible.append(tail.letter)
            self.matrix[y][x] = ''.join(possible)

        # Has letters orthogonally on both sides
        elif prefix != '' and suffix != '':
            node = self.board.context.trie.root.get(prefix)
            if node is None:
                self.matrix[y][x] = ""
            else:
                possible = []
                for head in node.children.values():
                    if head.search(suffix):
                        possible.append(head.letter)
                self.matrix[y][x] = ''.join(possible)

    def place_letter(self, letter, pos):
        x, y = pos
        self.matrix[y][x] = letter

    def is_possible(self, x, y, letter):
        return letter in self.matrix[y][x]

    def get_possible(self, x, y):
        return self.matrix[y][x]