# -*- coding: utf-8 -*-
import os
import web
import time
import conf
import hashlib
from bs4 import BeautifulSoup
import logging, logging.handlers
import random

urls = ('/', 'index')
loggers = {}

db = web.database(dbn='mysql', user=conf.DB_USER, pw=conf.DB_PWD, db=conf.DB_NAME)

gstr = ["偶老师，他还没教我这个/::'(", 
        '小战舰还是笨笨的菜鸟，恳请大侠刀下留人~~~', 
        '想用神一样的思维，难倒我？[左哼哼]',
        '你有木有打错字哦，害我答不上',
        '为了弥补我不懂的事实，给你讲个笑话吧。',
        '想听笑话还是糗事？',
        '''实惠的欢迎方式\n 我和女儿在家一边嗑瓜子吃水果，一边看电视。不一会儿，弟弟和弟媳来了，女儿开心得不得了，吃着香蕉说：“欢迎，欢迎，热烈欢迎舅舅和舅妈来我家玩。” \n弟媳望着女儿手上的香蕉笑道：“嘴上欢迎是虚的，有什么实惠的方式来欢迎我们？” 女儿赶紧放下香蕉：“舅舅和舅妈来了，我们掌声欢迎。”说着，欢快地拍起了手掌。”''',
        '地球不缺你这个资源，回火星去吧~~~',
        '想用神一样的思维，难倒我？/:<@',
        '啊哦，回答这个问题俺还需要更多的魔法值。。。',
        '[晕]不懂，我知道不少名人资料，譬如雨神----萧敬腾~~']

def get_orderlist(openid):
    orders = db.select('microfront_order', what='order_time, shoplist, price', where='openid=$openid', order='order_time desc', vars={'openid':openid}, limit = 5)
    order_str = ""
    for order in orders:
        order_str = order_str + u"%s %s共%s元\n" %(order.order_time, order.shoplist.replace('\n', ''), order.price)
        print order_str.encode('utf-8')
    return order_str.encode('utf-8') 

class index:
    def __init__(self):
        self.app_root = os.path.dirname(__file__)
        self.templates_root = os.path.join(self.app_root, 'templates')
        self.render = web.template.render(self.templates_root)
        self.wxlogger = self.myLogger('ihaoshi')

    def myLogger(self, name):
        global loggers

        if loggers.get(name):
            return loggers.get(name)
        else:
            logger=logging.getLogger(name)
            logger.setLevel(logging.DEBUG)
            handler=logging.FileHandler(filename='wxrun.log', mode='a')
            formatter = logging.Formatter('[%(name)s:%(lineno)s] - %(asctime)s - %(levelname)s: %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            loggers.update(dict(name=logger))
            return logger

    def GET(self):
        try:
            data = web.input()
            signature = data.signature
            timestamp = data.timestamp
            nonce = data.nonce
            echostr = data.echostr
            token = conf.TOKEN
            list = [token, timestamp,nonce]
            list.sort()
            sha1=hashlib.sha1()
            map(sha1.update, list)
            hashcode=sha1.hexdigest()
            if hashcode == signature:
                return echostr
        except Exception as e:
            self.wxlogger.error("get fail %s" % (e))
            return ''

    def POST(self):
        try:
            poststr = web.data()
            soup = BeautifulSoup(poststr, "xml")
            fromuser = soup.FromUserName.text
            touser = soup.ToUserName.text
            frommsgtype = soup.MsgType.text
            curtime = int(time.time())
        except Exception as e:
            echostr = "parse fail", e
            self.wxlogger.error("parse fail %s" % (e))
        self.wxlogger.info("poststr[%s]" % (poststr))
        
        if "text" == frommsgtype:
            echostr = ''
            keyword = soup.Content.text.strip()
            #infos = db.select('microfront_order', what='id', where='like $keyword', order='id', vars={'keyword':'%'+keyword+'%'}, limit = 5)
            rsltlen = 0
            for info in infos:
                rsltlen = rsltlen + 1
                echostr = echostr + info['tel'] + info['tel_no'] + "  \n" + u'''  <a href=\"%s\">点击查看详情</a>\n\n''' %(info['url'])
            #print echostr
            if 0 == rsltlen:
                #echostr = '想用神一样的思维，难倒我？/:<@'
                idx = 0
                idx = random.randint(0, len(gstr)-1)
                echostr = gstr[idx]
            #return self.render.reply_text(fromuser, touser, curtime, echostr)
        elif "event" == frommsgtype:
            fromevent = soup.Event.text
            if 'subscribe' == fromevent:
                #url='http://211.154.149.170:8600/microfront?code=%s' %(fromuser)
                #url = 'http://www.ihaoshi.cn/ihaoshi/home.php?code=%s' %(fromuser)
                url = 'http://mp.weixin.qq.com/s?__biz=MzA4NjM5NDcyNw==&mid=200343771&idx=1&sn=0b731b29357eceaacd683e572a2a0872#rd'
                print url
                return self.render.reply_pic(fromuser, touser, curtime, u'爱好食第一章：引领健康生活，从生鲜开始', u'爱好食，打造简单、健康、时尚的都市生活', 'http://www.ihaoshi.cn/img/ihaoshi.jpg', url) 

            if 'CLICK' == fromevent:
                evtkey = soup.EventKey.text
                if 'IHAOSHI_JQHD' == evtkey:
                    url = 'http://mp.weixin.qq.com/s?__biz=MzA4NjM5NDcyNw==&mid=200444522&idx=1&sn=10443811cd8643e29ad1e52bdfa646a4#rd'
                    return self.render.reply_pic(fromuser, touser, curtime, u'好食来，福利到，你选菜，我买单啦！', u'为庆祝爱好食生鲜平台上线，现推出“你选菜，我买单”活动，活动期间，每天都有由“您”决定的免费产品，赶快行动吧，福利可不容错过啊！！', 'http://www.ihaoshi.cn/img/ihaoshi.jpg', url)

                if 'IHAOSHI_HSTJ' == evtkey:
                    return self.render.reply_text(fromuser, touser, curtime, u'''编辑中。。。''')
           
                if 'IHAOSHI_MENU' == evtkey:
                    #url='http://211.154.149.170:8600/microfront?code=%s' %(fromuser)
                    url = 'http://www.ihaoshi.cn/ihaoshi/home.php?code=%s' %(fromuser)
                    print url
                    return self.render.reply_pic(fromuser, touser, curtime, u'点击查看今日菜品', u'爱好食，打造简单、健康、时尚的都市生活', 'http://www.ihaoshi.cn/img/cover.jpg', url) 
          
                if 'IHAOSHI_KFRX' == evtkey:
                    text = u'''客服热线：15889613776\n 服务时间：周一~周五9:00~20:00\n订餐说明：\n1、绿色蔬菜当天下单，次日送达，仅限南山科技园地铁站附近；\n2、有机蔬菜提前4天下单，配送范围为深圳区域，可宅配；\n3、阳澄湖大闸蟹礼券当天下单，24~48小时送达，全国包邮；\n4、每天优惠活动可进入微社区了解并参与其中。'''
                    return self.render.reply_text(fromuser, touser, curtime, text)
           
                if 'IHAOSHI_DDCX' == evtkey:
                    #text = u'''您还没有下单哦，要不要来点刚上市的梅子食品?~'''
                    url = 'http://www.ihaoshi.cn/ihaoshi/orders/index.php?code=%s' %(fromuser)
                    #text = get_orderlist(fromuser)
                    #return self.render.reply_text(fromuser, touser, curtime, text)
                    return self.render.reply_pic(fromuser, touser, curtime, u'我的订单', u'点击查看我的订单', 'http://www.ihaoshi.cn/img/cover.jpg', url) 
           
                if 'IHAOSHI_PSFW' == evtkey:
                    text = u'''1、绿色蔬菜仅限南山科技园地铁站附近1000米；\n2、有机蔬菜配送范围为深圳区域，可宅配，不支持货到付款；\n3、阳澄湖大闸蟹礼券全国包邮，不支持货到付款。\n 订餐说明\n1、绿色蔬菜当天下单，次日送达\n2、有机蔬菜提前4天下单，支持可宅配；\n3、阳澄湖大闸蟹礼券当天下单，24~48小时送达，全国包邮；\n4、每天优惠活动可进入微社区了解并参与其中。'''
                    return self.render.reply_text(fromuser, touser, curtime, text)
           
                if 'IHAOSHI_DCSM' == evtkey:
                    text = u'''目前暂只支持南山科技园附近及宝安中心区地铁口附近区域，努力覆盖更广范围中，带来不便，敬请谅解！订餐说明：1、绿色蔬菜需提前一天下单，次日下班前送达，2、有机蔬菜和海鲜即将亮相，敬请期待。3、每天优惠活动可进入微社区了解并参与其中。'''
                    return self.render.reply_text(fromuser, touser, curtime, text)
           
                if 'IHAOSHI_ABOUT' == evtkey:
                    #text = u'''爱好食，打造简单、健康、时尚的都市生活。'''
                    url = 'http://mp.weixin.qq.com/s?__biz=MzA4NjM5NDcyNw==&mid=200343771&idx=1&sn=0b731b29357eceaacd683e572a2a0872#rd'
                    return self.render.reply_pic(fromuser, touser, curtime, u'爱好食第一章：引领健康生活，从生鲜开始', u'爱好食，打造简单、健康、时尚的都市生活', 'http://www.ihaoshi.cn/img/ihaoshi.jpg', url) 
           
        else:
            return self.render.reply_text(fromuser, touser, curtime, u'''火星来的?Unknown message from you.''')

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
