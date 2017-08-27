from __future__ import absolute_import
from __future__ import unicode_literals

import functools

from clay import config
from flask import abort, request


def authorize(f):
    @functools.wraps(f)
    def decorated_function(*args, **kws):
        # Do something with your request here
        token = request.form.get('token', None)
        if not token or token != config.get('auth_token'):
            abort(400)
        return f(*args, **kws)
    return decorated_function
