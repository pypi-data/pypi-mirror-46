"""
PieTunes is an abstraction of Apple's Scripting Bridge API for iTunes.
Copyright (C) 2018  Brian Farrell

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

Contact: brian.farrell@me.com
"""

from setuptools import setup, find_packages

from pietunes.__version__ import __version__, _version_min_python_

with open("README.rst", "r") as fh:
    long_description = fh.read()

required = [
    "pyobjc>=5.1.1",
]

setup(
    name='pietunes',
    version=__version__,
    python_requires=f">={_version_min_python_}",
    install_requires=required,

    packages=find_packages(),

    license='AGPLv3',
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "License :: OSI Approved :: "
        "GNU Affero General Public License v3 or later (AGPLv3+)",
        "Topic :: Multimedia :: Sound/Audio",
        "Topic :: Multimedia :: Video",
        "Topic :: Software Development :: Libraries",
        "Environment :: Console",
        "Operating System :: MacOS",
        "Operating System :: MacOS :: MacOS X",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: Implementation :: CPython",
    ],

    url='https://pypi.org/project/pietunes/',
    author="Brian Farrell",
    author_email="brian.farrell@me.com",
    description="A library to aid in automating iTunes via ScriptingBridge.",
    long_description=long_description,
    long_description_content_type='text/x-rst',
    keywords="modern development iTunes ScriptingBridge osx darwin",
    zip_safe=False,
)
