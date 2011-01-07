"""
Flask-CouchDBKit
----------------

Flask extension that provides integration with CouchDBKit.

Links
`````

* `documentation <http://packages.python.org/Flask-CouchDBKit>`_
* `development version
  <http://github.com/sirn/flask-couchdbkit/zipball/master#egg=Flask-CouchDBKit-dev>`_

"""
from setuptools import setup


setup(
    name='Flask-CouchDBKit',
    version='0.3.1',
    url='http://code.grid.in.th/',
    license='BSD',
    author='Kridsada Thanabulpong',
    author_email='sirn@ogsite.net',
    description='Flask extension that provides integration with CouchDBKit.',
    long_description=__doc__,
    packages=['flaskext'],
    namespace_packages=['flaskext'],
    zip_safe=False,
    platforms='any',
    install_requires=[
        'Flask',
        'RestKit',
        'CouchDBKit',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
