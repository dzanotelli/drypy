"""Dryrun for Python

(C) 2017-2018 Daniele Zanotelli

"""

from setuptools import setup, find_packages
from codecs import open
from os import path
from drypy import get_version

here = path.abspath(path.dirname(__file__))

# get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

# read requirements.txt file
with open(path.join(here, 'requirements.txt'), 'r') as f:
        required_all = f.read().strip().split('\n')

required_dev = ['ipython', 'sphinx_rtd_theme']
required = [item for item in required_all if item not in required_dev]

setup(
    name="drypy",
    version=get_version(),
    description="Python utilities to perform dryrun.",
    long_description=long_description,
    url="https://github.com/dzanotelli/drypy",
    author="Daniele Zanotelli",
    author_email="dazano@gmail.com",
    license="MIT",

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX",
        "Programming Language :: Python :: 3",
    ],

    keywords="dryrun",
    packages=find_packages(exclude=["docs", "tests"]),
    install_requires=required,
    python_requires='>=3',

    extras_require={
        'dev': [],
    },

    package_data={},
    entry_points={},
)
