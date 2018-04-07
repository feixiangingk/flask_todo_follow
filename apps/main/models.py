#-*-coding:utf-8-*-
# author:       lenovo
# createtime:   2018/4/7 1:03
# software:     PyCharm

from __future__ import unicode_literals
from apps.ext import db
import time
class TodoList(db.Model):
    __tablename__ = 'todolist'
    id=db.Column(db.Integer,primary_key=True)
    user_id=db.Column(db.Integer,nullable=False)
    title=db.Column(db.String(254),nullable=False)
    status=db.Column(db.String(10),nullable=False)
    create_time=db.Column(db.String(20),default=str(time.time()))

    def __repr__(self):
        return "TodoList {}".format(self.title)

