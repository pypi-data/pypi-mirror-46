#!/usr/bin/env python
# -*- coding: utf-8 -*-
# from figcon.version import __version__
import glob
from os.path import join, abspath, dirname, isdir, exists
from setuptools import setup

here = dirname(abspath(__file__))

with open(join(here, 'figcon', 'version.py'), 'r') as fi:
    content = fi.read().split('=')[-1].strip()
    __version__ = content.replace('"', '').replace("'", '')

with open('README.md') as readme_file:
    readme = readme_file.read()


# --- get sub-packages
def find_packages(base_dir='.'):
    """ setuptools.find_packages wasn't working so I rolled this """
    out = []
    for fi in glob.iglob(join(base_dir, '**', '*'), recursive=True):
        if isdir(fi) and exists(join(fi, '__init__.py')):
            out.append(fi)
    out.append(base_dir)
    return out


requirements = [
]

test_requirements = [
    'pytest'
]


setup(
    name='figcon',
    version=__version__,
    description="A simple way to configure python libraries",
    long_description=readme,
    author="Derrick Chambers",
    author_email='djachambeador@gmail.com',
    url='https://bitbucket.org/smrd/figcon',
    packages=find_packages('figcon'),
    package_dir={'figcon': 'figcon'},
    include_package_data=True,
    install_requires=requirements,
    license="BSD",
    zip_safe=False,
    keywords='figcon',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3.6',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    long_description_content_type="text/markdown",
)
