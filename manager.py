#coding:utf-8
from flask_script import Manager
from apps import create_app

app=create_app()
manager=Manager(app)

@manager.command
def dev():
    app.config['DEBUG']=True
    app.run()

if __name__ == '__main__':
    manager.run()