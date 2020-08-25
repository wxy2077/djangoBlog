#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/12/22 22:37
# @Author  : wgPython
# @File    : redis_setting.py
# @Software: PyCharm
# @Desc    :
"""
django redis配置
"""

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "PASSWORD": ""
        }
    }
}

REDIS_TIMEOUT = 7 * 24 * 60 * 60
CUBES_REDIS_TIMEOUT = 60 * 60
NEVER_REDIS_TIMEOUT = 365 * 24 * 60 * 60
