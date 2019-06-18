#!/usr/local/bin/python3
# -*- conding: utf-8 -*-

import json
import logging

from config import Config
from .utils import db, cache
from app.auth import auth_api

from flask import Flask


# 将创建app的动作封装成一个函数
def create_app():
    # 创建app实例对象
    app = Flask(__name__)
    # 加载配置
    app.config.from_object(Config)
    # 执行额外的初始化
    Config.init_app(app)
    db.init_app(app)
    cache.init_app(app)
    # 添加日志
    # app.logger = logging.getLogger(__name__)
    # app.logger.setLevel(level=logging.INFO)
    # handler = logging.FileHandler("/var/log/uwsgi/flaskapi_info.log")
    # handler.setLevel(logging.INFO)
    # formatter = logging.Formatter(
    #     '%(asctime)s - %(name)s - %(process)d - %(thread)d - %(filename)s - %(levelname)s - %(message)s')
    # handler.setFormatter(formatter)
    # # if not app.logger.handlers:
    # app.logger.addHandler(handler)
    # 定制错误
    @app.errorhandler(404)
    def page_not_found(error):
        return json.dumps({'code': 404, 'msg': "404 Not Found"}), 404

    app.register_blueprint(auth_api)
    return app