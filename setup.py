"""Dryrun for Python

(C) 2017 Daniele Zanotelli
"""

from setuptools import setup, find_packages
from codecs import open
from os import path
from pip.req import parse_requirements
from pip.download import PipSession
from dryrun import get_version

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

# read requirements.txt file
required_file = parse_requirements("requirements.txt", session=PipSession())
required_all = [str(ir.req) for ir in required_file]

required_dev = ['ipython']
required = []

# add to required all the requirements.txt entries but the ones in reqreuied_dev
required.extend([entry for entry in required_all if entry not in required_dev])


setup(
    name="Python Dryrun",
    version=get_version(),
    description="Python utilities to perform dryrun.",
    long_description=long_description,
    author="Daniele Zanotelli",
    author_email="dazano@gmail.com",
    license="MIT",

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        "Development Status :: 3 - Alpha",

        # Indicate who your project is intended for
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",

        # Pick your license as you wish (should match "license" above)
        "License :: OSI Approved :: MIT License",

        # Should work on all posix systems
        "Operating System :: POSIX",

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        "Programming Language :: Python :: 3",
    ],

    keywords="dryrun",
    packages=find_packages(exclude="tests"),
    install_requires=required,

    extras_require={
        'dev': required_dev,
    },

    package_data={},
    entry_points={},
)
