#! /usr/bin/env python
#coding=utf-8
"""
    frontend.py
    ~~~~~~~~~~~~~
    :license: BSD, see LICENSE for more details.
"""

import datetime
import os

from flask import Module,render_template,g

from bg.models import Post,User,RelationPostComment

frontend = Module(__name__)

@frontend.route("/")
@frontend.route("/archives/<int:year>/<int:month>/")
def index(year=None, month=None):
    if year:
        posts = Post.query.archive(year, month).filter_by(author_id=g.identity.id).all()
    else:
        posts = Post.query.all()

    for p in posts:
        p.author_name = User.query.get(p.author_id).username
        p.comment_num = RelationPostComment.query.filter_by(post_id=p.id).count()
    return render_template("index.html", posts=posts)

