#coding: utf-8
'''************************************************************************
    > File Name: blogSender.py
    > Author: mbinary
    > Mail: zhuheqin1@gmail.com 
    > Created Time: Thu 05 Apr 2018 04:31:35 PM DST
 ************************************************************************'''

import os
import re
import requests


class blogSender:
    def __init__(self,url,cookie):
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0",
                  "verify": 'false'}
        self.cookie = self.parseCookie(cookie)
        self.url = url
        self.ss = self.getSession()
    def parseCookie(self,cookie):
        dic  = {}
        li = cookie.replace('\"','').replace(' ','').split(';')
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
    def getMetadata(self,data,s):
        for entry in  data:
            val = re.search(entry+':(.*?)\n',s)
            if val!=None and val.group().strip() !='':
                data[entry] = val.group().strip()
        return data
    def post(selfl,path):
        pass

class csdn(blogSender):    
    def post(self,path):
        if not os.path.exists(path):
            print('file path {}  doesn\'t exist!'.format(path))
            return
        data = {"title":"do you know my name?",
             "markdowncontent":'# emm',
             "content": '''<h1>hello, world~</h1>''',
             "categories":"默认分类",
             "channel":33,
             "tags":"python",
            'type':'original',
             "artideedittype":1,
             "private":0,
             "status":0
             #"id":     修改已有文章
             }
        s = None
        with open(path,'r',encoding='utf8',errors='ignore') as f:
            s=f.read()
        data['title'] = os.path.basename(path)
        self.getMetadata(data,s)
        m = re.match('(```.*?```).*',s)
        end = 0 if m is None else m.end
        data['content'] = s[end:]
        try:
            res = self.ss.post(url=self.url,headers = self.headers,data=data)
            return res.json()
        except Exception as e:
            print('post csdn blog failed QAQ')
            print(e)
    
    def upload(self,session,url,fileName,file):
        try:
            f = {"file":(fileName,open(file,"rb"),"image/png")}
            re = session.post(url=url,headers = self.headers,files = f)
            return re.json()["content"]
        except Exception as e:
            print(e)
class jianshu(blogSender):    
    pass


if __name__ == '__main__':
    
    url = "https://mp.csdn.net/mdeditor/saveArticle?isPub=1"
    cookie = '''
            
            '''
    if cookie == '':cookie = input("输入cookie")
    poster = csdn(url,cookie)
    # poster.upload()   sh上传图片
    json= poster.post('D:/blog/blog/source/_posts/share-books.md')
    print(json)
    
