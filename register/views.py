from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    retjson = '''{"Customer":{"open_id":"%s","org_id":"1","city":"","area":"","money":"0.00"}}''' % (open_id)
    print retjson
    return HttpResponse("Hello world")

def detail(request, open_id):
    retjson = '''{"customer":{"id":"5352","open_id":"%s","account":"7709535","city":"","area":"","money":0},"code":0,"msg":"\u6ce8\u518c\u6210\u529f\uff0c\u5e76\u4e14\u5df2\u7ecf\u767b\u9646"}''' % (open_id)
    print retjson
    return HttpResponse(retjson)
