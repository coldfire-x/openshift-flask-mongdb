# -*- coding: utf8 -*-
import os

from flask import Flask, url_for, redirect
from flask.ext.mongoengine import MongoEngine

import utilities

# NOTE : tricky here, import self otherwise there will be
#        import cycle issue
import main

app = Flask(__name__)
app.config.from_object('settings')

# get db connection
db = MongoEngine(app)

from blueprints.admin.views import admin
from blueprints.posts.views import posts
from blueprints.apis.views import apis
app.register_blueprint(admin, url_prefix='/admin')
app.register_blueprint(posts)
app.register_blueprint(apis, url_prefix='/apis')


if __name__ == "__main__":
    app.run()
