# coding=utf-8
'''************************************************************************
    > File Name: bloger.py
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



class bloger:
    def __init__(self):
        self.headers = {
                  "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299",
                  #"verify": 'false',
                  'Connection': 'Keep-Alive'
                  }
    def getData():pass    
    def parseCookie(self,cookie):
        dic= {}
        li = cookie.replace('\"','')\
                   .replace('\t','')\
                   .replace('\n','')\
                   .replace(' ','')\
                   .split(';')
        for i in li:
            try:
                a,b = i.split('=')
                dic[a]= b
            except:
                p = i.find('=')
                dic[i[:p]] = i[p+1:]
        self.cookie = dic
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

    def ck_post(self,data):
        self.ss = self.getSession()
        name = self.__class__.__name__
        try:
            res = self.ss.post(url=self.url,headers = self.headers,data=data,allow_redirects=False)
            if res.status_code==200:
                print('Send to {name} successfully'.format(name=name))
            return res.json()
        except Exception as e:
            print(e)
            print('post {name} blog failed QAQ \nMaybe the configuration data are out of date.'.format(name=name))
class csdn(bloger):
    
    def __init__(self):
        super().__init__()
        self.url = "https://mp.csdn.net/mdeditor/saveArticle"  
        self.po_data = CSDN_DEFAULT_DATA
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
                    p = line.find(':')
                    if p==-1: continue
                    else :
                        val = line[p+1:].strip(' \'\"\n').strip('[]')
                        if val!='': dic[line[:p].strip(' \'\"')] =val
                self.po_data .update(dic)
                s = f.read()
        s=s.strip().strip('\t')
        self.po_data['content'] = md2html(s) if MDON else s
        self.po_data['markdowncontent'] = s
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
            print('post {name} blog failed QAQ \nMaybe the configuration data are out of date.'.format(name=self.__class__.__name__))
                       

    def upload(self,session,url,fileName,file):
        '''upload pics'''
        try:
            f = {"file":(fileName,open(file,"rb"),"image/png")}
            res = session.post(url=url,headers = self.headers,files = f)
            return res.json()["content"]
        except Exception as e:
            print(e)


            
            
class cnblog(bloger):
    
    def __init__(self):
        super().__init__()
        #  文章 self.url = "https://i.cnblogs.com/EditArticle.aspx?opt=1"
        self.url = "https://i.cnblogs.com/EditPosts.aspx?opt=1"
        self.po_data = CNBLOG_DEFAULT_DATA
        self.cookie = self.parseCookie(CNBLOG_COOKIE)
        
    def getData(self,path):
        if not os.path.exists(path):
            print('file path {}  doesn\'t exist!'.format(path))
            return
        self.po_data['Editor$Edit$txbTitle'] = os.path.basename(path)
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
                    p = line.find(':')
                    if p==-1: continue
                    else :
                        val = line[p+1:].strip(' \'\"\n').strip('[]')
                        if val!='': dic[line[:p].strip(' \'\"')] =val
                if 'tags' in dic:self.po_data['Editor$Edit$Advanced$txbTag'] = dic['tags']
                if 'title' in dic: self.po_data['Editor$Edit$txbTitle'] = dic['title']
                s = f.read()
        self.po_data['Editor$Edit$EditorBody'] =  md2html(s) if MDON else s
        return self.po_data
def do(poster = csdn):
    po =poster()
    data = po.getData(file.strip())
    ret = po.at_post(data) if 'at_poat' in dir(po)  else po.ck_post(data) 
    print(ret)
               
if __name__ == '__main__':
    paths = sys.argv[1:]  
    for file in  paths:
        do(csdn)
        #do(cnblog)
