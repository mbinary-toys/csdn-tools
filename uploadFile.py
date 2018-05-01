#coding: utf-8
'''************************************************************************
    > File Name: uploadFile.py
    > Author: mbinary
    > Mail: zhuheqin1@gmail.com 
    > Blog: https://mbinary.github.io
    > Created Time: Sun 08 Apr 2018 11:04:17 PM DST
 ************************************************************************'''
import os, random, sys, requests
from requests_toolbelt.multipart.encoder import MultipartEncoder

url = 'https://download.csdn.net/upload/do_upload'
files = sys.argv[1:]
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
def formData(path):
    name = getName(path)
    return  MultipartEncoder(
            fields={
                    'txt_title':name*(50//len(name)),
                     'sel_filetype':'3',# nota all value should be str
                    'txt_tag': '工具书籍',
                     'sel_primary':'15',
                     'sel_subclass': '15013',
                     'sel_score':'2',
                     'txt_desc':name*20,
                     'txt_userfile': (os.path.basename(path) ,open(path, 'rb'),'text/plain')#'application/X-zip-compressed'  
                    }
   # boundary='-----------------------------' + str(random.randint(1e28, 1e29 - 1))
    )


from config import CSDN_UPLOAD_COOKIE as ck
for path in files:
    data = formData(path)
    headers['Content-Type'] = data.content_type
    #请求头必须包含一个特殊的头信息，类似于Content-Type: multipart/form-data; boundary=${bound}
    r = requests.post(url, data=data,cookies=parseCookie(ck), headers=headers)
    print(path,r.json())
