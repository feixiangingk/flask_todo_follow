# -*-coding:utf-8-*-
# author:       lenovo
# createtime:   2018/4/5 18:04
# software:     PyCharm


from flask import Flask
from main import main as main_blueprint
from ext import db
from common.todo_log import RecordLog
from flask_bootstrap import Bootstrap
from ext import loginManager

recordLog = RecordLog()
bootstrap = Bootstrap()


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile("settings.py")
    app.register_blueprint(main_blueprint)
    db.init_app(app)
    bootstrap.init_app(app)
    recordLog.init_app(app)
    loginManager.init_app(app)
    loginManager.login_view = 'main.login'  # 注意使用loginManager多了一步，指定视图函数
    return app


if __name__ == '__main__':
    app = create_app()
    app.run("0.0.0.0", port=5000, debug=False)
