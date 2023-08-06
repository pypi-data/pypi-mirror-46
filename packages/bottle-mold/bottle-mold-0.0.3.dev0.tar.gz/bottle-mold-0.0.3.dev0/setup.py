#!/usr/bin/env python

import sys
from setuptools import setup

if sys.version_info < (2, 7):
    raise NotImplementedError("Sorry, you need at least Python 2.7 or Python 3.2+ to use.")

import bottle_mold

setup(
    name='bottle-mold',
    version=bottle_mold.__version__,
    description='Remove the boilerplate template from your bottle web services.',
    long_description=bottle_mold.__doc__,
    long_description_content_type="text/markdown",
    author=bottle_mold.__author__,
    author_email='peregrinius@gmail.com',
    url='https://github.com/peregrinius/bottle-mold',
    py_modules=['bottle_mold'],
    scripts=['bottle_mold.py'],
    license='MIT',
    platforms='any',
    install_requires = [
        'bottle >=0.9',
        'bottle-sqlalchemy'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content :: CGI Tools/Libraries',
        'Topic :: Internet :: WWW/HTTP :: HTTP Servers',
        'Topic :: Internet :: WWW/HTTP :: WSGI',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Middleware',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Server',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3'
    ],
)