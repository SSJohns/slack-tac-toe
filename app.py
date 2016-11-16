from flask import Flask, request, jsonify
from slacker import Slacker

import channels as channels_obj
import config
import re

app = Flask(__name__)
from werkzeug.serving import run_simple
slacker = Slacker(config.SLACK_API_KEY)
# game = game.Game()


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
    if token != config.SECRET_KEY:
        resp['response_type'] = '401 Unauthorized'
        resp['text'] = 'Authorization token not recognized'
        return jsonify(resp)

    # get the rest of our message
    text = request.form.get('text')
    text = text.split(' ')
    command = text[0]
    channel = str(request.form.get('channel_id'))
    user = {
        'id':str(request.form.get('user_id')),
        'name':str(request.form.get('user_name'))
        }
    # print user
    curr_channel = channels_obj.add_channel(channel, users)

    if 'start' == command:
        opponent = dict()
        if len(text) < 2:
            resp["text"] = 'Arguments for start are `/ttt start [user]`'
            return jsonify(resp)
        opponent['name'] = re.sub('@', '', text[1])
        resp['text'] = curr_channel.new_game(user, opponent, users)
        return jsonify(resp)

    if 'current' == command:
        board, stats = curr_channel.game_status()
        resp['text'] = board + '\n' + stats['status'] + '\n' + stats['state']
        return jsonify(resp)

    if 'move' == command:
        if len(text) < 2:
            resp["text"] = 'Arguments for move are `/ttt move [1-9]`, not enough arguments'
            return jsonify(resp)
        # try:
        digit = int(text[1])
        print "Dig",digit
        if digit <= 9 and digit >= 1:
            print digit, 'in range'
            resp["text"] = curr_channel.move_piece(user, digit-1)
            print resp["text"]
            return jsonify(resp)
        else:
            raise ValueError('Outside range')
        # except:
        #     resp["text"] = 'Arguments for move are `/ttt move [1-9]`'
        #     return jsonify(resp)

    if 'end' == command:
        resp = curr_channel.end_game(user)

    # if 'move' in text:
    return jsonify(resp)


if __name__ == '__main__':
    # app.debug = True
    app.run()
