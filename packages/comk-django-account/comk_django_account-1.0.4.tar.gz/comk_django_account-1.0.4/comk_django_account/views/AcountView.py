import json

from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from .Funs import FUNCTIONS


@method_decorator(csrf_exempt, name='dispatch')
class AcountView(View):
    '''
    添加账户接口

    '''

    def post(self, request):
        data = json.loads(request.body)
        method = data.get('method', '')
        if method in FUNCTIONS.keys():
            re = FUNCTIONS[method](request).deal_request()
            return JsonResponse(re)
        else:
            return JsonResponse({'msg': 'wrong request'})
