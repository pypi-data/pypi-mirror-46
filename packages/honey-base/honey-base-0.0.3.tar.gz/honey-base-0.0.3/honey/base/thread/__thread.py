#coding:utf8
import threading



# some demos
# import time
# import threading
#
# class A(threading.Thread):
#     def __init__(self, args):
#         threading.Thread.__init__(self)
#         self.args = args
#
#     def run(self):
#         n = self.args
#         while n > 0:
#             print("n:", n)
#             n -= 1
#             time.sleep(1)
#
#
#
# if __name__=='__main__':
#
#     t = A(10)
#     t.start()
#     t.join()
#     print("exit")