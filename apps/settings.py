#-*-coding:utf-8-*-
# author:       lenovo
# createtime:   2018/4/5 19:17
# software:     PyCharm

import os
#全局配置
INSTANCE_PATH = os.path.abspath(os.path.dirname(__file__))

#log
LOG_PATH = os.path.join(INSTANCE_PATH, 'log')
LOG_FILE = os.path.join(LOG_PATH, 'mock.log')


#csrf
SECRET_KEY="dfdlkeeekj34234"

# database 配置
DATABASE_HOST = '127.0.0.1'
DATABASE_PORT = 3306

DATABASE_USER = 'root'
DATABASE_PWD = '123456'
DATABASE_NAME = 'test'
# sqlalchemy  数据库引擎
SQLALCHEMY_DATABASE_URI = 'mysql://' + DATABASE_USER + ':' + DATABASE_PWD + '@' + \
                          DATABASE_HOST + ':' + str(DATABASE_PORT) + '/' + DATABASE_NAME + '?charset=utf8'
SQLALCHEMY_ECHO = False
SQLALCHEMY_POOL_RECYCLE = 3600
SQLALCHEMY_TRACK_MODIFICATIONS = False

del os