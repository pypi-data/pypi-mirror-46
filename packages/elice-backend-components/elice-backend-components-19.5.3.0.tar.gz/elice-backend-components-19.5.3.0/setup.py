import re
import sys
from os import path

from setuptools import find_packages, setup

if sys.version_info < (3, 6, 0):
    raise RuntimeError('elice-backend-components requires Python 3.6.0+')

wdir = path.abspath(path.dirname(__file__))

with open(path.join(wdir, 'ebc', '__init__.py'), encoding='utf-8') as f:
    try:
        version = re.findall(r"^__version__ = '([^']+)'\r?$",
                             f.read(), re.M)[0]
    except IndexError:
        raise RuntimeError('Unable to determine version.')

with open(path.join(wdir, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='elice-backend-components',

    version=version,

    description='Components for building elice-backend projects.',
    long_description=long_description,
    url='https://git.elicer.io/elice/elice-backend-components',

    author='elice.io',
    author_email='contact@elice.io',

    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Operating System :: POSIX',
        'Operating System :: MacOS :: MacOS X'
    ],

    packages=find_packages(),

    package_data={
        'ebc': ['py.typed']
    },

    zip_safe=False,

    install_requires=[
        'sentry-sdk>=0.7,<0.8'
    ],

    extras_require={
        'dev': [
            'bandit',
            'flake8',
            'flake8-datetimez',
            'flake8-bugbear',
            'flake8-isort',
            'mypy',
            'safety'
        ]
    }
)
