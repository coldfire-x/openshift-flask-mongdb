#!/usr/bin/python
import os
import sys

sys.path.append(os.path.join(os.environ['OPENSHIFT_REPO_DIR'], 'blog'))

virtenv = os.environ['APPDIR'] + '/virtenv/'
os.environ['PYTHON_EGG_CACHE'] = os.path.join(virtenv, 'lib/python2.6/site-packages')
virtualenv = os.path.join(virtenv, 'bin/activate_this.py')
try:
    execfile(virtualenv, dict(__file__=virtualenv))
except IOError:
    pass

from main import app
