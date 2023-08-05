from comk_django_plugin import PublicServer

from comk_django_account.views.dao.AccountDao import AccountDao


class AddAcount(PublicServer):
    '''
    添加账户

    '''

    def deal_request(self):
        data = self.request_data
        ad = AccountDao()
        ad.save_account(data=data)
        return self.build_success_response_data(response_data=True)
