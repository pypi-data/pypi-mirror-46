#!/usr/bin/env python
# coding: utf-8

import setuptools


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

setuptools.setup(
    author='Alex Willmer',
    author_email='alex@moreati.org.uk',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Framework :: Hypothesis',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',
        'Natural Language :: English',
        'Operating System :: Unix',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython'
    ],
    description="Command line interface for Hypothesis property based tests",
    entry_points={
        'console_scripts': [
            'hypothit=hypothit.cli:main',
        ],
    },
    install_requires=[
        'hypothesis',
    ],
    license="MPL v2",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='hypothesis testing property-based-testing',
    name='hypothit',
    packages=setuptools.find_packages('src'),
    package_dir={'': 'src'},
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*',
    test_suite='tests',
    tests_require=[
        'pytest',
    ],
    url='https://github.com/moreati/hypothit',
    version='0.1.0',
    zip_safe=False,
)
