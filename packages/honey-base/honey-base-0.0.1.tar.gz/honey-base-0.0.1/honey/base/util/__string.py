#coding:utf-8

import string

def contains_any(str,array=[]):
    return str in array

def is_empty(str):
    if str == None:
        return True
    return str == ''

def is_blank(str):
    if is_empty(str):
        return True
    return str.strip() == ''

def trim(str):
    if is_blank(str):
        return ''
    return str.strip()


