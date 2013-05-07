# -*- coding: utf8 -*-

from flask import Blueprint, jsonify, request
from flask.views import MethodView
from werkzeug.contrib.cache import SimpleCache

from blueprints.posts.models import Post
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


class TagAutocomplete(MethodView):
    def get(self):
        term = request.args.get('term', None)
        items = Post.objects().only('tags')

        result = []
        for item in items:
            result.extend(item.tags)
        result = list(filter(lambda tag: term.lower() in tag.lower(),
            set(result)))

        return jsonify(items=result)


apis.add_url_rule('/cnbeta.json',
    view_func=CnbetaFeedView.as_view('cnbetacallpoint'))

apis.add_url_rule('/tagautocomplete.json',
    view_func=TagAutocomplete.as_view('tagautocomplete'))
