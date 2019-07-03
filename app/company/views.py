#!/usr/local/bin/python3
# -*- conding: utf-8 -*-

from app.models.companyModels import Company
from app.models.staffModels import Staff
from app.utils import apiResponse, loginauth
from . import company_api
from ..utils import db

from flask import request


@company_api.route('/getcompanys', endpoint='api_getcompanys')
@loginauth
def getcompanys():
    """
    获取所有公司名称
    params: request
    return: response
    """
    name = request.args.get('name') or ''
    size = request.args.get('size') or 10
    page = request.args.get('page') or 1
    _query = Company.query.filter(Company.name.like('%'+name+'%')).paginate(int(page), int(size), False)
    data = [u.to_dict() for u in _query.items]
    return apiResponse(200, data={'data': data, 'total': _query.total})


@company_api.route('/addcompany', methods=['POST'], endpoint='api_addcompany')
@loginauth
def addcompany():
    """
    添加公司
    params: request
    return: response
    """
    name = request.get_json().get('name')
    is_default = request.get_json().get('is_default') or '0'
    if not name:
        return apiResponse(204)
    company = Company.query.filter_by(name=name).first()
    if company:
        return apiResponse(204, '公司已存在')
    if int(is_default) == 1:
        Company.query.update({'is_default': False})
    comdata = Company(name=name, is_default=(int(is_default) == 1))
    db.session.add(comdata)
    db.session.commit()
    return apiResponse(200)


@company_api.route('/changecompany', methods=['POST'], endpoint='api_changecompany')
@loginauth
def changecompany():
    """
    修改公司名称或者状态
    params: request
    return: response
    """
    comid = request.get_json().get('comid')
    name = request.get_json().get('name')
    is_default = request.get_json().get('is_default') or '0'
    if not comid:
        return apiResponse(204)
    company = Company.query.get(comid)
    ocom = Company.query.first()
    if not company:
        return apiResponse(204)
    if int(is_default) == 1:
        Company.query.update({'is_default': False})
    company.name = name
    company.is_default = int(is_default) == 1
    if ocom == company:
        company.is_default = True
    db.session.commit()
    return apiResponse(200)



@company_api.route('/delcompany', methods=['POST'], endpoint='api_delcompany')
@loginauth
def delcompany():
    """
    删除公司
    params: request
    return: response
    """
    comid = request.get_json().get('comid')
    if not comid:
        return apiResponse(204)
    company = Company.query.get(comid)
    if not company:
        return apiResponse(204, '公司不存在')
    db.session.delete(company)
    if company.is_default == 1:
        ocom = Company.query.first()
        ocom.is_default = True
        Staff.query.filter_by(job=comid).update({'job':ocom.id})
    db.session.commit()
    return apiResponse(200)
        