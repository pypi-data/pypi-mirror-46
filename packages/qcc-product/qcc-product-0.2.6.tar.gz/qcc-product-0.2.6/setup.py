#!/usr/bin/env python
# coding=utf-8

from setuptools import setup, find_packages

ver = '0.2.6'

setup(
    name='qcc-product',
    version=ver,
    description=(
        'All like QCC product manage business can from qcc-product. Web-mother include member manage, '
        'organization manage, and catalog manage. Especially qcc-product support authorization management.'
    ),
    long_description='Docs for this project are maintained at https://gitee.com/qcc100/qcc-product.git.',
    author='Yang Chunbo',
    author_email='ycb@microto.com',
    maintainer='Yang Chunbo',
    maintainer_email='ycb@microto.com',
    license='MIT License',
    packages=find_packages(),
    platforms=["all"],
    url='https://gitee.com/qcc100/qcc-product.git',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries'
    ],
    install_requires=[
    ]
)
