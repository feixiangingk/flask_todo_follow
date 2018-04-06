#-*-coding:utf-8-*-
# author:       lenovo
# createtime:   2018/4/5 18:32
# software:     PyCharm
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import time
from datetime import datetime
import pymysql
from .import main
from flask import render_template,g,url_for,redirect,request,session,flash,abort
from flask_sqlalchemy import SQLAlchemy
from flask import current_app
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



@main.route('/',methods=['GET','POST'])
def show_todo_list():
    if not session.has_key('logged_in') or session['logged_in']==False:
        return redirect(url_for('main.login',title=u'登录页'))
    if request.method=='GET':
        with g.db as cur:
            sql="select * from todolist;"
            cur.execute(sql)
            todo_list = [dict(id=row[0], user_id=row[1], title=row[2], status=row[3], create_time=row[4]) for row in
                         cur.fetchall()]
            return render_template("index_follow.html", todo_list=todo_list, title=u"首页")
    elif request.method=='POST':
        title=request.form['title']
        status=request.form['status']
        with g.db as cur:
            sql='''insert into todolist (`user_id`, `title`, `status`, `create_time`) VALUES''' \
                ''' ({user_id},"{title}","{status}",{create_time});'''.format(user_id=1,title=title,status=status,create_time=int(time.time()))
            cur.execute(sql)
            current_app.logger.debug(sql)
            flash(u'记录新增成功！')
            return redirect(url_for('main.show_todo_list'))

@main.route("/delete",methods=['GET'])
def delete():
    id=request.args.get("id",None)
    if id is None:
        abort(404)
    else:
        with g.db as cur:
            sql='''delete from todolist where id={};'''.format(id)
            cur.execute(sql)
            current_app.logger.debug(sql)
            flash(u"任务删除成功！")
            return redirect(url_for('main.show_todo_list'))

@main.route('/modify',methods=['GET'])
def modify():
    id=request.args.get('id',None)
    if id is None:
        abort(404)
    else:
        return redirect(url_for('main.show_todo_list'))



@main.route("/login",methods=['POST','GET'])
def login():
    if request.method=="POST":
        if str(request.form['user'])=="admin" and str(request.form['pwd'])=="admin":
            session['logged_in']=True
            current_app.logger.info(u"用户 admin 在{} 登录成功！".format(datetime.now().strftime("%Y/%m/%d-%H:%M:%S")))
            flash(u"登录成功！")
            return redirect(url_for("main.show_todo_list",title=u"首页"))
        else:
            flash(u"用户名或密码错误！")
    return render_template("login_follow.html",title=u"登录页")

@main.route("/logout",methods=['GET'])
def logout():
    session['logged_in']=False
    flash(u"您已退出登录！")
    return render_template('login_follow.html',title=u'登录页')
