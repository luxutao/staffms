#!/usr/local/bin/python3
# -*- conding: utf-8 -*-

import datetime

from app.models.staffInfoModels import StaffInfo
from app.models.staffModels import Staff
from app.models.departModels import Department
from app.models.companyModels import Company
from app.models.jobModels import Job
from app.models.logModels import Log
from app.utils import apiResponse, loginauth
from . import staff_api
from ..utils import db, templates, cache

from flask import request
from sqlalchemy import func


@staff_api.route('/getRegisdata', endpoint='api_getRegisdata')
@loginauth
def getRegisdata():
    """
    获取所有职位部门等简单的信息
    params: request
    return: response
    """
    v = request.args.get('v') or ''
    jobs = [{'id': job.id, 'name': job.name} for job in Job.query.all()]
    companys = [{'id': company.id, 'name': company.name} for company in Company.query.all()]
    staffs = [{'id': staff.id, 'name': staff.name} for staff in Staff.query.all()]
    departs = [{'id': depart.id, 'name': depart.name} for depart in Department.query.all()]
    data = {'jobs': jobs, 'companys': companys, 'staffs': staffs, 'departs': departs}
    if v in ['jobs', 'companys', 'staffs', 'departs']:
        data = {v: data[v]}
    return apiResponse(200, data=data)


@staff_api.route('/getStaffinfo', endpoint='api_getstaffinfo')
@loginauth
def getStaffinfo():
    """
    获取员工信息
    params: request
    return: response
    """
    sid = request.args.get('id') or ''
    if not sid:
        return apiResponse(204)
    staffinfo = StaffInfo.query.get(sid)
    if not staffinfo:
        return apiResponse(204)
    return apiResponse(200, data=staffinfo.to_dict())


@staff_api.route('/getcard', endpoint='api_getcard')
@loginauth
def getcard():
    """
    获取首页card数据
    params: request
    return: response
    """
    untreated = StaffInfo.query.filter(StaffInfo.finished==0).count()
    stafftotal = Staff.query.count()
    lastmonth = (datetime.date.today() + datetime.timedelta(days = -1)).strftime("%Y-%m-%d %H:%M:%S")
    leavetotal = Staff.query.filter(Staff.leavetime.between(datetime.datetime.now()\
        .strftime("%Y-%m-%d %H:%M:%S"), lastmonth)).count()
    warning = StaffInfo.query.group_by(StaffInfo.name).having(func.count(StaffInfo.id)>=2).count()
    is_worker = Staff.query.filter(Staff.is_leave == 0).count()
    not_worker = Staff.query.filter(Staff.is_leave == 1).count()
    data = {
        'untreated': untreated,
        'stafftotal': stafftotal,
        'leavetotal': leavetotal,
        'warning': warning,
        'is_worker': is_worker,
        'not_worker': not_worker,
    }
    return apiResponse(200, data=data)


@staff_api.route('/getnews', endpoint='api_getnews')
@loginauth
def getnews():
    """
    获取填写员工入职表的员工
    params: request
    return: response
    """
    data = [{
        'id':info.id,
        'name':info.name,
        'phone': info.phone,
        'create_time': info.create_time.strftime('%Y-%m-%d %H:%M:%S')
        } for info in StaffInfo.query.filter(StaffInfo.finished == 0).all()]
    return apiResponse(200, data=data)


@staff_api.route('/getEasystaffs', endpoint='api_getEasystaffs')
@loginauth
def getEasystaffs():
    """
    获取所有人员的简单信息
    params: request
    return: response
    """
    data = [{'id':staff.id,'name':staff.name} for staff in Staff.query.all()]
    return apiResponse(200, data=data)


@staff_api.route('/getChartdata', endpoint='api_getChartdata')
@loginauth
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


@staff_api.route('/staffhrRegistration', methods=['POST'], endpoint='api_staffhrRegistration')
@loginauth
def staffhrRegistration():
    """
    HR填写的部分信息
    params: request
    return: response
    """
    data = request.get_json()
    staffdata = Staff(**data)
    StaffInfo.query.filter(StaffInfo.id==data.get('staffinfo')).update({'finished': True})
    db.session.add(staffdata)
    db.session.commit()
    return apiResponse(200)


@staff_api.route('/getStaffs', endpoint='api_getStaffs')
@loginauth
def getStaffs():
    """
    获取所有员工
    params: request
    return: response
    """
    sid = request.args.get('id') or None
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


@staff_api.route('/changeStaff', methods=['POST'], endpoint='api_changeStaff')
@loginauth
def changeStaff():
    """
    更改员工信息
    params: request
    return: response
    """
    uid = request.get_json().get('id')
    column = request.get_json().get('column')
    value = request.get_json().get('value')
    if uid == None or column == None or value == None:
        return apiResponse(204)
    staff = Staff.query.filter(Staff.id==uid)
    if staff.count() == 0:
        return apiResponse(204)
    if column == 'is_leave':
        value = True if value == 1 else False
    staff.update({column: value})
    # message = templates[column].format(source=getattr(staff.first(), column), now=value)
    # logdata = Log(uid, message, cache.get(request.cookies.get('token')))
    # db.session.add(logdata)
    db.session.commit()
    return apiResponse(200)
    

