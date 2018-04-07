#-*-coding:utf-8-*-
# author:       lenovo
# createtime:   2018/4/6 22:38
# software:     PyCharm
from __future__ import unicode_literals
from flask_wtf import FlaskForm
from wtforms import RadioField,StringField,SubmitField,PasswordField
from wtforms.validators import Length,DataRequired

class TodoListForm(FlaskForm):
    title=StringField(label=u"标题",validators=[DataRequired()])
    status=RadioField(label=u"是否完成",choices=[("yes", '是'),("no",'否')])
    submit=SubmitField("submit")

class LoginForm(FlaskForm):
    name=StringField(label="用户名",validators=[DataRequired()])
    pwd=PasswordField(label="密码",validators=[DataRequired()])
    submit=SubmitField("登录")