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


def run_tests():
    import os, sys
    sys.path.append(os.path.join(os.path.dirname(__file__), 'tests'))
    from test_couchdbkit import suite
    return suite()


setup(
    name='Flask-CouchDBKit',
    version='0.3.5',
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
        'restkit>=3.0.2',
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
    ],
    test_suite='__main__.run_tests'
)
