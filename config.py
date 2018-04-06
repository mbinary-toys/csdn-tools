#coding: utf-8
'''************************************************************************
    > File Name: config.py
    > Author: mbinary
    > Mail: zhuheqin1@gmail.com 
    > Created Time: Fri 06 Apr 2018 11:06:16 AM DST
 ************************************************************************'''

# python变量 配置参数


# 两者二选一
# CSDN_AUTH_DATA 在 使用api  需要在http://open.csdn.net/wiki/api/注册开发者,得到cliet_id 和 client_secret
# CSDN_COOKIE 在发博客页面获取cookie,     
CSDN_AUTH_DATA = {'client_id' :'1100668',
               'client_secret': '***',
               'grant_type': 'password',
               'username': 'marvellousbinary',
               'password': '***'
                }
# str
CSDN_COOKIE = '''
              
              '''

# markdown 语法, 需pip install markdown
MDON  = True


# xdefault configuration


DEFAULT_DATA = {
             "title":"do you know my name?",
             "content": '''<h1>hello, world~</h1>''',
             "categories":"默认分类",
             "channel":33,
             "tags":"python,tag2",
             }
             
'''
channel  各个值的含义
1:移动开发  
2:云计算大数据 
3:研发管理 
6:数据库
12:运维
14:前端
15:架构
16:编程语言
28:人工智能
29:物联网
30:游戏开发
31:后端
32:安全
33:程序人生
34:区块链
35:音视频开发
36:资讯
37:计算机理论与基础

'''      