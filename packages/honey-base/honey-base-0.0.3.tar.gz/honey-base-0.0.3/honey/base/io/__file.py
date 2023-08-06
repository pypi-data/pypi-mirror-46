#coding:utf8
#文件写入功能

import honey.base.log.__log as _log
import os
import honey.base.cmn.__env as _env
import honey.base.util.__string as _string

LINE_SEPERATOR = "\n"

class FileWriter(object):

    #如果要追加则使用a+
    def __init__(self,filename,mode="w+"):
        self.filename = filename
        parent_dir = get_parentdir(filename)
        if parent_dir != None:
            mkdirs(parent_dir)
        self.fp = open(filename,"w+")
        #__init__ should return None

    def writelines(self,lines):
        for line in lines:
            self.writeline(line)

    def writeline(self,line):
        self.writestr(line+LINE_SEPERATOR)

    def write(self,s):
        self.fp.write(s)

    def writestr(self,str):
        self.fp.write(str)

    def flush(self):
        self.fp.flush()

    def close(self):
        self.fp.close()

    def __enter__(self):
        _log.info("filewriter enter the file->" + self.filename)
        return self

    def __exit__(self, a, b, c):
        #destory
        self.fp.close()
        _log.info("filewriter close the file->" + self.filename)

class FileReader(object):

    def __init__(self,filename,mode="r+"):
        self.filename = filename
        parent_dir = get_parentdir(filename)
        if parent_dir != None:
            mkdirs(parent_dir)
        self.fp = open(filename,mode)

    def readline(self):
        return self.fp.readline()

    def readlines(self):
        return self.fp.readlines()

    def read(self):
        return self.read()

    def readline_withcallback(self,callback):
        while True:
            #在文件中，如果遇到一个空白行，readline()并不会返回一个空串，因为每一行的末尾还有一个或多个分隔符，因此“空白行”至少会有一个换行符或者系统使用的其他符号。只有当真的读到文件末尾时，才会读到空串""。
            line = self.fp.readline()
            if not line:
                break
            callback(self.filename,line)

    def __enter__(self):
        #with
        _log.info("filereader enter the file->" + self.filename)
        return self

    def __exit__(self, a, b, c):
        #destory
        _log.info("filereader close the file->" + self.filename)

def get_parentdir(filename):
    # sep = "\" ? if env.is_windows() else "/"
    sep = "/"
    if _env.is_windows():
        sep = "\\"
    if not sep in filename:
        return None
    last_index = _string.last_indexof(filename,sep)
    dest_dir = filename[0:last_index]
    if _string.is_blank(dest_dir):
        return None
    return dest_dir

def mkdirs(dirs):
    if os.path.exists(dirs):
        return
    os.makedirs(dirs)

def mkdir(dir):
    if os.path.exists(dir):
        return
    os.mkdir(dir)

def rmdir(dir):
    if not os.path.exists(dir):
        return
    os.rmdir(dir)

#删除多级目录
def removedirs(dir):
    os.removedirs(dir)

def rmfile(file):
    #如果不是一个文件
    if not os.path.isfile(file):
        return
    os.remove(file)

def touch(filename):
    dirs = get_parentdir(filename)
    if dirs != None:
        mkdirs(dirs)
    with open(filename,"w+") as f:
        _log.info("success create file->" + filename)

