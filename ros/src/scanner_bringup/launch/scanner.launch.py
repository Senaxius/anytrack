from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    ld = LaunchDescription()

    scanner_node = Node(
        package="scanner",
        executable="scan_manager"
    )

    ld.add_action(scanner_node)

    return ld