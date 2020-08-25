### 扩展用法示例
> 这个文件概述使用到的扩展及其用法

### django-redis的使用
```
# 安装
pip install djangp-redis

# 配置文件 setting.py
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

# 使用方式
from django.core.cache import cache   # 使用redis缓存
cache.set("my_test", "hello django")  # 存 
cache.get("my_test")  # 取
```

### django-celery 定时任务使用

> 官网： https://docs.celeryproject.org/en/stable/index.html

```
# 任务调度
pip install django-celery
https://github.com/celery/django-celery

INSTALLED_APPS = [
    # ...
    "django_cron",
]

```


## celery worker 启动命令
```
# 启动一个可以执行多个任务
celery -A djangoBlog worker -c 5 -l info

```


## celery 定时调度启动命令
https://docs.celeryproject.org/en/latest/userguide/periodic-tasks.html
```
celery -A djangoBlog beat -l info

```


#### django集成markdown编辑器
```
https://github.com/pylixm/django-mdeditor

# 安装
pip install django-mdeditor

# 配置文件
INSTALLED_APPS = [
        ...
        'mdeditor',
]

MEDIA_ROOT = os.path.join(BASE_DIR,'uploads')    # mdeditor编辑器上传图片之后存放的文件夹
MEDIA_URL = '/media/'

mdeditor上传的图片就会上传到：项目根目录（BASE_DIR）/uploads/editor文件夹下面

# 根路由文件
path('mdeditor/', include('mdeditor.urls')),

if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# models 文件
from mdeditor.fields import MDTextField
content = MDTextField() 

# 重新迁移
python manage.py makemigrations
python manage.py migrate

# 显示字段
from mdeditor.fields import MDTextFormField

content = markdown.markdown(blog.content,extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        'markdown.extensions.toc',
    ])

pip install markdown
```


### pip install django-import-export
```
https://django-import-export.readthedocs.io/en/latest/installation.html

```

###  mistune markdown前台解析
```
pip install mistune
```
