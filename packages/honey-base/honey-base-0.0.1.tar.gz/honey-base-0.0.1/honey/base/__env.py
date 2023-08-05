#coding:utf8
#所有的Class都继承该类，方便进行python各个版本的兼容处理

import sys


def get_python_version():
    print(sys.version)