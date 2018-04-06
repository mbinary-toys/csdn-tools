#coding: utf-8
'''************************************************************************
    > File Name: blogSender.py
    > Author: mbinary
    > Mail: zhuheqin1@gmail.com 
    > Created Time: Thu 05 Apr 2018 04:31:35 PM DST
 ************************************************************************'''

import os
import re
import sys
import requests
import markdown
from config  import *



def md2html(s):
    exts = ['markdown.extensions.extra', 'markdown.extensions.codehilite','markdown.extensions.tables','markdown.extensions.toc']

    html = '''
            <html lang="zh-cn">
            <head>
            <meta content="text/html; charset=utf-8" http-equiv="content-type" />
            <link href="http://ounix1xcw.bkt.clouddn.com/github.markdown.css" rel="stylesheet">
            </head>
            <body>
            {mdstr}
            </body>
            </html>
           '''

    mdstr = markdown.markdown(s,extensions=exts)
    return html.format(mdstr = mdstr)



class blogSender:
    def __init__(self):
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0",
                  "verify": 'false'}
    def ck_post(self,data):
        self.ss = self.getSession()
        try:
            res = self.ss.post(url=self.url,headers = self.headers,data=data)
            return res.json()
        except Exception as e:
            print(e)
            print('post csdn blog failed QAQ \nMaybe the configuration data are out of date.')
    def parseCookie(self,cookie):
        dic  = {}
        li = cookie.replace('\"','').replace('\n','').replace(' ','').split(';')
        for i in li:
            try:
                a,b = i.split('=')
                dic[a]= b
            except:
                p = i.find('=')
                dic[i[:p]] = i[p+1:]
        return dic
    def getSession(self):
        try:
            ss= requests.session()
            jar = requests.cookies.RequestsCookieJar()
            for a,b in self.cookie.items():
                jar.set(a,b)
            ss.cookies.update(jar)
            return ss
        except Exception as e:
            print(e)

class csdn(blogSender):
    
    def __init__(self):
        super().__init__()
        self.url = "https://mp.csdn.net/mdeditor/saveArticle"
        self.po_data = {"title":"do you know my name?",
             "markdowncontent":'# hello, world~',
             "content": '''<h1>hello, world~</h1>''',
             "categories":"默认分类",
             "channel":33,
             "tags":"python,tag2",
            'type':'original', #original原创 report转载 translated 翻译
             "private":0,
             #"id": 0     修改已有文章
             }
        self.po_data.update(DEFAULT_DATA)
        self.cookie = self.parseCookie(CSDN_COOKIE)
    def getData(self,path):
        if not os.path.exists(path):
            print('file path {}  doesn\'t exist!'.format(path))
            return
        self.po_data['title'] = os.path.basename(path)
        s = None
        with open(path,'r',encoding='utf8',errors='ignore') as f:
            s=f.read()
        
        fd = re.search('\s*---(.*?)---',s,re.DOTALL)
        if not fd:
            self.po_data['content'] = md2html(s) if MDON else s
        else:
            meta = fd.groups()[0]
            p  = len(meta)+7
            self.po_data['content'] = md2html(s[p:]) if MDON else s[p:]
            for entry in  ["content","categories","tags",'type','channel','title']:
                val = re.search(entry+':(.*?)\n',s)
                try:self.po_data[entry] = val.groups()[0].strip()
                except:pass
        
        return self.po_data
        
    def at_post(self,data):
        '''
        使用api  需要在http://open.csdn.net/wiki/api/注册开发者,得到cliet_id 和 client_secret
        '''
        auth_url = 'http://api.csdn.net/oauth2/access_token'
        po_url = 'http://api.csdn.net/blog/savearticle'
        
        try:
            access_token = requests.get(auth_url,data= CSDN_AUTH_DATA ).json()['access_token']
            self.po_data['access_token'] = access_token
            r = requests.post(po_url,data=data)
            return r.json()
        except Exception as e:
            print(e)
            print('post csdn blog failed QAQ \nMaybe the configuration data are out of date.')
                       

    def upload(self,session,url,fileName,file):
        try:
            f = {"file":(fileName,open(file,"rb"),"image/png")}
            res = session.post(url=url,headers = self.headers,files = f)
            return res.json()["content"]
        except Exception as e:
            print(e)
            
class jianshu(blogSender):    
    pass


if __name__ == '__main__':
    poster = csdn()
    #path = ['D:/blog/blog/source/_posts/about.md']
    
    # poster.upload()   上传图片
    post=None
    if 'session' in CSDN_COOKIE or 'SESSION' in CSDN_COOKIE:
        post = poster.ck_post
    elif  CSDN_AUTH_DATA['password'] != '***' and CSDN_AUTH_DATA['client_secret'] != '***' :
        post = poster.at_post
    if post is None:
        print("[Error]: please edit the config.py first to configue neccessary args")
    else:
        for file in  sys.argv[1:]:
            data = poster.getData(file.strip())
            json= poster.ck_post(data)
            print(json)
