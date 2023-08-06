#!/usr/bin/env python
#-*- coding:utf8 -*-

import datetime
import time
#时间操作函数的封装

#2.7->32位：-2^31~2^31-1 64位：-2^63~2^63-1
#3.5->在3.5中init长度理论上是无限的
def current_milliseconds():
    return int(round(time.time() * 1000))