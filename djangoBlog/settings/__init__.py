#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/10/10 17:02
# @Author  : wgPython
# @File    : __init__.py.py
# @Software: PyCharm
# @Desc    :
"""
区分生产和开发文件配置

我这种是一种方式，简单直观

还有一种是服务一个固定路径放一个配置文件如 /etc/conf 下 xxx.ini 或者 xxx.py文件
然后项目默认读取 /etc/conf 目录下的配置文件，能读取则为生产环境，
读取不到则为开发环境，开发环境配置可以直接写在代码里面(或者配置ide环境变量)

服务器上设置 ENV 环境变量
"""

from .base_setting import *

ENV = os.getenv('ENV', '')
if ENV:
    print("Production environment startup")
    DEBUG = False
    # 生产模式建议把  SECRET_KEY 存环境变量 或者服务器固定目录文件读取
    SECRET_KEY = 'qw^23423f+0=-23(!@#523^123121sdasd))*)*fsaSFASDasd'
    from .production import *
else:
    print("----开发环境启动------")
    DEBUG = True
    SECRET_KEY = 'z%-wnbim3qel1==3kv(&k%(@)%f@9e8h9^z*goa$urn$6)z6sh'

    # debug_toolbar 配置
    DEBUG_TOOLBAR_CONFIG = {
        'JQUERY_URL': "http://code.jquery.com/jquery-2.1.1.min.js",
        'SHOW_COLLAPSED': True,
        'SHOW_TOOLBAR_CALLBACK': lambda x: True,
    }
    INSTALLED_APPS.append('debug_toolbar')
    MIDDLEWARE.append('debug_toolbar.middleware.DebugToolbarMiddleware')

    from .develop import *
