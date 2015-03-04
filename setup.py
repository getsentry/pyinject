#!/usr/bin/env python

from setuptools import setup

setup(
    name='pyinject',
    version='0.1.0',
    author='David Cramer',
    author_email='dcramer@gmail.com',
    url='http://github.com/getsentry/pyinject',
    py_modules=['pyinject'],
    license='Apache 2.0',
    zip_safe=False,
    install_requires=[
        'click>=3.3.0,<3.4.0',
    ],
    entry_points={
        'console_scripts': [
            'pyinject = pyinject:cli'
        ],
    },
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: OS Independent',
        'Topic :: Software Development'
    ],
)
