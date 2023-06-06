import rclpy
from rclpy.node import Node
import time
import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription, LaunchService
from launch_ros.actions import Node as Action
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

class manager(Node): 
    def __init__(self):
        super().__init__("manager") 
        # declare manager parameters
        self.declare_parameter("websocket", 0)
        self.declare_parameter("gazebo", 0)
        self.declare_parameter("simulation", 0)
        self.declare_parameter("simulation_publisher", 0)
        self.declare_parameter("ball_count", 1)
        self.declare_parameter("config_path", '/home/ALEX/anytrack/config/camera_positions.json')
        self.declare_parameter("device_count", 0)
        self.declare_parameter("image_vis", 0)
        self.declare_parameter("vector", 1)
        self.declare_parameter("filter", 1)
        self.declare_parameter("estimator", 1)
        self.declare_parameter("width", 1280)
        self.declare_parameter("height", 720)
        self.declare_parameter("debug", 0)

        # import parameters
        self.websocket = self.get_parameter("websocket").value
        self.gazebo = self.get_parameter("gazebo").value
        self.simulation = self.get_parameter("simulation").value
        self.simulation_publisher = self.get_parameter("simulation_publisher").value
        self.ball_count = self.get_parameter("ball_count").value
        self.config_path = self.get_parameter("config_path").value
        self.device_count = self.get_parameter("device_count").value
        self.image_vis= self.get_parameter("image_vis").value
        self.vector = self.get_parameter("vector").value
        self.filter = self.get_parameter("filter").value
        self.estimator = self.get_parameter("estimator").value
        self.width = self.get_parameter("width").value
        self.height = self.get_parameter("height").value
        self.debug = self.get_parameter("debug").value

        self.get_logger().info("Starting manager...")

        self.get_logger().info("Searching for devices...")
        if self.device_count == 0:
            self.devices = self.search_devices()
            if not self.devices:
                self.get_logger().warning("No cameras were detected!")
                exit()
        else:
            self.devices = []
            for i in range(self.device_count):
                self.devices.append(i)
        self.get_logger().info("Found Number of Devices: " + str(len(self.devices)))

        ls = LaunchService()
        ls.include_launch_description(self.generate_launch_description())
        ls.run()

    def search_devices(self):
        buffer = []
        stream = os.popen('ls /dev/ | grep video')
        output = stream.read()
        if (output == ''):
            self.devices = []
            return
        output = output.strip()
        output = output.replace("video", '')
        output = output.replace("\n", ',')
        untested_devices = output.split(',')

        for index in untested_devices:
            command = "v4l2-ctl -d /dev/video" + index + " -D | grep 'Video Pixel Formatter'"
            stream = os.popen(command)
            output = stream.read()
            if (output != ''):
                buffer.append(int(index))
        
        return buffer

    def generate_launch_description(self):
        ld = LaunchDescription()

        count = 0
        length = len(self.devices)

        for cam in self.devices:
            device = cam
            index = count
            count += 1

            camX_driver = Action(
                package="anytrack",
                executable="camera_driver",
                name=('camera_driver'),
                namespace= ('cam' + str(index)),
                parameters=[
                    {"index": index},
                    {"device": device},
                    {"debug": self.debug},
                    {"framerate": 30},
                    {"width": self.width},
                    {"height": self.height},
                    {"filter": self.filter},
                ]
            )

            camX_detector = Action(
                package="anytrack",
                executable="camera_detector",
                name=('camera_detector'),
                namespace= ('cam' + str(index)),
                parameters=[
                    {"index": index},
                    {"visualize": self.image_vis},
                    {"debug": self.debug},
                    {"width": self.width},
                    {"height": self.height},
                ]
            )
            camX_camera_info = Action(
                package="anytrack",
                executable="camera_info",
                name=('camera_info'),
                namespace= ('cam' + str(index)),
                parameters=[
                    {"index": index},
                    {"device": device},
                    {"width": self.width},
                    {"height": self.height},
                ]
            )
            camX_vector= Action(
                package="anytrack",
                executable="camera_vector",
                name=('vector'),
                namespace= ('cam' + str(index)),
                parameters=[
                    {"index": index},
                    {"device": device},
                    {"multiplier": 10},
                    {"width": self.width},
                    {"height": self.height},
                ]
            )

            if self.simulation == 0:
                ld.add_action(camX_driver)
                ld.add_action(camX_camera_info)
            ld.add_action(camX_detector)
            if self.vector == 1:
                ld.add_action(camX_vector)

        position_manager = Action(
            package="anytrack",
            executable="position_manager",
            name=('position_manager'),
            parameters=[
                {"device_count": length},
                {"config_path": self.config_path}
            ]
        )
        object_estimator = Action(
            package="anytrack",
            executable="object_estimator",
            name=('object_estimator'),
            parameters=[
                {"device_count": length},
            ]
        )
        gazebo = IncludeLaunchDescription(
            PythonLaunchDescriptionSource([os.path.join(get_package_share_directory('simulation'), 'launch'), '/gazebo.launch.py']),
            )
        simulation_publisher = Action(
            package="anytrack",
            executable="simulation_publisher",
            name=('simulation_publisher'),
            parameters=[
                {"ball_count": self.ball_count},
            ]
        )
        websocket = Action(
            package="foxglove_bridge",
            executable="foxglove_bridge",
            name=('foxglove_bridge'),
        )

        if self.gazebo == 1:
            ld.add_action(gazebo)
        if self.estimator == 1:
            ld.add_action(object_estimator)
        if self.simulation_publisher == 1:
            ld.add_action(simulation_publisher)
        if self.websocket == 1:
            ld.add_action(websocket)
        ld.add_action(position_manager)
        return ld

def main(args=None):
    rclpy.init(args=args)
    node = manager()
    rclpy.spin(node)
    rclpy.shutdown()
 
if __name__ == "__main__":
    main()
