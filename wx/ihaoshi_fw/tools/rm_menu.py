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
                     {"type":"view", "name":"店长推荐", "url":"http://www.ihaoshi.cn/tuijian.html"}
                 ]
            }, 
            {
                "name":"好食菜单",
                "sub_button":[
                    {"type":"click", "name":"好食菜单", "key":"IHAOSHI_MENU"}, 
                    {"type":"click", "name":"好食DIY", "key":"IHAOSHI_DIY"}, 
                    {"type":"click", "name":"好食下午茶", "key":"IHAOSHI_XWC"}
                ]
            }, 
            {
                "name":"我的好食",
                "sub_button":[
                    {"type":"click", "name":"我的建议", "key":"IHAOSHI_ADVICE"}, 
                    {"type":"click", "name":"客服热线", "key":"IHAOSHI_KFRX"}, 
                    {"type":"click", "name":"订单查询", "key":"IHAOSHI_DDCX"}, 
                    {"type":"click", "name":"会员中心", "key":"IHAOSHI_HYZX"},
                    {"type":"click", "name":"订餐说明", "key":"IHAOSHI_DCSM"}
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

    #remove menu
    f = urllib.urlopen("https://api.weixin.qq.com/cgi-bin/menu/delete?access_token=%s" % token)
    print f.read()
