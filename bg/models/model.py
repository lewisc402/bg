#!/usr/bin/env python
#coding=utf-8

from datetime import datetime
from flaskext.sqlalchemy import BaseQuery
from bg.extensions import db

class PostQuery(BaseQuery):
    def archive(self, year, month):
        if not year:
            return self

        criteria = []
        criteria.append(db.extract('year',Post.create_date)==year)
        #tmp = self.from_self(Post.created_date).all()
        if month: criteria.append(db.extract('month',Post.create_date)==month)
        #if day: criteria.append(db.extract('day',Post.created_date)==day)

        q = reduce(db.and_, criteria)
        return self.filter(q)

class Post(db.Model):
    query_class = PostQuery
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Unicode(80), index=True)
    content = db.Column(db.UnicodeText)
    author_id = db.Column(db.Integer)
    create_date = db.Column(db.DateTime, default=datetime.utcnow)
    update_date = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        super(Post, self).__init__(*args, **kwargs)

class Comment(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(50))
	comment = db.Column(db.UnicodeText)
	create_date = db.Column(db.DateTime, default=datetime.utcnow)
	update_date = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

	def __init__(self, *args, **kwargs):
		super(Comment, self).__init__(*args, **kwargs)

class RelationPostCommentQuery(BaseQuery):

	def __init__(self, *args, **kwargs):
		super(RelationPostCommentQuery, self).__init__(*args, **kwargs)

	def list_comments(self, post_id):
		'''return the comment list of the post'''
		rpcs = self.filter(RelationPostComment.post_id == post_id).all()
		return [Comment.query.get(r.comment_id) for r in rpcs]

	def delete_comments(self, post_id):
		'''delete all the comment of the post'''
		rpcs = self.filter(RelationPostComment.post_id == post_id).all()
        #Comment.query.filter_by(id in [c.comment_id for c in rpcs]).delete()

	def delete_one_comments(self, post_id):
		rpcs = self.filter(RelationPostComment.post_id == post_id).all()

class RelationPostComment(db.Model):
	query_class = RelationPostCommentQuery

	post_id = db.Column(db.Integer, primary_key=True)
	comment_id = db.Column(db.Integer, primary_key=True)

	def __init__(self, *args, **kwargs):
		super(RelationPostComment, self).__init__(*args, **kwargs)

class UserQuery(BaseQuery):
    def authenticate(self, login, password):

        user = self.filter(db.or_(User.username==login,
                                  User.email==login)).first()

        if user:
            authenticated = user.check_password(password)
        else:
            authenticated = False

        return user, authenticated


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    _password = db.Column("password", db.String(80), nullable=False)
    code = db.Column(db.String(20), nullable=False)
    date_joined = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime, default=datetime.utcnow)

    query_class = UserQuery
    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)

    def _get_password(self):
        return self._password

    def _set_password(self, password):
        self._password = password

    def check_password(self,password):
        if self.password is None:
            return False
        return self.password == password

    password = db.synonym("_password",
                          descriptor=property(_get_password,
                                              _set_password))


