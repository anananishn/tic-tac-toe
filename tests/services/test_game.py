from __future__ import absolute_import
from __future__ import unicode_literals

from services.game import GameService
from services.game import instruction
from services.game import START_COMMAND
from services.game import MOVE_COMMAND


class TestGameService(object):

    def test_game_status(self):
        game_service = GameService()
        channel_id = 'ch_1'
        o_user = 'me'
        command = 'start @you'
        game_service.create_new_game(
            channel_id,
            command_text=command,
            o_player=o_user,
        )
        result = game_service.get_game_status(channel_id)
        assert '<@you> \'s turn is next' in result['text']
        assert result['response_type'] == 'in_channel'

    def test_game_status_no_game(self):
        game_service = GameService()
        channel_id = 'ch_1'
        result = game_service.get_game_status(channel_id)
        assert result['text'] == instruction.get_no_games_text()
        assert result['response_type'] == 'ephemeral'

    def test_create_game(self):
        game_service = GameService()
        channel_id = 'ch_1'
        o_user = 'me'
        command = 'start @you'
        result = game_service.create_new_game(
            channel_id,
            command_text=command,
            o_player=o_user,
        )
        assert game_service.ongoing_games[channel_id]
        assert result['text'].startswith('<@you> is X.')
        assert result['response_type'] == 'in_channel'

    def test_game_exists(self):
        game_service = GameService()
        channel_id = 'ch_1'
        o_user = 'me'
        command = 'start @you'
        game_service.create_new_game(
            channel_id,
            command_text=command,
            o_player=o_user,
        )
        result = game_service.create_new_game(
            channel_id,
            command_text=command,
            o_player=o_user,
        )
        assert game_service.ongoing_games[channel_id]
        assert result['text'] == instruction.get_ongoing_game_exists_text()
        assert result['response_type'] == 'ephemeral'

    def test_invaid_create_command(self):
        game_service = GameService()
        channel_id = 'ch_1'
        o_user = 'me'
        command = 'start something'

        result = game_service.create_new_game(
            channel_id,
            command_text=command,
            o_player=o_user,
        )
        assert not game_service.ongoing_games.get(channel_id)
        assert result['text'] == instruction.get_invalid_command_text(START_COMMAND)
        assert result['response_type'] == 'ephemeral'

    def test_move(self):
        game_service = GameService()
        channel_id = 'ch_1'
        o_user = 'me'
        command = 'start @you'
        game_service.create_new_game(
            channel_id,
            command_text=command,
            o_player=o_user,
        )
        assert game_service.ongoing_games[channel_id]

        result = game_service.make_move(channel_id, 'you', 'move 1 1')
        assert result['text'] == (
            '|   |   |   |\n'
            '|--+--+--|\n'
            '|   | X |   |\n'
            '|--+--+--|\n'
            '|   |   |   |\n'
            '|--+--+--|\n'
            '<@me> \'s turn is next'
        )
        assert result['response_type'] == 'in_channel'

    def test_move_no_game(self):
        game_service = GameService()
        channel_id = 'ch_1'

        result = game_service.make_move(channel_id, 'you', 'move 1 1')
        assert result['text'] == instruction.get_no_games_text()
        assert result['response_type'] == 'ephemeral'

    def test_move_invalid_command(self):
        game_service = GameService()
        channel_id = 'ch_1'

        result = game_service.make_move(channel_id, 'you', 'move 1,1')
        assert result['text'] == instruction.get_invalid_command_text(MOVE_COMMAND)
        assert result['response_type'] == 'ephemeral'

    def test_move_invalid_move(self):
        game_service = GameService()
        channel_id = 'ch_1'
        o_user = 'me'
        command = 'start @you'
        game_service.create_new_game(
            channel_id,
            command_text=command,
            o_player=o_user,
        )

        result = game_service.make_move(channel_id, 'me', 'move 1 1')
        assert result['text'] == instruction.get_invalid_move_text('It is not your turn.')
        assert result['response_type'] == 'ephemeral'
