# coding=utf-8
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
#import argparse

#parser = argparse.ArgumentParser()
#parser.add_argument('-d','--directory')
#parser.add_argument('-f','--file')


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
        self.po_data = DEFAULT_DATA
        self.cookie = self.parseCookie(CSDN_COOKIE)
    
    def getData(self,path):
        if not os.path.exists(path):
            print('file path {}  doesn\'t exist!'.format(path))
            return
        self.po_data['title'] = os.path.basename(path)
        s = None
        with open(path,'r',encoding='utf8',errors='ignore') as f:
            line = f.readline()
            if not  line.startswith('---'):
                s = line +f.read()
            else:
                dic={}
                line=''
                while not  line.startswith('---'):
                    line = f.readline()
                    print(line,123)
                    p = line.find(':')
                    if p==-1: continue
                    else :
                        val = line[p+1:].strip(' \'\"\n').strip('[]')
                        if val!='': dic[line[:p].strip(' \'\"')] =val
                print(dic)
                self.po_data .update(dic)
                s = f.read()
        pre = '这篇文章是程序自动发表的,详情可以见<a href="https://blog.csdn.net/marvellousbinary/article/details/79832708)">这里</a><br>\n\n'
        self.po_data['content'] = pre+ md2html(s) if MDON else s
        self.po_data['markdowncontent'] = pre + s
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
        '''upload pics'''
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
    post=None
    if 'session' in CSDN_COOKIE or 'SESSION' in CSDN_COOKIE:
        post = poster.ck_post
    elif  CSDN_AUTH_DATA['password'] != '***' and CSDN_AUTH_DATA['client_secret'] != '***' :
        post = poster.at_post
       
    paths = sys.argv[1:]  
    if post is None:
        print("[Error]: please edit the config.py first to configue neccessary args")
    else:
        for file in  paths:
            data = poster.getData(file.strip())
            ret= post(data)
            print(ret)
