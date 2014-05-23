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
    params = urllib.urlencode({'grant_type':'client_credential','appid':'wx113f2cdd690c64e4','secret':'b81e93227dbcacaff9810e219af3a8fd'})
    f = urllib.urlopen("https://api.weixin.qq.com/cgi-bin/token?%s" % params)
    token = f.read()
    token = json.loads(token)
    return token['access_token']

if '__main__' == __name__:
    #token = getToken()
    token = '11U6nRr49qjoPlRF8IDuAs4l-Zv72v4N5v8dsTtwj70Bxt4o1iyZ4OxQVKUOXoCPiU9H6u53epnx-IMARdY8F34n3KHj7ipYwBJ9iQLLa3i0iuekDN_bwn6UnYcuu2-GlcVxK5_B_Zb51x0g75Nlew'
    print 'Token is %s' %(token)

    #create menu
    f = urllib.urlopen("https://api.weixin.qq.com/cgi-bin/menu/create?access_token=%s" %(token), menu)
    print f.read()
