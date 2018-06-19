#coding: utf-8
'''************************************************************************
    > File Name: uploadFile.py
    > Author: mbinary
    > Mail: zhuheqin1@gmail.com 
    > Blog: https://mbinary.github.io
    > Created Time: Sun 08 Apr 2018 11:04:17 PM DST
 ************************************************************************'''
import time
import os, random, sys, requests
from zipfile import ZipFile
from config import CSDN_UPLOAD_COOKIE as ck
from requests_toolbelt.multipart.encoder import MultipartEncoder
url = 'https://download.csdn.net/upload/do_upload'
headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:50.0) Gecko/20100101 Firefox/50.0',
            'Referer': url
                        }

def parseCookie(cookie):
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
def getName(path):
    name = os.path.basename(path)
    p = name.find('.')
    if p!=-1:name = name[:p]
    return name

zipForm = ['.rar','.zip','.7z','.tar','.gz','.xz']
with open('readme.txt','w') as f:
    tm = time.strftime('%Y-%m-%d  %H:%M')
    f.write('made by: mbinary\n blog: https://mbinary.coding.me\n time: {tm}'.format(tm=tm))

def makePack(path):
    #for i in zipForm:
        #if  path.endswith(i):return path 
    base =os.path.basename(path)
    name = '.zipfile/'+ base + '-mbinary.zip'
    with  ZipFile(name,'w')  as z:
        cur = os.getcwd()
        os.chdir(os.path.dirname(path))
        z.write(base)
        os.chdir(cur)
        z.write('readme.txt')
    return name 
def formData(path):
    name = getName(path)
    return  MultipartEncoder(
            fields={
                    'txt_title':name*(50//len(name)),
                     'sel_filetype':'3',# nota all value should be str
                    'txt_tag': '工具书籍',
                     'sel_primary':'15',
                     'sel_subclass': '15013',
                     'sel_score':'3',
                     'txt_desc':name*20,
                     'txt_userfile': (os.path.basename(path) ,open(path, 'rb'),'application/X-zip-compressed' )
                   }
                    # 'txt_userfile': (os.path.basename(path) ,open(path, 'rb'),'text/plain') 
   # boundary='-----------------------------' + str(random.randint(1e28, 1e29 - 1))
    )

def handleDir(arg):
    gen = os.walk(arg)
    for path, dirs,files in gen:
        li = [os.path.join(path,i) for i  in files] 
        li = [makePack(i) for i in li]
        doLst(li)

def doLst(lst):
    for path in lst:
        time.sleep(2)
        data = formData(path)
        headers['Content-Type'] = data.content_type
        #请求头必须包含一个特殊的头信息，类似于Content-Type: multipart/form-data; boundary=${bound}
        r = requests.post(url, data=data,cookies=parseCookie(ck), headers=headers)
        print(path,r.json())

if __name__=='__main__':
    args = sys.argv[1:]
    li = []
    for arg in args:
        if os.path.isdir(arg):handleDir(arg)
        else :li.append(arg)
    else:
        li = [makePack(i) for i in li]
        doLst(li)
