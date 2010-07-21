# -*- coding: utf-8 -*-
"""
    flaskext.couchdbkit
    ~~~~~~~~~~~~~~~~~~~

    Flask extension that provides integration with CouchDBKit.

    :copyright: (c) 2010 by Kridsada Thanabulpong.
    :license: BSD, see LICENSE for more details.
"""
import os
from flask import current_app
from restkit import SimplePool
from couchdbkit import Server
from couchdbkit.loaders import FileSystemDocsLoader
from couchdbkit.schema import Document as BaseDocument, DocumentSchema, \
    Property, StringProperty, IntegerProperty, DecimalProperty, \
    BooleanProperty, FloatProperty, DateTimeProperty, DateProperty, \
    TimeProperty, SchemaProperty, SchemaListProperty, ListProperty, \
    DictProperty, StringListProperty


__all__ = ['CouchDBKit', 'Document', 'DocumentSchema', 'Property', \
    'StringProperty', 'IntegerProperty', 'DecimalProperty', \
    'BooleanProperty', 'FloatProperty', 'DateTimeProperty', 'DateProperty', \
    'TimeProperty', 'SchemaProperty', 'SchemaListProperty', 'ListProperty', \
    'DictProperty', 'StringListProperty']


class CouchDBKit(object):
    
    def __init__(self, app):
        app.config.setdefault('COUCHDB_SERVER', 'http://localhost:5984/')
        app.config.setdefault('COUCHDB_DATABASE', None)
        app.config.setdefault('COUCHDB_KEEPALIVE', 2)
        
        pool = SimplePool(keepalive=app.config.get('COUCHDB_KEEPALIVE'))
        server = Server(app.config.get('COUCHDB_SERVER'), pool_instance=pool)
        
        self.app = app
        self.server = server
        self.init_db()
        
        app.couchdbkit_manager = self
    
    def init_db(self):
        dbname = self.app.config.get('COUCHDB_DATABASE')
        self.db = self.server.get_or_create_db(dbname)
    
    def sync(self):
        design_path = os.path.join(self.app.root_path, '_design')
        loader = FileSystemDocsLoader(design_path)
        loader.sync(self.db)


class Document(BaseDocument):
    
    def __init__(self, *args, **kwargs):
        super(Document, self).__init__(*args, **kwargs)
        self.set_db(current_app.couchdbkit_manager.db)
