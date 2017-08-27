from __future__ import absolute_import
from __future__ import unicode_literals

import re

from flask import jsonify

from utils.exceptions import InvalidCommandUseException


def create_response(text, public=True):
    return {
        'response_type': 'in_channel' if public else 'ephemeral',
        'text': text
    }


def get_user_from_start_command(command):
    command_list = command.split()
    if len(command_list) != 2:
        return InvalidCommandUseException
    user_alias = re.search('@(.+?)', command_list[1])
    if user_alias:
        return command_list[1][1:]
    else:
        raise InvalidCommandUseException


def parse_move_command(command):
    command_list = command.split()
    if len(command_list) != 3:
        raise InvalidCommandUseException
    x = command_list[1]
    y = command_list[2]
    if x.isdigit() and y.isdigit():
        return x, y
    else:
        raise InvalidCommandUseException





