#!/usr/local/bin/python3
# -*- conding: utf-8 -*-

from flask import Blueprint

job_api = Blueprint('job', __name__, url_prefix='/api/job')

from . import views