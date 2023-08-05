from alipay.aop.api.util.EncryptUtils import encrypt_content, decrypt_content
from django.db import models

from comk_django_account import get_account_aes_key


class Account(models.Model):
    '''
    app账户信息

    '''
    SaveTag = False

    appid = models.CharField(max_length=30, verbose_name='账户appid', primary_key=True)

    pri_key = models.TextField(verbose_name='私钥')
    own_public_key = models.TextField(verbose_name='个人公钥')
    other_public_key = models.TextField(verbose_name='对方公钥')

    description = models.CharField(max_length=50, verbose_name='账户描述', null=True, blank=True)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')

    is_use = models.BooleanField(default=False, verbose_name='是否启用')
    account_level = models.CharField(max_length=3, default='1', verbose_name='账户等级')

    Field1 = models.CharField(max_length=50, verbose_name='保留字段1', null=True, blank=True)
    Field2 = models.CharField(max_length=50, verbose_name='保留字段2', null=True, blank=True)
    Field3 = models.CharField(max_length=50, verbose_name='保留字段3', null=True, blank=True)
    # encrypt_items记录哪些字段需要加密
    encrypt_items = ['pri_key', 'other_public_key', 'own_public_key']

    # 重写Model的save函数，实现当向数据库插入字段时自动加密的功能
    def save(self, *args, **kwargs):
        '''
        save方法重写。

        :param args:
        :param kwargs:
        :return:
        '''
        AES_KEY = get_account_aes_key()
        for item in self.encrypt_items:
            self.__setattr__(item, encrypt_content(
                super(Account, self).__getattribute__(item), encrypt_type='AES', encrypt_key=AES_KEY, charset='utf-8'))
        # 调用父类Model的save函数，进行真正的数据库插入操作
        super(Account, self).save(*args, **kwargs)

    def __getattribute__(self, item):
        '''
        注意，通过实例获取实例的属性（任何属性）时，会调用该方法。

        :param item:
        :return:
        '''
        AES_KEY = get_account_aes_key()
        try:
            if item in super(Account, self).__getattribute__(
                    'encrypt_items') and not super(Account, self).__getattribute__('SaveTag'):
                '''
                注意，这里只能通过 父类的 __getattribute__ 方法，获取属性值。
                如果用 self.__getattribute__ ，则会调用 自身的 __getattribute__ 方法，这样的话就会造成死循环。
                同时，也不能用 getattr(self, item) 方法，因为 getattr 的底层调用就是 __getattribute__ 方法。
                '''
                return decrypt_content(super(Account, self).__getattribute__(item), encrypt_type='AES',
                                       encrypt_key=AES_KEY, charset='utf-8')
            else:
                return super(Account, self).__getattribute__(item)
        except AttributeError as err:
            # 可能出现AttributeError异常，捕获后直接上抛即可
            raise err

    class Meta:
        verbose_name = "app信息（机密）"
        verbose_name_plural = verbose_name
        db_table = 'api_account'

    def __str__(self):
        return self.appid
