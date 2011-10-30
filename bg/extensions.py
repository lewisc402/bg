#!/usr/bin/env python
#coding=utf-8

from functools import wraps
from flask import g, Response, abort, request

from flaskext.mail import Mail
from flaskext.sqlalchemy import SQLAlchemy
from flaskext.cache import Cache
from flaskext.uploads import UploadSet, IMAGES


__all__ = ['mail', 'db', 'cache', 'photos']

mail = Mail()
db = SQLAlchemy()
cache = Cache()
photos = UploadSet('photos', IMAGES)

from flask.signals import Namespace
signals = Namespace()
identity_changed = signals.signal('identity-changed', doc='login signal')
http_excep = 401

class Identity(object):
    def __init__(self, id, name):
        self.id = id
        self.name = name

def check_user():
    import pdb
    pdb.set_trace

    if request.view_args.has_key('post_id'):
        post_id = request.view_args['post_id']
        user_id = User.query.get(post_id)
        if user_id != g.identity.id:
            return abort(http_excep)
    else:
        pass

def auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        check_user()
        #if g.identity.id <= 0:
        #    return abort(http_excep)
        return f(*args, **kwargs)
    return decorated


