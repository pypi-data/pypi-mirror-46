#-*- coding:utf-8 -*-

import honey.base.util.__string as _string
import os
import subprocess

#!!如果在linux体系模式下，可以使用commands这个python库

def execute(cmd):
    return os.popen(cmd).read()

def execute_async(cmd):
    os.popen(cmd)

def execute_subprocess(cmd):
    p = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    res = p.communicate()[0]
    return res

# command模块只使用与linux的shell模式下
#
# 在我们平时码字时，经常需要调用系统脚本或者系统命令来解决很多问题，接下来我们就介绍给大家一个很好用的模块command，可以通过python调用系统命令，调用系统命令command模块提供了三种方法：cmd代表系统命令
#
# 1.commands.getoutput(cmd)
# 只返回执行shell命令的结果：
#
# 举个例子：
#
# [root@localhost ~]# cat a.py

#!/usr/bin/env python

#-*- coding:utf-8 -*-


# import commands
#
#  
#
# cmd = 'ls /home/admin'
#
# a = commands.getoutput(cmd)
#
# print(type(a))
#
# print(a)
#
#  
#
# 结果：
#
# [root@localhost ~]# python a.py
#
# <type 'str'>
#
# nginx.conf
#
# nginx_upstream_check_module-master.zip
#
# test.py
#
# commands是提供linux系统环境下支持使用shell命令的一个模块，在企业中，我们很多的脚本和环境都是在linux系统中跑起来的，
#
# 2.commands.getstatusoutput(cmd)
#
# 在上面我们在执行shell命令的时候，我们的shell命令可能执行报错，或者异常退出，我们就要有一个条件来判断shell最终执行的结果是什么，commands.getstatusoutput(cmd)的返回结果有两个值，
#
# [root@localhost ~]# cat c.py
#
# #!/usr/bin/env python
#
# #-*- coding:utf-8 -*-
#
# import commands
#
# cmd = 'ls /home/admin'
#
# c = commands.getstatusoutput(cmd)
#
# print(type(c))
#
# status, output =commands.getstatusoutput(cmd)
#
# print(status)
#
# print(output)
#
# print(type(output))
#
# 结果：
#
# [root@localhost ~]# python c.py
#
# <type 'tuple'>
#
# 0
#
# nginx.conf
#
# nginx_upstream_check_module-master.zip
#
# test.py
#
# <type 'str'>
#
# 解释：
#
# Commands.getstatusoutput(cmd)的返回结果是一个tuple，第一个值是shell执行的结果，如果shell执行成功，返回0，否则，为非0，第二个是一个字符串，就是我们shell命令的执行结果，python通过一一对应的方式复制给status和output，这个就是python语言的额巧妙之处。
