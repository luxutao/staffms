#!/usr/local/bin/python3
# -*- conding: utf-8 -*-

import base64
import hashlib

from config import Config

import smtplib
from email.utils import parseaddr, formataddr
from email.header import Header
from email.mime.text import MIMEText
from flask import request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cache import Cache

db = SQLAlchemy()
cache = Cache(config=Config.REDIS_CONFIG)

templates = {
    'phone': '字段：{column}-日志类型：手机号-原值：{source}-现值：{now}',
    'job': '字段：{column}-日志类型：职位-原值：{source}-现值：{now}',
    'company': '字段：{column}-日志类型：公司-原值：{source}-现值：{now}',
    'department': '字段：{column}-日志类型：部门-原值：{source}-现值：{now}',
    'salary': '字段：{column}-日志类型：薪资-原值：{source}-现值：{now}',
    'is_leave': '字段：{column}-日志类型：是否离职-原值：否-现值：是',
}


def apiResponse(code, msg="", data=""):
    """
    封装返回结果
    params: int code
    params: str msg
    params: dict data
    return: json
    """
    if code == 200 and not msg:
        msg = "请求成功"
    if code == 204 and not msg:
        msg = "未知参数"
    if code == 403 and not msg:
        msg = "验证失败"
    return jsonify({'code': code, 'msg': msg, 'data': data})


def format_addr(s):
    """
    格式化发送邮件地址
    params: str s
    return: str
    """
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))


def encrypt(u_password):
    """
    加密密码
    params: str u_password
    return: str
    """
    md5 = hashlib.md5()
    md5.update(u_password.encode("utf-8"))
    u_password = md5.hexdigest()
    return u_password


def authticket(func):
    """
    普通验证路径加密
    params: func func
    return: 
    """
    def wrapper(*args, **kwargs):
        request_path = request.base_url.split('/')[-1]
        ticket = request.args.get('ticket') or None
        enstr = 'LRnS4t'
        if ticket:
            ticket = ticket + len(ticket) % 4 * '='
            destrlist = base64.b64decode(ticket.encode()).decode().split('-')
            if destrlist[0] == request_path and len(destrlist[1]) == 10 and destrlist[2] == enstr:
                return func()
        return apiResponse(403, '验证失败')
    return wrapper


def loginauth(func):
    """
    登陆验证接口加密
    params: func func
    return: 
    """
    def wrapper(*args, **kwargs):
        token = request.cookies.get('token')  or None
        if  token:
            info = cache.get(token)
            if info:
                return func()
        return apiResponse(403, '验证失败')
    return wrapper


def makemail(context, to_addr, subject):
    """
    发送邮件
    params: str context
    params: email to_addr
    params: subject
    return: bool
    """
    from_addr = Config.MAIL_USERNAME
    from_pass = Config.MAIL_PASSWORD
    smtp_server = Config.MAIL_SERVER
    content = MIMEText(context, 'html', 'utf-8')
    content['From'] = format_addr('Animekid <%s>' % from_addr)
    content['To'] = format_addr('{to_addr} <{to_addr}>'.format(to_addr=to_addr))
    content['Subject'] = Header(subject, 'utf-8').encode()
    server = smtplib.SMTP_SSL(smtp_server, 465)
    server.login(from_addr, from_pass)
    if server.noop()[0] == 250:
        server.sendmail(from_addr, [to_addr], content.as_string())
        server.close()
        return True
    server.close()
    return False