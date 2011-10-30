#! /usr/bin/env python
#coding=utf-8
"""
    post.py
    ~~~~~~~~~~~~~
    :license: BSD, see LICENSE for more details.
"""

import datetime
import os

from flask import Module,render_template,redirect,url_for,flash,request,g,abort

from bg.extensions import db
from bg.forms import PostForm,CommentForm
from bg.models import User,Post,Comment,RelationPostComment
from bg.permissions import auth

post= Module(__name__)

@post.route("/", methods=("GET","POST"))
def newpost():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author_id=
                g.identity.id)
        db.session.add(post)
        db.session.commit()

        flash(("Posting success"), "success")

        return redirect(url_for('post.view', post_id=post.id))
    return render_template("newpost.html", form=form)

@post.route("/<int:post_id>/", methods=("GET","POST"))
@auth
def view(post_id):
    post = Post.query.get_or_404(post_id)
    post.comment_num = RelationPostComment.query.filter_by(post_id=post_id).count()
    post.author_name = User.query.get(post.author_id).username
    comments = RelationPostComment.query.list_comments(post_id)
    return render_template("post.html", post=post,form=CommentForm(), comments=comments)


@post.route("/<int:post_id>/edit/", methods=("GET","POST"))
@auth
def edit(post_id):
    post = Post.query.get_or_404(post_id)

    form = PostForm(title = post.title,
                    content = post.content)
                    #obj = post)

    if form.validate_on_submit():
        form.populate_obj(post)
        db.session.add(post)
        db.session.commit()
        flash(("Post has been changed"), "success")
        return redirect(url_for('post.view', post_id=post.id))

    return render_template("newpost.html", form=form)

@post.route("/<int:post_id>/delete/", methods=("GET","POST"))
def delete(post_id):
    post = Post.query.get_or_404(post_id)
    RelationPostComment.query.delete_comments(post_id)   #delete the comments of this post

    db.session.delete(post)
    db.session.commit()
    flash(("The post has been deleted"), "success")

    return redirect(url_for('frontend.index'))

@post.route("/<int:post_id>/addcomment", methods=("POST",))
def add_comment(post_id):
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(email=form.email.data, comment=form.comment.data)
        #comment = Comment(name=form.name.data, email=form.email.data, comment=form.comment.data)
        db.session.add(comment)
        db.session.commit()

        relationpostcomment = RelationPostComment(post_id=post_id, comment_id=comment.id)
        db.session.add(relationpostcomment)
        db.session.commit()
        flash(("Comment post success"), "success")
    else:
        flash(("Comment post fail"), "fail")

    return redirect(url_for('post.view',post_id=post_id))

@post.route("/<int:post_id>/deletecomment/<int:comment_id>/", methods=("POST","GET"))
def delete_comment(post_id, comment_id):
    rpc = RelationPostComment.query.get_or_404((post_id, comment_id))
    comment = Comment.query.get_or_404(comment_id)
    db.session.delete(rpc)
    db.session.delete(comment)
    db.session.commit()
    flash(("Comment delete successful"), "success")
    return redirect(url_for('post.view',post_id=post_id))


@post.route("/user/<int:user_id>/", methods=("GET","POST"))
def post_list(user_id):
    if g.identity.id == user_id:
        posts = Post.query.filter_by(author_id=user_id).all()
        for p in posts:
            p.author_name = User.query.get(user_id).username
            p.comment_num = RelationPostComment.query.filter_by(post_id=p.id).count()
        return render_template("userpage.html", posts=posts)
    else:
        return abort(401)
