from __future__ import absolute_import
from __future__ import unicode_literals

from entities.board import Board
from entities.board import IllegalMoveException
from services import instruction
from utils.slack_commands_helper import (
    create_response,
    get_user_from_start_command,
    InvalidCommandUseException,
    parse_move_command,
)

START_COMMAND = 'start'
MOVE_COMMAND = 'move'
STATUS_COMMAND = 'status'

class GameService:
    def __init__(self):
        self.ongoing_games = {}

    def get_game_status(self, channel_id):
        board = self.ongoing_games.get(channel_id)
        if board:
            return create_response(board.to_string())
        if not board:
            return create_response(
                instruction.get_no_games_text(),
                public=False
            )

    def create_new_game(self, channel_id, command_text, o_player):
        if self.ongoing_games.get(channel_id):
            return create_response(
                instruction.get_ongoing_game_exists_text(),
                public=False
            )

        try:
            x_player = get_user_from_start_command(command_text)
        except InvalidCommandUseException:
            return create_response(
                instruction.get_invalid_command_text(START_COMMAND),
                public=False
            )

        new_board = Board(x_player, o_player)
        self.ongoing_games[channel_id] = new_board

        response = '<@' + x_player + '> is X.\n' + new_board.to_string()

        return create_response(response)

    def make_move(self, channel_id, user, command_text):
        try:
            x, y = parse_move_command(command_text)
        except InvalidCommandUseException:
            return create_response(
                instruction.get_invalid_command_text(MOVE_COMMAND),
                public=False
            )

        board = self.ongoing_games.get(channel_id)
        if not board:
            return create_response(
                instruction.get_no_games_text(),
                public=False
            )

        try:
            board.move(int(x), int(y), user)
        except IllegalMoveException as e:
            return create_response(
                instruction.get_invalid_move_text(e.message),
                public=False
            )

        is_complete, winner = board.is_complete()
        result = board.to_string()
        if is_complete:
            self.ongoing_games[channel_id] = None
            if winner:
                result += 'The winner is <@' + winner + '>'
            else:
                result += 'the game ended in a tie.'

        return create_response(result)





