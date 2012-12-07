# -*- coding: utf8 -*-
import hashlib
from datetime import datetime

import flask
from flask import (Blueprint, request, redirect, session,
    render_template, url_for, escape)
from flask.views import MethodView
from flask.ext.mongoengine.wtf import model_form

from blueprints.admin.models import Users
from utilities import login_required


admin = Blueprint('admin', __name__, template_folder='templates')


class AdminLogin(MethodView):
    def get(self):
        if not 'uid' in session:
            return render_template('login.html')
        
        else:
            return redirect(url_for('.console'))
            
    def post(self):
        username = escape(request.form['username'])
        password = escape(request.form['password'])
        passwd_md5 = hashlib.md5(password).hexdigest()
        
        is_valid = Users.check_user_passwd(username, passwd_md5)
        if is_valid:
            session['uid'] = username
            return redirect(url_for('.console'))

        else:
            error = 'Invalid credentials'

        return render_template('login.html', error=error)


@admin.route('/console')
@login_required
def console():
    return redirect(url_for('posts.index'))

admin.add_url_rule('/', view_func=AdminLogin.as_view('login'))
admin.add_url_rule('/login', view_func=AdminLogin.as_view('login'))
