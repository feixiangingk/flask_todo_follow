#-*-coding:utf-8-*-
# author:       lenovo
# createtime:   2018/4/7 1:03
# software:     PyCharm

from __future__ import unicode_literals
from apps.ext import db
from flask_login import UserMixin
import time
class TodoList(db.Model):
    __tablename__ = 'todolist'
    id=db.Column(db.Integer,primary_key=True)
    user_id=db.Column(db.Integer,nullable=False)
    title=db.Column(db.String(254),nullable=False)
    status=db.Column(db.String(10),nullable=False)
    create_time=db.Column(db.Integer,default=int(time.time()))

    def __repr__(self):
        return "TodoList {}".format(self.title)

class User(db.Model,UserMixin):
    __tablename__='user'
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(30),nullable=False)
    pwd=db.Column(db.String(30),nullable=False)

    def __repr__(self):
        return "User {}".format(self.name)

