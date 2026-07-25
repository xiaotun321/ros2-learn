#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@作者: 古月居(www.guyuehome.com)
@说明: ROS2动作示例-请求执行圆周运动动作的客户端
"""

import rclpy                                      # ROS2 Python接口库
from rclpy.node   import Node                     # ROS2 节点类
from rclpy.action import ActionClient             # ROS2 动作客户端类

from learning_interface.action import MoveCircle  # 自定义的圆周运动接口

class MoveCircleActionClient(Node):
    def __init__(self, name):
        super().__init__(name)                   # ROS2节点父类初始化
        self._action_client = ActionClient(      # 2.1、创建动作客户端（接口类型、动作名）
            self, MoveCircle, 'move_circle') 

    def send_goal(self, enable):                 # 创建一个发送动作目标的函数
        goal_msg = MoveCircle.Goal()             # 3.1、创建一个动作目标的消息
        goal_msg.enable = enable                 # 设置动作目标为使能，希望机器人开始运动


        self._action_client.wait_for_server()    # 3.2、等待动作的服务器端启动【阻塞轮询在 DDS 分布式网络中发现动作服务端，找到同名、同接口类型的动作服务节点，才返回 True】与service不同，action是一个长时间的过程，客户端发送目标后，服务端会周期性反馈执行状态，直到最终结果返回给客户端。
        self._send_goal_future = self._action_client.send_goal_async(   # 3.3、异步方式发送动作的目标(动作目标, 处理周期反馈消息的回调函数)
            goal_msg,                                                   
            feedback_callback=self.feedback_callback)                   
                          
        self._send_goal_future.add_done_callback(self.goal_response_callback) # 设置一个服务器收到目标之后反馈时的回调函数
                                                                              # 配套的回调——等待服务端是否接收这个 Goal（接受 / 拒绝任务）
    # 第一层回调
    def goal_response_callback(self, future):           # 创建一个服务器收到目标之后反馈时的回调函数
        goal_handle = future.result()                   # 接收动作的结果 【这里只是得到Goal，拿不到 finish 结果，只有任务被接受之后，利用 goal\handle 再调用 `get_result_async()` 才能拿到最终结果】
        if not goal_handle.accepted:                    # 如果动作被拒绝执行
            self.get_logger().info('Goal rejected :(')
            return

        self.get_logger().info('Goal accepted :)')                            # 动作被顺利执行

        self._get_result_future = goal_handle.get_result_async()              # 异步获取动作最终执行的结果反馈
        self._get_result_future.add_done_callback(self.get_result_callback)   # 设置一个收到最终结果的回调函数 

    # 实时反馈回调(持续推送角度)
    def get_result_callback(self, future):                                    # 创建一个收到最终结果的回调函数
        result = future.result().result                                       # 读取动作执行的结果
        self.get_logger().info('Result: {%d}' % result.finish)                # 日志输出执行结果

    # 最终结果回调(任务全部跑完)
    def feedback_callback(self, feedback_msg):                                # 创建处理周期反馈消息的回调函数
        feedback = feedback_msg.feedback                                      # 读取反馈的数据
        self.get_logger().info('Received feedback: {%d}' % feedback.state) 

def main(args=None):                                       # ROS2节点主入口main函数
    rclpy.init(args=args)                                  # 1、ROS2 Python接口初始化
    node = MoveCircleActionClient("action_move_client")    # 2、创建ROS2节点对象并进行初始化
    node.send_goal(True)                                   # 3、发送动作目标
    rclpy.spin(node)                                       # 循环等待ROS2退出
    node.destroy_node()                                    # 销毁节点对象
    rclpy.shutdown()                                       # 关闭ROS2 Python接口
