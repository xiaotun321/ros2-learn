from launch import LaunchDescription           # launch文件的描述类 承载所有待启动任务(节点、定时器、进程)
from launch_ros.actions import Node            # 节点启动的描述类  【专门描述一个ROS2节点如何启动 等价于 ros2 run xxx xxx】

def generate_launch_description():             # 自动生成launch文件的函数  【ros2启动launch时，自动调用这个函数，函数名固定。 函数需要返回LaunchDescription对象】
    return LaunchDescription([                 # 返回launch文件的描述信息
        Node(                                  # 配置一个节点的启动
            package='learning_topic',          # 节点所在的功能包
            executable='topic_helloworld_pub', # 节点的可执行文件
        ),
        Node(                                  # 配置一个节点的启动
            package='learning_topic',          # 节点所在的功能包
            executable='topic_helloworld_sub', # 节点的可执行文件名
        ),
    ])
