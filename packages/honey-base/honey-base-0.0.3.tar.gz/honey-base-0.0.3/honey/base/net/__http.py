#coding:utf8

import urllib
import urllib3
from PIL import Image
import os, sys
from honey.base.secure import __hash as hash
import json

#把上一级目录加入系统路径
#lib_path = os.path.abspath(os.path.join('..'))
#sys.path.append(lib_path)
#from ..secure import md5

def download_file(url,dest_file,params={},throw_exp=False):
    http = urllib3.PoolManager()
    try:
        resp = http.request("GET", url,params)
        if resp.status == 200:
            with open(dest_file,"wb") as f:
                f.write(resp.data)
            return True
        else:
            raise Exception("download the url->" + url + ",failed")
    except Exception as e:
        if throw_exp:
            raise e
        else:
            print(e)
        return False
    finally:
        if resp:
            resp.release_conn()


def get_image(url,rgb=False,params={},throw_exp=False):
    tmp_dir = ".tmpdowns"
    if not os.path.exists(tmp_dir):
        os.mkdir(tmp_dir)
    filename = tmp_dir + "/" + hash.random_md5();

    download_file(url,filename,params,throw_exp);
    try:
        im = Image.open(filename);
        if rgb and im.format != "JPEG":
            #如果是RGBA格式的
            if len(im.split()) == 4:
                r, g, b, a = im.split()
                im = Image.merge("RGB", (r, g, b))
                # im.save(filename, "JPEG")
        return im
    except Exception as e:
        if throw_exp:
            raise e;
        else:
            print(e)
        return None
    finally:
        os.remove(filename)

def get_text(url,params={},throw_exp=False):
    http = urllib3.PoolManager()
    try:
        resp = http.request("GET",url,params)
        if resp.status == 200:
            return resp.data
        else:
            raise Exception("get the url->" + url + ",failed")
        return None
    except Exception as e:
        if throw_exp:
            raise e
        else:
            print(e)
        return None
    finally:
        if resp:
            resp.release_conn()

def get_json(url,params={},throw_exp=False):
    text = get_text(url,params,throw_exp)
    if not text:
        return None
    return json.loads(text)

def post(url,params={},throw_exp=False):
    http = urllib3.PoolManager()
    try:
        resp = http.request("POST",url,params)
        if resp.status == 200:
            return resp.data
        else:
            raise Exception("post the url->" + url + ",failed")
    except Exception as e:
        if throw_exp:
            raise e
        else:
            print(e)
        return None
    finally:
        if resp:
            resp.release_conn()

#自定制接口
def custom(method,url,params={},headers={},conn_timeout=10,read_timeout=20,proxy=None,throw_exp=False):
    #resp.data
    return None



