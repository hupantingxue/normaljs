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
            infos = db.select('aws_tel6', what='tel, tel_no, url', where='title like $keyword', order='id', vars={'keyword':'%'+keyword+'%'}, limit = 5)
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
            return self.render.reply_text(fromuser, touser, curtime, echostr)
        elif "event" == frommsgtype:
            fromevent = soup.Event.text
            if 'subscribe' == fromevent:
                return self.render.reply_text(fromuser, touser, curtime, u'''您好，欢迎关注爱好食！本公众号致力于打造简单、健康和时尚的都市白领生活！''')

            if 'CLICK' == fromevent:
                evtkey = soup.EventKey.text
                if 'IHAOSHI_JQHD' == evtkey:
                    return self.render.reply_text(fromuser, touser, curtime, u'''您好，欢迎查看近期活动''')
           
                if 'IHAOSHI_MENU' == evtkey:
                    return self.render.reply_text(fromuser, touser, curtime, u'''您好，好食菜单正在出炉''')
           
                if 'IHAOSHI_DIY' == evtkey:
                    text = u'''好食DIY'''
                    return self.render.reply_text(fromuser, touser, curtime, text)
           
                if 'IHAOSHI_XWC' == evtkey:
                    text = u'''下午茶时刻，欢迎光临'''
                    return self.render.reply_text(fromuser, touser, curtime, text)
           
                if 'IHAOSHI_ADVICE' == evtkey:
                    text = u'''您有好的建议欢迎留言哈'''
                    return self.render.reply_text(fromuser, touser, curtime, text)
           
                if 'IHAOSHI_KFRX' == evtkey:
                    text = u'''欢迎致电：33527'''
                    return self.render.reply_text(fromuser, touser, curtime, text)
           
                if 'IHAOSHI_DDCX' == evtkey:
                    text = u'''您还没有下单哦，要不要来点刚上市的梅子食品?~'''
                    return self.render.reply_text(fromuser, touser, curtime, text)
           
                if 'IHAOSHI_HYZX' == evtkey:
                    text = u'''您还不是会员哈'''
                    return self.render.reply_text(fromuser, touser, curtime, text)
           
                if 'IHAOSHI_DCSM' == evtkey:
                    text = u'''爱好食致力于打造简单、健康和时尚的都市白领生活！'''
                    return self.render.reply_text(fromuser, touser, curtime, text)
           
        else:
            return self.render.reply_text(fromuser, touser, curtime, u'''火星来的?Unknown message from you.''')

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
