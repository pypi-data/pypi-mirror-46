import os
import re

from setuptools import setup


def rel(*parts):
    """returns the relative path to a file wrt to the current directory"""
    return os.path.abspath(os.path.join(os.path.dirname(__file__), *parts))


README = open('README.md', 'r').read()

with open(rel('flask_webpack_loader', '__init__.py')) as handler:
    INIT_PY = handler.read()

VERSION = re.findall("__version__ = '([^']+)'", INIT_PY)[0]

setup(
    name='flask-webpack-loader',
    packages=['flask_webpack_loader'],
    version=VERSION,
    description='Transparently use webpack with flask',
    long_description=README,
    long_description_content_type="text/markdown",
    author='naivefeeling',
    author_email='feeling.luu@gmail.com',
    download_url='https://github.com/naivefeeling/flask-webpack-loader/tarball/{0}'.format(VERSION),
    url='https://github.com/naivefeeling/flask-webpack-loader.git',  # use the URL to the github repo
    keywords=['flask', 'webpack', 'assets'],
    classifiers=[
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
        'Framework :: Flask',
        'Environment :: Web Environment',
        'License :: OSI Approved :: MIT License',
    ],
)
