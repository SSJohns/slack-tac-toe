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
            'status':'None',
            'winner':''
        }
        self.board = [['-','-','-'],
                      ['-','-','-'],
                      ['-','-','-']
                     ]
        self.game = Game()
        self.members = users

    def new_game(self, challenger, opponent):
        if self.active['status'] == 'Playing' or self.active['status'] == 'Pending':
            return ('200','There\'s already existing a game, you have to finish it before starting a new')
        self.challenger = challenger
        self.opponent = opponent
        self.active['status'] = 'Playing'
        self.turn = challenger
        return ('200','"Created a new game state, your turn as {!s}. To make move `/ttt move [1-9]`."'.format(challenger))

    def move_piece(self, player, spot):
        self.game.move(player, spot)

    def game_status(self):
        if self.game.cat_game():
            self.active['winner'] = 'Game Ended winner is {!s}'.format(self.game.winner)
        elif self.game.winning_move():
            self.active['winner'] = 'Game Ended winner is {!s}'.format(self.game.winner)
        return self.active

    def end_game(self, user):
        '''Only end a game if one of the two players request it. They then lose the match'''
        if user == self.challenger:
            self.winner = self.opponent
            self.active['status'] = 'Done'
            self.active['winner'] = self.opponent
            return '{!s} forfeited the game, {!s} is the winner'.format(user, self.opponent)
        elif user == self.opponent:
            self.winner = self.challenger
            self.active['status'] = 'Done'
            self.active['winner'] = self.challenger
            return '{!s} forfeited the game, {!s} is the winner'.format(user, self.challenger)
        else:
            return 'User {!s} not authorized to end this game'.format(user)

def new_channel(chan_id, users):
    """Logging a new channel"""
    channel_list[chan_id] = Channel(chan_id, users)

def add_channel(chan_id, users):
    if chan_id not in channel_list:
        new_channel(chan_id, users)
    return channel_list[chan_id]
