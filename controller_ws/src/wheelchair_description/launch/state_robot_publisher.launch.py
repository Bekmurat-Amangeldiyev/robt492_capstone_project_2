import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from ament_index_python import get_package_prefix

def generate_launch_description():
    # Path to the URDF file
    
    urdf_file_path = os.path.join(
        get_package_share_directory('wheelchair_description'),  # Adjust package name as necessary
        'urdf',
        'wheelchair.urdf'
    )

    # Use simulation time configuration
    use_sim_time = LaunchConfiguration('use_sim_time', default='false')

    # Declare launch argument for simulation time
    declare_use_sim_time_cmd = DeclareLaunchArgument(
        'use_sim_time',
        default_value='false',
        description='Use simulation time if true'
    )

    # Read the URDF file content
    with open(urdf_file_path, 'r') as urdf_file:
        robot_description_content = urdf_file.read()

    # Node to publish the robot state
    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{
            'use_sim_time': use_sim_time,
            'robot_description': robot_description_content
        }],
    )

    # Create the launch description
    ld = LaunchDescription()

    # Add declared launch argument
    ld.add_action(declare_use_sim_time_cmd)

    # Add the robot state publisher node
    ld.add_action(robot_state_publisher_node)

    return ld

