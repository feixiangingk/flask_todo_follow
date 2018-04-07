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
from flask import render_template, g, url_for, redirect, request, session, flash, abort
from forms import TodoListForm
from flask import current_app
from models import TodoList, db


def connect_db():
    return pymysql.connect(host='127.0.0.1',
                           user='root',
                           passwd='123456',
                           db='test',
                           charset='utf8')


@main.before_request
def bf_request():
    print(u"每次request前的操作")
    g.db = connect_db()


@main.after_request
def af_request(response):
    print(u"结束request前的处理")  # 注意要把response返回
    g.db.close()
    return response


@main.route('/', methods=['GET', 'POST'])
def show_todo_list():
    if not session.has_key('logged_in') or session['logged_in'] == False:
        return redirect(url_for('main.login', title=u'登录页'))

    todoListform = TodoListForm()
    if request.method == 'GET':
        todolists = TodoList.query.all()
        # with g.db as cur:
        #     sql="select * from todolist;"
        #     cur.execute(sql)
        #     todolists = [dict(id=row[0], user_id=row[1], title=row[2], status=row[3], create_time=row[4]) for row in
        #                  cur.fetchall()]
        return render_template("index_follow.html", todo_list=todolists, form=todoListform, title=u"首页")

    elif request.method == 'POST':
        if todoListform.validate_on_submit():
            todolist = TodoList(user_id=1, title=todoListform.title.data, status=todoListform.status.data)
            db.session.add(todolist)
            db.session.commit()

            # title=request.form['title']
            # status=request.form['status']
            # db.session.commit()
            # with g.db as cur:
            #     sql='''insert into todolist (`user_id`, `title`, `status`, `create_time`) VALUES''' \
            #         ''' ({user_id},"{title}","{status}",{create_time});'''.format(user_id=1,title=title,status=status,create_time=int(time.time()))
            #     cur.execute(sql)
            # current_app.logger.debug(sql)

            flash('记录新增成功！')
        else:
            flash(todoListform.errors)
        return redirect(url_for('main.show_todo_list'))


@main.route("/delete/<int:id>", methods=['GET'])
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
    if request.method == "POST":
        if str(request.form['user']) == "admin" and str(request.form['pwd']) == "admin":
            session['logged_in'] = True
            current_app.logger.info(u"用户 admin 在{} 登录成功！".format(datetime.now().strftime("%Y/%m/%d-%H:%M:%S")))
            flash(u"登录成功！")
            return redirect(url_for("main.show_todo_list", title=u"首页"))
        else:
            flash(u"用户名或密码错误！")
    return render_template("login_follow.html", title=u"登录页")


@main.route("/logout", methods=['GET'])
def logout():
    session['logged_in'] = False
    flash(u"您已退出登录！")
    return render_template('login_follow.html', title=u'登录页')
