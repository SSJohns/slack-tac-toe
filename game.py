from app import db

oSymbol = ":o:"
xSymbol = ":x:"
cSymbol = ":no_entry_sign:"

class Game(db.Model):
    __tablename__ = 'game'
    game_id = db.Column(db.Interger, primary_key=True)
    challenger_id = db.Column(db.String)
    challenger_name = db.Column(db.String)
    opponent_id = db.Column(db.String)
    opponent_name = db.Column(db.String)
    winner = db.Column(db.String)
    turn = db.Column(db.String)
    state = db.Column(db.String)
    moves = db.Column(db.Interger)
    board_id = db.Column(db.Interger, db.Foreign_key('board.board_id'))

    def __init__(self, challenger, opponent):
        self.challenger_id = challenger['id']
        self.channel_name = challenger['name']
        self.opponent_id = opponent['id']
        self.opponent_name = opponent['name']
        self.turn = challenger['id']
        self.winner = None
        self.state = 'It is @{!s}\'s turn. They are x'.format(self.challenger_id)
        self.board = Board()
        self.board_id = self.board.board_id
        self.moves = 0

    def __repr__(self):
        return '<Game %r>' % self.channel_name

    def turn(self):
    	return self.get_name(self.turn)

    def get_name(self, given_id):
    	if given_id == self.challenger_id:
    		return self.challenger_name
    	else:
    		return self.opponent_name

    def print_game(self):
        return '| {!s} | {!s} | {!s} |\t\n|-----+-----+-----|\n| {!s} | {!s} | {!s} |\t\n|-----+-----+-----|\n| {!s} | {!s} | {!s} |'.format(self.board.contents.split())

    def winning_move(self):
    	combinations = (
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
        for move in combinations:
            if (self.board.contents[move[0]] == self.board.contents[move[1]] == self.board.contents[move[2]] == xSymbol):
                self.winner = self.challenger_id
                return True
            if (self.board.contents[move[0]] == self.board.contents[move[1]] == self.board.contents[move[2]] == oSymbol):
                self.winner = self.opponent_id
                return True
        if self.cat_game():
            return True
        return False

    def cat_game(self):
        if self.moves >= 9:
            self.winner = 'cat game'
            self.reset_game()
            return True
        return False

    def is_empty(self, spot):
        return (self.board[spot] == '-')

    def move(self, player, spot):
        if not self.is_empty(spot):
            return False
        if player == self.challenger_id:
            self.board[spot] = self.challenger_sym
            self.moves += 1
            return True
        elif player == self.opponent_id:
            self.board[spot] = self.opponent_sym
            self.moves += 1
            return True