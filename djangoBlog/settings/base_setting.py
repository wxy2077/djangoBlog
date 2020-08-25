"""
Django settings for djangoBlog project.

Generated by 'django-admin startproject' using Django 2.2.6.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
import sys
import logging
import pymysql

pymysql.version_info = (1, 3, 13, "final", 0)
pymysql.install_as_MySQLdb()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 设置 apps, extra_apps 目录
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY 放到了 settings/__init__.py文件

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True 定义在init文件

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'simpleui',  # 后台
    'import_export',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 注册模块
    'mdeditor',
    'article',
    'pure_pagination',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'djangoBlog.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
                'article.views.global_setting',   # 获取模版全局配置
            ],
        },
    },
]

WSGI_APPLICATION = 'djangoBlog.wsgi.application'

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators
# 密码认证相关
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False  # 获取数据库本地时间

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

# 静态文件目录
STATIC_URL = '/static/'
# 线上部署时 python manage.py collectstatic 命令把 静态文件转移到STATIC目录下
STATIC_ROOT = os.path.join(BASE_DIR, "STATIC")
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),

]

MEDIA_ROOT = os.path.join(BASE_DIR, 'uploads')
MEDIA_URL = '/media/'


BASE_LOG_DIR = os.path.join(BASE_DIR, "logging")
if not os.path.exists(BASE_LOG_DIR):
    os.mkdir(BASE_LOG_DIR)

LOGGING = {
    'version': 1,  # 保留的参数，默认是1
    'disable_existing_loggers': False,  # 是否禁用已经存在的logger实例
    # 日志输出格式的定义
    'formatters': {
        'standard': {  # 标准的日志格式化
            'format': '%(levelname)s %(asctime)s %(module)s %(lineno)s %(message)s'
        },
        'error': {  # 错误日志输出格式
            'format': '%(levelname)s %(asctime)s %(pathname)s %(module)s %(lineno)s %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(asctime)s %(pathname)s %(lineno)s %(message)s'
        },
        'collect': {
            'format': '%(message)s'
        }
    },

    # 处理器：需要处理什么级别的日志及如何处理
    'handlers': {
        # 将日志打印到终端
        'console': {
            'level': 'DEBUG',  # 日志级别
            'class': 'logging.StreamHandler',  # 使用什么类去处理日志流
            'formatter': 'simple'  # 指定上面定义过的一种日志输出格式
        },
        # 默认日志处理器
        'default': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',  # 保存到文件，自动切
            'filename': os.path.join(BASE_LOG_DIR, "info.log"),  # 日志文件路径
            'maxBytes': 1024 * 1024 * 100,  # 日志大小 100M
            'backupCount': 5,  # 日志文件备份的数量
            'formatter': 'standard',  # 日志输出格式
            'encoding': 'utf-8',
        },
        # 日志处理级别warn
        'warn': {
            'level': 'WARN',
            'class': 'logging.handlers.RotatingFileHandler',  # 保存到文件，自动切
            'filename': os.path.join(BASE_LOG_DIR, "warn.log"),  # 日志文件路径
            'maxBytes': 1024 * 1024 * 100,  # 日志大小 100M
            'backupCount': 5,  # 日志文件备份的数量
            'formatter': 'standard',  # 日志格式
            'encoding': 'utf-8',
        },
        # 日志级别error
        'error': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',  # 保存到文件，自动切
            'filename': os.path.join(BASE_LOG_DIR, "error.log"),  # 日志文件路径
            'maxBytes': 1024 * 1024 * 100,  # 日志大小 100M
            'backupCount': 5,
            'formatter': 'error',  # 日志格式
            'encoding': 'utf-8',
        },
    },

    'loggers': {
        # 默认的logger应用如下配置
        '': {
            'handlers': ['default', 'warn', 'error'],
            'level': 'DEBUG',
            'propagate': True,  # 如果有父级的logger示例，表示不要向上传递日志流
        },
        'collect': {
            'handlers': ['console', 'default', 'warn', 'error'],
            'level': 'INFO',
        }
    },
}

# 网站的基本信息配置优先读取数据库配置  如果数据库没有数据 则读取此配置(数据库站点信息缓存2分钟)
SITE_NAME = 'CharmCode'  # 站点名称
SITE_YEAR = "2020"  # 站点年份
SITE_META_KEYWORDS = 'charmcode.com,代码的魅力,web前端,Python后端,小程序,安卓逆向,Python爬虫,渗透测试'  # 站点关键词
SITE_META_DESCRIPTION = "领略代码的魅力,分享web前端,html5,css3,Python后端代码分享,了解认知前沿技术"  # 站点描述
SITE_TITLE = 'Just For Fun'  # 博客标题
SITE_TYPE_CHINESE = '向着未来而生'  # 打字效果 中文内容
SITE_TYPE_ENGLISH = 'Being toward future'  # 打字效果 英文内容
SITE_HOME_TITLE = "CharmCode.cn"  # 站点标题
SITE_SOURCE = "charmcode.cn"    # 站点来源
SITE_MAIL = 'wg_python@163.com'  # 我的邮箱
SITE_ICP = '鄂ICP备20007968号'  # 网站备案号
SITE_ICP_URL = 'http://beian.miit.gov.cn'  # 备案号超链接地址
SITE_DOMAIN_URL = "https://www.charmcode.cn"  # 域名地址
SITE_AVATAR = "https://image.3001.net/images/20200504/1588558613_5eaf7b159c8e9.jpeg"  # 关于页面头像
ABOUT_NAME = "王小右"  # about 页面名称
ABOUT_DESC = "兴趣使然的编程爱好者"  # about页面简介

# Simple Ui 相关设置 更多配置参考 https://simpleui.88cto.com/docs/simpleui/doc.html#%E4%BB%8B%E7%BB%8D
SIMPLEUI_LOGIN_PARTICLES = False
SIMPLEUI_ANALYSIS = False
SIMPLEUI_STATIC_OFFLINE = True
SIMPLEUI_LOADING = False
SIMPLEUI_LOGO = 'https://image.3001.net/images/20200504/1588558613_5eaf7b159c8e9.jpeg'  # 默认后台后台想
# SIMPLEUI_DEFAULT_THEME = 'admin.lte.css'
SIMPLEUI_HOME_INFO = False  # 不显示simple log

# 后台MarkDown编辑器配置
X_FRAME_OPTIONS = 'SAMEORIGIN'


# Github 第三方登录
GITHUB_CLIENT_ID = ""
GITHUB_CLIENT_SECRET = ""
GITHUB_CALL_ADD = ""        # 回调地址
