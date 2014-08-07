#!/usr/bin/python
#-*- coding:utf-8 -*-

from conf import *
import time
import MySQLdb
import json
import os
import redis
import sys

conn = MySQLdb.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWD, db=DB_NAME ,charset="utf8")
cur = conn.cursor()
r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)

def getAllMenus():
    '''
        return user set
    '''
    global conn
    global cur
    sql = '''select distinct(id) from microfront_menu order by id;'''
    try:
        conn.commit()
    except Exception as e:
        conn = MySQLdb.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWD, db=DB_NAME ,charset="utf8")
        cur = conn.cursor()
        print e
    cur.execute(sql)
    rslt = cur.fetchall()
    return rslt

def menuInfo(menu_id):
    '''
        return menu info 
    '''
    global conn
    global cur
    print "menuInfo ", menu_id
    sql = '''select total, sales from microfront_menu where id = %d;''' %(int(menu_id))
    try:
        conn.commit()
    except Exception as e:
        conn = MySQLdb.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWD, db=DB_NAME ,charset="utf8")
        cur = conn.cursor()
        print e
    cur.execute(sql)
    rslt = cur.fetchall()
    total = rslt[0][0]
    sales = rslt[0][1]
    return total, sales

def writeFile(menu_id):
    '''
        write menu json string to file 
    '''
    base = u'/home/otto/src/github/normaljs/microfront/microfront/items/'
    if not os.path.exists(base):
        print 'create base', base
        os.makedirs(base)

    jsonfn = "%s%s.json" % (base, menu_id)
    # get menuinfo by menu_id
    total, sales = menuInfo(menu_id)

    fd = open(jsonfn, 'rb+')
    try:
        strinfo = fd.read()
        #strinfo = u"%s" % (strinfo)
        strinfo.replace('\n', '\\n').replace('\r', '\\r')
    except Exception as e:
        print e
    #print strinfo
    jsinfo = json.loads(strinfo)
    jsinfo['rt_obj']['data']['Goods']['total'] = total
    jsinfo['rt_obj']['data']['Goods']['sales'] = sales
    strinfo = json.dumps(jsinfo,  ensure_ascii=False, separators=(',', ':'))
    fd.seek(0)
    fd.write(strinfo.encode('utf-8'))
    print "write menu[%d] info[%s]" %(int(menu_id), strinfo)
    fd.truncate()
    fd.close()
    return ''
 
if "__main__" == __name__:
    last_rdate = 0
    ii = 1
    while 0 < 1:
        menu_id = None
        menu_id = r.rpop(MENU_RQUEUE)
        if menu_id is None:
            time.sleep(1)
            continue
        rdate = time.strftime("%Y-%m-%d")
        if (0 == int(menu_id)) or (last_rdate != rdate):
            menu_ids = getAllMenus()
            last_rdate = rdate
        else:
            menu_ids = [[menu_id]]
        for ii in menu_ids:
            menu_id = ii[0]
            writeFile(menu_id)
    cur.close()
    conn.close()
