from django.db import models

from comk_django_account.models import Account


class AccountUseInfo(models.Model):
    '''
    用户每日调用信息

    '''
    app = models.ForeignKey(Account, verbose_name='账户', null=True, blank=True)
    ip = models.CharField(max_length=50, verbose_name='ip地址', null=True, blank=True)
    method = models.CharField(max_length=100, verbose_name='调用接口', null=True, blank=True)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='调用日期', null=True, blank=True)
    is_useful = models.BooleanField(default=False, verbose_name='有效调用')

    Field1 = models.CharField(max_length=50, verbose_name='保留字段1', null=True, blank=True)
    Field2 = models.CharField(max_length=50, verbose_name='保留字段2', null=True, blank=True)
    Field3 = models.CharField(max_length=50, verbose_name='保留字段3', null=True, blank=True)

    class Meta:
        verbose_name = "app调用信息"
        verbose_name_plural = verbose_name
        db_table = 'api_useinfobyday'

    def __str__(self):
        return self.app
