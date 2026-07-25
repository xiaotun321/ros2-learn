#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@作者: 古月居(www.guyuehome.com)
@说明: ROS2服务示例-发送两个加数，请求加法器计算
"""

import sys

import rclpy                                                                      # ROS2 Python接口库
from rclpy.node   import Node                                                     # ROS2 节点类
from learning_interface.srv import AddTwoInts                                     # 自定义的服务接口

class adderClient(Node):
    def __init__(self, name):
        super().__init__(name)                                                    # ROS2节点父类初始化
        self.client = self.create_client(AddTwoInts, 'add_two_ints')              # 2、创建服务客户端对象（服务接口类型，服务名）
                                                                                  # 然后登记想要寻找的服务名与类型(此时不知道服务端在不在)

        while not self.client.wait_for_service(timeout_sec=1.0):                  # 循环等待服务器端成功启动 【查询DDS内部服务注册表，搜寻名称 = `add_two_ints` 并且类型 = `AddTwoInts` 的服务端 成功返回True】
            self.get_logger().info('service not available, waiting again...') 
        self.request = AddTwoInts.Request()                                       # 创建服务请求的数据对象
                                                                                  # （服务接口类型的Request类）【Request类是由ROS2自动生成的，里面包含了服务请求的参数】
                    
    def send_request(self):                                                       # 创建一个发送服务请求的函数
        self.request.a = int(sys.argv[1])
        self.request.b = int(sys.argv[2])
        self.future = self.client.call_async(self.request)                        # 3、异步方式发送服务请求,不需要一直等待数据返回
                                                                                  # call_async() 会立即返回一个 future 对象，这个对象原生自带：
                                                                                  # done() 方法，表示数据是否处理完成；
                                                                                  # result() 方法，表示获取服务端的反馈数据。   
                                                                                  # exception() 方法查看是否发生异常


def main(args=None):
    rclpy.init(args=args)                                                         # ROS2 Python接口初始化
    node = adderClient("service_adder_client")                                    # 1、创建ROS2节点对象并进行初始化
    node.send_request()                                                           # 发送服务请求
    
    while rclpy.ok():                                                             # ROS2系统正常运行
        rclpy.spin_once(node)                                                     # 循环执行一次节点

        if node.future.done():                                                    # 数据是否处理完成
            try:
                response = node.future.result()                                   # 接收服务器端的反馈数据
            except Exception as e:
                node.get_logger().info(
                    'Service call failed %r' % (e,))
            else:
                node.get_logger().info(                                           # 将收到的反馈信息打印输出
                    'Result of add_two_ints: for %d + %d = %d' % 
                    (node.request.a, node.request.b, response.sum))
            break
            
    node.destroy_node()                                                           # 销毁节点对象
    rclpy.shutdown()                                                              # 关闭ROS2 Python接口
'''
1. 先启动客户端：
    `create_client()` → 开始搜寻服务；
    `wait_for_service()` 不断查询 DDS 表，打印等待日志。
2. 新开终端启动服务端：
    `create_service()` → 向 DDS 注册自己。
3. DDS 自动同步信息给客户端。
4. 客户端下一轮 `wait_for_service()` 查询时，检测到服务 → 返回 True, 退出循环。
5. 客户端构造 request, 发起 call_async 调用。
6. 服务端收到请求，依靠 spin 运行服务回调，计算结果返回 response。
7. 客户端依靠 spin 收到应答, future 获取结果。
'''