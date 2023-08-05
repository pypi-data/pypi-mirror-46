#coding:utf8

import hashlib
import time
import random

def md5(str):
    m = hashlib.md5()
    # strs必须指定要加密的字符串的字符编码
    m.update(str.encode("utf8"))
    return m.hexdigest();

def random_md5():
    return md5(str(random.random()) + str(int(round(time.time() * 1000))))

def sha256(str):
    sha256 = hashlib.sha256()
    sha256.update(str.encode('utf-8'))
    return sha256.hexdigest()

def sha384(str):
    sha384 = hashlib.sha384()
    sha384.update(str.encode('utf-8'))
    return sha384.hexdigest()

def sha512(str):
    sha512 = hashlib.sha512()
    sha512.update(str.encode('utf-8'))
    return sha512.hexdigest()

def sha1(str):
    shaa1 = hashlib.sha1()
    shaa1.update(str.encode('utf-8'))
    return shaa1.hexdigest()
    #或者使用byte转换为二进制
    #shab1 = hashlib.sha1()
    #shab1.update(bytes(str,encoding='utf-8'))
    #res = shab1.hexdigest()

def md5_withkey(str,key):
    high = hashlib.md5(key.encode("utf-8"))
    high.update(str.encode('utf-8'))
    return high.hexdigest()