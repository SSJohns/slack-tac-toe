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
            'status': 'Nope',
            'state': 'No Games in Progress'
        }
        self.game = Game()
        self.members = users

    def new_game(self, challenger, opponent, users):
        '''Init a game if there are no current games going
        '''
        if self.active['status'] == 'Playing' or self.active['status'] == 'Pending':
            return self.game.print_game() + '\nThere\'s already existing a game, you have to finish it before starting a new'
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
        self.game.init_game({
            'challenger': challenger,
            'opponent': opponent
        })
        return self.game.print_game() + '\nCreated a new game state, it is @{!s}\'s turn. To make move `/ttt move [1-9]`.'.format(self.turn['name'])

    def move_piece(self, player, spot):
        '''Run thorugh checks to see if we can move a piece, then update turns
        '''
        if self.active['status'] == 'Done':
            return 'in_channel', self.active['state']

        # if it's this players turn move their pieces
        print player, self.turn, spot, type(spot)
        if player['id'] == self.turn['id']:
            if player['id'] == self.challenger['id']:
                if self.game.move(player, spot):
                    self.turn = self.opponent
                    self.active['state'] = 'It is @{!s}\'s turn. They are {!s}'.format(self.opponent['name'], self.game.opponent_sym)
                    if self.game.winning_move():
                        self.active['status'] = 'Done'
                        self.active['state'] = 'Game Ended winner is {!s}'.format(self.game.winner['name'])
                    return 'in_channel',self.game.print_game() + '\n' + self.active['state']
                else:
                    return 'ephemeral',self.game.print_game() + '\n' + 'Invalid move'
            else:
                if self.game.move(player, spot):
                    self.turn = self.challenger
                    self.active['state'] = 'It is @{!s}\'s turn. They are {!s}'.format(self.challenger['name'], self.game.challenger_sym)
                    if self.game.winning_move():
                        self.active['status'] = 'Done'
                        self.active['state'] = 'Game Ended winner is {!s}'.format(self.game.winner['name'])
                    return 'in_channel',self.game.print_game() + '\n' + self.active['state']
                else:
                    return 'ephemeral',self.game.print_game() + '\n' + 'Invalid move'
        else:
            return 'ephemeral',self.game.print_game() + '\n' + 'It is not that users turn'

    def game_status(self):
        '''Returns the board and active state of the game
        '''
        if self.active['status'] == 'Done':
            self.active['state'] = 'Game Ended winner is {!s}'.format(self.game.winner)
        elif self.active['status'] == 'Playing':
            self.active['state'] = 'It is {!s}\'s turn'.format(self.turn['name'])
        return self.game.print_game(), self.active

    def end_game(self, user):
        '''Only end a game if one of the two players request it. They then lose the match
        '''
        if user['id'] == self.challenger['id']:
            self.winner = self.opponent['name']
            self.active['status'] = 'Done'
            self.active['winner'] = self.opponent['name']
            board = self.game.print_game()
            self.game.reset_game()
            return '{!s}\n{!s} forfeited the game, {!s} is the winner'.format(board, user['name'], self.opponent['name'])
        elif user['id'] == self.opponent['id']:
            self.winner = self.challenger
            self.active['status'] = 'Done'
            self.active['winner'] = self.challenger
            board = self.game.print_game()
            self.game.reset_game()
            return '{!s}\n{!s} forfeited the game, {!s} is the winner'.format(board, user['name'], self.challenger['name'])
        else:
            return self.game.print_game() + '\n' + 'User {!s} not authorized to end this game'.format(user)


def new_channel(chan_id, users):
    """Logging a new channel"""
    channel_list[chan_id] = Channel(chan_id, users)


def add_channel(chan_id, users):
    if chan_id not in channel_list:
        new_channel(chan_id, users)
    return channel_list[chan_id]
