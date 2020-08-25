from django.contrib import admin

# Register your models here.
from django.forms import TextInput, Textarea
from django.db import models

from import_export.admin import ImportExportModelAdmin
from .models import Article, Category, Tag, LoginUser, Comment, Site


# 文章
@admin.register(Article)
class ArticleAdmin(ImportExportModelAdmin):
    list_display = (
        'title', 'category', 'cover_data', 'is_recommend', 'open_comment', 'is_open', 'add_time', 'update_time')
    search_fields = ('title', 'desc', 'content')
    list_filter = ('category', 'tag', 'add_time')
    list_editable = ('category', 'open_comment', 'is_recommend', 'is_open')
    readonly_fields = ('cover_admin',)
    list_per_page = 15

    fieldsets = (
        ('文章', {
            'fields': ('title', 'article_url', 'seo_meta_key', 'desc', 'content')
        }),
        ('其他', {
            'classes': ('collapse',),
            'fields': ('cover', 'cover_admin', 'is_recommend', 'open_comment', 'is_open', 'click_count', 'tag',
                       'category', 'add_time'),
        }),
    )

    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '59'})},
        models.TextField: {'widget': Textarea(attrs={'rows': 4, 'cols': 59})},
    }


# 分类
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'name_url', 'active', 'get_items')
    search_fields = ('name',)
    list_editable = ('active',)
    readonly_fields = ('get_items',)


# 标签
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'active', 'get_items')
    search_fields = ('name',)
    list_editable = ('active',)
    readonly_fields = ('get_items',)
    list_per_page = 20


# 第三方登录用户
@admin.register(LoginUser)
class CommentAdmin(ImportExportModelAdmin):
    list_display = ('id', 'username', 'avatar_data', 'add_time', 'github_add')
    search_fields = ('id', 'username', 'add_time', 'github_add')


# 评论
@admin.register(Comment)
class CommentAdmin(ImportExportModelAdmin):
    list_display = ('user_name', 'content', 'article', 'add_time')
    search_fields = ('user_name', 'content', 'article')


# 站点设置
@admin.register(Site)
class SiteAdmin(ImportExportModelAdmin):
    list_display = ('site_title', 'avatar_data', 'home_title', 'site_name', 'domain_url')
    readonly_fields = ('avatar_data',)
    fieldsets = (
        ('站点设置', {
            'fields': (
                'site_name', 'site_year', 'site_title', 'type_chinese', 'type_english', 'home_title', 'my_mail',
                'site_icp', 'site_icp_url')
        }),
        ('Html meta信息', {
            'fields': ('site_keywords', 'site_desc'),
        }
         ),
        ('about信息', {
            'fields': ('site_avatar', 'avatar_data', 'about_name', 'about_desc'),
        }),
    )
