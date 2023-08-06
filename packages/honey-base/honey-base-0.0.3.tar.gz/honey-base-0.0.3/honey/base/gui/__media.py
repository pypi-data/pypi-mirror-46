#coding:utf8
#多媒体显示某块，如图片、声音、视频、文字

import numpy
import cv2
import PIL
from PIL import Image as Image
import matplotlib.pyplot as plt


def show(obj,title="default"):
    #在ndarray这类对象用如下判断是错误的
    #ValueError: The truth value of an array with more than one element is ambiguous. Use a.any() or a.all()
    # if obj == None:
    #     return
    #if not obj:
    #    return
    #Python中会把下面几种情况当做空值来处理:None,False,(0,0.0,0L),'',(),[],{}
    # if not any(obj):
    #     return
    # if all(obj):
    #     return
    # (obj == [0, 1, 2]).all()
    typename = str(type(obj))
    # if isinstance(obj,PIL.JpegImagePlugin.JpegImageFile):
    if "PIL.JpegImagePlugin.JpegImageFile" in typename:
        obj.show()
    # elif isinstance(obj,numpy.ndarray):
    elif "numpy.ndarray" in typename:
        #1.使用opencv来显示图片
        # cv2.imshow(title,obj)
        # k = cv2.waitKey()
        # if k == 27:  # wait for ESC key to exit
        #     cv2.destroyAllWindows()
        # elif k == ord('s'):  # wait for 's' key to save and exit
        #     cv2.imwrite('newimage.img',obj)
        #     cv2.destroyAllWindows()
        #2.使用matplot来显示图片
        plt.imshow(obj)
        plt.show()