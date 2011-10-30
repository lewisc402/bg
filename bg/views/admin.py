#!/usr/bin/env python
#coding=utf-8

"""
    admin.py

    :license: BSD, see LICENSE for more details.
"""

import os

from flask import Module,render_template,redirect,url_for,flash
from flaskext.sqlalchemy import SQLAlchemy
from bg.extensions import db

from bg.forms import PostForm
from bg.models import Post

admin = Module(__name__)

@admin.route('/', methods=["GET","POST"])
def index():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author_id="Lewis")
        db.session.add(post)
        db.session.commit()
        flash(("Posting success"), "success")
        return redirect(url_for('frontend.index'))

    return render_template("admin.html", form=form)

if __name__ == '__main__':
    app.run()

