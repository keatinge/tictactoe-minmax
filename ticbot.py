import itertools

i = 0
class Board:
    def __init__(self, state=None):
        self.state = state or [" "]*9
        self.numRows = 3

    def __str__(self):
        row_strs = []
        for row in self.rows():
            row_strs.append("|" + "|".join([cell or " " for cell in row]) + "|")
        return "\n".join(row_strs)

    def __repr__(self):
        return self.__str__()

    def __getitem__(self, item):
        return self.state[item]

    def __len__(self):
        return len(list(filter(lambda x: x != " ", self.state)))

    def rows(self):
        for i in range(self.numRows):
            yield self.state[i*3:(i*3)+3]

    def add_move(self, char:str, pos:int):
        assert char in ["X", "O"]
        assert 0 <= pos < len(self.state)
        self.state[pos] = char


class TTT():
    @staticmethod
    def get_winner(board:Board):
        win_combos = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]
        for combo in win_combos:
            combRow = [board[pos] for pos in combo]
            if len(set(combRow)) == 1 and " " not in combRow:
                return combRow[0]

    @staticmethod
    def abst_disp():
        abst_board = Board()
        abst_board.state = list(map(str, range(9)))
        print(abst_board.__str__())

    @staticmethod
    def get_pos_next_moves(board:Board, chr:str) -> list:
        state = board.state
        empty_indicies = [i for i, chr in enumerate(state) if chr == " "]

        boards = []
        for i in empty_indicies:
            new_board = Board(state[:])
            new_board.add_move(chr, i)
            boards.append(new_board)

        return boards

    @staticmethod
    def swap_chr(chr):
        assert chr in ["X", "O"]
        return "X" if chr == "O" else "O"

    #TODO
    def evaluate_score(self):
        pass
class Node:
    def __init__(self, board, chr="O", parent=None):
        self.board = board
        self.chr = chr
        self.childCr = TTT.swap_chr(chr)
        self.winner = TTT.get_winner(board)
        self.scoreX = (self.winner == "X") * 1
        self.scoreO = (self.winner == "O") * 1
        self.parent = parent


        if self.winner:
            self.children = []
        else:
            self.children = [Node(b, self.childCr, self) for b in TTT.get_pos_next_moves(board, self.childCr)]

    def __getitem__(self, item):
        return self.children[item]

    def find_best_child(self, scoreFN):
        if not self.children:
            return self
        return max([child.find_best_child(scoreFN) for child in self.children], key=scoreFN)

    def find_all_winners(self):
        if not self.children and self.scoreX == 1:
            yield self
        else:
            for child in self.children:
                yield from child.find_all_winners()

    def find_all_abs_children(self):
        if not self.children:
            yield self
        else:
            for child in self.children:
                yield from child.find_all_abs_children()

    def traverse_parents(self):
        cur_node = self

        while cur_node.parent:
            yield cur_node
            cur_node = cur_node.parent
        yield cur_node

b1 = Board()

b1.state = [" ", " ", " ", " ", " ", " ", " ", " ", " "]
print(b1)

n1 = Node(b1)
print("Fin gen nodes")
print(len(n1.children))




#child = n1.find_best_child(lambda x: x.scoreX - len(x.board))
bottoms = list(n1.find_all_abs_children())
