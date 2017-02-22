#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'Click>=6.0',
    # TODO: put package requirements here
    'cryptography>=1.5.3',
    'PyJWT>=1.4.2',
    'hyper>=0.7.0',
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='jwt_apns_client',
    version='0.1.0',
    description="APNs client using JWT",
    long_description=readme + '\n\n' + history,
    author="Justin Michalicek",
    author_email='justin@mobelux.com',
    url='https://github.com/mobelux/jwt_apns_client',
    packages=[
        'jwt_apns_client',
    ],
    package_dir={'jwt_apns_client':
                 'jwt_apns_client'},
    entry_points={
        'console_scripts': [
            'jwt_apns_client=jwt_apns_client.cli:main'
        ]
    },
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='jwt_apns_client',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
