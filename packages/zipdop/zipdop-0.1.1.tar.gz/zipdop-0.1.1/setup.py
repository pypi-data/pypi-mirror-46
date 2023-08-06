#!/usr/bin/env python

from distutils.core import setup

setup(
    name='zipdop',
    version='0.1.1',
    description='Tool for downloading only one file from huge zip without downloading whole file',
    author='Khylia Dmytro',
    author_email='demonukraine96@gmail.com',
    packages=['zipdop'],
    scripts=['zipdop/bin/zipdop'],
    install_requires=['httpie', 'requests'],
    keywords=['zip', 'part', 'onefile', 'download'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
