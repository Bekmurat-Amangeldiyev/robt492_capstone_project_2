import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import socket
import json

class UDPTwistBridge(Node):
    def __init__(self):
        super().__init__('udp_twist_bridge')
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.target_ip = '192.168.0.35'  # IP of the Raspberry Pi
        self.target_port = 5005
        self.subscriber = self.create_subscription(
            Twist,
            '/cmd_vel',
            self.twist_callback,
            10
        )

    def twist_callback(self, msg):
        data = {
            'linear': {'x': msg.linear.x},
            'angular': {'z': msg.angular.z}
        }
        print("Sending UDP packet:", data)  # ADD THIS LINE
        self.sock.sendto(json.dumps(data).encode(), (self.target_ip, self.target_port))
        print("Data sent.")

def main(args=None):
    rclpy.init(args=args)
    node = UDPTwistBridge()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
