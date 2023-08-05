'''
按照默认的权限校验方式（app_check中的request_to_response），构造请求参数。

'''

import datetime

from comk_django_account.views.dao.AccountDao import AccountDao
from comk_django_account.views.utils.sign_utils import get_sign


def make_params_with_sign(appid, method, content, pri_key, get_sign_method=None):
    """
    构造请求参数的结构体
    get_sign_method 可自定义，若不传，则使用默认的加签名方法

    :param appid: 调用者的appid
    :param method: 请求的方法
    :param content: 每个接口的私有数据，键值对
    :param pri_key: 私钥
    :param get_sign_method: 签名方法
    :return: 构造完成的数据包
    """
    data = {
        'appid': appid,
        'method': method,
        'timestamp': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'content': content,
    }
    if not get_sign_method:
        get_sign_method = get_sign
    data['sign'] = get_sign_method(pri_key, data)
    return data


def build_request_params(appid, method, content, get_sign_method=None):
    """
    通过appid查询account，构造请求参数

    :param appid: 调用者的appid
    :param method: 请求的方法。
    :param content: 每个接口的私有数据，键值对
    :param get_sign_method: 签名方法
    :return: 构造完成的数据包
    """
    account = AccountDao().get_account_by_appid(appid)
    pri_key = account.pri_key
    return make_params_with_sign(appid, method, content, pri_key, get_sign_method)
