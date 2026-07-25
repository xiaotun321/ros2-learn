#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@作者: 古月居(www.guyuehome.com)
@说明: ROS2服务示例-提供加法器的服务器处理功能
"""

import rclpy                                     # ROS2 Python接口库
from rclpy.node   import Node                    # ROS2 节点类
from learning_interface.srv import AddTwoInts    # 自定义的服务接口

class adderServer(Node):
    def __init__(self, name):
        super().__init__(name)                                                             # ROS2节点父类初始化
        self.srv = self.create_service(AddTwoInts, 'add_two_ints', self.adder_callback)    # 3、创建服务器对象（接口类型、服务名、服务器回调函数）
                                                                                           #  向ros2系统注册一个服务对象，即服务节点向 DDS 发布通信公告,在分布式网络里登记：
                                                                                           #  我是一个服务节点，我提供一个名为“add_two_ints”的服务，服务接口类型是AddTwoInts，收到请求后调用回调函数 adder_callback

    def adder_callback(self, request, response):                                           # 创建回调函数，执行收到请求后对数据的处理
        response.sum = request.a + request.b                                               # 完成加法求和计算，将结果放到反馈的数据中
        self.get_logger().info('Incoming request\na: %d b: %d' % (request.a, request.b))   # 输出日志信息，提示已经完成加法求和计算
        return response                                                                    # 反馈应答信息

def main(args=None):                                 # ROS2节点主入口main函数
    rclpy.init(args=args)                            # 1、ROS2 Python接口初始化
    node = adderServer("service_adder_server")       # 2、创建ROS2节点对象并进行初始化
    rclpy.spin(node)                                 # 循环等待ROS2退出【持续等待客户端请求】
    node.destroy_node()                              # 销毁节点对象
    rclpy.shutdown()                                 # 关闭ROS2 Python接口
'''
spin 内部不停循环调用 spin_once()，持续查询节点的事件队列，队列里存放：订阅消息、定时器、服务请求等待处理任务。
客户端发起请求 → DDS 传输 → 服务端事件队列存入任务 →
spin 检测到任务 → 自动运行服务回调 → 返回响应给客户端。
'''