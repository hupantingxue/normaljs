#!/usr/bin/python
#-*- coding:utf-8 -*-

from conf import DB_USER,  DB_PASSWD, DB_HOST, DB_PORT, DB_NAME
import time
import MySQLdb
import json
import os

conn = MySQLdb.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWD, db=DB_NAME ,charset="utf8")
cur = conn.cursor()

def getOrders(wechat_id):
    '''
        return order list and order-history list;
    '''
    sql = '''select * from microfront_order where openid = "%s" order by id;''' %(wechat_id)
    cur.execute(sql)
    rslt = cur.fetchall()
    row_num = len(rslt)
    if 0 >= row_num:
        return None, None
    elif 1 == row_num:
        return rslt, None
    else:
        return rslt[0:1], rslt[1:]
    return rslt[0:1], rslt[1:]

def writeJSON(wechat_id, rslt, type):
    '''
        write order json or hostory order json file. rslt is the order list;
    '''
    row_num = len(rslt)
    ii = 0
    if 0 >= row_num:
        return ''

    print "type:%s ||| rslt:%r" %(type, rslt)

    rt_obj = {"data":{"orders":[], "orderItems":{}}}
    rt_obj["data"]["orderItems"] = {}
    for ii in range(row_num):
        # do something
        rtime = rslt[ii][10]
        rdate = rtime.strftime("%Y%m%d")
        order_id = rslt[ii][0]
        item_id = "%s%d" %(rdate, order_id)
        item_info = '''{"Order": {"id": "%s","org_id": "1","user_id": "%s","status": "1","order_time": "%s","order_date": "%s","order_money": "%s","pay_mode": "%s","delivery_status": "%d","freight": "0.00"}}''' %(item_id, wechat_id, rtime, rdate, rslt[ii][1], rslt[ii][4], rslt[ii][9])
        item_info = json.loads(item_info)
        rt_obj["data"]["orders"].append(item_info)

        # get order item menu list
        shoplist = rslt[ii][13].split(";")
        
        print item_id, shoplist
        rt_obj["data"]["orderItems"][item_id] = []

        for shop in shoplist:
            if '\n' == shop:
                break
            try:
                goods_name, goods_num, goods_unit = shop.split()
            except Exception as e:
                goods_name1, goods_name2, goods_num, goods_unit = shop.split()
                goods_name = "%s %s" % (goods_name1, goods_name2)
            
            #get goods_id and goods_price 
            menu_sql = 'select id, price from microfront_menu where name = "%s";' %(goods_name)
            cur.execute(menu_sql)
            menu_rslt = cur.fetchone()
            goods_id = menu_rslt[0]
            goods_price = menu_rslt[1]
            
            order_jsitem = u'''{"OrderGoods": {"order_id": "%s","goods_id": "%s","goods_price": "%f","goods_num": "%s","goods_name": "%s","customers": "2"}}''' %(item_id, goods_id, goods_price, goods_num, goods_name)
            order_jsitem = json.loads(order_jsitem)
            rt_obj['data']['orderItems'][item_id].append(order_jsitem)


    rt = {"rt_obj": rt_obj}
    rt_json = json.dumps(rt) #, ensure_ascii = False)
    base = u'/home/haomatong/test/python/normaljs/microfront/orders/' + wechat_id + "/"
    if not os.path.exists(base):
        print 'create base', base
        os.makedirs(base)

    jsonfn = "%s%s.json" % (base, type)
    print rt_json
    fd = open(jsonfn, 'w')
    fd.write(rt_json)
    fd.close()
    
    return ''

if "__main__" == __name__:
    wechat_id = u'111'
    order, his_order = getOrders(wechat_id)
    writeJSON(wechat_id, order, 0)
    writeJSON(wechat_id, his_order, 1)
    conn.close()
