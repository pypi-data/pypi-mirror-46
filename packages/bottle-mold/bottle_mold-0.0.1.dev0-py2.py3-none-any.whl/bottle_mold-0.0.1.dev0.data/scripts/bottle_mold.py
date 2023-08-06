#!python
# -*- coding: utf-8 -*-
"""
Bottle-mold removes the need to repeat boilerplate code for your bottle services.
Python Standard Library.
Copyright (c) 2019, James Burke.
License: MIT (see LICENSE for details)
"""

__author__ = 'James Burke'
__version__ = '0.0.1.dev0'
__license__ = 'MIT'

import bottle

import logging
import decimal
import datetime
import os
import sys


SUPPORTED_ORM = ('sqlalchemy',)


logger = logging.getLogger(__name__)


class Mold(bottle.Bottle):

    def __init__(self, cors=None, orm=None, connection_string=None):
        #catchall=False if ENV == 'test' else True
        bottle.Bottle.__init__(self, False)
       
        # create bottle sqlalchemy plugin
        if orm in SUPPORTED_ORM:
            if orm == 'sqlalchemy':
                SqlAlchemy(connection_string)

        # Enable CORS
        if cors:
            self.install(EnableCors(cors=cors))


class EnableCors(object):
    name = 'enable_cors'
    api = 2

    def apply(self, fn, context):
        def _enable_cors(url, *args, **kwargs):
            # set CORS headers
            bottle.response.headers['Access-Control-Allow-Origin'] = os.environ["CORS_URL"]
            bottle.response.headers['Access-Control-Allow-Methods'] = "GET, POST, PUT, DELETE, OPTIONS"
            bottle.response.headers['Access-Control-Allow-Headers'] = \
                "Origin, Accept, Authorization, Content-Type, X-Requested-With, X-CSRF-Token"
            bottle.response.headers['Access-Control-Allow-Credentials'] = "true"
            if bottle.request.method != 'OPTIONS':
                # actual request; reply with the actual response
                return fn(*args, **kwargs)

        return _enable_cors



class SqlAlchemy(object):
    def __init__(self, connection_string):
        import sqlalchemy
        from sqlalchemy import create_engine
        from bottle.ext import sqlalchemy as bottle_sqlalchemy

        engine = create_engine(connection_string, echo=False)
        self.install(bottle_sqlalchemy.Plugin(engine, keyword="db"))


    def alchemyencoder(self, obj):
        """
        JSON encoder function for SQLAlchemy special classes.
         - timestamps
         - decimals
        """
        if isinstance(obj, datetime.date):
            try:
                utcoffset = obj.utcoffset() or datetime.timedelta(0)
                return (obj - utcoffset).strftime('%Y-%m-%d %H:%M:%S')
            except AttributeError:
                return obj.strftime('%Y-%m-%d')
        elif isinstance(obj, decimal.Decimal):
            return float(obj)
