#!/usr/local/bin/python3
# -*- conding: utf-8 -*-

import time

from app.models.authModels import Auth
from app.utils import apiResponse, encrypt, loginauth
from . import auth_api
from ..utils import db, cache

from datetime import datetime
from flask import request, make_response


@auth_api.route('/login', methods=['POST'], endpoint='api_login')
def login():
    """
    登录账号
    params: request
    return: response
    """
    username = request.get_json().get('username')
    password = request.get_json().get('password')
    if not username or not password:
        return apiResponse(204)
    auth = Auth.query.filter_by(username=username).first()
    if auth is None:
        return apiResponse(403)
    if encrypt(password) == auth.password:
        token = encrypt(str(auth.id) + str(int(time.time()*1000)))
        logintoken = cache.get(token)
        if logintoken is None:
            cache.set(token, auth.id, 24*60*60)
        res = make_response(apiResponse(200, data=token))
        res.set_cookie('token', token, 24*60*60)
        auth.last_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        auth.last_ip = request.remote_addr
        db.session.commit()
        return res
    else:
        return apiResponse(403)


@auth_api.route('/getusers', endpoint='api_getauthusers')
# @loginauth
def getusers():
    """
    获取登录账号
    params: request
    return: response
    """
    size = request.args.get('size') or 10
    page = request.args.get('page') or 1
    username = request.args.get('username') or ''
    _query = Auth.query.filter(Auth.username.like('%'+username+'%')).paginate(int(page), int(size), False)
    data = [u.to_dict() for u in _query.items]
    return apiResponse(200, data={'data': data, 'total': _query.total})


@auth_api.route('/adduser', methods=['POST'], endpoint='api_adduser')
# @loginauth
def adduser():
    """
    注册账号
    params: request
    return: response
    """
    username = request.get_json().get('username')
    password = request.get_json().get('password')
    is_active = request.get_json().get('is_active') or 0
    if not username or not password:
        return apiResponse(204)
    auth = Auth.query.filter_by(username=username).first()
    if auth:
        return apiResponse(204, '用户已存在!')
    encrypt_password = encrypt(password)
    userdata = Auth(username=username, password=encrypt_password, is_active=(int(is_active) == 1))
    db.session.add(userdata)
    db.session.commit()
    return apiResponse(200)


@auth_api.route('/deluser', methods=['POST'], endpoint='api_deluser')
# @loginauth
def deluser():
    """
    删除账号
    params: request
    return: response
    """
    authid = request.get_json().get('authid')
    if not authid:
        return apiResponse(204)
    auth = Auth.query.filter_by(id=authid).first()
    if not auth:
        return apiResponse(204, '用户不存在!')
    db.session.delete(auth)
    db.session.commit()
    return apiResponse(200)


@auth_api.route('/resetpassword', methods=['POST'], endpoint='api_resetpassword')
# @loginauth
def resetpassword():
    """
    重置密码
    params: request
    return: response
    """
    authid = request.get_json().get('authid')
    newpassword = request.get_json().get('newpassword')
    if not authid or not newpassword:
        return apiResponse(204)
    auth = Auth.query.filter_by(id=authid).first()
    if auth is None:
        return apiResponse(405, '账号不存在!')
    encrypt_newpassword = encrypt(newpassword)
    auth.password = encrypt_newpassword
    db.session.commit()
    return apiResponse(200)