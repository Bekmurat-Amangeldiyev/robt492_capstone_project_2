import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node, PushRosNamespace

def generate_launch_description():
    # Launch arguments
    namespace = LaunchConfiguration('namespace', default='demo')
    use_sim_time = LaunchConfiguration('use_sim_time', default='true')

    # Package directories and file paths
    pkg_nav2_bringup = get_package_share_directory('nav2_bringup')
    pkg_wheelchair = get_package_share_directory('wheelchair_description')

    nav2_params_file = os.path.join(pkg_wheelchair, 'config', 'nav2_params.yaml')
    ekf_params_file = os.path.join(pkg_wheelchair, 'config', 'ekf_localization.yaml')
    diff_drive_params_file = os.path.join(pkg_wheelchair, 'config', 'diff_drive_controller.yaml')

    # Include Nav2 bringup launch file with an empty 'map' argument
    nav2_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(pkg_nav2_bringup, 'launch', 'bringup_launch.py')),
        launch_arguments={
            'namespace': namespace,
            'use_sim_time': use_sim_time,
            'params_file': nav2_params_file,
            'slam': 'False',
            'autostart': 'True',
            'map': ''
        }.items()
    )

    # cmd_vel republisher node: relays /cmd_vel (Nav2) to the controller's expected topic
    cmd_vel_republisher = Node(
        package='wheelchair_description',
        executable='cmd_vel_republisher',
        name='cmd_vel_republisher',
        namespace=namespace,
        output='screen'
    )

    return LaunchDescription([
        DeclareLaunchArgument('namespace', default_value='demo', description='Robot namespace'),
        DeclareLaunchArgument('use_sim_time', default_value='true', description='Use simulation time'),
        PushRosNamespace(namespace),
        nav2_launch,
        cmd_vel_republisher
    ])

if __name__ == '__main__':
    generate_launch_description()




