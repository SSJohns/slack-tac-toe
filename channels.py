from game import Game
channel_list = {}


class Channel:
    def __init__(self, channel_id, users):
        self.channel = channel_id
        self.challenger = ''
        self.opponent = ''
        self.players = set()
        self.challenge_accepted = False
        self.turn = ''
        self.win = None
        self.active = {
            'status':'Done',
            'state':'No Games in Progress'
        }
        self.game = Game()
        self.members = users

    def new_game(self, challenger, opponent, users):
        print challenger, opponent, users
        if self.active['status'] == 'Playing' or self.active['status'] == 'Pending':
            return 'There\'s already existing a game, you have to finish it before starting a new'
        for usr in users:
            if opponent['name'] == usr['name']:
                opponent['id'] = usr['id']
        if 'id' not in opponent:
            return 'Sorry, couldn\'t find that user'
        self.challenger = challenger
        self.opponent = opponent
        self.active['status'] = 'Playing'
        self.active['state'] = 'It is {!s}\'s turn.'.format(self.challenger['name'])
        self.turn = challenger
        self.game.init_game(
            {
            'challenger':challenger,
            'opponent':opponent
            }
        )
        # import ipdb; ipdb.set_trace()
        return "Created a new game state, it is {!s}\'s turn. To make move `/ttt move [1-9]`.".format(self.turn['name'])

    def move_piece(self, player, spot):
        print player, self.active, self.turn
        if self.active['status'] == 'Done':
            return self.active['state']
        if player['id'] == self.turn['id']:
            if player['id'] == self.challenger['id']:
                if self.game.move(player, spot):
                    self.turn = self.opponent
                    self.active['state'] = 'It is {!s}\'s turn. They are {!s}'.format(self.opponent['name'], self.game.opponent_sym)
                    if self.game.winning_move():
                        self.active['status'] = 'Done'
                        self.active['state'] = 'Game Ended winner is {!s}'.format(self.game.winner['name'])
                    return self.active['state']
                else:
                    return 'Invalid move'
            else:
                if self.game.move(player, spot):
                    self.turn = self.challenger
                    self.active['state'] = 'It is {!s}\'s turn. They are {!s}'.format(self.challenger['name'], self.game.challenger_sym)
                    if self.game.winning_move():
                        self.active['status'] = 'Done'
                        self.active['state'] = 'Game Ended winner is {!s}'.format(self.game.winner['name'])
                    return self.active['state']
                else:
                    return 'Invalid move'
        else:
            return 'It is not that users turn'

    def game_status(self):
        if self.active['status'] == 'Done':
            self.active['state'] = 'Game Ended winner is {!s}'.format(self.game.winner)
        elif self.active['status'] == 'Playing':
            self.active['state'] = 'It is {!s}\'s turn'.format(self.turn['name'])
        return self.game.print_game(), self.active

    def end_game(self, user):
        '''Only end a game if one of the two players request it. They then lose the match'''
        print "User", user
        print "challenger",self.challenger
        print "opp", self.opponent
        if user['id'] == self.challenger['id']:
            self.winner = self.opponent['name']
            self.active['status'] = 'Done'
            self.active['winner'] = self.opponent['name']
            board = self.game.print_board()
            self.game.reset_game()
            return '{!s}\n{!s} forfeited the game, {!s} is the winner'.format(board, user['name'], self.opponent['name'])
        elif user['id'] == self.opponent['id']:
            self.winner = self.challenger
            self.active['status'] = 'Done'
            self.active['winner'] = self.challenger
            board = self.game.print_board()
            self.game.reset_game()
            return '{!s}\n{!s} forfeited the game, {!s} is the winner'.format(board, user['name'], self.challenger['name'])
        else:
            return 'User {!s} not authorized to end this game'.format(user)

def new_channel(chan_id, users):
    """Logging a new channel"""
    channel_list[chan_id] = Channel(chan_id, users)

def add_channel(chan_id, users):
    if chan_id not in channel_list:
        new_channel(chan_id, users)
    return channel_list[chan_id]
