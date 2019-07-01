#!/usr/local/bin/python3
# -*- conding: utf-8 -*-

from app.models.staffInfoModels import StaffInfo
from app.models.staffModels import Staff
from app.utils import apiResponse, loginauth
from . import staff_api
from ..utils import db

from flask import request


@staff_api.route('/getEasystaffs', endpoint='api_getEasystaffs')
# @loginauth
def getEasystaffs():
    """
    获取所有人员的简单信息
    params: request
    return: response
    """
    data = [{'id':staff.id,'name':staff.name} for staff in Staff.query.all()]
    return apiResponse(200, data=data)


@staff_api.route('/staffRegistration', methods=['POST'], endpoint='api_staffRegistration')
def staffRegistration():
    """
    员工自己填写的部分信息
    params: request
    return: response
    """
    password = request.get_json().get('password')
    if password != 'saddtaff':
        return apiResponse(403, '验证失败')
    data = request.get_json()
    data['gender'] = True if data.get('gender') == '1' else False
    data['marriage'] = True if data.get('marriage') == '1' else False
    staffinfo = StaffInfo(**request.get_json())
    db.session.add(staffinfo)
    db.session.commit()
    return apiResponse(200)


@staff_api.route('/getStaffs', endpoint='api_getStaffs')
def getStaffs():
    """
    获取所有员工
    params: request
    return: response
    """
    name = request.args.get('name') or ''
    page = request.args.get('page') or 1
    size = request.args.get('size') or 10
    _query = Staff.query.filter(Staff.name.like('%'+name+'%')).paginate(int(page), int(size), False)
    data = [u.to_dict() for u in _query.items]
    return apiResponse(200, data={'data': data, 'total': _query.total})