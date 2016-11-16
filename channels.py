from game import Game
channel_list = {}


class Channel:
    def __init__(self, channel_id):
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
        self.members = self.member_list()

    def new_game:
        if self.active['status'] == 'Playing' or self.active['status'] == 'Pending':
            return 'Game in Progress'
        self.challenger = challenger
        self.opponent = opponent
        self.active['status'] = 'Pending'

    def member_list(self, resp):
        """Generate a list of members in the channel"""
        existing_users = []
        for it in resp:
            print it
            for key, value in it.iteritems():
                if key == "name":
                    existing_users.append(str(value))
        return existing_users

    def move_piece(self, player, spot):
        self.game.move(player, spot)

    def game_status():
        if self.game.cat_game():
            self.active['winner'] = 'Game Ended winner is %s'.format(self.game.winner)
        elif self.game.winning_move():
            self.active['winner'] = 'Game Ended winner is %s'.format(self.game.winner)
        return self.active =

def new_channel(chan_id):
    """Logging a new channel"""
    channel_list[chan_id].append(Channel(chan_id))

def add_channel(chan_id):
    if chan_id not in channel_list:
        new_channel(chan_id)
    return channel_list[chan_id]
