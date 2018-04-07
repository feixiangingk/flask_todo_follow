# -*-coding:utf-8-*-
# author:       lenovo
# createtime:   2018/4/5 18:32
# software:     PyCharm
from __future__ import unicode_literals
import sys

reload(sys)
sys.setdefaultencoding("utf-8")
from datetime import datetime
import pymysql
from . import main
from flask import render_template, g, url_for, redirect, request, session, flash
from forms import TodoListForm,LoginForm
from flask import current_app
from models import TodoList, db ,User
from flask_login import login_required,login_user,logout_user,current_user
from apps.ext import loginManager

@main.route('/', methods=['GET', 'POST'])
@login_required
def show_todo_list():
    todoListform = TodoListForm()
    if request.method == 'GET':
        todolists = TodoList.query.all()
        return render_template("index_follow.html", todo_list=todolists, form=todoListform, title=u"首页")

    elif request.method == 'POST':
        if todoListform.validate_on_submit():
            todolist = TodoList(user_id=current_user.id, title=todoListform.title.data, status=todoListform.status.data)
            db.session.add(todolist)
            db.session.commit()
            flash('记录新增成功！')
        else:
            flash(todoListform.errors)
        return redirect(url_for('main.show_todo_list'))


@main.route("/delete/<int:id>", methods=['GET'])
@login_required
def delete(id):
    """
    resful风格
    :param id:
    :return:
    """
    todolist = TodoList.query.filter_by(id=id).first_or_404()
    db.session.delete(todolist)
    db.session.commit()
    flash(u"任务删除成功！")
    return redirect(url_for('main.show_todo_list'))


@main.route('/modify/<int:id>', methods=['GET', 'POST'])
@login_required
def modify(id):
    if request.method == 'GET':
        todolist = TodoList.query.filter_by(id=id).first_or_404()
        form = TodoListForm()
        form.title.data = todolist.title
        form.status.data = todolist.status
        return render_template("modify_follow.html", form=form)
    elif request.method == 'POST':
        todoListForm = TodoListForm()
        if todoListForm.validate_on_submit():
            todolist = TodoList.query.filter_by(id=id).first_or_404()
            todolist.title = todoListForm.title.data
            todolist.status = todoListForm.status.data
            db.session.add(todolist)
            db.session.commit()
            flash('任务修改成功！')
        else:
            flash(todoListForm.errors)
        return redirect(url_for("main.show_todo_list"))


@main.route("/login", methods=['POST', 'GET'])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(name=request.form['name'],pwd=request.form['pwd']).first()
        if user:
            login_user(user)
            current_app.logger.info(u"用户 admin 在{} 登录成功！".format(datetime.now().strftime("%Y/%m/%d-%H:%M:%S")))
            flash(u"登录成功！")
            return redirect(url_for("main.show_todo_list", title=u"首页"))
        else:
            flash(u"用户名或密码错误！")
    return render_template("login_follow.html", title=u"登录页",form=form)


@main.route("/logout", methods=['GET'])
def logout():
    logout_user()
    flash(u"您已退出登录！")
    # return render_template('login_follow.html', title=u'登录页')
    return redirect(url_for("main.login"))

@loginManager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=int(user_id)).first()
