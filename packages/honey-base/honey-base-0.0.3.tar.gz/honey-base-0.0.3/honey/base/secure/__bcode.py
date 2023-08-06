#coding:utf8

import base64

def encode64(str):
    return base64.b64encode(str.encode('utf-8'))

def decode64(str):
    return base64.b64decode(str.encode("utf-8"))