from __future__ import absolute_import
from __future__ import unicode_literals

import pytest

from entities.board import Board
from entities.board import IllegalMoveException


class TestBoard(object):

    def test_board_creation(self):
        new_board = Board('x', 'o')
        expected_string = (
            '|   |   |   |\n'
            '|--+--+--|\n'
            '|   |   |   |\n'
            '|--+--+--|\n'
            '|   |   |   |\n'
            '|--+--+--|\n'
            '<@x> \'s turn is next'
        )
        assert new_board.turn == new_board.x_player
        assert new_board.to_string() == expected_string

    def test_move_wrong_turn(self):
        new_board = Board('x', 'o')
        with pytest.raises(IllegalMoveException) as e:
            new_board.move(0, 1, 'o')
        assert e.value.error == 'It is not your turn.'

    def test_move(self):
        new_board = Board('x', 'o')
        result = new_board.move(0, 1, 'x')
        assert new_board.turn == new_board.o_player
        assert not result
        result = new_board.move(0, 2, 'o')
        assert new_board.turn == new_board.x_player
        assert not result

        expected_string = (
            '|   | X | O |\n'
            '|--+--+--|\n'
            '|   |   |   |\n'
            '|--+--+--|\n'
            '|   |   |   |\n'
            '|--+--+--|\n'
            '<@x> \'s turn is next'
        )
        assert new_board.turn == new_board.x_player
        assert new_board.to_string() == expected_string

    def test_x_win(self):
        new_board = Board('x', 'o')
        result = new_board.move(0, 1, 'x')
        assert not result
        result = new_board.move(0, 2, 'o')
        assert not result
        result = new_board.move(1, 1, 'x')
        assert not result
        result = new_board.move(2, 2, 'o')
        assert not result
        result = new_board.move(2, 1, 'x')
        assert not result
        has_winner, winner = new_board.is_complete()

        assert has_winner is True
        assert not new_board.turn
        assert winner == 'x'

    def test_o_win(self):
        new_board = Board('x', 'o')
        new_board.move(0, 1, 'x')
        new_board.move(0, 2, 'o')
        new_board.move(2, 1, 'x')
        new_board.move(1, 2, 'o')
        new_board.move(0, 0, 'x')
        new_board.move(2, 2, 'o')
        has_winner, winner = new_board.is_complete()

        assert has_winner is True
        assert not new_board.turn
        assert winner == 'o'

    def test_not_complete(self):
        new_board = Board('x', 'o')
        new_board.move(0, 1, 'x')
        new_board.move(0, 2, 'o')

        has_winner, winner = new_board.is_complete()

        assert has_winner is False
        assert new_board.turn
        assert winner == ''

    def test_tie_game(self):
        new_board = Board('x', 'o')
        new_board.move(0, 0, 'x')
        new_board.move(0, 2, 'o')
        new_board.move(0, 1, 'x')

        new_board.move(1, 0, 'o')
        new_board.move(1, 1, 'x')
        new_board.move(2, 1, 'o')

        new_board.move(1, 2, 'x')
        new_board.move(2, 2, 'o')
        new_board.move(2, 0, 'x')
        is_complete, winner = new_board.is_complete()

        assert is_complete is True
        assert not new_board.turn
        assert winner == ''

    def test_move_invalid_coordinate(self):
        new_board = Board('x', 'o')

        with pytest.raises(IllegalMoveException) as e:
            new_board.move(0, 10, 'x')
        assert e.value.error == 'Invalid coordinates.'

    def test_move_already_taken(self):
        new_board = Board('x', 'o')
        result = new_board.move(0, 0, 'x')
        assert not result
        with pytest.raises(IllegalMoveException) as e:
            new_board.move(0, 0, 'o')
        assert e.value.error == 'This cell is already taken.'
