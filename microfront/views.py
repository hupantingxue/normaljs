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
from django.views.decorators.csrf import csrf_exempt

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
import Image
from PIL import ImageFile
import shutil
import redis
from conf import *

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

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)

# Create your views here.
#@csrf_protect
def index(request):
    if request.method == 'GET':
        qd = request.GET
    elif request.method == 'POST':
        qd = request.POST

    code = qd.__getitem__('code')
    try:
        slctidx = qd.__getitem__('idx') 
    except Exception as e:
        slctidx = 1
    template = loader.get_template('microfront/index.html')
    context = Context({
        'cur_usr': code,
        'slctidx': slctidx,
    })

    try:
        cl = Customer.objects.get(openid=code)
        status = "CUSTOMER"
    except Exception as e:
        cl = None
        status = "NEW_USER"
        print e

    return render_to_response('microfront/index.html', {'cur_usr':code, 'slctidx':slctidx, 'cusr':cl, 'usr_status':status, 'catalog_json':get_catajson()[0], 'morecatalog_json':get_morecatajson(), 'org_json':get_orgjson(), 'dltime_json':get_dltimejson(), 'menu_json':get_menujson()})

#/microfront/zan/
def zan_add(request):
    resp = 0
    itemid = 0
    if request.POST.has_key('zan'):
        try:
            post = request.POST
            item = post['zan']
            itemid = int(item[5:])
            #print "itemid: ", itemid
        except Exception as e:
            print "zan_add: ", e

        try:
            ml = Menu.objects.get(id=itemid)
            ml.zan_num = ml.zan_num + 1
            ml.save()
        except Menu.DoesNotExist:
            ml = None
            #print itemid, " menu not exist."
    return HttpResponse(resp)

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
                #prex = u'科技园'
                prex = u'宝安区'
            if 383 == narea:
                #prex = u'腾讯大厦'
                prex = u'南山区'
            if 601 == narea:
                prex = u'白石洲地铁B出口'
            if 700 == narea:
                prex = u'测试'
            address = u'深圳市' + prex + post['address']
            rtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

            price = 0.0
            amount = 0
            count=[0]*100
            goods=[0]*100

            good_info = get_menuinfo()
            #print json.dumps(good_info)

            for key in post:
                if 'count' in key:
                    idx = int(key[5])
                    #print 'count idx: ', idx
                    count[idx] = int(post[key])
                    #print key, int(key[5])
                if 'goods' in key:
                    idx = int(key[5])
                    goods[idx] = post[key]
                    #print 'goods idx: ', idx
                    #print key, type(key)
                #print key, post[key]
            #print count, goods

            #count amount
            amount = sum(count)

            #count price
            price = 0
            ii = 0
            shoplist = ""
            while ii < 100:
                if 0 >= count[ii] or 0 >= goods[ii]:
                    break
                price = price + count[ii] * float(good_info.get(goods[ii]).get('price', 14.0))
                #print goods[ii], type(goods[ii]), good_name.get(goods[ii], u"好食"), type(good_name.get(goods[ii], u"好食").encode())
                #shoplist = shoplist + u"%s %d 份;\n" %(good_name.get(goods[ii], u"好食"), count[ii])
                shoplist = shoplist + u"%s %d 份;\n" %(good_info.get(goods[ii]).get('name', u'好食'), count[ii])

                try:
                    order_goodsid = int(goods[ii])
                    order_goods = Menu.objects.get(id=order_goodsid)
                    order_goods.sales = order_goods.sales + count[ii]
                    order_goods.save()
                except Excpetion as e:
                    print 'order add menu id %d not found' %(order_goodsid)

                ii = ii + 1
            #print shoplist
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

            rdate = time.strftime("%Y%m%d", time.localtime())
            cart_id = "%s%04d" %(rdate, ol.id)

            ########################################################################
            #  write good items info to json file(begin)
            ########################################################################
            ii = 0
            rt_obj = {"data":{"orders":[], "orderItems":{}}}
            rt_obj['data']['orderItems'][cart_id]=[]
            while ii < 100:
                if 0 >= count[ii] or 0 >= goods[ii]:
                    break
                order_jsitem = u'''{"OrderGoods": {"order_id": "%s","goods_id": "%s","goods_price": "%f","goods_num": "%d","goods_name": "%s","customers": "2"}}''' %(cart_id, goods[ii], float(good_info.get(goods[ii]).get('price', 14.0)), count[ii], good_info.get(goods[ii]).get('name', u'好食'))
                #print '%d order_jsitem [%s]' %(ii, order_jsitem)
                order_jsitem = json.loads(order_jsitem)
                rt_obj['data']['orderItems'][cart_id].append(order_jsitem)
                ii = ii + 1

            item_info = '''{"Order": {"id": "%s","org_id": "1","user_id": "%s","status": "1","order_time": "%s","order_date": "%s","order_money": "%s","pay_mode": "%s","delivery_status": "2","freight": "0.00"}}''' %(cart_id, openid, rtime, rdate, price, pay_type)
            item_info = json.loads(item_info)
            rt_obj["data"]["orders"].append(item_info)
            rt_obj = {"rt_obj":rt_obj}
            #print "===========================notice: ", repr(rt_obj)

            # copy order json file to history order json file
            curpath = os.path.dirname(os.path.abspath('.'))

            # json file and history order json file
            srcfn = curpath + '/normaljs/microfront/orders/'+openid+'/0.json'
            dstfn = curpath + '/normaljs/microfront/orders/'+openid+'/1.json'
            if os.path.exists(srcfn):
                shutil.copyfile(srcfn, dstfn)

            # write new order file
            write_order_json(openid, rt_obj)
            try:
                r.lpush(REDIS_QUEUE, openid)
            except Exception as e:
                r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)
                r.lpush(REDIS_QUEUE, openid)
            ########################################################################
            #  write good items info to json file(end)
            ########################################################################

            resp = '''{"code":0,"msg":"\u4e0b\u5355\u6210\u529f\uff0c\u901a\u8fc7\u201c\u6211\u7684\u8ba2\u5355\u201d\u67e5\u770b~","data":{"cart_id":"%s","amount":%d,"status":1,"pay_mode":"%s"}}''' %(cart_id, amount, pay_type)
        except Exception as e:
            resp = e
            print "Exception:", e
    return HttpResponse(resp)

#/microfront/orders/date
def order_querydate(request):
    orders = Order.objects.all().filter(~Q(order_status=4))
    total_turnover = orders.aggregate(Sum('price'))
    if request.GET.has_key('cdate'):
        try:
            cdate = request.GET['cdate']
            value = datetime.datetime.strptime(cdate, '%Y-%m-%d')
            orders = Order.objects.filter(order_time__range=(
                           datetime.datetime.combine(value, datetime.time.min),
                           datetime.datetime.combine(value, datetime.time.max))).filter(~Q(order_status=4)).order_by('-order_time')
            if None == orders:
                turnover = {'price__sum':0}
            else:
                turnover = orders.aggregate(Sum('price'))
        except Exception as e:
            timestr = time.strftime('%Y-%m-%d',time.localtime(time.time()))
            value = datetime.datetime.strptime(timestr, '%Y-%m-%d')
            orders = Order.objects.filter(order_time__range=(
                           datetime.datetime.combine(value, datetime.time.min),
                           datetime.datetime.combine(value, datetime.time.max))).filter(~Q(order_status=4))
            turnover = orders.aggregate(Sum('price'))
    else:
        #print '[===NOT EXIST CDATE!!!===]'
        turnover = total_turnover
    catalogs = Catalog.objects.all()
    return render_to_response('microfront/admin_manage.html', {'catalogs':catalogs, 'orders':orders, 'foods':get_food_list(), 'turnover':turnover, 'total_turnover':total_turnover})

#/microfront/orders/query
def order_query(request):
    try:
        odate = request.POST['odate']
        odate = odate.strip()
        if 'all' != odate:
            value = datetime.datetime.strptime(odate, '%Y-%m-%d')
            orders = Order.objects.filter(order_time__range=(
                       datetime.datetime.combine(value, datetime.time.min),
                       datetime.datetime.combine(value, datetime.time.max))).order_by('order_time')
        else:
            orders = Order.objects.all()
    except Order.DoesNotExist:
        print "Not exist such orders."
    except Exception as e:
        #print "Orders query exception: ", e
        odate = time.strftime("%Y-%m-%d", time.localtime())
        value = datetime.datetime.strptime(odate, '%Y-%m-%d')
        orders = Order.objects.filter(order_time__range=(
                       datetime.datetime.combine(value, datetime.time.min),
                       datetime.datetime.combine(value, datetime.time.max))).order_by('order_time')

    if ('orders' in dir()) and (0 < orders.count()):
        data = serializers.serialize('json', orders)
        return HttpResponse(data)
    else:
        return HttpResponse({"order_query":""})


#/microfront/orders/shop
def order_shoplist(request):
    shopdict = {}
    try:
        odate = request.POST['odate']
        value = datetime.datetime.strptime(odate, '%Y-%m-%d')
        orders = Order.objects.filter(order_time__range=(
                       datetime.datetime.combine(value, datetime.time.min),
                       datetime.datetime.combine(value, datetime.time.max))).filter(~Q(order_status=4)).order_by('order_time')
    except Order.DoesNotExist:
        print "Not exist such orders."
    except Exception as e:
        print "Orders query exception: ", e
        odate = time.strftime("%Y-%m-%d", time.localtime())
        value = datetime.datetime.strptime(odate, '%Y-%m-%d')
        orders = Order.objects.filter(order_time__range=(
                       datetime.datetime.combine(value, datetime.time.min),
                       datetime.datetime.combine(value, datetime.time.max))).filter(~Q(order_status=4)).order_by('order_time')

    if ('orders' in dir()) and (0 < orders.count()):
        for order in orders:
            shopstr = order.shoplist
            shopstr = shopstr.strip('\n')
            shopset = shopstr.split(';')
            for shop in shopset:
                try:
                    shop = shop.strip('\n')
                    try:
                        name, cnt, unit= shop.split()
                    except Exception as e:
                        name1, name2, cnt, unit= shop.split()
                        name = name1 + name2
                    cnt = int(cnt)
                    if name in shopdict:
                        shopdict[name] = shopdict[name] + cnt
                    else:
                        shopdict[name] = cnt
                except Exception as e:
                    print e
        #data = serializers.serialize('json', shopdict)
        shopdictstr = json.dumps(shopdict)
        #print 'shopdict: ', shopdictstr
        return HttpResponse(shopdictstr, mimetype = "application/json")
    else:
        return HttpResponse({"shopdict":""}, mimetype = "application/json")

#/microfront/orders/purchase
def order_purchase(request):
    shopdict = {}
    ingredt_dict = {}
    try:
        odate = request.POST['odate']
        value = datetime.datetime.strptime(odate, '%Y-%m-%d')
        orders = Order.objects.filter(order_time__range=(
                       datetime.datetime.combine(value, datetime.time.min),
                       datetime.datetime.combine(value, datetime.time.max))).filter(~Q(order_status=4)).order_by('order_time')
    except Order.DoesNotExist:
        print "Not exist such orders."
    except Exception as e:
        print "Orders query exception: ", e
        odate = time.strftime("%Y-%m-%d", time.localtime())
        value = datetime.datetime.strptime(odate, '%Y-%m-%d')
        orders = Order.objects.filter(order_time__range=(
                       datetime.datetime.combine(value, datetime.time.min),
                       datetime.datetime.combine(value, datetime.time.max))).filter(~Q(order_status=4)).order_by('order_time')

    if ('orders' in dir()) and (0 < orders.count()):
        for order in orders:
            shopstr = order.shoplist
            shopstr = shopstr.strip('\n')
            shopset = shopstr.split(';')
            for shop in shopset:
                try:
                    shop = shop.strip('\n')
                    try:
                        name, cnt, unit= shop.split()
                    except Exception as e:
                        name1, name2, cnt, unit= shop.split()
                        name = name1 + name2
                    cnt = int(cnt)
                    if name in shopdict:
                        shopdict[name] = shopdict[name] + cnt
                    else:
                        shopdict[name] = cnt
                except Exception as e:
                    print shop, e
        #data = serializers.serialize('json', shopdict)

        #get ingredit by menu name
        for name in shopdict:
            ingredts = Ingredient.objects.filter(menu_name=name);
            for ingredt in ingredts:
                if ingredt.name in ingredt_dict:
                    ingredt_dict[ingredt.name] = ingredt_dict[ingredt.name] + ingredt.quantity * shopdict[name]
                else:
                    ingredt_dict[ingredt.name] = ingredt.quantity * shopdict[name]

        ingredt_dictstr = json.dumps(ingredt_dict)
        #print 'ingredt dict: ', ingredt_dictstr 
        return HttpResponse(ingredt_dictstr, mimetype = "application/json")
    else:
        return HttpResponse({"ingredt_dict":""}, mimetype = "application/json")


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
        #print id, " order not exist."

    if ol:
        ol.order_status = status
        if u'已完成' == status:
            ol.delivery_status = 3
        elif u'已结束' == status:
            ol.delivery_status = 4
        ol.name = name
        ol.phone = phone
        ol.address = addr
        ol.save()
    else:
        resp = "Order %s not exist." %(id)
    try:
        r.lpush(REDIS_QUEUE, openid)
    except Exception as e:
        r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)
        r.lpush(REDIS_QUEUE, openid)

    return HttpResponse(resp)

def clear_orderdata(openid, shoplist, price):
    try:
        ul = Customer.objects.get(openid=openid)
        ul.account = ul.account - 1
        ul.money = ul.money - price
        ul.save()
    except Exception as e:
        print e

    try:
        shopdict = {}
        shopset = shoplist.split(';')
        for shop in shopset:
            if 1 >= len(shop):
                continue
            try:
                name, cnt, unit = shop.split()
                cnt = int(cnt)
            except Exception, e:
                name1, name2, cnt, unit = shop.split()
                cnt = int(cnt)
                name = name1

            if name in shopdict:
                shopdict[name] = cnt + shopdict[name]
            else:
                shopdict[name] = cnt

        for name in shopdict:
            shop_f = Menu.objects.filter(name__startswith=name)
            for shop in shop_f:
                shop.sales = shop.sales - long(shopdict[name])
                shop.save()

    except Exception as e:
        print e
    return ''

#/microfront/orders/del  for admin  cancel
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
        openid = ol.openid
        shoplist = ol.shoplist
        clear_orderdata(openid, shoplist, price)
        ol.delete()
    else:
        resp = "Order %s not exist." %(id)

    try:
        r.lpush(REDIS_QUEUE, openid)
    except Exception as e:
        r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)
        r.lpush(REDIS_QUEUE, openid)
    return HttpResponse(resp)

#/microfront/orders/delete for user order cancel
def order_cancel(request, order_id):
    resp = u'''{"code":0, "msg":"订单删除成功"}'''
    try:
        order_id = int(order_id[8:])
        id = order_id
    except Exception as e:
        print e

    try:
        ol = Order.objects.get(id=id)
    except Order.DoesNotExist:
        ol = None
        print id, " order not exist."

    if ol:
        openid = ol.openid
        shoplist = ol.shoplist
        price = ol.price
        clear_orderdata(openid, shoplist, price)

        #set order status
        ol.order_status = 4
        ol.save()

        #empty myorder json file: orders/0.json
        rt_obj = {"rt_obj":{"data":{"orders":[], "orderItems":{}}}}
        write_order_json(openid, rt_obj)

    else:
        resp = "Order %s not exist." %(id)
        resp = u'''{"code":0, "msg":"订单删除成功"}'''
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
            #print "sgenre", sgenre 
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
    try:
        odate = request.GET['odate']
        value = datetime.datetime.strptime(odate, '%Y-%m-%d')
    except Exception as e:
        print 'odate format error: ', e
        #odate = time.strftime('%Y-%m-%d', time.localtime())
        #value = datetime.datetime.strptime(odate, '%Y-%m-%d')
        value = None

    if value is None:
        orders = Order.objects.all()
    else:
        orders = Order.objects.filter(order_time__range=(
                    datetime.datetime.combine(value, datetime.time.min),
                    datetime.datetime.combine(value, datetime.time.max))).order_by('order_time')

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
        status = order.order_status
        if (type(1) == status) or (status.isdigit()):
            worksheet.write(loc, u'订单取消')
        else:
            worksheet.write(loc, status)
        print "order: ", order.id, order.openid, status.encode('utf-8'), type(status)
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
            sex = request.POST['sex']
            #print "phone[%s] name[%s]" %(phone, name)
            rtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            if p:
                p.name = name
                p.telphone = phone
                p.sex = sex
                p.save()
            else:
                cl = Customer(openid=open_id, name=name, telphone=phone, sex=sex, reg_date=str(rtime), modify_date=str(rtime))
                cl.save()
            #resp = u'''{"customer":"id":"6662","open_id":"%s","account":"8449640","city":"","area":"","money":0},"code":0,"msg":"注册成功，并且已经登陆"}''' %(open_id)
            resp = u'''{"customer":{"id":"5352","open_id":"%s","account":"7709535","city":"","area":"","money":0},"code":0,"msg":"注册成功，并且已经登陆"}''' % (open_id)
        except Exception as e:
            resp = e
            print e
    #print resp
    return HttpResponse(resp)

#/microfront/home/login
def login(request, open_id):
    resp = u'''{"code":0, "msg":"登录成功"}'''
    #print "%s", resp
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
            str = str + u'''{"id":%d, "sex":"%s", "area":"%s", "addr":"%s","reg_date":"%s", "openid":"%s", "name":"%s", "phone":"%s", "money":"%f", "account":"%d"}''' %(cl.id, cl.sex, cl.area, cl.addr, cl.reg_date, cl.openid, cl.name, cl.telphone, cl.money, cl.account)
            ii = ii + 1
    resp = u'''{"cnt":%d, "user":[%s]}''' % (cnt, str)
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

    igt_menuname = goodsname.replace(' ', '')
    for ii in range(len(namel)):
        name = namel[ii]
        qunty = quntyl[ii]
        unit = unitl[ii]
        ingredt = Ingredient(menu_id = goodsid, menu_name = igt_menuname, name = name, mclass = type, quantity=qunty, unit=unit)
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

#/microfront/ingredit/del
def ingredit_del(request):
    code = 0
    try:
        goodsid = int(request.POST['food_id'])
        type = int(request.POST['type'])
        name = request.POST['name']
    except Exception as e:
        print e

    try:
        ingredts = Ingredient.objects.filter(Q(menu_id=goodsid)&Q(mclass=type)&Q(name=name))
    except Ingredient.DoesNotExist:
        print "Not exist such ingredts."
    except Exception as e:
        print "Ingredients query exception: ", e

    if 'ingredts' in dir():
        ingredts[0].delete()
        return HttpResponse({"code":0})
    else:
        return HttpResponse({"code":-1})



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
            #print open_id, ' not exist.'
        try:
            name = request.POST['Customer[name]']
            phone = request.POST['Customer[phone]']
            city = request.POST['Customer[city]']
            area = request.POST['Customer[area]']
            address = request.POST['Customer[address]']
            remark = request.POST['Customer[remark]']
            rtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            #print "rtime: ", rtime
            if p:
                #print '%s has registered.' %(open_id)
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

    #print 'resp post customer data: ', resp
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

def orderjson_resource(request,fname):
    wechat_id = request.COOKIES.get("wechat_id")
    #print "cookie wechat_id: ", wechat_id, type(wechat_id)
    text=open('microfront/orders/'+wechat_id+"/"+fname+'.json','r+').read()
    return HttpResponse(text, mimetype = "application/json")

def admin_manage(request):
    catalogs = dbcatalog.select().order_by(dbcatalog.c.sort).execute()
    ll = []
    for row in catalogs:
        ll.append(row[1])
    return render_to_response('microfront/admin_manage.html', {'catalogs':ll})

def admin(request):
    base='micromall/micromall/files/upfiles/' + time.strftime('%Y%m%d', time.localtime()) + "/"
    if not os.path.exists(base):
        #print 'create path: ', base
        os.makedirs(base)

    username = 'qi_admin'
    #print "+++++++++++++++++++++++++++++++", request
    if request.POST.has_key('cataname'):
        #print 'cata: ', request.POST
        cataname = request.POST['cataname']
        sort = request.POST['cata_sort']
        status = u'off'
        if request.POST.has_key('cata_status'):
            status = request.POST['cata_status']
        add_catalog_db(cataname, sort, status);
        return HttpResponseRedirect('/microfront/admin/')

    if request.POST.has_key('foodid'):
        #print "menu_add === ", request

        if request.FILES.has_key('pic'):
            pic=request.FILES['pic']
            extension=get_extension(pic)
            if extension:  #without pic file
                #print pic,'uploaded'

                num = int(time.time()*1000)
                fname=str(num)+extension
                fullname=base+fname
                detail_fullname = base + str(num + 1) + extension
                #print "fullname: ", fullname
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

        foodlevel = int(request.POST['food_level'])
        foodstatus = int(request.POST['food_status'])
        foodgenre = int(request.POST['food_genre'])
        category=int(request.POST['category'])
        print "menu genre and status ======", foodgenre, foodstatus
        introduce=request.POST['introduce']#.replace('\n','')
        #introduce = introduce + "\n"
        #print foodname,foodprice,category,introduce, foodgenre, foodstatus, foodlevel

        total = request.POST['amount']
        foodid = int(request.POST['foodid'])

        if 0 == foodid:
            menu = Menu(orgid=1, sales=0, name=foodname, cover_url=fullname[19:], detail_url=detail_fullname[10:], old_price=foodprice, price=sprice, catalog_id=category, status=foodstatus, genre=foodgenre, level=foodlevel, total=total, introduce='')
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
            menu.level=foodlevel
            menu.save()
            #print "******************update food content: ", introduce
            add_menu_json(foodid, detail_fullname[19:], fullname[20:], foodname, category, foodprice, sprice, introduce, 1)

        
        return HttpResponseRedirect('/microfront/admin/')

    catalogs = Catalog.objects.all()
    #print "menu: ", get_food_list()
    orders = Order.objects.order_by('-order_time')
    dladdrs = Dladdr.objects.all()
    dltimes = Dltime.objects.all()
    users = Customer.objects.all()
    turnover = Order.objects.all().filter(~Q(order_status=4)).aggregate(Sum('price'))
    othersets = Otherset.objects.all()

    print "turnover", turnover
    #print "otherset", othersets
    return render_to_response('microfront/admin_manage.html', {'g_dltimejson':get_gdltimejson(), 'g_catajson': get_gcatajson(), 'dladdrs':dladdrs, 'users':users, 'dltimes':dltimes, 'catalogs':catalogs, 'orders':orders, 'foods':get_food_list(), 'turnover':turnover, 'total_turnover':turnover, 'othersets':othersets})

def add_menu_json(id, detail_url, cover_url, name, catalog_id, oprice, price, introduce, type=0):
    reload(sys)
    sys.setdefaultencoding('utf-8')
    jsonfn = 'microfront/microfront/items/' + str(id) + '.json'
    #print "Write menu json file: ", jsonfn
    if 0 == type:
        menujson = u'''{"rt_obj":{"code":0,"data":{"Goods":{"id":"%d","org_id": "1","detail_url": "%s","cover_url": "%s","name": "%s","catalog_id":"%s","old_price": "%f","price": "%f","sales":"0","total": "0","genre": "1","level": "20","content": "%s","status": "1","servings": "1","stime": "2014-03-18 14:38:40"}}}}''' %(id, detail_url, cover_url, name, catalog_id, oprice, price, introduce.replace('\r\n', '').replace('"', '\\\"'))
        menujson = json.loads(menujson)
        menujson = json.dumps(menujson)
    else:
        fdr = open(jsonfn, 'r') 
        jstr = fdr.read()
        menujson = json.loads(jstr)
        if 1 < len(introduce):
            #print "*****************Update content************** len:", len(introduce)
            menujson['rt_obj']['data']['Goods']['content'] = introduce
        else:
            #print "*****************Not Update content************** "
            menujson['rt_obj']['data']['Goods']['content'] = menujson['rt_obj']['data']['Goods']['content']
        if price is not None:
            menujson['rt_obj']['data']['Goods']['price'] = price 
        if oprice is not None:
            menujson['rt_obj']['data']['Goods']['oprice'] = oprice 

        if 1 < len(detail_url):
            menujson['rt_obj']['data']['Goods']['detail_url'] = detail_url 
        else:
            #print "*****************Not Update Detail url ************** "
            menujson['rt_obj']['data']['Goods']['detail_url'] = menujson['rt_obj']['data']['Goods']['detail_url'] 

        if 1 < len(cover_url):
            menujson['rt_obj']['data']['Goods']['cover_url'] = cover_url 
        else:
            #print "*****************Not Update Cover url ************** "
            menujson['rt_obj']['data']['Goods']['cover_url'] = menujson['rt_obj']['data']['Goods']['cover_url'] 
        fdr.close()
        menujson = json.dumps(menujson)

    #print "add Menujson[%s]" % (menujson)
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
    #print strjson, g_catajson
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
    #print  g_catajson
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
    #print strjson
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

    #print '''===menuinfo json===: %s''' %(strjson)
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
            #menus = Menu.objects.filter(catalog_id=cid).order_by('-genre', 'level')
            menus = Menu.objects.filter(catalog_id=cid).filter(~Q(status=2)).order_by('-genre', 'level')
            cnt = menus.count();
            if 0 < cnt:
                #The first catalog add prefix '{'
                if 0 == cidx:
                    strjson = strjson + '{'
                else: #The normal catalog add prefix ','
                    strjson = strjson + ','

                idx = 0
                for menu in menus:
                    #if 2 == menu.status:
                    #    continue
                    if menu.total >= menu.sales:
                        total = menu.total - menu.sales
                    else:
                        total = 0

                    if 0 == idx:
                        str = '''"%d":[{"Goods":{"id":"%d","org_id":"1","detail_url":"%s","cover_url":"%s","name":"%s","zan_num":"%d", "catalog_id":"%d","old_price":"%f","price":"%f","sales":"%d","total":"%d","genre":"%d","level":"%d","content":"%s","status":"1","servings":"1","stime":"2014-03-18 15:45:30"}}''' %(cid, menu.id, menu.detail_url, menu.cover_url, menu.name, menu.zan_num, menu.catalog_id, menu.old_price, menu.price, menu.sales, total, menu.genre, menu.level, menu.introduce)
                    else:
                        str = ''',{"Goods":{"id":"%d","org_id":"1","detail_url":"%s","cover_url":"%s","name":"%s","zan_num":"%d", "catalog_id":"%d","old_price":"%f","price":"%f","sales":"%d","total":"%d","genre":"%d","level":"%d","content":"%s","status":"1","servings":"1","stime":"2014-03-18 15:45:30"}}''' %(menu.id, menu.detail_url, menu.cover_url, menu.name, menu.zan_num, menu.catalog_id, menu.old_price, menu.price, menu.sales, total, menu.genre, menu.level, menu.introduce)
                    strjson = strjson + str
                    idx = idx + 1
                # all menu scaned, add ']'
                strjson = strjson + "]"
                cidx = cidx + 1

        # all catalog scaned, add '}'
        strjson = strjson + '}'

        #print "strjson===", strjson

    except Exception as e:
        print 'exception..........', e
    #print '''===menujson===: %s''' %(strjson)
    strjson = json.loads(strjson)
    strjson = json.dumps(strjson)
    return strjson

# Get organization json
def get_orgjson():
    idx = 0
    org = Otherset.objects.get(id=1)
    strjson = u'''{"Organization":{"id":"1","name":"爱好食","kf_phone":"%s","tip_content":"%s","distribution_range":"%s","freight":"%f"}}''' %(org.kf_phone, org.tip_content, org.distribution_range, org.freight)
    #print "org json:", strjson
    strjson = strjson.replace('\n', '\\n')
    strjson = json.loads(strjson)
    strjson = json.dumps(strjson)
    #print strjson
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
    #print strjson
    return strjson

 
# Get global dltime json
def get_gdltimejson():
    strjson='''{'''
    idx = 0
    dltimes = Dltime.objects.all()
    for dltime in dltimes:
        if 0 == idx:
            str = u'''"%d":"%s---%s"''' %(dltime.id, dltime.begin_time, dltime.end_time)
        else:
            str = u''',"%d":"%s---%s"''' %(dltime.id, dltime.begin_time, dltime.end_time)
        strjson = strjson + str
        idx = idx + 1
    strjson = strjson + "}"
    strjson = json.loads(strjson)
    strjson = json.dumps(strjson)
    #print strjson
    return strjson

@csrf_exempt
def upload_image(request):  
    if request.method == 'POST':  
        if "upload_file" in request.FILES:  
            f = request.FILES["upload_file"]  
            parser = ImageFile.Parser()
            for chunk in f.chunks():  
                parser.feed(chunk)  
            img = parser.close()  
            #在img被保存之前，可以进行图片的各种操作，在各种操作完成后，在进行一次写操作
            #dt = datetime.now()
            #cur_dir = '%s_%s_%s' % (dt.year, dt.month, dt.day)
            #file_path = os.path.join(STATIC_ROOT,IMAGES_UPLOAD_DIR, cur_dir)
            file_path = 'micromall/micromall/files/upfiles/' + time.strftime('%Y%m%d', time.localtime()) + "/"
            if not os.path.exists(file_path):
                os.mkdirs(file_path)

            #print "upload file dir path: ", file_path

            num = int(time.time())*1000
            file_name = file_path + str(num + 9)
            thumb_fn = file_name+'_min'
            #print "upload file path: ", file_path
            f = file_name
            tf = thumb_fn

            new_img=img.resize((120,120), Image.ANTIALIAS)
            new_img.save(tf+'.jpg','JPEG')
            img.save(f+'.jpg','JPEG')
            #print "upload image: ", file_name
            return HttpResponse('%s.jpg' % (file_name))
    return HttpResponse(u"Some error!Upload faild!格式：jpeg")

def write_order_json(openid, rt_obj):
    base = 'microfront/orders/'+openid
    jsonfn = base+'/0.json'
    print jsonfn
    if not os.path.exists(base):
        print 'create base', base
        os.makedirs(base)

    order_json = json.dumps(rt_obj)    
    fd = open(jsonfn, 'wb')
    fd.write(order_json)
    fd.close()
    return ''
