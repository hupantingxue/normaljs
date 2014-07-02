#!/usr/bin/python2.6 
#-*- coding:utf8 -*-

import httplib
import urllib
import sys
import json

sys.path.append('..')
import conf

menu = '''{
        "button":[
            {
                "name":"好食推荐",
                "sub_button":[
                     {"type":"click", "name":"近期活动", "key":"IHAOSHI_JQHD"}, 
                     {"type":"click", "name":"好食推荐", "key":"IHAOSHI_HSTJ"}
                 ]
            }, 
            {
                "type":"click", 
                "name":"好食菜单",
                "key":"IHAOSHI_MENU" 
            }, 
            {
                "name":"我的好食",
                "sub_button":[
                    {"type":"click", "name":"客服热线", "key":"IHAOSHI_KFRX"}, 
                    {"type":"click", "name":"订单查询", "key":"IHAOSHI_DDCX"}, 
                    {"type":"click", "name":"配送范围", "key":"IHAOSHI_PSFW"},
                    {"type":"click", "name":"订购说明", "key":"IHAOSHI_DCSM"},
                    {"type":"click", "name":"关于好食", "key":"IHAOSHI_ABOUT"} 
                ]
            }
        ]
    }'''

def getToken():
    strinfo = '''{"grant_type":"client_credential","appid":"%s","secret":"%s"}''' %(conf.APPID, conf.APP_SECRET)
    print strinfo
    jstr = json.loads(strinfo)
    params = urllib.urlencode(jstr)
    f = urllib.urlopen("https://api.weixin.qq.com/cgi-bin/token?%s" % params)
    token = f.read()
    token = json.loads(token)
    return token['access_token']

if '__main__' == __name__:
    token = getToken()
    print 'Token is %s' %(token)

    #create menu
    f = urllib.urlopen("https://api.weixin.qq.com/cgi-bin/menu/create?access_token=%s" %(token), menu)
    print f.read()
