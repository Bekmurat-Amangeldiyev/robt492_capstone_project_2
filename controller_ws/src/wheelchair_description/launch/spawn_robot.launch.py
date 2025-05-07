import os
import numpy as np
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from ament_index_python import get_package_prefix

def generate_launch_description():
    # Path to the URDF file
    urdf_file_path = os.path.join(
        get_package_share_directory('wheelchair_description'),  # Adjust package name as needed
        'urdf',
        'wheelchair.urdf'
    )
    pkg_share_path = os.pathsep + os.path.join(get_package_prefix('wheelchair_description'), 'share')
    if 'GAZEBO_MODEL_PATH' in os.environ:
      os.environ['GAZEBO_MODEL_PATH'] += pkg_share_path
    else:
      os.environ['GAZEBO_MODEL_PATH'] =  pkg_share_path
    # Launch configuration variables
    x_pose = LaunchConfiguration('x_pose', default='12.0')
    y_pose = LaunchConfiguration('y_pose', default='0.0')
    
    bridge_params = os.path.join(
    get_package_share_directory('wheelchair_description'),
    'config',
    'gz_bridge.yaml'
    )
    
    start_gazebo_ros_bridge_cmd = Node(
      package='ros_gz_bridge',
      executable='parameter_bridge',
      arguments=[
        '--ros-args',
        '-p',
        f'config_file:={bridge_params}',
    ],
    output='screen',
    )
    start_gazebo_ros_image_bridge_cmd = Node(
      package='ros_gz_image',
      executable='image_bridge',
      arguments=['/camera/image_raw'],
      output='screen',
    )
    # Declare the launch arguments
    declare_x_position_cmd = DeclareLaunchArgument(
        'x_pose', default_value='12.0',
        description='Specify X position of the robot'
    )

    declare_y_position_cmd = DeclareLaunchArgument(
        'y_pose', default_value='0.0',
        description='Specify Y position of the robot'
    )

    
    # Node to spawn the wheelchair robot in Gazebo
    start_gazebo_ros_spawner_cmd = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=[
            '-name', 'wheelchair',
            '-file', '/home/robot/beka_gau/src/wheelchair_description/urdf/wheelchair.urdf',
            '-x', x_pose,
            '-y', y_pose,
            '-z', '0.06',
            '-Y', '3.141'
        ],
        output='screen',
    )

    # Create the launch description
    ld = LaunchDescription()

    # Add actions
    ld.add_action(declare_x_position_cmd)
    ld.add_action(declare_y_position_cmd)
    ld.add_action(start_gazebo_ros_bridge_cmd)
    ld.add_action(start_gazebo_ros_image_bridge_cmd)
    ld.add_action(start_gazebo_ros_spawner_cmd)
    

    return ld

