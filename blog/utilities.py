import functools
import feedparser

from jinja2 import Markup
from flask import request, session, url_for, redirect


def login_required(func):
    @functools.wraps(func)
    def wrappered_func(*args, **kwargs):
        if not 'uid' in session:
            return redirect(url_for('admin.login'))
        return func(*args, **kwargs)
    return wrappered_func


def uniq_list(list_in, sep):
    new_list = [ele for ele in set(x.strip().lower() 
        for x in list_in.split(sep))]

    return new_list


def get_cnbeta_feed():
    d = feedparser.parse('http://www.cnbeta.com/backend.php')

    tips = []
    for entry in d.entries[:20]:
        tip = {}
        tip['title'] = entry.title
        tip['content'] = Markup(entry.summary).striptags()
        tip['link'] = entry.link
        tips.append(tip)

    return tips
