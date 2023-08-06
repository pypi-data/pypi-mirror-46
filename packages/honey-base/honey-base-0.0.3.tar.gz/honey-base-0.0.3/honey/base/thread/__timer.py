#-*- coding:utf8 -*-

import threading

#timer定时器分clock定时器和quartz定时器
#APScheduler是基于Quartz的 一个Python定时任务框架，实现了Quartz的所有功能，使用起来十分方便。提供了基于日期、固定时间间隔以及crontab类型的任务，并且可以 持久化任务。基于这些功能，我们可以很方便的实现一个python定时任务系统



# timer = threading.Timer(5, func)
# timer.start()

# timer类
# 　　Timer（定时器）是Thread的派生类，用于在指定时间后调用一个方法。
#
# 构造方法：
# Timer(interval, function, args=[], kwargs={})
# 　　interval: 指定的时间
# 　　function: 要执行的方法
# 　　args/kwargs: 方法的参数