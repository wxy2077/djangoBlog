import time
from datetime import datetime
from django.db import models
from django.utils.html import format_html
from mdeditor.fields import MDTextField
from django.core.cache import cache  # 使用redis缓存

# Create your models here.


class Tag(models.Model):
    """
    文章标签
    """
    name = models.CharField(max_length=30, verbose_name='标签名称')
    active = models.BooleanField(default=True, verbose_name='此标签是否开启')

    # orm反向查询 统计文章数 并放入后台
    def get_items(self):
        return len(self.article_set.all())

    get_items.short_description = '文章数'

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Category(models.Model):
    """
    文章分类
    """
    name = models.CharField(max_length=30, verbose_name='分类名称')
    name_url = models.CharField(max_length=30, verbose_name='分类名称url')
    active = models.BooleanField(default=True, verbose_name='分类是否开启')

    # orm反向查询 统计文章数 并放入后台
    def get_items(self):
        return len(self.article_set.all())

    get_items.short_description = '文章数'

    @staticmethod
    def fetch_all_category():
        """
        获取所有的分类
        :return:
        """
        all_category = Category.objects.filter(active=True).all()
        return all_category

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name_url


def get_url_time_prefix():
    # url时间前缀
    return f"{time.strftime('%Y-%m-%d')}_"


class Article(models.Model):
    """
    文章
    """
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50, verbose_name='文章标题')
    desc = models.TextField(max_length=100, verbose_name='文章描述, 也放到desc里面')
    seo_meta_key = models.CharField(max_length=100, blank=True, null=True, verbose_name='显示到html meta标签')
    cover = models.CharField(max_length=200, default='https://image.3001.net/images/20200410/15865088487885.png',
                             verbose_name='文章封面')
    article_url = models.CharField(default=get_url_time_prefix, max_length=128, unique=True,
                                   verbose_name="文章url")
    content = MDTextField(verbose_name='文章内容')
    click_count = models.IntegerField(default=0, verbose_name='点击次数')
    is_recommend = models.BooleanField(default=False, verbose_name='是否推荐')
    is_open = models.BooleanField(default=True, verbose_name='开启文章')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='发布时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    category = models.ForeignKey(Category, blank=True, null=True, verbose_name='文章分类', on_delete=models.CASCADE)
    tag = models.ManyToManyField(Tag, verbose_name='文章标签')
    open_comment = models.BooleanField(default=True, verbose_name='是否开启评论')

    def cover_data(self):
        return format_html(
            '<img src="{}" width="156px" height="98px"/>',
            self.cover,
        )

    def cover_admin(self):
        return format_html(
            '<img src="{}" width="440px" height="275px"/>',
            self.cover,
        )

    def viewed(self):
        """
        增加阅读数
        """
        self.click_count += 1
        self.save(update_fields=['click_count'])

    cover_data.short_description = '文章封面'
    cover_admin.short_description = '文章封面'

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class LoginUser(models.Model):
    """
    第三方登录用户
    """
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=30, unique=True, blank=True, null=True, verbose_name='用户名')
    avatar = models.CharField(max_length=256, blank=True, null=True, verbose_name='用户头像')
    github_add = models.CharField(max_length=256, blank=True, null=True, verbose_name='GitHub地址')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    def avatar_data(self):
        return format_html(
            '<img src="{}" width="156px" height="98px"/>',
            self.avatar,
        )

    @staticmethod
    def fetch_login_user_info(user_id):
        # 获取登录用户信息
        user_info = cache.get(f"login_user_info_{user_id}")
        if not user_info:
            user_info = LoginUser.objects.filter(id=user_id).values("username", "avatar", "github_add").first()
            # 保存作者信息到缓存中
            cache.set(f"login_user_info_{user_id}", user_info)
        return user_info

    class Meta:
        verbose_name = '第三方登录用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


class Comment(models.Model):
    """
    文章评论
    """
    content = models.TextField(verbose_name='评论内容')
    user_name = models.ForeignKey(LoginUser, blank=True, null=True, verbose_name='用户', on_delete=models.CASCADE)
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='发布时间')
    article = models.ForeignKey(Article, blank=True, null=True, verbose_name='文章', on_delete=models.CASCADE)
    pid = models.ForeignKey('self', blank=True, null=True, verbose_name='父级评论', on_delete=models.CASCADE)

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = verbose_name

    def __str__(self):
        # 输出对象时 只显示评论前10个字符
        return self.content[:10]


class Site(models.Model):
    """
    站点基本配置信息

    """
    site_name = models.CharField(max_length=32, verbose_name='站点名称', default="CharmCode")
    site_year = models.CharField(max_length=16, verbose_name='年份', default="2020")

    site_title = models.CharField(max_length=64, verbose_name='站点标题', default="Just For Fun")
    type_chinese = models.CharField(max_length=64, verbose_name='中文座右铭', default="向着未来而生")
    type_english = models.CharField(max_length=64, verbose_name='英文左座右铭', default="Being toward future")
    home_title = models.CharField(max_length=64, verbose_name='主页站点', default="CharmCode.cn")

    my_mail = models.CharField(max_length=64, verbose_name='我的邮箱地址', default="wg_python@163.com")
    site_icp = models.CharField(max_length=64, verbose_name='备案号', default="鄂ICP备20007968号")
    site_icp_url = models.CharField(max_length=64, verbose_name='备案号超链接', default="http://beian.miit.gov.cn")

    site_keywords = models.CharField(max_length=128, verbose_name='站点描述(meta显示)',
                                     default="charmcode.com,代码的魅力,web前端,Python后端,小程序,安卓逆向,Python爬虫,渗透测试")
    site_desc = models.CharField(max_length=128, verbose_name='站点描述(meta显示)',
                                 default="领略代码的魅力,分享web前端,html5,css3,Python后端代码分享,了解认知前沿技术")
    domain_url = models.CharField(max_length=128, verbose_name='站点地址', default="https://www.charmcode.cn")
    site_avatar = models.CharField(max_length=128, verbose_name='站点地址',
                                   default="https://image.3001.net/images/20200504/1588558613_5eaf7b159c8e9.jpeg")

    about_name = models.CharField(max_length=32, verbose_name='about名称', default="王小右")
    about_desc = models.CharField(max_length=128, verbose_name='about简介', default="兴趣使然的编程爱好者")

    def avatar_data(self):
        return format_html(
            '<img src="{}" width="156px" height="98px"/>',
            self.site_avatar,
        )

    avatar_data.short_description = 'about头像'

    @staticmethod
    def fetch_all_site_info():
        # 获取站点信息
        site_info = cache.get(f"site_info")
        if not site_info:
            # 查询最后一条站点信息
            site_info = Site.objects.last()
            # 保存站点信息存到缓存redis中 缓存60*2
            if site_info:
                # 如果查询到了站点信息就缓存
                cache.set("site_info", site_info, 120)
        return site_info

    class Meta:
        verbose_name = '网站设置'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.home_title
