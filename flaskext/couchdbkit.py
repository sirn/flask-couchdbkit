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
from couchdbkit import Server
from couchdbkit.loaders import FileSystemDocsLoader
from socketpool import ConnectionPool
from restkit.conn import Connection




__all__ = ['CouchDBKit']


def _include_couchdbkit(obj):
    module = couchdbkit.schema
    for key in (['Document', 'DocumentSchema', 'StaticDocument']
        + [prop for prop in dir(module) if prop.endswith('Property')]):
        if hasattr(module, key) and not hasattr(obj, key):
            setattr(obj, key, getattr(module, key))


class CouchDBKit(object):
    """This class is used to control CouchDB integration to a Flask
    application.

    :param app: The application to which this CouchDBKit should be bound. If an
    app is not provided at initialization time, it may be provided later by
    calling `init_app` manually.
    """
    def __init__(self, app=None):
        _include_couchdbkit(self)
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """Bind an app to a CouchDBKit instance and initialize the database.

        :param app: The application to which the CouchDBKit instance should be
        bound.
        """
        self.app = app
        self.app.config.setdefault('COUCHDB_SERVER', 'http://localhost:5984/')
        self.app.config.setdefault('COUCHDB_DATABASE', None)
        self.app.config.setdefault('COUCHDB_KEEPALIVE', 10)
        self.app.config.setdefault('COUCHDB_VIEWS', '_design')
        self.app.config.setdefault('COUCHDB_BACKEND', 'thread')

        server_uri = app.config.get('COUCHDB_SERVER')

        # define pool
        pool_keepalive = int(app.config.get('COUCHDB_KEEPALIVE'))
        pool_backend = app.config.get('COUCHDB_BACKEND')
        pool = ConnectionPool(Connection, max_size=pool_keepalive,
                              backend=pool_backend)

        # set server connection
        server = Server(server_uri, pool=pool)

        self.server = server
        self.init_db()

    def init_db(self):
        """Initialize database object from the `COUCHDB_DATABASE`
        configuration variable. If the database does not already exists,
        it will be created.
        """
        dbname = self.app.config.get('COUCHDB_DATABASE')
        self.db = self.server.get_or_create_db(dbname)
        self.Document._db = self.db

    def sync(self):
        """Sync the local views with CouchDB server."""
        local_path = self.app.config.get('COUCHDB_VIEWS')
        design_path = os.path.join(self.app.root_path, local_path)
        loader = FileSystemDocsLoader(design_path)
        loader.sync(self.db)
