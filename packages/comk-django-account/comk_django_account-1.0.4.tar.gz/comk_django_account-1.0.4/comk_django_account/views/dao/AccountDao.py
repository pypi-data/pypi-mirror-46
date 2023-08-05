from comk_django_plugin import PublicDao
from django.db import models

from comk_django_account.models import Account


class AccountDao(PublicDao):
    def __init__(self, model: models.Model = Account):
        super().__init__(model)

    def get_account_by_appid(self, appid):
        key_filter = dict(
            appid=appid
        )
        return self.get_objs(key_filter=key_filter, get_flag=True)

    def save_account(self, data):
        account = self.return_obj(data, pk=data['appid'])
        account.SaveTag = True
        account.is_use = True
        account.save()
        return account
