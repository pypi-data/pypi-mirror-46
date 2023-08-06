#coding:utf8
#所有的Class都继承该类，方便进行python各个版本的兼容处理

import sys
import platform
import honey.base.util.__string as _string

def get_python_version():
    print(sys.version)

def osname():
    sysname = _string.lower(platform.system());
    if "windows" in sysname:
        return "windows"
    elif "macos" in sysname:
        return "macos"
    elif "darwin" in sysname:
        return "macos"
    else:
        return sysname

def uname():
    return platform.uname()

def is_windows():
    name = osname()
    return name == "windows"

def is_macos():
    name = osname()
    return name == "macos"


