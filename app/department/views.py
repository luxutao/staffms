#!/usr/local/bin/python3
# -*- conding: utf-8 -*-

from app.models.departModels import Department
from app.models.staffModels import Staff
from app.utils import apiResponse, loginauth
from . import department_api
from ..utils import db

from flask import request
from sqlalchemy import or_


@department_api.route('getleaders', endpoint='api_getleaders')
# @loginauth
def getleaders():
    """
    获取所有领导信息
    params: request
    return: response
    """
    size = request.args.get('size') or 10
    page = request.args.get('page') or 1
    data = Department.query.with_entities(Department.leader, Department.vp, Department.hrbp).distinct().all()
    staffids = set([])
    for staff in data:
        staffids.update(list(staff))
    staffs = Staff.query.filter(Staff.id.in_(list(staffids))).paginate(int(page), int(size), False)
    data = [{'id': staff.id, 'name': staff.name} for staff in staffs.items]
    return apiResponse(200, data=data)


@department_api.route('/getOrganization', endpoint='api_getOrganization')
# @loginauth
def getOrganization():
    """
    获取部门树型架构
    params: request
    return: response
    """
    departs = Department.query.filter(Department.level == 1).all()
    data = []
    for depart in departs:
        data.append({
            'id': depart.id,
            'label': depart.name,
            'children': getchildren(depart.id)
        })
    return apiResponse(200, data=data)


def getchildren(depid):
    """
    获取子部门
    params: depid int
    return: list
    """
    departs = Department.query.filter(Department.parent == depid).all()
    data = []
    for depart in departs:
        data.append({
            'id': depart.id,
            'label': depart.name,
            'children': getchildren(depart.id)
        })
    return data


@department_api.route('/getdeparts', endpoint='api_getdeparts')
# @loginauth
def getdeparts():
    """
    获取所有部门
    params: request
    return: response
    """
    name = request.args.get('name') or ''
    leader = request.args.get('leader') or ''
    size = request.args.get('size') or 10
    page = request.args.get('page') or 1
    params = []
    if name:
        departs = Department.query.filter(Department.name.like('%'+name+'%')).with_entities(Department.id).all()
        depids = [dep.id for dep in departs]
        params.append(or_(Department.name.like('%'+name+'%'), Department.parent.in_(depids)))
    if leader:
        params.append(or_(
            Department.leader == leader,
            Department.vp == leader,
            Department.hrbp == leader
        ))
    _query = Department.query.filter(*params).paginate(int(page), int(size), False)
    data = [u.to_dict() for u in _query.items]
    return apiResponse(200, data={'data': data, 'total': _query.total})


@department_api.route('/adddepart', methods=['POST'], endpoint='api_adddepart')
# @loginauth
def adddepart():
    """
    添加部门
    params: request
    return: response
    """
    name = request.get_json().get('name')
    parent = request.get_json().get('parent')
    leader = request.get_json().get('leader')
    vp = request.get_json().get('vp')
    hrbp = request.get_json().get('hrbp')
    level = request.get_json().get('level')
    if not name or not leader or not vp or not hrbp or not level:
        return apiResponse(204)
    depart = Department(name, parent, leader, vp, hrbp, level)
    db.session.add(depart)
    db.session.commit()
    return apiResponse(200)


@department_api.route('/deldepart', methods=['POST'], endpoint='api_deldepart')
# @loginauth
def deldepart():
    """
    删除部门
    params: request
    return: response
    """
    depid = request.get_json().get('depid')
    if not depid:
        return apiResponse(204)
    depart = Department.query.get(depid)
    if not depart:
        return apiResponse(204, '部门不存在')
    if depart.to_dict()['staffcounts'] > 0:
        return apiResponse(204, '该部门有绑定员工')
    db.session.delete(depart)
    db.session.commit()
    return apiResponse(200)