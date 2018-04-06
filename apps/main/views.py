#-*-coding:utf-8-*-
# author:       lenovo
# createtime:   2018/4/5 18:32
# software:     PyCharm
import pymysql
from .import main
from flask import render_template,g,url_for,redirect,request,session,flash
from flask_sqlalchemy import SQLAlchemy
db=SQLAlchemy()

def connect_db():
    return pymysql.connect(host='127.0.0.1',
            user='root',
            passwd='123456',
            db='test',
            charset='utf8')

@main.before_request
def bf_request():
    print(u"每次request前的操作")
    g.db=connect_db()

@main.after_request
def af_request(response):
    print(u"结束request前的处理") #注意要把response返回
    g.db.close()
    return response



@main.route('/')
def show_todo_list():
    if not session['logged_in']:
        return redirect(url_for('main.login',title=u'登录页'))

    with g.db as cur:
        sql="select * from todolist;"
        cur.execute(sql)
        todo_list = [dict(id=row[0], user_id=row[1], title=row[2], status=bool(row[3]), create_time=row[4]) for row in
                     cur.fetchall()]
    return render_template("index_follow.html",todo_list=todo_list,title=u"首页")

@main.route("/login",methods=['POST','GET'])
def login():
    if request.method=="POST":
        if str(request.form['user'])=="admin" and str(request.form['pwd'])=="admin":
            session['logged_in']=True
            return redirect(url_for("main.show_todo_list",title=u"首页"))
        else:
            flash(u"用户名或密码错误")
    return render_template("login_follow.html",title=u"登录页")

@main.route("/logout",methods=['GET'])
def logout():
    session['logged_in']=False
    return render_template('login_follow.html',title=u'登录页')
