from app import db

oSymbol = ":o:"
xSymbol = ":x:"
cSymbol = ":no_entry_sign:"

class Board(db.Model):
    board_id = db.Column(db.Interger, primary_key=True)
    contents = db.Column(db.String, default='---------')
    game_id = db.Column(db.Interger, db.Foreign_key('game.game_id'))

    def __repr__(self):
        return '%r' % self.contents

    def reset():
    	self.contents = [cSymbol]*9