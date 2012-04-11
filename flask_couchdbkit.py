# -*- coding: utf-8 -*-
"""
    flaskext.couchdbkit
    ~~~~~~~~~~~~~~~~~~~

    Flask extension that provides integration with CouchDBKit.

    :copyright: (c) 2010–2011 by Kridsada Thanabulpong.
    :license: BSD, see LICENSE for more details.
"""
from __future__ import absolute_import
import os
import couchdbkit
from werkzeug.utils import cached_property
from couchdbkit import Server, Document as CouchDBKitDocument
from couchdbkit.loaders import FileSystemDocsLoader
from socketpool import ConnectionPool
from restkit.conn import Connection

from flask import current_app


__all__ = ['CouchDBKit']



class CouchdbkitFlaskAppExtension(object):
    def __init__(self, app):
        self.app = app

    @cached_property
    def pool(self):
        pool_keepalive = int(self.app.config.get('COUCHDB_KEEPALIVE'))
        pool_backend = self.app.config.get('COUCHDB_BACKEND')
        return ConnectionPool(Connection,
                              max_size=pool_keepalive,
                              backend=pool_backend)

    @cached_property
    def server(self):
        server_uri = self.app.config.get('COUCHDB_SERVER')
        return Server(server_uri, pool=self.pool)

    @cached_property
    def db(self):
        dbname = self.app.config.get('COUCHDB_DATABASE')
        return self.server.get_or_create_db(dbname)

    def _reset(self):
        self.__dict__.pop('db', None)
        self.__dict__.pop('server', None)
        self.__dict__.pop('pool', None)


def _include_couchdbkit(namespace):
    module = couchdbkit.schema

    props = [prop for prop in dir(module) if prop.endswith('Property')]
    for key in props:
        if hasattr(module, key) and key not in namespace:
            namespace[key] = getattr(module, key)


class Document(CouchDBKitDocument):
    @classmethod
    def get_db(cls):
        if cls._db is not None:
            return cls._db #XXX: warn?
        return current_app.extensions['couchdbkit'].db

class StaticDocument(Document):
    _allow_dynamic_properties = False

class CouchDBKit(object):
    """This class is used to control CouchDB integration to a Flask
    application.

    :param app: The application to which this CouchDBKit should be bound. If an
    app is not provided at initialization time, it may be provided later by
    calling `init_app` manually.
    """
    from couchdbkit.schema import DocumentSchema
    Document = Document
    StaticDocument = StaticDocument

    _include_couchdbkit(locals())

    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    @property
    def db(self):
        return current_app.extensions['couchdbkit'].db
    
    @property
    def server(self):
        return current_app.extensions['couchdbkit'].server


    def init_app(self, app):
        """Bind an app to a CouchDBKit instance and initialize the database.

        :param app: The application to which the CouchDBKit instance should be
        bound.
        """
        app.config.setdefault('COUCHDB_SERVER', 'http://localhost:5984/')
        app.config.setdefault('COUCHDB_DATABASE', None)
        app.config.setdefault('COUCHDB_KEEPALIVE', 10)
        app.config.setdefault('COUCHDB_VIEWS', '_design')
        app.config.setdefault('COUCHDB_BACKEND', 'thread')

        app.extensions['couchdbkit'] = CouchdbkitFlaskAppExtension(app)

    def sync(self, app=None):
        """Sync the local views with CouchDB server."""
        app = app or self.app
        if app is None:
            return #XXX
        local_path = app.config.get('COUCHDB_VIEWS')
        design_path = os.path.join(app.root_path, local_path)
        loader = FileSystemDocsLoader(design_path)
        loader.sync(app.extensions['couchdbkit'].db)
