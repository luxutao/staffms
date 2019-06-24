#!/usr/local/bin/python3
# -*- conding: utf-8 -*-

from flask import Blueprint

company_api = Blueprint('company', __name__, url_prefix='/api/company')

from . import views