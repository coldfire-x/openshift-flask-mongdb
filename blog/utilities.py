import functools

from flask import request, session, url_for, redirect

def login_required(func):
    @functools.wraps(func)
    def wrappered_func(*args, **kwargs):
        if not 'uid' in session:
            return redirect(url_for('admin.login'))
        return func(*args, **kwargs)
    return wrappered_func
