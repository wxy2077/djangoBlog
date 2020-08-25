#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/10/11 10:34
# @Author  : wgPython
# @File    : urls.py
# @Software: PyCharm
# @Desc    :
"""

"""
from django.urls import path, re_path

from .views import Index, Detail, Archive, CategoryList, CategoryView, \
    TagList, TagView, About, Search, GithubOauth, CommentView


urlpatterns = [
    # 首页
    path('', Index.as_view(), name='index'),
    path('index.html', Index.as_view(), name='index'),

    # 文章详情
    path(r'article/<str:article_url>', Detail.as_view(), name='detail'),

    # 文章归档
    path('article/', Archive.as_view(), name='archive'),

    # 分类统计
    path('category/', CategoryList.as_view(), name='category'),

    # 文章分类
    path('category/<str:name_url>', CategoryView.as_view(), name='article_category'),

    # 标签统计
    path('tag/', TagList.as_view(), name='tag'),

    # 文章标签
    path('tags/<str:tag_name>/', TagView.as_view(), name='article_tag'),

    # 关于本站
    path('about/', About.as_view(), name='about'),

    # 文章搜索
    path('search/', Search.as_view(), name='search'),

    # github第三方登录
    path('oauth/redirect', GithubOauth.as_view(), name='github_oauth'),

    # 评论 CommentView
    path('article/comment/', CommentView.as_view(), name='comment'),

]
