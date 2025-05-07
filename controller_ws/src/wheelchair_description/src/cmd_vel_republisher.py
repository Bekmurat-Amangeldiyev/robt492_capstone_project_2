#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class CmdVelRepublisher(Node):
    def __init__(self):
        super().__init__('cmd_vel_republisher')
        # Input topic from Nav2
        self.input_topic = '/cmd_vel'
        # Output topic for the diff drive controller
        self.declare_parameter('output_topic', '/diff_drive_controller/cmd_vel_unstamped')
        self.output_topic = self.get_parameter('output_topic').get_parameter_value().string_value

        self.subscription = self.create_subscription(
            Twist,
            self.input_topic,
            self.listener_callback,
            10)
        self.publisher = self.create_publisher(Twist, self.output_topic, 10)
        self.get_logger().info(f"Republishing {self.input_topic} to {self.output_topic}")

    def listener_callback(self, msg):
        self.publisher.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = CmdVelRepublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()




