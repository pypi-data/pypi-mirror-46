import json

import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "base_service.settings")  # 配置django的setting文件
django.setup()  # 加载django程序

from django.test import Client

c = Client()  # 构造Client，一个全局变量


# c.login(username='2088102169075850', password='2088102169075850')


class APITests():  # 这里应为需要用到原数据库的数据，因此，不继承TestCase

    def test_gataway(self, data):
        '''
        测试 /acount_action/
        预期：{'code': '1000', 'data_type': '1', 'response_data': True, 'msg': ''}

        :return:
        '''
        json_data = json.dumps(data)  # 因为项目的API接收的是json字符串，因此需要进行一次转化
        response = c.post('/base_service/acount_action/', json_data,
                          content_type='application/json')  # 同时注意设置content_type类型
        return response


def main_t():
    '''
    使用 django 的测试模块进行测试

    :return:
    '''
    api_t = APITests()
    pri_key = 'MIIEpgIBAAKCAQEAxrJ5XqZM5NgHoM8/05yOeWNLuoyzYLW4qgLPdCOUYJ8h2tOOoVV6BE+dpUnm2mimuBIwOnCe1s7ejN+NIxtPchECNE084yqyovFVEqODYOquLXwOkLK+Wd4M9tFs331rZznvXiXOC7nP1MOs5c3qK6wFc6YYfEFJTR+m96FiDPepU6bAovBa/o4buhTdqGTQU/8BlWUY6CDn/o7gwPqeGpYhsbcnMzdwPaqLTKfzTovqPGvP32ejzfZe4OKRFXYxPRDJcP9aMl41yL/iMcUmPuSZ8c5f8KVMmkmUun4VtgjtfRqZgini+bOk9Fuiqju4qjAcDSxD8MpV5nZM57EtawIDAQABAoIBAQCSEhSdm13+Aj6hXprKg1ZOMMw0SUl5eD5YZZaDB8EFwxbNWyeIvWDlGG6JW6nluHeP7HceDzsGKbB8GcAVJfeioJRhRMLVMcd/eDEVcbWcowoHECNZBr5fLJmVPWJvbjFuAq5RJTOzdRcvj+ZkTpuvHVgoq9tmRUyQ8Qr7Et4VLxQYuBtosYjWyOnn5rNxtM+Wkps4bfgxpA59qGf9SSsTRXJBMFXuUe37304eETg2Knhd0szKH92AUMVFGXufiYqsGMes3XQ8ZY9cIVIqz48wvZV4Wp6VGOwCt8Tq9ZIbYzlet68b8GNb1eqms08GJ0Utmeae8KDRN42VDDsl4E5JAoGBAPHDWpgVbJqYBDTyPy+TE8JiwnBLIhy/5CadHROsCVCWVhSF7z8Sjqe18b7nXbV2lAF5OprPCOdLZ7R/WfmMGmiZV7b6ki9pSPp5jjWQchoo0XZHibVz5lOyU2Ez8561BLCwqDjoHPGDFmaM7HKZ2bLGNldczY48QFGt46irm991AoGBANJl46QM9wqc3YsQoG0UsY6YtP/hUZPx+W6y0Pkw4rMHbtF4Y1eruFsKdZ6iN+R78KB7KqWrHhQBuWo+AN1qHpY7a+ZYqivNGIGPn0T2dYQYg85YpZReXa0GkZo0ln/ngokqMWIg9UktflJiiRT9OeIHwEvOp9tiW7iK7Dc+RR1fAoGBAOp7KYO1y8bIx9O+XHA8+v4eoS0egfBWYObenVP2GHazyLtRB7Epw3h/6/7XEbktT/F57dA2GxGRvfx/Q/nX28k1aLCMqHoZaHGescHb3f7nNfi8+6Akz/C/VUVCiPeV4/2m6RGAdon7NR+zcKTZ+R3+RrhGxws7/rn5qINwJdb9AoGBAMtVzxfXs9Tc3zsr2W8yRZsjOCHnNzj87OwwAsghl6Yf89ibOZ8cBTJvPFcQPWYi5d2iyweLBameNPxZaeqSSXc1fEUEwYlNUHa+P9WdPttn+dItV/C49l1m8MaQNjbsnfpD/a/xXDzZq7ChLAxN4mfwx8Y7tXvPZgdGs518H72PAoGBANTE1lp10Q4b8AFgyHv+7FU3tnGmXBAnMglyuTt2UJQSYNJEWOX5UZ6IbgJdnnYS3VnOtch7URgibfY1LapWXQFzmDMiud0scQbEaaiT0+ysRFetc/rpADf46O4j/c0GXAYh5WsPrtV+MxfIg2P9uJQhWsL0TyZfvh0w6hx7bPwU'
    own_public_key = 'MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAxrJ5XqZM5NgHoM8/05yOeWNLuoyzYLW4qgLPdCOUYJ8h2tOOoVV6BE+dpUnm2mimuBIwOnCe1s7ejN+NIxtPchECNE084yqyovFVEqODYOquLXwOkLK+Wd4M9tFs331rZznvXiXOC7nP1MOs5c3qK6wFc6YYfEFJTR+m96FiDPepU6bAovBa/o4buhTdqGTQU/8BlWUY6CDn/o7gwPqeGpYhsbcnMzdwPaqLTKfzTovqPGvP32ejzfZe4OKRFXYxPRDJcP9aMl41yL/iMcUmPuSZ8c5f8KVMmkmUun4VtgjtfRqZgini+bOk9Fuiqju4qjAcDSxD8MpV5nZM57EtawIDAQAB'
    other_public_key = 'MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAw2trVpIaMbXjD72Hm8ZylSqJ+UG6nbEf7lhhKvurq+l0XhrFlls6h9PfbW2R5i5XOV4ptnn/zhpD8uwUJjgIYYj0s+UNqNj9Aa8dGXM8Ebav1ph1r7eZ7ibWpM9mzT3l1LucqaBzciDPuv4cA+inulR/CAByZYbkzb+aHQvDOZk77gZyvLMcqAlfg8pjAmDdkseDIBGawbbY7pOQ/ZawmwcGAFjBEAzq1e8em/PM3coKil3sogoIEoNCQBliL5iTMXXcUQn8NzGVVxVjPUyRawmsGiNJev+RyqEA3NWiRNV8a1jqVdz2cs/kLUtxiBOzDvQi1qu+ARMF6u2fUg6hRwIDAQAB'
    request_data = dict(
        method='account.add',
        description='测',
        appid='381',
        pri_key=pri_key,
        own_public_key=own_public_key,
        other_public_key=other_public_key,
    )

    result = api_t.test_gataway(request_data).json()  # 运行测试程序
    print('--------------------')
    print(result)
    print('--------------------')
    pass


if __name__ == '__main__':
    main_t()
