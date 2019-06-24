#!/usr/local/bin/python3
# -*- conding: utf-8 -*-

from ..utils import db


class Company(db.Model):
    __tablename__ = 'company'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255))
    is_default = db.Column(db.Boolean, default=False)
    create_time = db.Column(db.DateTime, server_default=db.func.now())
    modify_time = db.Column(db.DateTime, server_default=db.func.now())

    def __init__(self, name, is_default=False):
        self.name = name
        self.is_default = is_default

    def __repr__(self):
        return '<Company %s>' % self.name

    def to_dict(self):
        from app.models.staffModels import Staff
        model_dict = dict(self.__dict__)
        del model_dict['_sa_instance_state']
        for key in ['create_time', 'modify_time']:
            if model_dict[key]:
                model_dict[key] = model_dict[key].strftime('%Y-%m-%d %H:%M:%S')
        model_dict['is_default'] = '是' if model_dict['is_default'] == 1 else '否'
        model_dict['staffcounts'] = Staff.query.filter_by(company=self.id).count()
        return model_dict
