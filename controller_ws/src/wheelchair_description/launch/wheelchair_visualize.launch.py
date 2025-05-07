import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

import xacro


def generate_launch_description():
    pkg_name = 'wheelchair_description'
    pkg_share = get_package_share_directory(pkg_name)

    urdf_path = 'urdf/wheelchair.urdf'
    rviz_relative_path = 'urdf/urdf.rviz'

    xacro_file = os.path.join(pkg_share, urdf_path)
    rviz_absolute_path = os.path.join(pkg_share, rviz_relative_path)

    # Process xacro file
    robot_description_content = xacro.process_file(xacro_file).toxml()
    print("Processing URDF file:", xacro_file)
    print("Generated robot description content:", robot_description_content)
    return LaunchDescription([
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            output='screen',
            parameters=[{'robot_description': robot_description_content}]
        ),
        Node(
            package='joint_state_publisher_gui',
            executable='joint_state_publisher_gui',
            name='joint_state_publisher_gui',
        ),
        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            arguments=['-d', rviz_absolute_path]
        ),
    ])

