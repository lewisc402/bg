#!/usr/bin/env python
#coding=utf-8

"""
    manager.py

    :license: BSD, see LICENSE for more details.
"""
#import os
#import sys
#os.sys.path.append('E:\\Workstation\\Project')

from flask import Flask, current_app
from flaskext.script import Server, Shell, Manager, Command, prompt_bool

from bg import create_app
from bg.extensions import db

manager = Manager(create_app('config.cfg'))
manager.add_command("runserver", Server('127.0.0.1',port=7070))

@manager.command
def createall():
    "Creates database tables"
    db.create_all()

@manager.command
def dropall():
    "Drops all database tables"

    if prompt_bool("Are you sure ? You will lose all your data !"):
        db.drop_all()

if __name__ == '__main__':
    #app = create_app("test.cfg")
    #db.app = app
    #db.create_all()
    manager.run()
