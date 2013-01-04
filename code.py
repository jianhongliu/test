#!/usr/bin/env python
#-*-coding:utf-8-*-
import web
import re, time
from httplib import *

web.config.smtp_server = 'smtp.gmail.com'
web.config.smtp_port = 587
web.config.smtp_username = 'xxx@xxx.com'
web.config.smtp_password = 'xxxxxxxx'
web.config.smtp_starttls = True

keyword = 'iphone'

site = {} 

site[1] = ('www.b5m.com', '/search/s/______________' + keyword + '.html', '找到相关商品(\d+)件', '购物搜索')
site[2] = ('sejie.b5m.com', '/sejie/s/____' + keyword + '.html', 'title="喜欢">(\d+)</span>', '色界搜索')
site[3] = ('www.b5m.com', '/guang/s/_____' + keyword + '.html', '逛街\((\d+)\)', '逛街搜索')
site[4] = ('www.b5m.com', '/o/tuan/s/' + keyword + '_________', '共有(\d+)条符合条件的结果', '团购搜索')
site[5] = ('www.b5m.com', '/o/ticket/s/' + '2012' + '_______', '找到<strong>(\d+)</strong>个相关演出', '搜票搜索')
site[6] = ('www.b5m.com', '/o/shj/s/' + 'a' + '_____', '正品保障<b>\((\d+)\)</b>', '商家搜索')
site[7] = ('www.b5m.com', '/clt/s/___' + keyword + '.html', '专题\((\d+)\)', '专题搜索')
site[8] = ('www.b5m.com', '/brandSearch_' + 'apple' + '_.html', '品牌\((\d+)\)', '品牌搜索')
site[9] = ('www.b5m.com', '/', '(\d+)天以前', '首页')
site[10] = ('www.b5m.com', '/guang', '￥(\d+)', '导航逛街')
site[11] = ('www.b5m.com', '/o/tuan', '<b>原价</b><span>¥</span><span><del>(\d+)', '导航团购')
site[12] = ('www.b5m.com', '/o/ticket', '<strong>演唱会</strong>\((\d+)\)</a></li>', '导航演出票务')
site[13] = ('www.b5m.com', '/fan', '返(\d+)%', '导航网购优惠')
site[14] = ('www.b5m.com', '/album/idx/__1.html', '<span class="likeico"></span>\((\d+)\)</span>', '导航专题')
site[15] = ('www.b5m.com', '/brand/', '<em class="likeico"></em>(\d+)</p>', '导航品牌')
site[16] = ('sejie.b5m.com', '/sejie/', 'title="喜欢">(\d+)</span>', '导航色界')


urls = (
    '/(.*)', 'index',
)

render = web.template.render('templates/')
app = web.application(urls, globals())

class index:
    def GET(self, emailflag):
        counts = {}
        message = ""
        emailflag = int(emailflag)
        for i in range(1,17):
            counts[site[i][3]] = [0, site[i][0]+site[i][1]] 
        for j in range(1,4):
            for i in range(1,17):
                conn = HTTPConnection(site[i][0],80,True,20)
                try:
                    conn.request('GET',site[i][1])
                    httpres = conn.getresponse()
                    data = httpres.read()
                    pr = re.findall(site[i][2],data)
                    if  pr:
                        value = counts[site[i][3]][0] +  int(pr[0])
                    else:
                        value = counts[site[i][3]][0] + 0
                    counts[site[i][3]][0] = value
                except:
                    value = counts[site[i][3]][0] + 0
                    counts[site[i][3]][0] = value
                    continue
                if counts[site[i][3]][0] == 0:
                    message = message + site[i][3] + " page is FAILED!"
                time.sleep(0)
        for i in range(1,17):
            counts[site[i][3]][0] = counts[site[i][3]][0]/3
            if counts[site[i][3]][0] == 0:
                message = message + site[i][3] + " page is FAILED!"
        if  message and emailflag==0:
#emailflag 防止邮件重发，出问题时，设置为1，则下次检测再出问题，不会发送email，待问题修复后设置为0，下次出问题就可继续发邮件
            subject = "搜索or导航 Page Failed"
            web.sendmail('xxx@xxx.com', 'yyy@xxx.com', subject, message) 
            emailflag = 1
        elif not message:
            emailflag = 0
        counts['emailflag'] = [emailflag, web.ctx.homedomain]
        return render.index(counts) 

if __name__ == "__main__":
    app.run()
