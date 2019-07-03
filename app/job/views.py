#!/usr/local/bin/python3
# -*- conding: utf-8 -*-

from app.models.jobModels import Job
from app.models.staffModels import Staff
from app.utils import apiResponse, loginauth
from . import job_api
from ..utils import db

from flask import request


@job_api.route('gettitles', endpoint='api_gettitles')
@loginauth
def gettitles():
    """
    获取所有职能
    params: request
    return: response
    """
    data = [job[0] for job in Job.query.with_entities(Job.title).distinct().all()]
    return apiResponse(200, data=data)


@job_api.route('/getjobs', endpoint='api_getjobs')
@loginauth
def getjobs():
    """
    获取所有岗位名称
    params: request
    return: response
    """
    name = request.args.get('name') or ''
    title = request.args.get('title') or ''
    size = request.args.get('size') or 10
    page = request.args.get('page') or 1
    params = []
    if name:
        params.append(Job.name.like('%'+name+'%'))
    if title:
        params.append(Job.title == title)
    _query = Job.query.filter(*params).paginate(int(page), int(size), False)
    data = [u.to_dict() for u in _query.items]
    return apiResponse(200, data={'data': data, 'total': _query.total})


@job_api.route('addjob', methods=['POST'], endpoint='api_addjob')
@loginauth
def addjob():
    """
    添加岗位
    params: request
    return: response
    """
    name = request.get_json().get('name')
    title = request.get_json().get('title')
    level = request.get_json().get('level')
    sublevel = request.get_json().get('sublevel')
    if not name and not title and not level and not sublevel:
        return apiResponse(204)
    jobdata = Job(name, title, level, sublevel)
    db.session.add(jobdata)
    db.session.commit()
    return apiResponse(200)


@job_api.route('deljob', methods=['POST'], endpoint='api_deljob')
@loginauth
def deljob():
    """
    删除岗位
    params: request
    return: response
    """
    jobid = request.get_json().get('jobid')
    job = Job.query.get(jobid)
    if not job:
        return apiResponse(204, '岗位不存在')
    if job.to_dict()['staffcounts'] != 0:
        return apiResponse(204, '该岗位有绑定人员')
    db.session.delete(job)
    db.session.commit()
    return apiResponse(200)