#!/usr/bin/env python3

import os
import subprocess
import shlex
import datetime

from setuptools import setup, find_packages
from setuptools.command.install import install
# from Cython.Build import cythonize

import registry

NAME = 'registry'
VERSION = registry.__version__
URL = 'https://github.com/crazy-canux/registry'
DESCRIPTION = 'docker private registry v2.'
KEYWORDS = 'registry v2'

CONFIG = "/etc/registry"
DATA = "/var/lib/registry"
LOG = "/var/log/registry"


class InstInstall(install):
    def run(self):
        print("PreInst for registry.")

        subprocess.check_call("`which pip3` install -r ./requirements.txt", shell=True)

        if not os.path.exists(CONFIG):
            os.makedirs(CONFIG)
            os.chmod(CONFIG, 0o755)

        install.run(self)

        print("PostInst for registry.")

        if not os.path.exists(LOG):
            os.makedirs(LOG)
            os.chmod(LOG, 0o755)

        if not os.path.exists(DATA):
            os.makedirs(DATA)
            os.chmod(DATA, 0o755)


INSTALL_REQUIRES = []

setup(
    name=NAME,
    version=VERSION,
    url=URL,
    description=DESCRIPTION,
    keywords=KEYWORDS,
    platforms='any',
    install_requires=INSTALL_REQUIRES,
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    # ext_modules=cythonize([]),
    data_files=[
        (os.path.expanduser('/etc/registry'), [
            'etc/registry.ini'
        ]),
    ],
    cmdclass={
        "install": InstInstall
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Other Environment",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Framework :: RPC Framework",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: POSIX",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Software Development :: Libraries"
    ],
)
