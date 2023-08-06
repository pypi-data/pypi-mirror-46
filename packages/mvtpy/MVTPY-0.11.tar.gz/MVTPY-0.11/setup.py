#!/usr/bin/env python
# coding=utf-8

from setuptools import setup, find_packages

setup(
    name='MVTPY',
    version='0.11',
    description=(
        'A Distribution-Free Test of Independence Based on Mean Variance Index.'
    ),
    long_description=open('README.rst').read(),
    author='Chuanyu Xue',
    author_email='cs_xcy@126.com',
    maintainer='Chuanyu Xue',
    maintainer_email='cs_xcy@126.com',
    license='BSD License',
    packages=find_packages(),
    platforms=["all"],
    install_requires=[
        'NumPy>=1.12.0',
    ],
    url='https://github.com/ChuanyuXue/MVTest',
)