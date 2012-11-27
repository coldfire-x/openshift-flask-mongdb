# -*- coding: utf8 -*-
import os
import hashlib

from flask import (Flask, render_template, request,
        session, escape, abort)
from flask.ext.mongoengine import MongoEngine

app = Flask(__name__)
app.debug = True

# set app secrete for session
app.secret_key = '=5NO>NO>a"Tj4=^#~Co^T#fD_b!-&J'

# mongodb configuration
app.config['MONGODB_DB'] = os.environ['OPENSHIFT_APP_NAME']
app.config['MONGODB_USERNAME'] = os.environ['OPENSHIFT_MONGODB_DB_USERNAME']
app.config['MONGODB_PASSWORD'] = os.environ['OPENSHIFT_MONGODB_DB_PASSWORD']
app.config['MONGODB_HOST'] = os.environ['OPENSHIFT_MONGODB_DB_HOST']
app.config['MONGODB_PORT'] = os.environ['OPENSHIFT_MONGODB_DB_PORT']

# get db connection
db = MongoEngine(app)

def register_blueprints(app):
    # Prevents circular imports
    from views import posts
    app.register_blueprint(posts)
register_blueprints(app)


@app.route("/admin", methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        username = escape(request.form['username'])
        password = escape(request.form['password'])
        
        pwmd5 = hashlib.md5(password).hexdigest()
        
        from models import Users
        is_valid = Users.check_user_passwd(username, pwmd5)

        if is_valid:
            session['uid'] = username
            return 'Bingo, You are in!'

        else:
            abort(403)
    else:
        if 'uid' in session:
            return 'Bingo, You have already in!'

        else:
            return render_template('login.html')


if __name__ == "__main__":
    app.run()
