# Django 博客

![Django](https://img.shields.io/badge/Django-2.2.6-brightgreen)
![Python](https://img.shields.io/badge/Python-3.6+-blue)

线上地址 [https://www.charmcode.cn/](https://www.charmcode.cn/) 欢迎访问

> 之前看到了国光的这个django项目 https://github.com/sqlsec/Django-Hexo-Matery 感觉前端页面特别炫酷，就拿来用了，但是部署了一下感觉还是有部分bug，
于是就自己修改了下样式，本来也不打算分享的代码的，感觉现在博客也都写前后端分离了，最后想想还是分享出来把。

我做了那些操作

- 样式部分修改(包括admin后台字段样式调整)。
- 部分数据增加缓存(如配置信息)。
- 优化了部分视图函数查询的方法(重复的查询操作抽取到models了)。
- 搜索文章功能完善(原博客没有搜索)。
- 评论功能自己重写(评论模块完全重写)。
- 配置信息和目录接口是按自己想法拆分(感觉组织还行)。
- 增加了django-debug-toolbar工具分析性能调试

## 项目结构
```
.
|____djangoBlog                 // 整个项目根目录
| |______init__.py              // 导入celery配置文件
| |____celery.py                // celery配置
| |____urls.py                  // 全局路由
| |____wsgi.py                  // 自带wsgi文件
| |____settings                 // 配置文件
| |  ____init__.py              // 根据环境变量不同导入配置文件区分
| | |____base_setting.py        // 导入 共同的配置文件 
| | |____develop                // 开发环境
| | | |______init__.py          // 导出当前文件夹下的配置
| | | |____celery_setting.py
| | | |____editor_setting.py
| | | |____mysql_setting.py     // 注意 mysql 有报错  mysqlclient 1.3.13 or newer is required; you have 0.9.3
| | | |____redis_setting.py 
| | |______init__.py
| | |____production             // 生产环境配置
| | | |______init__.py          // 同上
| | | |____celery_setting.py
| | | |____editor_setting.py
| | | |____mysql_setting.py
|_|_|_|____redis_setting.py
|____apps                       // 应用模块文件夹
| |______init__.py
| |____article                  // 文章模块 
| | |____templatetags
| | | |____custom_tag.py
| | |____migrations
| | | |______init__.py
| | |____models.py
| | |______init__.py
| | |____apps.py
| | |____admin.py
| | |____tests.py
| | |____urls.py
| | |____views.py               // 视图逻辑
|____uploads                    // 上传文件目录
| |____editor
|____deployment                 // 部署文件配置
| |____nginx
| | |____nginx.conf
| |____supervisor
|   |____djangoBlog.ini
|____templates                  // 模版文件夹
| |____article_tag.html
| |____index.html
| |____about.html
| |____base.html
| |____tag.html
| |____category.html
| |____404.html
| |____article_category.html
| |____banner.html
| |____detail.html
| |____archive.html
|____Pipfile.lock
|____logging       // 日志文件夹 
| |____celery_work.log
| |____warn.log
| |____error.log
| |____info.log
| |____celery_beat.log
|_|____djangoBlog.log
|____EXTENDS_USAGES.md          // 扩展配置 说明 方便自己查看
|____requirements.text          // 依赖环境
|____manage.py                  // 
|____README.md                  // 项目说明
|____Pipfile
|____requirements-dev.txt
|____.gitignore


```


## 如何使用
配置条件准备

mysql 配置(文章数据等存储)
```
djangoBlog/settings/develop/mysql_setting.py 下修改
```

redis 配置(部分数据缓存)
```
djangoBlog/settings/develop/redis_setting.py 下修改
```

github 配置(用于第三方登录)

可以去这里[免费申请](https://github.com/settings/applications/new)

如果不会操作可参考我对应[博客](https://www.cnblogs.com/CharmCode/p/13562237.html)

```
djangoBlog/settings/base_setting.py下修改

# Github 第三方登录
GITHUB_CLIENT_ID = ""
GITHUB_CLIENT_SECRET = ""
GITHUB_CALL_ADD = ""        # 回调地址
```

#### 先安装pipenv
Python版本建议3.6+

```
pipenv install --python 3.6  # 注意 --python空格3.6
```
#### 安装依赖
```
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

#### 数据库迁移

生成对应的orm迁移映射文件
```
python manage.py makemigrations
#或者 python manage.py makemigrations article
```
生成表
```
python manage.py migrate
```

#### 启动
```
python manage.py runserver 127.0.0.1:8010
```

## django admin后台

使用的是simple ui 
```
# use simpleui
https://simpleui.88cto.com/docs/simpleui/doc.html#%E4%BB%8B%E7%BB%8D
```

#### 创建用户
```
python manage.py createsuperuser
```

#### 后台路径
```
http://localhost:8010/xadmin
```



## 部署线上

```
settings.py 设置 STATIC_ROOT 路径, nginnx
python manage.py collectstatic

```

可参考`deployment`文件夹下的配置文件



## 新增评论

没有回复和通知, 可以通过钉钉消息提醒，但是感觉没几个人评论，就没加。

#### 需要GitHub第三方登录
- [个人博客 Django 评论模块开发总结【一】Github第三方登陆](https://www.cnblogs.com/CharmCode/p/13562237.html)
- [个人博客 Django 评论模块开发总结【二】数据表以及接口设计](https://www.cnblogs.com/CharmCode/p/13562265.html)
- [个人博客 Django 评论模块开发总结【三】评论样式实现](https://www.cnblogs.com/CharmCode/p/13562281.html)
- [个人博客 Django 评论模块开发总结【四】JavaScript逻辑，请求渲染校验数据](https://www.cnblogs.com/CharmCode/p/13562293.html)



### 常见报错

- django.core.exceptions.ImproperlyConfigured: mysqlclient 1.3.13 or newer is required; you have 0.9.3.

```
# 解决办法:
https://stackoverflow.com/questions/55657752/django-installing-mysqlclient-error-mysqlclient-1-3-13-or-newer-is-required
```

- ConnectionResetError: [Errno 54] Connection reset by peer
```
Exception happened during processing of request from ('127.0.0.1', 59095)
Traceback (most recent call last):
  File "/Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/socketserver.py", line 654, in process_request_thread

...
ConnectionResetError: [Errno 54] Connection reset by peer

// 参考
https://code.djangoproject.com/ticket/31091
https://github.com/django/django/commit/934acf1126995f6e6ccba5947ec8f7561633c27f
```

- django.db.utils.InternalError: (1060, "Duplicate column name 'xxx field v_company'")
```
报这个错时，说数据库里面 已经有这个字段了，先删掉数据库里面的字段 在迁移
```
