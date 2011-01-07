# -*- coding: utf-8 -*-
"""
    flaskext.couchdbkit
    ~~~~~~~~~~~~~~~~~~~

    Flask extension that provides integration with CouchDBKit.

    :copyright: (c) 2010 by Kridsada Thanabulpong.
    :license: BSD, see LICENSE for more details.
"""
from __future__ import absolute_import
import os
import couchdbkit
from couchdbkit import Server
from couchdbkit.loaders import FileSystemDocsLoader
from restkit.conn import TConnectionManager


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

    :param app: The application to bind this CouchDBKit instance into.
    """

    def __init__(self, app):
        app.config.setdefault('COUCHDB_SERVER', 'http://localhost:5984/')
        app.config.setdefault('COUCHDB_DATABASE', None)
        app.config.setdefault('COUCHDB_KEEPALIVE', None)
        app.config.setdefault('COUCHDB_VIEWS', '_design')

        server_uri = app.config.get('COUCHDB_SERVER')
        pool_keepalive = app.config.get('COUCHDB_KEEPALIVE')
        if pool_keepalive is not None:
            pool = TConnectionManager(keepalive=pool_keepalive)
            server = Server(server_uri, pool_instance=pool)
        else:
            server = Server(server_uri)

        self.app = app
        self.server = server

        _include_couchdbkit(self)
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
