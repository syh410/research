#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from api import init_app

app = init_app()

if __name__ == '__main__':
    app.run(port=25000)