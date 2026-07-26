#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@作者: 古月居(www.guyuehome.com)
@说明: ROS2 TF示例-广播静态的坐标变换
"""

import rclpy                                                                 # ROS2 Python接口库
from rclpy.node import Node                                                  # ROS2 节点类
from geometry_msgs.msg import TransformStamped                               # 坐标变换消息
import tf_transformations                                                    # TF坐标变换库
from tf2_ros.static_transform_broadcaster import StaticTransformBroadcaster  # TF静态坐标系广播器类

class StaticTFBroadcaster(Node):
    def __init__(self, name):
        super().__init__(name)                                                  # ROS2节点父类初始化
        self.tf_broadcaster = StaticTransformBroadcaster(self)                  # 创建一个静态TF广播器对象
                                                                                # 内部自动创建一个Publisher, 目标话题 /tf_static

        static_transformStamped = TransformStamped()                            # 创建一个坐标变换的消息对象 消息对象,用来描述：父坐标系 → 子坐标系 的坐标变换。
                                                                                # 
        static_transformStamped.header.stamp = self.get_clock().now().to_msg()  # 设置坐标变换消息的时间戳
        static_transformStamped.header.frame_id = 'world'                       # 设置一个坐标变换的源坐标系(父坐标系-参考坐标系)
        static_transformStamped.child_frame_id  = 'house'                       # 设置一个坐标变换的目标坐标系(子坐标系) house 坐标系 在 world 坐标系下 的位置姿态

        # 平移：house原点相对world原点偏移
        static_transformStamped.transform.translation.x = 3.0                  # 设置坐标变换中的X、Y、Z向的平移
        static_transformStamped.transform.translation.y = 2.0                    
        static_transformStamped.transform.translation.z = 0.0

        # 欧拉角转四元数 roll,pitch,yaw(弧度） 函数输出顺序：`[x,y,z,w]`,用四元数表示旋转,避免欧拉角万向锁
        quat = tf_transformations.quaternion_from_euler(0.0, 0.0, 0.0)          # 将欧拉角转换为四元数(roll, pitch, yaw）
        static_transformStamped.transform.rotation.x = quat[0]                  # 设置坐标变换中的X、Y、Z向的旋转(四元数）,塞进消息发给 TF 系统,用来描述 house 坐标系朝向
        static_transformStamped.transform.rotation.y = quat[1]
        static_transformStamped.transform.rotation.z = quat[2]
        static_transformStamped.transform.rotation.w = quat[3]

        self.tf_broadcaster.sendTransform(static_transformStamped)              # 广播静态坐标变换,广播后两个坐标系的位置关系保持不变
                                                                                # 把这条坐标变换打包进 tf2_msgs/TFMessage 消息,发布到 /tf_static 话题, TF2 缓冲区永久保存这条坐标变换关系

def main(args=None):
    rclpy.init(args=args)                                # ROS2 Python接口初始化
    node = StaticTFBroadcaster("static_tf_broadcaster")  # 创建ROS2节点对象并进行初始化
    rclpy.spin(node)                                     # 循环等待ROS2退出
    node.destroy_node()                                  # 销毁节点对象
    rclpy.shutdown()
'''
静态TF——代表 两个坐标系相对位置永远不变 (机器人雷达、相机相对于底盘,world 里固定建筑物）。
静态变换只发送一次位置关系——节点启动发送一次,之后不再发送; TF2 缓冲永久保存这份关系,别的节点可以随着查询

以上代码的意思是,子坐标系相对父坐标系的位置,由于相对位置不变,只需发送一次位置关系
别的程序(TF 监听器）可以随时询问 TF2: 请告诉我 house 的原点在 world 坐标系下坐标是多少? TF2 直接返回 (10,5,0)
'''

'''
一个坐标系相对另一个坐标系的位置姿态,由两部分组合确定：
1. translation.x/y/z → 位置(3 个数）   —————— 子坐标系原点,在父坐标系里的 空间坐标。
2. rotation.x/y/z/w (四元数)→ 姿态(4 个数） ————— 子坐标系自身是朝哪个方向摆放的。子坐标系的坐标轴方向,在父坐标系里的朝向。
   roll(横滚)、pitch(俯仰)、yaw(偏航) → 分别是绕 x y z 旋转
   q = w + xi + yj + zk
'''


'''
ros2 run tf2_tools view_frames 
1. 收集当前所有 TF 坐标系关系
2. 在当前终端目录生成一份 frames.pdf
3. PDF 里面画出整张坐标系树(父子关系）
'''