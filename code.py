#!/usr/bin/env python
#-*-coding:utf-8-*-
import web
import re, time
from httplib import *

web.config.smtp_server = 'smtp.gmail.com'
web.config.smtp_port = 587
web.config.smtp_username = 'xxx@gmail.com'
web.config.smtp_password = '123456'
web.config.smtp_starttls = True

keyword = 'iphone'

site1 = ('www.b5m.com', '/search/s/______________' + keyword + '.html', '找到相关商品(\d+)件', '购物')
site2 = ('sejie.b5m.com', '/sejie/s/____' + keyword + '.html', 'title="喜欢">(\d+)</span>', '色界')
site3 = ('www.b5m.com', '/guang/s/_____' + keyword + '.html', '逛街\((\d+)\)', '逛街')
site4 = ('www.b5m.com', '/o/tuan/s/' + keyword + '_________', '共有(\d+)条符合条件的结果', '团购')
site5 = ('www.b5m.com', '/o/ticket/s/' + '2012' + '_______', '找到<strong>(\d+)</strong>个相关演出', '搜票')
site6 = ('www.b5m.com', '/o/shj/s/' + 'a' + '_____', '正品保障<b>\((\d+)\)</b>', '商家')
site7 = ('www.b5m.com', '/clt/s/___' + keyword + '.html', '专题\((\d+)\)', '专题')
site8 = ('www.b5m.com', '/brandSearch_' + 'apple' + '_.html', '品牌\((\d+)\)', '品牌')
site9 = ('www.b5m.com', '/', '(\d+)天以前', '首页')
site10 = ('www.b5m.com', '/guang', '￥(\d+)', '导航逛街')
site11 = ('www.b5m.com', '/o/tuan', '<b>原价</b><span>¥</span><span><del>(\d+)', '导航团购')
site12 = ('www.b5m.com', '/o/ticket', '<strong>演唱会</strong>\((\d+)\)</a></li>', '导航演出票务')
site13 = ('www.b5m.com', '/fan', '返(\d+)%', '导航网购优惠')
site14 = ('www.b5m.com', '/album/idx/__1.html', '<span class="likeico"></span>\((\d+)\)</span>', '导航专题')
site15 = ('www.b5m.com', '/brand/', '<em class="likeico"></em>(\d+)</p>', '导航品牌')
site16 = ('sejie.b5m.com', '/sejie/', 'title="喜欢">(\d+)</span>', '导航色界')

urls = (
    '/', 'index',
)

render = web.template.render('templates/')

class index:
    def GET(self):
        counts = {}
        for i in range(1,17):
            conn = HTTPConnection(eval('site'+str(i))[0],80,True,20)
            try:
                conn.request('GET',eval('site'+str(i))[1])
                httpres = conn.getresponse()
                data = httpres.read()
                pr = re.findall(eval('site'+str(i))[2],data)
                if  pr:
                    counts.update({str(eval('site'+str(i))[3]):pr[0]})
                else:
                    counts.update({str(eval('site'+str(i))[3]):0})
            except:
                counts.update({str(eval('site'+str(i))[3]):0})
                continue
            if counts[str(eval('site'+str(i))[3])] == 0:
               subject = str(eval('site'+str(i))[3]) + " page is FAILED!"
               message = str(eval('site'+str(i))[3]) + " page is FAILED!"
               web.sendmail('xxx@gmail.com', 'toyyy@gmail.com', subject, message) 
            time.sleep(2)
        return render.index(counts) 

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
