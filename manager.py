#coding:utf-8
from flask_script import Manager
from apps import create_app,db
from flask_migrate import MigrateCommand,Migrate

migrate=Migrate()
app=create_app()
migrate.init_app(app,db)
manager=Manager(app)
manager.add_command("db",MigrateCommand)

@manager.command
def dev():
    app.config['DEBUG']=True
    app.run()

if __name__ == '__main__':
    manager.run()