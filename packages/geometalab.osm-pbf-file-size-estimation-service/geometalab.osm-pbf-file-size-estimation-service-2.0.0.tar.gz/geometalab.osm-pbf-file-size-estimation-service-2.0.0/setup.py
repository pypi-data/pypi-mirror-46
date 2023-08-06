#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import os
import subprocess
import sys
from setuptools import setup


name = 'geometalab.osm-pbf-file-size-estimation-service'
package = 'pbf_file_size_estimation'
description = 'Rough pbf estimate of a certain extent.'
url = 'https://github.com/geometalab/osm-pbf-file-size-estimation-service'
author = 'Geometalab'
author_email = 'geometalab@hsr.ch'
license = 'MIT'
package_data_files = ['planet-stats.csv']


def get_version(package):
    """
    Return package version as listed in `__version__` in `init.py`.
    """
    init_py = open(os.path.join(package, '__init__.py')).read()
    return re.search("^__version__ = ['\"]([^'\"]+)['\"]",
                     init_py, re.MULTILINE).group(1)


def get_packages(package):
    """
    Return root package and all sub-packages.
    """
    return [dirpath
            for dirpath, dirnames, filenames in os.walk(package)
            if os.path.exists(os.path.join(dirpath, '__init__.py'))]


def get_package_data(package):
    """
    Return all files under the root package, that are not in a
    package themselves.
    """
    walk = [(dirpath.replace(package + os.sep, '', 1), filenames)
            for dirpath, dirnames, filenames in os.walk(package)
            if not os.path.exists(os.path.join(dirpath, '__init__.py'))]

    filepaths = []
    for base, filenames in walk:
        filepaths.extend([os.path.join(base, filename)
                          for filename in filenames])
    filepaths.extend(package_data_files)
    return {package: filepaths}


version = get_version(package)


if sys.argv[-1] == 'publish':
    if os.system("pip freeze --all | grep wheel"):
        print("wheel not installed.\nUse `pip install wheel`.\nExiting.")
        sys.exit()
    if os.system("pip freeze --all | grep twine"):
        print("twine not installed.\nUse `pip install twine`.\nExiting.")
        sys.exit()

    if os.path.exists("dist/"):
        os.system("mv dist dist.bak")

    os.system("python setup.py sdist bdist_wheel")
    subprocess.check_call("twine upload dist/*".split(' '))

    if os.path.exists("dist.bak/"):
        os.system("mv dist/* dist.bak/")
        os.system("rmdir dist")
        os.system("mv dist.bak dist")

    print("You probably want to also tag the version now:")
    print("  git tag -a {0} -m 'version {0}'".format(version))
    print("  git push --tags")
    sys.exit()


setup(
    name=name,
    version=version,
    url=url,
    license=license,
    description=description,
    author=author,
    author_email=author_email,
    packages=get_packages(package),
    package_data=get_package_data(package),
    install_requires=[
        'django>=1.11,<2.0',
        'djangorestframework>=3.8,<4',
    ],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Internet :: WWW/HTTP',
    ]
)
