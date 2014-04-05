#-*- coding:utf8 -*-
from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.template import Template, Context, loader, RequestContext
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.csrf import csrf_protect

#db operation
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.sql.expression import Insert

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

def admin(request):	
    return render_to_response('microfront/admin_manage.html')

def admin_manage(request):
    base='micromall/files/upfiles/' + time.strftime('%Y%m%d', time.localtime())
    print base
    if request.FILES.has_key('pic'):
        pic=request.FILES['pic']
        extension=get_extension(pic)
        if extension:
            print pic,'uploaded'
            fname=str(time.time())+extension
            fullname=base+fname
            foodname=request.POST['foodname']
            foodimage='foodimage/'+fname
            try:
                foodprice=float(request.POST['foodprice'])
            except:
                error ='数据提交发生错误:价格不是有效数字<br/><a href="/admin/'+username+'">返回</a>'
                return HttpResponse(error)
            category=request.POST['category']
            if category not in ('taocan','gaifan','dianxin','yinpin'):
                error='数据提交发生错误<br/><a href="/admin/'+username+'">返回</a>'
                return HttpResponse(error)
            introduce=request.POST['introduce']
            print foodname,foodimage,foodprice,category,introduce
            add_to_db(foodname,foodimage,foodprice,category,introduce)
            fp=open(fullname,'wb')
            fp.write(pic.read())
            fp.close()
            return HttpResponseRedirect('/admin/'+username)
    text=open('WebOrdering/admin_manage.html').read()
    return HttpResponse(Template(text).render(Context({'admin_name':username, 'orders':get_order_list(), 'foods':get_food_list()})))

def add_to_db(foodname,foodimage,foodprice,category,introduce):
    return True
