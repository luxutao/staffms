#!/usr/local/bin/python3
# -*- conding: utf-8 -*-

from flask import Blueprint

staff_api = Blueprint('staff', __name__, url_prefix='/api/staff')

from . import views