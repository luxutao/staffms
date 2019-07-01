#!/usr/local/bin/python3
# -*- conding: utf-8 -*-

from ..utils import db
from .jobModels import Job
from .companyModels import Company
from .departModels import Department
from .staffInfoModels import StaffInfo

from sqlalchemy.orm import  relationship


class Staff(db.Model):
    __tablename__ = 'staff'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255))
    email = db.Column(db.String(255))
    number = db.Column(db.String(24))
    jointime = db.Column(db.DateTime, server_default=db.func.now())
    leavetime = db.Column(db.DateTime, default=None)
    is_leave = db.Column(db.Boolean, default=False)
    job = db.Column(db.Integer, db.ForeignKey('job.id'))
    job_to = relationship("Job",backref="staff_of_job") 
    salary = db.Column(db.Integer)
    equity = db.Column(db.Integer)
    salary_structure = db.Column(db.Integer, default=12)
    company = db.Column(db.Integer, db.ForeignKey('company.id'))
    company_to = relationship("Company", backref="staff_of_company")
    department = db.Column(db.Integer, db.ForeignKey('department.id'))
    department_to = relationship("Department", backref="staff_of_department")
    staffinfo = db.Column(db.Integer, db.ForeignKey('staffinfo.id'))
    staffinfo_to = relationship("StaffInfo", backref="staff_of_staffinfo")
    leader = db.Column(db.Integer)
    create_time = db.Column(db.DateTime, server_default=db.func.now())
    modify_time = db.Column(db.DateTime, server_default=db.func.now())

    def __init__(self, name, email, number, jointime, job, salary, company, department, leader, equity=0, salary_structure=12):
        self.name = name
        self.email = email
        self.number = number
        self.jointime = jointime
        self.job = job
        self.salary = salary
        self.equity = equity
        self.salary_structure = salary_structure
        self.company = company
        self.department = department
        self.leader = leader

    def __repr__(self):
        return '<Staff %s>' % self.name

    def to_dict(self):
        model_dict = dict(self.__dict__)
        del model_dict['_sa_instance_state']
        model_dict['job'] = self.job_to.to_dict()
        model_dict['company'] = self.company_to.to_dict()
        model_dict['department'] = self.department_to.to_dict()
        model_dict['staffinfo'] = self.staffinfo_to.to_dict()
        for key in ['jointime', 'leavetime', 'create_time', 'modify_time']:
            if model_dict[key]:
                model_dict[key] = model_dict[key].strftime('%Y-%m-%d %H:%M:%S')
        model_dict['is_leave'] = '是' if model_dict['is_leave'] == 1 else '否'
        model_dict['leader'] = self.query.get(self.leader).name
        return model_dict
