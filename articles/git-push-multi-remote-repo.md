---
title: git-push到多个远程仓库,github,coding
data: 2018-4-5
categories: linux
tags: github,coding,git
keyword: 
description: 
top: 
---
我最近想把github上的仓库都推送到coding上,所以就了解了一下git

git是个优秀的版本控制软件(佩服Linus Torvalds ✪ ω ✪)
可以推送到多个远程仓库, 比如github, coding
## 关联多个仓库
只需要通过`git remote add   <refs>  <addr>`即可关联多个仓库
refs 指向远程仓库, 默认的就是origin, addr 就是仓库地址了,比如` git@git.coding.net:mbinary/netease-cached-music.git`

输入
`git remote add origin git@git.coding.net:mbinary/netease-cached-music.git`
报错
>fatal: remote origin already exists.

这是远程仓库的refs相同的原因, 可以换个名字,  比如cod
`git remote add cod git@git.coding.net:mbinary/netease-cached-music.git`
即可,然后就关联上了多个仓库, 可以通过git remote -v 查看,

![origin.png](https://upload-images.jianshu.io/upload_images/7130568-f6ce35394349e26b.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

 也可以进入 `.git/config`查看

 ![config.png](https://upload-images.jianshu.io/upload_images/7130568-e6859d0e887775cc.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
# 多个仓库的git push 
## 方法一--- 逐个push
 通过`git push --help`可以看到
 git push直接用的话默认的是push到origin , 


 ![gitpush.png](https://upload-images.jianshu.io/upload_images/7130568-46fd61f172ccbe4e.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


 所以要到不同仓库需要
 使用`git push  <refs> <branch>`多次

## 方法二-- 一条命令全部push
可以写个sh脚本处理

搜索发现还有另一种方法,
即在一个
ref下设置多个url

通过`git remote set-url --add origin git@git.coding.net:mbinary/netease-cached-music.git`
来关联新的远程仓库,
可以进入.git/config发现origin下新加入了这个远程仓库的url
```
[remote "origin"]
        url = git@github.com:mbinary/netease-cached-music.git
		fetch = +refs/heads/*:refs/remotes/origin/*
		url = git@git.coding.net:mbinary/netease-cached-music.git
```
这样`git push origin`就可以全部push到所有仓库
但是git pull 会出问题,只会pull第一个url的, 而且可能还会冲突,  所以这两种方法自己选择吧,如果不pull,显然方法2比较方便

