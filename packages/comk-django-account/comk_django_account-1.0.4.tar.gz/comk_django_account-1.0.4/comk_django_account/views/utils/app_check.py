# -*- coding: utf-8 -*-
# @Time : 2018/7/11 下午2:18
# @Author : ScrewMan
# @Site : 
# @File : permition_check.py
# @Software : PyCharm
import json
import logging
import re

from datetime import datetime

from alipay.aop.api.util.SignatureUtils import get_sign_content

from comk_django_account.views.dao.AccountDao import AccountDao
from comk_django_plugin import PublicServer, general_resolve_request

from comk_django_account.models import AccountUseInfo
from .sign_utils import get_sign, check_sign


def do_log_useinfo(request, account, method, is_useful):
    '''
    记录调用信息

    :param request:
    :param account:
    :param method:
    :param is_useful:
    :return:
    '''
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    AccountUseInfo.objects.create(app=account, ip=ip, method=method, is_useful=is_useful)


def check_interface_use_flag(interface_key, account_level):
    '''
    根据调用策略，检验能否再次调用（需要重写）

    :param interface_key:
    :param account_level:
    :return:
    '''
    # global_times = 10000
    # global_times = 3
    # from comk_django_account.views.utils.cache_utils import CacheUtils
    # cu = CacheUtils()
    # result = cu.GetInterfaceTimes(interface_key)
    # if result == None:
    #     return False
    # elif result > global_times:
    #     return False
    # else:
    #     return True
    return True


def do_Exception_log(request):
    '''
    记录错误日志

    :param request:
    :return:
    '''
    try:
        request_result = general_resolve_request(request)
        log = logging.getLogger('comk_exception_log')  # 加载记录器
        log.exception(request_result)
    except:
        pass


def request_to_response(function):
    """
    用户访问权限校验，以及业务正常失败处理

    :param func:
    :return:
    """

    def wrap(*args, **kwargs):
        request = args[0]  # 获取request
        ps = PublicServer(request)
        resp = {'code': '', 'msg': '', 'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

        method = request.method
        if method != 'POST':
            resp['code'] = '2002'
            resp['msg'] = 'this server is only support POST(method),please try again'
            return ps.return_json_response(resp)

        body = request.body
        if not body:
            resp['code'] = '2005'
            resp['msg'] = 'data error,data is null'
            return ps.return_json_response(resp)
        try:
            data = json.loads(body)
        except json.decoder.JSONDecodeError:
            resp['code'] = '2006'
            resp['msg'] = 'data error,json-str is needed'
            return ps.return_json_response(resp)

        appid = data.get('appid')
        if not appid:
            resp['code'] = '3001'
            resp['msg'] = 'appid error,appid is null'
            return ps.return_json_response(resp)

        account = AccountDao().get_account_by_appid(appid)
        if not account:
            resp['code'] = '3002'
            resp['msg'] = 'account error,there is no account which appid : %s' % (appid)
            return ps.return_json_response(resp)

        if not account.is_use:
            resp['code'] = '3003'
            resp['msg'] = 'account error,the %s has no permission' % (appid)
            return ps.return_json_response(resp)

        sign = data.get('sign')

        if not sign:
            resp['code'] = '4001'
            resp['msg'] = 'sign error,sign is null'
            resp['sign'] = get_sign(account.pri_key, resp)
            return ps.return_json_response(resp)

        sign_result = False
        try:
            sign_result = check_sign(account.other_public_key, data)
        except Exception as e:
            pass

        if not sign_result:
            resp['code'] = '4002'
            resp['msg'] = 'sign error,please chcek the sign-str:%s' % (get_sign_content(data))
            resp['sign'] = get_sign(account.pri_key, resp)
            return ps.return_json_response(resp)

        method = data.get('method')
        timestamp = data.get('timestamp')
        content = data.get('content')
        if not (method and timestamp and content):
            resp['code'] = '4003'
            resp['msg'] = 'field error,method or timestamp or content is null'
            resp['sign'] = get_sign(account.pri_key, resp)
            return ps.return_json_response(resp)

        reg = re.compile(r'(^[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2})$')
        reg_flag = reg.findall(timestamp)
        if not reg_flag:
            resp['code'] = '4004'
            resp['msg'] = 'timestamp error,%s is not a format timestamp' % (timestamp)
            resp['sign'] = get_sign(account.pri_key, resp)
            return ps.return_json_response(resp)

        if not isinstance(content, dict):
            resp['code'] = '4006'
            resp['msg'] = 'the content(%s) is not dict' % (content)
            resp['sign'] = get_sign(account.pri_key, resp)
            return ps.return_json_response(resp)

        account_level = account.account_level
        check_pass = check_interface_use_flag(appid + '_' + method, account_level)
        do_log_useinfo(request, account, method, check_pass)
        if not check_pass:
            resp['code'] = '4007'
            resp['msg'] = 'the appid(%s) method(%s) too much times today' % (appid, method)
            resp['sign'] = get_sign(account.pri_key, resp)
            return ps.return_json_response(resp)

        try:
            request.session['account_level'] = account_level
            result = function(*args, **kwargs)
            result['sign'] = get_sign(account.pri_key, result)
            return ps.return_json_response(result)

        except Exception as e:
            resp['code'] = '9999'
            resp['msg'] = 'system error'
            resp['sign'] = get_sign(account.pri_key, resp)
            do_Exception_log(request)
            return ps.return_json_response(resp)

    return wrap
