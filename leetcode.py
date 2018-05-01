#coding: utf-8
import os
import re
import sys


path = sys.argv[1]
s=None
with open(path,'r') as f:
    s = f.read()

pt = re.compile(r'\/a>[\n\s]+\*\s+##\s+\[(.*?)\]\((.*?)\).*?--leetcode (\d+)\n(.*?)\*\*代码\*\*.*?```\w+(.*?)```',re.DOTALL)
li = pt.findall(s)
ct=0


for i in li:
    ct+=1
    name,href,num,cont,code =  i
    fileName = 'leetcode/[一起来刷leetcode吧][{ct}]--No.{num}  {name}'.format(ct=ct,num=num,name=name)
    with open(fileName,'w') as f:
        f.write('''---\ncategories: leetcode\ntags: [python,leetcode,os]\nchannel:16\n---\n''')
        f.write('这是leetcode的[第{num}题]({href})--{name}\n\n'.format(href = href,num=num,name=name))
        f.write(cont)
        f.write('\n## show me the code\n```python\n')
        f.write(code)
        f.write('```\n')
