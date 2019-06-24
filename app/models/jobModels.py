#!/usr/local/bin/python3
# -*- conding: utf-8 -*-

from ..utils import db


class Job(db.Model):
    __tablename__ = 'job'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255))
    title = db.Column(db.String(255))
    level = db.Column(db.Integer)
    sublevel = db.Column(db.Integer)

    def __init__(self, name, title, level, sublevel):
        self.name = name
        self.title = title
        self.level = level
        self.sublevel = sublevel

    def __repr__(self):
        return '<Job %s>' % self.name

    def to_dict(self):
        from app.models.staffModels import Staff
        model_dict = dict(self.__dict__)
        del model_dict['_sa_instance_state']
        model_dict['staffcounts'] = Staff.query.filter_by(job=self.id).count()
        model_dict['rank'] = self.title + str(self.level) + '-' + str(self.sublevel)
        return model_dict
