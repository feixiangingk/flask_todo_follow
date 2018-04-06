#-*-coding:utf-8-*-
# author:       lenovo
# createtime:   2018/4/6 14:13
# software:     PyCharm
import logging

class RecordLog():
    def init_app(self,app):
        handler = logging.FileHandler(app.config['LOG_FILE'])
        app.logger.addHandler(handler)

