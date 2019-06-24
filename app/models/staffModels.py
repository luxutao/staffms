#!/usr/local/bin/python3
# -*- conding: utf-8 -*-

from ..utils import db
from .jobModels import Job
from .companyModels import Company
from .departModels import Department


class Staff(db.Model):
    __tablename__ = 'staff'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255))
    email = db.Column(db.String(255))
    jointime = db.Column(db.DateTime, server_default=db.func.now())
    leavetime = db.Column(db.DateTime, default=None)
    is_leave = db.Column(db.Boolean, default=False)
    job = db.Column(db.Integer, db.ForeignKey('job.id'))
    salary = db.Column(db.Integer)
    company = db.Column(db.Integer, db.ForeignKey('company.id'))
    department = db.Column(db.Integer, db.ForeignKey('department.id'))
    leader = db.Column(db.Integer)
    create_time = db.Column(db.DateTime, server_default=db.func.now())
    modify_time = db.Column(db.DateTime, server_default=db.func.now())

    def __init__(self, name, email, jointime, job, salary, company, department, leader):
        self.name = name
        self.email = email
        self.jointime = jointime
        self.job = job
        self.salary = salary
        self.salary = salary
        self.company = company
        self.department = department
        self.leader = leader

    def __repr__(self):
        return '<Staff %s>' % self.name

    def to_dict(self):
        model_dict = dict(self.__dict__)
        del model_dict['_sa_instance_state']
        model_dict['job'] = Job.query.get(model_dict['job']).to_dict()
        model_dict['company'] = Company.query.get(model_dict['company']).to_dict()
        model_dict['department'] = Department.query.get(model_dict['department']).to_dict()
        for key in ['jointime', 'leavetime', 'create_time', 'modify_time']:
            if model_dict[key]:
                model_dict[key] = model_dict[key].strftime('%Y-%m-%d %H:%M:%S')
        model_dict['is_leave'] = '是' if model_dict['is_leave'] == 1 else '否'
        return model_dict
