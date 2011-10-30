#!/usr/bin/env python
#coding=utf-8

from datetime import datetime
from bg.extensions import db

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Unicode(80), index=True)
    content = db.Column(db.UnicodeText)
    author_id = db.Column(db.Integer)
    create_date = db.Column(db.DateTime, default=datetime.utcnow)
    update_date = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        super(Post, self).__init__(*args, **kwargs)

    @classmethod
    def archive(self):
        '''return the archive list'''
        posts = Post.query.all()
        pass

class Comment(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(50))
	comment = db.Column(db.UnicodeText)
	create_date = db.Column(db.DateTime, default=datetime.utcnow)
	update_date = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

	def __init__(self, *args, **kwargs):
		super(Comment, self).__init__(*args, **kwargs)

class RelationPostComment(db.Model):
	post_id = db.Column(db.Integer, primary_key=True)
	comment_id = db.Column(db.Integer, primary_key=True)
