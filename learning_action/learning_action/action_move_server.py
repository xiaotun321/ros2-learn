#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@作者: 古月居(www.guyuehome.com)
@说明: ROS2动作示例-负责执行圆周运动动作的服务端
"""

import time

import rclpy                                      # ROS2 Python接口库
from rclpy.node   import Node                     # ROS2 节点类
from rclpy.action import ActionServer             # ROS2 动作服务器类
from learning_interface.action import MoveCircle  # 自定义的圆周运动接口

class MoveCircleActionServer(Node):
    def __init__(self, name):
        super().__init__(name)                   # ROS2节点父类初始化
        self._action_server = ActionServer(      # 2.1、创建动作服务器（接口类型、动作名、回调函数） 
                                                 # 向DDS注册一个动作服务端，告诉DDS网络：我提供一个名为“move_circle”的动作服务，接口类型是MoveCircle，收到客户端Goal后调用 execute_callback 回调函数。
            self,
            MoveCircle,
            'move_circle',
            self.execute_callback)

    def execute_callback(self, goal_handle):            # 2.2、执行收到动作目标Goal之后的处理函数
                                                        # 当客户端 Goal 到达：
                                                        # 1、rclpy 内部先进入Goal 接收校验阶段；
                                                        # 2、默认策略：自动回复 Accepted 给客户端；
                                                        # 3、然后进入 execute_callback 回调函数，执行具体的动作处理逻辑。【这些都是在底层自动完成的】
        self.get_logger().info('Moving circle...')
        feedback_msg = MoveCircle.Feedback()            # 创建一个动作反馈信息的消息

        for i in range(0, 360, 30):                     # 从0到360度，执行圆周运动，并周期反馈信息
            feedback_msg.state = i                      # 创建反馈信息，表示当前执行到的角度
            self.get_logger().info('Publishing feedback: %d' % feedback_msg.state)
            goal_handle.publish_feedback(feedback_msg)  # 发布反馈信息  【持续不断发布Feedback 实时角度】
            time.sleep(0.5)

        goal_handle.succeed()                           # 动作执行成功
        result = MoveCircle.Result()                    # 创建结果消息
        result.finish = True                            
        return result                                   # 反馈最终动作执行的结果

def main(args=None):                                       # ROS2节点主入口main函数
    rclpy.init(args=args)                                  # 1、ROS2 Python接口初始化
    node = MoveCircleActionServer("action_move_server")    # 2、创建ROS2节点对象并进行初始化
    rclpy.spin(node)                                       # 循环等待ROS2退出
    node.destroy_node()                                    # 销毁节点对象
    rclpy.shutdown()                                       # 关闭ROS2 Python接口
