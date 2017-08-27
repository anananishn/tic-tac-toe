from __future__ import absolute_import
from __future__ import unicode_literals


class AuthorizationException(Exception):
    """Authorization exception."""

    def __init__(self):
        super(AuthorizationException, self).__init__()
        self.error = 'Unknown token'


class InvalidCommandUseException(Exception):
    """Invalid command use exception."""

class IllegalMoveException(Exception):
    """Illegal game move exception."""
    def __init__(self, message):
        super(IllegalMoveException, self).__init__(message)
        self.error = message
