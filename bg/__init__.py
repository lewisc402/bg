#!/usr/bin/env python
#coding=utf-8

"""
    __init__.py

    :license: BSD, see LICENSE for more details.
"""

import os
import logging
import sys

from logging.handlers import SMTPHandler, RotatingFileHandler
from flask import Flask, g, session, request, flash, redirect, jsonify, url_for
from flaskext.babel import Babel

from bg import helpers
from bg.extensions import db, mail, cache, photos, identity_changed, Identity

from bg.views import frontend,admin,post,account
from bg.models import Post

DEFAULT_MODULES = (
    (frontend, ""),
    (post, "/post"),
    (account, "/account"),
    (admin, "/admin"),)

DEFAULT_APP_NAME = 'bg'

def create_app(config=None, modules=None):

    if modules is None:
        modules = DEFAULT_MODULES

    app = Flask(DEFAULT_APP_NAME)

    #config
    app.config.from_pyfile(config)
    configure_extensions(app)

    configure_logging(app)
    configure_errorhandlers(app)
    configure_before_handlers(app)
    configure_template_filters(app)
    configure_context_processors(app)
    configure_signals(app)
    babel = Babel(app)

    # register module
    configure_modules(app, modules)

    return app

def on_identity_changed(app, identity):
    g.identity = identity
    session['identity'] = identity

def configure_signals(app):
    identity_changed.connect(on_identity_changed, app)

def configure_errorhandlers(app):

    @app.errorhandler(401)
    def unauthorized(error):
        #if request.is_xhr:
        #    return jsonfiy(error=_("Login required"))
        flash(("Please login to see this page"), "error")
        #return redirect(url_for("account.login", next=request.path))
        return redirect(url_for("account.login"))


def configure_before_handlers(app):

    @app.before_request
    def authenticate():
        try:
            g.identity = session['identity']
        except Exception:
            g.identity = Identity(0,'Login')


def configure_extensions(app):
    # configure extensions
    db.init_app(app)
    #db.app = app
    #db.create_all()
    mail.init_app(app)
    cache.init_app(app)
    #setup_themes(app)

def configure_context_processors(app):
    @app.context_processor
    def archives():
        archives = set()
        for dt in Post.query.from_self(Post.create_date).order_by().filter_by(author_id=g.identity.id):
            item = (dt.create_date.year, dt.create_date.month)
            archives.add(item)
            if len(archives) > 5:
                break
        archives = sorted(list(archives))
        return dict(archives=archives)

def configure_modules(app, modules):

    for module, url_prefix in modules:
        app.register_module(module, url_prefix=url_prefix)

def configure_template_filters(app):

    @app.template_filter()
    def timesince(value):
        return helpers.timesince(value)

    @app.template_filter()
    def endtags(value):
        return helpers.endtags(value)

    @app.template_filter()
    def gravatar(email,size):
        return helpers.gravatar(email,size)

    @app.template_filter()
    def format_date(date,s='full'):
        return helpers.format_date(date,s)

    @app.template_filter()
    def format_datetime(time,s='full'):
        return helpers.format_datetime(time,s)

    @app.template_filter()
    def format_yearmonth(date):
        return '%s-%s'%date

def configure_logging(app):

    mail_handler = \
            SMTPHandler(app.config['MAIL_SERVER'],
                    app.config['DEFAULT_MAIL_SENDER'],
                    app.config['ADMINS'],
                    'application error',
                    (
                        app.config['MAIL_USERNAME'],
                        app.config['MAIL_PASSWORD'],
                        ))

    mail_handler.setLevel(logging.ERROR)
    app.logger.addHandler(mail_handler)

    formatter = logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s '
            '[in %(pathname)s:%(lineno)d]')

    debug_log = os.path.join(app.root_path,
            app.config['DEBUG_LOG'])

    debug_file_handler = \
            RotatingFileHandler(debug_log,
                    maxBytes=100000,
                    backupCount=10)

    debug_file_handler.setLevel(logging.DEBUG)
    debug_file_handler.setFormatter(formatter)
    app.logger.addHandler(debug_file_handler)

    error_log = os.path.join(app.root_path,
            app.config['ERROR_LOG'])

    error_file_handler = \
            RotatingFileHandler(error_log,
                    maxBytes=100000,
                    backupCount=10)

    error_file_handler.setLevel(logging.ERROR)
    error_file_handler.setFormatter(formatter)
    app.logger.addHandler(error_file_handler)

