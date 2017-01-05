import os
import re

from flask import Flask, request, jsonify
from slacker import Slacker
from flask.ext.sqlalchemy import SQLAlchemy

from channel import Channel 
from game import Game 
from board import Board 

app = Flask(__name__)
from werkzeug.serving import run_simple
slacker = Slacker(os.environ['SLACK_API_KEY'])
db = SQLAlchemy(app)

def channel_in_db():
    return Channel.query.order_by(Channel.channel_name)

def add_channel(chan, users, channel_list, team):
    for chan_obj in channel_list:
        if chan['id'] == chan_obj.channel_id:
            return chan_obj
    return Channel(chan, team)

# Get users list
response = slacker.users.list()
users = response.body['members']

@app.route('/', methods=['POST'])
def main():
    """ token=SECRET
        team_id=T0001
        team_domain=example
        channel_id=C2147483705
        channel_name=test
        user_id=U2147483697
        user_name=Steve
        command=/weather
        text=94070
        response_url=https://hooks.slack.com/commands/1234/5678
    """

    resp = {
        "response_type": "in_channel",
        "text": ""
    }
    # check auth
    token = request.form.get('token')
    if token != os.environ['SECRET_KEY']:
        resp['response_type'] = 'ephemeral'
        resp['text'] = 'Authorization token not recognized'
        return jsonify(resp)

    # get the rest of our message
    # and the users who are issueing it
    text = request.form.get('text')
    text = text.split(' ')
    if len(text) == 0:
        resp["response_type"] = 'ephemeral'
        resp["text"] = 'Not a valid command'
        jsonify(resp)
    command = text[0]
    channel = {
        'id':str(request.form.get('channel_id')),
        'name': str(request.form.get('channel_name'))
        }
    user = {
        'id': str(request.form.get('user_id')),
        'name': str(request.form.get('user_name'))
        }
    team = {
        'id': str(request.form.get('team_id')),
        'domain': str(request.form.get('team_domain'))
        }
    channel_list = channels_in_db()

    curr_channel = add_channel(channel, users, channel_list, team)

    if 'start' == command:
        '''Have a user challenge another to user
        '''
        opponent = dict()
        if len(text) < 2:
            resp["response_type"] = 'ephemeral'
            resp["text"] = 'Arguments for start are `/ttt start [user]`'
            return jsonify(resp)
        opponent['name'] = re.sub('@', '', text[1])
        resp['text'] = curr_channel.new_game(user, opponent, users)
        return jsonify(resp)

    elif 'current' == command:
        '''Print out the board and who moves next in the game
        '''
        board, stats = curr_channel.game_status()
        resp['text'] = board + '\n' + stats[0] + '\n' + stats[1]
        return jsonify(resp)

    elif 'move' == command:
        '''Confirm digit is in range and free to move to
        '''
        if len(text) < 2:
            resp["text"] = 'Arguments for move are `/ttt move [1-9]`, not enough arguments'
            return jsonify(resp)
        digit = int(text[1])
        if digit <= 9 and digit >= 1:
            resp["response_type"], resp["text"] = curr_channel.move_piece(user, digit-1)
        else:
            resp["response_type"] = 'ephemeral'
            resp["text"] = 'Digit not in acceptable range.'

    elif 'end' == command:
        '''Force quit current game
        '''
        resp["text"] = curr_channel.end_game(user)

    elif 'help' == command:
        resp["response_type"] = 'ephemeral'
        resp["text"] = '''Play a game of tictactoe against your friends\n
        `/ttt start [user]` - Begin a game againt a specific user\n
        `/ttt move [1-9]'*** - Move the users piece and returns the new board\n
        `/ttt instructions'*** - Returns the instructions for the game\n
        `/ttt help'*** - Returns all of the possible moves for the slash command\n
        `/ttt end'*** - Allows one of the two users to forfeit and stop the game\n'''

    return jsonify(resp)



if __name__ == '__main__':
    app.run()
