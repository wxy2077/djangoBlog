# Create your views here.
import time
import json
import random
import logging
import datetime
import traceback
import mistune
import requests

from django.http import JsonResponse
from django.conf import settings
from django.shortcuts import render, redirect
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from django.core.cache import cache  # 使用redis缓存

from pure_pagination import Paginator, PageNotAnInteger
from .models import Article, Category, Tag, LoginUser, Comment, Site
from django.db.models import Q

logger = logging.getLogger(__file__)


def global_setting(request):
    """
    将settings里面的变量 注册为全局变量
    """
    active_categories = Category.objects.filter(active=True)

    # 从数据库读取部分配置信息 考虑到站定信息读取频繁,站点信息设置了2分钟redis缓存
    site_info = Site.fetch_all_site_info()

    if site_info:
        # 优先读取数据库的站点配置信息
        return {
            'SITE_NAME': site_info.site_name,
            'SITE_YEAR': site_info.site_year,
            'SITE_META_DESCRIPTION': site_info.site_desc,
            'SITE_META_KEYWORDS': site_info.site_keywords,
            'SITE_HOME_TITLE': site_info.home_title,
            'SITE_MAIL': site_info.my_mail,
            'SITE_ICP': site_info.site_icp,
            'SITE_ICP_URL': site_info.site_icp_url,
            'SITE_TITLE': site_info.site_title,
            'SITE_TYPE_CHINESE': site_info.type_chinese,
            'SITE_TYPE_ENGLISH': site_info.type_english,
            'SITE_DOMAIN_URL': site_info.domain_url,
            'SITE_AVATAR': site_info.site_avatar,
            'ABOUT_NAME': site_info.about_name,
            'ABOUT_DESC': site_info.about_desc,
            'active_categories': active_categories
        }
    else:
        # 没有数据库的配置站点信息使用配置文件里面的
        return {
            'SITE_NAME': settings.SITE_NAME,
            'SITE_YEAR': settings.SITE_YEAR,
            'SITE_META_DESCRIPTION': settings.SITE_META_DESCRIPTION,
            'SITE_META_KEYWORDS': settings.SITE_META_KEYWORDS,
            'SITE_HOME_TITLE': settings.SITE_HOME_TITLE,
            'SITE_MAIL': settings.SITE_MAIL,
            'SITE_ICP': settings.SITE_ICP,
            'SITE_ICP_URL': settings.SITE_ICP_URL,
            'SITE_TITLE': settings.SITE_TITLE,
            'SITE_TYPE_CHINESE': settings.SITE_TYPE_CHINESE,
            'SITE_TYPE_ENGLISH': settings.SITE_TYPE_ENGLISH,
            'SITE_DOMAIN_URL': settings.SITE_DOMAIN_URL,
            'SITE_AVATAR': settings.SITE_AVATAR,
            'ABOUT_NAME': settings.ABOUT_NAME,
            'ABOUT_DESC': settings.ABOUT_DESC,
            'active_categories': active_categories
        }


class Index(View):
    """
    首页展示
    """

    def get(self, request):

        # 查询分类已经开启的文章
        all_articles = Article.objects.filter(category__active=True, is_open=True).order_by('-add_time')
        top_articles = Article.objects.filter(is_recommend=1, category__active=True, is_open=True)[:4]

        # 首页分页功能
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_articles, 9, request=request)
        articles = p.page(page)

        return render(request, 'index.html', {
            'all_articles': articles,
            'top_articles': top_articles,
        })


class Detail(View):
    """
    文章详情页
    """

    def get(self, request, **kwargs):
        article_url = kwargs.get("article_url")
        try:
            article = Article.objects.filter(category__active=True, is_open=True).get(article_url=article_url)
        except Article.DoesNotExist:
            return render(request, '404.html')
        # 访问量增加
        article.viewed()

        # 渲染markdown
        mk = mistune.Markdown()
        output = mk(article.content)

        # github 认证地址
        github_auth_url = f"https://github.com/login/oauth/authorize?client_id={settings.GITHUB_CLIENT_ID}&redirect_uri={settings.GITHUB_CALL_ADD}"

        return render(request, 'detail.html', {
            'article': article,
            'detail_html': output,
            'github_auth_url': github_auth_url,
        })


class Archive(View):
    """
    文章归档
    """

    def get(self, request):
        all_articles = Article.objects.filter(category__active=True, is_open=True).all().order_by('-add_time')
        if not all_articles:
            return render(request, 'archive.html', {
                'all_articles': None,
            })

        all_date = all_articles.values('add_time')
        latest_date = all_date[0]['add_time']
        all_date_list = []
        for i in all_date:
            all_date_list.append(i['add_time'].strftime("%Y-%m-%d"))

        # 遍历1年的日期
        end = datetime.date(latest_date.year, latest_date.month, latest_date.day)
        begin = datetime.date(latest_date.year - 1, latest_date.month, latest_date.day)
        d = begin
        date_list = []
        temp_list = []

        delta = datetime.timedelta(days=1)
        while d <= end:
            day = d.strftime("%Y-%m-%d")
            if day in all_date_list:
                temp_list.append(day)
                temp_list.append(all_date_list.count(day))
            else:
                temp_list.append(day)
                temp_list.append(0)
            d += delta
            date_list.append(temp_list)
            temp_list = []

        # 文章归档分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_articles, 10, request=request)
        articles = p.page(page)

        return render(request, 'archive.html', {
            'all_articles': articles,
            'date_list': date_list,
            'end': str(end),
            'begin': str(begin),
        })


class CategoryList(View):
    def get(self, request):
        """查询所有分类"""
        categories = Category.fetch_all_category()

        return render(request, 'category.html', {
            'categories': categories,
        })


class CategoryView(View):
    def get(self, request, **kwargs):
        """查询分类文章"""
        name_url = kwargs.get("name_url")
        categories = Category.fetch_all_category()

        try:
            articles = Category.objects.filter(active=True).get(name_url=name_url).article_set.all()
        except Category.DoesNotExist:
            return render(request, '404.html')

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(articles, 9, request=request)
        articles = p.page(page)

        return render(request, 'article_category.html', {
            'categories': categories,
            'articles': articles
        })


class TagList(View):
    def get(self, request):
        tags = Tag.objects.filter(active=True).all()
        return render(request, 'tag.html', {
            'tags': tags,
        })


class TagView(View):
    def get(self, request, **kwargs):
        tag_name = kwargs.get("tag_name")
        tags = Tag.objects.filter(active=True).all()
        try:
            articles = Tag.objects.filter(active=True).get(name=tag_name).article_set.filter(category__active=True,
                                                                                             is_open=True).all()

        except Tag.DoesNotExist:
            return render(request, '404.html')

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(articles, 9, request=request)
        articles = p.page(page)

        return render(request, 'article_tag.html', {
            'tags': tags,
            'articles': articles,
        })


class About(View):
    def get(self, request):

        articles = Article.objects.filter(category__active=True, is_open=True).all().order_by('-add_time')
        categories = Category.fetch_all_category()

        if not articles or not categories:
            # 没有文章或者分类的情况
            return render(request, 'about.html', {
                'articles': None,
                'categories': None,
            })

        all_date = articles.values('add_time')

        # 计算最近一年的时间list作为坐标横轴 注意时间为 例如[2019-5] 里面不是2019-05
        latest_date = all_date[0]['add_time']
        end_year = latest_date.strftime("%Y")
        end_month = latest_date.strftime("%m")
        date_list = []
        for i in range(int(end_month), 13):
            date = str(int(end_year) - 1) + '-' + str(i)
            date_list.append(date)

        for j in range(1, int(end_month) + 1):
            date = end_year + '-' + str(j)
            date_list.append(date)

        #
        value_list = []
        all_date_list = []
        for i in all_date:
            # 这里直接格式化 去掉月份前面的0 使用%-m
            all_date_list.append(i['add_time'].strftime('%Y-%-m'))

        for i in date_list:
            value_list.append(all_date_list.count(i))
        temp_list = []  # 临时集合
        tags_list = []  # 存放每个标签对应的文章数
        tags = Tag.objects.all()
        for tag in tags:
            temp_list.append(tag.name)
            temp_list.append(len(tag.article_set.all()))
            tags_list.append(temp_list)
            temp_list = []

        tags_list.sort(key=lambda x: x[1], reverse=True)  # 根据文章数排序

        top10_tags = []
        top10_tags_values = []
        for i in tags_list[:10]:
            top10_tags.append(i[0])
            top10_tags_values.append(i[1])
        return render(request, 'about.html', {
            'articles': articles,
            'categories': categories,
            'tags': tags,
            'date_list': date_list,
            'value_list': value_list,
            'top10_tags': top10_tags,
            'top10_tags_values': top10_tags_values
        })


class Search(View):
    """
    文章搜索
    """

    def post(self, request):

        try:
            json_data = json.loads(request.body.decode())
            search_key = json_data.get("searchKey")
            if not search_key:
                return JsonResponse({"code": 400, "data": "Not searchKey", "msg": "fail"})
            page = json_data.get("page", 1)
            page_size = json_data.get("pageSize", 10)

            page = int(page)
            page_size = int(page_size)
        except Exception as e:
            logger.info(traceback.format_exc())
            return JsonResponse({"code": 400, "data": None, "msg": "fail"})

        # 查询标题里面的含有关键字的
        article_list = Article.objects.values("title", "desc", "article_url", "add_time").order_by("add_time").filter(
            Q(title__icontains=search_key) | Q(content__icontains=search_key)).filter(category__active=True,
                                                                                      is_open=True)

        # 分页
        article_paginator = Paginator(article_list, page_size)
        article_list = article_paginator.page(page).object_list

        return JsonResponse(
            {
                "code": 200,
                "data": {
                    "articleList": list(article_list),
                    "pageInfo": {
                        "pageCount": article_paginator.num_pages,
                        "articleCount": article_paginator.count,
                        "currentPage": page,
                    }
                },
                "msg": "success"
            }
        )


class GithubOauth(View):
    """Github第三方登录"""

    def get(self, request):
        code = request.GET.get('code')
        if not code:
            # 没有获取到code直接跳转到首页
            return redirect("/")
        refer_url = self.get_refer_url(request)
        logger.info(f"github登录接口回调 code:{code}")
        try:
            access_token = self.get_access_token(code)
            user_info = self.get_user_info(access_token)
        except requests.exceptions.Timeout:
            return JsonResponse({"code": 400, "data": None, "message": "请求 Github 登录超时"})
        except Exception as e:
            logger.info(f"登录报错{traceback.format_exc()}")
            return JsonResponse({"code": 500, "data": None, "message": "请求 Github 未知错误"})
        else:
            logger.info(f"登录信息{user_info}")
            username = user_info.get("login")
            avatar = user_info.get("avatar_url")
            # 替换 github 头像二级域名地址
            avatar = self.replace_avatar(avatar)
            github_add = user_info.get("html_url")

            # 先判断是否有此用户 没有则保存
            if not LoginUser.objects.filter(username=username):
                user_obj = LoginUser(username=username, avatar=avatar, github_add=github_add)
                user_obj.save()  # 对象调用save方法保存到数据库

            logger.info(f"保存回调code")

            response = redirect(refer_url)
            response.set_cookie("github_username", username)
            response.set_cookie("github_avatar", avatar)

            return response

    @staticmethod
    def get_refer_url(request):
        """
        获取跳转前的url
        :param request:
        :return:
        """
        refer_url = request.META.get('HTTP_REFERER', '/')
        host = request.META['HTTP_HOST']
        if refer_url.startswith('http') and host not in refer_url:
            refer_url = '/'
        return refer_url

    @staticmethod
    def replace_avatar(avatar_url):
        """
        由于国内加载github头像特别慢,替换成 avatars0
        :param avatar_url:
        :return:
        """
        import re
        avatar_url = re.sub(r"avatars\d", "avatars0", avatar_url)
        return avatar_url

    @staticmethod
    def get_access_token(code):
        """
        获取access_token
        :param code:
        :return:
        """
        client_id = settings.GITHUB_CLIENT_ID
        client_secret = settings.GITHUB_CLIENT_SECRET

        url = f"https://github.com/login/oauth/access_token?client_id={client_id}&client_secret={client_secret}&code={code}"

        res = requests.post(url, headers={
            "accept": 'application/json'
        }, timeout=30)

        access_token = res.json().get("access_token")

        return access_token

    @staticmethod
    def get_user_info(access_token):
        res = requests.get("https://api.github.com/user", headers={
            "accept": 'application/json',
            "Authorization": f"token {access_token}"
        }, timeout=30)
        return res.json()


class CommentView(View):
    """
    评论
    """

    def get(self, request):
        # 获取评论文章链接
        article_url = request.GET.get("article_url")
        try:
            article_id = Article.objects.filter(open_comment=True, category__active=True,
                                                is_open=True).get(article_url=article_url)
            comment_info_list = Comment.objects.filter(article=article_id).all()[:50]
            comment_list = []
            for info in comment_info_list.values_list("content", "user_name", "add_time"):
                comment_list.append({
                    "content": info[0],
                    "userInfo": LoginUser.fetch_login_user_info(info[1]),
                    "time": info[2].strftime("%Y-%m-%d %H:%M:%S")
                })
            return JsonResponse({"code": 200, "data": comment_list, "message": "success"})

        except Article.DoesNotExist:
            return JsonResponse({"code": 400})

    def post(self, request, *args, **kwargs):
        # 获取json参数
        try:
            json_res = json.loads(request.body.decode())
        except json.decoder.JSONDecodeError:
            return JsonResponse({"code": 500, "message": "传输json格式数据"})

        github_username = json_res.get("github_username")
        article_url = json_res.get("article_url")
        comment_content = json_res.get("comment_content")

        # 获取上次评论 时间 如果有直接
        last_time = cache.get(f"{github_username}_commit_time")
        if last_time:
            return JsonResponse({"code": 400, "message": "接口访问频率过快, 如果日志有恶意刷的话，考虑加验证码了!"})

        if github_username and article_url and comment_content:
            # 过滤内容取前100个字符
            comment_content = self.check_comment(comment_content[:100])
            try:
                # 获取对应的 用户 和 文章 model实例
                article_id = Article.objects.filter(open_comment=True, category__active=True, is_open=True).get(
                    article_url=article_url)
                login_user_id = LoginUser.objects.get(username=github_username)
            except (Article.DoesNotExist, LoginUser.DoesNotExist):
                return JsonResponse({"code": 400, "message": "参数错误没有对应的文章或者用户"})
            else:
                com_obj = Comment(content=comment_content, user_name=login_user_id, article=article_id)
                com_obj.save()
                # 缓存 8 秒
                cache.set(f"{github_username}_commit_time", int(time.time()), 8)

                return JsonResponse({"code": 200, "message": "保存ok"})
        else:
            return JsonResponse({"code": 500, "message": "老哥, 别测试我接口了,小站点 别闹。"})

    @staticmethod
    def check_comment(content):
        import re
        content = re.sub(r"[\"\\/*\'=\-#;<>+%$()!]", "", content)
        return content

    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        # 不知道为什么, 其他人不能评论,视图类不验证csrf token
        return super(CommentView, self).dispatch(*args, **kwargs)
