# -*- coding: utf8 -*-
import hashlib

import flask
from flask import (Blueprint, request, redirect, session,
    render_template, url_for, escape)
from flask.views import MethodView

from models import Users
from utilities import login_required
     

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


class AdminConsole(MethodView):
    def get(self):
        return redirect(url_for('posts.list'))


admin = Blueprint('admin', __name__, template_folder='templates')
admin.add_url_rule('/admin/console', view_func=login_required(AdminConsole.as_view('console')))
admin.add_url_rule('/admin/login', view_func=AdminLogin.as_view('login'))
