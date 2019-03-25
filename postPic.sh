#!/bin/bash
# debug on,  print exected cmds
set -x
bucket=mbinary
#`qin domains $bucket`
srcpath=/mnt/c/Users/mbinary/gitrepo/csapp-lab/bomb/src
#  ${repo}"/csapp/bomb/src"  get  /csapp/bomb/src   why?
post="csapp-bomb-lab-report.md"
path=/mnt/d/blog/blog/source/_posts/csapp-bomb-lab-report.md
read title < `sed  "s/title: \(.*\)/\1/p'  -n  $path"`

sed   's/!\[\(.*\)\](.*\/*\(.*\))/![\1](http:\/\/ounix1xcw.bkt.clouddn.com\/\2)/g'  $path  > $path

# notice that in regex: !, ()不需要转义,而[]要转义, 而且没有?非贪婪模式, 匹配组是从\1开始的


for file in `ls $srcpath`:
do
	#qin fput $bucket $file  $srcpath/$file
done

set +x
