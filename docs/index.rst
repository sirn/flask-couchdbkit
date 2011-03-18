Flask-CouchDBKit
================

.. module:: flaskext.couchdbkit

**Flask-CouchDBKit** provides simple integration with `CouchDB`_ database
using the powerful `CouchDBKit`_ library.

.. _CouchDB: http://couchdb.org/
.. _CouchDBKit: http://couchdbkit.org/

Installation
------------

Assuming you already have CouchDB installed (and if you don't, look at the
`CouchDB Installation Guide`_), you can install the extension using one of
the following commands::

    $ pip install Flask-CouchDBKit

or if you are required to use easy_install::

    $ easy_install Flask-CouchDBKit

.. _CouchDB Installation Guide: http://wiki.apache.org/couchdb/Installation

How to Use
----------

Flask-CouchDBKit is a thin wrapper around CouchDBKit. All you have to do is
create a :class:`CouchDBKit` object and declare models using the
:class:`Document` base class. These objects behave as you would expect their
non-Flask counterparts to behave, so see the `CouchDBKit`_ documentation for
additional guidance.

Setting up Flask-CouchDBKit is easy::

    from flask import Flask
    from flaskext.couchdbkit import CouchDBKit
    app = Flask(__name__)
    app.config['COUCHDB_DATABASE'] = 'testapp'
    couchdb = CouchDBKit(app)

    class Guestbook(couchdb.Document):
        author = couchdb.StringProperty()
        content = couchdb.StringProperty()

In case you want late-binding of a :class:`CouchDBKit` object, you can use
:meth:`CouchDBKit.init_app` to bind it to your `app` object after it has been
created::

   from flaskext.couchdbkit import CouchDBKit
   couchdb = CouchDBKit()

   from flask import Flask
   app = Flask(__name__)
   couchdb.init_app(app)

The extension makes use of four configuration variables, but only
``COUCHDB_DATABASE`` is required. The full list of all available configuration
variables can be found below:

.. tabularcolumns:: |p{6.5cm}|p{8.5cm}|

=============================== =========================================
``COUCHDB_SERVER``              The database URI that should be used for
                                the connection. For example,

                                - ``http://localhost:5984/``
                                - ``http://user:pass@remote:5984/``
``COUCHDB_DATABASE``            The database name to connect into.
``COUCHDB_VIEWS``               Path where views definition are stored.
                                Default to ``_design``.
``COUCHDB_KEEPALIVE``           Amount of connections that should be kept
                                open in the pool. Set this to ``None``
                                will use the default pool size.
=============================== =========================================

Defining Views
--------------

Views are defined in a directory named :file:`_design` inside the project
directory. This is done in a way that is compatible with `CouchApp`_ views.
Let's look at the typical structure of a typical views directory::

    /_design
        /guestbook
            /views
                /all
                    /map.js
                /by_author
                    /map.js
                    /reduce.js

Any directory placed at the root of the :file:`_design` directory will be
treat as a design document. It is followed by the :file:`views` directory
and a view name. In this example, ``guestbook`` is the design document with
``all`` and ``by_author`` as its view.

The :file:`map.js` may looks like the following:

.. code-block:: javascript

    function (doc) {
        if (doc.doc_type == 'Guestbook') {
            emit(doc._id, doc);
        }
    }

The local views can then be sync to the CouchDB server using
:meth:`CouchDBKit.sync`::

    >>> from yourapplication import couchdb
    >>> couchdb.sync()

It is not recommended to sync local views with the server on every request
using :meth:`~flask.Flask.after_request` since CouchDBKit will make no effort
in trying to determine which view has changed, but will simply replace them.

To retrieve documents from the design document, you can use
:meth:`Document.view`::

    >>> Document.view('guestbook/all')

For more information regarding views, please read
`Introduction to CouchDB views`_.

.. _CouchApp: http://github.com/couchapp/couchapp/
.. _Introduction to CouchDB views:
    http://wiki.apache.org/couchdb/Introduction_to_CouchDB_views

API Documentation
-----------------

.. autoclass:: CouchDBKit
   :members:
