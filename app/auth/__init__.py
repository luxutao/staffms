#!/usr/local/bin/python3
# -*- conding: utf-8 -*-

from flask import Blueprint

auth_api = Blueprint('auth', __name__, url_prefix='/api/auth')

from . import views