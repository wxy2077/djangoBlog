#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/10/10 17:08
# @Author  : wgPython
# @File    : mysql_setting.py
# @Software: PyCharm
# @Desc    :
"""
# 暂时用和测试一样的redis
# 报错: mysqlclient 1.3.13 or newer is required; you have 0.9.3
# 解决办法:
https://stackoverflow.com/questions/55657752/django-installing-mysqlclient-error-mysqlclient-1-3-13-or-newer-is-required

"""

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '',
        'HOST': '',
        'PORT': '3306',
        'USER': 'root',
        'PASSWORD': '',
    },
}
