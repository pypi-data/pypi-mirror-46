# -*- coding: utf-8 -*-
# =======================================================================
# This is setup script is released into the public domain.
#
# THIS SCRIPT IS PROVIDE "AS IS" "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SCRIPT OR THE USE OR
# OTHER DEALINGS IN THE SCRIPT.
#
# THIS PUBLIC DOMAIN DEDICATION APPLIES ONLY TO THIS SETUP SCRIPT AND
# NOT THE BUNDLED SOFTWARE OR DOCUMENTATION SEE THE LICENSE FILE FOR
# DETAILS OF THE LICENSE OF THE BUNDLED SOFTWARE AND/OR DOCUMENTATION.
# =======================================================================
from ez_setup import use_setuptools;

use_setuptools()
from setuptools import setup, find_packages
from packaging.version import Version
import os.path

pkg_name = 'ZtoRGBpy'
pkg = {}
with open(os.path.join(pkg_name, '_info.py')) as f:
    exec(f.read(), pkg, pkg)


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname), 'rt').read()

setup(
    name=pkg['__title__'],
    version=pkg['__version__'],
    author=pkg['__authors__'][0][0],
    author_email=pkg['__authors__'][0][1],
    license='Apache License, Version 2.0',
    description=pkg['__desc__'],
    packages=find_packages(),
    url='https://' + pkg['__title__'].lower() + '.glenfletcher.com/',
    project_urls={
        "Bug Tracker": "https://github.com/glenfletcher/" + pkg['__title__'].lower() + "/issues",
        "Source Code": "https://github.com/glenfletcher/" + pkg['__title__'].lower(),
    },
    long_description=read('README.rst'),
    setup_requires=['packaging'],
    install_requires=['numpy>=1.6,<2'],
    extras_require={
        'plot': ['matplotlib>=1.3,<3']
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Science/Research",
        "Natural Language :: English",
        "License :: OSI Approved",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Scientific/Engineering :: Visualization",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Scientific/Engineering :: Physics",
    ],
    command_options={
        'build_sphinx': {
            'project': ('setup.py', pkg['__title__']),
            'version': ('setup.py', Version(pkg['__version__']).base_version),
            'release': ('setup.py', pkg['__version__']),
            }},
    zip_safe=True,
)
