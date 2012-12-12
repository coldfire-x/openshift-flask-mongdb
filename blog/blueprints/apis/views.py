# -*- coding: utf8 -*-

from flask import Blueprint, jsonify
from flask.views import MethodView
from werkzeug.contrib.cache import SimpleCache

from utilities import get_cnbeta_feed

apis = Blueprint('apis', __name__)

cache = SimpleCache()

class CnbetaFeedView(MethodView):
    def get(self):
        tips = cache.get('tips')

        if not tips:
            tips = get_cnbeta_feed()
            cache.set('tips', tips)

        return jsonify(tips=tips)

apis.add_url_rule('/cnbeta.json', view_func=CnbetaFeedView.as_view('callpoint'))
