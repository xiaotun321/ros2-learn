#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@作者: 古月居(www.guyuehome.com)
@说明: ROS2服务示例-请求目标识别，等待目标位置应答
"""

import rclpy                                            # ROS2 Python接口库
from rclpy.node   import Node                           # ROS2 节点类
from learning_interface.srv import GetObjectPosition    # 自定义的服务接口

class objectClient(Node):
    def __init__(self, name):
        super().__init__(name)                                                                  # ROS2节点父类初始化
        self.client = self.create_client(GetObjectPosition, 'get_target_position')              # 2、创建服务客户端对象（服务接口类型，服务名）

        while not self.client.wait_for_service(timeout_sec=1.0):                                # 循环等待服务器端成功启动 【查询DDS内部服务注册表，搜寻名称 = `GetObjectPosition` 并且类型 = `get_target_position` 的服务端 成功返回True】
            self.get_logger().info('service not available, waiting again...')
        self.request = GetObjectPosition.Request()
                     
    def send_request(self):
        self.request.get = True
        self.future = self.client.call_async(self.request)                                      # 3、异步方式发送服务请求,不需要一直等待数据返回

def main(args=None):
    rclpy.init(args=args)                              # ROS2 Python接口初始化
    node = objectClient("service_object_client")       # 1、创建ROS2节点对象并进行初始化
    node.send_request()                                # 发送服务请求
    
    while rclpy.ok():
        rclpy.spin_once(node)

        if node.future.done():
            try:
                response = node.future.result()
            except Exception as e:
                node.get_logger().info(
                    'Service call failed %r' % (e,))
            else:
                node.get_logger().info(
                    'Result of object position:\n x: %d y: %d' %
                    (response.x, response.y))
            break
    node.destroy_node()                              # 销毁节点对象
    rclpy.shutdown()                                 # 关闭ROS2 Python接口
