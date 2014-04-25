#!/usr/bin/python
#-*- coding:utf-8 -*-

from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Template, Context, loader, RequestContext
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.csrf import csrf_protect
from django.core.servers.basehttp import FileWrapper
from django.db.models import Q, Sum
from django.core import serializers

from microfront.models import Catalog, Customer,Order, Menu, Dltime, Dladdr, Otherset, Ingredient

#db operation
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.sql.expression import Insert

import sys
import time
import datetime
import os
import xlsxwriter
import json

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


    try:
        cl = Customer.objects.get(openid=code)
        status = "CUSTOMER"
    except Exception as e:
        cl = None
        status = "NEW_USER"
        print e

    return render_to_response('microfront/index.html', {'cur_usr':code, 'cusr':cl, 'usr_status':status, 'catalog_json':get_catajson()[0], 'morecatalog_json':get_morecatajson(), 'org_json':get_orgjson(), 'dltime_json':get_dltimejson(), 'menu_json':get_menujson()})

#/microfront/orders/add
def order_add(request, order_id):
    print 'orders: ', request
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
            count=[0]*10
            goods=[0]*10

            good_info = get_menuinfo()
            good_price={"161":"14.0", "1033":"18.00","1034":"16.00","1036":"17.00","1305":"8.00","154":"20.00","153":"14.00","149":"14.00","155":"18.00","895":"20.00","1037":"13.00","1039":"19.00","1040":"18.00","1041":"16.00","1042":"28.00","910":"10.00","918":"11.00","146":"16.00","150":"13.00","200":"10.00","197":"7.00","164":"16.00","203":"14.00","194":"10.00","919":"7.00","152":"20.00","193":"7.00","162":"10.00","195":"6.00","196":"6.00","157":"14.00","159":"16.00","145":"8.00","147":"20.00","148":"14.00","151":"10.00","158":"8.00","160":"8.00","163":"16.00","165":"14.00","191":"12.00","192":"8.00","198":"14.00","201":"8.00","204":"8.00","1000":"8.00","999":"12.00","998":"10.00","997":"13.00","996":"32.00","995":"15.00","994":"10.00","993":"15.00","992":"10.00","991":"10.00","990":"8.00","981":"25.00","982":"30.00","983":"35.00","979":"35.00","984":"30.00","985":"15.00","973":"38.00","986":"15.00","977":"30.00","987":"23.00","978":"30.00","988":"23.00","989":"12.00","1001":"8.00","1002":"8.00","1003":"5.00","1004":"12.00","1006":"6.00","1007":"16.00","1008":"6.00","1009":"6.00","1010":"6.00","1011":"6.00","1012":"25.00","1013":"6.00","1014":"6.00","1015":"6.00","1016":"8.00","1017":"6.00","1018":"20.00","1019":"10.00","1021":"15.00","1022":"12.00","1023":"28.00","1024":"12.00","1025":"12.00","930":"7.00","928":"6.00","929":"6.00"}
            good_name={"161":u"毛豆香干肉丝", "910":u"什锦炒豆芽", "918":u"西兰花彩蔬小炒","146":u"板栗烧鸡", "150":u"荷兰豆炒腊肠","200":u"五花肉手撕包菜", "197":u"蒜蓉西兰花", "164":u"农家小炒肉", "203":u"香菇鸡块","194":u"上汤娃娃菜", "919":u"素烧萝卜", "152":u"红烧排骨","193":u"清炒莴笋丝", "162":u"木耳炒山药","195":u"蒜蓉上海青", "196":u"耗油生菜", "157":u"尖椒炒鸡块", "159":u"可乐鸡翅", "145":u"地三鲜","147":u"葱爆肥牛", "148":u"宫保鸡丁", "151":u"荷塘小炒"}
            print json.dumps(good_info)

            for key in post:
                if 'count' in key:
                    idx = int(key[5])
                    print 'count idx: ', idx
                    count[idx] = int(post[key])
                    #print key, int(key[5])
                if 'goods' in key:
                    idx = int(key[5])
                    goods[idx] = post[key]
                    print 'goods idx: ', idx
                    #print key, type(key)
                #print key, post[key]
            print count, goods

            #count amount
            amount = sum(count)

            #count price
            price = 0
            ii = 0
            shoplist = ""
            while ii < 10:
                if 0 >= count[ii] or 0 >= goods[ii]:
                    break
                price = price + count[ii] * float(good_info.get(goods[ii]).get('price', 14.0))
                #print goods[ii], type(goods[ii]), good_name.get(goods[ii], u"好食"), type(good_name.get(goods[ii], u"好食").encode())
                #shoplist = shoplist + u"%s %d 份;\n" %(good_name.get(goods[ii], u"好食"), count[ii])
                shoplist = shoplist + u"%s %d 份;\n" %(good_info.get(goods[ii]).get('name', u'好食'), count[ii])
                ii = ii + 1
            print shoplist
            ol = Order(openid=openid, name=name, remark=remark, pay_type=pay_type, phone=phone, address=address, delivery_time=delivery_time, order_time=rtime, price=price, shoplist=shoplist, amount=amount)
            ol.save()

            try:
                cl = Customer.objects.get(openid=openid)
            except Exception as e:
                cl = None

            if cl:
                cl.account = cl.account + 1
                cl.money = cl.money + price
                cl.save()

            resp = '''{"code":0,"msg":"\u4e0b\u5355\u6210\u529f\uff0c\u901a\u8fc7\u201c\u6211\u7684\u8ba2\u5355\u201d\u67e5\u770b~","data":{"cart_id":"040220357129","amount":%d,"status":1,"pay_mode":"%s"}}''' %(amount, pay_type)
        except Exception as e:
            resp = e
            print "Exception:", e
    return HttpResponse(resp)

#/microfront/orders/date
def order_querydate(request):
    orders = Order.objects.all()
    total_turnover = orders.aggregate(Sum('price'))
    if request.GET.has_key('cdate'):
        try:
            cdate = request.GET['cdate']
            value = datetime.datetime.strptime(cdate, '%Y-%m-%d')
            orders = Order.objects.filter(order_time__range=(
                           datetime.datetime.combine(value, datetime.time.min),
                           datetime.datetime.combine(value, datetime.time.max))).order_by('-order_time')
            if None == orders:
                turnover = {'price__sum':0}
            else:
                turnover = orders.aggregate(Sum('price'))
        except Exception as e:
            timestr = time.strftime('%Y-%m-%d',time.localtime(time.time()))
            value = datetime.datetime.strptime(timestr, '%Y-%m-%d')
            orders = Order.objects.filter(order_time__range=(
                           datetime.datetime.combine(value, datetime.time.min),
                           datetime.datetime.combine(value, datetime.time.max)))
            turnover = orders.aggregate(Sum('price'))
    else:
        print '[===NOT EXIST CDATE!!!===]'
        turnover = total_turnover
    catalogs = Catalog.objects.all()
    return render_to_response('microfront/admin_manage.html', {'catalogs':catalogs, 'orders':orders, 'foods':get_food_list(), 'turnover':turnover, 'total_turnover':total_turnover})

#/microfront/orders/shop
def order_shoplist(request):
    catalogs = Catalog.objects.all()
    orders = Order.objects.all()
    return render_to_response('microfront/admin_manage.html', {'catalogs':catalogs, 'orders':orders, 'foods':get_food_list()})

#/microfront/orders/date
def order_save(request):
    resp = {"code":0}
    try:
        id = request.POST['order_id']
        status = request.POST['order_status']
        info = request.POST['order_info']
        addr = request.POST['order_addr']
        name, phone = info.split('/')
    except Exception as e:
        print e

    try:
        ol = Order.objects.get(id=id)
    except Order.DoesNotExist:
        ol = None
        print id, " order not exist."

    if ol:
        ol.order_status = status
        ol.name = name
        ol.phone = phone
        ol.address = addr
        ol.save()
    else:
        resp = "Order %s not exist." %(id)

    return HttpResponse(resp)

#/microfront/orders/del
def order_del(request):
    resp = {"code":0}
    try:
        id = request.POST['order_id']
    except Exception as e:
        print e

    try:
        ol = Order.objects.get(id=id)
    except Order.DoesNotExist:
        ol = None
        print id, " order not exist."

    if ol:
        ol.delete()
    else:
        resp = "Order %s not exist." %(id)

    return HttpResponse(resp)

#/microfront/foods/del
def food_del(request):
    resp = {"code":0}
    try:
        id = request.POST['food_id']
    except Exception as e:
        print e

    try:
        ml = Menu.objects.get(id=id)
    except Menu.DoesNotExist:
        ml = None
        print id, " menu not exist."

    if ml:
        ml.delete()
    else:
        resp = "Menu %s not exist." %(id)

    return HttpResponse(resp)

#/microfront/foods/del
def food_srch(request):
    try:
        if request.POST.has_key('name'):
            keyword = request.POST['name']
        else:
            keyword = ''

        if request.POST.has_key('sstaus'):
            status = request.POST['sstaus']
            print "status", status
            if '' == status:
                status = [0, 1, 2]
            else:
                status = [int(status)]
        else:
            status = [0, 1, 2]
            
        if request.POST.has_key('sgenre'):
            sgenre = request.POST['sgenre']
            print "sgenre", sgenre 
            if '' == sgenre:
                sgenre = [0, 1, 2, 3]
            else:
                sgenre = [int(sgenre)]
        else:
            sgenre = [0, 1, 2, 3]

        if request.POST.has_key('scatalog'):
            scatalog = request.POST['scatalog']
            print "scatalog", scatalog
            if '' == scatalog:
                scatalog = range(100)
            else:
                scatalog = [int(scatalog)]
        else:
            scatalog = range(100)
    except Exception as e:
        print 'foodsrch params query ', e
    
    try:
        if '' == keyword:
            foods = Menu.objects.filter(Q(status__in=status)&Q(genre__in=sgenre)&Q(catalog_id__in=scatalog))
        else:
            foods = Menu.objects.filter(Q(name__contains=keyword)&Q(status__in=status)&Q(genre__in=sgenre)&Q(catalog_id__in=scatalog))
        #foods = Menu.objects.get(id=12)
        #foods = Menu.objects.all()
    except Menu.DoesNotExist:
        foods = None
        print " has no such good."
    except Exception as e:
        foods = None
        print 'foods query', e

    if foods:
        data = serializers.serialize('json', foods)

        #if 1 >= foods.count():
        #    data = serializers.serialize('json', [foods])
        #else:
        #    data = serializers.serialize('json', foods)
        return HttpResponse(data)
    else:
        print "foods is none."
        return HttpResponse({'food_srch':''})

# /microfront/catalog/del
def cata_del(request):
    resp = {"code":0}
    try:
        id = request.POST['catalog_id']
    except Exception as e:
        print e

    try:
        cl = Catalog.objects.get(id=id)
    except Catalog.DoesNotExist:
        cl = None
        print id, " catalog not exist."

    if cl:
        cl.delete()
    else:
        resp = "Catalog %s not exist." %(id)

    return HttpResponse(resp)

# /microfront/catalog/save
def cata_save(request):
    resp = {"code":0}
    try:
        id = request.POST['catalog_id']
        sort = request.POST['catalog_sort']
        sts = request.POST['catalog_sts']
        name = request.POST['catalog_name']
        print "Catalog save: ", id, sort, sts
    except Exception as e:
        print "Catalog save", e

    try:
        cl = Catalog.objects.get(id=id)
    except Catalog.DoesNotExist:
        cl = None
        print id, " catalog not exist."

    if cl:
        cl.sort = sort
        cl.status = sts
        cl.name = name
        cl.save()
    else:
        resp = "Catalog %s not exist." %(id)
    return HttpResponse(resp)

# /microfront/dladdr/save
def dladdr_save(request):
    resp = {"code":0}
    try:
        id = request.POST['dladdr_id']
        area = request.POST['area']
    except Exception as e:
        print "Dladdr save", e

    try:
        dl = Dladdr.objects.get(id=id)
    except Dladdr.DoesNotExist:
        dl = None
        print id, " dladdr not exist."

    if dl:
        dl.area = area
        dl.save()
    else:
        resp = "Dladdr %s not exist." %(id)
    return HttpResponse(resp)


# /microfront/dladdr/del
def dladdr_del(request):
    resp = {"code":0}
    try:
        id = request.POST['dladdr_id']
    except Exception as e:
        print "Dladdr save", e

    try:
        dl = Dladdr.objects.get(id=id)
    except Dladdr.DoesNotExist:
        dl = None
        print id, " dladdr not exist."

    if dl:
        dl.delete()
    else:
        resp = "Dladdr %s not exist." %(id)
    return HttpResponse(resp)


# 
def get_paytype(type):
    stype = u'货到付款'
    if 1 == type:
        stype=u'支付宝方式'
    return stype

def get_dltime(dl):
    dltime = '11:00:00-14:30:00';
    if 65 == dl:
        dltime = '15:30:00-18:00:00'
    if 5 == dl:
        dltime = '19:30:00-21:00:00'
    return dltime


#/microfront/orders/export
def order_export(request):
    filename=time.strftime('%Y%m%d%H%M%S', time.localtime())+".xlsx"

    workbook = xlsxwriter.Workbook(filename)
    worksheet = workbook.add_worksheet()
    worksheet.set_column('A:M', 20)
    bold = workbook.add_format({'bold': True})

    str = ['', u'订单号',  u'注册会员卡号', u'收货人/手机',  u'用户住址', u'总价', u'商品数量', u'下单时间', u'配送时间', u'备注信息', u'支付方式', u'所购产品', u'订单状态']
    ll = ['', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L']
    ii = 1
    while ii <= 12:
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
        str=order.name+"/"+order.phone
        worksheet.write(loc, str)
        loc = "D%d" % line
        worksheet.write(loc, order.address)
        loc = "E%d" % line
        worksheet.write(loc, order.price)
        loc = "F%d" % line
        worksheet.write(loc, order.amount)
        loc = "G%d" % line
        worksheet.write(loc, order.order_time, format)
        loc = "H%d" % line
        str = get_dltime(int(order.delivery_time))
        worksheet.write(loc, str)
        loc = "I%d" % line
        worksheet.write(loc, order.remark)
        loc = "J%d" % line
        str = get_paytype(int(order.pay_type))
        worksheet.write(loc, str)
        loc = "K%d" % line
        worksheet.write(loc, order.shoplist)
        loc = "L%d" % line
        worksheet.write(loc, order.order_status)
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
    #print 'register: ', request
    if request.POST.has_key('username'):
        try:
            p = Customer.objects.get(openid=open_id)
            print 'exist user: ',p
        except Customer.DoesNotExist:
            p = None
            print open_id, ' not exist.'

        try:
            phone = request.POST['username']
            name = request.POST['name']
            print "phone[%s] name[%s]" %(phone, name)
            rtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            if p:
                p.name = name
                p.telphone = phone
                p.save()
            else:
                cl = Customer(openid=open_id, name=name, telphone=phone, reg_date=str(rtime), modify_date=str(rtime))
                cl.save()
            #resp = u'''{"customer":"id":"6662","open_id":"%s","account":"8449640","city":"","area":"","money":0},"code":0,"msg":"注册成功，并且已经登陆"}''' %(open_id)
            resp = u'''{"customer":{"id":"5352","open_id":"%s","account":"7709535","city":"","area":"","money":0},"code":0,"msg":"注册成功，并且已经登陆"}''' % (open_id)
        except Exception as e:
            resp = e
            print e
    print resp
    return HttpResponse(resp)

#/microfront/home/login
def login(request, open_id):
    resp = u'''{"code":0, "msg":"登录成功"}'''
    print resp
    return HttpResponse(resp)

#/microfront/users/save
def user_save(request):
    resp = {"code":0}
    try:
        post = request.POST
        id = post['id']
        if post.has_key('name'):
            name = post['name']
        else:
            name = None

        if post.has_key('phone'):
            phone = post['phone']
        else:
            phone = None

        if post.has_key('money'):
            money = post['money']
        else:
            money = None
    except Exception as e:
        print e

    try:
        cl = Customer.objects.get(id=id)
    except Order.DoesNotExist:
        cl = None
        print id, " customer not exist."

    if cl:
        if name:
            cl.name = name
        if phone:
            cl.telphone = phone
        if money:
            mny = float(money)
            cl.money = mny
        cl.save()
    else:
        resp = "Customer %s not exist." %(id)

    return HttpResponse(resp)

#/microfront/users/del
def user_del(request):
    resp = {"code":0}
    try:
        id = request.POST['id']
    except Exception as e:
        print e

    try:
        cl = Customer.objects.get(id=id)
    except Customer.DoesNotExist:
        cl = None
        print id, " order not exist."

    if cl:
        cl.delete()
    else:
        resp = "Customer %s not exist." %(id)

    return HttpResponse(resp)

#/microfront/users/query
def user_query(request):
    resp = '''{"cnt":0}'''
    try:
        keyword = request.POST['keyword']
    except Exception as e:
        print e
    try:
        cls = Customer.objects.filter(Q(name__contains=keyword)|Q(addr__contains=keyword))
    except Customer.DoesNotExist:
        cls = None
        print keyword, " has no such users."
    except Exception as e:
        print e

    cnt = cls.count()
    resp = '''{"cnt":%d}''' % cnt
    str = ""
    if 0 < cnt:
        ii = 0
        for cl in cls:
            if 0 != ii:
                str = str + ","
            str = str + '''{"id":%d, "openid":"%s", "name":"%s", "phone":"%s", "money":"%f"}''' %(cl.id, cl.openid, cl.name, cl.telphone, cl.money)
            ii = ii + 1
    resp = '''{"cnt":%d, "user":[%s]}''' % (cnt, str)
    print resp
    return HttpResponse(resp)

#/microfront/addr
def add_addr(request):
    resp = 999
    try:
        area = request.POST['area']
        dl = Dladdr(area=area)
        dl.save()
        print '====add addr id: ', dl.id
        resp = dl.id
    except Exception as e:
        print e
    return HttpResponse(resp)

#/microfront/dltime/add
def add_dltime(request):
    resp = 0
    try:
        begin_time = request.POST['begin_time']
        end_time = request.POST['end_time']
        dl = Dltime(begin_time=begin_time, end_time=end_time)
        dl.save()
        resp = dl.id
    except Exception as e:
        print e
    return HttpResponse(resp)

#/microfront/dltime/save
def save_dltime(request):
    resp = 0
    try:
        id = request.POST['dltime_id']
        dltime = request.POST['dltime_info']
        print id, dltime
        dlinfo = dltime.split('-')
        begin_time = dlinfo[0]
        end_time = dlinfo[-1]
        print begin_time, end_time
    except Exception as e:
        print "dltime save", e
    
    try:
        dl = Dltime.objects.get(id=id)
    except Dltime.DoesNotExist:
        dl = None
        print id, " dltime not exist."

    if dl:
        dl.begin_time = begin_time
        dl.end_time = end_time
        dl.save()
    else:
        resp = "Dltime %s not exist" %(id)
    return HttpResponse(resp)

#/microfront/otherset/save
def save_otherset(request):    
    resp = 0
    try:
        dx_mobile = request.POST['dx_mobile']
        kf_phone = request.POST['kf_phone']
        tip_content = request.POST['tip_content']
        distribution_range = request.POST['distribution_range']
        freight = float(request.POST['freight'])
    except Exception as e:
        print e

    try:
        other = Otherset.objects.get(id=1)
        other.dx_mobile = dx_mobile
        other.kf_phone = kf_phone 
        other.tip_content = tip_content 
        other.distribution_range = distribution_range
        other.freight = freight 
        other.save()
    except Otherset.DoesNotExist:
        other = Otherset(dx_mobile=dx_mobile, kf_phone=kf_phone, tip_content=tip_content, distribution_range=distribution_range, freight=freight)
        other.save()
        
    return HttpResponse(resp)

#/microfront/ingredit/save
def ingredit_save(request):
    code = 0
    try:
        goodsid = int(request.POST['goods_id'])
        goodsname = request.POST['goods_name']
        type = int(request.POST['type'])
        names = request.POST['names']
        quantitys = request.POST['quantitys']
        units = request.POST['units']
    except Exception as e:
        print e

    if 0 == type:
        type = 1

    if 0 == goodsid:
        # search goods by name
        goods = Menu.objects.get(name=goodsname)
        try:
            goodsid = goods.id
        except NameError:
            print "get none goods by name:", goodsname
    else:
        try:
            ingredts = Ingredient.objects.filter(Q(menu_id=goodsid)&Q(mclass=type))
            ingredts.delete()
        except Exception as e:
            print "Ingredients query exception: ", e

    namel = names.split('|')
    quntyl = quantitys.split('|')
    unitl = units.split('|')

    for ii in range(len(namel)):
        name = namel[ii]
        qunty = quntyl[ii]
        unit = unitl[ii]
        ingredt = Ingredient(menu_id = goodsid, name = name, mclass = type, quantity=qunty, unit=unit)
        ingredt.save()
    return HttpResponse(code)

#/microfront/ingredit/query
def ingredit_query(request):
    code = 0
    try:
        goodsid = int(request.POST['goods_id'])
        type = int(request.POST['type'])
    except Exception as e:
        print e

    try:
        ingredts = Ingredient.objects.filter(Q(menu_id=goodsid)&Q(mclass=type))
    except Ingredient.DoesNotExist:
        print "Not exist such ingredts."
    except Exception as e:
        print "Ingredients query exception: ", e

    if 'ingredts' in dir():
        data = serializers.serialize('json', ingredts)
        return HttpResponse(data)
    else:
        return HttpResponse({"ingredt_query":""})


#/microfront/dltime/del
def del_dltime(request):
    resp = 0
    try:
        id = request.POST['dltime_id']
    except Exception as e:
        print e
    
    try:
        dl = Dltime.objects.get(id=id)
    except Dltime.DoesNotExist:
        dl = None
        print id, " dltime not exist."

    if dl:
        dl.delete()
    else:
        resp = "Dltime %s not exist" %(id)
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
            city = request.POST['Customer[city]']
            area = request.POST['Customer[area]']
            address = request.POST['Customer[address]']
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
    #text=open('micromall/'+fname+'.jpg','rb').read()
    text=open(fname+'.jpg','rb').read()
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

def htm_resource(request,fname):
    text=open('microfront/skin/'+fname+'.htm','rb').read()
    return HttpResponse(text, mimetype="text/html")

def admin_manage(request):
    catalogs = dbcatalog.select().order_by(dbcatalog.c.sort).execute()
    ll = []
    for row in catalogs:
        ll.append(row[1])
    return render_to_response('microfront/admin_manage.html', {'catalogs':ll})

def admin(request):
    base='micromall/micromall/files/upfiles/' + time.strftime('%Y%m%d', time.localtime()) + "/"
    if not os.path.exists(base):
        print 'create path: ', base
        os.makedirs(base)

    username = 'qi_admin'
    print "+++++++++++++++++++++++++++++++", request
    if request.POST.has_key('cataname'):
        print 'cata: ', request.POST
        cataname = request.POST['cataname']
        sort = request.POST['cata_sort']
        status = u'off'
        if request.POST.has_key('cata_status'):
            status = request.POST['cata_status']
        add_catalog_db(cataname, sort, status);
        return HttpResponseRedirect('/microfront/admin/')

    if request.POST.has_key('foodid'):
        print "menu_add === ", request

        if request.FILES.has_key('pic'):
            pic=request.FILES['pic']
            extension=get_extension(pic)
            if extension:  #without pic file
                print pic,'uploaded'

                num = int(time.time()*1000)
                fname=str(num)+extension
                fullname=base+fname
                detail_fullname = base + str(num + 1) + extension
                print "fullname: ", fullname
                #write cover pic file
                fp=open(fullname,'wb')
                fp.write(pic.read())
                fp.close()
        else:
            fullname = ''

        #write detail pic file
        if request.FILES.has_key('detail_pic'):
            detail_pic=request.FILES['detail_pic']
            extension=get_extension(detail_pic)
            fp = open(detail_fullname, 'wb')
            fp.write(detail_pic.read())
            fp.close()
        else:
            detail_fullname = ''

        foodname=request.POST['foodname']
 
        try:
            foodprice=float(request.POST['origprice'])
            sprice=float(request.POST['sprice'])
        except:
            error ='数据提交发生错误:价格不是有效数字<br/><a href="/admin/'+username+'">返回</a>'
            return HttpResponse(error)

        foodstatus = int(request.POST['food_status'])
        foodgenre = int(request.POST['food_genre'])
        category=int(request.POST['category'])
        print "menu genre and status ======", foodgenre, foodstatus
        introduce=request.POST['introduce']#.replace('\n','')
        #introduce = introduce + "\n"
        print foodname,foodprice,category,introduce, foodgenre, foodstatus

        total = request.POST['amount']
        foodid = int(request.POST['foodid'])

        if 0 == foodid:
            menu = Menu(orgid=1, sales=0, name=foodname, cover_url=fullname[19:], detail_url=detail_fullname[10:], old_price=foodprice, price=sprice, catalog_id=category, status=foodstatus, genre=foodgenre, total=total, introduce='')
            menu.save()
            add_menu_json(menu.id, detail_fullname[19:], fullname[20:], foodname, category, foodprice, sprice, introduce)
        else:
            #TODO: need to update info; 

            menu = Menu.objects.get(id=foodid)
            menu.name = foodname
            if 19 < len(fullname):
                menu.cover_url = fullname[19:]
            if 10 < len(detail_fullname):
                menu.detail_url = detail_fullname[10:]
            menu.old_price = foodprice
            menu.price = sprice
            menu.catalog_id = category
            menu.total = total
            menu.introduce = ''
            menu.status=foodstatus
            menu.genre=foodgenre
            menu.save()
            print "******************update food content: ", introduce
            #add_menu_json(foodid, detail_fullname[19:], fullname[20:], foodname, category, foodprice, sprice, introduce, 1)

        
        return HttpResponseRedirect('/microfront/admin/')

    catalogs = Catalog.objects.all()
    print "menu: ", get_food_list()
    orders = Order.objects.order_by('-order_time')
    dladdrs = Dladdr.objects.all()
    dltimes = Dltime.objects.all()
    users = Customer.objects.all()
    turnover = Order.objects.aggregate(Sum('price'))
    othersets = Otherset.objects.all()

    print "turnover", turnover
    print "otherset", othersets
    return render_to_response('microfront/admin_manage.html', {'g_catajson': get_gcatajson(), 'dladdrs':dladdrs, 'users':users, 'dltimes':dltimes, 'catalogs':catalogs, 'orders':orders, 'foods':get_food_list(), 'turnover':turnover, 'total_turnover':turnover, 'othersets':othersets})

def add_menu_json(id, detail_url, cover_url, name, catalog_id, oprice, price, introduce, type=0):
    reload(sys)
    sys.setdefaultencoding('utf-8')
    menujson = u'''{"rt_obj":{"code":0,"data":{"Goods":{"id":"%d","org_id": "1","detail_url": "%s","cover_url": "%s","name": "%s","catalog_id":"%s","old_price": "%f","price": "%f","sales":"0","total": "0","genre": "1","level": "20","content": "%s","status": "1","servings": "1","stime": "2014-03-18 14:38:40"}}}}''' %(id, detail_url, cover_url, name, catalog_id, oprice, price, introduce.replace('\r\n', '').replace('"', '\\\"'))
    menujson = json.loads(menujson)
    menujson = json.dumps(menujson)
     
    jsonfn = 'microfront/microfront/items/' + str(id) + '.json'
    print "Write menu json file: ", jsonfn
    print "Menujson[%s]" % (menujson)
    fd = open(jsonfn, 'wb') 
    fd.write(menujson)
    fd.close()

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

# Get catalog json
def get_catajson():
    strjson='''['''
    g_catajson = '''{'''
    idx = 0
    allcatalogs = Catalog.objects.order_by('sort')
    catalogs = allcatalogs[:4]
    for catalog in catalogs:
        if 1 == catalog.status:
            if 0 == idx:
                str = u'''{"Catalog":{"id":"%d","name":"%s","url":"url","sort":"%d","status":"%d","org_id":"1"}}''' %(catalog.id, catalog.name, catalog.sort, catalog.status)
                str2 = u'''"%d":"%s"''' %(catalog.id, catalog.name)
            else:
                str = u''',{"Catalog":{"id":"%d","name":"%s","url":"url","sort":"%d","status":"%d","org_id":"1"}}''' %(catalog.id, catalog.name, catalog.sort, catalog.status)
                str2 = u''',"%d":"%s"''' %(catalog.id, catalog.name)
            strjson = strjson + str
            g_catajson = g_catajson + str2
            idx = idx + 1
    strjson = strjson + "]"
    g_catajson = g_catajson + "}"
    strjson = json.loads(strjson)
    strjson = json.dumps(strjson)
    g_catajson = json.loads(g_catajson)
    g_catajson = json.dumps(g_catajson)
    print strjson, g_catajson
    return strjson, g_catajson

# Get catalog json
def get_gcatajson():
    g_catajson = '''{'''
    idx = 0
    catalogs = Catalog.objects.order_by('sort')
    for catalog in catalogs:
        if 0 == idx:
            str2 = u'''"%d":"%s"''' %(catalog.id, catalog.name)
        else:
            str2 = u''',"%d":"%s"''' %(catalog.id, catalog.name)
        g_catajson = g_catajson + str2
        idx = idx + 1
    g_catajson = g_catajson + "}"
    g_catajson = json.loads(g_catajson)
    g_catajson = json.dumps(g_catajson)
    print  g_catajson
    return g_catajson

# Get catalog json
def get_morecatajson():
    strjson='''['''
    g_catajson = '''{'''
    idx = 0
    allcatalogs = Catalog.objects.order_by('sort')
    catalogs = allcatalogs[4:]
    if 0 >= len(catalogs):
        mjson = {}
        return mjson
    for catalog in catalogs:
        if 1 == catalog.status:
            if 0 == idx:
                str = u'''{"Catalog":{"id":"%d","name":"%s","url":"url","sort":"%d","status":"%d","org_id":"1"}}''' %(catalog.id, catalog.name, catalog.sort, catalog.status)
            else:
                str = u''',{"Catalog":{"id":"%d","name":"%s","url":"url","sort":"%d","status":"%d","org_id":"1"}}''' %(catalog.id, catalog.name, catalog.sort, catalog.status)
            strjson = strjson + str
            idx = idx + 1
    strjson = strjson + "]"
    strjson = json.loads(strjson)
    strjson = json.dumps(strjson)
    print strjson
    return strjson

# Get menu info(include price, name) json
def get_menuinfo():
    strjson=''
    idx = 0
    try:
        foods = Menu.objects.order_by('id')
        for food in foods:
            foodid = food.id
            name = food.name
            price = food.price
            if 0 == idx:
                infostr = u'''{"%d":{"price":"%f", "name":"%s"}''' %(foodid, price, name)
                strjson = strjson + infostr
            else:
                infostr = u''',"%d":{"price":"%f", "name":"%s"}''' %(foodid, price, name)
                strjson = strjson + infostr
            idx = idx + 1
        strjson = strjson + "}"
    except Exception as e:
        print 'exception..........', e

    print '''===menuinfo json===: %s''' %(strjson)
    strjson = json.loads(strjson)
    #strjson = json.dumps(strjson)
    return strjson

# Get menu json
def get_menujson():
    strjson=''
    idx = 0
    cidx = 0
    try:
        cataids = Catalog.objects.order_by('id').values('id').distinct()
        for cataid in cataids:
            cid = cataid['id']
            menus = Menu.objects.filter(catalog_id=cid)
            cnt = menus.count();
            if 0 < cnt:
                #The first catalog add prefix '{'
                if 0 == cidx:
                    strjson = strjson + '{'
                else: #The normal catalog add prefix ','
                    strjson = strjson + ','

                idx = 0
                for menu in menus:
                    if 0 == idx:
                        str = '''"%d":[{"Goods":{"id":"%d","org_id":"1","detail_url":"%s","cover_url":"%s","name":"%s","catalog_id":"%d","old_price":"%f","price":"%f","sales":"0","total":"0","genre":"1","level":"20","content":"%s","status":"1","servings":"1","stime":"2014-03-18 15:45:30"}}''' %(cid, menu.id, menu.detail_url, menu.cover_url, menu.name, menu.catalog_id, menu.old_price, menu.price, menu.introduce)
                    else:
                        str = ''',{"Goods":{"id":"%d","org_id":"1","detail_url":"%s","cover_url":"%s","name":"%s","catalog_id":"%d","old_price":"%f","price":"%f","sales":"0","total":"0","genre":"1","level":"20","content":"%s","status":"1","servings":"1","stime":"2014-03-18 15:45:30"}}''' %(menu.id, menu.detail_url, menu.cover_url, menu.name, menu.catalog_id, menu.old_price, menu.price, menu.introduce)
                    strjson = strjson + str
                    idx = idx + 1
                # all menu scaned, add ']'
                strjson = strjson + "]"
                cidx = cidx + 1

        # all catalog scaned, add '}'
        strjson = strjson + '}'

        print "strjson===", strjson

    except Exception as e:
        print 'exception..........', e
    print '''===menujson===: %s''' %(strjson)
    strjson = json.loads(strjson)
    strjson = json.dumps(strjson)
    return strjson

# Get organization json
def get_orgjson():
    idx = 0
    org = Otherset.objects.get(id=1)
    strjson = u'''{"Organization":{"id":"1","name":"爱好食","kf_phone":"%s","tip_content":"%s","distribution_range":"%s","freight":"%f"}}''' %(org.kf_phone, org.tip_content, org.distribution_range, org.freight)
    print "org json:", strjson
    strjson = json.loads(strjson)
    strjson = json.dumps(strjson)
    print strjson
    return strjson    
    
# Get dltime json
def get_dltimejson():
    strjson='''['''
    idx = 0
    dltimes = Dltime.objects.all()
    for dltime in dltimes:
        if 0 == idx:
            str = u'''{"DeliveryTime":{"id":"%d","start_time":"%s","end_time":"%s", "org_id":"1"}}''' %(dltime.id, dltime.begin_time, dltime.end_time)
        else:
            str = u''',{"DeliveryTime":{"id":"%d","start_time":"%s","end_time":"%s", "org_id":"1"}}''' %(dltime.id, dltime.begin_time, dltime.end_time)
        strjson = strjson + str
        idx = idx + 1
    strjson = strjson + "]"
    strjson = json.loads(strjson)
    strjson = json.dumps(strjson)
    print strjson
    return strjson
