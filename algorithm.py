from package.board import TwoByThreeBoards, Direction, PossibilityMatrix

class Move:
    def __init__(self, pos, word, direction, heuristic=0, score=0, placement_count=0):
        self.pos = pos
        self.word = word
        self.direction = direction
        self.heuristic = heuristic
        self.score = score
        self.placement_count = placement_count

    def __gt__(self, other):
        if self.heuristic == other.heuristic:
            return self.score > other.score
        return self.heuristic > other.heuristic

class BadAppleAlgorithm:
    def __init__(self, px, board, gaddag, letter_scores):
        self.px = px
        self.board = board
        self.gaddag = gaddag
        self.letter_scores = letter_scores
        self.skip_node_cache = {}
        self.racks = [[], []]
        self.current_player_index = 0
        self.temp_rack = []

    def has_value(self, pos, direction):
        x = pos[0] * direction.value[1]
        y = pos[1] * direction.value[0]
        while x < 15 and y < 15:
            if self.px[x,y] == 255 and self.board.is_empty(x, y):
                return True
            x += direction.value[0]
            y += direction.value[1]
        return False

    def get_heuristic(self, pos):
        x, y = pos
        if not self.board.is_empty(x, y):
            return 0
        if self.px[x,y] == 255:
            return 2
        return -1

    def find_best_prefix(self, pos, node, direction, rack, blanks, word="", heuristic=0, score=0, placement_count=0):
        x, y = pos

        # End of prefix
        if node.letter == '+':
            # Existing tiles continue
            if x >= 0 and y >= 0 and not self.board.is_empty(x, y):
                return None

            # No suffix
            if node.is_terminal:
                return Move((x+1, y+1), word, direction, heuristic, score, placement_count)
            
            # Get best suffix from children
            best_move = None
            for child in node.children.values():
                move = self.find_best_suffix((x + len(word) + 1, y + len(word) + 1), child, direction, rack, blanks, word, heuristic, score, placement_count)
                if move is not None:
                    best_move = move if best_move is None else max(best_move, move)
            return best_move

        # Not possible
        if x < 0 or y < 0 or not self.board.can_place_letter(node.letter, pos, direction):
            return None

        updated_rack = rack.copy()

        # Increase placement if new tile
        if self.board.is_empty(x, y):
            if node.letter not in rack:
                if blanks == 0:
                    return None
                else:
                    blanks -= 1
            else:
                updated_rack.remove(node.letter)
            placement_count += 1
        if placement_count > 7:
            return None

        # Update prefix
        word = node.letter + word
        heuristic += self.get_heuristic(pos)
        if heuristic <= -7:
            return None
        score += self.letter_scores.get(node.letter, 0)
        
        # Get best prefix from children
        best_move = None
        for child in node.children.values():
            move = self.find_best_prefix((x - direction.value[0], y - direction.value[1]), child, direction, updated_rack, blanks, word, heuristic, score, placement_count)
            if move is not None:
                best_move = move if best_move is None else max(move, best_move)
        return best_move

    def find_best_suffix(self, pos, node, direction, rack, blanks, word, heuristic, score, placement_count):
        x, y = pos

        # Not possible
        if x >= 15 or y >= 15 or not self.board.can_place_letter(node.letter, pos, direction):
            return None

        updated_rack = rack.copy()

        # Increase placement if new tile
        if self.board.is_empty(x, y):
            if node.letter not in rack:
                if blanks == 0:
                    return None
                else:
                    blanks -= 1
            else:
                updated_rack.remove(node.letter)
            placement_count += 1
        if placement_count > 7:
            return None

        # Update suffix
        word += node.letter
        heuristic += self.get_heuristic(pos)
        if heuristic <= -7:
            return None
        score += self.letter_scores.get(node.letter, 0)

        # End of suffix
        if node.is_terminal:
            x2, y2 = x + direction.value[0], y + direction.value[1]
            if x2 < 15 and y2 < 15 and not self.board.is_empty(x2, y2):
                return None
            return Move((x - direction.value[0]*(len(word)-1), y - direction.value[1]*(len(word)-1)), word, direction, heuristic, score, placement_count)
        
        # Get best suffix from children
        moves = []
        for child in node.children.values():
            move = self.find_best_suffix((x + direction.value[0], y + direction.value[1]), child, direction, updated_rack, word, heuristic, score, placement_count)
            if move is not None:
                moves.append(move)
        return None if len(moves) == 0 else max(moves)
    
    def get_best_move_in_direction(self, direction, rack):
        rack_without_blanks = rack.copy()
        blanks = rack.count('#')
        for b in range(blanks):
            rack_without_blanks.remove('#')

        best_move = None
        for a in self.board.adjacents:
            x, y = a
            for a_letter in self.board.possibilities[direction].get_possible(x, y):
                for head in self.gaddag.get(a_letter):
                    if head in self.skip_node_cache.setdefault(a, set()):
                        continue
                    move = self.find_best_prefix((x, y), head, direction, rack_without_blanks, blanks)
                    if move is None:
                        self.skip_node_cache[a].add(head)
                        continue
                    if move.placement_count > 0 and (best_move is None or move > best_move):
                        best_move = move
                        if best_move.heuristic >= 10:
                            return best_move
        return best_move

    def get_best_move(self, rack):
        move1 = self.get_best_move_in_direction(Direction.RIGHT, rack)
        if move1 is not None and move1.heuristic >= 10:
            move = move1
        else:
            move2 = self.get_best_move_in_direction(Direction.DOWN, rack)
            if move1 is None and move2 is None:
                return None, rack
            if move1 is None:
                return move2, rack
            if move2 is None:
                return move1, rack
            move = max(move1, move2)

        # Reintroduce blanks
        word_with_blanks = ""
        for letter in move.word:
            if letter not in rack:
                # Lowercase signifies blank
                word_with_blanks += letter.lower()
                rack.remove('#')
            else:
                word_with_blanks += letter
                rack.remove(letter)
        move.word = word_with_blanks
        return move, rack

    def play(self, log=False):
        is_first_branch = True
        while True:
            self.racks[self.current_player_index] += self.board.draw_tiles(7 - len(self.racks[self.current_player_index]))
            print("Rack: %s" % ' '.join(self.racks[self.current_player_index]))
            move, self.racks[self.current_player_index] = self.get_best_move(self.racks[self.current_player_index])
            if move is None or move.heuristic < 0:
                if log:
                    print("No good move")
                if is_first_branch:
                    self.board.clear()
                break
            if log:
                print(move.pos, move.direction, move.heuristic, move.word)
            self.board.place_word(move.word, move.pos, move.direction)
            is_first_branch = False
            self.current_player_index = 1 - self.current_player_index