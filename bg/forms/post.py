#!/usr/bin/env python
#coding=utf-8

"""
    post.py
    ~~~~~~~~~~~~~

    :license: BSD, see LICENSE for more details.
"""
from flaskext.wtf import Form, TextAreaField, SubmitField, TextField, PasswordField, \
            HiddenField, required, url, email, AnyOf

from flaskext.babel import gettext, lazy_gettext as _

class LoginForm(Form):
    username = TextField(("Username"), validators=[required("this field is required")])
    password = PasswordField(_("Password"))
    next = HiddenField()
    submit = SubmitField(_("Login"))

class SignupForm(Form):
    username = TextField(_("Username"), validators=[
                         required(message=_("Username required"))])
    password = PasswordField(_("Password"), validators=[
                             required(message=_("Password required"))])
    email = TextField(_("Email address"), validators=[
                      required(message=_("Email address required")),
                      email(message=_("A valid email address is required"))])
    code = TextField(_("Signup Code"), validators=[AnyOf('test', message='code is not valid')])
    next = HiddenField()
    submit = SubmitField(_("Signup"))

class PostForm(Form):
    title = TextField(("Title"), validators=[required("this field is required")])
    content = TextAreaField(("Contents"))
    submit = SubmitField(("Save"))

class CommentForm(Form):
    name = TextField(("Name"), validators=[required("this field is required")])
    email = TextField(("Email"), validators=[
                      required(message=("Email required")),
                      email(message=("A valid email address is required"))])
    comment = TextAreaField(("Comment"), validators=[
                      required(message=("Comment required"))])

    submit = SubmitField(("Submit"))

