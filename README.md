# 发表博客的工具
>利用api或者cookie发表博客,目前支持csdn

## 为什么有它?
我在很多网站上都有博客,当发表博客时,每个网站都要更新,太累了,为了避免重复操作,所以想b通过程序自动发博客
同时, 这个repo 还有其他一些小工具, 比如 picPost可以检查文章中的本地图片链接, 然后上传到七牛云

## 需要些什么?

### blog-sender
* python3
* python 模块
    - requests
    - markdown (可选)
    

### picPost(可选)
* qshell: 七牛云的一个命令行工具
* 七牛云账号

## 怎么使用?
```
git clone  git@github.com:mbinary/blog-sender.git
cd blog-sender
# pip3 install markdown 可选
vim config.py  # 配置必要参数
python3 blogSender.py  file1  file2 ...
```
这是配置参数的页面,有详细介绍

![](src/conf.png)

注意写文章的时候可以带上元信息,像hexo文章那样
如果没有,那么就是默认的了.
```
---

title: ABOUT
categories: 总结
tags: [blog,me]

---
```

## 未来的可能
有需求再添加功能吧 :see-no-evil:

## 欢迎fork & PR

## LICENCE
[MIT](LICENCE-MIT.txt)

## 联系我
* mail: <img style="display:inline" src="http://ounix1xcw.bkt.clouddn.com/gmail.png"></img>
* QQ  : 414313516 
