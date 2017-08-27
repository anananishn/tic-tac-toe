from __future__ import absolute_import
from __future__ import unicode_literals

import pytest

from utils import slack_commands_helper
from utils.slack_commands_helper import InvalidCommandUseException


def test_parse_start_command():
    start_text = 'start @blabla'
    user_alias = slack_commands_helper.get_user_from_start_command(start_text)
    assert user_alias == 'blabla'


def test_parse_start_command_invalid():
    start_text = 'start now'
    with pytest.raises(InvalidCommandUseException):
        slack_commands_helper.get_user_from_start_command(start_text)


def test_parse_move_command():
    start_text = 'move 1 2'
    x, y = slack_commands_helper.parse_move_command(start_text)
    assert x, y == (1, 2)

def test_parse_move_command_invalid():
    start_text = 'move 1,2'
    with pytest.raises(InvalidCommandUseException):
        slack_commands_helper.parse_move_command(start_text)
