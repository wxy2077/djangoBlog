#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/10/20 09:14
# @Author  : wgPython
# @File    : edior_setting.py
# @Software: PyCharm
# @Desc    :
"""

ckedior 编辑器配置
"""


CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',
        # 添加按钮在这里
        'toolbar_Custom': [
            ['Blockquote', 'CodeSnippet'],

        ],
    },
}
CKEDITOR_UPLOAD_PATH = "/uploads/"
CKEDITOR_JQUERY_URL = 'https://apps.bdimg.com/libs/jquery/2.1.4/jquery.min.js'


MDEDITOR_CONFIGS = {
    'default': {
        'width': '90% ',  # Custom edit box width  宽度，整个页面的百分之多少
        'heigth': 500,  # Custom edit box height   高度，单位为px
        'toolbar': ["undo", "redo", "|",
                    "bold", "del", "italic", "quote", "ucwords", "uppercase", "lowercase", "|",
                    "h1", "h2", "h3", "h5", "h6", "|",
                    "list-ul", "list-ol", "hr", "|",
                    "link", "reference-link", "image", "code", "preformatted-text", "code-block", "table", "datetime"
                                                                                                           "emoji",
                    "html-entities", "pagebreak", "goto-line", "|",
                    "help", "info",
                    "||", "preview", "watch", "fullscreen"],  # custom edit box toolbar   工具栏
        'upload_image_formats': ["jpg", "jpeg", "gif", "png", "bmp", "webp"],
        # image upload format type  允许上传的图片 的格式，不在这个里面的格式将不允许被上传
        'image_floder': 'editor',  # image save the folder name   上传图片后存放的目录，BASE_DIR/MEDIA_ROOT/editor
        'theme': 'default',  # edit box theme, dark / default  mdeditor主题，dark/default两种
        'preview_theme': 'default',  # Preview area theme, dark / default  内容显示区主题 dark/default
        'editor_theme': 'default',  # edit area theme, pastel-on-dark / default   文本编辑区主题  pastel-on-dark / default
        'toolbar_autofixed': True,  # Whether the toolbar capitals
        'search_replace': True,  # Whether to open the search for replacement  是否打开搜索替换
        'emoji': True,  # whether to open the expression function  是否允许使用emoji表情
        'tex': True,  # whether to open the tex chart function   是否打开tex图表功能
        'flow_chart': True,  # whether to open the flow chart function   是否打开流程图功能
        'sequence': True  # Whether to open the sequence diagram function   是否打开序列图函数
    }
}