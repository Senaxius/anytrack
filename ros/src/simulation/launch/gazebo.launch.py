from ament_index_python.packages import get_package_share_directory
import os
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

from launch_ros.actions import Node
import xacro

def generate_launch_description():
    # Specify the name of the package and path to xacro file within the package
    pkg_name = 'simulation'
    # file_subpath = 'description/simulation.urdf.xacro'
    # world = '/home/ALEX/anytrack/ros/src/simulation/worlds/single_ball.world'
    # world = '/home/ALEX/anytrack/ros/src/simulation/worlds/multi_camera.world'
    # world = '/home/ALEX/anytrack/ros/src/simulation/worlds/test.world'
    # world = '/home/ALEX/anytrack/ros/src/simulation/worlds/multi_ball.world'
    world = '/home/ALEX/anytrack/ros/src/simulation/worlds/4-camera-simulation-720.world'
    # world = '/home/ALEX/anytrack/ros/src/simulation/worlds/4-camera-simulation-720-multiple-ball.world'

    # Use xacro to process the file
    # xacro_file = os.path.join(get_package_share_directory(pkg_name),file_subpath)
    # robot_description_raw = xacro.process_file(xacro_file).toxml()

    # Configure the node
    # node_robot_state_publisher = Node(
    #     package='robot_state_publisher',
    #     executable='robot_state_publisher',
    #     output='screen',
    #     parameters=[{'robot_description': robot_description_raw,
    #     'use_sim_time': True}] # add other parameters here if required
    # )

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(get_package_share_directory('gazebo_ros'), 'launch'), '/gazebo.launch.py']),
        launch_arguments={
            'world': world,
            'gui': 'false',
            # 'world': '/home/ALEX/anytrack/ros/src/simulation/worlds/calibration_simulation.xml',
        }.items()
        )

    # spawn_entity = Node(package='gazebo_ros', executable='spawn_entity.py',
    #                 arguments=['-topic', 'robot_description',
    #                             '-entity', 'my_bot'],
    #                 output='screen')

    # Run the node
    print(get_package_share_directory('gazebo_ros'))
    return LaunchDescription([
        gazebo,
        # node_robot_state_publisher,
        # spawn_entity
    ])
