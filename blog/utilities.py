from flask import request, session, abort

def login_required(func):
    def wrappered_func(*args, **kwargs):
        if not 'uid' in session:
            abort(403)

        return func(*args, **kwargs)
    return wrappered_func
