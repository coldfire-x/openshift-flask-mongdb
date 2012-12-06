import os

# debug
DEBUG = os.environ.get('FLASK_DEBUG', False)

# mongodb configuration
MONGODB_DB = os.environ['OPENSHIFT_APP_NAME']
MONGODB_USERNAME = os.environ['OPENSHIFT_MONGODB_DB_USERNAME']
MONGODB_PASSWORD = os.environ['OPENSHIFT_MONGODB_DB_PASSWORD']
MONGODB_HOST = os.environ['OPENSHIFT_MONGODB_DB_HOST']
MONGODB_PORT = os.environ['OPENSHIFT_MONGODB_DB_PORT']

# secret keys
SECRET_KEY = '=5NO>NO>a"Tj4=^#~Co^T#fD_b!-&J'
