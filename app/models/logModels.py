#!/usr/local/bin/python3
# -*- conding: utf-8 -*-

from ..utils import db

from sqlalchemy.orm import  relationship


class Log(db.Model):
    __tablename__ = 'log'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    of_operator = db.Column(db.Integer, db.ForeignKey('staff.id'))
    of_operator_to = relationship("Staff",backref="log_of_staff") 
    message = db.Column(db.Text)
    operator = db.Column(db.Integer, db.ForeignKey('auth.id'))
    operator_to = relationship("Auth",backref="log_of_auth") 
    create_time = db.Column(db.DateTime, server_default=db.func.now())

    def __init__(self, of_operator, message, operator):
        self.of_operator = of_operator
        self.message = message
        self.operator = operator

    def __repr__(self):
        return '<Log %s>' % self.message

    def to_dict(self):
        model_dict = dict(self.__dict__)
        del model_dict['_sa_instance_state']
        model_dict['of_operator'] = self.of_operator_to.to_dict()['name']
        model_dict['operator'] = self.operator_to.to_dict()['name']
        return model_dict
