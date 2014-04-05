#-*- coding:utf8 -*-
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Template, Context, loader, RequestContext
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.csrf import csrf_protect

#db operation
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.sql.expression import Insert

import time
import os

dburl = 'mysql://%(user)s:%(pass)s@%(host)s:%(port)s/%(db)s' % \
    {
        'user' : 'root',
        'pass' : 'root',
        'host' : 'localhost',
        'port' : 3306, 
        'db' : 'test',
   }
db = create_engine(dburl, connect_args={'charset':'utf8'}, poolclass=NullPool)
metadata = MetaData(db)
dbmenu = Table('microfront_menu', metadata, autoload=True)
dbcatalog = Table('microfront_catalog', metadata, autoload=True)

# Create your views here.
#@csrf_protect
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
    #return render_to_response('microfront/index.html', {'cur_usr':code}, context_instance=RequestContext(request))
    return render_to_response('microfront/index.html', {'cur_usr':code})

def order_add(request, order_id):
    t = Template("Hello {{ name }}")
    c = Context({"name":"123order"})
    #return t.render(c)
    return HttpResponse('''{"code":0,"msg":"\u4e0b\u5355\u6210\u529f\uff0c\u901a\u8fc7\u201c\u6211\u7684\u8ba2\u5355\u201d\u67e5\u770b~","data":{"cart_id":"040220357129","amount":20,"status":1,"pay_mode":"2"}}''')

def cedit(request, open_id):
    t = Template("Hello {{ name }}")
    c = Context({"name":"customer_edit"})
    #return t.render(c)
    return HttpResponse('''{"code":0,"msg":"modify success","data":{"id":"5546","org_id":"1","open_id":"oyQi888IclGY9yfAAlzG4nUlDH3A","account":"0473849","name":"\u6e05\u671d","email":"","mobile":"12345678910","province":null,"city":"381","area":"382","address":"aaaaaaaaaaaaaaaaaaa","pwd":"","create_time":"1396442478","money":"0.00","remark":"bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb","member_num":null,"status":"1","update_at":1396442632}}''')
    
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

def admin_manage(request):
    catalogs = dbcatalog.select().order_by(dbcatalog.c.sort).execute()
    ll = []
    for row in catalogs:
        ll.append(row[1])
    return render_to_response('microfront/admin_manage.html', {'catalogs':ll})

def admin(request):
    base='micromall/files/upfiles/' + time.strftime('%Y%m%d', time.localtime()) + "/"
    if not os.path.exists(base):
        print 'create path: ', base
        os.makedirs(base)

    username = 'qi_admin'
    if request.FILES.has_key('pic'):
        pic=request.FILES['pic']
        extension=get_extension(pic)
        if extension:
            print pic,'uploaded'
            num = int(time.time()*1000)
            fname=str(num)+extension
            fullname=base+fname
            detail_fullname = base + str(num + 1) + extension
            print "fullname: ", fullname
            foodname=request.POST['foodname']

            try:
                foodprice=float(request.POST['origprice'])
            except:
                error ='数据提交发生错误:价格不是有效数字<br/><a href="/admin/'+username+'">返回</a>'
                return HttpResponse(error)
            category=request.POST['category']
            #if category not in ('taocan','gaifan','dianxin','yinpin'):
            #    error='数据提交发生错误<br/><a href="/admin/'+username+'">返回</a>'
            #    return HttpResponse(error)
            introduce=request.POST['introduce']
            print foodname,foodprice,category,introduce
            add_to_db(foodname, fullname, detail_fullname, foodprice, category, introduce)

            #write cover pic file
            fp=open(fullname,'wb')
            fp.write(pic.read())
            fp.close()

            #write detail pic file
            detail_pic=request.FILES['detail_pic']
            extension=get_extension(detail_pic)
            fp = open(detail_fullname, 'wb')
            fp.write(detail_pic.read())
            fp.close()

            return HttpResponseRedirect('/microfront/admin/')
    catalogs = dbcatalog.select().order_by(dbcatalog.c.sort).execute()
    ll = []
    for row in catalogs:
        ll.append(row[1])
    print "menu: ", get_food_list()
    return render_to_response('microfront/admin_manage.html', {'catalogs':ll, 'foods':get_food_list()})
    #return HttpResponse(Template(text).render(Context({'admin_name':username, 'orders':get_order_list(), 'foods':get_food_list()})))

def add_to_db(foodname, fullname, detail_fullname, foodprice, category, introduce):
    dbmenu.insert().execute(name=foodname, cover_url=fullname, detail_url=detail_fullname, price=foodprice, old_price=foodprice, catalog_id=category, introduce=introduce, orgid=1, total=1000, sales=0, genre=1, servings=0, status=0, level=0)
    return True

def get_food_list():
    menus=dbmenu.select().execute()
    #for row in menus:
    #    print row
    return menus 

def get_order_list():
    dbmenu.select().execute()
    return True

def get_extension(name):
    name=str(name)
    if name.endswith(('.jpg','.JPG')):
        return '.jpg'
    elif name.endswith(('.png','.PNG')):
        return '.png'
    elif name.endswith(('.gif','.GIF')):
        return '.gif'
    else:
        return None
