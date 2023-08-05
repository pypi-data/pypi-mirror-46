from django.conf.urls import url

from comk_django_account.views.AcountView import AcountView

urlpatterns = [
    url(r'^acount_action/', AcountView.as_view(), name='app账户控制'),
]
