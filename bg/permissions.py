#!/usr/bin/env python
#coding=utf-8
"""
    permissions.py

    :license: BSD, see LICENSE for more details.
"""

from functools import wraps
from flask import g, Response, abort, request
from flask.signals import Namespace

from bg.models import Post

signals = Namespace()
identity_changed = signals.signal('identity-changed', doc='login signal')
http_excep = 401

class Identity(object):
    def __init__(self, id, name):
        self.id = id
        self.name = name

def check_user():
    if request.view_args.has_key('post_id'):
        post_id = request.view_args['post_id']
        user_id = Post.query.get(post_id).author_id
        if user_id != g.identity.id:
            g.isuser = False
            if request.method == 'POST':
                return abort(http_excep)
        else:
            g.isuser = True
    else:
        pass

def auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        check_user()
        return f(*args, **kwargs)
    return decorated



