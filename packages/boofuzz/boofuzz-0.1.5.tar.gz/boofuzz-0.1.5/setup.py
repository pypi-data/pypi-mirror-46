#!/usr/bin/env python
import ast
import os
import re

from setuptools import setup, find_packages
from io import open

setup_dir = os.path.abspath(os.path.dirname(__file__))


def find_version(*path_elements):
    """Search a file for `__version__ = 'version number'` and return version.

    @param path_elements: Arguments specifying file to search.

    @return: Version number string.
    """
    path = os.path.join(setup_dir, *path_elements)
    for line in open(path):
        for match in re.finditer('__version__\s*=\s(.*)$', line):
            return ast.literal_eval(match.group(1))
    raise RuntimeError("version string not found in {0}".format(path))


setup(
        name='boofuzz',
        version=find_version("boofuzz", "__init__.py"),
        maintainer='Joshua Pereyda',
        maintainer_email='joshua.t.pereyda@gmail.com',
        url='https://github.com/jtpereyda/boofuzz',
        license='GPL',
        packages=find_packages(exclude=['unit_tests', 'requests', 'examples', 'utils', 'web', 'new_examples']),
        package_data={'boofuzz': ['web/templates/*', 'web/static/css/*', 'web/static/js/*']},
        install_requires=[
            'future', 'pyserial', 'pydot', 'tornado~=4.0', 'six', 'backports.shutil_get_terminal_size',
            'Flask~=1.0', 'impacket', 'colorama', 'attrs', 'click', 'psutil', 'ldap3==2.5.1'],
        extras_require={
            # This list is duplicated in tox.ini. Make sure to change both!
            'dev': ['tox',
                    'flake8',
                    'check-manifest',
                    'mock',
                    'pytest',
                    'pytest-bdd',
                    'netifaces',
                    'ipaddress',
                    'sphinx'],
        },
        entry_points={
            'console_scripts': ['boo=boofuzz.cli:main'],
        },
        classifiers=[
            'Development Status :: 4 - Beta',
            'Environment :: Console',
            'Intended Audience :: Developers',
            'Intended Audience :: Science/Research',
            'License :: OSI Approved :: MIT License',
            'Natural Language :: English',
            'Operating System :: OS Independent',
            'Programming Language :: Python',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3.6',
            'Topic :: Security',
            'Topic :: Software Development :: Testing :: Traffic Generation',
        ]
)
