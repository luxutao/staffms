#!/usr/local/bin/python3
# -*- conding: utf-8 -*-

from app.models.staffInfoModels import StaffInfo
from app.models.staffModels import Staff
from app.models.departModels import Department
from app.models.companyModels import Company
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


@staff_api.route('/getChartdata', endpoint='api_getChartdata')
# @loginauth
def getChartdata():
    """
    获取图表数据
    params: request
    return: response
    """
    data = {'staff': {}}
    data['staff']['is_worker'] = Staff.query.filter(Staff.is_leave==True).count()
    data['staff']['not_worker'] = Staff.query.filter(Staff.is_leave==False).count()
    data['staff']['total_worker'] = data['staff']['is_worker'] + data['staff']['not_worker']
    data['department'] = [{'name': department.name, 'value': len(department.staff_of_department)} for department in Department.query.all()]
    data['company'] = [{'name': company.name, 'value': len(company.staff_of_company)} for company in Company.query.all()]
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
    sid = request.args.get('sid') or None
    name = request.args.get('name') or ''
    page = request.args.get('page') or 1
    size = request.args.get('size') or 10
    params = []
    if sid:
        params.append(Staff.id==sid)
    if name:
        params.append(Staff.name.like('%'+name+'%'))
    _query = Staff.query.filter(*params).paginate(int(page), int(size), False)
    data = [u.to_dict() for u in _query.items]
    return apiResponse(200, data={'data': data, 'total': _query.total})