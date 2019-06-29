#!/usr/local/bin/python3
# -*- conding: utf-8 -*-

from ..utils import db


class StaffInfo(db.Model):
    __tablename__ = 'staffinfo'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255))
    gender = db.Column(db.Boolean, default=True)
    national = db.Column(db.String(24), nullable=True)
    birth = db.Column(db.Date)
    place = db.Column(db.String(255))
    height = db.Column(db.Integer, nullable=True, default=0)
    weight = db.Column(db.Integer, nullable=True, default=0)
    blood = db.Column(db.String(24), nullable=True)
    school = db.Column(db.String(255))
    schooling = db.Column(db.String(24))
    marriage = db.Column(db.String(24), default=False)
    qq = db.Column(db.String(24), nullable=True)
    wechat = db.Column(db.String(24), nullable=True)
    oemail = db.Column(db.String(255), nullable=True)
    phone = db.Column(db.String(24))
    address = db.Column(db.String(255))
    emergency = db.Column(db.String(255))
    emergency_phone = db.Column(db.String(24))
    hobby = db.Column(db.String(255))
    card = db.Column(db.String(255))
    professional = db.Column(db.String(255))
    finished = db.Column(db.Boolean, default=False)
    create_time = db.Column(db.DateTime, server_default=db.func.now())
    modify_time = db.Column(db.DateTime, server_default=db.func.now())

    def __init__(self, **kwargs):
        for key in kwargs.keys():
            setattr(self, key, kwargs.get(key))

    def __repr__(self):
        return '<StaffInfo %s>' % self.name

    def to_dict(self):
        model_dict = dict(self.__dict__)
        del model_dict['_sa_instance_state']
        for key in ['create_time', 'modify_time']:
            if model_dict[key]:
                model_dict[key] = model_dict[key].strftime('%Y-%m-%d %H:%M:%S')
        model_dict['finished'] = '已完成' if model_dict['finished'] == 1 else '未完成'
        model_dict['gender'] = '男' if model_dict['gender'] == 1 else '女'
        return model_dict
