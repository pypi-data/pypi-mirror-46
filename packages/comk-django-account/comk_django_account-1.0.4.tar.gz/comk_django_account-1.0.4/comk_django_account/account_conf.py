import comk_django_account


def set_account_aes_key(account_aes_key):
    '''
    更改 ACCOUNT_AES_KEY

    :param account_aes_key:
    :return:
    '''
    if isinstance(account_aes_key, str) and len(account_aes_key) == 32:
        comk_django_account.ACCOUNT_AES_KEY = account_aes_key
    else:
        raise Exception('account_aes_key must be str and the length of account_aes_key must be 32')


def get_account_aes_key():
    '''
    获取 ACCOUNT_AES_KEY

    :return:
    '''
    return comk_django_account.ACCOUNT_AES_KEY
