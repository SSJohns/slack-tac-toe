from app import db

oSymbol = ":o:"
xSymbol = ":x:"
cSymbol = ":no_entry_sign:"

class Channel(db.Model):
    channel_id = db.Column(db.String, primary_key=True)
    channel_name = db.Column(db.String)
    team_id = db.Column(db.String)
    team_domain = db.Column(db.String)
    game_id = db.Column(db.Interger, db.Foreign_key('game.game_id'))

    def __init__(self, channel, team):
        self.channel_id = channel['id']
        self.channel_name = channel['name']
        self.team_id = team['id']
        self.team_name = team['name']

    def __repr__(self):
        return '<Channel %r>' % self.channel_name

    def new_game(self, challenger, opponent, users):
        '''Init a game if there are no current games going
        '''
        game = Game.query.filter_by(game_id=self.game_id).first()

        if game is not None:
            return self.game.print_game() + '\nThere\'s already existing a game, you have to finish it before starting a new'

        for usr in users:
            if opponent['name'] == usr['name']:
                opponent['id'] = usr['id']

        if 'id' not in opponent:
            return 'Sorry, couldn\'t find that user'
        game = Game(challenger, opponent)

        self.game_id = game.game_id

        return game.print_game() + '\nCreated a new game state, it is @{!s}\'s turn. To make move `/ttt move [1-9]`.'.format(game.turn())

    def move_piece(self, player, spot):
        '''Run thorugh checks to see if we can move a piece, then update turns
        '''
        game = Game.query.filter_by(game_id=self.game_id).first()
        
        if game is None:
        	return 'ephemeral', 'No games in progress'

        if game.winner is not None:
            return 'in_channel', game.print_game()

        def move(start_id, other_id,move, sym):
        	if game.move(start_id, move):
                    game.turn = other_id
                    game.state = 'It is @{!s}\'s turn. They are {!s}'.format(other_id, sym)
                    if game.winning_move():
                        game.status = 'Done'
                        game.state = 'Game Ended winner is {!s}'.format(game.winner['name'])
                    return 'in_channel', game.print_game() + '\n' + game.state
                else:
                    return 'ephemeral', game.print_game() + '\n' + 'Invalid move'
        # if it's this players turn move their pieces
        if player['id'] == game.turn:
            if player['id'] == game.challenger_id:
                move(game.challenger_id, game.opponent_id, spot, oSymbol)
            else:
                move(game.opponent_id, game.challenger_id, spot, xSymbol)
        else:
            return 'ephemeral', game.print_game() + '\n' + 'It is not that users turn'

	def game_status(self):
        '''Returns the board and active state of the game
        '''
		game = Game.query.filter_by(game_id=self.game_id).first()
        
        if game is None:
        	return 'ephemeral', 'No games in progress'

        if game.winner is not None:
            return 'in_channel', game.print_game()

        if game.status == 'Done':
            game.state = 'Game Ended winner is {!s}'.format(game.get_name(game.winner) )
        else:
            game.state = 'It is {!s}\'s turn'.format(game.turn())
        return game.print_game(), (game.status, game.state)

	def end_game(self, user):
        '''Only end a game if one of the two players request it. They then lose the match
        '''
        game = Game.query.filter_by(game_id=self.game_id).first()
        
        if game is None:
        	return 'ephemeral', 'No games in progress'

        if game.winner is not None:
            return 'in_channel', game.print_game()

        def winner(loser, winner):
        	game.winner = winner
            game.status = 'Done'
            board = game.print_game()
            self.game_id = None
            return '{!s}\n{!s} forfeited the game, {!s} is the winner'.format(board, game.get_name(loser), game.get_name(winner))

        if user['id'] == game.challenger_id:
            winner(game.challenger_id, game.opponent_id)
        elif user['id'] == game.opponent_id:
            winner(game.opponent_id, game.challenger_id)
        else:
            return game.print_game() + '\n' + 'User {!s} not authorized to end this game'.format(user['name'])        