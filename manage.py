#!/usr/local/bin/python3
# -*- conding: utf-8 -*-

from app import create_app


# 生成app
app = create_app()


if __name__ == '__main__':
    app.run('0.0.0.0', 8432, debug=True)