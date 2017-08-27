from __future__ import absolute_import
from __future__ import unicode_literals

from flask import Flask, request, jsonify, abort
import os

from utils.auth import authorize
from utils import slack_commands_helper
from services.game import GameService
from services.game import START_COMMAND
from services.game import MOVE_COMMAND
from services.game import STATUS_COMMAND

app = Flask(__name__)
game_service = GameService()



@app.route('/hello', methods=['POST'])
@authorize
def slash_command():
    """Parse the command parameters, validate them, and respond.
    Note: This URL must support HTTPS and serve a valid SSL certificate.
    """
    # Parse the parameters you need
    print 'blablah'
    token = request.form.get('token', None)  # TODO: validate the token
    command = request.form.get('command', None)
    team_id = request.form.get('team_id', None)
    text = request.form.get('text', None)
    # Validate the request parameters
    if not token:  # or some other failure condition
        abort(400)
    # 2. Return a JSON payload
    # See https://api.slack.com/docs/formatting and
    # https://api.slack.com/docs/attachments to send richly formatted messages
    return jsonify({
        # Uncomment the line below for the response to be visible to everyone
        # 'response_type': 'in_channel',
        'text': 'More fleshed out response to the slash command ' + token,
        'attachments': [
            {
                'fallback': 'Required plain-text summary of the attachment.',
                'color': '#36a64f',
                'pretext': 'Optional text above the attachment block',
                'author_name': 'Bobby Tables',
                'author_link': 'http://flickr.com/bobby/',
                'author_icon': 'http://flickr.com/icons/bobby.jpg',
                'title': 'Slack API Documentation',
                'title_link': 'https://api.slack.com/',
                'text': 'Optional text that appears within the attachment',
                'fields': [
                    {
                        'title': 'Priority',
                        'value': 'High',
                        'short': False
                    }
                ],
                'image_url': 'http://my-website.com/path/to/image.jpg',
                'thumb_url': 'http://example.com/path/to/thumb.png'
            }
        ]
    })


@app.route('/ttt', methods=['POST'])
@authorize
def tic_tac_toe_command():
    """Parse the command parameters, validate them, and respond.
    Note: This URL must support HTTPS and serve a valid SSL certificate.
    """

    # Parse the parameters you need
    text = request.form.get('text', None)
    channel_id = request.form.get('channel_id', None)
    user = request.form.get('user_name', None)

    if not text or text == 'help':
        return jsonify({
            'text': 'blah blah how to use the game'
        })
    elif text == STATUS_COMMAND:
        result = game_service.get_game_status(channel_id)
        return jsonify(result)
    elif text.startswith(START_COMMAND):
        result = game_service.create_new_game(
            channel_id,
            command_text=text,
            o_player=user,
        )
        print result
        return jsonify(result)
    elif text.startswith(MOVE_COMMAND):
        result = game_service.make_move(channel_id, user, text)
        return jsonify(result)
    else:
        return jsonify({
            'text': 'blah blah how to use the game'
        })


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
