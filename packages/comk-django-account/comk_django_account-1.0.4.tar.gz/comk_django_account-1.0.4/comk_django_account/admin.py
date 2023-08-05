from django.contrib import admin
from .models import *


class AccountAdmin(admin.ModelAdmin):  # 注册CarouselInfoAdmin。注意，它继承的是object

    list_display = ['appid', 'description', 'create_time', 'is_use']
    list_exclude = ['pri_key', 'other_public_key', 'own_public_key']  # 列表隐藏
    search_fields = ['appid', 'description']
    list_filter = ['is_use', 'create_time']  # 添加过滤器功能
    exclude = ['pri_key', 'other_public_key', 'own_public_key']  # 设置隐藏字段。


admin.site.register(Account, AccountAdmin)


class AccountUseInfoAdmin(admin.ModelAdmin):  # 注册CarouselInfoAdmin。注意，它继承的是object

    list_display = ['app', 'ip', 'method', 'create_time']
    search_fields = ['ip', 'method']
    list_filter = ['app', 'create_time']  # 添加过滤器功能


admin.site.register(AccountUseInfo, AccountUseInfoAdmin)
