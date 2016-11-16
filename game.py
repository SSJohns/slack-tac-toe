oSymbol = ":o:"
xSymbol = ":x:"
cSymbol = ":no_entry_sign:"

class Game:
    def __init__(self):
        self.board = [cSymbol,cSymbol,cSymbol,cSymbol,cSymbol,cSymbol,cSymbol,cSymbol,cSymbol]
        self.challenger = ''
        self.opponent = ''
        self.challenger_sym = xSymbol
        self.opponent_sym = oSymbol
        self.combinations = (
    		# Horisontal lines
    		[0, 1, 2],
    		[3, 4, 5],
    		[6, 7, 8],

    		# Vertical lines
    		[0, 3, 6],
    		[1, 4, 7],
    		[2, 5, 8],

    		# Diagonals
    		[0, 4, 8],
    		[2, 4, 6],
        )
        self.moves = 0
        self.winner = ''

    def init_game(self, players):
        self.challenger = players['challenger']
        self.opponent = players['opponent']
        self.turn = self.challenger
        self.board = [cSymbol,cSymbol,cSymbol,cSymbol,cSymbol,cSymbol,cSymbol,cSymbol,cSymbol]

    def print_game(self):
        return '| {!s} | {!s} | {!s} |\t\n|---+---+---|\n| {!s} | {!s} | {!s} |\t\n|---+---+---|\n| {!s} | {!s} | {!s} |'.format(self.board[0],self.board[1],self.board[2],self.board[3],self.board[4],self.board[5],self.board[6],self.board[7],self.board[8])

    def winning_move(self):
        for move in self.combinations:
            print move
            if (self.board[move[0]] == self.board[move[1]] == self.board[move[2]] == xSymbol):
                self.winner = self.challenger
                return True
            if (self.board[move[0]] == self.board[move[1]] == self.board[move[2]] == oSymbol):
                self.winner = self.opponent
                return True
        if self.cat_game():
            return True
        return False

    def is_empty(self, spot):
        return (self.board[spot] == cSymbol)

    def move(self, player, spot):
        if not self.is_empty(spot):
            return False
        if player['id'] == self.challenger['id']:
            self.board[spot] = self.challenger_sym
            self.moves += 1
            return True
        elif player['id'] == self.opponent['id']:
            self.board[spot] = self.opponent_sym
            self.moves += 1
            return True

    def cat_game(self):
        if self.moves >= 9:
            self.winner = 'cat game'
            self.reset_game()
            return True
        return False

    def reset_game(self):
        self.moves = 0
        self.board = [cSymbol,cSymbol,cSymbol,cSymbol,cSymbol,cSymbol,cSymbol,cSymbol,cSymbol]
        self.challenger = ''
        self.opponent = ''
