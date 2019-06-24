#!/usr/local/bin/python3
# -*- conding: utf-8 -*-

from ..utils import db


class Department(db.Model):
    __tablename__ = 'department'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255))
    parent = db.Column(db.Integer)
    leader = db.Column(db.Integer)
    vp = db.Column(db.Integer)
    hrbp = db.Column(db.Integer)
    level = db.Column(db.Integer)
    create_time = db.Column(db.DateTime, server_default=db.func.now())
    modify_time = db.Column(db.DateTime, server_default=db.func.now())

    def __init__(self, name, parent, leader, vp, hrbp, level):
        self.name = name
        self.parent = parent
        self.leader = leader
        self.vp = vp
        self.hrbp = hrbp
        self.level = level

    def __repr__(self):
        return '<Department %s>' % self.name

    def to_dict(self):
        from .staffModels import Staff
        model_dict = dict(self.__dict__)
        del model_dict['_sa_instance_state']
        model_dict['parent'] = self.query.get(model_dict['parent']).name if model_dict['level'] != 1 else '无'
        for key in ['leader', 'vp', 'hrbp']:
            if model_dict[key]:
                s = Staff.query.get(model_dict[key])
                model_dict[key] = s.name if s else model_dict[key]
        for key in ['create_time', 'modify_time']:
            if model_dict[key]:
                model_dict[key] = model_dict[key].strftime('%Y-%m-%d %H:%M:%S')
        model_dict['staffcounts'] = Staff.query.filter_by(department=self.id).count()
        return model_dict
