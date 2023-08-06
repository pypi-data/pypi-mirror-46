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

def upper(str):
    if is_blank(str):
        return str
    return str.upper()

def lower(str):
    if is_blank(str):
        return str
    return str.lower()

def last_indexof(str,chars):
    last_position = -1
    while True:
        position = str.find(chars,last_position + 1)
        if position == -1:
            return last_position
        last_position = position
    return last_position

