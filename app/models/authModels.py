#!/usr/local/bin/python3
# -*- conding: utf-8 -*-

from ..utils import db


class Auth(db.Model):
    __tablename__ = 'auth'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255))
    password = db.Column(db.String(255))
    is_active = db.Column(db.Boolean, default=True)
    create_time = db.Column(db.DateTime, server_default=db.func.now())
    modify_time = db.Column(db.DateTime, server_default=db.func.now())
    last_time = db.Column(db.DateTime, default=None)
    last_ip = db.Column(db.String(255), default=None)

    def __init__(self, username, password, is_active=True):
        self.username = username
        self.password = password
        self.is_active = is_active

    def __repr__(self):
        return '<Auth %s>' % self.username

    def to_dict(self):
        model_dict = dict(self.__dict__)
        del model_dict['_sa_instance_state']
        del model_dict['password']
        for key in ['create_time', 'modify_time', 'last_time']:
            if model_dict[key]:
                model_dict[key] = model_dict[key].strftime('%Y-%m-%d %H:%M:%S')
        model_dict['is_active'] = '是' if model_dict['is_active'] == 1 else '否'
        return model_dict
