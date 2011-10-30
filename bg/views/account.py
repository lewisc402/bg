#! /usr/bin/env python
#coding=utf-8
"""
    account.py
    ~~~~~~~~~~~~~
    :license: BSD, see LICENSE for more details.
"""
import datetime
import os

from flask import Module,render_template,redirect,url_for,flash,request,current_app,g

from bg.extensions import db,identity_changed,Identity
from bg.forms import LoginForm,SignupForm
from bg.models import User

account = Module(__name__)

@account.route("/login/", methods=("GET","POST"))
def login():
    form = LoginForm(login=request.args.get('login',None),
                     next=request.args.get('next',None))

    if form.validate_on_submit():
        user, authenticated = User.query.authenticate(form.username.data,
                                                      form.password.data)

        if user and authenticated:
            identity_changed.send(current_app._get_current_object(),
                                  identity=(Identity(user.id, user.username)))
            flash(("Welcome, %(name)s come back" % {'name':user.username}), "success")
            #return redirect(url_for("frontend.index"))
            return redirect(url_for("post.post_list", user_id = g.identity.id))   #should return to last page
        else:
            flash(("Sorry, invalid login"), "error")

    return render_template("account/login.html", form=form)


@account.route("/signup/", methods=("GET","POST"))
def signup():
    form = SignupForm(next=request.args.get('next',None))

    if form.validate_on_submit():
        user = User()
        form.populate_obj(user)

        db.session.add(user)
        #db.session.delete(code)
        db.session.commit()

        identity_changed.send(current_app._get_current_object(),
                              identity=(Identity(user.id, user.username)))

        flash(("Welcome, %(name)s" % {'name':user.username}), "success")
        return redirect(url_for("post.post_list", user_id = g.identity.id))
    else:
        pass
        #flash(("Sorry, Signup error"), "error")

    return render_template("account/signup.html", form=form)

@account.route("/logout/")
def logout():
    flash(("You are now logged out"), "success")
    identity_changed.send(current_app._get_current_object(),
                          identity=Identity(0,'Login'))
    return redirect(url_for("frontend.index"))

