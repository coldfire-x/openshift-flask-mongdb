# -*- coding: utf8 -*-
import hashlib

from flask import (Blueprint, request, redirect, session,
    render_template, url_for, escape)
from flask.views import MethodView

from models import Users
from utilities import login_required
     

class AdminLogin(MethodView):
    def get(self):
        if 'uid' in session:
            return redirect(url_for('.editor'))

        else:
            return render_template('login.html')
            

    def post(self):
        username = escape(request.form['username'])
        password = escape(request.form['password'])
        passwd_md5 = hashlib.md5(password).hexdigest()
        
        is_valid = Users.check_user_passwd(username, passwd_md5)
        if is_valid:
            session['uid'] = username
            return redirect(url_for('.editor'))

        else:
            error = 'Invalid credentials'

        return render_template('login.html', error=error)


class Admin(MethodView):
    def get(self):
        return render_template('editor.html')


admin = Blueprint('admin', __name__, template_folder='templates')
admin.add_url_rule('/admin', view_func=AdminLogin.as_view('login'))

admin.add_url_rule('/admin/editor', view_func=login_required(Admin.as_view('editor')))
