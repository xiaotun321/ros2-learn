#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@作者: 古月居(www.guyuehome.com)
@说明: ROS2参数示例-创建、读取、修改参数
"""

import rclpy                                     # ROS2 Python接口库
from rclpy.node   import Node                    # ROS2 节点类

class ParameterNode(Node):
    def __init__(self, name):
        super().__init__(name)                                    # ROS2节点父类初始化
        self.timer = self.create_timer(2, self.timer_callback)    # 创建一个定时器（单位为秒的周期，定时执行的回调函数）
        self.declare_parameter('robot_name', 'mbot')              # 2.1、创建一个参数，键名robot_name，并设置参数的默认值(若外部没有传来参数值，则使用默认值)
                                                                  # 向当前节点注册这个键名，告诉ROS2系统，这个节点有一个参数，键名为robot_name，默认值为mbot
                                                                  # 类似Python字典的键值对，键名为robot_name，键值为mbot (通过键名可以获得键值)
                                                                  

    def timer_callback(self):                                      # 创建定时器周期执行的回调函数
        robot_name_param = self.get_parameter('robot_name').get_parameter_value().string_value   # 2.2、从ROS2系统中读取参数的值

        self.get_logger().info('Hello %s!' % robot_name_param)     # 输出日志信息，打印读取到的参数值

        # 这里代码又重新设置参数值为mbot, 
        # new_name_param = rclpy.parameter.Parameter(                # 2.3、构造新参对象，重新将参数值设置为指定值(参数键名、参数类型(字符串)、参数新值)
        #                     'robot_name',   
        #                     rclpy.Parameter.Type.STRING, 
        #                     'mbot')
        # all_new_parameters = [new_name_param]                      # ROS2 的 set_parameters() 接收列表，支持一次性同时修改多个参数，所以要放到列表 [new_name_param] 里。
        # self.set_parameters(all_new_parameters)                    # 2.4、将重新创建的参数列表发送给ROS2系统
                                                                   

def main(args=None):                                 # ROS2节点主入口main函数
    rclpy.init(args=args)                            # 1、ROS2 Python接口初始化
    node = ParameterNode("param_declare")            # 2、创建ROS2节点对象并进行初始化
    rclpy.spin(node)                                 # 循环等待ROS2退出
    node.destroy_node()                              # 销毁节点对象
    rclpy.shutdown()                                 # 关闭ROS2 Python接口
'''
ros2 param set <节点名称> <参数键名> <新值>

ros2 param set param_declare robot_name turtle 
'''