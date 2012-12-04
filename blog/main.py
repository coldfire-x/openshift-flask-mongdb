# -*- coding: utf8 -*-
import os

from flask import Flask
from flask.ext.mongoengine import MongoEngine

app = Flask(__name__)

debug = os.environ.get('FLASK_DEBUG', False)
app.debug = True if debug else False

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
    from blueprints.posts import posts
    from blueprints.admin import admin
    app.register_blueprint(posts)
    app.register_blueprint(admin)
register_blueprints(app)

if __name__ == "__main__":
    app.run()
