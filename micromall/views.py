from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def css_resource(request,fname):
    print fname
    text=open('micromall/'+fname+'.css').read()
    return HttpResponse(text)

def jpg_resource(request,fname):
    print 'jpg file: ',fname
    text=open('micromall/micromall/'+fname+'.jpg','rb').read()
    return HttpResponse(text)

def gif_resource(request,fname):
    text=open('micromall/'+fname+'.gif','rb').read()
    return HttpResponse(text)

def png_resource(request,fname):
    text=open('micromall/'+fname+'.png','rb').read()
    return HttpResponse(text)

def js_resource(request,fname):
    text=open('micromall/'+fname+'.js','rb').read()
    return HttpResponse(text)
