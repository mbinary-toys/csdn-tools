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
               'client_secret': '********************************',
               'grant_type': 'password',
               'username': 'marvellousbinary',
               'password': 'R**********'
                }

CSDN_COOKIE = '''
                
              '''

# markdown 语法, 需pip install markdown
MDON  = True
