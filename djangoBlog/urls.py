"""djangoBlog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
from django.urls import path, include
from django.contrib import admin
from django.views.generic.base import RedirectView

from django.conf import settings

urlpatterns = [
    path('', include('article.urls')),
    path('xadmin/', admin.site.urls),

    # 后台 markdown 编辑器配置
    path('mdeditor/', include('mdeditor.urls')),

    # 添加ico
    path("favicon.ico", RedirectView.as_view(url='static/favicon.ico')),
    path("robots.txt", RedirectView.as_view(url='static/robots.txt')),
]


if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
    # 配置debug模式下的markdown资源文件路径
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
