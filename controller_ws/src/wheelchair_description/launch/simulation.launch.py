import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from ament_index_python import get_package_prefix
from launch_ros.actions import Node

def generate_launch_description():
    # Get the directories for necessary packages
    pkg_ros_gz_sim = get_package_share_directory('ros_gz_sim')
    wheelchair_description_dir = get_package_share_directory('wheelchair_description')  # Adjust package name as necessary
    print(wheelchair_description_dir)


    # Launch configurations
    use_sim_time = LaunchConfiguration('use_sim_time', default='true')
    x_pose = LaunchConfiguration('x_pose', default='12.0')
    y_pose = LaunchConfiguration('y_pose', default='0.0')
    yaw_pose = LaunchConfiguration('pitch', default='1.57')


    # Path to the empty world file
    world_file_path = os.path.join(
        wheelchair_description_dir,
        'meshes',
        'worlds',
        'empty_world.world'  # Adjust this path if your Gazebo package has a custom world file
    )
    world = LaunchConfiguration('world')
    world_arg = DeclareLaunchArgument('world', default_value=world_file_path, description='World to load')
    # Include Gazebo server launch
    gzserver_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_ros_gz_sim, 'launch', 'gz_sim.launch.py')
        ),
        launch_arguments={'gz_args':['-r ',world],'on_exit_shutdown': 'true'}.items()
    )
    gzclient_cmd = IncludeLaunchDescription(
    	PythonLaunchDescriptionSource(
        	os.path.join(pkg_ros_gz_sim, 'launch', 'gz_sim.launch.py')
    	),
    	launch_arguments={'gz_args': '-g '}.items()
    )
    if 'GAZEBO_MODEL_PATH' in os.environ:
      os.environ['GAZEBO_MODEL_PATH'] += wheelchair_description_dir
    else:
      os.environ['GAZEBO_MODEL_PATH'] =  wheelchair_description_dir
    # Launch configuration variables
    x_pose = LaunchConfiguration('x_pose', default='12.0')
    y_pose = LaunchConfiguration('y_pose', default='0.0')
    
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
    

    bridge_params = os.path.join(get_package_share_directory('wheelchair_description'),'config','gz_bridge.yaml')
    ros_gz_bridge = Node(
        package="ros_gz_bridge",
        executable="parameter_bridge",
        arguments=[
            '--ros-args',
            '-p',
            f'config_file:={bridge_params}',
        ]
    )

    ros_gz_image_bridge = Node(
        package="ros_gz_image",
        executable="image_bridge",
        arguments=["/camera/image_raw"]
    )
    # Create the launch description
    # Add actions
   

    # Include robot_state_publisher.launch.py
    robot_state_publisher_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(wheelchair_description_dir, 'launch', 'state_robot_publisher.launch.py')
        ),
        launch_arguments={'use_sim_time': use_sim_time}.items()
    )

    rviz_launch_cmd = IncludeLaunchDescription(PythonLaunchDescriptionSource(os.path.join(wheelchair_description_dir,'launch','wheelchair_visualize.launch.py')))
    # Create the launch description
    ld = LaunchDescription()

    # Add actions to the launch description
    ld.add_action(world_arg)
    ld.add_action(gzserver_cmd)
    ld.add_action(gzclient_cmd)
    ld.add_action(robot_state_publisher_cmd)
    ld.add_action(rviz_launch_cmd)
    ld.add_action(ros_gz_bridge)
    ld.add_action(ros_gz_image_bridge)
    
    return ld

