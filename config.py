#!/usr/local/bin/python3
# -*- conding: utf-8 -*-

import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


# 定义配置基类
class Config:
    # 秘钥
    SECRET_KEY = os.environ.get('SECRET_KEY') or '4329581751'

    # 数据库配置
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MYSQL_USER = 'root'
    MYSQL_PASS = ''
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{mysql_user}:{mysql_pass}@localhost/staffms'.format(
        mysql_user = MYSQL_USER, mysql_pass = MYSQL_PASS)

    # Redis配置
    REDIS_CONFIG = {
        'CACHE_TYPE': 'redis',
        'CACHE_REDIS_HOST': '127.0.0.1',
        'CACHE_REDIS_PORT': 6379,
        'CACHE_REDIS_DB': '',
        'CACHE_REDIS_PASSWORD': ''
    }

    # 发邮件配置
    MAIL_SERVER = 'smtp.animekid.cn'
    MAIL_USERNAME = ''
    MAIL_PASSWORD = ''

    # 额外的初始化操作
    @staticmethod
    def init_app(app):
        pass