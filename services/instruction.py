from __future__ import absolute_import
from __future__ import unicode_literals


def get_invalid_command_text(command):
    return 'Invalid use of {}'.format(command)

def get_ongoing_game_exists_text():
    return 'There is an ongoing game in this channel'

def get_no_games_text():
    return 'There is no ongoing games in this channel'

def get_invalid_move_text(text):
    return 'Illegal move. {}'.format(text)
