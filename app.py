from flask import Flask, request, jsonify
from slacker import Slacker

import channels as channels_obj
import config
import re

app = Flask(__name__)
from werkzeug.serving import run_simple
slacker = Slacker(config.SLACK_API_KEY)


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
        "response_type": "200",
        "text": ""
    }
    # check auth
    token = request.form.get('token')
    if token != config.SECRET_KEY and token != config.LUG_SECRET_KEY:
        resp['response_type'] = '401 Unauthorized'
        resp['text'] = 'Authorization token not recognized'
        return jsonify(resp)

    # get the rest of our message
    # and the users who are issueing it
    text = request.form.get('text')
    text = text.split(' ')
    if len(text) == 0:
        resp["response_type"] = '400 Bad Request'
        resp["text"] = 'Not a valid command'
        jsonify(resp)
    command = text[0]
    channel = str(request.form.get('channel_id'))
    user = {
        'id': str(request.form.get('user_id')),
        'name': str(request.form.get('user_name'))
        }
    curr_channel = channels_obj.add_channel(channel, users)

    if 'start' == command:
        '''Have a user challenge another to user
        '''
        opponent = dict()
        if len(text) < 2:
            resp["text"] = 'Arguments for start are `/ttt start [user]`'
            return jsonify(resp)
        opponent['name'] = re.sub('@', '', text[1])
        resp['text'] = curr_channel.new_game(user, opponent, users)
        return jsonify(resp)

    if 'current' == command:
        '''Print out the board and who moves next in the game
        '''
        board, stats = curr_channel.game_status()
        resp['text'] = board + '\n' + stats['status'] + '\n' + stats['state']
        return jsonify(resp)

    if 'move' == command:
        '''Confirm digit is in range and free to move to
        '''
        if len(text) < 2:
            resp["text"] = 'Arguments for move are `/ttt move [1-9]`, not enough arguments'
            return jsonify(resp)
        digit = int(text[1])
        if digit <= 9 and digit >= 1:
            resp["text"] = curr_channel.move_piece(user, digit-1)
        else:
            resp["text"] = 'Digit not in acceptable range.'

    if 'end' == command:
        '''Force quit current game
        '''
        resp["text"] = curr_channel.end_game(user)

    return jsonify(resp)


if __name__ == '__main__':
    # app.debug = True
    app.run()
