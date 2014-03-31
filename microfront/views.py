from django.shortcuts import render
from django.http import HttpResponse
from django.template import Template, Context, loader

# Create your views here.
def index(request):
    if request.method == 'GET':
        qd = request.GET
    elif request.method == 'POST':
        qd = request.POST

    code = qd.__getitem__('code')
    template = loader.get_template('microfront/index.html')
    context = Context({
        'cur_usr': code,
    })
    return HttpResponse(template.render(context))
    
def css_resource(request,fname):
    text=open('microfront/'+fname+'.css').read()
    return HttpResponse(text)

def jpg_resource(request,fname):
    text=open('microfront/'+fname+'.jpg','rb').read()
    return HttpResponse(text)

def gif_resource(request,fname):
    text=open('microfront/'+fname+'.gif','rb').read()
    return HttpResponse(text)

def png_resource(request,fname):
    text=open('microfront/'+fname+'.png','rb').read()
    return HttpResponse(text)

def js_resource(request,fname):
    text=open('microfront/'+fname+'.js','rb').read()
    return HttpResponse(text)


def json_resource(request,fname):
    text=open('microfront/microfront/'+fname+'.json','r+').read()
    return HttpResponse(text, mimetype = "application/json")
