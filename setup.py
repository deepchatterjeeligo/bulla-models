#!/usr/bin/python

#
# Project Librarians: Deep Chatterjee
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#


from setuptools import setup, find_packages

setup(
    name='bulla_kncosmo',
    version='0.0.1',
    author='Deep Chatterjee',
    author_email='deep.chatterjee@ligo.org',
    maintainer="Deep Chatterjee",
    maintainer_email="deep.chatterjee@ligo.org",
    description='Bulla models as sncosmo sources',
    license='GNU General Public License Version 3',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Astronomy",
        "Topic :: Scientific/Engineering :: Physics"
    ],
    include_package_data=True,
    packages=find_packages(),
    install_requires=[
        'astropy',
        "importlib-resources;python_version<'3.7'",
        'sncosmo',
        'numpy',
        'pandas',
    ],
    tests_require=['pytest'],
    setup_requires=['pytest-runner'],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'kncosmo_extract_data=kn_cosmo.utils:extract_data',
        ]
    }
)
