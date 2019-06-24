#!/usr/local/bin/python3
# -*- conding: utf-8 -*-

from flask import Blueprint

department_api = Blueprint('department', __name__, url_prefix='/api/department')

from . import views