from functools import wraps
from flask import session, redirect, url_for


def is_logged(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('login'))
        return func(*args, **kwargs)
    return decorator
