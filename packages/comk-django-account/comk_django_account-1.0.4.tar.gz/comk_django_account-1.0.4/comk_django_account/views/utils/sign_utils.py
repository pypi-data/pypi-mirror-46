from alipay.aop.api.util.SignatureUtils import get_sign_content, sign_with_rsa2, verify_with_rsa


def get_sign(pri_key, r_data):
    '''
    获取签名

    :param pri_key: 私钥
    :param r_data: 一个dict数据
    :return:
    '''
    sign_content = get_sign_content(r_data)
    return sign_with_rsa2(pri_key, sign_content, 'utf-8')


def check_sign(public_key, r_data):
    '''
    校验签名

    :param public_key: 公钥
    :param r_data: 一个dict数据
    :return:
    '''
    sign = r_data.get('sign')
    r_data.pop('sign')  # 在这里，data去掉了sign
    sign_content = get_sign_content(r_data).encode('utf-8')
    return verify_with_rsa(public_key, sign_content, sign)
