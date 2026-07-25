#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@作者: 古月居(www.guyuehome.com)
@说明: ROS2话题示例-订阅“Hello World”话题消息
"""

import rclpy                                     # ROS2 Python接口库
from rclpy.node   import Node                    # ROS2 节点类
from std_msgs.msg import String                  # ROS2标准定义的String消息

"""
创建一个订阅者节点
"""
class SubscriberNode(Node):
    
    def __init__(self, name):
        super().__init__(name)                                    # ROS2节点父类初始化
        self.sub = self.create_subscription(\
            String, "chatter", self.listener_callback, 10)        # 3、创建订阅者对象（消息类型、话题名、订阅者回调函数、队列长度）【向ROS系统登记: 我要监听chatter话题，收到消息就调用回调函数】
                                                                  #    向ros2系统注册一个订阅者对象，订阅名为“chatter”的话题消息,消息类型String
                                                                  #    rclpy.spin(node)持续循环节点内部事件，收到发布方发来的话题数据，ROS2底层接收二进制数据包，自动按照String消息类型进行序列化，生成 std_msgs.msg.String类型的实例对象
                                                                  #    ROS2内部自动调用定义的回调函数，把实例传给形参 msg

    def listener_callback(self, msg):                             # 4、创建回调函数，执行收到话题消息后对数据的处理
                                                                  #    msg 是回调函数的形式参数，名字你可以随便改（比如改成message）
        self.get_logger().info('I heard: "%s"' % msg.data)        # 输出日志信息，提示订阅收到的话题消息 
        
def main(args=None):                                 # ROS2节点主入口main函数
    rclpy.init(args=args)                            # 1、ROS2 Python接口初始化【ROS2上下文初始化】
    node = SubscriberNode("topic_helloworld_sub")    # 2、创建ROS2节点对象并进行初始化
    rclpy.spin(node)                                 # 循环等待ROS2退出
    node.destroy_node()                              # 5、销毁节点对象
    rclpy.shutdown()                                 # 关闭ROS2 Python接口
'''
rclpy.spin(node) 是 ROS 2 的 事件循环机制，它背后是通过 ROS 2 的 执行器(Executor)模型 实现的。 
rclpy.spin(node) node 就是节点实例的对象，会持续轮询这个节点内部所有待处理事件：
- 收到订阅话题 → 执行订阅回调
- 定时器时间到达 → 执行定时器回调
- 服务、动作客户端 / 服务端回调等
'''