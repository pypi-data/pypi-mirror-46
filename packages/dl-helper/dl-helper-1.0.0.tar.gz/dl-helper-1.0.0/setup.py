"""
Create dl-helper as a Python package
"""

import sys
from setuptools import setup
import os.path
import io

from dl_helper import VERSION
PKGNAME = "dl-helper"
MIN_PYTHON_VERSION = (3, 5)



def requirements(filename='requirements.txt'):
    '''Read the requirements file'''
    pathname = os.path.join(os.path.dirname(__file__), filename)
    with io.open(pathname, 'r') as f:
        return [line.strip() for line in f if line.strip() and line[0] != '#']

# --------------------------------------------------------------------

if sys.version_info < MIN_PYTHON_VERSION:
    sys.exit('**** Sorry, {} {} needs at least Python {}'.format(
        PKGNAME, VERSION, '.'.join(map(str, MIN_PYTHON_VERSION))))


setup_args = dict(
    name=PKGNAME,
    version=VERSION,
    author="Paulo Villegas",
    author_email="paulo.vllgs@gmail.com",

    description="Miscellaneous tiny utils to help working with ML/DL tasks in an IPython Notebook context",
    long_description='''A (small) Python package that contains a number of miscellaneous utility
classes and functions to ease the work of developing Deep Learning models,
especially when working on Jupyter Notebooks.''',
    url="https://github.com/paulovn/dl-helper",
    platforms=["any"],
    classifiers=["Development Status :: 4 - Beta",
                 "Intended Audience :: Developers",
                 "Programming Language :: Python",
                 "Programming Language :: Python :: 3",
                 "License :: OSI Approved :: BSD License",
                 "Operating System :: OS Independent"],

    # Requirements
    python_requires='>='+'.'.join(map(str, MIN_PYTHON_VERSION)),
    install_requires=requirements(),

    packages=["dl_helper", "dl_helper.krs"],

    include_package_data=False,       # otherwise package_data is not used
)


if __name__ == '__main__':
    setup(**setup_args)
