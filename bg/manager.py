#!/usr/bin/env python
#coding=utf-8

"""
    manager.py

    :license: BSD, see LICENSE for more details.
"""
import os
import sys
os.sys.path.append('E:\\Workstation\\Project')

from bg import create_app
from bg.extensions import db

def createall():
    "Creates database tables"
    db.create_all()

if __name__ == '__main__':
    app = create_app("test.cfg")
    #db.app = app
    #db.create_all()
    app.run()
