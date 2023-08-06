#-*- utf8 -*-

#zkpython的简单封装，主要是为了业务上更方便的做统一配置中心的管理

# >> > import zookeeper
# >> > zk = zookeeper.init("localhost:2181")  # 初始化zookeeper连接
#
# # 创建zookeeper节点
# >> > zookeeper.create(zk, "/zk_for_py", "mydata1", [{"perms": 4, "scheme": "world", "id": "anyone"}], 0)
# '/zk_for_py'
#
# # 获取'/'下面的所以节点
#
# >> > zookeeper.get_children(zk, "/", None)
# ['app', 'zookeeper', 'zk_for_py']
# # 创建zookepper节点
# >> > zookeeper.create(zk, "/zk_for_py1", "mydata1", [{"perms": 0x1f, "scheme": "world", "id": "anyone"}], 0)
# '/zk_for_py1'
#
# # 获取节点信息
# >> > zookeeper.get(zk, "/zk_for_py1")
# ('mydata1', {'pzxid': 9L, 'ctime': 1398512377068L, 'aversion': 0, 'mzxid': 9L, 'numChildren': 0, 'ephemeralOwner': 0L,
#              'version': 0, 'dataLength': 7, 'mtime': 1398512377068L, 'cversion': 0, 'czxid': 9L})
# >> > zookeeper.get_children(zk, "/zk_for_py1", None)
# []
#
# >> > zookeeper.get_children(zk, "/")
# ['app', 'zookeeper', 'zk_for_py1', 'zk_for_py']
# # 节点的数据只能是字符串
# >> > zookeeper.set(zk, "/zk_for_py1", {"k": "v"})
# Traceback(most
# recent
# call
# last):
# File
# "<stdin>", line
# 1, in < module >
# TypeError: must
# be
# string or read - only
# buffer, not dict
# >> > zookeeper.set(zk, "/zk_for_py1", "hello")
# 0
# >> > zookeeper.get(zk, "/zk_for_py1")
# ('hello', {'pzxid': 9L, 'ctime': 1398512377068L, 'aversion': 0, 'mzxid': 10L, 'numChildren': 0, 'ephemeralOwner': 0L,
#            'version': 1, 'dataLength': 5, 'mtime': 1398512533595L, 'cversion': 0, 'czxid': 9L})
# >> > zookeeper.delete(zk, "zk_for_py")
# Traceback(most
# recent
# call
# last):
# File
# "<stdin>", line
# 1, in < module >
# zookeeper.BadArgumentsException: bad
# arguments
# >> > zookeeper.delete(zk, "/zk_for_py")
# 0
# >> > zookeeper.get(zk, "/zk_for_py1")
# ('hello', {'pzxid': 9L, 'ctime': 1398512377068L, 'aversion': 0, 'mzxid': 10L, 'numChildren': 0, 'ephemeralOwner': 0L,
#            'version': 1, 'dataLength': 5, 'mtime': 1398512533595L, 'cversion': 0, 'czxid': 9L})
#
# 复制代码
# 这是可以新开一个shell页面，在python中再初始化一个连接，可以获取前面set的数据“hello
# "
#
# 复制代码
# >> > import zookeeper
# >> > zk = zookeeper.init("localhost:2181")
#
# >> > zookeeper.get(zk, "/zk_for_py1")
# ('hello', {'pzxid': 9L, 'ctime': 1398512377068L, 'aversion': 0, 'mzxid': 10L, 'numChildren': 0, 'ephemeralOwner': 0L,
#            'version': 1, 'dataLength': 5, 'mtime': 1398512533595L, 'cversion': 0, 'czxid': 9L})
# # 定义一个监听器
# >> > def myWatch(zk, type, state, path):
#     ...
#     print
#     "zk:", str(type), str(state), str(path)
#
#
# ...
# zookeeper.get(zk, path, myWatch)
# ...
# >> > data = zookeeper.get(zk, "/zk_for_py1", myWatch)  # 设定监听节点
# # 当在上面的shell中改变这个节点的数据时，这个shell就会有这样的输出
# >> > TypeError: 'str'
# object is not callable
#
# zk: 3
# 3 / zk_for_py1
# zk: 3
# 3 / zk_for_py1
# 复制代码
# 创建节点说明：
#
# zookeeper.create(self.handle, path, data, [acl2], flags)
# zk创建节点的api，flags可以为EPHEMERAL
# SEQUENCE
# 或0，如果设置为EPHEMERAL ，这个节点只会短暂存在，即过期就好被删除，过期的时间为session的时间，SEQUENCE
# a
# unique
# monotonically
# increasing
# sequence
# number is appended
# to
# the
# path
# name ，可能是排序的意思。
#
#
#
# zookeeper.create(handler, "/zkpython_create_node", "mydata1", [{"perms": 0x1f, "scheme": "world", "id": "anyone"}]), 0);
#
# 这个地方需要详细的解释一下, 第一个参数就是我们刚才建立的链接, 第二个参数是创建的节点的路径, 第三个是创建的节点的数据, 第四个是acl(zookeeper中的访问控制列表), 第四个是创建的节点的类型(0
# 表示持久化的, 1
# 表示持久化 + 序号, 2
# 表示瞬时的, 3
# 表示瞬时加序号型的)
#
# 好...疑问来了, acl的描述为什么是这样的, 首先第一个参数是perms, 这个代表了控制这个节点的权限, 具体值参考如下:
#
# int
# READ = 1 << 0;
# int
# WRITE = 1 << 1;
# int
# CREATE = 1 << 2;
# int
# DELETE = 1 << 3;
# int
# ADMIN = 1 << 4;
# 也就是说, 这是一个数字, 而我们例子中为什么是1f呢?实际上就是
# READ | WRITE | CREATE | DELETE | ADMIN的结果, 这下明白是什么意思了吧??好, 后面还有两个参数, 实际上现在java和c的api中定义的值只有两种, 除了例子中的还有一种是
#
# "scheme": "auth", "id": ""
# 组合的, 但是实际上, 官方的文档中是有四种的, 有兴趣的同学可以参考:
#
# http: // zookeeper.apache.org / doc / trunk / zookeeperProgrammers.html
# 里的内容
#
# 监听器说明：
#
# 首先, 我们先要定义一个watch方法, 比如这里的myWatch方法, 之后在调用get方法的时候, 把这个watch传递进去就可以了
#
# 接下来详细解释下watcher中的各个参数的意思
#
# handler: 就是我们创建连接之后的返回值, 我试了下, 发现好像指的是连接的一个索引值, 以0开始
#
# type: 事件类型, -1
# 表示没有事件发生, 1
# 表示创建节点, 2
# 表示节点删除, 3
# 表示节点数据被改变, 4
# 表示子节点发生变化
#
# state: 客户端的状态, 0: 断开连接状态, 3: 正常连接的状态, 4
# 认证失败, -112: 过期啦
#
# path: 这个状态就不用解释了, znode的路径
#
# 参考资料：http: // justfansty.blog.sohu.com / 218331818.
# html
#
# http: // justfansty.blog.sohu.com / 217953183.
# html
#
# http: // blog.csdn.net / chenyi8888 / article / details / 6626302