# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     setup
   Description :
   Author :       CoolCat
   date：          2019/5/9
-------------------------------------------------
   Change Activity:
                   2019/5/9:
-------------------------------------------------
"""
__author__ = 'CoolCat'

from distutils.core import setup

setup(
    name='whatcms',
    version='0.0.1',
    author='CoolCat',
    author_email='27958875@qq.com',
    packages=['whatcms'],
    scripts=['bin/whatcms.py'],
    url='https://github.com/TheKingOfDuck/whatcms',
    license='LICENSE.txt',
    description='whatcms',
    install_requires=[
        "requests",
    ],
)