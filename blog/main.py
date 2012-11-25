# -*- coding: utf8 -*-
import os

from flask import Flask, render_template
from flask.ext.mongoengine import MongoEngine

app = Flask(__name__)
app.debug = True

# mongodb configuration
app.config['MONGODB_DB'] = os.environ['OPENSHIFT_APP_NAME']
app.config['MONGODB_USERNAME'] = os.environ['OPENSHIFT_MONGODB_DB_USERNAME']
app.config['MONGODB_PASSWORD'] = os.environ['OPENSHIFT_MONGODB_DB_PASSWORD']
app.config['MONGODB_HOST'] = os.environ['OPENSHIFT_MONGODB_DB_HOST']
app.config['MONGODB_PORT'] = os.environ['OPENSHIFT_MONGODB_DB_PORT']

# get db connection
db = MongoEngine(app)


@app.route("/")
def hello():
    return "Hello World!"

@app.route("/admin", methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        do_the_login()

    else:
        return render_template('login.html')

if __name__ == "__main__":
    app.run()
