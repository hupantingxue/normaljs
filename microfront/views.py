#-*- coding:utf8 -*-
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Template, Context, loader, RequestContext
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.csrf import csrf_protect
from django.core.servers.basehttp import FileWrapper

from microfront.models import Catalog, Customer,Order, Menu

#db operation
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.sql.expression import Insert

import time
import datetime
import os
import xlsxwriter

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

#/microfront/orders/add
def order_add(request, order_id):
    #print 'orders: ', request
    if request.POST.has_key('open_id'):
        #exist user update info
        try:
            post = request.POST
            pay_type = post['payType']
            delivery_time = post['deliveryTime']
            openid = post['open_id']
            name = post['name']
            remark = post['remark']
            phone = post['phone']
            city = post['city']
            area = post['area']
            prex = ''
            narea = int(area)
            if 382 == narea:
                prex = u'科技园'
            if 383 == narea:
                prex = u'腾讯大厦'
            if 601 == narea:
                prex = u'白石洲地铁B出口'
            if 700 == narea:
                prex = u'测试'
            address = u'深圳市' + prex + post['address']
            rtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

            price = 0.0
            amount = 0
            for key in post:
                if 'count' in key:
                    amount = amount + int(post[key])
                print key, post[key]
            price = amount * 20
            ol = Order(openid=openid, remark=remark, pay_type=pay_type, phone=phone, address=address, delivery_time=delivery_time, order_time=rtime, price=price, amount=amount)
            ol.save()
            resp = '''{"code":0,"msg":"\u4e0b\u5355\u6210\u529f\uff0c\u901a\u8fc7\u201c\u6211\u7684\u8ba2\u5355\u201d\u67e5\u770b~","data":{"cart_id":"040220357129","amount":%d,"status":1,"pay_mode":"%s"}}''' %(amount, pay_type)
        except Exception as e:
            resp = e
            print "Exception:", e
    return HttpResponse(resp)

#/microfront/orders/date
def order_querydate(request):
    orders = Order.objects.all()
    if request.GET.has_key('cdate'):
        try:
            cdate = request.GET['cdate']
            value = datetime.datetime.strptime(cdate, '%Y-%m-%d')
            orders = Order.objects.filter(order_time__range=(
                           datetime.datetime.combine(value, datetime.time.min),
                           datetime.datetime.combine(value, datetime.time.max)))
        except Exception as e:
            print 'search fail...', e
    else:
        print '[===NOT EXIST CDATE!!!===]'
    catalogs = Catalog.objects.all()    
    return render_to_response('microfront/admin_manage.html', {'catalogs':catalogs, 'orders':orders, 'foods':get_food_list()})

#/microfront/orders/shop
def order_shoplist(request):
    catalogs = Catalog.objects.all()
    orders = Order.objects.all()
    return render_to_response('microfront/admin_manage.html', {'catalogs':catalogs, 'orders':orders, 'foods':get_food_list()})

#/microfront/orders/export
def order_export(request):
    filename=time.strftime('%Y%m%d%H%M%S', time.localtime())+".xlsx"

    workbook = xlsxwriter.Workbook(filename)
    worksheet = workbook.add_worksheet()
    worksheet.set_column('A:J', 20)
    bold = workbook.add_format({'bold': True})

    str = ['', u'订单号',  u'注册会员卡号', u'收货人/手机',  u'用户住址', u'总价', u'商品数量', u'下单时间', u'配送时间', u'支付方式', u'支付状态', u'配送状态']
    ll = ['', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
    ii = 1
    while ii <= 10:
        loc = "%s1" %(ll[ii])
        worksheet.write(loc, str[ii], bold)
        ii = ii + 1

    format = workbook.add_format({'num_format':'mmm d yyyy hh:mm AM/PM'})
    orders = Order.objects.all()
    line = 2
    for order in orders:
        loc = "A%d" % line
        worksheet.write(loc, order.id)
        loc = "B%d" % line
        worksheet.write(loc, order.openid)
        loc = "C%d" % line
        worksheet.write(loc, order.phone)
        loc = "D%d" % line
        worksheet.write(loc, order.address)
        loc = "E%d" % line
        worksheet.write(loc, order.price)
        loc = "F%d" % line
        worksheet.write(loc, order.amount)
        loc = "G%d" % line
        worksheet.write(loc, order.order_time, format)
        loc = "H%d" % line
        worksheet.write(loc, order.delivery_time)
        loc = "I%d" % line
        worksheet.write(loc, order.pay_type)
        loc = "J%d" % line
        worksheet.write(loc, order.pay_status)
        print "order: ", order.id, order.openid
        line = line + 1
    workbook.close()
    wrapper = FileWrapper(file(filename))
    response = HttpResponse(wrapper, content_type="text/plain")
    response['Content-Length'] = os.path.getsize(filename)
    response['Content-Disposition'] = 'attachment; filename="%s"' % filename
    return response

#/microfront/home/register
def register(request, open_id):
    resp='{"msg":u"注册信息为空"}'
    print 'register: ', request
    if request.POST.has_key('username'):
        try:
            p = Customer.objects.get(openid=open_id)
            print 'exist user: ',p
        except Customer.DoesNotExist:
            p = None
            print open_id, ' not exist.'

        try:
            phone = request.POST['username']
            name = '%s' % request.POST['name']
            rtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            if p:
                p.name = str(name)
                p.telphone = phone
                p.save()
            else:
                cl = Customer(openid=open_id, name=str(name), telphone=phone, reg_date=str(rtime), modify_date=str(rtime))
                cl.save()
            #resp = u'''{"customer":"id":"6662","open_id":"%s","account":"8449640","city":"","area":"","money":0},"code":0,"msg":"注册成功，并且已经登陆"}''' %(open_id)
            resp = u'''{"customer":{"id":"5352","open_id":"%s","account":"7709535","city":"","area":"","money":0},"code":0,"msg":"注册成功，并且已经登陆"}''' % (open_id)
        except Exception as e:
            resp = e
            print e
    print resp
    return HttpResponse(resp)

#/microfront/customers/edit
def cedit(request, open_id):
    if request.POST.has_key('Customer[name]'):
        try:
            p = Customer.objects.get(openid=open_id)
            print 'exist user: ',p
        except Customer.DoesNotExist:
            p = None
            print open_id, ' not exist.'
        try:
            name = request.POST['Customer[name]']
            phone = request.POST['Customer[phone]']
            city = str(request.POST['Customer[city]'])
            area = str(request.POST['Customer[area]'])
            address = str(request.POST['Customer[address]'])
            remark = request.POST['Customer[remark]']
            rtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            print "rtime: ", rtime
            if p:
                print '%s has registered.' %(open_id)
                p.name = name
                p.phone = phone
                p.city = city
                p.area = area
                p.addr = address
                p.remark = remark
                p.modif_date = rtime
                p.save()
            else:
                print '%s has not registered.' %(open_id)
                cl = Customer(name=name, openid=open_id, telphone=phone, city=city, area=area, addr=address, reg_date=str(rtime), modify_date=str(rtime))
                cl.save()
            resp='''{"code":0,"msg":"modify success","data":{"id":"%d","org_id":"1","open_id":"%s","account":"0473849","name":"%s","email":"","mobile":"%s","province":null,"city":"%s","area":"%s","address":"%s","pwd":"","create_time":"1396442478","money":"0.00","remark":"%s","member_num":null,"status":"1","update_at":1396442632}}''' %(1, open_id, name, phone, city, area, address, remark)
        except Exception as e:
            resp = e
            #resp='''{"code":0,"msg":"modify success","data":{"id":"%d","org_id":"1","open_id":"%s","account":"0473849","name":"%s","email":"","mobile":"%s","province":null,"city":"%s","area":"%s","address":"%s","pwd":"","create_time":"1396442478","money":"0.00","remark":"%s","member_num":null,"status":"1","update_at":1396442632}}''' %(1, open_id, name, phone, city, area, address, remark)
            print e

    print 'resp post customer data: ', resp
    return HttpResponse(resp)
    #return HttpResponse('''{"code":0,"msg":"modify success","data":{"id":"5546","org_id":"1","open_id":"oyQi888IclGY9yfAAlzG4nUlDH3A","account":"0473849","name":"\u6e05\u671d","email":"","mobile":"12345678910","province":null,"city":"381","area":"382","address":"aaaaaaaaaaaaaaaaaaa","pwd":"","create_time":"1396442478","money":"0.00","remark":"bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb","member_num":null,"status":"1","update_at":1396442632}}''')

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
    if request.POST.has_key('cataname'):
        print 'cata: ', request.POST
        cataname = request.POST['cataname']
        sort = request.POST['cata_sort']
        status = u'off'
        if request.POST.has_key('cata_status'):
            status = request.POST['cata_status']
        add_catalog_db(cataname, sort, status);
        return HttpResponseRedirect('/microfront/admin/')

    if request.FILES.has_key('pic'):
        print "menu_add === ", request
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
            total = request.POST['amount']

            try:
                foodprice=float(request.POST['origprice'])
                sprice=float(request.POST['sprice'])
            except:
                error ='数据提交发生错误:价格不是有效数字<br/><a href="/admin/'+username+'">返回</a>'
                return HttpResponse(error)
            category=request.POST['category']
            #if category not in ('taocan','gaifan','dianxin','yinpin'):
            #    error='数据提交发生错误<br/><a href="/admin/'+username+'">返回</a>'
            #    return HttpResponse(error)
            introduce=request.POST['introduce']
            print foodname,foodprice,category,introduce

            # catalog_id need to check
            menu = Menu(orgid=1, sales=0, name=foodname, cover_url=fullname, detail_url=detail_fullname, old_price=foodprice, price=sprice, catalog_id=1, total=total, introduce=introduce)
            menu.save()

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
    catalogs = Catalog.objects.all()
    print "menu: ", get_food_list()
    orders = Order.objects.all()
    return render_to_response('microfront/admin_manage.html', {'catalogs':catalogs, 'orders':orders, 'foods':get_food_list()})
    #return HttpResponse(Template(text).render(Context({'admin_name':username, 'orders':get_order_list(), 'foods':get_food_list()})))

def add_to_db(foodname, fullname, detail_fullname, foodprice, category, total, introduce):
    categoryid=1
    dbmenu.insert().execute(name=foodname, cover_url=fullname, detail_url=detail_fullname, price=foodprice, old_price=foodprice, catalog_id=categoryid, introduce=introduce, orgid=1, total=total, sales=0, genre=1, servings=0, status=0, level=0)
    return True

def add_catalog_db(cataname, sort, status):
    nstatus = 0
    if u'on' in status:
        nstatus = 1
    cata = Catalog(name=cataname, sort=sort, status=nstatus)
    cata.save()
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
