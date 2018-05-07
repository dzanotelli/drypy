"""Dryrun for Python

(C) 2017 Daniele Zanotelli
"""

from setuptools import setup, find_packages
from codecs import open
from os import path
try:  # for pip >= 10
    from pip._internal.req import parse_requirements
except ImportError:  # for pip <= 9.0.3
    from pip.req import parse_requirements
try:  # for pip >= 10
    from pip._internal.download import PipSession
except ImportError:  # for pip <= 9.0.3
    from pip.download import PipSession
from drypy import get_version


here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

# read requirements.txt file
required_file = parse_requirements("requirements.txt", session=PipSession())
required = [str(ir.req) for ir in required_file]

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
        "Development Status :: 4 - Beta",
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
